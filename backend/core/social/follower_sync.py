"""Follower sync logic.

This module provides a 'safe' implementation of unfollower detection:
- Only runs identity-level unfollower detection when the platform supports an
  official followers list endpoint.
- For other platforms, use MetricsSnapshot followers_count time-series.

Currently implemented:
- X (Twitter) followers list snapshot + diff -> FollowerChange rows.

Docs referenced:
- X followers endpoint: https://docs.x.com/x-api/users/get-followers
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

from django.core.cache import cache
from django.db import transaction

from core.social.models import FollowerChange, OAuthToken, SocialAccount
from core.utils.crypto import maybe_decrypt
from core.social.x_api import get_x_followers_page, XApiError


@dataclass
class SyncResult:
    platform: str
    account_id: str
    fetched_users: int
    new_followers: int
    unfollowers: int


def _followers_cache_key(account_id: str) -> str:
    return f"followers:{account_id}"


def _user_cache_key(platform: str, user_id: str) -> str:
    return f"user:{platform}:{user_id}"


def _extract_user(user: Dict[str, Any]) -> Dict[str, Any]:
    public_metrics = user.get("public_metrics") or {}
    return {
        "id": str(user.get("id") or ""),
        "username": user.get("username") or "",
        "profile_image_url": user.get("profile_image_url"),
        "verified": bool(user.get("verified", False)),
        "followers_count": public_metrics.get("followers_count"),
        "raw": user,
    }


def sync_x_followers_snapshot(
    *,
    social_account_id: str,
    max_pages: int = 50,
    page_size: int = 1000,
    cache_user_ttl_seconds: int = 86400 * 30,
) -> SyncResult:
    account = SocialAccount.objects.select_related("oauth_token").get(id=social_account_id)
    if account.platform != SocialAccount.PLATFORM_X:
        raise ValueError("sync_x_followers_snapshot can only run for X accounts")

    # Resolve token (plain in dev; decrypt if Fernet-like and ENCRYPTION_KEY set)
    token_row: OAuthToken = account.oauth_token
    access_token = maybe_decrypt(token_row.access_token_enc)
    if not access_token:
        raise ValueError("Missing access token for X account")

    # Fetch full follower list (paged)
    all_users: List[Dict[str, Any]] = []
    next_token: Optional[str] = None

    for _ in range(max_pages):
        page = get_x_followers_page(
            platform_user_id=account.platform_user_id,
            access_token=access_token,
            pagination_token=next_token,
            max_results=page_size,
        )
        all_users.extend(page.users)
        next_token = page.next_token
        if not next_token:
            break

    current_ids: Set[str] = set()
    current_map: Dict[str, Dict[str, Any]] = {}

    for u in all_users:
        eu = _extract_user(u)
        if not eu["id"]:
            continue
        current_ids.add(eu["id"])
        current_map[eu["id"]] = eu

    prev_ids: Set[str] = cache.get(_followers_cache_key(str(account.id)), set()) or set()

    new_ids = current_ids - prev_ids
    unfollow_ids = prev_ids - current_ids

    # Persist changes; keep it idempotent-ish by not creating duplicates in tight loops.
    with transaction.atomic():
        # New followers
        new_changes: List[FollowerChange] = []
        for uid in new_ids:
            info = current_map.get(uid) or {}
            new_changes.append(
                FollowerChange(
                    social_account=account,
                    change_type=FollowerChange.TYPE_NEW_FOLLOWER,
                    user_id=uid,
                    username=info.get("username", ""),
                    profile_pic_url=info.get("profile_image_url"),
                    verified=bool(info.get("verified", False)),
                    follower_count=info.get("followers_count"),
                    extra_data={"platform": "x"},
                )
            )

        if new_changes:
            FollowerChange.objects.bulk_create(new_changes, ignore_conflicts=True)

        # Unfollowers: best effort enrichment from cache
        unf_changes: List[FollowerChange] = []
        for uid in unfollow_ids:
            cached = cache.get(_user_cache_key("x", uid), {}) or {}
            unf_changes.append(
                FollowerChange(
                    social_account=account,
                    change_type=FollowerChange.TYPE_UNFOLLOWER,
                    user_id=uid,
                    username=cached.get("username", ""),
                    profile_pic_url=cached.get("profile_image_url"),
                    verified=bool(cached.get("verified", False)),
                    follower_count=cached.get("followers_count"),
                    extra_data={"platform": "x"},
                )
            )

        if unf_changes:
            FollowerChange.objects.bulk_create(unf_changes, ignore_conflicts=True)

    # Cache follower set snapshot
    cache.set(_followers_cache_key(str(account.id)), current_ids, timeout=None)

    # Cache per-user enrichment (only for currently visible followers)
    for uid, info in current_map.items():
        cache.set(_user_cache_key("x", uid), info, timeout=cache_user_ttl_seconds)

    return SyncResult(
        platform="x",
        account_id=str(account.id),
        fetched_users=len(current_map),
        new_followers=len(new_ids),
        unfollowers=len(unfollow_ids),
    )

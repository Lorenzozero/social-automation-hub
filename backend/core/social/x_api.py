"""X (Twitter) API v2 client utilities used for analytics.

Implements the official followers list endpoint:
GET https://api.x.com/2/users/{id}/followers

Docs: https://docs.x.com/x-api/users/get-followers
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


@dataclass
class XFollowersPage:
    users: List[Dict[str, Any]]
    next_token: Optional[str]


class XApiError(RuntimeError):
    pass


def get_x_followers_page(
    *,
    platform_user_id: str,
    access_token: str,
    pagination_token: Optional[str] = None,
    max_results: int = 1000,
    timeout: int = 30,
) -> XFollowersPage:
    url = f"https://api.x.com/2/users/{platform_user_id}/followers"

    params: Dict[str, Any] = {
        "max_results": max_results,
        "user.fields": "profile_image_url,verified,public_metrics",
    }
    if pagination_token:
        params["pagination_token"] = pagination_token

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    r = requests.get(url, params=params, headers=headers, timeout=timeout)

    if r.status_code == 429:
        raise XApiError("X rate limit exceeded (HTTP 429)")

    if r.status_code >= 400:
        try:
            payload = r.json()
        except Exception:
            payload = {"text": r.text}
        raise XApiError(f"X API error {r.status_code}: {payload}")

    data = r.json() or {}
    users = data.get("data", []) or []
    meta = data.get("meta", {}) or {}
    next_token = meta.get("next_token")

    return XFollowersPage(users=users, next_token=next_token)

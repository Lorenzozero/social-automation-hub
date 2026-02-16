from celery import shared_task
from django.utils import timezone
from datetime import timedelta, datetime
import logging

from core.social.models import (
    SocialAccount,
    MetricsSnapshot,
    FollowerChange,
    TopContent,
    AudienceInsight,
)
from core.social.views.oauth import decrypt_token
from core.social.platform_apis import InstagramAPI, TikTokAPI, LinkedInAPI, XAPI

logger = logging.getLogger(__name__)


@shared_task
def sync_all_accounts_metrics():
    """Periodic task: sync metrics for all active accounts. Runs every 15 minutes."""
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            sync_account_metrics.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue metrics sync for {account}: {e}")


@shared_task
def sync_account_metrics(account_id):
    """Fetch and save current metrics for a single account."""
    try:
        account = SocialAccount.objects.get(id=account_id)
        token = decrypt_token(account.oauth_token.access_token_enc)

        metrics = {}

        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            api = InstagramAPI(token)
            profile = api.get_user_profile(account.platform_user_id)
            insights = api.get_user_insights(
                account.platform_user_id,
                metrics=["reach", "impressions", "profile_views"],
                period="day",
            )

            # Parse insights data
            insights_data = insights.get("data", [])
            reach = next((m["values"][0]["value"] for m in insights_data if m["name"] == "reach"), 0)
            impressions = next((m["values"][0]["value"] for m in insights_data if m["name"] == "impressions"), 0)
            profile_views = next((m["values"][0]["value"] for m in insights_data if m["name"] == "profile_views"), 0)

            metrics = {
                "followers": profile.get("followers_count", 0),
                "following": profile.get("follows_count", 0),
                "posts": profile.get("media_count", 0),
                "reach": reach,
                "impressions": impressions,
                "engagement": 0,  # Calculate from posts
                "profile_views": profile_views,
            }

        elif account.platform == SocialAccount.PLATFORM_TIKTOK:
            api = TikTokAPI(token)
            user_info = api.get_user_info()

            metrics = {
                "followers": user_info.get("follower_count", 0),
                "following": user_info.get("following_count", 0),
                "posts": user_info.get("video_count", 0),
                "reach": 0,  # TikTok doesn't provide real-time reach easily
                "impressions": 0,
                "engagement": 0,
                "profile_views": 0,
            }

        elif account.platform == SocialAccount.PLATFORM_LINKEDIN:
            api = LinkedInAPI(token)
            profile = api.get_user_profile()

            # LinkedIn metrics are limited for personal profiles
            metrics = {
                "followers": 0,  # Requires organization context
                "following": 0,
                "posts": 0,
                "reach": 0,
                "impressions": 0,
                "engagement": 0,
                "profile_views": 0,
            }

        elif account.platform == SocialAccount.PLATFORM_X:
            api = XAPI(token)
            user_metrics = api.get_user_metrics(account.platform_user_id)

            metrics = {
                "followers": user_metrics.get("followers_count", 0),
                "following": user_metrics.get("following_count", 0),
                "posts": user_metrics.get("tweet_count", 0),
                "reach": 0,  # X doesn't provide easy reach metrics
                "impressions": 0,
                "engagement": 0,
                "profile_views": 0,
            }

        # Save snapshot
        MetricsSnapshot.objects.create(
            social_account=account,
            followers_count=metrics.get("followers", 0),
            following_count=metrics.get("following", 0),
            posts_count=metrics.get("posts", 0),
            reach=metrics.get("reach", 0),
            impressions=metrics.get("impressions", 0),
            engagement_count=metrics.get("engagement", 0),
            profile_views=metrics.get("profile_views", 0),
            extra_data=metrics.get("extra", {}),
        )

        logger.info(f"Synced metrics for {account}: {metrics['followers']} followers")

    except Exception as e:
        logger.error(f"Failed to sync metrics for account {account_id}: {e}")


@shared_task
def detect_all_follower_changes():
    """Periodic task: detect follower changes for all active accounts. Runs every 30 minutes."""
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            detect_follower_changes.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue follower detection for {account}: {e}")


@shared_task
def detect_follower_changes(account_id):
    """Compare current followers with previous snapshot to detect new/unfollowers."""
    try:
        account = SocialAccount.objects.get(id=account_id)

        # Get current and previous follower counts
        snapshots = MetricsSnapshot.objects.filter(social_account=account).order_by("-timestamp")[:2]

        if len(snapshots) < 2:
            logger.info(f"Not enough snapshots for {account}, skipping follower detection")
            return

        current = snapshots[0]
        previous = snapshots[1]

        follower_diff = current.followers_count - previous.followers_count

        if follower_diff > 0:
            # New followers detected
            for i in range(follower_diff):
                FollowerChange.objects.create(
                    social_account=account,
                    change_type=FollowerChange.TYPE_NEW_FOLLOWER,
                    user_id=f"unknown_{i}",  # Real implementation would fetch actual user IDs
                    username=f"new_follower_{i}",
                    timestamp=timezone.now(),
                )
            logger.info(f"Detected {follower_diff} new followers for {account}")

        elif follower_diff < 0:
            # Unfollowers detected
            for i in range(abs(follower_diff)):
                FollowerChange.objects.create(
                    social_account=account,
                    change_type=FollowerChange.TYPE_UNFOLLOWER,
                    user_id=f"unknown_{i}",
                    username=f"unfollower_{i}",
                    timestamp=timezone.now(),
                )
            logger.info(f"Detected {abs(follower_diff)} unfollowers for {account}")

    except Exception as e:
        logger.error(f"Failed to detect follower changes for account {account_id}: {e}")


@shared_task
def update_all_top_content():
    """Periodic task: update top content for all active accounts. Runs daily at 2 AM."""
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            update_top_content.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue top content update for {account}: {e}")


@shared_task
def update_top_content(account_id):
    """Fetch recent posts and update performance metrics."""
    try:
        account = SocialAccount.objects.get(id=account_id)
        token = decrypt_token(account.oauth_token.access_token_enc)

        posts = []

        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            api = InstagramAPI(token)
            media_list = api.get_media_list(account.platform_user_id, limit=50)

            for media in media_list:
                try:
                    insights = api.get_media_insights(
                        media["id"],
                        metrics=["reach", "saved", "shares"] if media["media_type"] != "VIDEO" else ["reach", "saved"],
                    )
                    insights_data = insights.get("data", [])
                    reach = next((m["values"][0]["value"] for m in insights_data if m["name"] == "reach"), 0)
                    saved = next((m["values"][0]["value"] for m in insights_data if m["name"] == "saved"), 0)

                    posts.append({
                        "id": media["id"],
                        "url": media.get("permalink", ""),
                        "caption": media.get("caption", ""),
                        "media_type": media.get("media_type", "").lower(),
                        "likes": media.get("like_count", 0),
                        "comments": media.get("comments_count", 0),
                        "shares": 0,
                        "saves": saved,
                        "reach": reach,
                        "posted_at": datetime.fromisoformat(media["timestamp"].replace("Z", "+00:00")),
                    })
                except Exception as e:
                    logger.warning(f"Failed to get insights for media {media['id']}: {e}")

        elif account.platform == SocialAccount.PLATFORM_TIKTOK:
            api = TikTokAPI(token)
            videos = api.list_videos(max_count=20)

            for video in videos:
                posts.append({
                    "id": video.get("id", ""),
                    "url": video.get("share_url", ""),
                    "caption": video.get("title", ""),
                    "media_type": "video",
                    "likes": video.get("like_count", 0),
                    "comments": video.get("comment_count", 0),
                    "shares": video.get("share_count", 0),
                    "saves": 0,
                    "reach": video.get("view_count", 0),
                    "posted_at": datetime.fromtimestamp(video.get("create_time", 0)),
                })

        elif account.platform == SocialAccount.PLATFORM_X:
            api = XAPI(token)
            tweets = api.get_user_tweets(account.platform_user_id, max_results=50)

            for tweet in tweets:
                metrics = tweet.get("public_metrics", {})
                posts.append({
                    "id": tweet["id"],
                    "url": f"https://x.com/{account.handle}/status/{tweet['id']}",
                    "caption": tweet.get("text", ""),
                    "media_type": "tweet",
                    "likes": metrics.get("like_count", 0),
                    "comments": metrics.get("reply_count", 0),
                    "shares": metrics.get("retweet_count", 0),
                    "saves": metrics.get("bookmark_count", 0),
                    "reach": metrics.get("impression_count", 0),
                    "posted_at": datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00")),
                })

        # Update or create TopContent records
        for post in posts:
            engagement_rate = calculate_engagement_rate(post)
            TopContent.objects.update_or_create(
                social_account=account,
                platform_post_id=post["id"],
                defaults={
                    "post_url": post["url"],
                    "caption": post.get("caption", "")[:500],
                    "media_type": post.get("media_type", ""),
                    "likes_count": post.get("likes", 0),
                    "comments_count": post.get("comments", 0),
                    "shares_count": post.get("shares", 0),
                    "saves_count": post.get("saves", 0),
                    "reach": post.get("reach", 0),
                    "engagement_rate": engagement_rate,
                    "posted_at": post.get("posted_at"),
                },
            )

        logger.info(f"Updated {len(posts)} posts for {account}")

    except Exception as e:
        logger.error(f"Failed to update top content for account {account_id}: {e}")


@shared_task
def fetch_all_audience_insights():
    """Periodic task: fetch audience insights for all active accounts. Runs weekly on Monday at 3 AM."""
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            fetch_audience_insights.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue audience insights for {account}: {e}")


@shared_task
def fetch_audience_insights(account_id):
    """Fetch audience demographics and activity patterns."""
    try:
        account = SocialAccount.objects.get(id=account_id)
        token = decrypt_token(account.oauth_token.access_token_enc)

        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            api = InstagramAPI(token)
            insights = api.get_audience_insights(account.platform_user_id)

            # Parse demographics from insights
            insights_data = insights.get("data", [])

            age_gender = next((m for m in insights_data if m["name"] == "audience_gender_age"), {})
            cities = next((m for m in insights_data if m["name"] == "audience_city"), {})
            countries = next((m for m in insights_data if m["name"] == "audience_country"), {})

            AudienceInsight.objects.update_or_create(
                social_account=account,
                snapshot_date=timezone.now().date(),
                defaults={
                    "age_ranges": parse_age_gender_data(age_gender),
                    "genders": parse_gender_data(age_gender),
                    "cities": parse_location_data(cities),
                    "countries": parse_location_data(countries),
                    "active_hours": [],  # Requires additional API calls
                    "active_days": [],
                },
            )

            logger.info(f"Fetched audience insights for {account}")

    except Exception as e:
        logger.error(f"Failed to fetch audience insights for account {account_id}: {e}")


# Helper functions

def calculate_engagement_rate(post: dict) -> float:
    """Calculate engagement rate: (likes + comments + shares + saves) / reach * 100."""
    total_engagement = (
        post.get("likes", 0)
        + post.get("comments", 0)
        + post.get("shares", 0)
        + post.get("saves", 0)
    )
    reach = post.get("reach", 1)
    return round((total_engagement / reach) * 100, 2) if reach > 0 else 0.0


def parse_age_gender_data(data: dict) -> list:
    """Parse Instagram age/gender insights into age ranges."""
    # Simplified parser - real implementation depends on API response structure
    values = data.get("values", [{}])[0].get("value", {})
    age_ranges = []
    for key, count in values.items():
        if key.startswith(("M", "F", "U")):
            age_range = key[2:]  # Remove gender prefix
            if age_range not in [r["range"] for r in age_ranges]:
                age_ranges.append({"range": age_range, "count": count})
    return age_ranges


def parse_gender_data(data: dict) -> list:
    """Parse Instagram age/gender insights into gender breakdown."""
    values = data.get("values", [{}])[0].get("value", {})
    genders = {"male": 0, "female": 0, "unknown": 0}
    for key, count in values.items():
        if key.startswith("M"):
            genders["male"] += count
        elif key.startswith("F"):
            genders["female"] += count
        elif key.startswith("U"):
            genders["unknown"] += count
    return [{"gender": k, "count": v} for k, v in genders.items() if v > 0]


def parse_location_data(data: dict) -> list:
    """Parse Instagram location insights."""
    values = data.get("values", [{}])[0].get("value", {})
    return [{"location": k, "count": v} for k, v in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]]

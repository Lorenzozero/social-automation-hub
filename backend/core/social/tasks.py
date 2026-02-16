from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from core.social.models import SocialAccount, MetricsSnapshot, FollowerChange, TopContent
from core.social.views.oauth import decrypt_token

logger = logging.getLogger(__name__)


@shared_task
def sync_all_accounts_metrics():
    """
    Periodic task: sync metrics for all active accounts.
    Runs every 15 minutes.
    """
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            sync_account_metrics.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue metrics sync for {account}: {e}")


@shared_task
def sync_account_metrics(account_id):
    """
    Fetch and save current metrics for a single account.
    TODO: Implement platform-specific API calls.
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
        token = decrypt_token(account.oauth_token.access_token_enc)
        
        # Platform-specific API calls
        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            metrics = fetch_instagram_metrics(account.platform_user_id, token)
        elif account.platform == SocialAccount.PLATFORM_TIKTOK:
            metrics = fetch_tiktok_metrics(account.platform_user_id, token)
        elif account.platform == SocialAccount.PLATFORM_LINKEDIN:
            metrics = fetch_linkedin_metrics(account.platform_user_id, token)
        elif account.platform == SocialAccount.PLATFORM_X:
            metrics = fetch_x_metrics(account.platform_user_id, token)
        else:
            logger.warning(f"Unknown platform: {account.platform}")
            return
        
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
        
        logger.info(f"Synced metrics for {account}")
        
    except Exception as e:
        logger.error(f"Failed to sync metrics for account {account_id}: {e}")


@shared_task
def detect_all_follower_changes():
    """
    Periodic task: detect follower changes for all active accounts.
    Runs every 30 minutes.
    """
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            detect_follower_changes.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue follower detection for {account}: {e}")


@shared_task
def detect_follower_changes(account_id):
    """
    Compare current followers with previous snapshot to detect new/unfollowers.
    TODO: Implement platform-specific follower list APIs.
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
        token = decrypt_token(account.oauth_token.access_token_enc)
        
        # Get current follower list from platform
        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            current_followers = fetch_instagram_followers(account.platform_user_id, token)
        # ... other platforms
        else:
            logger.warning(f"Follower detection not implemented for {account.platform}")
            return
        
        # Get previous follower list (stored in cache or DB)
        # Compare and create FollowerChange records
        # This is a simplified example - production needs proper caching
        
        logger.info(f"Detected follower changes for {account}")
        
    except Exception as e:
        logger.error(f"Failed to detect follower changes for account {account_id}: {e}")


@shared_task
def update_all_top_content():
    """
    Periodic task: update top content for all active accounts.
    Runs daily at 2 AM.
    """
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            update_top_content.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue top content update for {account}: {e}")


@shared_task
def update_top_content(account_id):
    """
    Fetch recent posts and update performance metrics.
    TODO: Implement platform-specific post APIs.
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
        token = decrypt_token(account.oauth_token.access_token_enc)
        
        # Fetch recent posts with metrics
        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            posts = fetch_instagram_posts(account.platform_user_id, token, limit=50)
        # ... other platforms
        else:
            logger.warning(f"Top content not implemented for {account.platform}")
            return
        
        # Update or create TopContent records
        for post in posts:
            TopContent.objects.update_or_create(
                social_account=account,
                platform_post_id=post["id"],
                defaults={
                    "post_url": post["url"],
                    "caption": post.get("caption", ""),
                    "media_type": post.get("media_type", ""),
                    "likes_count": post.get("likes", 0),
                    "comments_count": post.get("comments", 0),
                    "shares_count": post.get("shares", 0),
                    "saves_count": post.get("saves", 0),
                    "reach": post.get("reach", 0),
                    "engagement_rate": calculate_engagement_rate(post),
                    "posted_at": post.get("posted_at"),
                },
            )
        
        logger.info(f"Updated top content for {account}")
        
    except Exception as e:
        logger.error(f"Failed to update top content for account {account_id}: {e}")


@shared_task
def fetch_all_audience_insights():
    """
    Periodic task: fetch audience insights for all active accounts.
    Runs weekly on Monday at 3 AM.
    """
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            fetch_audience_insights.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue audience insights for {account}: {e}")


@shared_task
def fetch_audience_insights(account_id):
    """
    Fetch audience demographics and activity patterns.
    TODO: Implement platform-specific insights APIs.
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
        # Implementation depends on platform API availability
        logger.info(f"Fetched audience insights for {account}")
    except Exception as e:
        logger.error(f"Failed to fetch audience insights for account {account_id}: {e}")


# Placeholder functions - implement with actual platform APIs

def fetch_instagram_metrics(user_id, token):
    # TODO: Call Instagram Graph API
    return {"followers": 0, "reach": 0, "impressions": 0, "engagement": 0}

def fetch_tiktok_metrics(user_id, token):
    # TODO: Call TikTok API
    return {"followers": 0, "reach": 0, "impressions": 0, "engagement": 0}

def fetch_linkedin_metrics(user_id, token):
    # TODO: Call LinkedIn API
    return {"followers": 0, "reach": 0, "impressions": 0, "engagement": 0}

def fetch_x_metrics(user_id, token):
    # TODO: Call X API
    return {"followers": 0, "reach": 0, "impressions": 0, "engagement": 0}

def fetch_instagram_followers(user_id, token):
    # TODO: Call Instagram Graph API
    return []

def fetch_instagram_posts(user_id, token, limit=50):
    # TODO: Call Instagram Graph API
    return []

def calculate_engagement_rate(post):
    # (likes + comments + shares + saves) / reach * 100
    total_engagement = post.get("likes", 0) + post.get("comments", 0) + post.get("shares", 0) + post.get("saves", 0)
    reach = post.get("reach", 1)
    return round((total_engagement / reach) * 100, 2)

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from core.social.models import (
    SocialAccount, MetricsSnapshot, FollowerChange, TopContent, AudienceInsight
)
from core.social.views.oauth import decrypt_token
from core.social.api_clients import (
    InstagramAPIClient, TikTokAPIClient, LinkedInAPIClient, XAPIClient
)

logger = logging.getLogger(__name__)


@shared_task
def sync_all_accounts_metrics():
    """Sync metrics for all active accounts."""
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
        
        # Fetch metrics based on platform
        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            client = InstagramAPIClient(token)
            account_info = client.get_account_info(account.platform_user_id)
            insights = client.get_insights(
                account.platform_user_id,
                metrics=["reach", "impressions", "profile_views"],
                period="day"
            )
            
            metrics = {
                "followers": account_info.get("followers_count", 0),
                "following": account_info.get("follows_count", 0),
                "posts": account_info.get("media_count", 0),
                "reach": insights.get("reach", 0),
                "impressions": insights.get("impressions", 0),
                "profile_views": insights.get("profile_views", 0),
                "engagement": 0,  # Calculated from posts
            }
            
        elif account.platform == SocialAccount.PLATFORM_TIKTOK:
            client = TikTokAPIClient(token)
            user_info = client.get_user_info()
            
            metrics = {
                "followers": user_info.get("follower_count", 0),
                "following": user_info.get("following_count", 0),
                "posts": user_info.get("video_count", 0),
                "reach": 0,  # TikTok doesn't provide this in basic API
                "impressions": 0,
                "profile_views": 0,
                "engagement": 0,
            }
            
        elif account.platform == SocialAccount.PLATFORM_LINKEDIN:
            # LinkedIn API is more restricted, basic profile only
            metrics = {
                "followers": 0,  # Requires additional permissions
                "following": 0,
                "posts": 0,
                "reach": 0,
                "impressions": 0,
                "profile_views": 0,
                "engagement": 0,
            }
            
        elif account.platform == SocialAccount.PLATFORM_X:
            client = XAPIClient(token)
            user_info = client.get_me()
            public_metrics = user_info.get("public_metrics", {})
            
            metrics = {
                "followers": public_metrics.get("followers_count", 0),
                "following": public_metrics.get("following_count", 0),
                "posts": public_metrics.get("tweet_count", 0),
                "reach": 0,  # Calculated from tweets
                "impressions": 0,
                "profile_views": 0,
                "engagement": 0,
            }
        else:
            logger.warning(f"Unknown platform: {account.platform}")
            return
        
        # Save snapshot
        MetricsSnapshot.objects.create(
            social_account=account,
            followers_count=metrics["followers"],
            following_count=metrics["following"],
            posts_count=metrics["posts"],
            reach=metrics["reach"],
            impressions=metrics["impressions"],
            engagement_count=metrics["engagement"],
            profile_views=metrics["profile_views"],
        )
        
        logger.info(f"Synced metrics for {account}")
        
    except Exception as e:
        logger.error(f"Failed to sync metrics for account {account_id}: {e}")
        raise


@shared_task
def detect_all_follower_changes():
    """Detect follower changes for all active accounts."""
    accounts = SocialAccount.objects.filter(status=SocialAccount.STATUS_ACTIVE)
    for account in accounts:
        try:
            detect_follower_changes.delay(str(account.id))
        except Exception as e:
            logger.error(f"Failed to queue follower detection for {account}: {e}")


@shared_task
def detect_follower_changes(account_id):
    """Compare current followers with previous snapshot."""
    try:
        account = SocialAccount.objects.get(id=account_id)
        
        # Get current and previous follower counts
        snapshots = MetricsSnapshot.objects.filter(
            social_account=account
        ).order_by("-timestamp")[:2]
        
        if len(snapshots) < 2:
            logger.info(f"Not enough snapshots for {account}")
            return
        
        current = snapshots[0].followers_count
        previous = snapshots[1].followers_count
        delta = current - previous
        
        if delta > 0:
            # New followers detected
            logger.info(f"{account} gained {delta} followers")
            # Note: Actual follower list tracking requires webhooks or polling follower IDs
            # This is a simplified version that tracks aggregate changes
            
        elif delta < 0:
            # Unfollowers detected
            logger.info(f"{account} lost {abs(delta)} followers")
        
    except Exception as e:
        logger.error(f"Failed to detect follower changes for {account_id}: {e}")


@shared_task
def update_all_top_content():
    """Update top content for all active accounts."""
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
        
        if account.platform == SocialAccount.PLATFORM_INSTAGRAM:
            client = InstagramAPIClient(token)
            media_list = client.get_media(account.platform_user_id, limit=50)
            
            for media in media_list:
                media_id = media["id"]
                insights = client.get_media_insights(media_id)
                
                engagement = (
                    media.get("like_count", 0) + 
                    media.get("comments_count", 0)
                )
                reach = insights.get("reach", 1)
                engagement_rate = (engagement / reach * 100) if reach > 0 else 0
                
                TopContent.objects.update_or_create(
                    social_account=account,
                    platform_post_id=media_id,
                    defaults={
                        "post_url": media["permalink"],
                        "caption": media.get("caption", ""),
                        "media_type": media["media_type"].lower(),
                        "likes_count": media.get("like_count", 0),
                        "comments_count": media.get("comments_count", 0),
                        "shares_count": 0,  # Instagram doesn't expose shares
                        "saves_count": insights.get("saved", 0),
                        "reach": reach,
                        "engagement_rate": engagement_rate,
                        "posted_at": media["timestamp"],
                    },
                )
        
        elif account.platform == SocialAccount.PLATFORM_X:
            client = XAPIClient(token)
            tweets = client.get_user_tweets(account.platform_user_id, max_results=50)
            
            for tweet in tweets:
                metrics = tweet.get("public_metrics", {})
                engagement = (
                    metrics.get("like_count", 0) +
                    metrics.get("retweet_count", 0) +
                    metrics.get("reply_count", 0)
                )
                
                # X doesn't provide reach in basic API, use impressions as proxy
                impressions = metrics.get("impression_count", 1)
                engagement_rate = (engagement / impressions * 100) if impressions > 0 else 0
                
                TopContent.objects.update_or_create(
                    social_account=account,
                    platform_post_id=tweet["id"],
                    defaults={
                        "post_url": f"https://twitter.com/i/web/status/{tweet['id']}",
                        "caption": tweet["text"],
                        "media_type": "tweet",
                        "likes_count": metrics.get("like_count", 0),
                        "comments_count": metrics.get("reply_count", 0),
                        "shares_count": metrics.get("retweet_count", 0),
                        "saves_count": 0,
                        "reach": impressions,
                        "engagement_rate": engagement_rate,
                        "posted_at": tweet["created_at"],
                    },
                )
        
        logger.info(f"Updated top content for {account}")
        
    except Exception as e:
        logger.error(f"Failed to update top content for {account_id}: {e}")


@shared_task
def fetch_all_audience_insights():
    """Fetch audience insights for all active accounts."""
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
            client = InstagramAPIClient(token)
            audience_data = client.get_audience_insights(account.platform_user_id)
            
            AudienceInsight.objects.update_or_create(
                social_account=account,
                snapshot_date=timezone.now().date(),
                defaults={
                    "cities": audience_data["cities"],
                    "countries": audience_data["countries"],
                    "age_ranges": [],  # Parse from age_gender
                    "genders": [],  # Parse from age_gender
                    "active_hours": [],  # Requires additional API calls
                    "active_days": [],
                },
            )
        
        logger.info(f"Fetched audience insights for {account}")
        
    except Exception as e:
        logger.error(f"Failed to fetch audience insights for {account_id}: {e}")

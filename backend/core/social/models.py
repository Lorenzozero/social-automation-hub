import uuid
from django.db import models
from core.workspaces.models import Workspace


class SocialAccount(models.Model):
    PLATFORM_INSTAGRAM = "instagram"
    PLATFORM_TIKTOK = "tiktok"
    PLATFORM_LINKEDIN = "linkedin"
    PLATFORM_X = "x"

    PLATFORM_CHOICES = [
        (PLATFORM_INSTAGRAM, "Instagram"),
        (PLATFORM_TIKTOK, "TikTok"),
        (PLATFORM_LINKEDIN, "LinkedIn"),
        (PLATFORM_X, "X"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_NEEDS_REVIEW = "needs_review"
    STATUS_DISCONNECTED = "disconnected"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_NEEDS_REVIEW, "Needs review"),
        (STATUS_DISCONNECTED, "Disconnected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="social_accounts")
    platform = models.CharField(max_length=32, choices=PLATFORM_CHOICES)
    handle = models.CharField(max_length=255)
    platform_user_id = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEEDS_REVIEW)

    class Meta:
        db_table = "social_accounts"
        unique_together = ("workspace", "platform", "handle")

    def __str__(self) -> str:
        return f"{self.platform}:{self.handle}"


class OAuthToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_account = models.OneToOneField(SocialAccount, on_delete=models.CASCADE, related_name="oauth_token")
    access_token_enc = models.TextField()
    refresh_token_enc = models.TextField(blank=True, null=True)
    scopes = models.TextField()
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "oauth_tokens"


class MetricsSnapshot(models.Model):
    """Time-series snapshots of account metrics for trend analysis."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, related_name="metrics_snapshots")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Core metrics
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    
    # Engagement metrics (last 24h unless specified)
    reach = models.IntegerField(default=0, help_text="Unique accounts reached")
    impressions = models.IntegerField(default=0, help_text="Total views")
    engagement_count = models.IntegerField(default=0, help_text="Likes + comments + shares")
    profile_views = models.IntegerField(default=0)
    
    # Platform-specific
    extra_data = models.JSONField(default=dict, blank=True, help_text="Platform-specific metrics")

    class Meta:
        db_table = "metrics_snapshots"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["social_account", "-timestamp"]),
        ]


class FollowerChange(models.Model):
    """Track individual follower/following changes for detailed analysis."""
    TYPE_NEW_FOLLOWER = "new_follower"
    TYPE_UNFOLLOWER = "unfollower"
    TYPE_NEW_FOLLOWING = "new_following"
    TYPE_UNFOLLOWING = "unfollowing"

    TYPE_CHOICES = [
        (TYPE_NEW_FOLLOWER, "New Follower"),
        (TYPE_UNFOLLOWER, "Unfollower"),
        (TYPE_NEW_FOLLOWING, "New Following"),
        (TYPE_UNFOLLOWING, "Unfollowing"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, related_name="follower_changes")
    change_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    user_id = models.CharField(max_length=255, help_text="Platform user ID")
    username = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Enrichment data
    profile_pic_url = models.URLField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    follower_count = models.IntegerField(null=True, blank=True, help_text="Their follower count")
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "follower_changes"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["social_account", "-timestamp"]),
            models.Index(fields=["social_account", "change_type", "-timestamp"]),
        ]


class TopContent(models.Model):
    """Track top-performing posts for each account."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, related_name="top_content")
    platform_post_id = models.CharField(max_length=255)
    post_url = models.URLField()
    caption = models.TextField(blank=True)
    media_type = models.CharField(max_length=32, blank=True, help_text="photo, video, carousel, reel")
    
    # Performance metrics
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0, help_text="Percentage")
    
    posted_at = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "top_content"
        ordering = ["-engagement_rate"]
        unique_together = ("social_account", "platform_post_id")


class AudienceInsight(models.Model):
    """Audience demographics and insights per account."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, related_name="audience_insights")
    snapshot_date = models.DateField(db_index=True)
    
    # Demographics (JSON arrays with {value, count} objects)
    age_ranges = models.JSONField(default=list, help_text='[{"range": "18-24", "count": 1234}, ...]')
    genders = models.JSONField(default=list, help_text='[{"gender": "male", "count": 5000}, ...]')
    countries = models.JSONField(default=list, help_text='[{"country": "US", "count": 3000}, ...]')
    cities = models.JSONField(default=list, help_text='[{"city": "New York", "count": 800}, ...]')
    
    # Activity patterns
    active_hours = models.JSONField(default=list, help_text='[{"hour": 14, "activity": 0.85}, ...]')
    active_days = models.JSONField(default=list, help_text='[{"day": "monday", "activity": 0.92}, ...]')

    class Meta:
        db_table = "audience_insights"
        unique_together = ("social_account", "snapshot_date")
        ordering = ["-snapshot_date"]

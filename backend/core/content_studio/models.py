import uuid
from django.db import models
from core.workspaces.models import Workspace
from core.social.models import SocialAccount


class ContentBrief(models.Model):
    """User-provided brief for AI content generation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="content_briefs")
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Brief input
    topic = models.CharField(max_length=255, help_text="Main topic/subject")
    goal = models.TextField(help_text="What do you want to achieve?")
    tone = models.CharField(max_length=50, default="casual", help_text="casual, professional, funny, inspiring")
    target_audience = models.CharField(max_length=255, blank=True)
    keywords = models.JSONField(default=list, help_text="Keywords to include")
    
    # Platform targeting
    target_platforms = models.JSONField(default=list, help_text="[instagram, tiktok, linkedin, x]")
    
    class Meta:
        db_table = "content_briefs"
        ordering = ["-created_at"]


class ContentVariant(models.Model):
    """AI-generated content variant from a brief."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brief = models.ForeignKey(ContentBrief, on_delete=models.CASCADE, related_name="variants")
    platform = models.CharField(max_length=32, help_text="instagram, tiktok, linkedin, x")
    
    # Generated content
    caption = models.TextField()
    hashtags = models.JSONField(default=list, help_text="List of hashtags")
    
    # AI metadata
    model_used = models.CharField(max_length=100, help_text="openai/gpt-4, anthropic/claude-3.5-sonnet")
    generation_tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # User interaction
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = "content_variants"
        ordering = ["-created_at"]

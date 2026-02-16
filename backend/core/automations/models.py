import uuid
from django.db import models
from core.workspaces.models import Workspace


class Automation(models.Model):
    """Automation workflow with trigger and actions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="automations")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Workflow definition
    trigger = models.JSONField(help_text="Trigger configuration: {type, params}")
    actions = models.JSONField(help_text="List of actions: [{type, params}, ...]")
    
    # Compliance
    consent_required = models.BooleanField(default=False, help_text="Requires explicit user consent (e.g., X automation)")
    
    class Meta:
        db_table = "automations"
        ordering = ["-created_at"]


class AutomationRun(models.Model):
    """Execution log for automation runs."""
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_SKIPPED = "skipped"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RUNNING, "Running"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
        (STATUS_SKIPPED, "Skipped"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    automation = models.ForeignKey(Automation, on_delete=models.CASCADE, related_name="runs")
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    # Execution metadata
    triggered_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    trigger_data = models.JSONField(default=dict, help_text="Data that triggered this run")
    
    # Results
    actions_executed = models.JSONField(default=list, help_text="List of executed action results")
    error_message = models.TextField(blank=True)
    
    class Meta:
        db_table = "automation_runs"
        ordering = ["-triggered_at"]
        indexes = [
            models.Index(fields=["automation", "-triggered_at"]),
        ]


class Consent(models.Model):
    """User consent for automation (X compliance)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_account = models.ForeignKey("social.SocialAccount", on_delete=models.CASCADE, related_name="consents")
    automation = models.ForeignKey(Automation, on_delete=models.CASCADE, related_name="consents")
    granted_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "consents"
        unique_together = ("social_account", "automation")
        indexes = [
            models.Index(fields=["social_account", "automation"]),
        ]

    def is_active(self) -> bool:
        return self.revoked_at is None

import logging
from datetime import datetime, timedelta
from django.utils import timezone

from core.social.models import SocialAccount, MetricsSnapshot, FollowerChange
from core.content_studio.models import ContentBrief, ContentVariant
from core.posts.models import Post

logger = logging.getLogger(__name__)


class AutomationExecutor:
    """Execute automation workflows."""

    def __init__(self, automation):
        self.automation = automation
        self.trigger_config = automation.trigger
        self.actions_config = automation.actions

    def check_trigger(self) -> tuple[bool, dict]:
        """Check if automation should trigger. Returns (should_trigger, trigger_data)."""
        trigger_type = self.trigger_config.get("type")
        
        if trigger_type == "new_post":
            return self._check_new_post_trigger()
        elif trigger_type == "new_follower":
            return self._check_new_follower_trigger()
        elif trigger_type == "unfollower":
            return self._check_unfollower_trigger()
        elif trigger_type == "kpi_threshold":
            return self._check_kpi_threshold_trigger()
        elif trigger_type == "schedule":
            return self._check_schedule_trigger()
        else:
            logger.warning(f"Unknown trigger type: {trigger_type}")
            return False, {}

    def _check_new_post_trigger(self) -> tuple[bool, dict]:
        """Trigger when new post is published."""
        params = self.trigger_config.get("params", {})
        account_id = params.get("account_id")
        since_minutes = params.get("since_minutes", 15)
        
        since = timezone.now() - timedelta(minutes=since_minutes)
        
        # Check for recent posts (would need Post model with publish tracking)
        # Placeholder: always return False for now
        return False, {}

    def _check_new_follower_trigger(self) -> tuple[bool, dict]:
        """Trigger when new followers detected."""
        params = self.trigger_config.get("params", {})
        account_id = params.get("account_id")
        threshold = params.get("threshold", 10)  # Minimum new followers to trigger
        since_minutes = params.get("since_minutes", 15)
        
        if not account_id:
            return False, {}
        
        since = timezone.now() - timedelta(minutes=since_minutes)
        
        new_followers_count = FollowerChange.objects.filter(
            social_account_id=account_id,
            change_type=FollowerChange.TYPE_NEW_FOLLOWER,
            timestamp__gte=since,
        ).count()
        
        if new_followers_count >= threshold:
            return True, {
                "account_id": account_id,
                "new_followers_count": new_followers_count,
                "threshold": threshold,
            }
        
        return False, {}

    def _check_unfollower_trigger(self) -> tuple[bool, dict]:
        """Trigger when unfollowers detected."""
        params = self.trigger_config.get("params", {})
        account_id = params.get("account_id")
        threshold = params.get("threshold", 5)
        since_minutes = params.get("since_minutes", 15)
        
        if not account_id:
            return False, {}
        
        since = timezone.now() - timedelta(minutes=since_minutes)
        
        unfollowers_count = FollowerChange.objects.filter(
            social_account_id=account_id,
            change_type=FollowerChange.TYPE_UNFOLLOWER,
            timestamp__gte=since,
        ).count()
        
        if unfollowers_count >= threshold:
            return True, {
                "account_id": account_id,
                "unfollowers_count": unfollowers_count,
                "threshold": threshold,
            }
        
        return False, {}

    def _check_kpi_threshold_trigger(self) -> tuple[bool, dict]:
        """Trigger when KPI crosses threshold."""
        params = self.trigger_config.get("params", {})
        account_id = params.get("account_id")
        metric = params.get("metric")  # e.g., "reach", "engagement", "followers"
        operator = params.get("operator")  # ">", "<", ">=", "<=", "=="
        threshold = params.get("threshold")
        
        if not all([account_id, metric, operator, threshold]):
            return False, {}
        
        # Get latest snapshot
        snapshot = MetricsSnapshot.objects.filter(social_account_id=account_id).first()
        
        if not snapshot:
            return False, {}
        
        # Get metric value
        metric_map = {
            "reach": snapshot.reach,
            "impressions": snapshot.impressions,
            "engagement": snapshot.engagement_count,
            "followers": snapshot.followers_count,
            "profile_views": snapshot.profile_views,
        }
        
        current_value = metric_map.get(metric, 0)
        
        # Evaluate condition
        should_trigger = False
        if operator == ">":
            should_trigger = current_value > threshold
        elif operator == "<":
            should_trigger = current_value < threshold
        elif operator == ">=":
            should_trigger = current_value >= threshold
        elif operator == "<=":
            should_trigger = current_value <= threshold
        elif operator == "==":
            should_trigger = current_value == threshold
        
        if should_trigger:
            return True, {
                "account_id": account_id,
                "metric": metric,
                "current_value": current_value,
                "threshold": threshold,
                "operator": operator,
            }
        
        return False, {}

    def _check_schedule_trigger(self) -> tuple[bool, dict]:
        """Trigger on schedule (cron-like)."""
        # Would implement cron parsing, for now return False
        return False, {}

    def execute_actions(self, trigger_data: dict) -> list:
        """Execute all actions in the automation. Returns list of action results."""
        results = []
        
        for action_config in self.actions_config:
            action_type = action_config.get("type")
            
            try:
                if action_type == "create_draft":
                    result = self._action_create_draft(action_config, trigger_data)
                elif action_type == "send_notification":
                    result = self._action_send_notification(action_config, trigger_data)
                elif action_type == "request_approval":
                    result = self._action_request_approval(action_config, trigger_data)
                elif action_type == "webhook":
                    result = self._action_webhook(action_config, trigger_data)
                else:
                    result = {"action": action_type, "status": "unknown", "error": "Unknown action type"}
                
                results.append(result)
            
            except Exception as e:
                logger.error(f"Action {action_type} failed: {e}")
                results.append({"action": action_type, "status": "failed", "error": str(e)})
        
        return results

    def _action_create_draft(self, action_config: dict, trigger_data: dict) -> dict:
        """Create a content draft."""
        params = action_config.get("params", {})
        
        # Would create ContentBrief and generate variants
        # For now, just log
        logger.info(f"Would create draft with params: {params}")
        
        return {
            "action": "create_draft",
            "status": "success",
            "message": "Draft creation logged (placeholder)",
        }

    def _action_send_notification(self, action_config: dict, trigger_data: dict) -> dict:
        """Send notification (email, Slack, etc.)."""
        params = action_config.get("params", {})
        message = params.get("message", "")
        
        # Format message with trigger data
        formatted_message = message.format(**trigger_data)
        
        logger.info(f"Notification: {formatted_message}")
        
        # Would integrate with notification service (email, Slack, etc.)
        
        return {
            "action": "send_notification",
            "status": "success",
            "message": formatted_message,
        }

    def _action_request_approval(self, action_config: dict, trigger_data: dict) -> dict:
        """Request manual approval."""
        params = action_config.get("params", {})
        
        # Would create approval request in UI
        logger.info(f"Approval request: {params}")
        
        return {
            "action": "request_approval",
            "status": "pending",
            "message": "Approval request created",
        }

    def _action_webhook(self, action_config: dict, trigger_data: dict) -> dict:
        """Send webhook to external URL."""
        import requests
        
        params = action_config.get("params", {})
        url = params.get("url")
        method = params.get("method", "POST")
        
        if not url:
            return {"action": "webhook", "status": "failed", "error": "No URL provided"}
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json={"trigger_data": trigger_data, "automation_id": str(self.automation.id)},
                timeout=10,
            )
            
            return {
                "action": "webhook",
                "status": "success",
                "response_code": response.status_code,
            }
        
        except Exception as e:
            return {"action": "webhook", "status": "failed", "error": str(e)}

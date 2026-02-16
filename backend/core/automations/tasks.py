from celery import shared_task
from django.utils import timezone
import logging

from core.automations.models import Automation, AutomationRun
from core.automations.executor import AutomationExecutor

logger = logging.getLogger(__name__)


@shared_task
def check_all_automations():
    """Periodic task: check all enabled automations for trigger conditions. Runs every 5 minutes."""
    automations = Automation.objects.filter(enabled=True)
    
    for automation in automations:
        try:
            trigger_automation.delay(str(automation.id))
        except Exception as e:
            logger.error(f"Failed to queue automation check for {automation}: {e}")


@shared_task
def trigger_automation(automation_id):
    """Check if automation should trigger and execute if conditions met."""
    try:
        automation = Automation.objects.get(id=automation_id)
        
        if not automation.enabled:
            logger.info(f"Automation {automation.name} is disabled, skipping")
            return
        
        executor = AutomationExecutor(automation)
        
        # Check trigger condition
        should_trigger, trigger_data = executor.check_trigger()
        
        if should_trigger:
            # Create run record
            run = AutomationRun.objects.create(
                automation=automation,
                status=AutomationRun.STATUS_PENDING,
                trigger_data=trigger_data,
            )
            
            # Execute automation
            execute_automation_run.delay(str(run.id))
        
    except Exception as e:
        logger.error(f"Failed to trigger automation {automation_id}: {e}")


@shared_task
def execute_automation_run(run_id):
    """Execute an automation run."""
    try:
        run = AutomationRun.objects.get(id=run_id)
        automation = run.automation
        
        # Update status
        run.status = AutomationRun.STATUS_RUNNING
        run.save()
        
        executor = AutomationExecutor(automation)
        
        # Execute actions
        results = executor.execute_actions(run.trigger_data)
        
        # Update run with results
        run.actions_executed = results
        run.status = AutomationRun.STATUS_SUCCESS
        run.completed_at = timezone.now()
        run.save()
        
        logger.info(f"Automation run {run.id} completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to execute automation run {run_id}: {e}")
        
        # Update run with error
        run = AutomationRun.objects.get(id=run_id)
        run.status = AutomationRun.STATUS_FAILED
        run.error_message = str(e)
        run.completed_at = timezone.now()
        run.save()

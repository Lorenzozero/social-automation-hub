from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Periodic tasks schedule
app.conf.beat_schedule = {
    'sync-metrics-every-15min': {
        'task': 'core.social.tasks.sync_all_accounts_metrics',
        'schedule': crontab(minute='*/15'),
    },
    'detect-follower-changes-every-30min': {
        'task': 'core.social.tasks.detect_all_follower_changes',
        'schedule': crontab(minute='*/30'),
    },
    'update-top-content-daily': {
        'task': 'core.social.tasks.update_all_top_content',
        'schedule': crontab(hour=2, minute=0),
    },
    'fetch-audience-insights-weekly': {
        'task': 'core.social.tasks.fetch_all_audience_insights',
        'schedule': crontab(day_of_week=1, hour=3, minute=0),
    },
}

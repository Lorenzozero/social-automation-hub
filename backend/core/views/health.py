"""System health check endpoint"""

import logging
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from celery import current_app as celery_app

logger = logging.getLogger(__name__)


def health_check(request):
    """
    System health check endpoint.
    Returns 200 if all systems healthy, 503 if any unhealthy.
    """
    
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'celery_worker': check_celery_worker(),
        'celery_beat': check_celery_beat(),
    }
    
    all_healthy = all(check['status'] == 'healthy' for check in checks.values())
    status_code = 200 if all_healthy else 503
    
    return JsonResponse({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks,
    }, status=status_code)


def check_database() -> dict:
    """Check PostgreSQL connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return {
            'status': 'healthy',
            'message': 'Database connection OK',
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            'status': 'unhealthy',
            'message': str(e),
        }


def check_redis() -> dict:
    """Check Redis connection"""
    try:
        cache.set('health_check', 'ok', timeout=10)
        value = cache.get('health_check')
        
        if value != 'ok':
            raise Exception("Cache read/write mismatch")
        
        return {
            'status': 'healthy',
            'message': 'Redis connection OK',
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return {
            'status': 'unhealthy',
            'message': str(e),
        }


def check_celery_worker() -> dict:
    """Check if Celery workers are running"""
    try:
        inspect = celery_app.control.inspect()
        active_workers = inspect.active()
        
        if not active_workers:
            return {
                'status': 'unhealthy',
                'message': 'No active Celery workers',
            }
        
        worker_count = len(active_workers)
        return {
            'status': 'healthy',
            'message': f'{worker_count} worker(s) active',
            'workers': list(active_workers.keys()),
        }
    except Exception as e:
        logger.error(f"Celery worker health check failed: {e}")
        return {
            'status': 'unhealthy',
            'message': str(e),
        }


def check_celery_beat() -> dict:
    """Check if Celery beat scheduler is running"""
    try:
        # Check if beat has updated its heartbeat recently
        last_heartbeat = cache.get('celery_beat_heartbeat')
        
        if not last_heartbeat:
            return {
                'status': 'unknown',
                'message': 'No beat heartbeat found',
            }
        
        # If heartbeat older than 5 minutes, beat is likely down
        if datetime.fromisoformat(last_heartbeat) < datetime.utcnow() - timedelta(minutes=5):
            return {
                'status': 'unhealthy',
                'message': 'Beat heartbeat stale',
                'last_heartbeat': last_heartbeat,
            }
        
        return {
            'status': 'healthy',
            'message': 'Beat scheduler active',
            'last_heartbeat': last_heartbeat,
        }
    except Exception as e:
        logger.error(f"Celery beat health check failed: {e}")
        return {
            'status': 'unhealthy',
            'message': str(e),
        }

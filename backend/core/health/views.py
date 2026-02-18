import time
import requests
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import redis
import psycopg2
from celery import current_app
from datetime import datetime
import os


def test_total(request):
    """
    Comprehensive system test endpoint.
    Tests all critical services, flows, and connections.
    
    Usage:
        curl -X GET http://localhost:8000/api/health/test_total/
        curl -X GET http://localhost:8000/api/health/test_total/ | jq
    """
    start_time = time.time()
    results = {
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "tests": {},
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
        },
        "overall_status": "unknown",
        "execution_time_ms": 0,
    }

    # Test 1: Django Application
    results["tests"]["django"] = test_django()
    
    # Test 2: PostgreSQL Database
    results["tests"]["database"] = test_database()
    
    # Test 3: Redis Cache/Queue
    results["tests"]["redis"] = test_redis()
    
    # Test 4: Celery Worker
    results["tests"]["celery_worker"] = test_celery_worker()
    
    # Test 5: Celery Beat Scheduler
    results["tests"]["celery_beat"] = test_celery_beat()
    
    # Test 6: Environment Variables
    results["tests"]["environment"] = test_environment()
    
    # Test 7: OAuth Credentials
    results["tests"]["oauth_config"] = test_oauth_config()
    
    # Test 8: File System Permissions
    results["tests"]["filesystem"] = test_filesystem()
    
    # Test 9: External API Connectivity
    results["tests"]["external_apis"] = test_external_apis()
    
    # Test 10: Django Models
    results["tests"]["models"] = test_models()
    
    # Calculate summary
    for test_name, test_result in results["tests"].items():
        results["summary"]["total"] += 1
        status = test_result.get("status", "failed")
        if status == "passed":
            results["summary"]["passed"] += 1
        elif status == "warning":
            results["summary"]["warnings"] += 1
        else:
            results["summary"]["failed"] += 1
    
    # Determine overall status
    if results["summary"]["failed"] == 0:
        if results["summary"]["warnings"] == 0:
            results["overall_status"] = "healthy"
        else:
            results["overall_status"] = "degraded"
    else:
        results["overall_status"] = "unhealthy"
    
    # Execution time
    results["execution_time_ms"] = round((time.time() - start_time) * 1000, 2)
    
    # HTTP status code based on overall status
    status_code = 200 if results["overall_status"] in ["healthy", "degraded"] else 503
    
    return JsonResponse(results, status=status_code, json_dumps_params={'indent': 2})


def test_django():
    """Test Django application health"""
    try:
        from django import get_version
        return {
            "status": "passed",
            "message": "Django application running",
            "details": {
                "version": get_version(),
                "debug_mode": settings.DEBUG,
                "allowed_hosts": settings.ALLOWED_HOSTS,
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Django application error",
            "error": str(e)
        }


def test_database():
    """Test PostgreSQL database connectivity and basic operations"""
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        # Test write operation
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TEMP TABLE health_check_test (id INTEGER);
                INSERT INTO health_check_test VALUES (1);
                SELECT * FROM health_check_test;
                DROP TABLE health_check_test;
            """)
        
        # Get DB info
        db_config = settings.DATABASES['default']
        
        return {
            "status": "passed",
            "message": "Database connection successful",
            "details": {
                "engine": db_config['ENGINE'],
                "name": db_config.get('NAME', 'N/A'),
                "host": db_config.get('HOST', 'localhost'),
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Database connection failed",
            "error": str(e)
        }


def test_redis():
    """Test Redis connectivity for cache and Celery broker"""
    try:
        # Test via Django cache
        test_key = "health_check_test"
        test_value = "test_value_123"
        cache.set(test_key, test_value, timeout=10)
        retrieved = cache.get(test_key)
        cache.delete(test_key)
        
        if retrieved != test_value:
            raise Exception("Cache value mismatch")
        
        # Test direct Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url)
        r.ping()
        
        # Get Redis info
        info = r.info('server')
        
        return {
            "status": "passed",
            "message": "Redis connection successful",
            "details": {
                "redis_version": info.get('redis_version', 'unknown'),
                "uptime_seconds": info.get('uptime_in_seconds', 0),
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Redis connection failed",
            "error": str(e)
        }


def test_celery_worker():
    """Test Celery worker availability"""
    try:
        # Inspect active workers
        inspect = current_app.control.inspect()
        active_workers = inspect.active()
        
        if not active_workers:
            return {
                "status": "failed",
                "message": "No active Celery workers found",
                "error": "Worker process not running"
            }
        
        # Get worker stats
        stats = inspect.stats()
        
        return {
            "status": "passed",
            "message": "Celery workers active",
            "details": {
                "worker_count": len(active_workers),
                "workers": list(active_workers.keys()),
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Celery worker check failed",
            "error": str(e)
        }


def test_celery_beat():
    """Test Celery Beat scheduler"""
    try:
        # Check if beat is running by inspecting scheduled tasks
        inspect = current_app.control.inspect()
        scheduled = inspect.scheduled()
        
        if scheduled is None:
            return {
                "status": "warning",
                "message": "Celery Beat status unknown",
                "details": "Cannot determine if Beat scheduler is running"
            }
        
        return {
            "status": "passed",
            "message": "Celery Beat accessible",
            "details": {
                "scheduled_tasks": len(scheduled) if scheduled else 0
            }
        }
    except Exception as e:
        return {
            "status": "warning",
            "message": "Celery Beat check inconclusive",
            "error": str(e)
        }


def test_environment():
    """Test critical environment variables"""
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'REDIS_URL',
        'ENCRYPTION_KEY',
    ]
    
    missing_vars = []
    present_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            present_vars.append(var)
        else:
            missing_vars.append(var)
    
    if missing_vars:
        return {
            "status": "failed",
            "message": "Missing required environment variables",
            "details": {
                "missing": missing_vars,
                "present": present_vars,
            }
        }
    
    return {
        "status": "passed",
        "message": "All required environment variables present",
        "details": {
            "checked": required_vars,
            "all_present": True,
        }
    }


def test_oauth_config():
    """Test OAuth credentials configuration"""
    oauth_platforms = {
        'instagram': ['INSTAGRAM_CLIENT_ID', 'INSTAGRAM_CLIENT_SECRET'],
        'tiktok': ['TIKTOK_CLIENT_KEY', 'TIKTOK_CLIENT_SECRET'],
        'linkedin': ['LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET'],
        'x': ['X_CLIENT_ID', 'X_CLIENT_SECRET'],
    }
    
    configured = []
    missing = []
    
    for platform, vars in oauth_platforms.items():
        if all(os.getenv(var) for var in vars):
            configured.append(platform)
        else:
            missing.append(platform)
    
    status = "passed" if configured else "warning"
    message = f"{len(configured)}/4 OAuth platforms configured"
    
    return {
        "status": status,
        "message": message,
        "details": {
            "configured": configured,
            "missing": missing,
        }
    }


def test_filesystem():
    """Test file system permissions"""
    try:
        import tempfile
        
        # Test write permission
        with tempfile.NamedTemporaryFile(mode='w', delete=True) as f:
            f.write('test')
            f.flush()
        
        # Test media directory if configured
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        media_writable = False
        if media_root and os.path.exists(media_root):
            media_writable = os.access(media_root, os.W_OK)
        
        return {
            "status": "passed",
            "message": "File system permissions OK",
            "details": {
                "temp_writable": True,
                "media_root": media_root,
                "media_writable": media_writable,
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "File system permission error",
            "error": str(e)
        }


def test_external_apis():
    """Test external API connectivity"""
    apis_to_test = [
        {"name": "Google", "url": "https://www.google.com", "timeout": 5},
        {"name": "GitHub", "url": "https://api.github.com", "timeout": 5},
    ]
    
    results = []
    all_passed = True
    
    for api in apis_to_test:
        try:
            start = time.time()
            response = requests.get(api["url"], timeout=api["timeout"])
            latency = round((time.time() - start) * 1000, 2)
            
            results.append({
                "name": api["name"],
                "status": "reachable",
                "http_code": response.status_code,
                "latency_ms": latency,
            })
        except Exception as e:
            all_passed = False
            results.append({
                "name": api["name"],
                "status": "unreachable",
                "error": str(e),
            })
    
    return {
        "status": "passed" if all_passed else "warning",
        "message": "External API connectivity test",
        "details": {
            "apis_tested": len(apis_to_test),
            "results": results,
        }
    }


def test_models():
    """Test Django models accessibility"""
    try:
        from django.apps import apps
        
        # Get all models
        all_models = apps.get_models()
        model_count = len(all_models)
        
        # Test a simple query on User model
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        
        return {
            "status": "passed",
            "message": "Django models accessible",
            "details": {
                "total_models": model_count,
                "user_count": user_count,
            }
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": "Model access error",
            "error": str(e)
        }


def health_check(request):
    """
    Simple health check endpoint (faster than test_total).
    
    Usage:
        curl http://localhost:8000/api/health/health/
    """
    try:
        # Quick DB check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
        })
    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }, status=503)

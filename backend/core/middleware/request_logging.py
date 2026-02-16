"""Request logging middleware for audit and debugging"""

import logging
import time
import json
from django.conf import settings

logger = logging.getLogger('core')


class RequestLoggingMiddleware:
    """Log all requests with timing and metadata"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log request details
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2),
            'user': str(request.user) if hasattr(request, 'user') and request.user.is_authenticated else 'anonymous',
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
        }
        
        # Log at appropriate level
        if response.status_code >= 500:
            logger.error('Request failed', extra=log_data)
        elif response.status_code >= 400:
            logger.warning('Client error', extra=log_data)
        else:
            logger.info('Request completed', extra=log_data)
        
        # Add custom headers
        response['X-Request-Duration'] = str(duration)
        
        return response

    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

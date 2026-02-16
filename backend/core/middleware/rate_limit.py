"""Rate limiting middleware"""

import logging
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
import hashlib
import time

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """Global rate limiting middleware"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'RATELIMIT_ENABLE', True)

    def __call__(self, request):
        if not self.enabled:
            return self.get_response(request)

        # Check rate limit
        if self.is_rate_limited(request):
            logger.warning(
                f"Rate limit exceeded for {request.path}",
                extra={
                    'user': str(request.user) if hasattr(request, 'user') else 'anonymous',
                    'ip': self.get_client_ip(request),
                    'path': request.path,
                }
            )
            return JsonResponse({
                'error': 'rate_limit_exceeded',
                'message': 'Too many requests. Please try again later.',
                'retry_after': 60,
            }, status=429)

        response = self.get_response(request)
        return response

    def is_rate_limited(self, request):
        """Check if request exceeds rate limit"""
        
        # Get rate limit key
        rate_key = self.get_rate_key(request)
        
        # Get current request count
        current_count = cache.get(rate_key, 0)
        
        # Get rate limit for this endpoint
        rate_limit = self.get_rate_limit(request)
        if not rate_limit:
            return False  # No limit configured
        
        requests_allowed, window_seconds = self.parse_rate(rate_limit)
        
        # Check if exceeded
        if current_count >= requests_allowed:
            return True
        
        # Increment counter
        if current_count == 0:
            cache.set(rate_key, 1, timeout=window_seconds)
        else:
            cache.incr(rate_key)
        
        return False

    def get_rate_key(self, request):
        """Generate unique rate limit key per user/IP + endpoint"""
        
        # Use user ID if authenticated, otherwise IP
        if hasattr(request, 'user') and request.user.is_authenticated:
            identifier = f"user:{request.user.id}"
        else:
            identifier = f"ip:{self.get_client_ip(request)}"
        
        # Hash endpoint path for cleaner keys
        path_hash = hashlib.md5(request.path.encode()).hexdigest()[:8]
        
        return f"ratelimit:{identifier}:{path_hash}"

    def get_rate_limit(self, request):
        """Get rate limit configuration for endpoint"""
        
        # Map paths to rate limit keys
        path = request.path
        
        if '/oauth/' in path and '/callback' in path:
            return '10/m'
        elif '/oauth/' in path:
            return '5/m'
        elif '/analytics/' in path:
            return '30/m'
        elif '/posts/' in path and request.method == 'POST':
            return '50/h'
        elif '/automations/' in path and '/execute' in path:
            return '100/h'
        elif '/content/generate' in path:
            return '10/h'
        
        # Default global limit
        return '1000/h'

    @staticmethod
    def parse_rate(rate_string):
        """Parse rate string like '10/m' or '100/h' to (requests, seconds)"""
        requests, period = rate_string.split('/')
        requests = int(requests)
        
        period_map = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
        }
        
        seconds = period_map.get(period, 60)
        return requests, seconds

    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

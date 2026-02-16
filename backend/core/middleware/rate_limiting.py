from django.core.cache import cache
from django.http import JsonResponse
import time
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    Rate limiting middleware using Django cache.
    
    Limits:
    - Anonymous: 100 requests/hour
    - Authenticated: 1000 requests/hour
    - Per-endpoint overrides via settings
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get client identifier
        if request.user.is_authenticated:
            client_id = f"user:{request.user.id}"
            limit = 1000  # requests per hour
        else:
            client_id = f"ip:{self.get_client_ip(request)}"
            limit = 100
        
        # Check rate limit
        cache_key = f"ratelimit:{client_id}:{int(time.time() // 3600)}"
        requests_count = cache.get(cache_key, 0)
        
        if requests_count >= limit:
            logger.warning(f"Rate limit exceeded for {client_id}")
            return JsonResponse(
                {"error": "Rate limit exceeded. Please try again later."},
                status=429
            )
        
        # Increment counter
        cache.set(cache_key, requests_count + 1, timeout=3600)
        
        # Add rate limit headers
        response = self.get_response(request)
        response["X-RateLimit-Limit"] = str(limit)
        response["X-RateLimit-Remaining"] = str(max(0, limit - requests_count - 1))
        response["X-RateLimit-Reset"] = str(int(time.time() // 3600 + 1) * 3600)
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')

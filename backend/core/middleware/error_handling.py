"""Custom error handling middleware"""

import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """Global error handler middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            return self.handle_exception(request, exc)

    def handle_exception(self, request, exc):
        """Convert exceptions to JSON responses"""
        
        # Log exception with context
        logger.error(
            f"Exception in {request.method} {request.path}",
            exc_info=True,
            extra={
                'user': str(request.user) if hasattr(request, 'user') else 'anonymous',
                'ip': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
        )

        # Permission denied (403)
        if isinstance(exc, PermissionDenied):
            return JsonResponse({
                'error': 'permission_denied',
                'message': 'You do not have permission to perform this action.',
                'details': str(exc),
            }, status=403)

        # Validation error (400)
        if isinstance(exc, ValidationError):
            return JsonResponse({
                'error': 'validation_error',
                'message': 'Invalid data provided.',
                'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc),
            }, status=400)

        # DRF API exceptions
        if isinstance(exc, APIException):
            return JsonResponse({
                'error': exc.default_code,
                'message': exc.detail,
            }, status=exc.status_code)

        # Generic server error (500)
        return JsonResponse({
            'error': 'internal_server_error',
            'message': 'An unexpected error occurred. Please try again later.',
            'request_id': request.META.get('HTTP_X_REQUEST_ID', 'unknown'),
        }, status=500)

    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

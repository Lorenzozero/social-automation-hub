"""Custom exception handler for REST Framework"""

import logging
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, Throttled
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError, IntegrityError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler with detailed error responses"""
    
    # Call REST framework's default handler first
    response = exception_handler(exc, context)
    
    # If DRF didn't handle it, handle custom exceptions
    if response is None:
        
        # Database errors
        if isinstance(exc, OperationalError):
            logger.error(f"Database operational error: {exc}")
            return Response({
                'error': 'database_error',
                'message': 'Database connection error. Please try again later.',
            }, status=503)
        
        if isinstance(exc, IntegrityError):
            logger.error(f"Database integrity error: {exc}")
            return Response({
                'error': 'integrity_error',
                'message': 'Data integrity constraint violation.',
                'details': str(exc),
            }, status=400)
        
        # Object not found
        if isinstance(exc, ObjectDoesNotExist):
            return Response({
                'error': 'not_found',
                'message': 'The requested resource does not exist.',
            }, status=404)
    
    # Enhance DRF responses with additional context
    if response is not None:
        # Add request context
        request = context.get('request')
        if request:
            response.data['path'] = request.path
            response.data['method'] = request.method
        
        # Add user-friendly messages
        if isinstance(exc, ValidationError):
            response.data['error'] = 'validation_error'
            response.data['message'] = 'Invalid data provided.'
        
        elif isinstance(exc, PermissionDenied):
            response.data['error'] = 'permission_denied'
            response.data['message'] = 'You do not have permission to perform this action.'
        
        elif isinstance(exc, NotFound):
            response.data['error'] = 'not_found'
            response.data['message'] = 'The requested resource was not found.'
        
        elif isinstance(exc, Throttled):
            response.data['error'] = 'rate_limit_exceeded'
            response.data['message'] = f'Too many requests. Please try again in {exc.wait} seconds.'
            response.data['retry_after'] = exc.wait
    
    return response


from rest_framework.response import Response

"""Webhook handlers for platform events"""

import json
import hmac
import hashlib
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.social.models import SocialAccount
from core.social.tasks import process_instagram_webhook, process_x_webhook

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def instagram_webhook(request):
    """Handle Instagram Graph API webhooks"""
    
    # Verify webhook (GET request for subscription verification)
    if request.method == "GET":
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode == 'subscribe' and token == settings.INSTAGRAM_WEBHOOK_VERIFY_TOKEN:
            logger.info("Instagram webhook verified")
            return HttpResponse(challenge)
        else:
            logger.warning("Instagram webhook verification failed")
            return HttpResponse(status=403)
    
    # Handle webhook event (POST)
    try:
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not verify_instagram_signature(request.body, signature):
            logger.warning("Instagram webhook invalid signature")
            return JsonResponse({'error': 'invalid_signature'}, status=403)
        
        data = json.loads(request.body)
        
        # Queue processing
        for entry in data.get('entry', []):
            process_instagram_webhook.delay(entry)
        
        logger.info(f"Instagram webhook received: {len(data.get('entry', []))} entries")
        return JsonResponse({'status': 'ok'})
    
    except Exception as e:
        logger.error(f"Instagram webhook error: {e}", exc_info=True)
        return JsonResponse({'error': 'processing_failed'}, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def x_webhook(request):
    """Handle X (Twitter) Account Activity API webhooks"""
    
    # CRC challenge (GET)
    if request.method == "GET":
        crc_token = request.GET.get('crc_token')
        if crc_token:
            response_token = generate_x_crc_response(crc_token)
            return JsonResponse({'response_token': response_token})
    
    # Handle event (POST)
    try:
        # Verify signature
        signature = request.headers.get('X-Twitter-Webhooks-Signature', '')
        if not verify_x_signature(request.body, signature):
            logger.warning("X webhook invalid signature")
            return JsonResponse({'error': 'invalid_signature'}, status=403)
        
        data = json.loads(request.body)
        
        # Queue processing
        process_x_webhook.delay(data)
        
        logger.info(f"X webhook received: {data.keys()}")
        return JsonResponse({'status': 'ok'})
    
    except Exception as e:
        logger.error(f"X webhook error: {e}", exc_info=True)
        return JsonResponse({'error': 'processing_failed'}, status=500)


def verify_instagram_signature(payload: bytes, signature: str) -> bool:
    """Verify Instagram webhook signature"""
    from django.conf import settings
    
    expected_signature = 'sha256=' + hmac.new(
        settings.INSTAGRAM_APP_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


def verify_x_signature(payload: bytes, signature: str) -> bool:
    """Verify X webhook signature"""
    from django.conf import settings
    
    expected_signature = 'sha256=' + hmac.new(
        settings.X_WEBHOOK_CONSUMER_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


def generate_x_crc_response(crc_token: str) -> str:
    """Generate CRC response for X webhook challenge"""
    from django.conf import settings
    
    response = 'sha256=' + hmac.new(
        settings.X_WEBHOOK_CONSUMER_SECRET.encode(),
        crc_token.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return response


from django.conf import settings
from django.http import HttpResponse

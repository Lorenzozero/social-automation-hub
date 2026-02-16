import base64
import secrets
from urllib.parse import urlencode

import requests
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.social.models import SocialAccount, OAuthToken
from core.workspaces.models import Workspace


def get_cipher():
    """Get Fernet cipher for token encryption/decryption."""
    key = settings.ENCRYPTION_KEY
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in settings")
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_token(token: str) -> str:
    """Encrypt OAuth token."""
    cipher = get_cipher()
    return cipher.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt OAuth token."""
    cipher = get_cipher()
    return cipher.decrypt(encrypted_token.encode()).decode()


# ========== INSTAGRAM/FACEBOOK (META) ==========

@require_http_methods(["GET"])
def instagram_authorize(request):
    """
    Redirect user to Instagram OAuth authorization.
    Query params: workspace_id (required)
    """
    workspace_id = request.GET.get("workspace_id")
    if not workspace_id:
        return JsonResponse({"error": "workspace_id required"}, status=400)

    state = base64.urlsafe_b64encode(f"{workspace_id}:{secrets.token_urlsafe(32)}".encode()).decode()
    
    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "scope": "instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement",
        "response_type": "code",
        "state": state,
    }
    
    authorize_url = f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
    return HttpResponseRedirect(authorize_url)


@csrf_exempt
@require_http_methods(["GET"])
def instagram_callback(request):
    """
    Handle Instagram OAuth callback.
    Exchange code for access token and save to database.
    """
    code = request.GET.get("code")
    state = request.GET.get("state")
    error = request.GET.get("error")

    if error:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error={error}")

    if not code or not state:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=missing_params")

    try:
        workspace_id = base64.urlsafe_b64decode(state.encode()).decode().split(":")[0]
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=invalid_state")

    # Exchange code for access token
    token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
    token_params = {
        "client_id": settings.META_APP_ID,
        "client_secret": settings.META_APP_SECRET,
        "redirect_uri": settings.META_REDIRECT_URI,
        "code": code,
    }

    try:
        token_response = requests.get(token_url, params=token_params, timeout=10)
        token_response.raise_for_status()
        token_data = token_response.json()
    except Exception as e:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=token_exchange_failed")

    access_token = token_data.get("access_token")
    if not access_token:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=no_access_token")

    # Get Instagram Business Account ID
    try:
        me_response = requests.get(
            "https://graph.facebook.com/v18.0/me",
            params={"fields": "id,name,accounts{instagram_business_account}", "access_token": access_token},
            timeout=10,
        )
        me_response.raise_for_status()
        me_data = me_response.json()
        
        ig_account = None
        for page in me_data.get("accounts", {}).get("data", []):
            if "instagram_business_account" in page:
                ig_account = page["instagram_business_account"]["id"]
                break

        if not ig_account:
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=no_instagram_business_account")

        # Get Instagram username
        ig_response = requests.get(
            f"https://graph.facebook.com/v18.0/{ig_account}",
            params={"fields": "username", "access_token": access_token},
            timeout=10,
        )
        ig_response.raise_for_status()
        ig_data = ig_response.json()
        username = ig_data.get("username", "unknown")

    except Exception as e:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=failed_to_get_profile")

    # Save to database
    workspace = Workspace.objects.get(id=workspace_id)
    social_account, created = SocialAccount.objects.update_or_create(
        workspace=workspace,
        platform=SocialAccount.PLATFORM_INSTAGRAM,
        platform_user_id=ig_account,
        defaults={
            "handle": username,
            "status": SocialAccount.STATUS_ACTIVE,
        },
    )

    OAuthToken.objects.update_or_create(
        social_account=social_account,
        defaults={
            "access_token_enc": encrypt_token(access_token),
            "refresh_token_enc": "",
            "scopes": "instagram_basic,instagram_content_publish",
            "expires_at": None,  # Meta tokens don't expire for Instagram Business
        },
    )

    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?success=instagram_connected")


# ========== TIKTOK ==========

@require_http_methods(["GET"])
def tiktok_authorize(request):
    workspace_id = request.GET.get("workspace_id")
    if not workspace_id:
        return JsonResponse({"error": "workspace_id required"}, status=400)

    state = base64.urlsafe_b64encode(f"{workspace_id}:{secrets.token_urlsafe(32)}".encode()).decode()
    
    params = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "redirect_uri": settings.TIKTOK_REDIRECT_URI,
        "scope": "user.info.basic,video.publish",
        "response_type": "code",
        "state": state,
    }
    
    authorize_url = f"https://www.tiktok.com/v2/auth/authorize/?{urlencode(params)}"
    return HttpResponseRedirect(authorize_url)


@csrf_exempt
@require_http_methods(["GET"])
def tiktok_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    error = request.GET.get("error")

    if error:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error={error}")

    if not code or not state:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=missing_params")

    try:
        workspace_id = base64.urlsafe_b64decode(state.encode()).decode().split(":")[0]
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=invalid_state")

    # Exchange code for access token
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    token_data = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "client_secret": settings.TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.TIKTOK_REDIRECT_URI,
    }

    try:
        token_response = requests.post(token_url, json=token_data, timeout=10)
        token_response.raise_for_status()
        token_result = token_response.json()
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=token_exchange_failed")

    access_token = token_result.get("data", {}).get("access_token")
    refresh_token = token_result.get("data", {}).get("refresh_token", "")
    open_id = token_result.get("data", {}).get("open_id")

    if not access_token or not open_id:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=no_access_token")

    # Get user info
    try:
        user_response = requests.get(
            "https://open.tiktokapis.com/v2/user/info/",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"fields": "open_id,union_id,avatar_url,display_name"},
            timeout=10,
        )
        user_response.raise_for_status()
        user_data = user_response.json().get("data", {}).get("user", {})
        username = user_data.get("display_name", "unknown")
    except Exception:
        username = "unknown"

    workspace = Workspace.objects.get(id=workspace_id)
    social_account, created = SocialAccount.objects.update_or_create(
        workspace=workspace,
        platform=SocialAccount.PLATFORM_TIKTOK,
        platform_user_id=open_id,
        defaults={
            "handle": username,
            "status": SocialAccount.STATUS_ACTIVE,
        },
    )

    OAuthToken.objects.update_or_create(
        social_account=social_account,
        defaults={
            "access_token_enc": encrypt_token(access_token),
            "refresh_token_enc": encrypt_token(refresh_token) if refresh_token else "",
            "scopes": "user.info.basic,video.publish",
            "expires_at": None,
        },
    )

    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?success=tiktok_connected")


# ========== LINKEDIN ==========

@require_http_methods(["GET"])
def linkedin_authorize(request):
    workspace_id = request.GET.get("workspace_id")
    if not workspace_id:
        return JsonResponse({"error": "workspace_id required"}, status=400)

    state = base64.urlsafe_b64encode(f"{workspace_id}:{secrets.token_urlsafe(32)}".encode()).decode()
    
    params = {
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "scope": "openid profile w_member_social",
        "response_type": "code",
        "state": state,
    }
    
    authorize_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    return HttpResponseRedirect(authorize_url)


@csrf_exempt
@require_http_methods(["GET"])
def linkedin_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    error = request.GET.get("error")

    if error:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error={error}")

    if not code or not state:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=missing_params")

    try:
        workspace_id = base64.urlsafe_b64decode(state.encode()).decode().split(":")[0]
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=invalid_state")

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
    }

    try:
        token_response = requests.post(token_url, data=token_data, timeout=10)
        token_response.raise_for_status()
        token_result = token_response.json()
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=token_exchange_failed")

    access_token = token_result.get("access_token")
    if not access_token:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=no_access_token")

    # Get user profile
    try:
        profile_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        user_id = profile_data.get("sub")
        username = profile_data.get("name", "unknown")
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=failed_to_get_profile")

    workspace = Workspace.objects.get(id=workspace_id)
    social_account, created = SocialAccount.objects.update_or_create(
        workspace=workspace,
        platform=SocialAccount.PLATFORM_LINKEDIN,
        platform_user_id=user_id,
        defaults={
            "handle": username,
            "status": SocialAccount.STATUS_ACTIVE,
        },
    )

    OAuthToken.objects.update_or_create(
        social_account=social_account,
        defaults={
            "access_token_enc": encrypt_token(access_token),
            "refresh_token_enc": "",
            "scopes": "openid profile w_member_social",
            "expires_at": None,
        },
    )

    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?success=linkedin_connected")


# ========== X (TWITTER) ==========

@require_http_methods(["GET"])
def x_authorize(request):
    workspace_id = request.GET.get("workspace_id")
    if not workspace_id:
        return JsonResponse({"error": "workspace_id required"}, status=400)

    state = base64.urlsafe_b64encode(f"{workspace_id}:{secrets.token_urlsafe(32)}".encode()).decode()
    code_verifier = secrets.token_urlsafe(32)
    
    # Store code_verifier in session (in production, use Redis or DB)
    request.session[f"x_code_verifier_{state}"] = code_verifier
    
    params = {
        "client_id": settings.X_CLIENT_ID,
        "redirect_uri": settings.X_REDIRECT_URI,
        "scope": "tweet.read tweet.write users.read offline.access",
        "response_type": "code",
        "state": state,
        "code_challenge": code_verifier,
        "code_challenge_method": "plain",
    }
    
    authorize_url = f"https://twitter.com/i/oauth2/authorize?{urlencode(params)}"
    return HttpResponseRedirect(authorize_url)


@csrf_exempt
@require_http_methods(["GET"])
def x_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    error = request.GET.get("error")

    if error:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error={error}")

    if not code or not state:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=missing_params")

    try:
        workspace_id = base64.urlsafe_b64decode(state.encode()).decode().split(":")[0]
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=invalid_state")

    code_verifier = request.session.get(f"x_code_verifier_{state}")
    if not code_verifier:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=missing_code_verifier")

    token_url = "https://api.twitter.com/2/oauth2/token"
    token_data = {
        "client_id": settings.X_CLIENT_ID,
        "client_secret": settings.X_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.X_REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    try:
        token_response = requests.post(token_url, data=token_data, timeout=10)
        token_response.raise_for_status()
        token_result = token_response.json()
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=token_exchange_failed")

    access_token = token_result.get("access_token")
    refresh_token = token_result.get("refresh_token", "")
    
    if not access_token:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=no_access_token")

    # Get user profile
    try:
        user_response = requests.get(
            "https://api.twitter.com/2/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        user_response.raise_for_status()
        user_data = user_response.json().get("data", {})
        user_id = user_data.get("id")
        username = user_data.get("username", "unknown")
    except Exception:
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?error=failed_to_get_profile")

    workspace = Workspace.objects.get(id=workspace_id)
    social_account, created = SocialAccount.objects.update_or_create(
        workspace=workspace,
        platform=SocialAccount.PLATFORM_X,
        platform_user_id=user_id,
        defaults={
            "handle": username,
            "status": SocialAccount.STATUS_ACTIVE,
        },
    )

    OAuthToken.objects.update_or_create(
        social_account=social_account,
        defaults={
            "access_token_enc": encrypt_token(access_token),
            "refresh_token_enc": encrypt_token(refresh_token) if refresh_token else "",
            "scopes": "tweet.read tweet.write users.read offline.access",
            "expires_at": None,
        },
    )

    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/accounts?success=x_connected")

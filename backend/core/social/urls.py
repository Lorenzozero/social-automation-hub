from django.urls import path
from .views import oauth

urlpatterns = [
    # Instagram/Facebook (Meta)
    path("instagram/authorize", oauth.instagram_authorize, name="instagram_authorize"),
    path("instagram/callback", oauth.instagram_callback, name="instagram_callback"),
    
    # TikTok
    path("tiktok/authorize", oauth.tiktok_authorize, name="tiktok_authorize"),
    path("tiktok/callback", oauth.tiktok_callback, name="tiktok_callback"),
    
    # LinkedIn
    path("linkedin/authorize", oauth.linkedin_authorize, name="linkedin_authorize"),
    path("linkedin/callback", oauth.linkedin_callback, name="linkedin_callback"),
    
    # X (Twitter)
    path("x/authorize", oauth.x_authorize, name="x_authorize"),
    path("x/callback", oauth.x_callback, name="x_callback"),
]

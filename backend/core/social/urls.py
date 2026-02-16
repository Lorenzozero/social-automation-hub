from django.urls import path
from .views import oauth, analytics

urlpatterns = [
    # OAuth flows
    path("instagram/authorize", oauth.instagram_authorize, name="instagram_authorize"),
    path("instagram/callback", oauth.instagram_callback, name="instagram_callback"),
    path("tiktok/authorize", oauth.tiktok_authorize, name="tiktok_authorize"),
    path("tiktok/callback", oauth.tiktok_callback, name="tiktok_callback"),
    path("linkedin/authorize", oauth.linkedin_authorize, name="linkedin_authorize"),
    path("linkedin/callback", oauth.linkedin_callback, name="linkedin_callback"),
    path("x/authorize", oauth.x_authorize, name="x_authorize"),
    path("x/callback", oauth.x_callback, name="x_callback"),
    
    # Analytics endpoints
    path("analytics/dashboard/<uuid:workspace_id>", analytics.dashboard_metrics, name="dashboard_metrics"),
    path("analytics/follower-changes/<uuid:account_id>", analytics.follower_changes, name="follower_changes"),
    path("analytics/top-content/<uuid:account_id>", analytics.top_content, name="top_content"),
    path("analytics/audience-insights/<uuid:account_id>", analytics.audience_insights, name="audience_insights"),
]

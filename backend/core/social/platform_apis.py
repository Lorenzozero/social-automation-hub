import requests
from datetime import datetime, timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class InstagramAPI:
    """Instagram Graph API integration."""
    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile info."""
        url = f"{self.BASE_URL}/{user_id}"
        params = {
            "fields": "id,username,followers_count,follows_count,media_count,profile_picture_url",
            "access_token": self.access_token,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_user_insights(self, user_id: str, metrics: list, period: str = "day") -> dict:
        """Get user-level insights (reach, impressions, profile_views)."""
        url = f"{self.BASE_URL}/{user_id}/insights"
        params = {
            "metric": ",".join(metrics),
            "period": period,
            "access_token": self.access_token,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_media_list(self, user_id: str, limit: int = 25) -> list:
        """Get recent media posts."""
        url = f"{self.BASE_URL}/{user_id}/media"
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
            "limit": limit,
            "access_token": self.access_token,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_media_insights(self, media_id: str, metrics: list) -> dict:
        """Get insights for a specific media post."""
        url = f"{self.BASE_URL}/{media_id}/insights"
        params = {
            "metric": ",".join(metrics),
            "access_token": self.access_token,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_audience_insights(self, user_id: str) -> dict:
        """Get audience demographics."""
        url = f"{self.BASE_URL}/{user_id}/insights"
        metrics = [
            "audience_city",
            "audience_country",
            "audience_gender_age",
            "online_followers",
        ]
        params = {
            "metric": ",".join(metrics),
            "period": "lifetime",
            "access_token": self.access_token,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


class TikTokAPI:
    """TikTok Open API integration."""
    BASE_URL = "https://open.tiktokapis.com/v2"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_user_info(self) -> dict:
        """Get authenticated user info."""
        url = f"{self.BASE_URL}/user/info/"
        params = {"fields": "open_id,union_id,avatar_url,display_name,follower_count,following_count,video_count"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", {}).get("user", {})

    def list_videos(self, max_count: int = 20) -> list:
        """List user's videos."""
        url = f"{self.BASE_URL}/video/list/"
        data = {"max_count": max_count}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json().get("data", {}).get("videos", [])

    def get_video_insights(self, video_id: str) -> dict:
        """Get insights for a specific video (requires creator permissions)."""
        # Note: TikTok insights API may require special permissions
        url = f"{self.BASE_URL}/video/query/"
        data = {"filters": {"video_ids": [video_id]}}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json().get("data", {}).get("videos", [{}])[0]


class LinkedInAPI:
    """LinkedIn API integration."""
    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_user_profile(self) -> dict:
        """Get authenticated user profile."""
        url = f"{self.BASE_URL}/me"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_organization_followers(self, org_id: str) -> dict:
        """Get organization follower statistics."""
        url = f"{self.BASE_URL}/networkSizes/{org_id}?edgeType=CompanyFollowedByMember"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_share_statistics(self, share_urn: str) -> dict:
        """Get statistics for a specific share/post."""
        url = f"{self.BASE_URL}/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={share_urn}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class XAPI:
    """X (Twitter) API v2 integration."""
    BASE_URL = "https://api.twitter.com/2"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_user_by_username(self, username: str) -> dict:
        """Get user by username."""
        url = f"{self.BASE_URL}/users/by/username/{username}"
        params = {"user.fields": "created_at,description,public_metrics,profile_image_url,verified"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", {})

    def get_user_metrics(self, user_id: str) -> dict:
        """Get user metrics."""
        url = f"{self.BASE_URL}/users/{user_id}"
        params = {"user.fields": "public_metrics"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})
        return data.get("public_metrics", {})

    def get_user_tweets(self, user_id: str, max_results: int = 10) -> list:
        """Get user's recent tweets."""
        url = f"{self.BASE_URL}/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,entities",
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_tweet_metrics(self, tweet_id: str) -> dict:
        """Get metrics for a specific tweet."""
        url = f"{self.BASE_URL}/tweets/{tweet_id}"
        params = {"tweet.fields": "public_metrics"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", {})
        return data.get("public_metrics", {})

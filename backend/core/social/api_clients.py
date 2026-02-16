import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)


class InstagramAPIClient:
    """Instagram Graph API client for metrics, followers, posts, and insights."""
    
    BASE_URL = "https://graph.instagram.com"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
        })
    
    def get_account_info(self, user_id: str) -> Dict:
        """Get basic account information."""
        url = f"{self.BASE_URL}/{user_id}"
        params = {
            "fields": "id,username,account_type,media_count,followers_count,follows_count",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Instagram API error (account info): {e}")
            raise
    
    def get_insights(self, user_id: str, metrics: List[str], period: str = "day") -> Dict:
        """Get account insights (reach, impressions, profile views, etc.)."""
        url = f"{self.BASE_URL}/{user_id}/insights"
        params = {
            "metric": ",".join(metrics),
            "period": period,
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Parse insights into normalized dict
            result = {}
            for item in data.get("data", []):
                metric_name = item["name"]
                values = item.get("values", [])
                if values:
                    result[metric_name] = values[-1].get("value", 0)
            
            return result
        except requests.RequestException as e:
            logger.error(f"Instagram API error (insights): {e}")
            raise
    
    def get_media(self, user_id: str, limit: int = 25) -> List[Dict]:
        """Get recent media posts."""
        url = f"{self.BASE_URL}/{user_id}/media"
        params = {
            "fields": "id,media_type,media_url,permalink,caption,timestamp,like_count,comments_count",
            "limit": limit,
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.RequestException as e:
            logger.error(f"Instagram API error (media): {e}")
            raise
    
    def get_media_insights(self, media_id: str) -> Dict:
        """Get insights for a specific media post."""
        url = f"{self.BASE_URL}/{media_id}/insights"
        params = {
            "metric": "reach,impressions,engagement,saved",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = {}
            for item in data.get("data", []):
                metric_name = item["name"]
                result[metric_name] = item.get("values", [{}])[0].get("value", 0)
            
            return result
        except requests.RequestException as e:
            logger.error(f"Instagram API error (media insights): {e}")
            raise
    
    def get_audience_insights(self, user_id: str) -> Dict:
        """Get audience demographics (city, country, age, gender)."""
        url = f"{self.BASE_URL}/{user_id}/insights"
        params = {
            "metric": "audience_city,audience_country,audience_gender_age",
            "period": "lifetime",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = {
                "cities": [],
                "countries": [],
                "age_gender": [],
            }
            
            for item in data.get("data", []):
                name = item["name"]
                values = item.get("values", [{}])[0].get("value", {})
                
                if name == "audience_city":
                    result["cities"] = [{"city": k, "count": v} for k, v in values.items()]
                elif name == "audience_country":
                    result["countries"] = [{"country": k, "count": v} for k, v in values.items()]
                elif name == "audience_gender_age":
                    result["age_gender"] = [{"category": k, "count": v} for k, v in values.items()]
            
            return result
        except requests.RequestException as e:
            logger.error(f"Instagram API error (audience insights): {e}")
            raise


class TikTokAPIClient:
    """TikTok API client for user info, video stats, and analytics."""
    
    BASE_URL = "https://open.tiktokapis.com/v2"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        })
    
    def get_user_info(self) -> Dict:
        """Get authenticated user info."""
        url = f"{self.BASE_URL}/user/info/"
        params = {
            "fields": "open_id,union_id,avatar_url,display_name,follower_count,following_count,video_count",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("data", {}).get("user", {})
        except requests.RequestException as e:
            logger.error(f"TikTok API error (user info): {e}")
            raise
    
    def get_video_list(self, max_count: int = 20) -> List[Dict]:
        """Get user's video list."""
        url = f"{self.BASE_URL}/video/list/"
        params = {
            "fields": "id,title,create_time,cover_image_url,share_url,view_count,like_count,comment_count,share_count",
            "max_count": max_count,
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("data", {}).get("videos", [])
        except requests.RequestException as e:
            logger.error(f"TikTok API error (video list): {e}")
            raise


class LinkedInAPIClient:
    """LinkedIn API client for profile, shares, and analytics."""
    
    BASE_URL = "https://api.linkedin.com/v2"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        })
    
    def get_profile(self) -> Dict:
        """Get authenticated user profile."""
        url = f"{self.BASE_URL}/me"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"LinkedIn API error (profile): {e}")
            raise
    
    def get_share_statistics(self, share_urn: str) -> Dict:
        """Get statistics for a specific share (post)."""
        url = f"{self.BASE_URL}/socialActions/{share_urn}/statistics"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"LinkedIn API error (share stats): {e}")
            raise


class XAPIClient:
    """X (Twitter) API v2 client for tweets, metrics, and user info."""
    
    BASE_URL = "https://api.twitter.com/2"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
        })
    
    def get_me(self) -> Dict:
        """Get authenticated user info."""
        url = f"{self.BASE_URL}/users/me"
        params = {
            "user.fields": "id,name,username,public_metrics,verified",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("data", {})
        except requests.RequestException as e:
            logger.error(f"X API error (user info): {e}")
            raise
    
    def get_user_tweets(self, user_id: str, max_results: int = 10) -> List[Dict]:
        """Get user's recent tweets."""
        url = f"{self.BASE_URL}/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "id,text,created_at,public_metrics,entities",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.RequestException as e:
            logger.error(f"X API error (tweets): {e}")
            raise
    
    def get_tweet_metrics(self, tweet_id: str) -> Dict:
        """Get metrics for a specific tweet."""
        url = f"{self.BASE_URL}/tweets/{tweet_id}"
        params = {
            "tweet.fields": "public_metrics,non_public_metrics,organic_metrics",
        }
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", {})
            return data.get("public_metrics", {})
        except requests.RequestException as e:
            logger.error(f"X API error (tweet metrics): {e}")
            raise

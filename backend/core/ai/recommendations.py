from typing import List, Dict, Optional
import logging
from django.conf import settings
import anthropic

logger = logging.getLogger(__name__)

anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if hasattr(settings, 'ANTHROPIC_API_KEY') else None


class RecommendationEngine:
    """AI-powered recommendation engine for content, posting times, and influencers."""
    
    @staticmethod
    def recommend_posting_time(
        account_id: str,
        historical_data: List[Dict]
    ) -> Dict[str, any]:
        """
        Recommend optimal posting times based on historical performance.
        
        Args:
            account_id: Social account ID
            historical_data: List of {posted_at, engagement_rate, reach}
        
        Returns:
            Dict with best_days, best_hours, confidence
        """
        if not historical_data:
            return {
                "best_days": ["monday", "wednesday", "friday"],
                "best_hours": [9, 12, 18],
                "confidence": 0.3,
            }
        
        # Aggregate performance by day and hour
        day_performance = {}
        hour_performance = {}
        
        for post in historical_data:
            posted_at = post["posted_at"]
            engagement = post["engagement_rate"]
            
            day = posted_at.strftime("%A").lower()
            hour = posted_at.hour
            
            if day not in day_performance:
                day_performance[day] = []
            day_performance[day].append(engagement)
            
            if hour not in hour_performance:
                hour_performance[hour] = []
            hour_performance[hour].append(engagement)
        
        # Calculate averages
        day_avg = {day: sum(rates) / len(rates) for day, rates in day_performance.items()}
        hour_avg = {hour: sum(rates) / len(rates) for hour, rates in hour_performance.items()}
        
        # Get top performers
        best_days = sorted(day_avg.items(), key=lambda x: x[1], reverse=True)[:3]
        best_hours = sorted(hour_avg.items(), key=lambda x: x[1], reverse=True)[:3]
        
        confidence = min(len(historical_data) / 50, 1.0)  # More data = higher confidence
        
        return {
            "best_days": [day for day, _ in best_days],
            "best_hours": [hour for hour, _ in best_hours],
            "confidence": confidence,
            "analysis": f"Based on {len(historical_data)} posts",
        }
    
    @staticmethod
    def recommend_content_topics(
        account_id: str,
        top_posts: List[Dict],
        audience_interests: List[str]
    ) -> List[Dict[str, str]]:
        """
        Recommend content topics based on past performance and audience.
        
        Returns:
            List of {topic, reasoning, estimated_engagement}
        """
        if not anthropic_client:
            return []
        
        # Prepare context
        top_captions = [post["caption"][:200] for post in top_posts[:5]]
        context = f"""
Top-performing content:
{chr(10).join(f'- {caption}' for caption in top_captions)}

Audience interests:
{', '.join(audience_interests) if audience_interests else 'General'}
"""
        
        prompt = f"""
Based on this account's top-performing content and audience interests, recommend 5 content topics that are likely to perform well.

{context}

For each topic, provide:
1. Topic title
2. Brief reasoning (why it will perform well)
3. Estimated engagement potential (high/medium/low)

Format each as:
---
TOPIC: [topic]
REASONING: [reasoning]
ENGAGEMENT: [potential]
---
"""
        
        try:
            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
            
            # Parse recommendations
            recommendations = []
            blocks = content.split("---")
            
            for block in blocks:
                if "TOPIC:" not in block:
                    continue
                
                topic = {"topic": "", "reasoning": "", "engagement": "medium"}
                for line in block.split("\n"):
                    if line.startswith("TOPIC:"):
                        topic["topic"] = line.replace("TOPIC:", "").strip()
                    elif line.startswith("REASONING:"):
                        topic["reasoning"] = line.replace("REASONING:", "").strip()
                    elif line.startswith("ENGAGEMENT:"):
                        topic["engagement"] = line.replace("ENGAGEMENT:", "").strip().lower()
                
                if topic["topic"]:
                    recommendations.append(topic)
            
            return recommendations
        
        except Exception as e:
            logger.error(f"Topic recommendation failed: {e}")
            return []
    
    @staticmethod
    def match_influencers(
        account_profile: Dict,
        potential_influencers: List[Dict],
        campaign_goal: str = "engagement"
    ) -> List[Dict[str, any]]:
        """
        Match account with relevant influencers for collaboration.
        
        Args:
            account_profile: {handle, followers, niche, audience_demographics}
            potential_influencers: List of {handle, followers, engagement_rate, niche}
            campaign_goal: engagement, reach, conversions
        
        Returns:
            Ranked list of influencer matches with scores
        """
        if not anthropic_client:
            return []
        
        context = f"""
Account profile:
- Handle: @{account_profile.get('handle')}
- Followers: {account_profile.get('followers', 0):,}
- Niche: {account_profile.get('niche', 'general')}

Campaign goal: {campaign_goal}

Potential collaborators:
{chr(10).join(f"- @{inf['handle']} ({inf.get('followers', 0):,} followers, {inf.get('engagement_rate', 0):.1f}% engagement, {inf.get('niche', 'general')} niche)" for inf in potential_influencers[:20])}
"""
        
        prompt = f"""
Analyze these potential influencer collaborations and rank the top 10 matches.

{context}

For each match, provide:
1. Influencer handle
2. Match score (0-100)
3. Key reasons for match
4. Collaboration ideas

Format:
---
INFLUENCER: @[handle]
SCORE: [score]
REASONS: [reasons]
IDEAS: [collaboration ideas]
---
"""
        
        try:
            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
            
            # Parse matches
            matches = []
            blocks = content.split("---")
            
            for block in blocks:
                if "INFLUENCER:" not in block:
                    continue
                
                match = {"handle": "", "score": 0, "reasons": "", "ideas": ""}
                for line in block.split("\n"):
                    if line.startswith("INFLUENCER:"):
                        match["handle"] = line.replace("INFLUENCER:", "").strip()
                    elif line.startswith("SCORE:"):
                        try:
                            match["score"] = int(line.replace("SCORE:", "").strip())
                        except ValueError:
                            pass
                    elif line.startswith("REASONS:"):
                        match["reasons"] = line.replace("REASONS:", "").strip()
                    elif line.startswith("IDEAS:"):
                        match["ideas"] = line.replace("IDEAS:", "").strip()
                
                if match["handle"]:
                    matches.append(match)
            
            # Sort by score
            matches.sort(key=lambda x: x["score"], reverse=True)
            return matches
        
        except Exception as e:
            logger.error(f"Influencer matching failed: {e}")
            return []

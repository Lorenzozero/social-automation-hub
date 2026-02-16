import os
from typing import List, Dict, Optional
import anthropic
import openai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize clients
anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if hasattr(settings, 'ANTHROPIC_API_KEY') else None
openai.api_key = settings.OPENAI_API_KEY if hasattr(settings, 'OPENAI_API_KEY') else None


class ContentStudioAI:
    """AI-powered content generation using Claude and GPT."""
    
    @staticmethod
    def generate_variants(
        brief: str,
        platform: str,
        tone: str = "professional",
        num_variants: int = 3,
        provider: str = "anthropic"
    ) -> List[Dict[str, str]]:
        """
        Generate multiple content variants for a platform.
        
        Args:
            brief: Content brief/topic
            platform: instagram, tiktok, linkedin, x
            tone: professional, casual, friendly, urgent, inspirational
            num_variants: Number of variants to generate (1-5)
            provider: anthropic or openai
        
        Returns:
            List of variants with text, hashtags, caption_length
        """
        # Platform-specific constraints
        platform_specs = {
            "instagram": {
                "max_length": 2200,
                "hashtag_count": 10,
                "style": "visual storytelling, emoji-friendly",
            },
            "tiktok": {
                "max_length": 2200,
                "hashtag_count": 5,
                "style": "short, punchy, trend-aware",
            },
            "linkedin": {
                "max_length": 3000,
                "hashtag_count": 3,
                "style": "professional, thought leadership",
            },
            "x": {
                "max_length": 280,
                "hashtag_count": 2,
                "style": "concise, engaging, conversation starter",
            },
        }
        
        spec = platform_specs.get(platform, platform_specs["instagram"])
        
        prompt = f"""
You are a social media content strategist. Generate {num_variants} distinct content variants for {platform.upper()}.

Brief: {brief}

Platform constraints:
- Max length: {spec['max_length']} characters
- Style: {spec['style']}
- Tone: {tone}
- Include {spec['hashtag_count']} relevant hashtags

For each variant, provide:
1. Main caption text
2. Hashtags (comma-separated)
3. Brief explanation of strategy

Variants should differ in:
- Hook/opening line
- Content structure (story, question, list, insight)
- Call-to-action

Format each variant as:
---
VARIANT X:
CAPTION: [caption text]
HASHTAGS: [hashtags]
STRATEGY: [brief explanation]
---
"""
        
        try:
            if provider == "anthropic" and anthropic_client:
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            
            elif provider == "openai" and openai.api_key:
                response = openai.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                )
                content = response.choices[0].message.content
            
            else:
                logger.error(f"AI provider {provider} not configured")
                return []
            
            # Parse response into structured variants
            variants = ContentStudioAI._parse_variants(content)
            return variants[:num_variants]
        
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return []
    
    @staticmethod
    def _parse_variants(content: str) -> List[Dict[str, str]]:
        """Parse AI response into structured variants."""
        variants = []
        blocks = content.split("---")
        
        for block in blocks:
            if "VARIANT" not in block:
                continue
            
            lines = block.strip().split("\n")
            variant = {"text": "", "hashtags": "", "strategy": ""}
            
            for i, line in enumerate(lines):
                if line.startswith("CAPTION:"):
                    # Collect caption lines until next section
                    caption_lines = [line.replace("CAPTION:", "").strip()]
                    for j in range(i + 1, len(lines)):
                        if lines[j].startswith(("HASHTAGS:", "STRATEGY:")):
                            break
                        caption_lines.append(lines[j].strip())
                    variant["text"] = " ".join(caption_lines).strip()
                
                elif line.startswith("HASHTAGS:"):
                    variant["hashtags"] = line.replace("HASHTAGS:", "").strip()
                
                elif line.startswith("STRATEGY:"):
                    variant["strategy"] = line.replace("STRATEGY:", "").strip()
            
            if variant["text"]:
                variants.append(variant)
        
        return variants
    
    @staticmethod
    def optimize_caption(
        caption: str,
        platform: str,
        optimization: str = "engagement"
    ) -> Dict[str, str]:
        """
        Optimize existing caption for better performance.
        
        Args:
            caption: Original caption
            platform: Target platform
            optimization: engagement, reach, conversions, clarity
        
        Returns:
            Optimized caption with suggestions
        """
        prompt = f"""
Optimize this {platform.upper()} caption for {optimization}:

Original:
{caption}

Provide:
1. Optimized version (maintain core message)
2. Key changes made
3. Expected impact

Format:
OPTIMIZED: [optimized caption]
CHANGES: [list of changes]
IMPACT: [expected improvement]
"""
        
        try:
            if anthropic_client:
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            else:
                return {"optimized": caption, "changes": "", "impact": ""}
            
            # Parse response
            result = {"optimized": "", "changes": "", "impact": ""}
            for line in content.split("\n"):
                if line.startswith("OPTIMIZED:"):
                    result["optimized"] = line.replace("OPTIMIZED:", "").strip()
                elif line.startswith("CHANGES:"):
                    result["changes"] = line.replace("CHANGES:", "").strip()
                elif line.startswith("IMPACT:"):
                    result["impact"] = line.replace("IMPACT:", "").strip()
            
            return result
        
        except Exception as e:
            logger.error(f"Caption optimization failed: {e}")
            return {"optimized": caption, "changes": "", "impact": ""}
    
    @staticmethod
    def suggest_hashtags(
        caption: str,
        platform: str,
        count: int = 5
    ) -> List[str]:
        """
        Suggest relevant hashtags for content.
        
        Args:
            caption: Post caption
            platform: Target platform
            count: Number of hashtags to suggest
        
        Returns:
            List of hashtag suggestions
        """
        prompt = f"""
Suggest {count} high-performing hashtags for this {platform.upper()} post:

{caption}

Criteria:
- Relevant to content
- Mix of popular and niche
- Platform-appropriate
- Trending potential

Provide only hashtags (with #), one per line.
"""
        
        try:
            if anthropic_client:
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
                hashtags = [line.strip() for line in content.split("\n") if line.strip().startswith("#")]
                return hashtags[:count]
            else:
                return []
        
        except Exception as e:
            logger.error(f"Hashtag suggestion failed: {e}")
            return []
    
    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, any]:
        """
        Analyze sentiment of text (for comments, captions).
        
        Returns:
            Dict with sentiment (positive/negative/neutral), score, emotions
        """
        prompt = f"""
Analyze the sentiment of this text:

{text}

Provide:
1. Overall sentiment: positive, negative, or neutral
2. Confidence score (0-1)
3. Primary emotions detected (comma-separated)
4. Tone: professional, casual, aggressive, supportive, etc.

Format:
SENTIMENT: [sentiment]
SCORE: [score]
EMOTIONS: [emotions]
TONE: [tone]
"""
        
        try:
            if anthropic_client:
                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
                
                result = {
                    "sentiment": "neutral",
                    "score": 0.5,
                    "emotions": [],
                    "tone": "neutral",
                }
                
                for line in content.split("\n"):
                    if line.startswith("SENTIMENT:"):
                        result["sentiment"] = line.replace("SENTIMENT:", "").strip().lower()
                    elif line.startswith("SCORE:"):
                        try:
                            result["score"] = float(line.replace("SCORE:", "").strip())
                        except ValueError:
                            pass
                    elif line.startswith("EMOTIONS:"):
                        emotions = line.replace("EMOTIONS:", "").strip()
                        result["emotions"] = [e.strip() for e in emotions.split(",")]
                    elif line.startswith("TONE:"):
                        result["tone"] = line.replace("TONE:", "").strip()
                
                return result
            else:
                return {"sentiment": "neutral", "score": 0.5, "emotions": [], "tone": "neutral"}
        
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {"sentiment": "neutral", "score": 0.5, "emotions": [], "tone": "neutral"}

import os
import logging
from typing import List, Dict
import anthropic
import openai

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


class ContentGenerator:
    """AI content generation service with multi-model support."""

    PLATFORM_CONSTRAINTS = {
        "instagram": {
            "max_caption_length": 2200,
            "max_hashtags": 30,
            "style": "Visual storytelling, emoji-friendly, engagement hooks",
        },
        "tiktok": {
            "max_caption_length": 150,
            "max_hashtags": 5,
            "style": "Short, punchy, trending language, call-to-action",
        },
        "linkedin": {
            "max_caption_length": 3000,
            "max_hashtags": 5,
            "style": "Professional, value-driven, thought leadership",
        },
        "x": {
            "max_caption_length": 280,
            "max_hashtags": 3,
            "style": "Concise, witty, conversation-starter",
        },
    }

    @staticmethod
    def generate_with_openai(brief: Dict, platform: str, variants: int = 3) -> List[Dict]:
        """Generate content variants using OpenAI GPT-4."""
        if not openai_client:
            raise ValueError("OpenAI API key not configured")

        constraints = ContentGenerator.PLATFORM_CONSTRAINTS.get(platform, {})
        
        system_prompt = f"""You are an expert social media copywriter specializing in {platform}.
Create engaging, platform-optimized content that:
- Matches the tone: {brief.get('tone', 'casual')}
- Targets audience: {brief.get('target_audience', 'general')}
- Stays within {constraints['max_caption_length']} characters
- Uses {constraints['max_hashtags']} hashtags max
- Follows {platform} best practices: {constraints['style']}

Return {variants} unique variants in JSON format:
[
  {{"caption": "...", "hashtags": ["#example", "#tags"]}},
  ...
]"""

        user_prompt = f"""Topic: {brief.get('topic', '')}
Goal: {brief.get('goal', '')}
Keywords to include: {', '.join(brief.get('keywords', []))}

Generate {variants} creative variants for {platform}."""

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            import json
            variants_data = json.loads(content)
            
            # Ensure it's a list
            if isinstance(variants_data, dict) and "variants" in variants_data:
                variants_data = variants_data["variants"]

            return [
                {
                    "caption": v["caption"],
                    "hashtags": v.get("hashtags", []),
                    "model_used": "openai/gpt-4-turbo",
                    "tokens": response.usage.total_tokens,
                }
                for v in variants_data[:variants]
            ]

        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise

    @staticmethod
    def generate_with_anthropic(brief: Dict, platform: str, variants: int = 3) -> List[Dict]:
        """Generate content variants using Anthropic Claude."""
        if not anthropic_client:
            raise ValueError("Anthropic API key not configured")

        constraints = ContentGenerator.PLATFORM_CONSTRAINTS.get(platform, {})

        prompt = f"""You are an expert social media copywriter for {platform}.

Brief:
- Topic: {brief.get('topic', '')}
- Goal: {brief.get('goal', '')}
- Tone: {brief.get('tone', 'casual')}
- Target audience: {brief.get('target_audience', 'general')}
- Keywords: {', '.join(brief.get('keywords', []))}

Platform constraints:
- Max caption length: {constraints['max_caption_length']} characters
- Max hashtags: {constraints['max_hashtags']}
- Style: {constraints['style']}

Generate {variants} unique, creative variants. Return as JSON array:
[
  {{"caption": "...", "hashtags": ["#tag1", "#tag2"]}},
  ...
]"""

        try:
            response = anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text
            
            # Extract JSON from markdown code block if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            import json
            variants_data = json.loads(content)

            return [
                {
                    "caption": v["caption"],
                    "hashtags": v.get("hashtags", []),
                    "model_used": "anthropic/claude-3.5-sonnet",
                    "tokens": response.usage.input_tokens + response.usage.output_tokens,
                }
                for v in variants_data[:variants]
            ]

        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise

    @staticmethod
    def generate_variants(brief: Dict, platform: str, model: str = "anthropic", variants: int = 3) -> List[Dict]:
        """Main entry point for content generation."""
        if model == "openai":
            return ContentGenerator.generate_with_openai(brief, platform, variants)
        elif model == "anthropic":
            return ContentGenerator.generate_with_anthropic(brief, platform, variants)
        else:
            raise ValueError(f"Unknown model: {model}")

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from core.content_studio.models import ContentBrief, ContentVariant
from core.content_studio.ai_generator import ContentGenerator
from core.workspaces.models import Workspace

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@csrf_exempt
def create_brief(request):
    """Create a new content brief and generate AI variants."""
    try:
        data = json.loads(request.body)
        workspace_id = data.get("workspace_id")
        
        workspace = Workspace.objects.get(id=workspace_id)
        
        # Create brief
        brief = ContentBrief.objects.create(
            workspace=workspace,
            created_by=request.user if request.user.is_authenticated else None,
            topic=data.get("topic", ""),
            goal=data.get("goal", ""),
            tone=data.get("tone", "casual"),
            target_audience=data.get("target_audience", ""),
            keywords=data.get("keywords", []),
            target_platforms=data.get("target_platforms", []),
        )
        
        # Generate variants for each target platform
        model = data.get("ai_model", "anthropic")  # anthropic or openai
        variants_per_platform = data.get("variants_per_platform", 3)
        
        generated_variants = []
        
        for platform in brief.target_platforms:
            try:
                variants = ContentGenerator.generate_variants(
                    brief={
                        "topic": brief.topic,
                        "goal": brief.goal,
                        "tone": brief.tone,
                        "target_audience": brief.target_audience,
                        "keywords": brief.keywords,
                    },
                    platform=platform,
                    model=model,
                    variants=variants_per_platform,
                )
                
                # Save variants to DB
                for variant_data in variants:
                    variant = ContentVariant.objects.create(
                        brief=brief,
                        platform=platform,
                        caption=variant_data["caption"],
                        hashtags=variant_data["hashtags"],
                        model_used=variant_data["model_used"],
                        generation_tokens=variant_data["tokens"],
                    )
                    generated_variants.append({
                        "id": str(variant.id),
                        "platform": variant.platform,
                        "caption": variant.caption,
                        "hashtags": variant.hashtags,
                    })
            
            except Exception as e:
                logger.error(f"Failed to generate variants for {platform}: {e}")
        
        return JsonResponse({
            "brief_id": str(brief.id),
            "variants": generated_variants,
        }, status=201)
    
    except Exception as e:
        logger.error(f"Failed to create brief: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def list_briefs(request, workspace_id):
    """List all briefs for a workspace."""
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        briefs = ContentBrief.objects.filter(workspace=workspace)
        
        results = []
        for brief in briefs:
            variants_count = brief.variants.count()
            approved_count = brief.variants.filter(is_approved=True).count()
            
            results.append({
                "id": str(brief.id),
                "topic": brief.topic,
                "goal": brief.goal[:100],
                "tone": brief.tone,
                "target_platforms": brief.target_platforms,
                "variants_count": variants_count,
                "approved_count": approved_count,
                "created_at": brief.created_at.isoformat(),
            })
        
        return JsonResponse({"briefs": results})
    
    except Exception as e:
        logger.error(f"Failed to list briefs: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def get_brief_variants(request, brief_id):
    """Get all variants for a brief."""
    try:
        brief = ContentBrief.objects.get(id=brief_id)
        variants = brief.variants.all()
        
        results = []
        for variant in variants:
            results.append({
                "id": str(variant.id),
                "platform": variant.platform,
                "caption": variant.caption,
                "hashtags": variant.hashtags,
                "model_used": variant.model_used,
                "is_approved": variant.is_approved,
                "is_published": variant.is_published,
                "created_at": variant.created_at.isoformat(),
            })
        
        return JsonResponse({
            "brief": {
                "id": str(brief.id),
                "topic": brief.topic,
                "goal": brief.goal,
            },
            "variants": results,
        })
    
    except Exception as e:
        logger.error(f"Failed to get brief variants: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["PATCH"])
@csrf_exempt
def approve_variant(request, variant_id):
    """Approve a content variant."""
    try:
        variant = ContentVariant.objects.get(id=variant_id)
        variant.is_approved = True
        variant.save()
        
        return JsonResponse({
            "id": str(variant.id),
            "is_approved": variant.is_approved,
        })
    
    except Exception as e:
        logger.error(f"Failed to approve variant: {e}")
        return JsonResponse({"error": str(e)}, status=500)

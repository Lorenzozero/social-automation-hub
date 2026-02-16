from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Avg, F, Q
from core.social.models import SocialAccount, MetricsSnapshot, FollowerChange, TopContent, AudienceInsight
from core.workspaces.models import Workspace


@require_http_methods(["GET"])
def dashboard_metrics(request, workspace_id):
    """
    Get aggregated metrics for all accounts in workspace.
    Query params: timeframe (24h, 7d, 30d, 90d)
    """
    try:
        workspace = Workspace.objects.get(id=workspace_id)
    except Workspace.DoesNotExist:
        return JsonResponse({"error": "Workspace not found"}, status=404)

    timeframe = request.GET.get("timeframe", "24h")
    timeframe_map = {
        "24h": timedelta(hours=24),
        "7d": timedelta(days=7),
        "30d": timedelta(days=30),
        "90d": timedelta(days=90),
    }
    delta = timeframe_map.get(timeframe, timedelta(hours=24))
    since = datetime.now() - delta

    accounts = SocialAccount.objects.filter(workspace=workspace, status=SocialAccount.STATUS_ACTIVE)
    
    # Get latest snapshot for each account
    latest_snapshots = []
    for account in accounts:
        snapshot = MetricsSnapshot.objects.filter(social_account=account).first()
        if snapshot:
            latest_snapshots.append({
                "account_id": str(account.id),
                "platform": account.platform,
                "handle": account.handle,
                "followers": snapshot.followers_count,
                "reach": snapshot.reach,
                "impressions": snapshot.impressions,
                "engagement": snapshot.engagement_count,
                "profile_views": snapshot.profile_views,
            })

    # Aggregate totals
    total_followers = sum(s["followers"] for s in latest_snapshots)
    total_reach = sum(s["reach"] for s in latest_snapshots)
    total_impressions = sum(s["impressions"] for s in latest_snapshots)
    total_engagement = sum(s["engagement"] for s in latest_snapshots)

    # Follower changes in timeframe
    new_followers_count = FollowerChange.objects.filter(
        social_account__workspace=workspace,
        change_type=FollowerChange.TYPE_NEW_FOLLOWER,
        timestamp__gte=since,
    ).count()

    unfollowers_count = FollowerChange.objects.filter(
        social_account__workspace=workspace,
        change_type=FollowerChange.TYPE_UNFOLLOWER,
        timestamp__gte=since,
    ).count()

    net_followers = new_followers_count - unfollowers_count

    return JsonResponse({
        "timeframe": timeframe,
        "accounts": latest_snapshots,
        "totals": {
            "followers": total_followers,
            "reach": total_reach,
            "impressions": total_impressions,
            "engagement": total_engagement,
        },
        "follower_changes": {
            "new_followers": new_followers_count,
            "unfollowers": unfollowers_count,
            "net_change": net_followers,
        },
    })


@require_http_methods(["GET"])
def follower_changes(request, account_id):
    """
    Get detailed follower/unfollower list.
    Query params: type (new_follower, unfollower), limit (default 50), offset (default 0)
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
    except SocialAccount.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)

    change_type = request.GET.get("type", FollowerChange.TYPE_NEW_FOLLOWER)
    limit = int(request.GET.get("limit", 50))
    offset = int(request.GET.get("offset", 0))

    changes = FollowerChange.objects.filter(
        social_account=account,
        change_type=change_type,
    )[offset:offset + limit]

    total_count = FollowerChange.objects.filter(
        social_account=account,
        change_type=change_type,
    ).count()

    results = []
    for change in changes:
        results.append({
            "id": str(change.id),
            "user_id": change.user_id,
            "username": change.username,
            "profile_pic_url": change.profile_pic_url,
            "verified": change.verified,
            "follower_count": change.follower_count,
            "timestamp": change.timestamp.isoformat(),
        })

    return JsonResponse({
        "account_id": str(account.id),
        "platform": account.platform,
        "handle": account.handle,
        "change_type": change_type,
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "results": results,
    })


@require_http_methods(["GET"])
def top_content(request, account_id):
    """
    Get top-performing content.
    Query params: limit (default 10), sort_by (engagement_rate, likes_count, reach)
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
    except SocialAccount.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)

    limit = int(request.GET.get("limit", 10))
    sort_by = request.GET.get("sort_by", "engagement_rate")

    content = TopContent.objects.filter(social_account=account).order_by(f"-{sort_by}")[:limit]

    results = []
    for post in content:
        results.append({
            "id": str(post.id),
            "platform_post_id": post.platform_post_id,
            "post_url": post.post_url,
            "caption": post.caption[:200] if post.caption else "",
            "media_type": post.media_type,
            "likes": post.likes_count,
            "comments": post.comments_count,
            "shares": post.shares_count,
            "saves": post.saves_count,
            "reach": post.reach,
            "engagement_rate": post.engagement_rate,
            "posted_at": post.posted_at.isoformat(),
        })

    return JsonResponse({
        "account_id": str(account.id),
        "platform": account.platform,
        "handle": account.handle,
        "sort_by": sort_by,
        "results": results,
    })


@require_http_methods(["GET"])
def audience_insights(request, account_id):
    """
    Get latest audience insights (demographics, activity patterns).
    """
    try:
        account = SocialAccount.objects.get(id=account_id)
    except SocialAccount.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)

    insight = AudienceInsight.objects.filter(social_account=account).first()

    if not insight:
        return JsonResponse({
            "account_id": str(account.id),
            "platform": account.platform,
            "handle": account.handle,
            "data": None,
        })

    return JsonResponse({
        "account_id": str(account.id),
        "platform": account.platform,
        "handle": account.handle,
        "snapshot_date": insight.snapshot_date.isoformat(),
        "demographics": {
            "age_ranges": insight.age_ranges,
            "genders": insight.genders,
            "countries": insight.countries,
            "cities": insight.cities,
        },
        "activity": {
            "active_hours": insight.active_hours,
            "active_days": insight.active_days,
        },
    })

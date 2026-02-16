# Analytics implementation (real)

This document describes how Social Automation Hub implements analytics in a **policy-safe** way.

## Key principle

Identity-level analytics (e.g., "who unfollowed") are only implemented where the platform provides an **official** endpoint for follower lists.

For platforms where follower lists are not available via official APIs, the app provides:
- `followers_count` time-series
- deltas
- correlations with content calendar (what posted before a drop)

## Unfollowers

### X (official unfollower identities)

- Endpoint: `GET https://api.x.com/2/users/{id}/followers`
- Implementation: periodic snapshots + set diff
- Storage:
  - Redis: `followers:{social_account_id}` (set of follower user IDs)
  - Postgres: `FollowerChange` rows for `new_follower` / `unfollower`

Code:
- `backend/core/social/x_api.py`
- `backend/core/social/follower_sync.py`
- Run manually: `python manage.py sync_x_followers --account <SOCIAL_ACCOUNT_UUID>`

### Instagram / LinkedIn / TikTok (delta only)

No identity-level unfollowers are produced.
Instead, implement:
- periodic `MetricsSnapshot.followers_count`
- show `delta followers` for selected time range
- show correlations with scheduled/published posts

## Next steps (to automate the command)

To run unfollower sync automatically:
- integrate `sync_x_followers_snapshot(...)` into a Celery task inside `backend/core/social/tasks.py`
- add a Celery Beat schedule to run it (e.g., every 30 minutes)

This is intentionally left as a separate follow-up change to avoid overwriting existing task modules.

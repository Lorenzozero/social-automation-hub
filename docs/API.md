# API Reference

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

All analytics endpoints require session authentication (cookies) or token authentication.

## OAuth Endpoints

### Start OAuth Flow

```http
GET /api/oauth/{platform}/authorize?workspace_id={uuid}
```

**Platforms**: `instagram`, `tiktok`, `linkedin`, `x`

**Response**: 302 redirect to platform OAuth page

### OAuth Callback

```http
GET /api/oauth/{platform}/callback?code={code}&state={state}
```

Handled automatically by platform. Redirects to frontend on success/error.

## Analytics Endpoints

### Dashboard Metrics

```http
GET /api/oauth/analytics/dashboard/{workspace_id}?timeframe={24h|7d|30d|90d}
```

**Response**:
```json
{
  "timeframe": "24h",
  "accounts": [
    {
      "account_id": "uuid",
      "platform": "instagram",
      "handle": "creator",
      "followers": 85000,
      "reach": 320000,
      "impressions": 890000,
      "engagement": 62000
    }
  ],
  "totals": {
    "followers": 125000,
    "reach": 450000,
    "impressions": 1200000,
    "engagement": 85000
  },
  "follower_changes": {
    "new_followers": 1250,
    "unfollowers": 340,
    "net_change": 910
  }
}
```

### Follower Changes

```http
GET /api/oauth/analytics/follower-changes/{account_id}?type={new_follower|unfollower}&limit=50&offset=0
```

**Response**:
```json
{
  "account_id": "uuid",
  "platform": "instagram",
  "handle": "creator",
  "change_type": "new_follower",
  "total": 1250,
  "limit": 50,
  "offset": 0,
  "results": [
    {
      "id": "uuid",
      "user_id": "12345678",
      "username": "new_follower",
      "profile_pic_url": "https://...",
      "verified": false,
      "follower_count": 5200,
      "timestamp": "2026-02-16T09:30:00Z"
    }
  ]
}
```

### Top Content

```http
GET /api/oauth/analytics/top-content/{account_id}?limit=10&sort_by={engagement_rate|likes_count|reach}
```

**Response**:
```json
{
  "account_id": "uuid",
  "platform": "instagram",
  "handle": "creator",
  "sort_by": "engagement_rate",
  "results": [
    {
      "id": "uuid",
      "platform_post_id": "123456789",
      "post_url": "https://instagram.com/p/...",
      "caption": "Amazing post...",
      "media_type": "reel",
      "likes": 15000,
      "comments": 320,
      "shares": 450,
      "saves": 890,
      "reach": 125000,
      "engagement_rate": 13.5,
      "posted_at": "2026-02-15T18:00:00Z"
    }
  ]
}
```

### Audience Insights

```http
GET /api/oauth/analytics/audience-insights/{account_id}
```

**Response**:
```json
{
  "account_id": "uuid",
  "platform": "instagram",
  "handle": "creator",
  "snapshot_date": "2026-02-16",
  "demographics": {
    "age_ranges": [
      {"range": "18-24", "count": 25000},
      {"range": "25-34", "count": 35000}
    ],
    "genders": [
      {"gender": "male", "count": 40000},
      {"gender": "female", "count": 45000}
    ],
    "countries": [
      {"country": "US", "count": 30000},
      {"country": "IT", "count": 15000}
    ],
    "cities": [
      {"city": "New York", "count": 8000},
      {"city": "Milan", "count": 5000}
    ]
  },
  "activity": {
    "active_hours": [
      {"hour": 14, "activity": 0.85},
      {"hour": 20, "activity": 0.92}
    ],
    "active_days": [
      {"day": "monday", "activity": 0.75},
      {"day": "friday", "activity": 0.95}
    ]
  }
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing/invalid params)
- `401` - Unauthorized (auth required)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

**Error format**:
```json
{
  "error": "Description of the error"
}
```

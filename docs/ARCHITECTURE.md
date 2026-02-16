# Architecture

## System Overview

Social Automation Hub is a multi-tenant SaaS platform for managing social media accounts across Instagram, TikTok, LinkedIn, and X (Twitter).

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Frontend (Next.js)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │Dashboard │  │ Calendar │  │ Analytics│  │Content Studio│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API (HTTPS)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (Django + DRF)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │Workspaces│  │  Social  │  │  Posts   │  │ Automations  │   │
│  │  + RBAC  │  │  + OAuth │  │Publishing│  │   Builder    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
│                             │                                    │
│                             ▼                                    │
│                    ┌─────────────────┐                          │
│                    │  Celery Workers │                          │
│                    │  (Async Tasks)  │                          │
│                    └─────────────────┘                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌──────────────┐ ┌──────────┐ ┌──────────────┐
    │  PostgreSQL  │ │  Redis   │ │Platform APIs │
    │  (Supabase)  │ │  (Queue) │ │ (IG/TT/LI/X) │
    └──────────────┘ └──────────┘ └──────────────┘
```

## Components

### Frontend (Next.js 15)

**Technology Stack**:
- Framework: Next.js 15 (App Router)
- Styling: Tailwind CSS + CSS variables
- State: Zustand (lightweight)
- i18n: Custom hook with JSON locales
- HTTP: fetch API (native)

**Key Pages**:
- `/dashboard` - KPI overview, follower changes
- `/calendar` - Editorial calendar with drag-drop
- `/content-studio` - AI-powered content creation
- `/inbox` - Unified comments/DM management
- `/analytics` - Deep-dive metrics and insights
- `/automations` - Workflow builder
- `/accounts` - OAuth connections
- `/settings` - Workspace, team, preferences

**State Management**:
- Theme (dark/light/system) → Zustand persist localStorage
- Language (en/it) → Zustand persist localStorage
- User session → Server-side via cookies
- Real-time updates → Supabase Realtime (optional)

### Backend (Django 5.0)

**Technology Stack**:
- Framework: Django 5.0 + Django REST Framework
- Database: PostgreSQL 14+ (Supabase)
- Queue: Celery + Redis
- Auth: Session + Token (DRF)
- Encryption: Fernet (symmetric)

**Django Apps**:

#### 1. `core.workspaces`
- **Models**: Workspace, WorkspaceMember
- **Purpose**: Multi-tenancy + RBAC (Owner, Editor, Analyst)
- **Key Features**:
  - Workspace creation and invitation
  - Role-based permissions
  - Team collaboration

#### 2. `core.social`
- **Models**: SocialAccount, OAuthToken, MetricsSnapshot, FollowerChange, TopContent, AudienceInsight
- **Purpose**: OAuth integration + Analytics
- **Key Features**:
  - OAuth 2.0 flows for 4 platforms
  - Token encryption and refresh
  - Metrics time-series storage
  - Follower tracking with enrichment
  - Top content analysis
  - Audience demographics

#### 3. `core.posts`
- **Models**: Post, PostVariant, PublishJob
- **Purpose**: Content scheduling + Publishing
- **Key Features**:
  - Draft → Approved → Scheduled → Published workflow
  - Platform-specific variants (text limits, media formats)
  - Queue-based publishing with retry
  - Idempotency (avoid duplicate posts)

#### 4. `core.automations`
- **Models**: Automation, Consent
- **Purpose**: Safe automation workflows
- **Key Features**:
  - Trigger-based workflows (new post, mention, KPI threshold)
  - Action types (create draft, send notification, request approval)
  - Consent management (X compliance)
  - Audit trail for all automations

#### 5. `core.audit`
- **Models**: Event, AuditLog
- **Purpose**: Compliance + Transparency
- **Key Features**:
  - Immutable event log
  - Actor + action + entity tracking
  - IP + timestamp for forensics
  - Export for compliance reporting

### Queue System (Celery + Redis)

**Celery Beat Schedule**:
- Every 15min: Sync metrics for all accounts
- Every 30min: Detect follower changes
- Daily 2 AM: Update top content
- Weekly Monday 3 AM: Fetch audience insights

**Task Types**:
1. **Metrics sync**: Fetch current stats from platform APIs
2. **Follower detection**: Compare snapshots to find new/unfollowers
3. **Content analysis**: Refresh top posts by engagement rate
4. **Publishing**: Execute scheduled posts
5. **Token refresh**: Renew expiring OAuth tokens

**Retry Policy**:
- Max retries: 3
- Backoff: Exponential (1s, 2s, 4s)
- On failure: Log error + alert admin

### Database (PostgreSQL)

**Key Tables**:

| Table | Purpose | Size Estimate |
|-------|---------|---------------|
| `users` | User accounts | 10K rows |
| `workspaces` | Tenant isolation | 5K rows |
| `social_accounts` | Connected profiles | 20K rows |
| `oauth_tokens` | Encrypted tokens | 20K rows |
| `metrics_snapshots` | Time-series data | 10M+ rows |
| `follower_changes` | Follower tracking | 5M+ rows |
| `posts` | Content objects | 100K rows |
| `audit_logs` | Compliance trail | 1M+ rows |

**Indexing Strategy**:
- `metrics_snapshots(social_account_id, timestamp)` - Time-series queries
- `follower_changes(social_account_id, change_type, timestamp)` - Drill-down
- `posts(workspace_id, status, scheduled_at)` - Calendar view
- `audit_logs(workspace_id, action, timestamp)` - Forensics

**Partitioning** (future optimization):
- `metrics_snapshots` by month (range partitioning)
- `audit_logs` by month (range partitioning)

### Security

**Authentication**:
- Session-based for web (Django sessions)
- Token-based for API (DRF tokens)
- OAuth 2.0 for social platforms

**Authorization**:
- RBAC via WorkspaceMember roles
- Object-level permissions (workspace boundary)
- API rate limiting (django-ratelimit)

**Encryption**:
- OAuth tokens: Fernet symmetric encryption (256-bit)
- Database: PostgreSQL SSL/TLS
- Transport: HTTPS only (HSTS enabled)

**CORS**:
- Allowed origins: Frontend URL only
- Credentials: Enabled (cookies)
- Methods: GET, POST, PUT, PATCH, DELETE

### Observability

**Logging**:
- Structured JSON logs (Django logging)
- Levels: DEBUG (dev), INFO (prod)
- Destinations: stdout + file + Sentry (errors)

**Monitoring**:
- Celery Flower: Task queue monitoring
- Django Debug Toolbar: Dev performance
- PostgreSQL slow query log: DB optimization
- Sentry: Error tracking + alerting

**Metrics** (future):
- Prometheus: Metrics collection
- Grafana: Visualization dashboards
- Alerts: Slack/Email on critical errors

## Data Flow Examples

### OAuth Connection Flow

```
1. User clicks "Connect Instagram" in frontend
2. Frontend → GET /api/oauth/instagram/authorize?workspace_id={uuid}
3. Backend generates state (workspace_id + random token)
4. Backend → 302 redirect to Meta OAuth
5. User authorizes on Meta
6. Meta → GET /api/oauth/instagram/callback?code={code}&state={state}
7. Backend validates state
8. Backend exchanges code for access_token + refresh_token
9. Backend calls Graph API to get user profile (user_id, username)
10. Backend encrypts tokens with Fernet
11. Backend saves SocialAccount + OAuthToken
12. Backend → 302 redirect to frontend?success=instagram_connected
13. Frontend shows success notification
```

### Metrics Sync Flow

```
1. Celery beat triggers sync_all_accounts_metrics (every 15min)
2. Task loops through all active SocialAccounts
3. For each account:
   a. Decrypt OAuth token
   b. Call platform API (e.g., Instagram Graph API /insights)
   c. Parse response (followers, reach, impressions, engagement)
   d. Create MetricsSnapshot record
   e. Log success/failure
4. Task completes
5. Frontend fetches updated metrics via /api/oauth/analytics/dashboard
```

### Publishing Flow

```
1. User creates post in Content Studio
2. Frontend → POST /api/posts with platform variants
3. Backend creates Post (status=draft) + PostVariant records
4. User approves post (status=approved)
5. User schedules post (status=scheduled, scheduled_at=timestamp)
6. Backend creates PublishJob
7. Celery beat checks for due jobs (every 1min)
8. When scheduled_at <= now:
   a. Task fetches PostVariant + OAuth token
   b. Task calls platform API (e.g., POST /2/tweets for X)
   c. On success: Update Post (status=published), log AuditLog
   d. On error: Retry with exponential backoff (max 3 times)
9. Frontend shows published status
```

## Scalability Considerations

### Horizontal Scaling

- **Web**: Multiple Django instances behind load balancer
- **Workers**: Multiple Celery workers (scale independently)
- **Database**: Read replicas for analytics queries
- **Cache**: Redis cluster for session + queue

### Performance Optimizations

- **Database**: Connection pooling (pgbouncer)
- **API**: Response caching (Redis)
- **Static files**: CDN (Cloudflare, CloudFront)
- **Images**: Lazy loading + WebP format
- **Queries**: Select_related, prefetch_related (N+1 elimination)

### Cost Optimization

- **Database**: Archive old metrics to cold storage (S3)
- **Workers**: Auto-scale based on queue depth
- **API**: Aggregate queries instead of per-account loops
- **Monitoring**: Sample logs instead of 100% capture

## Future Architecture Enhancements

### Microservices (when needed)

- **OAuth Service**: Isolated token management
- **Analytics Service**: Heavy data processing
- **Publishing Service**: High-throughput posting
- **Notification Service**: Email, push, webhooks

### Event-Driven Architecture

- Replace Celery with Kafka/RabbitMQ for event streaming
- Event sourcing for audit trail
- CQRS for read/write separation

### AI/ML Pipeline

- Content recommendation engine
- Optimal posting time prediction
- Sentiment analysis on comments
- Influencer matching algorithm

---

**Architecture is a living document. Update as the system evolves.**

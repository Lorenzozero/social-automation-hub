# Data Model

## Entity Relationship Diagram

```
┌──────────────┐
│    users     │
│──────────────│
│ id (PK)      │
│ email        │
│ password_hash│
│ mfa_enabled  │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────────┐
│   workspaces     │
│──────────────────│
│ id (PK)          │
│ name             │
│ owner_id (FK)    │
│ created_at       │
└──────┬───────────┘
       │
       │ 1:N
       ├─────────────────────────────────────┐
       │                                     │
       ▼                                     ▼
┌──────────────────┐              ┌──────────────────┐
│workspace_members │              │ social_accounts  │
│──────────────────│              │──────────────────│
│ id (PK)          │              │ id (PK)          │
│ workspace_id (FK)│              │ workspace_id (FK)│
│ user_id (FK)     │              │ platform         │
│ role             │              │ handle           │
└──────────────────┘              │ platform_user_id │
                                  │ status           │
                                  └──────┬───────────┘
                                         │
                                         │ 1:1
                                         ▼
                                  ┌──────────────────┐
                                  │  oauth_tokens    │
                                  │──────────────────│
                                  │ id (PK)          │
                                  │ social_account   │
                                  │   _id (FK)       │
                                  │ access_token_enc │
                                  │ refresh_token_enc│
                                  │ scopes           │
                                  │ expires_at       │
                                  └──────────────────┘
                                         │
                                         │ 1:N
                                         ├────────────┐
                                         ▼            ▼
                                  ┌──────────────────┐
                                  │metrics_snapshots │
                                  │──────────────────│
                                  │ id (PK)          │
                                  │ social_account   │
                                  │   _id (FK)       │
                                  │ timestamp        │
                                  │ followers_count  │
                                  │ reach            │
                                  │ impressions      │
                                  │ engagement_count │
                                  └──────────────────┘
```

## Tables

### users

**Purpose**: User accounts (authentication)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | User ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| mfa_enabled | BOOLEAN | DEFAULT FALSE | Two-factor auth enabled |
| created_at | TIMESTAMP | DEFAULT NOW() | Registration timestamp |
| last_login | TIMESTAMP | NULL | Last login timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (email)

---

### workspaces

**Purpose**: Multi-tenant workspace isolation

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Workspace ID |
| name | VARCHAR(255) | NOT NULL | Workspace name |
| owner_id | UUID | FK → users(id) | Workspace owner |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (owner_id)

---

### workspace_members

**Purpose**: RBAC (Role-Based Access Control)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Member ID |
| workspace_id | UUID | FK → workspaces(id) | Workspace |
| user_id | UUID | FK → users(id) | User |
| role | VARCHAR(32) | NOT NULL | owner/editor/analyst |
| joined_at | TIMESTAMP | DEFAULT NOW() | Join timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (workspace_id, user_id)
- INDEX (user_id)

---

### social_accounts

**Purpose**: Connected social media accounts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Account ID |
| workspace_id | UUID | FK → workspaces(id) | Workspace |
| platform | VARCHAR(32) | NOT NULL | instagram/tiktok/linkedin/x |
| handle | VARCHAR(255) | NOT NULL | @username |
| platform_user_id | VARCHAR(255) | NOT NULL | Platform's user ID |
| status | VARCHAR(32) | DEFAULT 'needs_review' | active/needs_review/disconnected |
| connected_at | TIMESTAMP | DEFAULT NOW() | Connection timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (workspace_id, platform, handle)
- INDEX (workspace_id)

---

### oauth_tokens

**Purpose**: Encrypted OAuth tokens

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Token ID |
| social_account_id | UUID | FK → social_accounts(id), UNIQUE | Account (1:1) |
| access_token_enc | TEXT | NOT NULL | Fernet encrypted access token |
| refresh_token_enc | TEXT | NULL | Fernet encrypted refresh token |
| scopes | TEXT | NOT NULL | Granted OAuth scopes |
| expires_at | TIMESTAMP | NULL | Token expiration |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (social_account_id)

**Security**: Tokens encrypted with Fernet before storage. Never log decrypted tokens.

---

### metrics_snapshots

**Purpose**: Time-series metrics for trend analysis

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Snapshot ID |
| social_account_id | UUID | FK → social_accounts(id) | Account |
| timestamp | TIMESTAMP | DEFAULT NOW() | Snapshot time |
| followers_count | INTEGER | DEFAULT 0 | Total followers |
| following_count | INTEGER | DEFAULT 0 | Total following |
| posts_count | INTEGER | DEFAULT 0 | Total posts |
| reach | INTEGER | DEFAULT 0 | Unique accounts reached (24h) |
| impressions | INTEGER | DEFAULT 0 | Total views (24h) |
| engagement_count | INTEGER | DEFAULT 0 | Likes + comments + shares (24h) |
| profile_views | INTEGER | DEFAULT 0 | Profile views (24h) |
| extra_data | JSONB | DEFAULT '{}' | Platform-specific metrics |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (social_account_id, timestamp DESC)

**Partitioning** (future): Range partition by timestamp (monthly)

---

### follower_changes

**Purpose**: Track individual follower/unfollower events

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Change ID |
| social_account_id | UUID | FK → social_accounts(id) | Account |
| change_type | VARCHAR(32) | NOT NULL | new_follower/unfollower |
| user_id | VARCHAR(255) | NOT NULL | Platform user ID |
| username | VARCHAR(255) | NOT NULL | @username |
| timestamp | TIMESTAMP | DEFAULT NOW() | Change timestamp |
| profile_pic_url | TEXT | NULL | Profile picture URL |
| verified | BOOLEAN | DEFAULT FALSE | Verified badge |
| follower_count | INTEGER | NULL | Their follower count (enrichment) |
| extra_data | JSONB | DEFAULT '{}' | Additional data |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (social_account_id, timestamp DESC)
- INDEX (social_account_id, change_type, timestamp DESC)

---

### top_content

**Purpose**: Top-performing posts by engagement

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Content ID |
| social_account_id | UUID | FK → social_accounts(id) | Account |
| platform_post_id | VARCHAR(255) | NOT NULL | Platform's post ID |
| post_url | TEXT | NOT NULL | Post URL |
| caption | TEXT | NULL | Post caption/text |
| media_type | VARCHAR(32) | NULL | photo/video/carousel/reel |
| likes_count | INTEGER | DEFAULT 0 | Likes |
| comments_count | INTEGER | DEFAULT 0 | Comments |
| shares_count | INTEGER | DEFAULT 0 | Shares |
| saves_count | INTEGER | DEFAULT 0 | Saves |
| reach | INTEGER | DEFAULT 0 | Unique views |
| engagement_rate | FLOAT | DEFAULT 0.0 | Engagement % |
| posted_at | TIMESTAMP | NOT NULL | Original post time |
| last_updated | TIMESTAMP | DEFAULT NOW() | Last metrics update |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (social_account_id, platform_post_id)
- INDEX (social_account_id, engagement_rate DESC)

**Formula**: `engagement_rate = ((likes + comments + shares + saves) / reach) * 100`

---

### audience_insights

**Purpose**: Audience demographics and activity patterns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Insight ID |
| social_account_id | UUID | FK → social_accounts(id) | Account |
| snapshot_date | DATE | NOT NULL | Snapshot date |
| age_ranges | JSONB | DEFAULT '[]' | `[{"range": "18-24", "count": 1234}, ...]` |
| genders | JSONB | DEFAULT '[]' | `[{"gender": "male", "count": 5000}, ...]` |
| countries | JSONB | DEFAULT '[]' | `[{"country": "US", "count": 3000}, ...]` |
| cities | JSONB | DEFAULT '[]' | `[{"city": "New York", "count": 800}, ...]` |
| active_hours | JSONB | DEFAULT '[]' | `[{"hour": 14, "activity": 0.85}, ...]` |
| active_days | JSONB | DEFAULT '[]' | `[{"day": "monday", "activity": 0.92}, ...]` |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (social_account_id, snapshot_date)
- INDEX (social_account_id, snapshot_date DESC)

---

### posts

**Purpose**: Content objects (draft → published workflow)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Post ID |
| workspace_id | UUID | FK → workspaces(id) | Workspace |
| created_by | UUID | FK → users(id) | Creator |
| status | VARCHAR(32) | DEFAULT 'draft' | draft/approved/scheduled/published/failed |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| scheduled_at | TIMESTAMP | NULL | Scheduled publish time |
| published_at | TIMESTAMP | NULL | Actual publish time |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (workspace_id, status, scheduled_at)

---

### post_variants

**Purpose**: Platform-specific post adaptations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Variant ID |
| post_id | UUID | FK → posts(id) | Post |
| platform | VARCHAR(32) | NOT NULL | instagram/tiktok/linkedin/x |
| text | TEXT | NOT NULL | Post copy |
| media_refs | JSONB | DEFAULT '[]' | Media URLs/IDs |
| metadata | JSONB | DEFAULT '{}' | Hashtags, mentions, etc. |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (post_id)

---

### publish_jobs

**Purpose**: Queue for scheduled publishing

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Job ID |
| post_variant_id | UUID | FK → post_variants(id) | Variant to publish |
| scheduled_at | TIMESTAMP | NOT NULL | When to publish |
| attempt | INTEGER | DEFAULT 0 | Retry count |
| last_error | TEXT | NULL | Last error message |
| provider_job_id | VARCHAR(255) | NULL | Platform's job ID |
| status | VARCHAR(32) | DEFAULT 'pending' | pending/running/success/failed |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (scheduled_at, status)

---

### automations

**Purpose**: Workflow automation rules

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Automation ID |
| workspace_id | UUID | FK → workspaces(id) | Workspace |
| name | VARCHAR(255) | NOT NULL | Automation name |
| enabled | BOOLEAN | DEFAULT TRUE | Active status |
| trigger | JSONB | NOT NULL | Trigger config |
| actions | JSONB | NOT NULL | Actions to execute |
| consent_required | BOOLEAN | DEFAULT FALSE | Needs user consent (X) |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (workspace_id, enabled)

---

### consents

**Purpose**: User consent for automations (X compliance)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Consent ID |
| social_account_id | UUID | FK → social_accounts(id) | Account |
| automation_id | UUID | FK → automations(id) | Automation |
| granted_at | TIMESTAMP | DEFAULT NOW() | Consent grant time |
| revoked_at | TIMESTAMP | NULL | Consent revoke time |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE (social_account_id, automation_id)

---

### events

**Purpose**: Raw event ingestion (webhooks, polling)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Event ID |
| workspace_id | UUID | FK → workspaces(id) | Workspace |
| platform | VARCHAR(32) | NOT NULL | Source platform |
| type | VARCHAR(64) | NOT NULL | Event type (new_comment, etc.) |
| payload | JSONB | NOT NULL | Raw event data |
| received_at | TIMESTAMP | DEFAULT NOW() | Ingestion time |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (workspace_id, type, received_at DESC)

---

### audit_logs

**Purpose**: Compliance and forensics trail

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Log ID |
| workspace_id | UUID | FK → workspaces(id) | Workspace |
| actor_id | UUID | FK → users(id) | Who performed action |
| action | VARCHAR(64) | NOT NULL | Action name (post.created, etc.) |
| entity_type | VARCHAR(64) | NOT NULL | Entity type (post, account, etc.) |
| entity_id | UUID | NOT NULL | Entity ID |
| timestamp | TIMESTAMP | DEFAULT NOW() | Action timestamp |
| ip_address | INET | NULL | Client IP |
| user_agent | TEXT | NULL | Client user agent |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (workspace_id, action, timestamp DESC)
- INDEX (actor_id, timestamp DESC)

**Immutability**: No UPDATE or DELETE allowed (append-only table)

---

## Migrations

All schema changes must be versioned via Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Backup Strategy

- **Daily**: Full PostgreSQL backup (Supabase automated)
- **Hourly**: Transaction log backup (PITR - Point-In-Time Recovery)
- **Retention**: 30 days for daily, 7 days for hourly
- **Testing**: Monthly restore drill

---

**Data model evolves with product. Keep this doc in sync with migrations.**

# Security & Performance Guide

## Security Hardening

### 1. Rate Limiting

#### Backend Implementation

**Global Rate Limits** (via middleware):
```python
# backend/core/middleware/rate_limit.py

# Per-endpoint limits
RATELIMIT_VIEW_RATES = {
    'oauth:start': '5/m',           # OAuth initiation
    'oauth:callback': '10/m',       # OAuth callback
    'analytics:dashboard': '30/m',  # Dashboard metrics
    'analytics:followers': '20/m',  # Follower changes
    'content:generate_ai': '10/h',  # AI content generation
    'posts:create': '50/h',         # Create posts
    'posts:publish': '20/h',        # Publish posts
    'automations:execute': '100/h', # Execute automation
}
```

**DRF Throttling** (per-user):
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',    # Anonymous users
        'user': '1000/hour',   # Authenticated users
    },
}
```

**Redis-based Rate Limiting**:
- Key format: `ratelimit:{user_id|ip}:{endpoint_hash}`
- Sliding window algorithm
- Automatic expiry after window
- Returns `429 Too Many Requests` when exceeded

#### Response Example

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

### 2. Security Headers

#### Production Headers

```python
# settings.py (production)

SECURE_SSL_REDIRECT = True              # Force HTTPS
SECURE_HSTS_SECONDS = 31536000          # HSTS 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True        # XSS protection
SECURE_CONTENT_TYPE_NOSNIFF = True      # Prevent MIME sniffing
X_FRAME_OPTIONS = 'DENY'                # Prevent clickjacking
```

#### CORS Configuration

```python
# settings.py

CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = ['content-type', 'authorization', 'x-csrf-token']
```

### 3. Token Encryption

#### Fernet Symmetric Encryption

```python
# backend/core/social/models.py

from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY').encode()
cipher = Fernet(ENCRYPTION_KEY)

class OAuthToken(models.Model):
    access_token_enc = models.BinaryField()  # Encrypted
    
    def set_access_token(self, token: str):
        """Encrypt and store token"""
        self.access_token_enc = cipher.encrypt(token.encode())
    
    def get_access_token(self) -> str:
        """Decrypt and return token"""
        return cipher.decrypt(self.access_token_enc).decode()
```

**Key Generation**:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. CSRF Protection

#### Django CSRF

```python
# settings.py

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True  # Production only
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
```

#### Frontend Implementation

```tsx
// Get CSRF token from cookie
function getCsrfToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}

// Include in POST requests
fetch('/api/posts/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCsrfToken(),
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
});
```

### 5. Password Security

#### Strong Password Requirements

```python
# settings.py

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Requirements**:
- Minimum 12 characters
- Not in common password list
- Not entirely numeric
- Not similar to user attributes

### 6. SQL Injection Prevention

**Always use Django ORM** (parameterized queries):

✅ **Safe**:
```python
FollowerChange.objects.filter(social_account=account_id, change_type='new_follower')
```

❌ **Unsafe**:
```python
FollowerChange.objects.raw(f"SELECT * FROM follower_changes WHERE account_id = {account_id}")
```

### 7. XSS Prevention

#### Backend
- Django auto-escapes template output
- Use `mark_safe()` only for trusted content

#### Frontend
```tsx
// ✅ Safe (React auto-escapes)
<p>{userInput}</p>

// ❌ Dangerous
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// Use sanitization library if needed
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

### 8. Audit Logging

#### Immutable Audit Trail

```python
# backend/core/audit/models.py

class AuditLog(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=64)  # 'post:publish', 'oauth:connect'
    entity_type = models.CharField(max_length=64)
    entity_id = models.UUIDField()
    at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    metadata = models.JSONField(default=dict)
    
    class Meta:
        indexes = [
            models.Index(fields=['workspace', '-at']),
            models.Index(fields=['actor', '-at']),
        ]
```

**Usage**:
```python
AuditLog.objects.create(
    workspace=workspace,
    actor=request.user,
    action='post:publish',
    entity_type='Post',
    entity_id=post.id,
    ip=get_client_ip(request),
    user_agent=request.META.get('HTTP_USER_AGENT'),
    metadata={'platform': 'instagram', 'scheduled_at': post.scheduled_at},
)
```

---

## Performance Optimization

### 1. Database Optimization

#### Indexing Strategy

```python
# Critical indexes

class FollowerChange(models.Model):
    class Meta:
        indexes = [
            # Fast lookup by account + type + time (covers drill-down queries)
            models.Index(fields=['social_account', 'change_type', '-timestamp']),
            
            # Fast time-range queries
            models.Index(fields=['social_account', '-timestamp']),
        ]

class MetricsSnapshot(models.Model):
    class Meta:
        indexes = [
            # Time-series queries
            models.Index(fields=['social_account', '-timestamp']),
        ]
```

#### Query Optimization

**Use select_related** (ForeignKey):
```python
# ❌ N+1 queries
for change in FollowerChange.objects.all():
    print(change.social_account.platform)  # Hits DB each time

# ✅ Single query with JOIN
for change in FollowerChange.objects.select_related('social_account'):
    print(change.social_account.platform)
```

**Use prefetch_related** (ManyToMany):
```python
Workspace.objects.prefetch_related('members__user')
```

**Use only()** (limit fields):
```python
# Only fetch needed fields
FollowerChange.objects.only('username', 'verified', 'timestamp')
```

#### Connection Pooling

```python
# settings.py

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}
```

### 2. Caching Strategy

#### Redis Cache Layers

**L1: Follower Lists** (never expire):
```python
cache_key = f"followers:{account.id}"
cache.set(cache_key, follower_ids_set, timeout=None)
```

**L2: User Metadata** (30 days):
```python
cache_key = f"user:{user_id}"
cache.set(cache_key, user_data_dict, timeout=86400*30)
```

**L3: Daily Metrics** (7 days):
```python
cache_key = f"metrics:{account.id}:{date}"
cache.set(cache_key, metrics_dict, timeout=86400*7)
```

#### View Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def dashboard_metrics(request, workspace_id):
    # ...
```

### 3. Async Processing

#### Celery Task Optimization

**Task Priorities**:
```python
@shared_task(priority=9)  # High priority (0-9, higher = more priority)
def publish_post_now(post_id):
    # Immediate publish
    pass

@shared_task(priority=5)  # Medium priority
def sync_metrics(account_id):
    # Background sync
    pass
```

**Task Retry**:
```python
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_instagram_metrics(self, account_id):
    try:
        # API call
        pass
    except APIException as exc:
        raise self.retry(exc=exc, countdown=60)  # Retry after 60s
```

**Task Timeouts**:
```python
# settings.py

CELERY_TASK_TIME_LIMIT = 30 * 60  # Hard limit: 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # Soft limit: 25 minutes (raises SoftTimeLimitExceeded)
```

### 4. Frontend Performance

#### Code Splitting

```tsx
// Lazy load heavy components
import dynamic from 'next/dynamic';

const AutomationBuilder = dynamic(() => import('./AutomationBuilder'), {
  loading: () => <SkeletonCard />,
  ssr: false,  // Disable SSR for client-only components
});
```

#### Image Optimization

```tsx
import Image from 'next/image';

<Image
  src={profilePicUrl}
  alt="Profile"
  width={48}
  height={48}
  className="rounded-full"
  loading="lazy"
  placeholder="blur"
/>
```

#### Debouncing Search

```tsx
import { useDebounce } from '@/lib/performance';

const [searchTerm, setSearchTerm] = useState('');
const debouncedSearch = useDebounce((term) => {
  fetchResults(term);
}, 500);

<input
  onChange={(e) => {
    setSearchTerm(e.target.value);
    debouncedSearch(e.target.value);
  }}
/>
```

#### Virtualization (Long Lists)

```tsx
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={followers.length}
  itemSize={64}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      <FollowerCard follower={followers[index]} />
    </div>
  )}
</FixedSizeList>
```

### 5. API Optimization

#### Pagination

```python
# Use limit/offset pagination
follower_changes = FollowerChange.objects.filter(...)[offset:offset+limit]

# Include total count
total = FollowerChange.objects.filter(...).count()

return JsonResponse({
    'total': total,
    'results': [serialize(change) for change in follower_changes],
})
```

#### Field Selection

```python
# Allow clients to request specific fields
fields = request.GET.get('fields', '').split(',')
if fields:
    queryset = queryset.only(*fields)
```

#### Compression

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Compress responses
    # ...
]
```

### 6. Monitoring & Alerts

#### Structured Logging

```python
import logging
import json

logger = logging.getLogger('core')

logger.info('Follower sync completed', extra={
    'account_id': str(account.id),
    'new_followers': len(new_follower_ids),
    'unfollowers': len(unfollower_ids),
    'duration_ms': duration * 1000,
})
```

#### Metrics Collection

```python
from django.core.cache import cache

# Increment counter
cache_key = 'metric:api_calls:today'
cache.incr(cache_key, default=0)

# Set expiry at midnight
import datetime
tonight = datetime.datetime.combine(
    datetime.date.today() + datetime.timedelta(days=1),
    datetime.time.min
)
seconds_until_midnight = (tonight - datetime.datetime.now()).seconds
cache.expire(cache_key, seconds_until_midnight)
```

#### Error Tracking (Sentry)

```python
# settings.py

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,  # 10% of transactions
        profiles_sample_rate=0.1,
    )
```

---

## Production Checklist

### Security

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` set via environment variable (not hardcoded)
- [ ] `ALLOWED_HOSTS` configured
- [ ] `ENCRYPTION_KEY` generated and set
- [ ] HTTPS enforced (`SECURE_SSL_REDIRECT = True`)
- [ ] HSTS headers enabled
- [ ] CSRF protection enabled
- [ ] Session cookies secure
- [ ] Password validators configured (min 12 chars)
- [ ] Rate limiting enabled
- [ ] CORS configured with specific origins
- [ ] Security headers set (XSS filter, nosniff, X-Frame-Options)

### Performance

- [ ] Database indexes created (`python manage.py sqlmigrate` to verify)
- [ ] Redis cache configured
- [ ] Celery workers running
- [ ] Celery beat scheduler running
- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Database connection pooling enabled
- [ ] Query optimization reviewed (no N+1)
- [ ] Frontend code splitting enabled
- [ ] Images optimized (Next.js Image component)

### Monitoring

- [ ] Structured logging configured
- [ ] Log rotation enabled (10MB max, 5 backups)
- [ ] Sentry error tracking enabled
- [ ] Metrics collection active
- [ ] Alerts configured (CPU, memory, disk, error rate)
- [ ] Backup schedule verified (daily full, hourly PITR)

### Compliance

- [ ] Audit logs enabled
- [ ] OAuth consent flow tested
- [ ] X/Twitter automation consent implemented
- [ ] GDPR data export implemented
- [ ] Data retention policy documented

---

## Incident Response

### Rate Limit Exceeded

**Symptom**: Users see `429 Too Many Requests`

**Diagnosis**:
```python
# Check Redis for rate limit keys
import redis
r = redis.from_url(os.environ['REDIS_URL'])
keys = r.keys('ratelimit:*')
for key in keys:
    print(key, r.get(key), r.ttl(key))
```

**Resolution**:
1. Identify offending user/IP
2. Increase rate limit if legitimate
3. Ban IP if abuse detected

### Token Decryption Failed

**Symptom**: `cryptography.fernet.InvalidToken` error

**Diagnosis**: `ENCRYPTION_KEY` changed or corrupt token

**Resolution**:
1. User must re-authenticate (OAuth flow)
2. Delete corrupt `OAuthToken` record
3. Verify `ENCRYPTION_KEY` environment variable

### Database Connection Pool Exhausted

**Symptom**: `OperationalError: FATAL: remaining connection slots are reserved`

**Diagnosis**: Too many concurrent connections

**Resolution**:
1. Increase PostgreSQL `max_connections`
2. Scale web dyno count
3. Review slow queries (enable `django-debug-toolbar` in staging)

---

## Resources

- [Django Security Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Celery Best Practices](https://docs.celeryproject.org/en/stable/userguide/tasks.html#tips-and-best-practices)
- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

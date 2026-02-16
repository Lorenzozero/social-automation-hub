# Deployment Guide

## Prerequisites

- PostgreSQL 14+ database
- Redis 7+ instance
- Domain with SSL certificate (Let's Encrypt recommended)
- Platform OAuth apps configured (production redirect URIs)

## Backend Deployment

### Option 1: Railway

1. **Create new project** on [railway.app](https://railway.app)

2. **Add services**:
   - PostgreSQL (auto-provisioned)
   - Redis (auto-provisioned)
   - Web service (Django)
   - Worker service (Celery worker)
   - Beat service (Celery beat)

3. **Configure Web service**:
   ```bash
   # Build Command
   pip install -r requirements.txt && python manage.py migrate
   
   # Start Command
   gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
   ```

4. **Configure Worker service**:
   ```bash
   # Start Command
   celery -A core worker -l info
   ```

5. **Configure Beat service**:
   ```bash
   # Start Command
   celery -A core beat -l info
   ```

6. **Environment variables** (all services):
   ```env
   DJANGO_SECRET_KEY=<generate-random-key>
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=<railway-postgres-url>
   CELERY_BROKER_URL=<railway-redis-url>
   CELERY_RESULT_BACKEND=<railway-redis-url>
   ENCRYPTION_KEY=<fernet-key>
   FRONTEND_URL=https://your-frontend.vercel.app
   META_APP_ID=<your-app-id>
   META_APP_SECRET=<your-app-secret>
   # ... other OAuth credentials
   ```

### Option 2: Render

Similar setup to Railway. Use Render's Web Services + Background Workers.

### Option 3: DigitalOcean App Platform

1. Connect GitHub repo
2. Configure app spec:
   ```yaml
   name: social-automation-hub
   services:
     - name: web
       build_command: pip install -r backend/requirements.txt
       run_command: gunicorn core.wsgi:application
     - name: worker
       build_command: pip install -r backend/requirements.txt
       run_command: celery -A core worker
   databases:
     - name: db
       engine: PG
   ```

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Connect GitHub repo** on [vercel.com](https://vercel.com)

2. **Framework preset**: Next.js

3. **Root directory**: `frontend`

4. **Build settings**:
   ```bash
   # Build Command (auto-detected)
   pnpm build
   
   # Output Directory
   .next
   ```

5. **Environment Variables**:
   ```env
   NEXT_PUBLIC_BACKEND_URL=https://your-backend.railway.app
   NEXT_PUBLIC_SUPABASE_URL=<your-supabase-url>
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-key>
   ```

6. **Deploy** - Auto-deploys on push to `main`

### Option 2: Netlify

Similar to Vercel. Use Netlify's Next.js plugin.

## Database Setup (Supabase)

1. **Create project** on [supabase.com](https://supabase.com)

2. **Get connection string** from Settings → Database

3. **Update backend .env** with connection string

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Enable Realtime** (optional):
   - Go to Database → Replication
   - Enable tables: `metrics_snapshots`, `follower_changes`

## OAuth Production Setup

Update all platform OAuth apps with production redirect URIs:

### Instagram (Meta)
- Redirect URI: `https://your-backend-domain.com/api/oauth/instagram/callback`

### TikTok
- Redirect URI: `https://your-backend-domain.com/api/oauth/tiktok/callback`

### LinkedIn
- Redirect URI: `https://your-backend-domain.com/api/oauth/linkedin/callback`

### X (Twitter)
- Redirect URI: `https://your-backend-domain.com/api/oauth/x/callback`

## SSL/HTTPS

- Railway/Render/Vercel: Auto-provisioned
- Custom domain: Use Cloudflare or Let's Encrypt

## Monitoring

### Logs
- **Railway**: Built-in logs viewer
- **Render**: Logs tab
- **Sentry**: Add `sentry-sdk` for error tracking

### Metrics
- **Celery Flower**: Web-based monitor for Celery
  ```bash
  celery -A core flower
  ```
- **Django Debug Toolbar**: Development only
- **Prometheus + Grafana**: Production metrics

## Backup Strategy

### Database
- **Supabase**: Automatic daily backups
- **Manual backups**:
  ```bash
  pg_dump $DATABASE_URL > backup.sql
  ```

### Media Files
- Use S3-compatible storage (AWS S3, DigitalOcean Spaces)
- Configure Django `MEDIA_ROOT` to S3

## Security Checklist

- [ ] `DJANGO_DEBUG=False` in production
- [ ] Strong `DJANGO_SECRET_KEY` (50+ random chars)
- [ ] HTTPS only (HSTS enabled)
- [ ] CORS limited to frontend origin
- [ ] OAuth redirect URIs whitelist
- [ ] Rate limiting enabled (django-ratelimit)
- [ ] Database backups scheduled
- [ ] Error monitoring (Sentry)
- [ ] Log rotation configured

## Scaling

### Horizontal Scaling
- **Web**: Add more web dynos/services
- **Workers**: Add more Celery workers
- **Database**: Use read replicas (Supabase Pro)

### Caching
- Add Redis caching layer
- Cache expensive queries (metrics aggregations)
- Use Django cache framework

### CDN
- Serve static files via CDN (Cloudflare, AWS CloudFront)
- Cache frontend assets

## Maintenance

### Updates
```bash
# Backend
pip install --upgrade -r requirements.txt
python manage.py migrate

# Frontend
pnpm update
pnpm build
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Celery Beat Schedule
Edit `core/celery_app.py` for periodic tasks schedule.

## Troubleshooting

### OAuth Redirect Mismatch
- Check redirect URI in platform developer console
- Ensure exact match (trailing slash matters)

### Database Connection Issues
- Verify `DATABASE_URL` format
- Check firewall rules (allow Railway/Render IPs)

### Celery Tasks Not Running
- Ensure Redis is accessible
- Check worker logs for errors
- Verify `CELERY_BROKER_URL` is correct

## Support

- GitHub Issues: [Report problems](https://github.com/Lorenzozero/social-automation-hub/issues)
- Discussions: [Ask questions](https://github.com/Lorenzozero/social-automation-hub/discussions)

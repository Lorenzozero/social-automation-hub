# 🇮🇹 Guida Completa in Italiano

> **Social Automation Hub: Il Manuale Per Dominare i Social Senza Vendere l'Anima**

Benvenuto nella documentazione completa in italiano del progetto. Qui trovi tutto quello che serve per capire, installare, configurare e deployare la piattaforma.

---

## 📋 Indice

1. [Introduzione](#introduzione)
2. [Architettura Sistema](#architettura-sistema)
3. [Setup Ambiente Sviluppo](#setup-ambiente-sviluppo)
4. [Configurazione OAuth](#configurazione-oauth)
5. [Modello Dati](#modello-dati)
6. [API Reference](#api-reference)
7. [Deploy in Production](#deploy-in-production)
8. [Sicurezza e Best Practices](#sicurezza-e-best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

---

## 👋 Introduzione

### Cos'è Social Automation Hub?

**TL;DR**: Piattaforma open-source per gestire Instagram, TikTok, LinkedIn e X con OAuth ufficiale, analytics real-time, scheduling, e automazioni compliance-first.

### Perché usarlo invece di Hootsuite/Buffer?

| Motivo | Social Automation Hub | SaaS Commerciali |
|--------|----------------------|------------------|
| **Costo** | $10/mese self-hosted | $99-249/mese/utente |
| **Controllo Dati** | Totale (tuo DB) | Vendor lock-in |
| **Customizzazione** | Fork e modifica | Feature request ignorata per anni |
| **Transparenza** | Open-source, audit logs | Black box |
| **Privacy** | Token encrypted nel TUO server | Chi sa cosa fanno con i tuoi dati |

### Cosa NON fa (Disclaimer Importante)

Questo tool **NON**:
- ❌ Follow/unfollow automation (ban in 48h garantito)
- ❌ Commenti spam "Amazing! 🔥🔥🔥"
- ❌ Scraping aggressivo di profili
- ❌ Bot che fingono di essere umani (siamo nel 2026, le platform hanno detection avanzato)

Questo tool **FA**:
- ✅ Scheduling multi-piattaforma con OAuth ufficiale
- ✅ Analytics avanzato (meglio di quello nativo delle app)
- ✅ Automazioni etiche (trigger-based, con consent esplicito)
- ✅ Content management centralizzato

---

## 🏛️ Architettura Sistema

### Overview High-Level

```
┌─────────────────────────────────────┐
│          FRONTEND (Next.js 15)          │
│  ┌──────────────────────────────┐  │
│  │  App Router (SSR + Client)   │  │
│  │  - Dashboard                  │  │
│  │  - Calendar                   │  │
│  │  - Analytics                  │  │
│  │  - Content Studio             │  │
│  │  - Automations                │  │
│  └──────────────────────────────┘  │
└────────────────────┬────────────────┘
                     │ REST API (JSON)
                     │
┌────────────────────┼────────────────┐
│          BACKEND (Django 5.0)           │
│  ┌──────────────────────────────┐  │
│  │  Django REST Framework       │  │
│  │  - workspaces (multi-tenant) │  │
│  │  - social (OAuth + API)      │  │
│  │  - posts (publishing)        │  │
│  │  - automations (workflows)   │  │
│  │  - audit (compliance logs)   │  │
│  └──────────────────────────────┘  │
└──────────┬──────────────────────────┘
           │
┌──────────┼──────────┐    ┌────────────────┐
│   PostgreSQL   │    │  Redis (Queue)  │
│   (Supabase)   │    │  + Celery       │
└────────────────────┘    └────────────────┘
           │
           │ OAuth 2.0 + API Calls
           │
┌──────────┼───────────────────────────┐
│  EXTERNAL SOCIAL PLATFORMS           │
│  - Instagram Graph API               │
│  - TikTok Content Posting API        │
│  - LinkedIn Share API                │
│  - X (Twitter) API v2                │
└─────────────────────────────────────┘
```

### Componenti Principali

#### 1. Frontend (Next.js 15)
- **App Router**: SSR per SEO + Client-side per interattività
- **Tailwind CSS**: Utility-first styling, tema custom con CSS variables
- **Zustand**: State management leggero (preferences, theme, user)
- **Custom i18n**: Hook personalizzato per traduzioni (en/it)

#### 2. Backend (Django 5.0)
- **DRF**: API RESTful con serializer, viewsets, permissions
- **OAuth Providers**: Implementazioni custom per ogni piattaforma
- **Celery**: Task queue per operazioni asincrone (analytics sync, scheduling)
- **Fernet Encryption**: Token social criptati con chiave simmetrica

#### 3. Database (PostgreSQL)
- **Modelli Django**: ORM per query type-safe
- **Supabase**: Postgres managed + Realtime (opzionale per live updates)
- **Migrations**: Versionamento schema con Django migrations

#### 4. Cache & Queue (Redis)
- **Celery Broker**: Code task per worker
- **Celery Result Backend**: Risultati task asincroni
- **Cache**: (Opzionale) Django cache framework per query frequenti

---

## 🛠️ Setup Ambiente Sviluppo

### Requisiti Sistema

```bash
# Verifica versioni
python --version    # 3.11+
node --version      # 18+
psql --version      # 14+
redis-cli --version # 7+
```

### Step 1: Clone Repository

```bash
git clone https://github.com/Lorenzozero/social-automation-hub.git
cd social-automation-hub
```

### Step 2: Backend Setup

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Genera encryption key per token
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# Output esempio: gAAAAABhkZ... (copia questo)

# Configura .env
cp .env.example .env
```

**Contenuto `.env` minimo**:

```bash
# Django
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (usa Supabase o Postgres locale)
DATABASE_URL=postgresql://user:password@localhost:5432/social_automation_hub

# Redis (per Celery)
REDIS_URL=redis://localhost:6379/0

# Encryption (generata sopra)
ENCRYPTION_KEY=gAAAAABhkZ...

# OAuth (configura dopo, vedi sezione OAuth)
INSTAGRAM_CLIENT_ID=
INSTAGRAM_CLIENT_SECRET=
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
X_CLIENT_ID=
X_CLIENT_SECRET=
```

**Migrazioni DB**:

```bash
python manage.py migrate
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: [scegli password strong, non "admin123"]
```

**Avvia Django**:

```bash
python manage.py runserver  # http://localhost:8000
```

**Avvia Celery** (in terminali separati):

```bash
# Terminal 2: Worker
celery -A core worker -l info

# Terminal 3: Beat (scheduler)
celery -A core beat -l info
```

### Step 3: Frontend Setup

```bash
cd ../frontend

# Dependencies (pnpm raccomandato)
pnpm install  # o npm install

# Configura .env.local
cp .env.example .env.local
```

**Contenuto `.env.local`**:

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

**Avvia Next.js**:

```bash
pnpm dev  # http://localhost:3000
```

### Step 4: Verifica Setup

1. Apri `http://localhost:3000`
2. Dovresti vedere l'onboarding wizard
3. Backend API disponibile su `http://localhost:8000/api/`
4. Admin panel Django: `http://localhost:8000/admin/`

---

## 🔑 Configurazione OAuth

### Instagram (Meta for Developers)

**Prerequisiti**:
- Account Facebook Developer
- Instagram Professional Account (Business o Creator)

**Procedura**:

1. Vai su [developers.facebook.com](https://developers.facebook.com)
2. **Crea App** → Tipo: **Business**
3. **Aggiungi Prodotti**:
   - Instagram Basic Display
   - Instagram Graph API
4. **Configura OAuth**:
   - Redirect URI: `http://localhost:8000/api/oauth/instagram/callback`
   - Deauthorize Callback: `http://localhost:8000/api/oauth/instagram/deauthorize`
5. **Copia Credenziali**:
   - App ID → `INSTAGRAM_CLIENT_ID`
   - App Secret → `INSTAGRAM_CLIENT_SECRET`

**Testa OAuth Flow**:

```bash
# Nel frontend, clicca "Connect Instagram"
# Dovresti vedere redirect a Meta OAuth
# Dopo autorizzazione, redirect a callback con token
```

### TikTok (TikTok for Developers)

**Prerequisiti**:
- Account TikTok Developer
- App approvata per Content Posting API

**Procedura**:

1. Vai su [developers.tiktok.com](https://developers.tiktok.com)
2. **Crea App**
3. **Request Content Posting API** (richiede approval)
4. **Configura OAuth**:
   - Redirect URI: `http://localhost:8000/api/oauth/tiktok/callback`
5. **Copia Credenziali**:
   - Client Key → `TIKTOK_CLIENT_KEY`
   - Client Secret → `TIKTOK_CLIENT_SECRET`

**Note**: Content Posting API richiede user consent screen compliant GDPR.

### LinkedIn (LinkedIn Developer Portal)

**Prerequisiti**:
- Account LinkedIn
- LinkedIn Developer App

**Procedura**:

1. Vai su [linkedin.com/developers](https://www.linkedin.com/developers)
2. **Crea App**
3. **Request Products**:
   - Sign In with LinkedIn
   - Share on LinkedIn
4. **Configura OAuth**:
   - Redirect URI: `http://localhost:8000/api/oauth/linkedin/callback`
5. **Copia Credenziali**:
   - Client ID → `LINKEDIN_CLIENT_ID`
   - Client Secret → `LINKEDIN_CLIENT_SECRET`

### X / Twitter (Developer Portal)

**Prerequisiti**:
- Account X Developer (Basic tier gratuito, ma con limiti)
- App con OAuth 2.0 abilitato

**Procedura**:

1. Vai su [developer.twitter.com](https://developer.twitter.com)
2. **Crea Project** → **Crea App**
3. **Configura OAuth 2.0**:
   - Type: **Web App**
   - PKCE: **Enabled**
   - Redirect URI: `http://localhost:8000/api/oauth/x/callback`
4. **Copia Credenziali**:
   - Client ID → `X_CLIENT_ID`
   - Client Secret → `X_CLIENT_SECRET`

**Compliance Note**: X richiede **transparenza** su automazioni. Il tool logga tutte le azioni automatiche in `audit` logs.

---

## 🗄️ Modello Dati

### Entity-Relationship Overview

```
User (Django Auth)
  │
  ├── WorkspaceMember ─── Workspace
  │                           │
  │                           ├── SocialAccount
  │                           │     ├── Post
  │                           │     ├── Analytics
  │                           │     └── FollowerChange
  │                           │
  │                           └── Automation
  │                                 ├── Trigger
  │                                 └── Action
  │
  └── AuditLog
```

### Modelli Principali

#### 1. **Workspace** (Multi-tenancy)
```python
class Workspace(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.CharField(choices=['FREE', 'PRO', 'ENTERPRISE'])
```

**Scopo**: Separazione clienti/progetti. Ogni workspace ha account social propri.

#### 2. **SocialAccount** (OAuth Token Storage)
```python
class SocialAccount(models.Model):
    workspace = models.ForeignKey(Workspace)
    platform = models.CharField(choices=['INSTAGRAM', 'TIKTOK', 'LINKEDIN', 'X'])
    username = models.CharField(max_length=255)
    access_token_encrypted = models.TextField()  # Fernet encrypted
    refresh_token_encrypted = models.TextField(null=True)
    expires_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
```

**Sicurezza**: Token sempre criptati con `Fernet(ENCRYPTION_KEY)`. Mai in plain text.

#### 3. **Post** (Content Scheduling)
```python
class Post(models.Model):
    workspace = models.ForeignKey(Workspace)
    social_account = models.ForeignKey(SocialAccount)
    content = models.TextField()
    media_urls = models.JSONField(default=list)
    scheduled_at = models.DateTimeField(null=True)
    published_at = models.DateTimeField(null=True)
    status = models.CharField(choices=['DRAFT', 'SCHEDULED', 'PUBLISHED', 'FAILED'])
    platform_post_id = models.CharField(max_length=255, null=True)
```

#### 4. **Analytics** (Metrics Storage)
```python
class Analytics(models.Model):
    social_account = models.ForeignKey(SocialAccount)
    post = models.ForeignKey(Post, null=True)  # null = account-level metrics
    metric_type = models.CharField()  # 'REACH', 'IMPRESSIONS', 'ENGAGEMENT'
    value = models.BigIntegerField()
    recorded_at = models.DateTimeField()
```

#### 5. **Automation** (Workflow Engine)
```python
class Automation(models.Model):
    workspace = models.ForeignKey(Workspace)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    trigger_type = models.CharField()  # 'NEW_POST', 'MENTION', 'KPI_THRESHOLD'
    trigger_config = models.JSONField()
    action_type = models.CharField()  # 'SEND_NOTIFICATION', 'POST_CONTENT'
    action_config = models.JSONField()
```

---

## 📡 API Reference

### Base URL
```
http://localhost:8000/api/
```

### Authentication

Tutte le API (tranne OAuth callbacks) richiedono **Django Session Auth** o **Token Auth**.

```bash
# Login
POST /api/auth/login
{
  "username": "admin",
  "password": "password123"
}

# Response
{
  "user_id": 1,
  "username": "admin",
  "workspaces": [1, 2]
}
```

### OAuth Endpoints

#### Inizia OAuth Flow
```bash
GET /api/oauth/{platform}/authorize?workspace_id=1

# Platforms: instagram | tiktok | linkedin | x
# Redirect a piattaforma OAuth
```

#### Callback (automatico)
```bash
GET /api/oauth/{platform}/callback?code=xxx&state=yyy

# Gestito automaticamente dal backend
# Salva token criptati in DB
# Redirect a frontend con success/error
```

### Analytics Endpoints

#### Dashboard Aggregato
```bash
GET /api/analytics/dashboard/{workspace_id}

# Response
{
  "total_reach": 150000,
  "total_impressions": 300000,
  "total_engagement": 12000,
  "follower_growth": 340,
  "accounts": [
    {
      "platform": "INSTAGRAM",
      "username": "@example",
      "reach": 80000,
      "followers": 5430
    }
  ]
}
```

#### Follower Changes
```bash
GET /api/analytics/follower-changes/{account_id}?date_from=2026-02-01&date_to=2026-02-18

# Response
{
  "new_followers": [
    {"username": "user1", "followed_at": "2026-02-15T10:30:00Z"},
    {"username": "user2", "followed_at": "2026-02-16T14:20:00Z"}
  ],
  "unfollowers": [
    {"username": "user3", "unfollowed_at": "2026-02-17T09:15:00Z"}
  ]
}
```

#### Top Content
```bash
GET /api/analytics/top-content/{account_id}?limit=10&metric=engagement

# Response
{
  "posts": [
    {
      "post_id": 123,
      "content": "Post text...",
      "engagement": 450,
      "reach": 12000,
      "published_at": "2026-02-10T12:00:00Z"
    }
  ]
}
```

### Post Endpoints

#### Crea Post (Draft)
```bash
POST /api/posts
{
  "workspace_id": 1,
  "social_account_id": 5,
  "content": "Testo del post...",
  "media_urls": ["https://example.com/image.jpg"],
  "scheduled_at": "2026-02-20T15:00:00Z",
  "status": "SCHEDULED"
}

# Response
{
  "post_id": 456,
  "status": "SCHEDULED",
  "scheduled_at": "2026-02-20T15:00:00Z"
}
```

#### Lista Post
```bash
GET /api/posts?workspace_id=1&status=SCHEDULED

# Response
{
  "posts": [
    {"id": 456, "content": "...", "scheduled_at": "..."}
  ]
}
```

---

## 🚀 Deploy in Production

### Opzione 1: Railway (Raccomandato)

**Backend**:

1. Crea account su [Railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub**
3. Seleziona repository `social-automation-hub`
4. Railway rileva automaticamente `backend/` come Django app
5. **Aggiungi Services**:
   - PostgreSQL (Railway Marketplace)
   - Redis (Railway Marketplace)
6. **Configura Environment Variables**:
   ```
   SECRET_KEY=...
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   ENCRYPTION_KEY=...
   INSTAGRAM_CLIENT_ID=...
   # etc.
   ```
7. **Deploy**: Railway auto-deploya su push a `main`

**Celery Worker** (Railway Service separato):

```yaml
# railway.json (nella root del repo)
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "celery -A core worker -l info",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

**Celery Beat** (Railway Service separato):

```yaml
# railway-beat.json
{
  "deploy": {
    "startCommand": "celery -A core beat -l info"
  }
}
```

**Frontend (Vercel)**:

1. Crea account su [Vercel.com](https://vercel.com)
2. **New Project** → Import da GitHub
3. Root Directory: `frontend/`
4. Framework Preset: **Next.js**
5. **Environment Variables**:
   ```
   NEXT_PUBLIC_BACKEND_URL=https://your-backend.railway.app
   ```
6. Deploy automatico su push

### Opzione 2: Docker Compose (Self-Hosted)

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: social_automation_hub
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    command: gunicorn core.wsgi:application --bind 0.0.0.0:8000
    environment:
      DATABASE_URL: postgresql://postgres:your_secure_password@db:5432/social_automation_hub
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: your_secret_key
      ENCRYPTION_KEY: your_encryption_key
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"

  celery_worker:
    build: ./backend
    command: celery -A core worker -l info
    environment:
      DATABASE_URL: postgresql://postgres:your_secure_password@db:5432/social_automation_hub
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery_beat:
    build: ./backend
    command: celery -A core beat -l info
    environment:
      DATABASE_URL: postgresql://postgres:your_secure_password@db:5432/social_automation_hub
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_BACKEND_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

**Avvia**:

```bash
docker-compose up -d
```

---

## 🛡️ Sicurezza e Best Practices

### 1. Token Encryption

**Problema**: OAuth token in plain text = disaster se DB leak.

**Soluzione**: Fernet symmetric encryption.

```python
from cryptography.fernet import Fernet

cipher = Fernet(settings.ENCRYPTION_KEY)
encrypted_token = cipher.encrypt(access_token.encode())

# Decrypt quando serve
decrypted_token = cipher.decrypt(encrypted_token).decode()
```

### 2. Environment Variables

**Mai committare**:
- `.env`
- `secrets.json`
- File con credentials

**Usa `.gitignore`**:
```
.env
.env.local
*.log
__pycache__/
db.sqlite3
```

### 3. HTTPS in Production

**Obbligatorio** per:
- OAuth callbacks (requirement piattaforme)
- Protezione token in transit
- SEO (Google penalizza HTTP)

**Soluzione**: Let's Encrypt (gratis) o CloudFlare Proxy.

### 4. Rate Limiting

TODO: Implementare `django-ratelimit` per endpoint API.

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='10/m', method='POST')
def post_create(request):
    # ...
```

### 5. Audit Logs

Ogni automazione logga:
- Chi (user_id)
- Cosa (action_type)
- Quando (timestamp)
- Perché (trigger_config)

Compliance X/Twitter richiede transparenza totale.

---

## 🔧 Troubleshooting

### Problema: "OAuth callback failed"

**Causa**: Redirect URI mismatch.

**Soluzione**:
1. Verifica URI in piattaforma OAuth sia **esatto** (include http/https, porta)
2. Controlla logs Django per dettagli errore
3. Testa con Postman/cURL per isolare frontend/backend

### Problema: "Celery tasks non partono"

**Causa**: Redis non connesso o Celery worker offline.

**Soluzione**:
```bash
# Verifica Redis
redis-cli ping  # Deve rispondere "PONG"

# Verifica Celery worker
celery -A core inspect active  # Lista task attivi

# Restart worker con debug
celery -A core worker -l debug
```

### Problema: "Token expired" dopo giorni

**Causa**: Access token scaduto, refresh token non implementato correttamente.

**Soluzione**:
1. Implementa refresh token logic in `social/oauth_providers.py`
2. Celery task periodico per refresh token prima scadenza

### Problema: "Analytics vuoti"

**Causa**: Sync non eseguito o API call fallita.

**Soluzione**:
1. Triggera manualmente sync:
   ```python
   from core.social.tasks import sync_analytics
   sync_analytics.delay(social_account_id=1)
   ```
2. Check Celery logs per errori API
3. Verifica scopes OAuth (potrebbero mancare permessi analytics)

---

## 🤝 Contributing

### Come Contribuire

1. **Fork** repository
2. **Branch** per feature: `git checkout -b feature/nome-feature`
3. **Commit** con Conventional Commits:
   ```
   feat: add LinkedIn video support
   fix: resolve token refresh bug
   docs: update Italian guide
   ```
4. **Push**: `git push origin feature/nome-feature`
5. **Pull Request** con descrizione dettagliata

### Cosa Contribuire

**High Priority**:
- Nuove piattaforme (YouTube, Pinterest, Threads)
- AI content generation (integration OpenAI/Anthropic)
- Mobile app (React Native)
- Test coverage (attualmente <50%)

**Medium Priority**:
- i18n altre lingue (ES, FR, DE)
- Export reports (PDF/CSV)
- Real-time dashboard (WebSocket)

**Docs**:
- Tutorial video
- Traduzioni
- Use case examples

---

## 📞 Supporto

- **GitHub Issues**: [Report bugs](https://github.com/Lorenzozero/social-automation-hub/issues)
- **Discussions**: [Ask questions](https://github.com/Lorenzozero/social-automation-hub/discussions)
- **Email**: support@example.com (per richieste private)

---

## 🙏 Conclusioni

Hai completato la guida! Ora dovresti essere in grado di:
- ✅ Capire l'architettura del sistema
- ✅ Configurare ambiente sviluppo
- ✅ Setupare OAuth per tutte le piattaforme
- ✅ Usare le API
- ✅ Deployare in production
- ✅ Contribuire al progetto

**Prossimi Step**:
1. Connetti i tuoi account social
2. Schedula i primi post
3. Esplora analytics dashboard
4. Crea automazioni custom
5. Contribuisci con feedback/PR!

---

**Built with 💻 by Lorenzo & the community.**

**Per domande o dubbi, apri un issue su GitHub!**

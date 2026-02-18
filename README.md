# 🎭 Social Automation Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Professional social media management platform** with multi-platform integration, advanced analytics, content scheduling, and compliant automation workflows.

**Open-source** solution for creators, influencers, and agencies to manage Instagram, TikTok, LinkedIn, and X (Twitter) with enterprise-grade features, OAuth 2.0 security, and transparent automation compliance.

🇮🇹 **[Leggi in Italiano](README.it.md)** | 🇬🇧 English (current)

---

## ✨ Why Social Automation Hub?

### ✅ Built For
- **Creators & Influencers**: Automate workflows without risking platform bans
- **Social Media Managers**: Manage multiple clients with centralized analytics
- **Digital Agencies**: White-label solution with multi-workspace support
- **Tech Teams**: Self-hosted, customizable, full API access

### 🚀 Key Differentiators
| Feature | Social Automation Hub | Traditional SaaS |
|---------|----------------------|------------------|
| **Cost** | $10/month self-hosted | $99-249/month per user |
| **Data Ownership** | Full control | Vendor-locked |
| **Customization** | Fork & modify | Limited |
| **Compliance** | Transparent audit logs | Black box |
| **OAuth Security** | Official APIs only | Often mixed with scraping |

---

## 🔥 Features

### 🌐 Multi-Platform Integration

| Platform | API Type | Capabilities | Rate Limits | Status |
|----------|----------|--------------|-------------|--------|
| **Instagram** | Graph API | Posts, Stories, Reels, Analytics | 100 posts/24h | ✅ |
| **TikTok** | Content Posting API | Video posts with user consent | Platform-dependent | ✅ |
| **LinkedIn** | UGC Posts API | Text/media posts, analytics | Standard limits | ✅ |
| **X (Twitter)** | OAuth 2.0 + API v2 | Posts, threads, analytics | Tier-based | ✅ |

**Note**: All integrations use official OAuth 2.0 flows. No scraping, no credential storage in plain text.

### 📊 Advanced Analytics

- **Real-Time Dashboard**: Aggregated KPIs (reach, impressions, engagement, follower growth)
- **Follower/Unfollower Tracking**: Identify who follows/unfollows with enrichment data
- **Top-Performing Content**: Analyze best posts by engagement, reach, and conversion
- **Audience Insights**: Demographics, location, activity patterns, device types
- **Time-Series Metrics**: Historical trends with configurable date ranges
- **Cross-Platform Correlation**: Understand how content performs across channels

### 📅 Content Management

- **Editorial Calendar**: Visual scheduling with drag-drop interface
- **AI-Powered Content Creation**: Multi-variant generation with platform-specific adaptations
- **Manual Approval Workflows**: Draft-first approach with review stages
- **Platform-Specific Formatting**: Automatic hashtag, mention, and character limit handling
- **Media Library**: Centralized asset management with tagging and search

### ⚙️ Safe Automations

- **Trigger-Based Workflows**: Event-driven actions (new post, mentions, KPI thresholds)
- **Explicit Consent Management**: X/Twitter compliance with user-initiated flows
- **Full Audit Logs**: Transparency for all automated actions (who, what, when, why)
- **Policy Engine**: Platform-specific rate limits and rules enforcement
- **No Spam**: Designed to prevent ban-triggering behaviors (no follow/unfollow bots)

### 🎨 Professional UX

- **Minimal Design**: Influencer-friendly interface with focus on content, not clutter
- **i18n Support**: English + Italian (extensible to other languages)
- **Theme System**: Dark/Light/System modes with smooth transitions
- **Responsive Layout**: Optimized for desktop, tablet, and mobile
- **Micro-Interactions**: Smooth animations and feedback for better UX

---

## 💻 Tech Stack

### Backend
```yaml
Framework:     Django 5.0 + Django REST Framework
Database:      PostgreSQL 14+ (Supabase recommended)
Task Queue:    Celery 5.3 + Redis 7+
Authentication: OAuth 2.0 (all platforms)
Encryption:    Fernet symmetric encryption for tokens
API Design:    RESTful with OpenAPI/Swagger docs
```

### Frontend
```yaml
Framework:     Next.js 15 (App Router)
Styling:       Tailwind CSS 3 + CSS variables
State:         Zustand 5 (lightweight, no Redux boilerplate)
i18n:          Custom hook with JSON locales
HTTP Client:   Fetch API with error handling
```

### Infrastructure
```yaml
Production:    Railway/Render (backend), Vercel/Netlify (frontend)
Database:      Supabase (managed Postgres + Realtime)
Cache/Queue:   Redis (Upstash free tier supported)
Monitoring:    Sentry (errors), LogRocket (sessions) [optional]
```

---

## 🚀 Quick Start

### Prerequisites

```bash
✅ Python 3.11+
✅ Node.js 18+ (LTS)
✅ PostgreSQL 14+
✅ Redis 7+
```

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Configure environment
cp .env.example .env
# Edit .env with:
# - DATABASE_URL (PostgreSQL connection string)
# - REDIS_URL
# - SECRET_KEY (generated above)
# - OAuth credentials (see OAuth Setup below)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Django development server
python manage.py runserver  # http://localhost:8000
```

**In separate terminals**:

```bash
# Terminal 2: Celery worker
celery -A core worker -l info

# Terminal 3: Celery beat (scheduler)
celery -A core beat -l info
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install  # or npm install

# Configure environment
cp .env.example .env.local
# Set: NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Start Next.js development server
pnpm dev  # http://localhost:3000
```

**Open browser** → `http://localhost:3000` → Complete onboarding guide.

---

## 🔑 OAuth Setup

Create developer applications on each platform:

### Instagram (Meta for Developers)

1. Visit [developers.facebook.com](https://developers.facebook.com)
2. Create App → Select **Business** type
3. Add Products: **Instagram Basic Display** + **Instagram Graph API**
4. Copy **App ID** and **App Secret** to `.env`:
   ```
   INSTAGRAM_CLIENT_ID=your_app_id
   INSTAGRAM_CLIENT_SECRET=your_app_secret
   ```
5. Add Redirect URI: `http://localhost:8000/api/oauth/instagram/callback`

### TikTok (TikTok for Developers)

1. Visit [developers.tiktok.com](https://developers.tiktok.com)
2. Create App → Enable **Content Posting API**
3. Copy **Client Key** and **Client Secret** to `.env`
4. Add Redirect URI: `http://localhost:8000/api/oauth/tiktok/callback`

### LinkedIn (LinkedIn Developer Portal)

1. Visit [linkedin.com/developers](https://www.linkedin.com/developers)
2. Create App → Request **Sign In with LinkedIn** + **Share on LinkedIn**
3. Copy **Client ID** and **Client Secret** to `.env`
4. Add Redirect URI: `http://localhost:8000/api/oauth/linkedin/callback`

### X / Twitter (Developer Portal)

1. Visit [developer.twitter.com](https://developer.twitter.com)
2. Create Project → Create App
3. Enable **OAuth 2.0** (Type: Web App, PKCE: enabled)
4. Copy **Client ID** and **Client Secret** to `.env`
5. Add Redirect URI: `http://localhost:8000/api/oauth/x/callback`

**Production Note**: Replace `http://localhost:8000` with your production domain (must be HTTPS).

---

## 📁 Project Structure

```
social-automation-hub/
├── backend/
│   ├── core/
│   │   ├── workspaces/      # Multi-tenancy + RBAC
│   │   ├── social/          # OAuth + Analytics engine
│   │   ├── posts/           # Publishing + Scheduling
│   │   ├── automations/     # Workflow builder
│   │   └── audit/           # Compliance logs
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── app/
│   │   ├── dashboard/       # KPI overview
│   │   ├── calendar/        # Editorial calendar
│   │   ├── content-studio/  # AI content generation
│   │   ├── inbox/           # Unified comments/DM
│   │   ├── analytics/       # Deep-dive reports
│   │   ├── automations/     # Workflow builder UI
│   │   ├── accounts/        # Social account management
│   │   └── settings/        # Workspace settings
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/             # Utilities + i18n
│   │   └── styles/          # Global CSS
│   └── package.json
├── docs/                    # Technical documentation
├── README.md                # This file
└── README.it.md             # Italian version (satirical tone)
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, module structure, data flow |
| [DATA_MODEL.md](docs/DATA_MODEL.md) | Database schema with ER diagrams |
| [DESIGN_GUIDELINES.md](docs/DESIGN_GUIDELINES.md) | UX/UI principles and component library |
| [API.md](docs/API.md) | Complete REST API reference with examples |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Contribution guidelines and workflow |
| [SECURITY_PERFORMANCE.md](docs/SECURITY_PERFORMANCE.md) | Security best practices and optimization tips |

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with clear, atomic commits
4. Write/update tests if applicable
5. Update documentation if needed
6. Push to your fork: `git push origin feature/amazing-feature`
7. Open Pull Request with detailed description

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat:      New feature
fix:       Bug fix
docs:      Documentation changes
style:     Code formatting (no logic change)
refactor:  Code refactoring
test:      Adding or updating tests
chore:     Build process or tooling changes
```

### Code Style

**Python**:
- Use `black` formatter (line length 100)
- Sort imports with `isort`
- Lint with `flake8`
- Type hints encouraged

**TypeScript**:
- ESLint + Prettier
- No `any` types (use `unknown` and narrow)
- Functional components with hooks
- Descriptive variable names

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

---

## 🛡️ Security

### Implemented Protections

- ✅ **OAuth 2.0**: Official platform APIs, no credential storage
- ✅ **Token Encryption**: Fernet symmetric encryption for all tokens
- ✅ **CSRF Protection**: Django built-in CSRF middleware
- ✅ **CORS**: Configured for frontend origin only (no wildcard `*`)
- ✅ **SQL Injection**: Protected via Django ORM (no raw queries)
- ✅ **Environment Variables**: Secrets in `.env`, never committed
- ✅ **Audit Logs**: All automated actions logged with user attribution

### Planned Enhancements

- 🚧 Rate limiting per user/workspace (via `django-ratelimit`)
- 🚧 Two-factor authentication (2FA) for admin accounts
- 🚧 IP whitelisting for API endpoints

### Report Security Issues

**Found a vulnerability?** → Email: `security@example.com`

**Do NOT** open public GitHub issues for security bugs. Responsible disclosure ensures user safety.

---

## 📊 Roadmap

### ✅ Completed (v1.0)
- Multi-platform OAuth flows
- Advanced analytics dashboard
- Follower/unfollower tracking
- Theme switcher + i18n
- Onboarding wizard

### 🚧 In Progress (Q1-Q2 2026)
- **Content Studio AI**: OpenAI/Anthropic integration for multi-variant content
- **Automation Builder UI**: Visual drag-drop workflow editor
- **Unified Inbox**: Centralized view for comments and DMs across platforms
- **Real-Time Sync**: Celery tasks for automatic metric updates (5min intervals)

### 🔮 Future (Q3-Q4 2026)
- Export reports (CSV/PDF) for client delivery
- Team collaboration features (comments, multi-step approval)
- Mobile app (React Native)
- Additional platform integrations (YouTube, Pinterest)

---

## 🚀 Deployment

### Backend (Django + Celery)

**Recommended Platforms**:
- [Railway](https://railway.app) → 1-click deploy, $5/month starter plan
- [Render](https://render.com) → Free tier available (with sleep on inactivity)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform) → $5/month, no sleep

**Requirements**:
- 1 web service (Gunicorn)
- 1 worker service (Celery worker)
- 1 scheduler service (Celery beat)
- PostgreSQL database
- Redis instance

### Frontend (Next.js)

**Recommended Platforms**:
- [Vercel](https://vercel.com) → Zero-config, free for hobby projects
- [Netlify](https://www.netlify.com) → Alternative with similar features

**Build Command**: `pnpm build`

**Environment Variables**:
```
NEXT_PUBLIC_BACKEND_URL=https://your-backend.railway.app
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
```

### Database

- [Supabase](https://supabase.com) → Free tier: 500MB storage, 2GB bandwidth
- [AWS RDS](https://aws.amazon.com/rds/) → Production-grade, scalable
- [DigitalOcean Managed Databases](https://www.digitalocean.com/products/managed-databases) → $15/month

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for step-by-step production setup.

---

## 💰 Cost Comparison

### Self-Hosted (Minimal Setup)
```
Railway (web + worker):   $10/month
Supabase (free tier):     $0/month
Vercel (frontend):        $0/month
Redis (Upstash free):     $0/month
────────────────────────────
TOTAL:                    ~$10/month
```

### SaaS Alternatives
```
Hootsuite Professional:   $99/month
Buffer Business:          $99/month
Later Growth:             $80/month
Sprout Social Standard:   $249/month
```

**Annual Savings**: `$1,068 - $2,868` vs. commercial SaaS

---

## ❓ FAQ

### Can I use this for client work?
Yes! MIT license allows commercial use, modification, and distribution. Attribution appreciated but not required.

### Do I need Business accounts on social platforms?
- **Instagram**: Yes, requires Professional Account (free upgrade)
- **TikTok**: No, personal accounts supported
- **LinkedIn**: No, personal accounts supported
- **X/Twitter**: No, personal accounts supported

### Will I get banned for using automation?
No, if you follow best practices:
- Use official OAuth APIs (no scraping)
- Respect rate limits
- No spam behaviors (follow/unfollow bots, generic comments)
- Maintain audit logs (required for X/Twitter transparency)

**You WILL get banned if**: You modify the tool for spam or violate platform ToS.

### How technical do I need to be?
**Minimal**: Basic command line, environment variable configuration
**Moderate**: Code customization requires Django/Next.js knowledge

Deployment platforms like Railway and Vercel offer 1-click deploys with minimal setup.

### Can I add more platforms?
Yes! Create a new OAuth provider in `backend/core/social/providers/`. Contributions via Pull Request are welcome.

---

## 🌟 Star This Repo If You:

- ✅ Want to support open-source social media tools
- ✅ Believe SaaS alternatives are overpriced
- ✅ Value data ownership and transparency
- ✅ Plan to use or contribute to this project

**Community Goal**: 1,000 stars by Q2 2026. Help us reach it by sharing!

---

## 📞 Community & Support

- **GitHub Repository**: [Lorenzozero/social-automation-hub](https://github.com/Lorenzozero/social-automation-hub)
- **Issue Tracker**: [Report Bugs](https://github.com/Lorenzozero/social-automation-hub/issues)
- **Discussions**: [Ask Questions](https://github.com/Lorenzozero/social-automation-hub/discussions)
- **X/Twitter**: Tag `@socialautohub` (if exists)

---

## 🙏 Acknowledgments

- **Meta** for Instagram Graph API
- **TikTok** for Content Posting API
- **LinkedIn** for Share on LinkedIn API
- **X (Twitter)** for API v2
- **Supabase** for managed PostgreSQL
- **Next.js**, **Tailwind CSS**, **Django** teams
- Open-source community contributors

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for full text.

Permissions: Commercial use, modification, distribution, private use.

---

**Built with ❤️ by the community for creators, influencers, and agencies.**

**⭐ Star this repo to support open-source social media automation! ⭐**

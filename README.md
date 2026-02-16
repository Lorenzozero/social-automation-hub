# Social Automation Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)

Piattaforma open-source per la gestione professionale dei social (monitoraggio, publishing, inbox, automazioni "safe" e compliance) pensata per creator, influencer e agency.

## 🚀 Features

### Multi-Platform Integration
- **Instagram**: Professional accounts, Graph API, 100 posts/24h limit
- **TikTok**: Content Posting API with UX consent requirements
- **LinkedIn**: UGC Posts with member/org social permissions
- **X (Twitter)**: OAuth 2.0 with PKCE, transparent automation rules

### Advanced Analytics
- 📊 Real-time KPI dashboard (reach, impressions, engagement)
- 👥 Follower/unfollower tracking with enrichment data
- 🏆 Top-performing content analysis
- 🌍 Audience insights (demographics, activity patterns)
- 📈 Time-series metrics with trend analysis
- 🔗 Cross-platform correlation and triage

### Content Management
- 📅 Editorial calendar with scheduling
- ✨ AI-powered multi-variant content creation
- ✅ Manual approval workflows (draft-first)
- 📝 Platform-specific adaptations

### Safe Automations
- ⚙️ Trigger-based workflows (new post, mentions, KPI thresholds)
- 🔒 Explicit consent management (X compliance)
- 📄 Full audit logs for transparency
- ⚠️ Policy engine (rate limits, platform rules)

### Professional UX
- 🎨 Minimal, influencer-friendly design
- 🌍 i18n support (English, Italian)
- 🌑 Dark/light/system theme
- 📱 Responsive mobile/desktop
- ⚡ Smooth animations and micro-interactions

## 💻 Stack

### Backend
- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL (Supabase managed)
- **Queue**: Celery + Redis
- **Auth**: OAuth 2.0 (all platforms)
- **Security**: Fernet encryption for tokens

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Styling**: Tailwind CSS + CSS variables
- **State**: Zustand (preferences, theme)
- **i18n**: Custom hook with JSON locales

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Configure .env (see .env.example)
cp .env.example .env
# Edit .env with your credentials

# Run migrations
python manage.py migrate
python manage.py createsuperuser

# Start server
python manage.py runserver

# Start Celery worker (separate terminal)
celery -A core worker -l info

# Start Celery beat (separate terminal)
celery -A core beat -l info
```

### Frontend Setup

```bash
cd frontend
pnpm install  # or npm install

# Configure .env.local
cp .env.example .env.local
# Set NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

pnpm dev  # or npm run dev
```

Visit `http://localhost:3000` and start the onboarding guide!

## 🔑 OAuth Setup

Create developer apps on each platform:

### Instagram (Meta)
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create App → Business type
3. Add **Instagram Basic Display** + **Instagram Graph API**
4. Copy App ID and App Secret to `.env`
5. Add redirect URI: `http://localhost:8000/api/oauth/instagram/callback`

### TikTok
1. Go to [developers.tiktok.com](https://developers.tiktok.com)
2. Create app and add **Content Posting API**
3. Copy Client Key and Client Secret to `.env`
4. Add redirect URI: `http://localhost:8000/api/oauth/tiktok/callback`

### LinkedIn
1. Go to [linkedin.com/developers](https://www.linkedin.com/developers)
2. Create app and request **Sign In** + **Share on LinkedIn**
3. Copy Client ID and Client Secret to `.env`
4. Add redirect URI: `http://localhost:8000/api/oauth/linkedin/callback`

### X (Twitter)
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Create Project → Create App
3. Enable **OAuth 2.0** (Type: Web App)
4. Copy Client ID and Client Secret to `.env`
5. Add redirect URI: `http://localhost:8000/api/oauth/x/callback`

## 📚 Documentation

Detailed documentation in `docs/`:

- [Architecture](docs/ARCHITECTURE.md) - System design and modules
- [Data Model](docs/DATA_MODEL.md) - Database schema
- [Design Guidelines](docs/DESIGN_GUIDELINES.md) - UX/UI principles
- [Contributing](docs/CONTRIBUTING.md) - Contribution guidelines
- [API Reference](docs/API.md) - REST API endpoints
- [Deployment](docs/DEPLOYMENT.md) - Production setup

## 🧪 Project Structure

```
social-automation-hub/
├── backend/
│   ├── core/
│   │   ├── workspaces/      # Workspace + RBAC
│   │   ├── social/          # OAuth + Analytics
│   │   ├── posts/           # Publishing + Scheduling
│   │   ├── automations/     # Workflow builder
│   │   └── audit/           # Logs + Compliance
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── calendar/
│   │   ├── content-studio/
│   │   ├── inbox/
│   │   ├── analytics/
│   │   ├── automations/
│   │   ├── accounts/
│   │   └── settings/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/             # Utils + i18n
│   │   └── styles/          # Global CSS
│   └── package.json
├── docs/
└── README.md
```

## 📦 Key Dependencies

### Backend
- `django>=5.0` - Web framework
- `djangorestframework>=3.15` - REST API
- `celery>=5.3` - Task queue
- `psycopg2-binary>=2.9` - PostgreSQL adapter
- `cryptography>=41.0` - Token encryption
- `requests>=2.31` - HTTP client for OAuth

### Frontend
- `next@15` - React framework
- `react@18` - UI library
- `tailwindcss@3` - Utility-first CSS
- `zustand@5` - State management
- `@supabase/supabase-js` - Supabase client

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Build/tooling changes

## 🛡️ Security

- OAuth tokens encrypted with Fernet (symmetric encryption)
- CSRF protection enabled
- CORS configured for frontend origin only
- Rate limiting on API endpoints (TODO)
- SQL injection protection via Django ORM

**Found a security issue?** Email security@example.com (do not open public issues).

## 📜 API Endpoints

### OAuth
- `GET /api/oauth/{platform}/authorize` - Start OAuth flow
- `GET /api/oauth/{platform}/callback` - OAuth callback

### Analytics
- `GET /api/oauth/analytics/dashboard/{workspace_id}` - Aggregated metrics
- `GET /api/oauth/analytics/follower-changes/{account_id}` - Follower/unfollower list
- `GET /api/oauth/analytics/top-content/{account_id}` - Top posts
- `GET /api/oauth/analytics/audience-insights/{account_id}` - Demographics

See [API.md](docs/API.md) for complete reference.

## 🚀 Deployment

### Backend (Django + Celery)
- **Recommended**: Railway, Render, DigitalOcean App Platform
- **Requirements**: PostgreSQL, Redis
- **Workers**: 1 web dyno + 1 worker dyno + 1 beat dyno

### Frontend (Next.js)
- **Recommended**: Vercel, Netlify
- **Build**: `pnpm build`
- **Env vars**: `NEXT_PUBLIC_BACKEND_URL`, `NEXT_PUBLIC_SUPABASE_URL`

### Database
- **Recommended**: Supabase (managed Postgres + Realtime)
- **Alternative**: AWS RDS, DigitalOcean Managed Databases

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production setup.

## 📊 Roadmap

- [x] OAuth flows for all platforms
- [x] Advanced analytics dashboard
- [x] Follower/unfollower tracking
- [x] Theme switcher + i18n
- [x] Onboarding guide
- [ ] Content Studio AI integration (OpenAI/Anthropic)
- [ ] Automation builder UI (drag-drop)
- [ ] Inbox unified view (comments/DM)
- [ ] Real-time metrics sync (Celery tasks)
- [ ] Export reports (CSV/PDF)
- [ ] Team collaboration features
- [ ] Mobile app (React Native)

## 👥 Community

- **GitHub**: [Lorenzozero/social-automation-hub](https://github.com/Lorenzozero/social-automation-hub)
- **Issues**: [Report bugs](https://github.com/Lorenzozero/social-automation-hub/issues)
- **Discussions**: [Ask questions](https://github.com/Lorenzozero/social-automation-hub/discussions)

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Meta for Instagram Graph API
- TikTok for Content Posting API
- LinkedIn for Share API
- X (Twitter) for API v2
- Supabase for managed Postgres
- Next.js and Tailwind teams

---

**Built with ❤️ by the community for creators, influencers, and agencies.**

Star ⭐ this repo if you find it useful!

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Content Studio AI integration (OpenAI/Anthropic)
- Automation builder UI (drag-drop)
- Inbox unified view (comments/DM)
- Real-time metrics sync (Celery tasks with platform APIs)
- Export reports (CSV/PDF)
- Team collaboration (workspace invites, approval workflows)
- Rate limiting (django-ratelimit)
- Tests (pytest + Playwright coverage > 80%)
- Docker compose (one-command dev environment)
- Mobile app (React Native)

## [0.1.0] - 2026-02-16

### Added

#### Backend
- Django 5.0 project structure with 5 core apps
- OAuth 2.0 flows for Instagram, TikTok, LinkedIn, X (Twitter)
- Token encryption with Fernet (256-bit symmetric encryption)
- Analytics API endpoints:
  - Dashboard metrics (aggregated KPIs)
  - Follower changes (new followers/unfollowers with enrichment)
  - Top content (posts by engagement rate)
  - Audience insights (demographics, activity patterns)
- Data models:
  - Multi-tenant workspaces with RBAC (Owner/Editor/Analyst)
  - Social accounts with OAuth token storage
  - Time-series metrics snapshots
  - Follower change tracking
  - Top content performance
  - Audience demographics
  - Posts with platform variants
  - Publishing queue
  - Automations with consent management
  - Audit logs (immutable, forensic trail)
- Celery task skeleton with beat schedule:
  - Sync metrics every 15 minutes
  - Detect follower changes every 30 minutes
  - Update top content daily at 2 AM
  - Fetch audience insights weekly on Monday 3 AM
- CORS configuration for frontend origin
- Security features:
  - Token encryption
  - CSRF protection
  - Session authentication
  - Workspace isolation (multi-tenancy)

#### Frontend
- Next.js 15 (App Router) project structure
- Pages:
  - Dashboard (KPI overview, follower changes, connected accounts)
  - Analytics followers drill-down (new/unfollowers list)
  - Accounts OAuth connection (4 platform cards with "Connect" buttons)
  - Onboarding guide (interactive setup wizard)
- Components:
  - Sidebar navigation with collapsible menu
  - Theme switcher (dark/light/system with persistence)
  - Language switcher (EN/IT with i18n hook)
  - StatCard (reusable KPI card)
  - EmptyState (placeholder for no data)
  - Badge (status indicators)
- Styling:
  - Tailwind CSS with CSS variables
  - Dark mode support
  - Responsive design (mobile/tablet/desktop)
  - Animations (fade-in, stagger, hover effects)
- State management:
  - Zustand for theme and language preferences
  - localStorage persistence
- i18n:
  - English and Italian translations
  - Custom hook with JSON locale files

#### Documentation
- README.md: Project overview, quick start, OAuth setup, community links
- LICENSE: MIT License
- docs/API.md: Complete API reference with request/response examples
- docs/DEPLOYMENT.md: Production setup guide (Railway, Vercel, Supabase)
- docs/CONTRIBUTING.md: Contributor guide with coding standards
- docs/ARCHITECTURE.md: System design deep-dive
- docs/DATA_MODEL.md: Database schema with ERD
- docs/DESIGN_GUIDELINES.md: UX/UI design system

### Security
- OAuth tokens encrypted with Fernet before storage
- CORS limited to frontend origin
- CSRF protection enabled
- Input validation via Django ORM
- Audit logs for all sensitive actions

---

## Version Schema

**Format**: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes (API incompatibility, data model migrations requiring manual intervention)
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes, documentation updates

**Example**:
- `1.0.0` - First production release
- `1.1.0` - Added Content Studio AI (new feature)
- `1.1.1` - Fixed OAuth token refresh bug (patch)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute changes and create pull requests.

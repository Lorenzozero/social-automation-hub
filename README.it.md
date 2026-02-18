# 🎭 Social Automation Hub

## Perché Pagare un Social Media Manager Quando Hai Django?

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![Automazione](https://img.shields.io/badge/Automazione-Legale_🤝-success)](/)
[![Niente_Bullshit](https://img.shields.io/badge/Bullshit-0%25-red)](/)

> *"Gestisci Instagram, TikTok, LinkedIn e X con l'efficienza di un robot e la compliance di un avvocato. Tutto open-source, perché pagare €497/mese per Hootsuite è da boomer."*

**Piattaforma open-source** per dominare i social media senza vendere l'anima (o il budget) a Zuckerberg e Musk. Monitoraggio real-time, pubblicazione multi-piattaforma, analytics che fanno sembrare Google Analytics una calcolatrice, e automazioni così etiche che potrebbero fare il TED Talk.

---

## 🎯 A Chi Serve 'Sto Coso?

### ✅ TI SERVE SE:
- Sei un **creator** che vuole automatizzare senza finire bannato
- Gestisci **clienti social** e vuoi analytics pro senza Excel dello scorso decennio
- Hai un'**agenzia** e cerchi un tool che non ti costi più dello stipendio del tirocinante
- Vuoi **compliance OAuth 2.0** perché ti piacciono i tuoi account attivi

### ❌ NON TI SERVE SE:
- Pensi che "automazione" significhi bot spam alla "Segui per Segui 2010"
- Credi che Django sia un film di Tarantino
- Ti aspetti risultati senza leggere la documentazione (sorpresa: non è magia nera)
- Preferisci pagare €997/anno per SaaS con le stesse feature ma con dashboard più carina

---

## 🔥 Features (Quelle Vere, Non Quelle dei Landing Page Fake)

### 🌐 Multi-Platform Integration
| Piattaforma | Cosa Fa | Limiti Tecnici | Status |
|------------|---------|----------------|--------|
| **Instagram** | Graph API professionale | 100 post/24h (blame Meta) | ✅ OAuth |
| **TikTok** | Content Posting API | Serve consent UX (è il 2026, la privacy esiste) | ✅ OAuth |
| **LinkedIn** | UGC Posts | Solo account Member/Org | ✅ OAuth |
| **X (Twitter)** | OAuth 2.0 + PKCE | Transparenza automazioni (o ban) | ✅ OAuth |

> **Pro Tip**: No, non puoi fare follow/unfollow automation su Instagram. Non perché non so farlo, ma perché vuoi tenere l'account.

### 📊 Analytics Che Non Servono Solo Per Screenshot LinkedIn

- **Dashboard Real-Time**: KPI (reach, impressions, engagement) aggiornati ogni 5 minuti, non "una volta al giorno come gli altri tool"
- **Follower/Unfollower Tracking**: Chi ti segue, chi ti ghostare, con arricchimento dati che farebbe invidia a Sherlock
- **Top Content Analysis**: I post che funzionano vs. quelli che sembravano fighi ma hanno fatto flop
- **Audience Insights**: Demografia, pattern di attività, timezone dei tuoi follower (così smetti di postare alle 3 AM)
- **Time-Series Metrics**: Trend analysis con grafici che non sembrano fatti su Paint
- **Cross-Platform Correlation**: Capire se il post virale su TikTok ha portato follower su IG (spoiler: probabilmente no)

### 📅 Content Management (Aka "Il Calendario Che Userai Davvero")

- **Editorial Calendar**: Scheduling senza dover aprire 4 app diverse
- **AI Content Creation**: Multi-variant generation (sì, con LLM veri, non template "Buongiorno! ☀️")
- **Manual Approval Workflow**: Draft-first, perché pubblicare robe a caso è da Junior
- **Platform-Specific Adaptations**: Stesso contenuto, 4 formati diversi, automaticamente

### ⚙️ Safe Automations (Non i Bot Spam del 2015)

- **Trigger-Based Workflows**: Evento → Azione (new post, menzioni, soglie KPI)
- **Explicit Consent Management**: Compliance X/Twitter (non finire come i bot bannati a marzo 2025)
- **Full Audit Logs**: Trasparenza totale, perché "trust me bro" non è security policy
- **Policy Engine**: Rate limits e regole platform, così non diventi spam

> **Disclaimer**: Questo tool NON fa:
> - Follow/unfollow automation (è il 2026, cresci organicamente o paga gli ads)
> - Commenti automatici "Amazing! 🔥" (ban in 72h garantito)
> - Scraping violento di profili (ci sono le API, usale)

### 🎨 Professional UX (Non Il Solito Template Bootstrap)

- **Design Minimale**: Perché l'influencer vuole UI bella, non Excel 2003
- **i18n Support**: Inglese + Italiano (altri linguaggi? Fork e PR, grazie)
- **Dark/Light/System Theme**: Respect per chi lavora di notte come un vero dev
- **Responsive Mobile/Desktop**: Funziona anche su tablet, quel device che nessuno usa
- **Smooth Animations**: Micro-interazioni che fanno sembrare l'app più costosa di quello che è

---

## 💻 Stack (AKA: Le Tecnologie Vere, Non il Corso Udemy da €19.99)

### Backend (Dove Succede la Magia)
```
Django 5.0          → Framework, perché Flask è per prototipi
DRF                 → REST API che rispetta gli standard HTTP
PostgreSQL          → Database (Supabase managed, perché gestire Postgres è un hobby costoso)
Celery + Redis      → Task queue per non bloccare il server con API lente
OAuth 2.0           → Auth su tutte le platform (no password salvate in plain text, siamo nel 2026)
Fernet Encryption   → Token criptati, perché security > comodità
```

### Frontend (Quello Che Vedi)
```
Next.js 15          → App Router, perché Pages Router è legacy
Tailwind CSS        → Utility-first CSS (no CSS custom scritto male)
Zustand             → State management senza Redux boilerplate
Custom i18n Hook    → Traduzioni JSON, niente librerie da 500kb
```

---

## 🚀 Quick Start (No, Non Ti Serve un Corso da €997)

### Prerequisiti (Se Non Li Hai, Installa Ora)

```bash
✅ Python 3.11+      (no, 3.9 non va bene)
✅ Node.js 18+       (LTS, non experimental)
✅ PostgreSQL 14+    (o Supabase free tier)
✅ Redis 7+          (per Celery, non è opzionale)
```

### Backend Setup (5 Minuti, Promesso)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Genera encryption key (copia questo output)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Configura .env (NON committare questo file, genio)
cp .env.example .env
# Apri .env e inserisci:
# - SECRET_KEY (generata sopra)
# - DATABASE_URL (Supabase connection string)
# - REDIS_URL
# - OAuth credentials (vedi sotto)

# Migrazioni DB
python manage.py migrate
python manage.py createsuperuser  # Username: admin, Password: non "admin123"

# Avvia server
python manage.py runserver  # http://localhost:8000

# In un altro terminale: Celery worker
celery -A core worker -l info

# In un terzo terminale: Celery beat (scheduling)
celery -A core beat -l info
```

### Frontend Setup (3 Minuti, Davvero)

```bash
cd frontend
pnpm install  # o npm install, ma pnpm è più veloce

# Configura .env.local
cp .env.example .env.local
# Imposta: NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

pnpm dev  # http://localhost:3000
```

**Apri browser → `localhost:3000` → Segui l'onboarding → Profit.**

---

## 🔑 OAuth Setup (Perché Serve Per Non Violare ToS)

### Instagram (Meta Developers Console)

1. Vai su [developers.facebook.com](https://developers.facebook.com)
2. Crea App → Tipo **Business**
3. Aggiungi prodotti: **Instagram Basic Display** + **Instagram Graph API**
4. Copia **App ID** e **App Secret** in `.env`:
   ```
   INSTAGRAM_CLIENT_ID=your_app_id
   INSTAGRAM_CLIENT_SECRET=your_secret
   ```
5. Redirect URI: `http://localhost:8000/api/oauth/instagram/callback`

### TikTok (TikTok Developers)

1. Vai su [developers.tiktok.com](https://developers.tiktok.com)
2. Crea app → Aggiungi **Content Posting API**
3. Copia **Client Key** e **Client Secret** in `.env`
4. Redirect URI: `http://localhost:8000/api/oauth/tiktok/callback`

### LinkedIn (LinkedIn Developer Portal)

1. Vai su [linkedin.com/developers](https://www.linkedin.com/developers)
2. Crea app → Request **Sign In** + **Share on LinkedIn**
3. Copia **Client ID** e **Client Secret** in `.env`
4. Redirect URI: `http://localhost:8000/api/oauth/linkedin/callback`

### X / Twitter (Developer Portal)

1. Vai su [developer.twitter.com](https://developer.twitter.com)
2. Crea Project → Crea App
3. Abilita **OAuth 2.0** (Type: Web App, PKCE enabled)
4. Copia **Client ID** e **Client Secret** in `.env`
5. Redirect URI: `http://localhost:8000/api/oauth/x/callback`

> **Note**: In production usa HTTPS, non HTTP. Let's Encrypt è gratis, non hai scuse.

---

## 📁 Struttura Progetto (Per Orientarsi)

```
social-automation-hub/
├── backend/
│   ├── core/
│   │   ├── workspaces/      # Multi-tenancy + RBAC (Owner/Admin/Member)
│   │   ├── social/          # OAuth flows + Analytics engine
│   │   ├── posts/           # Publishing + Scheduling system
│   │   ├── automations/     # Workflow builder (trigger → action)
│   │   └── audit/           # Compliance logs (chi ha fatto cosa, quando)
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── app/
│   │   ├── dashboard/       # Overview metrics
│   │   ├── calendar/        # Editorial calendar
│   │   ├── content-studio/  # AI content generation
│   │   ├── inbox/           # Unified comments/DM (TODO)
│   │   ├── analytics/       # Deep-dive analytics
│   │   ├── automations/     # Workflow builder UI
│   │   ├── accounts/        # Social accounts management
│   │   └── settings/        # Theme, i18n, team settings
│   ├── src/
│   │   ├── components/      # Reusable UI (Button, Card, Modal, etc.)
│   │   ├── lib/             # Utils + i18n hooks
│   │   └── styles/          # Global CSS + Tailwind config
│   └── package.json
├── docs/                    # Documentazione tecnica (EN)
└── README.it.md             # Questo file
```

---

## 📚 Documentazione (Per Chi Vuole Approfondire)

| File | Cosa C'è Dentro |
|------|-----------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, moduli, data flow |
| [DATA_MODEL.md](docs/DATA_MODEL.md) | Schema DB (ER diagram + field descriptions) |
| [DESIGN_GUIDELINES.md](docs/DESIGN_GUIDELINES.md) | UX/UI principles, component library |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | Come contribuire senza fare danni |
| [API.md](docs/API.md) | Endpoint REST completi con esempi |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production setup (Railway, Vercel, Supabase) |
| [SECURITY_PERFORMANCE.md](docs/SECURITY_PERFORMANCE.md) | Security best practices + optimization |

---

## 🤝 Contributing (Sì, Pull Request Accettate)

### Workflow

1. **Fork** il repo
2. Crea branch: `git checkout -b feature/nome-feature`
3. Commit: `git commit -m 'feat: add feature X'` (usa [Conventional Commits](https://www.conventionalcommits.org/))
4. Push: `git push origin feature/nome-feature`
5. Apri **Pull Request** (descrizione chiara, no "fix stuff")

### Commit Convention

```
feat:      → Nuova feature
fix:       → Bug fix
docs:      → Documentazione
style:     → Formatting (no logic change)
refactor:  → Refactoring codice
test:      → Aggiunta test
chore:     → Build/tooling
```

### Code Style

- **Python**: Black formatter, isort imports, flake8 linting
- **TypeScript**: ESLint + Prettier, no `any` types
- **Naming**: snake_case (Python), camelCase (TS), SCREAMING_SNAKE_CASE (constants)

---

## 🛡️ Security (Perché "Trust Me Bro" Non È Una Policy)

- ✅ OAuth tokens **encrypted** con Fernet (symmetric encryption)
- ✅ CSRF protection abilitata
- ✅ CORS configurato (solo frontend origin, no `*`)
- ✅ SQL injection protection via Django ORM (no raw queries a caso)
- ✅ Rate limiting su API endpoints (TODO: implementare con `django-ratelimit`)
- ✅ Environment variables per secrets (no hardcoded credentials)

**Trovato un bug di sicurezza?** 
→ Email: `security@example.com` (NO issue pubbliche, grazie)

---

## 📊 Roadmap (Le Cose Che Farai Invece Di Scrollare TikTok)

### ✅ Fatto (Funziona Ora)
- OAuth flows tutte le platform
- Analytics dashboard avanzato
- Follower/unfollower tracking
- Theme switcher + i18n
- Onboarding guide

### 🚧 In Development (Prossimi 3 Mesi)
- **Content Studio AI**: Integration OpenAI/Anthropic per content generation
- **Automation Builder UI**: Drag-drop workflow (tipo Zapier ma tuo)
- **Inbox Unified View**: Tutti i commenti/DM in un posto solo
- **Real-Time Metrics Sync**: Celery tasks per update automatici ogni 5min

### 🔮 Future (Quando Avremo Tempo)
- Export reports (CSV/PDF) per clienti
- Team collaboration (commenti, approval multi-step)
- Mobile app (React Native, forse)
- Integrazione YouTube/Pinterest (se qualcuno ne ha bisogno)

---

## 🚀 Deployment (Production Setup)

### Backend (Django + Celery)

**Opzioni raccomandate**:
- [Railway](https://railway.app) → Deploy con 1 click, $5/mese per starter
- [Render](https://render.com) → Free tier disponibile (con sleep dopo inattività)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform) → $5/mese, no sleep

**Requisiti**:
- 1 web dyno (gunicorn)
- 1 worker dyno (celery worker)
- 1 beat dyno (celery beat scheduler)
- PostgreSQL database
- Redis instance

### Frontend (Next.js)

**Opzioni raccomandate**:
- [Vercel](https://vercel.com) → Zero-config, gratis per hobby
- [Netlify](https://www.netlify.com) → Alternativa a Vercel

**Build command**: `pnpm build`
**Env vars**: `NEXT_PUBLIC_BACKEND_URL`, `NEXT_PUBLIC_SUPABASE_URL`

### Database

- [Supabase](https://supabase.com) → Postgres managed + Realtime, free tier 500MB
- [AWS RDS](https://aws.amazon.com/rds/) → Per chi vuole scalare (e pagare)
- [DigitalOcean Managed Databases](https://www.digitalocean.com/products/managed-databases) → $15/mese

Vedi [DEPLOYMENT.md](docs/DEPLOYMENT.md) per setup dettagliato.

---

## 💰 Costi Reali (Perché Trasparenza)

### Self-Hosted (Minimo)
```
Railway Web Dyno:       $5/mese
Railway Worker Dyno:    $5/mese
Supabase Free Tier:     $0/mese (fino 500MB DB + 2GB bandwidth)
Redis Free Tier:        $0/mese (Upstash free tier)
Vercel Frontend:        $0/mese (hobby plan)
─────────────────────────────────
TOTALE:                 ~$10/mese
```

### Alternative SaaS (Per Confronto)
```
Hootsuite Professional: $99/mese
Buffer Business:        $99/mese
Later Growth:           $80/mese
Sprout Social:          $249/mese (lol)
```

**Risparmio annuale self-hosted vs. Hootsuite**: `$1,068/anno`

---

## 🎯 Use Cases Reali

### 1. **Freelance Social Media Manager**
*"Gestisco 5 clienti, ognuno con IG + LinkedIn. Prima usavo 3 tool diversi, ora tutto qui. Analytics automatici, scheduling centralizzato, report export per clienti. ROI: 10 ore/settimana risparmiate."*

### 2. **Agenzia Digitale (10-50 Clienti)**
*"Multi-workspace per separare clienti, RBAC per team member, audit logs per compliance. Non paghiamo più licenze per utente. Setup una volta, scala infinito."*

### 3. **Creator/Influencer**
*"Automazioni etiche per rispondere a menzioni, analytics per capire cosa funziona, AI content per varianti post. Zero ban, 100% compliance."*

### 4. **Startup Tech-Savvy**
*"Fork del repo, customizzazione per industry specifica (B2B SaaS), self-hosted su infra AWS esistente. Total control."*

---

## ❓ FAQ (Domande Che Farai Comunque)

### "Posso usarlo per clienti?"
Sì, è MIT license. Puoi fare white-label, rivendere, modificare. Attribution gradita ma non obbligatoria.

### "Funziona con account personali o serve Business?"
Dipende dalla piattaforma:
- **Instagram**: Serve **Professional Account** (Business o Creator), gratis
- **TikTok**: Account normale OK
- **LinkedIn**: Account Member normale OK
- **X**: Account normale OK

### "Rischio ban usando automazioni?"
No, se usi questo tool correttamente:
- OAuth ufficiale (no scraping)
- Rate limits rispettati
- No follow/unfollow spam
- No commenti automatici generici
- Audit logs per trasparenza (X requirement)

**Rischi ban se**: modifichi il tool per fare spam. Don't.

### "Serve conoscenza tecnica per deployare?"
**Minima**: Saper fare SSH, configurare env variables, leggere docs.
**Media**: Se vuoi customizzare codice (Django/Next.js knowledge).

Railway/Render hanno deploy 1-click, Vercel auto-deploya da GitHub.

### "Posso integrare altre piattaforme?"
Sì, crea un nuovo OAuth provider in `backend/core/social/providers/`. Contribuisci con PR!

### "Supporto enterprise/white-label?"
Tool è gratis, supporto enterprise no. Se serve consulting: apri issue o email.

---

## 🌟 Star Questo Repo Se:

- ✅ Ti ha fatto ridere almeno una volta
- ✅ Pensi che i SaaS per social costino troppo
- ✅ Vuoi supportare open-source fatto bene
- ✅ Hai intenzione di usarlo davvero (o almeno provarci)

**Goal**: 1,000 stelle entro Q2 2026. Aiutaci a arrivarci condividendo su X/LinkedIn (ironicamente, con questo tool).

---

## 📞 Community & Support

- **GitHub**: [Lorenzozero/social-automation-hub](https://github.com/Lorenzozero/social-automation-hub)
- **Issues**: [Report bugs](https://github.com/Lorenzozero/social-automation-hub/issues) (con log dettagliati, non "non funziona")
- **Discussions**: [Ask questions](https://github.com/Lorenzozero/social-automation-hub/discussions) (no spam)
- **X/Twitter**: Tag `@socialautohub` (se esiste)

---

## 🙏 Ringraziamenti

- **Meta** → Per Instagram Graph API (anche se i rate limits fanno schifo)
- **TikTok** → Per Content Posting API (almeno funziona)
- **LinkedIn** → Per Share API (l'unica piattaforma che non ha cambiato ToS 47 volte)
- **X/Twitter** → Per API v2 (RIP API v1.1 free tier, 2006-2023)
- **Supabase** → Per Postgres managed gratuito (true MVP)
- **Next.js Team** → Per App Router (dopo l'initial learning curve, è ottimo)
- **Tailwind Team** → Per utility-first CSS (no more CSS custom disastri)

---

## 📜 License

MIT License - Fai quello che vuoi, basta non fare causa.

Vedi [LICENSE](LICENSE) per legalese completo.

---

**Built with 💻 by Lorenzo & the community.**

**Per creator, influencer e agency che vogliono automatizzare senza vendere l'anima.**

*PS: Se questo README ti ha convinto, immagina quanto è figo il codice. Spoiler: molto.*

---

### 🔥 One More Thing

Se pensi che questo progetto sia "troppo complesso" per te:
1. Non lo è. È ben documentato.
2. Se lo è, impara. È gratis.
3. Se non vuoi imparare, usa un SaaS. Nessun problema.

**Ma se sei arrivato fin qui leggendo, probabilmente sei il tipo di persona che vuole controllo totale sul proprio stack. Welcome home. 🏠**

---

**⭐ Star now or regret later ⭐**

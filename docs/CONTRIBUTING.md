# Contributing to Social Automation Hub

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and constructive. We're building a community-driven project for everyone.

## How to Contribute

### Reporting Bugs

1. Check [existing issues](https://github.com/Lorenzozero/social-automation-hub/issues) first
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python/Node version)
   - Screenshots if applicable

### Suggesting Features

1. Check [discussions](https://github.com/Lorenzozero/social-automation-hub/discussions) for similar ideas
2. Create a new discussion with:
   - Use case / problem you're solving
   - Proposed solution
   - Alternatives considered
   - Mockups/wireframes if applicable

### Pull Requests

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/social-automation-hub.git`
3. **Create branch**: `git checkout -b feature/your-feature-name`
4. **Make changes** following our coding standards (see below)
5. **Test** your changes locally
6. **Commit** with conventional commits: `git commit -m 'feat: add amazing feature'`
7. **Push**: `git push origin feature/your-feature-name`
8. **Open PR** against `main` branch

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
pnpm install
cp .env.example .env.local
# Edit .env.local
pnpm dev
```

## Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8
- **Formatter**: Black (`black .`)
- **Linter**: Flake8 (`flake8 .`)
- **Type hints**: Use where beneficial
- **Docstrings**: Use for public functions/classes
- **Imports**: Group stdlib, third-party, local

### TypeScript (Frontend)

- **Style**: Follow Airbnb style guide
- **Formatter**: Prettier (`pnpm format`)
- **Linter**: ESLint (`pnpm lint`)
- **Types**: Prefer explicit types over `any`
- **Components**: Functional components with hooks
- **File naming**: kebab-case for files, PascalCase for components

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: fix bug
docs: update documentation
style: format code (no logic change)
refactor: refactor code structure
test: add or update tests
chore: update build tools, dependencies
perf: performance improvements
ci: CI/CD changes
```

**Examples**:
```
feat(analytics): add follower growth chart
fix(oauth): handle expired token refresh
docs(readme): update deployment instructions
refactor(dashboard): extract KPI card component
```

## Project Structure

### Backend Modules

- `core/workspaces/` - Workspace + RBAC logic
- `core/social/` - OAuth + Analytics
- `core/posts/` - Publishing + Scheduling
- `core/automations/` - Workflow builder
- `core/audit/` - Logs + Compliance

### Frontend Structure

- `app/` - Next.js pages (App Router)
- `src/components/common/` - Reusable UI components
- `src/components/layout/` - Layout components (Sidebar, Header)
- `src/lib/` - Utilities, hooks, i18n
- `src/styles/` - Global CSS, Tailwind config

## Testing

### Backend Tests

```bash
pytest
pytest --cov=core  # with coverage
```

### Frontend Tests

```bash
pnpm test
pnpm test:coverage
```

### Writing Tests

- **Unit tests**: Test individual functions/components
- **Integration tests**: Test API endpoints, database interactions
- **E2E tests**: Test full user flows (Playwright/Cypress)

## Database Migrations

When changing models:

```bash
python manage.py makemigrations
python manage.py migrate
```

Commit both the model changes and migration files.

## Adding Dependencies

### Backend

```bash
pip install package-name
pip freeze > requirements.txt
```

### Frontend

```bash
pnpm add package-name
# or for dev dependencies
pnpm add -D package-name
```

Document why the dependency is needed in your PR.

## Documentation

Update documentation when:

- Adding new features
- Changing API endpoints
- Modifying configuration
- Adding environment variables

Documentation files:

- `README.md` - Overview, quick start
- `docs/API.md` - API reference
- `docs/DEPLOYMENT.md` - Production setup
- `docs/ARCHITECTURE.md` - System design
- Inline code comments for complex logic

## Platform API Integration Guidelines

When implementing platform API calls:

1. **Error handling**: Wrap in try/except, log errors
2. **Rate limiting**: Respect platform limits (check response headers)
3. **Token refresh**: Handle expired tokens automatically
4. **Pagination**: Fetch all pages when needed
5. **Data validation**: Validate API responses before saving to DB
6. **Testing**: Mock API responses for tests (don't call real APIs)

### Example API Implementation

```python
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def fetch_instagram_metrics(user_id: str, token: str) -> dict:
    """
    Fetch Instagram account metrics via Graph API.
    
    Args:
        user_id: Instagram user ID
        token: OAuth access token
        
    Returns:
        dict with followers, reach, impressions, engagement
        
    Raises:
        requests.RequestException: On API errors
    """
    url = f"https://graph.instagram.com/{user_id}/insights"
    params = {
        "metric": "follower_count,reach,impressions",
        "period": "day",
        "access_token": token,
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse and return normalized data
        return {
            "followers": data.get("follower_count", 0),
            "reach": data.get("reach", 0),
            "impressions": data.get("impressions", 0),
            "engagement": data.get("engagement", 0),
        }
    except requests.RequestException as e:
        logger.error(f"Instagram API error for user {user_id}: {e}")
        raise
```

## Security

### Never Commit

- OAuth credentials (use `.env`)
- Database passwords
- API keys
- Encryption keys
- User data

### Always

- Encrypt sensitive data in DB
- Validate user inputs
- Use parameterized queries (Django ORM)
- Sanitize outputs
- Log security events

## Review Process

1. **Automated checks**: CI must pass (tests, linting)
2. **Code review**: At least one maintainer approval
3. **Testing**: Verify changes work locally
4. **Documentation**: Check if docs need updates
5. **Merge**: Maintainers will merge once approved

## Getting Help

- **Questions**: [GitHub Discussions](https://github.com/Lorenzozero/social-automation-hub/discussions)
- **Bugs**: [GitHub Issues](https://github.com/Lorenzozero/social-automation-hub/issues)
- **Real-time chat**: Join our Discord (link in README)

## Recognition

Contributors will be:

- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Given credit in documentation

Significant contributors may be invited as maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Social Automation Hub! 🚀

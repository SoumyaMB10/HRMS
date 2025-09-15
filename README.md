HRMS FastAPI (modular scaffold)

Quickstart:
1. Copy .env.example -> .env (no changes required for local Docker compose)
2. Start Postgres:
   docker compose up -d
3. Create virtual env & install:
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
4. Run app:
   uvicorn src.main:app --reload
5. Open docs:
   http://localhost:8000/docs

Auth:
- Current simple auth: use header X-User-Id (numeric) to identify current user for endpoints.
- /api/auth/login returns {"role": "<role>"} for an identifier (email or id).

Next steps:
- Replace header auth + login with JWT/OAuth2
- Add Alembic migrations
- Add notifications (Celery/Redis)

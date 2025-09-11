# HRMS FastAPI Backend (Postgres)

This repository contains a complete FastAPI backend for an HRMS product (attendance, leaves, policies, recruitment) using PostgreSQL.

## What you get
- Clear folder/file layout ready to copy into a repository
- Sync SQLAlchemy models and Pydantic schemas
- CRUD + approval logic that enforces manager → HR → CFO approval chains
- Simple, explicit endpoints your frontend can call (designed to be wired to Vercel / Lovable frontend)
- `docker-compose.yml` for quick local Postgres

## Prerequisites
- Python 3.10+
- Docker (for local Postgres) or a running Postgres instance
- `pip` to install Python packages

## Quickstart (copy files and run)
1. Create project folder and paste files from this scaffold.
2. Create `.env` from `.env.example` and set your DB URL (or use docker-compose).
3. Start Postgres locally:
   ```bash
   docker-compose up -d
   ```
4. Create a Python venv and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. Start the server (it will create tables automatically on startup):
   ```bash
   uvicorn app.main:app --reload
   ```
6. Open docs: http://localhost:8000/docs

## Files & Layout
The canvas contains the complete project under the `app/` folder. Read the `app/README` in the canvas for per-file details.

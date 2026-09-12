# Development

Local setup for the Sotto Salon foundation (SAL-007). Everything here is **synthetic
only**: no real identity documents, payment credentials, or customer data. Production
refuses the synthetic verification/payment adapters (see `backend/salon/core/config.py`).

## Prerequisites

- Python 3.12+ (developed against 3.14)
- Node.js 20+ (developed against 25) and npm
- Docker (optional, for the backing-services stack)

## Backing services (optional but recommended)

```sh
docker compose up -d          # postgres, minio, redis — all bound to 127.0.0.1
docker compose -p sotto-salon down -v   # stop and wipe
```

The database is published at `postgresql+psycopg://salon:salon@127.0.0.1:5432/salon`.

## Backend (API + worker)

```sh
cd backend
python -m venv .venv
# Windows:            .venv\Scripts\python -m pip install -e ".[dev]"
# macOS/Linux:        .venv/bin/python  -m pip install -e ".[dev]"
cp .env.example .env          # then adjust values

# Apply migrations to an empty database
.venv/Scripts/python -m alembic upgrade head          # (Scripts\ on Windows)

# Run the API
.venv/Scripts/python -m uvicorn salon.api.main:app --reload --port 8000

# Run the worker (separate process)
.venv/Scripts/python -m salon.workers.main
```

Exact dependency versions are pinned in `backend/requirements.lock`
(`pip install -r requirements.lock` for a reproducible environment).

### Checks

```sh
cd backend
.venv/Scripts/python -m pytest         # unit/integration tests
.venv/Scripts/python -m ruff check .   # lint
```

Migrations can be exercised against a throwaway SQLite database without Postgres:

```sh
.venv/Scripts/python -m alembic -x db_url=sqlite:///tmp.db upgrade head
.venv/Scripts/python -m alembic -x db_url=sqlite:///tmp.db downgrade base
```

## API contract types

The web app consumes generated types from the backend OpenAPI schema.

```sh
cd backend && .venv/Scripts/python scripts/export_openapi.py ../contracts/openapi/openapi.json
cd ../contracts && npm install && npm run generate && npm run check
```

The export is deterministic; regenerating an unchanged API is byte-identical (CI can
diff to detect drift — wired in SAL-008).

## Web

```sh
cd apps/web
npm install
# API location (defaults to http://127.0.0.1:8000)
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
npm run dev          # http://localhost:3000
npm run build        # production build + type-check
```

The home page calls `GET /api/v1/meta` and shows the running environment and configured
adapters, confirming the web-to-API path end to end.

## Configuration

All backend settings use the `SALON_` prefix (see `backend/.env.example`). Missing or
invalid settings fail fast with **redacted** diagnostics that name the offending
variables but never print their values.

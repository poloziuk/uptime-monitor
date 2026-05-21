# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A lightweight uptime/health-check monitoring system. It periodically queries a list of URLs, stores results in PostgreSQL, exposes a web dashboard at `/` and a JSON API at `/status`, and sends Slack alerts on failures.

## Commands

### Run (Docker — primary method)
```bash
docker compose up --build
```
- Web UI: http://localhost:8000
- JSON status: http://localhost:8000/status
- Adminer (DB browser): http://localhost:8080

### Run locally (requires a running PostgreSQL instance)
```bash
pip install -r requirements.txt
# Set env vars (see Configuration below)
uvicorn src.api:app --host 0.0.0.0 --port 8000   # web server
python src/worker.py                               # background checker
```

### Lint
```bash
black --check .
flake8 .
mypy .
```

### Tests
```bash
pytest                        # all tests
pytest tests/test_import_app.py::test_smoke  # single test
```

## Architecture

Two separate processes share one PostgreSQL database:

```
Worker (src/worker.py)
  └─ every CHECK_INTERVAL seconds:
       asyncio.gather() → src/checker.py (httpx async)
         └─ writes results to `checks` table via src/db.py

API Server (src/api.py — FastAPI + Uvicorn)
  └─ GET /        → renders templates/index.html (recent check rows)
  └─ GET /status  → returns latest status per URL as JSON
```

Key modules:
- **`src/config.py`** — all env vars and their defaults; single source of truth for configuration
- **`src/models.py`** — `Check` SQLAlchemy model (`id`, `url`, `status`, `response_time`, `timestamp`)
- **`src/db.py`** — `SessionLocal`, `init_db()`, `save_check()`, `get_recent_checks()`
- **`src/checker.py`** — `check_url()`: returns `True` only for HTTP 200; all errors → `False`
- **`src/alerts.py`** — posts to `SLACK_WEBHOOK` on DOWN status; no-ops when webhook is unset

## Configuration

Set via environment variables (or a `.env` file picked up by `python-dotenv`):

| Variable | Default | Purpose |
|---|---|---|
| `URLS` | `https://google.com,https://github.com` | Comma-separated URLs to monitor |
| `CHECK_INTERVAL` | `60` | Seconds between check rounds |
| `SLACK_WEBHOOK` | `""` | Slack incoming webhook URL (optional) |
| `DB_URL` | `sqlite:///monitor.db` | SQLAlchemy DB URL (PostgreSQL in Docker) |

## CI/CD (`.github/workflows/ci-cd.yml`)

Pipeline stages in order: **lint → semgrep → unit-tests → docker-build → image-tests → orca → push-to-ghcr → deploy-dev → smoke-tests → deploy-prod**.

The `lint` job runs Black, Flake8, and MyPy. The `image-tests` job spins up `docker compose`, waits for the `/status` endpoint to respond, then tears down.

## Notes

- `PYTHONPATH=/app` is required for `src.*` imports — set automatically in the Dockerfile and in `pyproject.toml`'s `[tool.pytest.ini_options]`.
- `flask` is listed in `requirements.txt` but is not used — ignore it.
- Linting ignores: `E203`, `W503` (flake8); missing stubs (mypy).

# Demo Script

## Setup

```bash
uv sync --extra dev
copy .env.example .env
docker compose up -d
uv run alembic upgrade head
```

## Run

```bash
uv run python scripts/ingest_cli.py datasets/seed_corpus
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8081
```

## Show

1. Open `http://localhost:8081/docs`.
2. Call `/health/live` and `/health/ready`.
3. Run `/v1/search` dense-only.
4. Run `/v1/search` hybrid.
5. Run `/v1/answer`.
6. Show answer citations.
7. Show retrieval benchmark report.

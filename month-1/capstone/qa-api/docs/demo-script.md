# Demo Script

## Local Setup

```bash
uv sync --extra dev
copy .env.example .env
docker compose up -d
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

## Demo Flow

1. Open `http://localhost:8080/docs`.
2. Call `GET /health/live`.
3. Call `GET /health/ready`.
4. Register a user.
5. Login and authorize Swagger with the bearer token.
6. Ask a question through `POST /qa/ask`.
7. Ask the same question again and show exact cache hit.
8. Ask a similar question and show semantic cache behavior.
9. Open `/qa/history`.
10. Show structured logs with request ID, cache outcome, provider, model, latency, and cost.

## Checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

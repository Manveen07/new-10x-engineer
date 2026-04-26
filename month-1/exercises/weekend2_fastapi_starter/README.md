# Weekend 2: Production FastAPI Starter

## Goal

Fold Week 2 exercises into `month-1/capstone/qa-api/`.

## Build

Implement the capstone skeleton:

- App factory and lifespan.
- Typed settings.
- Health router.
- Auth router.
- Users router.
- Admin placeholder route.
- Pydantic schemas.
- Consistent error envelope.
- Request ID and timing middleware.
- Async database session dependency.
- Alembic migration for users and refresh tokens.
- Tests for health and auth.
- ADR for FastAPI project structure.

## Required Commands

```bash
uv run ruff check .
uv run mypy app
uv run pytest
```

## Done When

- `/docs` renders.
- `/health/live` returns OK.
- `/health/ready` checks dependencies.
- Register -> login -> `/users/me` works.
- Admin route rejects normal users.
- Tests pass with dependency overrides.
- The app still works with `DEFAULT_PROVIDER=mock`.

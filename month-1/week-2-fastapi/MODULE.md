# Week 2: FastAPI Production Patterns

## Outcome

By the end of Week 2 the capstone should no longer be a collection of isolated exercises. It should be a real FastAPI app skeleton with typed settings, dependency injection, auth, RBAC, middleware, async database sessions, health checks, and tests.

## What This Week Teaches

- FastAPI application structure.
- Pydantic v2 request and response schemas.
- Pydantic Settings for typed environment config.
- Dependency injection for settings, database sessions, current user, and roles.
- JWT access and refresh token flow.
- RBAC and protected endpoints.
- Middleware for request IDs, timing, CORS, and logging.
- Consistent error envelopes.
- Async SQLAlchemy session-per-request pattern.
- Test dependency overrides.

## Day 6: FastAPI Structure And Dependency Injection

Exercise: `../exercises/day6_fastapi_structure.py`

Build in the capstone:

- `app/main.py` with `create_app()`.
- Lifespan function for startup and shutdown resources.
- `app/config.py` using `pydantic-settings`.
- `app/dependencies.py` for shared dependencies.
- `app/routers/`, `app/schemas/`, `app/services/`, `app/repositories/`.
- `/health/live` and `/health/ready`.

Done when:

- App imports without side effects.
- `/docs` renders.
- Settings load from `.env` and are type-checked at startup.

## Day 7: Pydantic V2 Validation And Error Handling

Exercise: `../exercises/day7_pydantic_validation.py`

Build:

- Request and response schemas for users, tokens, questions, answers, and errors.
- Field constraints for email, password length, question length, and pagination.
- Cross-field validators where useful.
- One consistent error envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": []
  }
}
```

Done when:

- Invalid input returns the same error shape everywhere.
- Response models never leak password hashes or internal secrets.
- Tests assert the error envelope shape.

## Day 8: Authentication And Authorization

Exercise: `../exercises/day8_auth.py`

Build:

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /users/me`
- One admin-only endpoint.
- Password hashing with Argon2 or bcrypt.
- Short-lived access tokens and revocable refresh tokens.
- Role dependency such as `require_role("admin")`.

Done when:

- Register -> login -> `/users/me` works.
- Regular users cannot access admin routes.
- Refresh tokens can be revoked or rotated.
- Tests cover happy path and rejection paths.

## Day 9: Middleware, CORS, Logging, And Rate Limits

Exercise: `../exercises/day9_middleware.py`

Build:

- Request ID middleware that sets `X-Request-ID`.
- Timing middleware that sets `X-Process-Time`.
- CORS config with explicit allowed origins.
- Rate limiter for expensive endpoints.
- Structured request logs with method, path, status, duration, and request ID.

Required log fields:

- `request_id`
- `method`
- `path`
- `status_code`
- `latency_ms`
- `user_id` when authenticated

Done when:

- Every response has a request ID.
- Every request produces one useful structured log line.
- Rate-limited routes return a clear error envelope.

## Day 10: Async Database Integration

Exercise: `../exercises/day10_database.py`

Build:

- Async SQLAlchemy engine and `async_sessionmaker`.
- Alembic migrations.
- Tables for users and refresh tokens.
- Repository functions for user creation, lookup, token storage, and token revocation.
- Dependency override pattern for tests.

Done when:

- Tests can use an isolated test database or transaction rollback pattern.
- Route handlers do not contain raw SQLAlchemy query logic.
- Sessions are not shared across concurrent requests.

## Weekend 2: Production API Starter

Exercise: `../exercises/weekend2_fastapi_starter/README.md`

Fold Days 6-10 into the capstone and produce:

- Running app skeleton.
- Health endpoints.
- Auth flow.
- RBAC.
- Database migrations.
- Middleware.
- Error handlers.
- Test suite for auth and health checks.

## Week 2 Acceptance Gate

- [ ] `/health/live` and `/health/ready` work.
- [ ] `/docs` renders.
- [ ] Settings use `pydantic-settings`.
- [ ] Auth flow is tested.
- [ ] Admin route is protected.
- [ ] Error responses are consistent.
- [ ] Request ID and timing are present.
- [ ] Database sessions are request-scoped.
- [ ] Test dependency overrides work.

## Core Resources

| Resource | Use |
|---|---|
| https://fastapi.tiangolo.com/ | FastAPI docs |
| https://fastapi.tiangolo.com/tutorial/dependencies/ | dependency injection |
| https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ | JWT auth |
| https://docs.pydantic.dev/latest/ | Pydantic v2 |
| https://docs.pydantic.dev/latest/concepts/pydantic_settings/ | typed settings |
| https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html | SQLAlchemy async |
| https://alembic.sqlalchemy.org/ | migrations |

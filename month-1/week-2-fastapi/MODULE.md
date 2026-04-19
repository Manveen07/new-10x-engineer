# Week 2: FastAPI Production Patterns

## Why This Matters
FastAPI is the dominant framework for serving AI backends — RAG APIs, agent endpoints, embedding services, and LLM gateways. This week builds the patterns you'll reuse in every subsequent project.

---

## Day-by-Day Plan

### Monday — Project Structure and Dependency Injection (1.5h)

**Read (1h):**
- zhanymkanov/fastapi-best-practices repo (17k+ stars)
  https://github.com/zhanymkanov/fastapi-best-practices
  Focus on: project structure, dependency injection, Pydantic usage, error handling

**Read (30 min):**
- FastAPI official tutorial on dependencies
  https://fastapi.tiangolo.com/tutorial/dependencies/

**Key concepts:**
- `Depends()` creates a dependency injection chain — databases, auth, config all flow through this
- Separate routes, schemas, services, and repositories into distinct modules
- Use `APIRouter` for domain-based route organization
- Lifespan events (`@asynccontextmanager`) replace `on_event("startup")`

**Exercise:** See `exercises/day6_fastapi_structure.py`

Scaffold a project with this layout:
```
app/
  main.py          # FastAPI app + lifespan
  config.py        # Pydantic Settings
  dependencies.py  # shared Depends
  routers/
    users.py
    items.py
  schemas/
    users.py
    items.py
  services/
    user_service.py
  repositories/
    user_repository.py
```

**Additional resources:**
- FastAPI full-stack template (reference architecture)
  https://github.com/tiangolo/full-stack-fastapi-template
- Pydantic Settings docs
  https://docs.pydantic.dev/latest/concepts/pydantic_settings/

---

### Tuesday — Pydantic V2 Validation and Error Handling (1.5h)

**Read (45 min):**
- FastAPI docs on request body with nested models
  https://fastapi.tiangolo.com/tutorial/body-nested-models/
- FastAPI docs on handling errors
  https://fastapi.tiangolo.com/tutorial/handling-errors/

**Read (45 min):**
- Pydantic V2 migration guide (if you know V1)
  https://docs.pydantic.dev/latest/migration/
- Pydantic V2 validators
  https://docs.pydantic.dev/latest/concepts/validators/

**Key concepts:**
- `model_validator(mode="before")` for cross-field validation
- `field_validator` for individual field checks
- Custom error responses with `@app.exception_handler`
- Consistent error shape: `{"error": {"code": "...", "message": "...", "details": [...]}}`
- `model_config = ConfigDict(from_attributes=True)` for ORM integration

**Exercise:** See `exercises/day7_pydantic_validation.py`

Build 3 endpoints with:
- Nested Pydantic models (e.g., User with Address with GeoLocation)
- Custom validators (email format, phone number, date ranges)
- Structured error responses that always return the same JSON shape
- Response models that differ from request models (don't leak internal fields)

---

### Wednesday — Authentication and Authorization (1.5h)

**Read (1h):**
- FastAPI Security tutorial
  https://fastapi.tiangolo.com/tutorial/security/
- FastAPI OAuth2 with Password and Bearer
  https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

**Read (30 min):**
- PyJWT library docs
  https://pyjwt.readthedocs.io/en/stable/

**Key concepts:**
- OAuth2PasswordBearer flow with JWT tokens
- Access token (short-lived, 15-30 min) + Refresh token (long-lived, 7 days)
- Password hashing with `passlib[bcrypt]`
- RBAC: roles stored in JWT claims, checked via `Depends()`
- Never store sensitive data in JWT — it's base64, not encrypted

**Exercise:** See `exercises/day8_auth.py`

Implement:
- `/auth/register` — create user with hashed password
- `/auth/login` — return access + refresh tokens
- `/auth/refresh` — exchange refresh token for new access token
- `/users/me` — protected endpoint, requires valid token
- `/admin/users` — protected endpoint, requires admin role
- Role-based dependency: `require_role("admin")`

**Additional resource:**
- python-jose (alternative JWT library with more features)
  https://python-jose.readthedocs.io/en/latest/

---

### Thursday — Middleware, CORS, and Rate Limiting (1.5h)

**Read (20 min):**
- FastAPI Middleware docs
  https://fastapi.tiangolo.com/tutorial/middleware/

**Read (40 min):**
- FastAPI CORS docs
  https://fastapi.tiangolo.com/tutorial/cors/
- slowapi documentation (rate limiting)
  https://slowapi.readthedocs.io/en/latest/

**Read (30 min):**
- Starlette middleware internals
  https://www.starlette.io/middleware/

**Key concepts:**
- Middleware executes BEFORE route handlers — ideal for logging, timing, auth
- CORS must be configured for any frontend-backend split
- Rate limiting protects your LLM endpoints from abuse (LLM calls are expensive!)
- Request ID middleware for distributed tracing
- Exception middleware for consistent error responses

**Exercise:** See `exercises/day9_middleware.py`

Add to your project:
- Request logging middleware (method, path, status, duration)
- Request ID middleware (adds `X-Request-ID` header)
- CORS configuration (allow specific origins)
- Rate limiter with slowapi (10 req/min for expensive endpoints)
- Timing middleware (adds `X-Process-Time` header)

---

### Friday — Async Database Integration (1.5h)

**Read (45 min):**
- SQLAlchemy async docs
  https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Alembic tutorial
  https://alembic.sqlalchemy.org/en/latest/tutorial.html

**Read (45 min):**
- FastAPI + SQLAlchemy pattern from full-stack-fastapi-template
  https://github.com/tiangolo/full-stack-fastapi-template
  Focus on: `app/core/db.py`, `app/crud/`, `app/models/`

**Key concepts:**
- `create_async_engine` + `async_sessionmaker` for connection pooling
- Session-per-request pattern via `Depends(get_db)`
- Alembic for schema migrations (never modify DB schema manually)
- Repository pattern: separate DB logic from business logic
- Always use `async with session.begin()` for transactions

**Exercise:** See `exercises/day10_database.py`

Set up:
- Async SQLAlchemy with PostgreSQL (or SQLite for quick dev)
- User and Item models with relationships
- Alembic migrations (init + first migration)
- CRUD endpoints: create, read, update, delete with proper error handling
- Pagination with `offset` and `limit` parameters

**Additional resource:**
- Databases library (alternative to SQLAlchemy async)
  https://www.encode.io/databases/
- Tortoise ORM (Django-like async ORM)
  https://tortoise.github.io/

---

### Weekend — Production FastAPI Starter (1-2h)

See `exercises/weekend2_fastapi_starter/` for the project scaffold.

**Build a complete production-ready FastAPI starter with:**

1. Project structure following best practices
2. JWT auth with access + refresh tokens
3. RBAC with at least 2 roles (user, admin)
4. Async PostgreSQL with SQLAlchemy + Alembic
5. Pydantic V2 models (separate request/response schemas)
6. Structured error handling (consistent JSON shape)
7. Request logging + timing middleware
8. Rate limiting on auth endpoints
9. Health check endpoint (`/health`)
10. Docker Compose setup (app + postgres)
11. Tests with pytest (>80% coverage on auth flow)

**Done when:**
- `docker compose up` starts the full stack
- Auth flow works end-to-end (register → login → access protected route)
- `pytest` passes with >80% coverage
- You can demonstrate RBAC (admin-only endpoints reject regular users)

---

## Skill Checkpoint

1. What's the difference between `Depends()` and middleware? When would you use each?
2. Why use async SQLAlchemy over sync? What's the actual performance difference?
3. Demonstrate proper error propagation: DB error → service layer → API response
4. How does FastAPI's dependency injection compare to Flask's approach?
5. Design the auth flow for a multi-tenant SaaS API — what changes?

---

## Core Resources

| Resource | Type | URL |
|----------|------|-----|
| FastAPI official docs | Reference | https://fastapi.tiangolo.com |
| Pydantic V2 docs | Reference | https://docs.pydantic.dev/latest/ |
| SQLAlchemy async docs | Reference | https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html |
| fastapi-best-practices repo | Patterns | https://github.com/zhanymkanov/fastapi-best-practices |
| full-stack-fastapi-template | Reference impl | https://github.com/tiangolo/full-stack-fastapi-template |

## Supplementary Resources

- Talk: Sebastian Ramirez — FastAPI internals (YouTube)
- pytest-asyncio for testing async endpoints
  https://pytest-asyncio.readthedocs.io/en/latest/
- httpx for async test client
  https://www.python-httpx.org/
- FastAPI production deployment with Gunicorn + Uvicorn workers
  https://fastapi.tiangolo.com/deployment/server-workers/

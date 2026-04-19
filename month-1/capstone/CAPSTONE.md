# Month 1 Capstone: AI-Powered Q&A API

## Overview

Build a production-grade Q&A API that combines everything from Month 1. This is not a toy project — it's the foundation you'll extend in Months 2-4 with RAG pipelines, agents, and MCP servers.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                       Client                              │
│              (curl, Postman, or frontend)                  │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Backend                         │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐ │
│  │ JWT Auth │  │ Rate     │  │ Middleware              │ │
│  │ + RBAC   │  │ Limiter  │  │ (logging, timing, IDs) │ │
│  └──────────┘  └──────────┘  └────────────────────────┘ │
│                                                           │
│  ┌────────────────────── /qa/ask ─────────────────────┐  │
│  │                                                     │  │
│  │  1. Validate input (Pydantic)                       │  │
│  │  2. Check semantic cache (Redis)                    │  │
│  │       ├─ HIT → return cached response               │  │
│  │       └─ MISS → continue                            │  │
│  │  3. Call LLM via adapter pattern                    │  │
│  │  4. Cache the response                              │  │
│  │  5. Log query to PostgreSQL                         │  │
│  │  6. Return structured response                      │  │
│  │                                                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                           │
└──────┬─────────────────┬───────────────────┬─────────────┘
       │                 │                   │
       ▼                 ▼                   ▼
┌────────────┐  ┌──────────────┐  ┌──────────────────┐
│ PostgreSQL │  │ Redis Stack  │  │ LLM Provider     │
│            │  │              │  │ (via adapter)     │
│ - users    │  │ - semantic   │  │                   │
│ - queries  │  │   cache      │  │ - OpenAI          │
│ - history  │  │ - vectors    │  │ - Mock (testing)  │
│ - stats    │  │              │  │ - Anthropic       │
└────────────┘  └──────────────┘  └──────────────────┘
```

## Detailed Requirements

### 1. Project Structure

```
qa-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # App creation, lifespan, middleware
│   ├── config.py            # Pydantic Settings
│   ├── dependencies.py      # DB session, current user, etc.
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # /auth/register, /auth/login, /auth/refresh
│   │   ├── qa.py            # /qa/ask, /qa/history
│   │   └── admin.py         # /admin/stats, /admin/cache
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py          # Token, UserCreate, UserResponse
│   │   ├── qa.py            # Question, Answer, QueryHistory
│   │   └── admin.py         # StatsResponse, CacheStats
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Password hashing, token creation
│   │   ├── qa_service.py    # Core Q&A logic (cache check → LLM → cache store)
│   │   └── cache_service.py # Semantic cache operations
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py          # LLMProvider abstract base class
│   │   ├── openai.py        # OpenAI adapter
│   │   ├── anthropic.py     # Anthropic adapter
│   │   ├── mock.py          # Mock adapter (testing)
│   │   └── factory.py       # Provider factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py      # SQLAlchemy ORM models
│   └── middleware/
│       ├── __init__.py
│       ├── logging.py       # Request logging
│       ├── timing.py        # Request timing
│       └── rate_limit.py    # Rate limiting
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (test DB, test client)
│   ├── test_auth.py         # Auth flow tests
│   ├── test_qa.py           # Q&A endpoint tests
│   └── test_cache.py        # Semantic cache tests
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── alembic.ini
└── alembic/
    └── versions/
```

### 2. API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | None | Create account |
| POST | /auth/login | None | Get access + refresh tokens |
| POST | /auth/refresh | Refresh token | Get new token pair |
| POST | /qa/ask | Bearer token | Ask a question |
| GET | /qa/history | Bearer token | User's past queries |
| GET | /admin/stats | Admin only | Cache stats, top queries, latency |
| DELETE | /admin/cache | Admin only | Clear semantic cache |
| GET | /health | None | Service + dependency health |

### 3. Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',  -- 'user' or 'admin'
    tier VARCHAR(20) DEFAULT 'free',  -- 'free' or 'paid' (for rate limiting)
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Query history table
CREATE TABLE queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    provider VARCHAR(50) NOT NULL,      -- which LLM answered
    cache_hit BOOLEAN DEFAULT FALSE,    -- was this served from cache?
    latency_ms FLOAT NOT NULL,          -- total response time
    input_tokens INTEGER,
    output_tokens INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_queries_user_id ON queries(user_id);
CREATE INDEX idx_queries_created_at ON queries(created_at);
CREATE INDEX idx_queries_cache_hit ON queries(cache_hit);
```

### 4. Core Flow: /qa/ask

```python
async def ask_question(question: str, user: User, db: AsyncSession):
    start = time.perf_counter()

    # Step 1: Check semantic cache
    cache_result = await cache_service.get(question)
    if cache_result.hit:
        latency = (time.perf_counter() - start) * 1000
        await log_query(db, user, question, cache_result.response,
                       cache_hit=True, latency_ms=latency, provider="cache")
        return {"answer": cache_result.response, "cached": True, "latency_ms": latency}

    # Step 2: Call LLM
    provider = get_llm_provider()  # From factory, based on env var
    llm_response = await provider.complete([
        {"role": "system", "content": "You are a helpful assistant. Answer concisely."},
        {"role": "user", "content": question},
    ])

    # Step 3: Cache the response
    await cache_service.set(question, llm_response.content)

    # Step 4: Log to database
    latency = (time.perf_counter() - start) * 1000
    await log_query(db, user, question, llm_response.content,
                   cache_hit=False, latency_ms=latency,
                   provider=provider.provider_name,
                   input_tokens=llm_response.input_tokens,
                   output_tokens=llm_response.output_tokens)

    return {
        "answer": llm_response.content,
        "cached": False,
        "latency_ms": latency,
        "provider": provider.provider_name,
    }
```

### 5. Rate Limiting Tiers

| Tier | /qa/ask limit | Other endpoints |
|------|--------------|-----------------|
| free | 10 req/min | 60 req/min |
| paid | 100 req/min | 300 req/min |
| admin | unlimited | unlimited |

### 6. Environment Variables

```env
# .env.example
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/qa_api
REDIS_URL=redis://localhost:6379

SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

LLM_PROVIDER=mock           # mock, openai, anthropic
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

CACHE_SIMILARITY_THRESHOLD=0.88
CACHE_TTL_SECONDS=3600

RATE_LIMIT_FREE=10
RATE_LIMIT_PAID=100
```

### 7. Docker Compose

```yaml
# docker-compose.yml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/qa_api
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: qa_api
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis/redis-stack:latest
    ports:
      - "6379:6379"
      - "8001:8001"  # RedisInsight UI

volumes:
  pgdata:
```

## Evaluation Criteria

### Must Have (pass/fail)
- [ ] Auth flow works end-to-end (register → login → ask question)
- [ ] RBAC enforced (admin endpoints reject regular users)
- [ ] Semantic cache returns cached results for similar queries
- [ ] LLM provider swappable via environment variable
- [ ] Docker Compose starts the full stack
- [ ] Health endpoint checks all dependencies

### Quality Metrics
- [ ] Cache hit rate >60% on repeated similar queries
- [ ] API handles 50 concurrent requests without errors
- [ ] Consistent error response shape across all endpoints
- [ ] All middleware working (request IDs, logging, timing)
- [ ] Tests pass with >70% coverage

### Stretch Goals
- [ ] Streaming responses for LLM calls
- [ ] WebSocket endpoint for real-time Q&A
- [ ] Query analytics dashboard endpoint
- [ ] Automatic cache warming on startup

## Architecture Decision Record (ADR)

After building, write a brief ADR answering:

1. **Why FastAPI over Flask/Django?**
   (async native, auto-docs, Pydantic integration, dependency injection)

2. **Why PostgreSQL for metadata + Redis for cache?**
   (relational data needs ACID; cache needs speed + vector similarity)

3. **Why the adapter pattern for LLM providers?**
   (providers change constantly; testing needs mocks; fallback support)

4. **Why semantic caching instead of exact-match?**
   (users ask the same question different ways; LLM calls are expensive)

5. **What would you change with more time?**
   (your honest assessment — this shows engineering maturity)

## How This Connects to Month 2

In Month 2, you'll extend this system with:
- Vector database (pgvector) for document storage
- RAG pipeline (retrieval + generation)
- Advanced retrieval (hybrid search, reranking)
- The /qa/ask endpoint becomes a full RAG endpoint

Everything you build this month is the foundation. Build it well.

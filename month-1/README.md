# Month 1 - Backend and Async Foundations for AI Systems

## Goal

Build the production Python foundation for AI engineering. By the end of this month, you should have a runnable Q&A API that demonstrates async Python, FastAPI, Pydantic v2, typed settings, auth, RBAC, async PostgreSQL, Redis semantic caching, swappable LLM providers, structured logs, tests, Docker, and clear architecture decisions.

This month is not about RAG yet. RAG starts in Month 2. Month 1 is the backend layer that every later AI system depends on.

## Final Outcome

The Month 1 capstone is `month-1/capstone/qa-api/`: a production-shaped FastAPI Q&A API.

It should include:

- `uv` project setup with `pyproject.toml`, lockfile, Ruff, mypy, and pytest.
- FastAPI app with `/health/live`, `/health/ready`, `/auth/*`, `/users/me`, `/qa/ask`, `/qa/history`, and admin cache/stats endpoints.
- Pydantic v2 schemas and `pydantic-settings` config.
- JWT auth with access and refresh tokens.
- RBAC for admin-only routes.
- Async SQLAlchemy + PostgreSQL for users, tokens, query history, provider calls, and cache metadata.
- Redis for exact cache, semantic cache, and rate-limit buckets.
- Provider abstraction with mock, OpenAI, Anthropic, and optional local provider paths.
- Structured JSON logs with request ID, user ID where available, provider, model, latency, cache outcome, token counts, and estimated cost.
- Tests that run without live LLM calls.
- Docker Compose for API, PostgreSQL, and Redis.
- ADRs explaining the major decisions.

## Technical Baseline

| Area | Standard |
|---|---|
| Python | 3.12+ |
| Environment and packages | `uv`, `pyproject.toml`, `uv.lock` |
| Lint and format | `ruff check`, `ruff format` |
| Types | `mypy --strict` for capstone code |
| API | FastAPI, async endpoints, lifespan-managed clients |
| Validation | Pydantic v2 and JSON Schema |
| Settings | `pydantic-settings`; no scattered `os.getenv` |
| HTTP | `httpx.AsyncClient` |
| Retries | `stamina` or equivalent bounded retries with explicit timeouts |
| Logs | `structlog` structured JSON logs |
| Tests | pytest, pytest-asyncio, httpx test client, respx, mocked providers |
| Data | PostgreSQL async SQLAlchemy, Alembic migrations |
| Cache | Redis exact cache and semantic cache |
| Deployment | Docker Compose locally, Cloud Run-ready container |

## Month Structure

| Week | Theme | Main deliverable |
|---|---|---|
| 1 | Tooling plus async Python | async scraper/enrichment pipeline with bounded concurrency |
| 2 | FastAPI production patterns | API starter with validation, auth, RBAC, middleware, DB sessions |
| 3 | PostgreSQL plus AI design patterns | query history schema, provider abstraction, retries, cost logging |
| 4 | Semantic caching plus capstone integration | Q&A API with Redis cache, provider calls, tests, docs, ADRs |

## Daily Exercise Map

Use this as the progress checklist. Each exercise should either update the capstone directly or produce a small standalone proof that you later fold into the capstone.

| Day | Exercise | File or folder | Required output |
|---|---|---|---|
| 0 | Modern tooling setup | `exercises/day0_tooling_setup.md` | uv project, Ruff, mypy, pytest, first ADR |
| 1 | Coroutines and event loop | `exercises/day1_coroutines.py` | working async functions and timing proof |
| 2 | Concurrent execution | `exercises/day2_gather.py` | gather/as_completed behavior and error handling |
| 3 | Semaphores and rate limits | `exercises/day3_semaphores.py` | bounded concurrency and token bucket limiter |
| 4 | Producer-consumer queues | `exercises/day4_queue.py` | queue with backpressure and clean shutdown |
| 5 | TaskGroup and cancellation | `exercises/day5_taskgroup.py` | structured concurrency and failure behavior |
| Weekend 1 | Async pipeline | `exercises/weekend1_scraper_pipeline.py` | scraper/enrichment pipeline with logs and retries |
| 6 | FastAPI structure and DI | `exercises/day6_fastapi_structure.py` | route/schema/service/repository layout |
| 7 | Pydantic v2 validation | `exercises/day7_pydantic_validation.py` | strict schemas, validators, error envelope |
| 8 | Auth and RBAC | `exercises/day8_auth.py` | register/login/refresh/me/admin flow |
| 9 | Middleware and rate limiting | `exercises/day9_middleware.py` | request ID, timing, CORS, rate-limit behavior |
| 10 | Async DB integration | `exercises/day10_database.py` | async sessions, migrations, repository pattern |
| Weekend 2 | Production API starter | `exercises/weekend2_fastapi_starter/README.md` | capstone skeleton with auth, DB, middleware, tests |
| 11 | EXPLAIN ANALYZE | `exercises/day11_explain_analyze.py` | before/after query plans and notes |
| 12 | Indexing strategies | `exercises/day12_indexing.py` | B-tree, GIN, partial, composite index benchmarks |
| 13 | Query tuning | `exercises/day13_query_tuning.py` | three rewritten slow queries with evidence |
| 14 | LLM provider adapter | `exercises/day14_adapter_pattern.py` | mock/OpenAI/Anthropic provider contract |
| 15 | Strategy and factory patterns | `exercises/day15_strategy_factory.py` | configurable embedding/retrieval/provider strategies |
| Weekend 3 | Provider integration | `exercises/weekend3_provider_observability.md` | capstone provider factory, retries, provider logs |
| 16 | Redis vector search | `exercises/day16_redis_vectors.py` | Redis Stack vector index and similarity search |
| 17 | Semantic cache | `exercises/day17_semantic_cache.py` | get/set cache API with threshold and TTL |
| 18 | Cache tuning and eval | `exercises/day18_cache_tuning.py` | threshold sweep, false hit/miss report, cost estimate |
| 19 | AI system design | `exercises/day19_ai_system_design.md` | architecture diagrams and failure-mode notes |
| 20 | Capstone polish | `capstone/CAPSTONE.md` | README, ADRs, tests, demo script, final checklist |

## Weekly Acceptance Gates

### Week 1 Gate

- You can explain `await`, the event loop, `gather`, `TaskGroup`, semaphores, queues, cancellation, and backpressure.
- The weekend pipeline processes 50+ items with bounded concurrency.
- Failures are logged and retried without crashing the whole run.
- The pipeline emits structured fields: item ID, status, latency, attempt, error.

### Week 2 Gate

- The capstone app starts with FastAPI and a clean folder layout.
- `/health/live` and `/health/ready` exist.
- Auth flow works: register, login, refresh, `/users/me`.
- Admin-only route rejects normal users.
- Errors return one consistent JSON shape.
- Tests cover auth, validation errors, and dependency overrides.

### Week 3 Gate

- PostgreSQL schema supports users, refresh tokens, query history, provider calls, and cache metadata.
- Slow-query exercises include evidence from `EXPLAIN (ANALYZE, BUFFERS)`.
- LLM provider calls go through a provider interface, never direct SDK imports inside routes.
- Mock provider works in tests without API keys.
- Provider logs include model, latency, token counts, status, retry count, and estimated cost.

### Week 4 Gate

- `/qa/ask` checks cache first, calls provider on miss, stores query history, and returns structured output.
- Redis exact cache and semantic cache are both demonstrable.
- Cache outcomes are logged as `exact_hit`, `semantic_hit`, or `miss`.
- Threshold tuning report explains false positives, false negatives, latency saved, and estimated cost saved.
- Docker Compose starts API, PostgreSQL, and Redis.
- README and ADRs make the system understandable in under five minutes.

## Capstone Milestones

Build the capstone incrementally instead of waiting until the last weekend.

| Milestone | When | Output |
|---|---|---|
| M1 | End of Day 0 | tooling, `pyproject.toml`, Ruff, mypy, pytest |
| M2 | End of Week 1 | async helper library for provider/cache calls |
| M3 | End of Week 2 | FastAPI app with auth, RBAC, health checks, middleware |
| M4 | End of Week 3 | database schema, provider abstraction, mocked provider tests |
| M5 | End of Week 4 | cache, `/qa/ask`, query history, docs, tests, Docker |

## Required Documentation

Create these docs as you build:

```text
month-1/capstone/qa-api/docs/
  architecture.md
  demo-script.md
  decisions/
    0001-tooling-choices.md
    0002-fastapi-project-structure.md
    0003-provider-adapter-pattern.md
    0004-semantic-cache-design.md
    0005-cloud-run-deployment-target.md
  benchmarks/
    cache-threshold-sweep.md
    qa-api-latency.md
```

## Not Doing In Month 1

- Full document RAG.
- LangChain or LangGraph.
- MCP.
- Multi-agent workflows.
- Fine-tuning.
- Kubernetes.
- A production frontend.

These start later. Month 1 should ship one reliable backend foundation.

## How To Work Each Day

1. Read the week module for context.
2. Complete the day's exercise.
3. Move the useful piece into the capstone.
4. Add or update at least one test.
5. Record any architecture decision that would matter to a reviewer.

## Final Month 1 Checklist

- [ ] `uv run ruff check .` passes.
- [ ] `uv run ruff format --check .` passes.
- [ ] `uv run mypy app` passes.
- [ ] `uv run pytest` passes.
- [ ] Docker Compose starts all local services.
- [ ] Auth flow works end to end.
- [ ] `/qa/ask` works with mock provider and no external API key.
- [ ] Cache hit and miss paths are tested.
- [ ] Provider failure path is tested.
- [ ] README has setup, architecture, demo, endpoints, tests, and known limitations.
- [ ] ADRs explain the major choices.
- [ ] Month 2 can reuse the app foundation for RAG.

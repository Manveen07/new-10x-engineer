# Month 1 Implementation Plan for new-10x-engineer

## Executive summary

The existing Month 1 material in the repository already sets the right end-state: an async Python and FastAPI foundation that culminates in a production-ready Q&A API with semantic caching, async PostgreSQL, and swappable LLM providers. The repository currently organizes Month 1 as learning modules for async Python, FastAPI, PostgreSQL/patterns, and caching/system design, so the right implementation move is **not** to rewrite those educational folders, but to add a **single recruiter-facing capstone implementation** under `month-1/capstone/qa-api/` that turns the syllabus into a runnable product. citeturn9view1turn10view0

My recommendation is to build Month 1 around **FastAPI + SQLAlchemy async + Cloud SQL PostgreSQL with pgvector + Redis + Cloud Run + Cloud Run Jobs**, with **OpenAI as the default hosted provider**, **Anthropic as the second hosted adapter**, and **Ollama or vLLM as the local/self-hosted path**. The strongest reason to choose **Cloud Run** over **AWS App Runner** today is that Cloud Run natively fits streaming HTTP responses, configurable concurrency, health checks, and run-to-completion jobs, while App Runner now carries an availability warning that it will no longer be open to new customers starting **April 30, 2026**. citeturn29search0turn17view3turn14view12turn17view4turn25view1

The highest-value Month 1 outcome is a system that is small enough to finish in four weeks, but concrete enough to impress recruiters. That means the implementation should optimize for: **production-readiness**, **observability**, **defensible architecture**, **clean async code**, and **public proof of work**. The capstone should ship with a deployed demo URL, a polished README, architecture diagrams, benchmark results, screenshots, and GitHub Actions automation, not just application code.

### Goals

| Goal | Why it matters | Month 1 target |
|---|---|---|
| Async backend fluency | This is the actual “backend & async foundations” layer the repo describes | All IO paths async: DB, Redis, provider calls, ingestion |
| Production API patterns | FastAPI alone is not enough; structure, auth, errors, and lifecycle matter | JWT auth, RBAC, typed schemas, consistent error envelope |
| AI-system primitives | Recruiters want evidence you understand LLM systems, not just CRUD | Provider abstraction, semantic caching, embeddings, streaming |
| Operational maturity | Job-ready means deploy, monitor, secure, and benchmark | CI/CD, Cloud Run deploy, structured logs, metrics, smoke and load tests |
| Portfolio signal | The repo needs one obvious artifact a reviewer can run or inspect | public README, diagrams, screenshots, demo URL, benchmark report |

### Deliverables

The Month 1 capstone should produce these concrete artifacts:

| Deliverable | Format | Acceptance signal |
|---|---|---|
| Public capstone service | Cloud Run URL | `/health/ready` works and `/docs` renders in staging |
| Production README | Markdown | explains architecture, setup, demo flow, screenshots, benchmarks |
| Architecture diagram | Mermaid + rendered PNG | embedded in README and docs |
| Benchmark report | Markdown + CSV/JSON results | latency, throughput, cache hit rates, estimated cost |
| Security slice | Code + tests | register/login/refresh, `/users/me`, admin-only ingestion |
| Semantic cache | Code + tests | exact Redis hit and semantic pgvector hit both demonstrated |
| Ingestion workflow | Cloud Run Job + local worker | can ingest seeded demo documents and answer from them |
| CI/CD pipeline | GitHub Actions | lint, type-check, tests, image build, deploy |
| Screenshots | PNGs in docs folder | Swagger, logs, benchmark chart, architecture, GitHub Actions run |

### Success criteria

These are the pass/fail criteria I would use for Month 1:

| Area | Success criterion |
|---|---|
| Correctness | Unit + integration tests pass; OpenAPI snapshot stable |
| Reliability | health endpoints work; streaming endpoint closes cleanly; retries are bounded |
| Security | no plaintext passwords; JWT access tokens short-lived; refresh tokens revocable; RBAC enforced |
| Performance | cache-hit path materially faster than cache-miss path |
| Observability | every request emits request ID, trace fields, provider/model, cache outcome, latency |
| Deployment | one-command local dev, one-merge staging deployment |
| Recruiter signal | README makes the system legible in under five minutes |

## Recommended technical baseline

### Why this stack is the right Month 1 scope

Use **FastAPI** because the framework directly supports async path operations, security helpers, generated OpenAPI, and streaming responses, which matches this month’s learning goals well. Use `async def` endpoints, an application-scoped `httpx.AsyncClient`, and a request-scoped SQLAlchemy `AsyncSession`; SQLAlchemy explicitly warns that a session is mutable, stateful, and **must not be shared across concurrent asyncio tasks**. Use `pydantic-settings` for configuration because it is designed to load typed settings from environment variables or secret files. citeturn15view4turn22view0turn22view1turn22view6turn22view4

Use **PostgreSQL + pgvector** as the default data plane because Month 1 should stay focused on one operationally coherent backend. pgvector lets you keep vectors with the rest of your application data, supports both exact and approximate nearest-neighbor search, and Cloud SQL supports pgvector on PostgreSQL. A particularly important nuance for Month 1 is that pgvector’s own release guidance says that if you can hit your performance target without ANN, exact search is preferable because it gives **100% recall**. That suggests a staged plan: start with exact vector search for small chunk tables and semantic cache tables, then add **HNSW** when the dataset or QPS justifies it. citeturn23search11turn24view2turn24view3turn15view1turn15view2

Use **Redis** as the hot cache and lock manager, not as the source of truth. Redis supports controlled expiration through `EXPIRE`/TTL, making it ideal for exact-key cache entries, stampede protection, and short-lived rate-limiter buckets. PostgreSQL remains the canonical store for semantic cache metadata and chunk embeddings. citeturn16view9turn16view8

Use **Cloud Run** for the API and **Cloud Run Jobs** for ingestion. Cloud Run supports streaming HTTP responses, configurable per-instance concurrency, health checks, minimum warm instances, and automatic logging into Cloud Logging. Cloud Run Jobs are explicitly designed for containers that run to completion and do not serve requests, which is exactly the shape of a document-ingestion worker. citeturn29search0turn17view1turn17view2turn17view3turn17view0turn14view12turn17view4turn21view0

### Deployment target decision

I recommend **Cloud Run** and not App Runner.

| Option | Verdict for Month 1 | Reason |
|---|---|---|
| Cloud Run | **Choose this** | Better fit for streaming AI responses, run-to-completion jobs, first-party GCP path to Cloud SQL and Memorystore |
| App Runner | Do not choose | Simpler source/image deploy story, but weaker fit for this exact design and currently carries an availability change for new customers |

Cloud Run’s fit is grounded in official documentation: it supports streaming HTTP responses with chunked transfer, allows up to 1,000 concurrent requests per instance with configurable lower limits, supports readiness/liveness health checks, and can keep idle instances warm via minimum instances. App Runner remains a valid managed container product in AWS, but AWS documentation now warns that it will no longer be open to new customers starting April 30, 2026, which makes it the wrong strategic bet for a new portfolio project built today. citeturn29search0turn17view1turn17view3turn17view0turn14view12turn25view0turn25view1

### Vector database comparison

| Option | Best fit | Strengths | Tradeoffs | Month 1 recommendation |
|---|---|---|---|---|
| pgvector | Early-stage product, one-database architecture | SQL joins, ACID, exact and ANN search, same DB as auth/app data | You own more query/index tuning | **Default choice** |
| Pinecone | Higher-scale dedicated retrieval layer | Fully managed, serverless, strong production retrieval story | Another service, eventual consistency, more ops surface | Later-stage move |
| Weaviate | Search-heavy AI apps, richer retrieval stack | Managed cloud option, semantic + BM25F hybrid search | More platform surface than Month 1 needs | Consider in Month 2+ |

This comparison is grounded in primary docs: pgvector stores vectors in Postgres and supports exact and approximate NN search; Cloud SQL supports pgvector and index creation for embeddings. Pinecone positions itself as fully managed and serverless, recommends a single hybrid index for most hybrid-search use cases, and documents that its system is eventually consistent. Weaviate documents both managed cloud and hybrid search that fuses vector search with BM25F search. For Month 1, that evidence points to pgvector as the lowest-complexity and most defensible choice. citeturn23search11turn24view2turn24view3turn28view0turn16view1turn16view2turn16view4turn16view3turn16view5

### LLM provider comparison

| Provider path | Best use | Strengths | Tradeoffs | Month 1 role |
|---|---|---|---|---|
| OpenAI | Default hosted provider | Responses API, semantic streaming events, built-in tools ecosystem, cached input pricing | Vendor lock-in if used directly everywhere | **Primary default** |
| Anthropic | Second hosted provider | Async streaming, strong tool-use model, official prompt caching | Different API shape from OpenAI | **Secondary adapter** |
| Local LLMs | Privacy-first or offline dev | Ollama is easy locally; vLLM gives OpenAI-compatible serving | Hardware burden, quality and latency depend on infra | **Dev and optional self-hosted path** |

This recommendation is supported by the vendor docs. OpenAI’s official API docs position the **Responses API** as the advanced interface, document semantic event-based streaming, and publish cached-input pricing. Anthropic documents async streaming, tool-use execution modes, and prompt caching that reduces latency and cost on repeated prompt material. Ollama documents a stable local API and default REST streaming, while vLLM documents an OpenAI-compatible server interface. For Month 1, the cleanest abstraction is **OpenAI-first with Anthropic parity and a local adapter seam**, not a “support every provider equally” design. citeturn17view9turn17view7turn26view0turn17view8turn27view0turn26view6turn17view11turn26view4turn17view12

## Target architecture

### Recommended shape

The capstone should be a small system with four runtime roles:

1. **API service** on Cloud Run, handling auth, Q&A, streaming, retrieval, and cache coordination.
2. **PostgreSQL** for users, roles, refresh tokens, documents, chunks, semantic cache metadata, and query audit rows.
3. **Redis** for exact-response cache entries, short locks, and rate-limit buckets.
4. **Ingestion worker** as a Cloud Run Job for chunking and embedding documents.

Cloud Run should sit in the same region as Cloud SQL, because Google explicitly recommends colocating Cloud Run and Cloud SQL for better latency and lower networking risk. Redis connectivity should use **Direct VPC egress**, which Google recommends because it lowers latency and cost and improves throughput versus connector-based paths. citeturn24view0turn24view1

```mermaid
flowchart LR
    U[Client or Recruiter Demo] --> G[Cloud Run API Service]
    G --> A[Auth and RBAC]
    G --> Q[Answer Service]
    G --> R[Redis Exact Cache and Locks]
    G --> P[(Cloud SQL PostgreSQL + pgvector)]
    Q --> O[LLM Provider Adapter]
    O --> OP[OpenAI]
    O --> AN[Anthropic]
    O --> LL[Ollama or vLLM]

    W[Cloud Run Job Ingestion Worker] --> P
    W --> O

    P --> T1[Users and Roles]
    P --> T2[Documents and Chunks]
    P --> T3[Semantic Cache Entries]
    P --> T4[Refresh Tokens and Audit]

    G --> L[Structured Logs and Metrics]
```

### Service-level recommendations

Treat the API as a mostly IO-bound service. FastAPI’s async guidance is clear: use `async def` when the libraries you call are awaitable, and mix sync/async only where appropriate. Because LLM requests and DB calls are network-bound, this service should be async end-to-end. Start Cloud Run at **concurrency 8** for the Q&A service, not the default 80, because streaming requests stay open longer and can amplify memory pressure; that is an engineering recommendation based on Cloud Run’s explicit support for configurable concurrency and the ability to lower it when your code should not process too many parallel requests per instance. Set **min instances = 1** in staging/production to reduce cold starts for recruiter demos, and set a **timeout of 120s** for the Q&A service. Cloud Run allows request timeouts below a hard maximum of 60 minutes. citeturn15view4turn17view3turn17view2turn17view0

### Semantic cache flow

```mermaid
sequenceDiagram
    participant C as Client
    participant API as FastAPI API
    participant REDIS as Redis
    participant PG as Postgres + pgvector
    participant LLM as Provider

    C->>API: POST /v1/answers/stream
    API->>REDIS: GET exact:{digest}
    alt Exact hit
        REDIS-->>API: cached payload
        API-->>C: stream cached answer
    else Exact miss
        API->>PG: semantic cache nearest-neighbor lookup
        alt Semantic hit above threshold and same fingerprint
            PG-->>API: cached semantic entry
            API->>REDIS: SET exact:{digest}
            API-->>C: stream cached semantic answer
        else True miss
            API->>LLM: stream generation request
            LLM-->>API: token deltas
            API-->>C: token stream
            API->>REDIS: SET exact cache + short lock cleanup
            API->>PG: INSERT semantic cache entry
        end
    end
```

The important design guardrails are: cache only when temperature is deterministic or near-deterministic, bind every semantic cache entry to a **namespace**, **provider/model**, **system-prompt hash**, and **retrieval fingerprint**, and never allow a semantic hit to cross tenant, auth, or knowledge-base boundaries. That gives you speed without silently serving stale or cross-tenant answers.

## API contract and data model

### API surface

Use a small but complete surface area:

| Path | Method | Auth | Purpose |
|---|---|---|---|
| `/health/live` | GET | none | liveness probe |
| `/health/ready` | GET | none | readiness probe, checks DB + Redis |
| `/v1/auth/register` | POST | none | create user |
| `/v1/auth/login` | POST | none | issue access + refresh tokens |
| `/v1/auth/refresh` | POST | refresh token | rotate access token |
| `/v1/users/me` | GET | bearer | current user profile |
| `/v1/documents/ingest` | POST | admin | enqueue or trigger ingestion |
| `/v1/documents/{document_id}` | GET | admin | inspect document metadata |
| `/v1/answers` | POST | bearer | synchronous answer |
| `/v1/answers/stream` | POST | bearer | SSE or chunked streaming answer |
| `/metrics` | GET | internal only | Prometheus-style metrics |

### OpenAPI outline

```yaml
openapi: 3.1.0
info:
  title: Month 1 QA API
  version: 0.1.0
servers:
  - url: https://staging.example.run.app
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    ErrorEnvelope:
      type: object
      properties:
        error:
          type: object
          properties:
            code: { type: string }
            message: { type: string }
            request_id: { type: string }
            details:
              type: array
              items: { type: object }
    AnswerRequest:
      type: object
      required: [question, namespace]
      properties:
        question: { type: string, minLength: 1 }
        namespace: { type: string }
        stream: { type: boolean, default: false }
        model: { type: string, default: "default" }
    AnswerResponse:
      type: object
      properties:
        answer: { type: string }
        citations:
          type: array
          items:
            type: object
            properties:
              document_id: { type: string, format: uuid }
              chunk_id: { type: string, format: uuid }
        cache:
          type: object
          properties:
            hit_type: { type: string, enum: [none, exact, semantic] }
            similarity: { type: number, nullable: true }
        usage:
          type: object
          properties:
            provider: { type: string }
            model: { type: string }
            input_tokens: { type: integer }
            output_tokens: { type: integer }
paths:
  /health/live:
    get:
      summary: Liveness check
      responses:
        "200": { description: OK }
  /health/ready:
    get:
      summary: Readiness check
      responses:
        "200": { description: Ready }
        "503": { description: Not ready }
  /v1/auth/login:
    post:
      summary: Login
      responses:
        "200": { description: Access and refresh tokens issued }
  /v1/answers:
    post:
      security: [{ bearerAuth: [] }]
      summary: Generate a full answer
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/AnswerRequest" }
      responses:
        "200":
          description: Answer generated
          content:
            application/json:
              schema: { $ref: "#/components/schemas/AnswerResponse" }
  /v1/answers/stream:
    post:
      security: [{ bearerAuth: [] }]
      summary: Stream answer tokens
      responses:
        "200":
          description: text/event-stream
```

### Security model

FastAPI’s official JWT tutorial is the right starting point: use OAuth2 password flow for login, JWT bearer tokens for access, and secure password hashing. FastAPI’s documentation explicitly notes that JWT payloads are **not encrypted**, only signed, so roles and identifiers are fine in claims, but secrets and sensitive data are not. The same tutorial now recommends `pwdlib[argon2]` with **Argon2** as the password hashing algorithm. citeturn19view0turn22view3

Recommended claim shape for access tokens:

```json
{
  "sub": "user_uuid",
  "email": "user@example.com",
  "roles": ["user"],
  "scope": "answers:read documents:read",
  "jti": "token_uuid",
  "exp": 1713530000,
  "iat": 1713529100,
  "iss": "month1-qa-api"
}
```

Recommended auth rules:

- access token TTL: **15 minutes**
- refresh token TTL: **7 days**
- store only a **hashed refresh token identifier** in Postgres
- rotate refresh tokens on use
- invalidate refresh tokens on logout and password reset
- enforce RBAC in dependencies, not inside route bodies

### Data schemas

Use a single relational schema with pgvector.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE roles (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE user_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_jti_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE documents (
    id UUID PRIMARY KEY,
    namespace TEXT NOT NULL,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_uri TEXT,
    content_sha256 TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    token_count INT NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE semantic_cache_entries (
    id UUID PRIMARY KEY,
    namespace TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    system_prompt_hash TEXT NOT NULL,
    retrieval_fingerprint TEXT NOT NULL,
    normalized_query TEXT NOT NULL,
    query_embedding VECTOR(1536) NOT NULL,
    response_text TEXT NOT NULL,
    response_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    similarity_threshold NUMERIC(4,3) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    input_tokens INT,
    output_tokens INT,
    latency_ms INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_document_chunks_namespace_doc
    ON documents(namespace, created_at DESC);

CREATE INDEX idx_chunks_embedding_hnsw
    ON document_chunks USING hnsw (embedding vector_cosine_ops);

CREATE INDEX idx_semantic_cache_embedding_hnsw
    ON semantic_cache_entries USING hnsw (query_embedding vector_cosine_ops);
```

The `VECTOR(1536)` choice is sensible if you standardize on a small OpenAI embedding model; OpenAI’s embeddings guide documents that `text-embedding-3-small` defaults to 1536 dimensions. If you switch embedding providers later, version the schema and namespace by embedding model to avoid mixing incompatible vector spaces. citeturn32search1

## File blueprint and core code

### Repository layout

Keep the current educational folders intact and add this implementation layout:

```text
new-10x-engineer/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── month1-ci.yml
│       └── month1-deploy-cloud-run.yml
├── month-1/
│   ├── README.md
│   ├── week-1-async-python/
│   ├── week-2-fastapi/
│   ├── week-3-postgres-and-patterns/
│   ├── week-4-caching-and-system-design/
│   └── capstone/
│       └── qa-api/
│           ├── README.md
│           ├── .env.example
│           ├── .dockerignore
│           ├── Makefile
│           ├── pyproject.toml
│           ├── alembic.ini
│           ├── Dockerfile
│           ├── docker-compose.yml
│           ├── alembic/
│           │   ├── env.py
│           │   └── versions/
│           │       └── 0001_initial.py
│           ├── app/
│           │   ├── main.py
│           │   ├── config.py
│           │   ├── dependencies.py
│           │   ├── logging.py
│           │   ├── observability.py
│           │   ├── exceptions.py
│           │   ├── api/
│           │   │   ├── auth.py
│           │   │   ├── users.py
│           │   │   ├── answers.py
│           │   │   ├── documents.py
│           │   │   └── health.py
│           │   ├── auth/
│           │   │   ├── jwt.py
│           │   │   ├── passwords.py
│           │   │   └── rbac.py
│           │   ├── cache/
│           │   │   ├── keys.py
│           │   │   ├── exact_cache.py
│           │   │   └── semantic_cache.py
│           │   ├── db/
│           │   │   ├── base.py
│           │   │   ├── session.py
│           │   │   ├── models.py
│           │   │   └── repositories/
│           │   │       ├── users.py
│           │   │       ├── documents.py
│           │   │       ├── chunks.py
│           │   │       ├── refresh_tokens.py
│           │   │       └── semantic_cache.py
│           │   ├── providers/
│           │   │   ├── base.py
│           │   │   ├── registry.py
│           │   │   ├── openai_provider.py
│           │   │   ├── anthropic_provider.py
│           │   │   └── ollama_provider.py
│           │   ├── schemas/
│           │   │   ├── auth.py
│           │   │   ├── users.py
│           │   │   ├── answers.py
│           │   │   └── documents.py
│           │   ├── services/
│           │   │   ├── answer_service.py
│           │   │   ├── retrieval_service.py
│           │   │   └── ingest_service.py
│           │   └── utils/
│           │       ├── chunking.py
│           │       ├── hashing.py
│           │       ├── ids.py
│           │       └── normalize.py
│           ├── worker/
│           │   ├── main.py
│           │   └── jobs.py
│           ├── docs/
│           │   ├── architecture.md
│           │   ├── architecture.mmd
│           │   ├── api.md
│           │   ├── benchmarks.md
│           │   ├── deployment-cloud-run.md
│           │   └── screenshots/
│           │       └── .gitkeep
│           ├── infra/
│           │   ├── cloudrun/
│           │   │   ├── api.service.yaml
│           │   │   └── ingest.job.yaml
│           │   └── sql/
│           │       └── init.sql
│           ├── scripts/
│           │   ├── seed_demo_user.py
│           │   ├── seed_sample_docs.py
│           │   └── export_openapi.py
│           └── tests/
│               ├── conftest.py
│               ├── unit/
│               ├── integration/
│               ├── contract/
│               └── load/
│                   ├── k6-smoke.js
│                   └── k6-stream.js
```

### Prioritized implementation tasks

| Priority | File path | What to implement |
|---|---|---|
| P0 | `app/config.py` | typed settings, env parsing, secret-friendly config |
| P0 | `app/db/session.py` | async engine, sessionmaker, dependency injection |
| P0 | `app/auth/passwords.py` | Argon2 hash + verify |
| P0 | `app/auth/jwt.py` | access/refresh token creation and verification |
| P0 | `app/auth/rbac.py` | `require_roles()` dependency |
| P0 | `app/providers/base.py` | provider interface |
| P0 | `app/providers/openai_provider.py` | default hosted adapter |
| P0 | `app/cache/semantic_cache.py` | exact + semantic cache orchestration |
| P0 | `app/services/answer_service.py` | retrieval, cache lookup, provider call, persistence |
| P0 | `app/api/answers.py` | sync + stream endpoints |
| P0 | `worker/main.py` | ingestion job entrypoint |
| P0 | `alembic/versions/0001_initial.py` | schema creation, pgvector extension |
| P1 | `app/providers/anthropic_provider.py` | secondary hosted adapter |
| P1 | `app/providers/ollama_provider.py` | local dev adapter |
| P1 | `app/observability.py` | metrics and trace hooks |
| P1 | `tests/load/*.js` | k6 smoke and stream benchmarks |
| P2 | `docs/screenshots/*` | recruiter-facing screenshots |
| P2 | `scripts/export_openapi.py` | spec snapshot export |

### Core code example

#### Async streaming FastAPI endpoint

FastAPI supports streaming responses with an async generator, and its docs call out a subtle but important implementation detail: the generator must yield control back to the event loop so cancellation works properly on long-running streams. citeturn22view0

```python
# app/api/answers.py
from __future__ import annotations

import json
from collections.abc import AsyncIterator
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_current_user, get_answer_service
from app.schemas.answers import AnswerRequest
from app.services.answer_service import AnswerService

router = APIRouter(prefix="/v1/answers", tags=["answers"])


@router.post("")
async def answer(
    request: AnswerRequest,
    current_user=Depends(get_current_user),
    service: AnswerService = Depends(get_answer_service),
):
    return await service.answer(request=request, user=current_user)


@router.post("/stream")
async def answer_stream(
    request: AnswerRequest,
    current_user=Depends(get_current_user),
    service: AnswerService = Depends(get_answer_service),
):
    async def event_source() -> AsyncIterator[bytes]:
        async for event in service.stream_answer(request=request, user=current_user):
            payload = {"type": event.type, "data": event.data}
            yield f"data: {json.dumps(payload)}\n\n".encode("utf-8")
        yield b"data: {\"type\":\"done\"}\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")
```

#### Semantic cache lookup

```python
# app/cache/semantic_cache.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CacheResult:
    hit_type: str  # none | exact | semantic
    payload: dict | None
    similarity: float | None = None


class SemanticCache:
    def __init__(self, redis_client, repo, embedder, threshold: float = 0.93) -> None:
        self.redis = redis_client
        self.repo = repo
        self.embedder = embedder
        self.threshold = threshold

    async def lookup(self, request_ctx) -> CacheResult:
        exact_key = request_ctx.exact_cache_key()
        exact_payload = await self.redis.get(exact_key)
        if exact_payload:
            return CacheResult(hit_type="exact", payload=exact_payload)

        query_embedding = await self.embedder.embed_text(request_ctx.normalized_query)

        row = await self.repo.find_best_semantic_hit(
            namespace=request_ctx.namespace,
            provider=request_ctx.provider,
            model=request_ctx.model,
            system_prompt_hash=request_ctx.system_prompt_hash,
            retrieval_fingerprint=request_ctx.retrieval_fingerprint,
            query_embedding=query_embedding,
        )

        if row and row.similarity >= self.threshold:
            await self.redis.set(
                exact_key,
                row.response_json,
                ex=request_ctx.exact_ttl_seconds,
            )
            return CacheResult(
                hit_type="semantic",
                payload=row.response_json,
                similarity=row.similarity,
            )

        return CacheResult(hit_type="none", payload=None)
```

#### Provider abstraction

```python
# app/providers/base.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from collections.abc import AsyncIterator


@dataclass(slots=True)
class ChatMessage:
    role: str
    content: str


@dataclass(slots=True)
class ChatRequest:
    messages: list[ChatMessage]
    model: str
    temperature: float = 0.0
    max_tokens: int = 512


@dataclass(slots=True)
class ChatResponse:
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None


@dataclass(slots=True)
class StreamEvent:
    type: str
    data: str | dict


class ChatProvider(Protocol):
    name: str

    async def generate(self, request: ChatRequest) -> ChatResponse: ...
    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]: ...
```

#### Ingestion worker

```python
# worker/main.py
from __future__ import annotations

import asyncio

from app.db.session import async_session_factory
from app.services.ingest_service import IngestService
from app.providers.registry import build_embedding_provider


async def main() -> None:
    embedder = build_embedding_provider()

    async with async_session_factory() as session:
        service = IngestService(session=session, embedder=embedder)

        # In Month 1, keep it simple:
        #   - read seeded markdown/text docs
        #   - chunk them
        #   - compute embeddings
        #   - upsert document + chunk rows
        await service.ingest_seeded_documents()


if __name__ == "__main__":
    asyncio.run(main())
```

### Dockerfile

Docker’s own best-practice docs explicitly recommend **multi-stage builds** to reduce final image size and keep only the runtime artifacts you need. citeturn16view13

```dockerfile
# month-1/capstone/qa-api/Dockerfile
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
COPY app ./app
COPY worker ./worker

RUN pip install --upgrade pip && pip install .

FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
```

### docker-compose

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: month1
      POSTGRES_USER: month1
      POSTGRES_PASSWORD: month1
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    env_file:
      - .env.example
    environment:
      APP_ENV: local
      DATABASE_URL: postgresql+asyncpg://month1:month1@postgres:5432/month1
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    ports:
      - "8080:8080"

  worker:
    build: .
    command: ["python", "-m", "worker.main"]
    env_file:
      - .env.example
    environment:
      APP_ENV: local
      DATABASE_URL: postgresql+asyncpg://month1:month1@postgres:5432/month1
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
```

## Delivery pipeline and operations

### Tests to include

Use `pytest`, `pytest-asyncio`, and `httpx.AsyncClient`. `pytest-asyncio` exists specifically to let you test coroutine code; HTTPX documents async streaming and the requirement to close manually streamed responses to avoid leaks. citeturn13search1turn22view1

| Test file | Scope | What it proves |
|---|---|---|
| `tests/unit/test_passwords.py` | unit | hash/verify and no plaintext handling |
| `tests/unit/test_jwt.py` | unit | exp, sub, roles, refresh rotation helpers |
| `tests/unit/test_rbac.py` | unit | role dependency rejects and allows correctly |
| `tests/unit/test_cache_keys.py` | unit | stable exact-cache key generation |
| `tests/unit/test_semantic_cache.py` | unit | exact hit, semantic hit, miss logic |
| `tests/unit/test_provider_registry.py` | unit | provider selection by config |
| `tests/integration/test_auth_flow.py` | integration | register → login → refresh → me |
| `tests/integration/test_answer_endpoint.py` | integration | cache miss path and successful persistence |
| `tests/integration/test_answer_stream.py` | integration | streamed chunks arrive and close cleanly |
| `tests/integration/test_ingest_and_query.py` | integration | ingest seeded docs then answer from them |
| `tests/contract/test_openapi_snapshot.py` | contract | public API did not drift unexpectedly |
| `tests/load/k6-smoke.js` | load | baseline latency and error rate |
| `tests/load/k6-stream.js` | load | time to first token under concurrent streams |

### CI/CD workflow

GitHub’s docs support a standard Python build-and-test workflow. For deployment, use **Workload Identity Federation**, because Google’s own GitHub Action documentation explicitly recommends it over long-lived service account keys. citeturn17view6turn30view0turn30view2

```yaml
# .github/workflows/month1-ci.yml
name: month1-ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: month1
          POSTGRES_USER: month1
          POSTGRES_PASSWORD: month1
        ports: ["5432:5432"]
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install --upgrade pip && pip install -e .[dev]
        working-directory: month-1/capstone/qa-api

      - run: ruff check .
        working-directory: month-1/capstone/qa-api

      - run: mypy app
        working-directory: month-1/capstone/qa-api

      - run: pytest -q
        working-directory: month-1/capstone/qa-api
```

```yaml
# .github/workflows/month1-deploy-cloud-run.yml
name: month1-deploy-cloud-run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WIF_PROVIDER }}
          service_account: ${{ secrets.GCP_DEPLOYER_SA }}

      - uses: google-github-actions/setup-gcloud@v3
        with:
          version: ">= 363.0.0"

      - run: |
          gcloud builds submit month-1/capstone/qa-api \
            --tag "${{ vars.IMAGE_URL }}:${{ github.sha }}"

      - run: |
          gcloud run deploy month1-qa-api \
            --image "${{ vars.IMAGE_URL }}:${{ github.sha }}" \
            --region "${{ vars.GCP_REGION }}" \
            --concurrency 8 \
            --min-instances 1 \
            --timeout 120s \
            --service-account "${{ secrets.GCP_RUNTIME_SA }}" \
            --update-secrets=OPENAI_API_KEY=openai-api-key:latest,ANTHROPIC_API_KEY=anthropic-api-key:latest

      - run: |
          gcloud run jobs replace month-1/capstone/qa-api/infra/cloudrun/ingest.job.yaml \
            --region "${{ vars.GCP_REGION }}"
```

### Infra steps for Cloud Run

1. Enable APIs: Cloud Run Admin, Cloud Build, Artifact Registry, Cloud SQL Admin, Secret Manager, Memorystore, IAM Credentials.
2. Create Artifact Registry repository.
3. Create runtime service account.
4. Create Cloud SQL PostgreSQL in the **same region** as Cloud Run.
5. Create DB and run `CREATE EXTENSION vector;`.
6. Create Memorystore Redis in the same region and connect via **Direct VPC egress**.
7. Grant Cloud Run runtime account `Cloud SQL Client` and `Secret Manager Secret Accessor`.
8. Store API keys in Secret Manager and reference them from Cloud Run, not plaintext env vars.
9. Deploy API service.
10. Deploy ingestion job.
11. Seed demo user and sample documents.
12. Run smoke tests against the deployed URL.

Those steps are aligned with first-party docs: Google recommends same-region Cloud SQL connectivity, recommends Direct VPC egress for Redis connections from Cloud Run, documents secret references from Secret Manager into Cloud Run services, and documents WIF for deployment pipelines. citeturn24view0turn24view1turn33view0turn30view2

### Logging and monitoring plan

Cloud Run automatically sends request logs, container logs, and system logs to Cloud Logging. It also parses single-line JSON logs into `jsonPayload`, which is exactly what you want for recruiter-visible structured observability without building a huge monitoring stack on day one. FastAPI can be instrumented with OpenTelemetry using the official FastAPI instrumentation package. citeturn21view0turn17view5

Recommended logging fields:

- `timestamp`
- `severity`
- `request_id`
- `trace_id`
- `user_id`
- `route`
- `status_code`
- `duration_ms`
- `provider`
- `model`
- `cache_hit_type`
- `semantic_similarity`
- `input_tokens`
- `output_tokens`

Recommended metrics:

- request count by route/status
- p50/p95/p99 latency
- time to first token
- cache hit rate by type
- provider error rate
- Redis lookup latency
- pgvector query latency
- ingestion job duration and chunk throughput

### Security plan

FastAPI provides first-party security helpers, and its JWT tutorial is enough for a serious Month 1 implementation. Use:

- `pwdlib[argon2]` for password hashing
- short-lived JWT access tokens
- hashed refresh-token identifiers stored in Postgres
- RBAC via a `require_roles()` dependency
- Redis-backed rate limiting
- Secret Manager for provider keys
- Dependabot for dependency security updates

GitHub’s documentation makes clear that Dependabot security updates are the native mechanism for automated vulnerable dependency updates; include `.github/dependabot.yml` from day one. citeturn19view0turn22view3turn13search4turn16view14

### Benchmark plan

Use **k6** for API load testing; Grafana’s k6 docs explicitly position it for API performance testing and load-test patterns like smoke, stress, and soak tests. For cost estimation, use provider-returned token usage plus the official pricing pages from OpenAI and Anthropic. citeturn13search0turn26view0turn26view1

Run these benchmark suites:

| Benchmark | Purpose | Target output |
|---|---|---|
| Smoke | verify no regressions | 1–5 VUs, 2 minutes |
| Average load | normal traffic | 10–25 VUs, 10 minutes |
| Stress | see first failure mode | ramp until p95 or errors degrade |
| Streaming | measure TTFT | concurrent SSE streams |
| Cache effectiveness | quantify exact vs semantic benefit | compare miss/exact/semantic latency |
| Ingestion throughput | worker performance | docs/minute, chunks/minute |

Track these evaluation metrics:

| Metric | Why it matters |
|---|---|
| p50/p95/p99 latency | overall responsiveness |
| TTFT | real UX for streamed AI answers |
| cache exact hit rate | savings on repeated identical prompts |
| cache semantic hit rate | savings on near-duplicate prompts |
| semantic false-positive rate | safety of semantic cache threshold |
| provider error rate | network/provider reliability |
| DB query p95 | retrieval and cache-search health |
| estimated cost per 100 answers | recruiter-friendly unit economics |

Cost calculation formulas:

- **Hosted providers**: `(input_tokens × input_price) + (output_tokens × output_price) + tool or cache modifiers`
- **Semantic cache savings**: compare miss path cost against semantic or exact hit path cost
- **Local/self-hosted**: amortize infra cost per benchmark run or per hour

OpenAI publishes token pricing with cached-input rates, and Anthropic publishes both base rates and prompt-caching multipliers, so your benchmark report should include a short assumptions section and show both “with cache” and “without cache” cost estimates. citeturn26view0turn26view6turn26view1

## Sprint schedule and recruiter packaging

### Four-week sprint plan

```mermaid
gantt
    title Month 1 implementation schedule
    dateFormat  YYYY-MM-DD
    section Week 1
    Scaffold repo and config           :a1, 2026-04-20, 2d
    Async DB, Redis, health endpoints  :a2, after a1, 2d
    Auth and RBAC baseline             :a3, after a2, 2d
    section Week 2
    Providers and answer service       :b1, 2026-04-27, 2d
    Streaming endpoint                 :b2, after b1, 1d
    Ingestion worker and chunking      :b3, after b2, 2d
    section Week 3
    Semantic cache and retrieval       :c1, 2026-05-04, 3d
    Integration tests and fixtures     :c2, after c1, 2d
    section Week 4
    CI/CD and Cloud Run deploy         :d1, 2026-05-11, 2d
    Benchmarks and screenshots         :d2, after d1, 2d
    README polish and recruiter pack   :d3, after d2, 2d
```

### Daily milestones

| Week | Day | Milestone |
|---|---|---|
| Week 1 | Mon | create capstone folder, `pyproject.toml`, config, Makefile, lint/type/test setup |
| Week 1 | Tue | async DB engine, migrations, base models, health endpoints |
| Week 1 | Wed | Redis client, exact cache helper, request ID middleware, error envelope |
| Week 1 | Thu | auth schemas, password hashing, register/login routes |
| Week 1 | Fri | refresh token rotation, RBAC dependency, `/users/me` tests |
| Week 2 | Mon | provider protocol, registry, OpenAI provider |
| Week 2 | Tue | synchronous answer endpoint, retrieval service, persistence |
| Week 2 | Wed | streaming answer endpoint, cancellation-safe streaming |
| Week 2 | Thu | chunking utility, documents schema, ingestion service |
| Week 2 | Fri | worker entrypoint and local seeded-doc ingestion |
| Week 3 | Mon | document chunk embeddings persisted in pgvector |
| Week 3 | Tue | semantic cache table + lookup repository |
| Week 3 | Wed | exact Redis + semantic pgvector combined flow |
| Week 3 | Thu | integration tests for miss, exact hit, semantic hit |
| Week 3 | Fri | threshold tuning and cache safety rules |
| Week 4 | Mon | Docker polish, CI workflow, Dependabot |
| Week 4 | Tue | Cloud Run deploy, Cloud SQL hookup, Redis hookup |
| Week 4 | Wed | load tests, TTFT tests, cost spreadsheet/report |
| Week 4 | Thu | README, diagrams, architecture docs, screenshots |
| Week 4 | Fri | final deploy verification, demo script, recruiter packaging |

### Weekly definition of done

| Week | Done means |
|---|---|
| Week 1 | service boots locally, DB/Redis healthy, auth works, tests green |
| Week 2 | API answers and streams, ingestion seeds knowledge docs |
| Week 3 | semantic cache works and integration tests prove hit/miss paths |
| Week 4 | staging deploy live, benchmarks committed, README polished, screenshots present |

### Recruiter-facing packaging

The final reviewer experience should look like this:

| Artifact | File or location | What to show |
|---|---|---|
| Demo URL | Cloud Run staging URL | `/docs`, login, ask a seeded question, show stream |
| Architecture diagram | `docs/architecture.mmd` and README | one-glance system understanding |
| Benchmarks | `docs/benchmarks.md` | p95 latency, TTFT, cache impact, cost estimate |
| Screenshots | `docs/screenshots/` | Swagger, Cloud Run logs, benchmark chart, CI pass |
| Design doc | `docs/deployment-cloud-run.md` | infra choices and security assumptions |
| API contract | generated OpenAPI + snapshot test | stable public interface |
| CI/CD evidence | GitHub Actions run badges/screenshots | job-ready operational discipline |

If this Month 1 implementation is executed along this plan, the repository will stop looking like a study program and start looking like a **small, credible AI backend system**—which is exactly what recruiters, hiring managers, and technical interviewers need to see.
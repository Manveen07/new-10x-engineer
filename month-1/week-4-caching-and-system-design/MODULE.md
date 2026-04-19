# Week 4: Semantic Caching & System Design Fundamentals

## Why This Matters
LLM calls are expensive ($0.01-0.10+ per query) and slow (1-5 seconds). Semantic caching can cut costs by 30-60% and latency by 10x for repeated similar queries. System design thinking ties together everything from Month 1 and prepares you for the architecture decisions in Months 2-4.

---

## Day-by-Day Plan

### Monday — Redis Vector Similarity Search (1.5h)

**Read (30 min):**
- Redis blog: What is Semantic Caching?
  https://redis.io/blog/what-is-semantic-caching/

**Read (30 min):**
- RedisVL SemanticCache documentation
  https://redis.io/docs/latest/develop/ai/redisvl/user_guide/llmcache/

**Read (30 min):**
- Redis Stack quickstart (Docker setup)
  https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/docker/

**Key concepts:**
- Traditional cache: exact key match (`"what is python"` != `"what's python"`)
- Semantic cache: vector similarity match (`"what is python"` ≈ `"what's python"`)
- Redis Stack includes RediSearch which supports vector similarity (HNSW index)
- Workflow: query → embed → search cache → if hit (similarity > threshold) return cached → else call LLM → cache result
- Similarity threshold is the critical tuning parameter: too low = stale results, too high = low hit rate

**Setup:**
```bash
# Start Redis Stack with Docker
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

# Install Python client
pip install redisvl redis openai
```

**Exercise:** See `exercises/day16_redis_vectors.py`

Set up Redis Stack and:
1. Store 100 text embeddings with metadata
2. Perform vector similarity search (KNN query)
3. Compare results at different distance thresholds
4. Measure search latency vs brute-force comparison

---

### Tuesday — Build a Semantic Cache (1.5h)

**Read (1h):**
- Redis LangCache tutorial (follow along with code)
  https://redis.io/tutorials/semantic-caching-with-redis-langcache/

**Read (30 min):**
- RedisVL SemanticCache API reference
  https://redis.io/docs/latest/develop/ai/redisvl/api/cache/

**Exercise:** See `exercises/day17_semantic_cache.py`

Build a semantic cache from scratch (not just using RedisVL's built-in):
1. `SemanticCache` class with `get()` and `set()` methods
2. On `get(query)`: embed query → search Redis for similar → return if above threshold
3. On `set(query, response)`: embed query → store in Redis with response as metadata
4. Add TTL support (cached entries expire after N hours)
5. Add namespace support (separate caches for different use cases)
6. Test with 20 query variations and measure hit rate

Target: cache hit rate >60% on semantically similar query variations.

---

### Wednesday — Tune and Evaluate the Cache (1.5h)

**Read (1h):**
- Medium: Semantic Caching of AI Agents Using Redis
  https://shilpathota.medium.com/semantic-caching-of-ai-agents-using-redis-database-b114edfa5e68

**Read (30 min):**
- RedisVL distance metrics documentation
  https://redis.io/docs/latest/develop/ai/redisvl/user_guide/

**Exercise:** See `exercises/day18_cache_tuning.py`

Tune your semantic cache:
1. Test similarity thresholds: 0.80, 0.85, 0.90, 0.95
   - For each: measure hit rate, false positive rate, false negative rate
2. Test different embedding models: text-embedding-3-small vs text-embedding-3-large
   - Measure quality difference vs cost difference
3. Add tag-based filtering (cache per user, per topic, per session)
4. Implement cache invalidation strategies:
   - TTL-based (time expires)
   - Event-based (source data changed → invalidate related entries)
   - Manual (admin clears specific entries)
5. Build a dashboard: hit rate, avg latency saved, cost saved

**Key tuning insights:**
- 0.85-0.90 is the sweet spot for most use cases
- Below 0.85: too many false positives (returning wrong cached answers)
- Above 0.95: too many misses (barely better than exact match)
- Embedding model quality matters more than threshold tuning

---

### Thursday — System Design for AI Applications (1.5h)

**Read (1h):**
- System Design Handbook: AI system design guide
  https://www.systemdesignhandbook.com/guides/ai-system-design/

**Read (30 min):**
- donnemartin/system-design-primer — Start here section
  https://github.com/donnemartin/system-design-primer#system-design-topics-start-here

**Key architecture patterns for AI systems:**

```
┌────────────────────────────────────────────────────────┐
│                    API Gateway / LB                      │
├────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │
│  │ Auth     │  │ Rate     │  │ Request Router       │ │
│  │ Service  │  │ Limiter  │  │ (simple vs complex)  │ │
│  └──────────┘  └──────────┘  └──────────────────────┘ │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌───────────────┐  ┌────────────┐  │
│  │ Semantic     │  │ RAG Pipeline  │  │ Agent      │  │
│  │ Cache (Redis)│  │ (retrieval)   │  │ Orchestrator│ │
│  └──────────────┘  └───────────────┘  └────────────┘  │
├────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │PostgreSQL│  │ Vector   │  │ LLM      │  │ Object│ │
│  │ (meta)   │  │ Store    │  │ Provider │  │ Store │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────┘ │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Observability│  │ Eval Pipeline│  │ Async Queue │  │
│  │ (traces)     │  │ (quality)    │  │ (ingestion) │  │
│  └──────────────┘  └──────────────┘  └─────────────┘  │
└────────────────────────────────────────────────────────┘
```

**No exercise today — study and diagram.** Draw the system architecture for:
1. A customer support chatbot serving 1000 users/day
2. A document Q&A system for a 50GB corpus
3. A multi-agent workflow that processes insurance claims

For each, identify: bottlenecks, scaling strategy, failure modes, and cost drivers.

---

### Friday — System Design Case Studies (1.5h)

**Read (30 min):**
- Evidently AI ML system design case studies
  https://www.evidentlyai.com/ml-system-design

**Read (30 min):**
- GitHub: themanojdesai/genai-llm-ml-case-studies
  https://github.com/themanojdesai/genai-llm-ml-case-studies
  Pick 2-3 that interest you and read them

**Read (30 min):**
- ombharatiya/ai-system-design-guide
  https://github.com/ombharatiya/ai-system-design-guide

**Study these real-world architectures:**
1. How does ChatGPT handle millions of concurrent users?
2. How does Notion AI serve document Q&A at scale?
3. How do companies like Stripe use AI for fraud detection?

**For each, note:**
- What's the data flow?
- Where does caching sit?
- How do they handle latency?
- What's the evaluation strategy?
- What would break first at 10x scale?

---

### Weekend — Month 1 Capstone Project (2-3h)

See `capstone/` directory for the full spec.

**Build: AI-Powered Q&A API**

This capstone combines everything from Month 1:

```
Client → FastAPI (auth, validation, rate limiting)
         ├─→ Semantic Cache (Redis) → return if hit
         ├─→ PostgreSQL (query metadata, user history)
         ├─→ LLM Provider Adapter → generate answer
         └─→ Store result in cache
```

**Requirements:**
1. **FastAPI backend** with proper project structure (Week 2)
2. **JWT auth** with RBAC — admin can see all queries, users see their own (Week 2)
3. **Async PostgreSQL** for user accounts, query history, and metadata (Week 2)
4. **Redis semantic caching** with measured hit rates (Week 4)
5. **LLM provider adapter** — swap providers via env var (Week 3)
6. **Structured error handling** — consistent JSON error responses (Week 2)
7. **Request logging + timing middleware** (Week 2)
8. **Rate limiting** — 10 queries/min for free tier, 100 for paid (Week 2)
9. **Health check** + cache stats endpoint (Week 4)
10. **Docker Compose** setup (FastAPI + PostgreSQL + Redis)

**Endpoints:**
- `POST /auth/register` — create account
- `POST /auth/login` — get tokens
- `POST /qa/ask` — ask a question (main endpoint)
- `GET /qa/history` — user's query history
- `GET /admin/stats` — cache hit rate, avg latency, top queries
- `GET /health` — service health + dependency checks

**Evaluation criteria:**
- Cache hit rate >60% on repeated similar queries
- API handles 50 concurrent requests without errors
- Swapping LLM providers requires only env var change
- Auth flow works end-to-end
- Tests pass with >70% coverage

**Deliverable:**
Write a brief Architecture Decision Record (ADR) explaining:
- Why you chose each technology
- What trade-offs you made
- What you'd change with more time

---

## Skill Checkpoint

1. Draw the system architecture for a production Q&A service handling 1000 req/s. Where does caching sit?
2. What's your caching strategy for queries with different parameters (e.g., different users, different contexts)?
3. How do you invalidate the semantic cache when source data changes?
4. Design a system that gracefully degrades when Redis is down (cache miss, not total failure)
5. Explain the cost analysis: how much does semantic caching save vs the cost of running Redis?

---

## Core Resources

| Resource | Type | URL |
|----------|------|-----|
| Redis semantic caching docs | Reference | https://redis.io/docs/latest/develop/ai/redisvl/user_guide/llmcache/ |
| System Design Primer | Reference | https://github.com/donnemartin/system-design-primer |
| AI System Design Guide | Patterns | https://github.com/ombharatiya/ai-system-design-guide |
| Evidently AI case studies | Case studies | https://www.evidentlyai.com/ml-system-design |

## Supplementary Resources

- Book: *Designing Data-Intensive Applications* by Martin Kleppmann — the bible of system design
- Book: *Designing Machine Learning Systems* by Chip Huyen — ML-specific system design
- Redis University (free courses) — https://university.redis.io
- System Design Interview channel (YouTube) — practical walkthroughs
- InfoQ architecture articles — https://www.infoq.com/architecture-design/

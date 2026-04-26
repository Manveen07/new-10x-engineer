# Week 4: Semantic Caching, System Design, And Capstone Integration

## Outcome

By the end of Week 4 the Month 1 capstone should be a runnable Q&A API. It should validate a question, authenticate the user, check exact and semantic cache paths, call a provider on cache miss, persist query history and provider-call data, log cost/latency/cache outcome, and return a structured answer.

## What This Week Teaches

- Redis Stack basics and vector search.
- Exact cache vs semantic cache.
- Similarity threshold tuning.
- Cache invalidation and TTLs.
- Latency and cost measurement.
- Health/readiness checks across dependencies.
- AI system design tradeoffs.
- Capstone documentation, tests, ADRs, and demo flow.

## Day 16: Redis Vector Search

Exercise: `../exercises/day16_redis_vectors.py`

Build:

- Redis Stack running locally through Docker.
- A small vector index.
- Insert query embeddings with metadata.
- Search similar vectors.
- Compare vector search latency against brute force for a small dataset.

Capstone connection:

- This becomes the semantic lookup path before calling the LLM provider.

Done when:

- You can insert and retrieve vector-like records.
- You can explain the distance metric and threshold.
- You can show search results with score and metadata.

## Day 17: Semantic Cache

Exercise: `../exercises/day17_semantic_cache.py`

Build:

- `SemanticCache.get(query)`.
- `SemanticCache.set(query, response, metadata)`.
- TTL support.
- Namespace support.
- Cache stats: hits, misses, hit rate, avg lookup latency.

Cache result model should include:

- `hit`
- `hit_type`
- `response`
- `matched_query`
- `similarity`
- `latency_ms`

Capstone connection:

- `/qa/ask` should return from cache before provider call where safe.

Done when:

- Repeated exact questions hit exact cache.
- Similar questions can hit semantic cache above threshold.
- Misses fall through to the provider.

## Day 18: Cache Tuning And Evaluation

Exercise: `../exercises/day18_cache_tuning.py`

Build:

- A small evaluation set of question variants.
- Threshold sweep for 0.80, 0.85, 0.90, and 0.95.
- False-positive and false-negative notes.
- Latency saved estimate.
- Cost saved estimate.

Recommended report:

```text
threshold | hit_rate | false_positive_rate | false_negative_rate | avg_latency_saved_ms | estimated_cost_saved_usd
```

Capstone connection:

- The README should not claim "semantic cache works" without a tiny measurement.

Done when:

- You choose a default threshold and explain why.
- You document when semantic caching is unsafe.

## Day 19: AI System Design

Exercise: `../exercises/day19_ai_system_design.md`

Build:

- Architecture diagram for the Q&A API.
- Failure-mode table.
- Cost-driver table.
- Scaling notes for 10x traffic.
- Degraded-mode behavior when Redis, DB, or provider is down.

Required scenarios:

- Redis down.
- PostgreSQL down.
- Provider timeout.
- Provider returns malformed output.
- User exceeds rate limit.

Capstone connection:

- These notes become the README "Architecture and tradeoffs" section and ADRs.

## Day 20: Final Capstone Integration

Exercise: `../capstone/CAPSTONE.md`

Build:

- `/qa/ask` route.
- `/qa/history` route.
- Admin cache/stats route.
- Exact cache and semantic cache.
- Provider call on cache miss.
- Query history write.
- Provider-call write.
- Tests for cache hit, cache miss, provider error, auth failure, and rate limit.
- Docker Compose.
- README, architecture diagram, ADRs, and demo script.

Done when:

- `uv run pytest` passes.
- The mock provider path works without API keys.
- Docker Compose starts all dependencies.
- The README can guide someone through the demo in under five minutes.

## Weekend 4: Portfolio Polish

Polish the capstone as a public proof-of-work artifact:

- Add screenshots of `/docs`, health endpoint, example answer, logs, and tests.
- Add `docs/demo-script.md`.
- Add `docs/architecture.md`.
- Add ADRs under `docs/decisions/`.
- Add benchmark notes under `docs/benchmarks/`.
- Add a "Not doing in Month 1" section so the scope is clear.

## Week 4 Acceptance Gate

- [ ] `/qa/ask` authenticates user and validates input.
- [ ] Exact cache works.
- [ ] Semantic cache works.
- [ ] Cache miss calls provider adapter.
- [ ] Query history is persisted.
- [ ] Provider-call metadata is persisted.
- [ ] Logs include request ID, cache outcome, latency, provider, model, token counts, and estimated cost.
- [ ] Readiness checks verify DB and Redis.
- [ ] Tests run without live API keys.
- [ ] README, ADRs, and benchmark notes exist.

## Core Resources

| Resource | Use |
|---|---|
| https://redis.io/docs/latest/develop/ai/ | Redis AI/vector docs |
| https://redis.io/docs/latest/develop/ai/redisvl/user_guide/llmcache/ | semantic cache concepts |
| https://www.python-httpx.org/advanced/timeouts/ | provider timeout design |
| https://fastapi.tiangolo.com/deployment/docker/ | Docker deployment |
| https://mermaid.js.org/syntax/flowchart.html | architecture diagrams |

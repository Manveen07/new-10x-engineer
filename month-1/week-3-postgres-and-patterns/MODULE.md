# Week 3: PostgreSQL And AI Design Patterns

## Outcome

By the end of Week 3 the capstone should have real persistence and a clean provider boundary. You should be able to inspect query performance, design indexes, tune slow queries, swap LLM providers without route changes, and log provider cost/latency data.

## What This Week Teaches

- PostgreSQL query plans with `EXPLAIN (ANALYZE, BUFFERS)`.
- B-tree, GIN, partial, composite, and covering indexes.
- Query rewrites for common performance mistakes.
- Repository/service separation.
- Provider adapter pattern for LLMs.
- Strategy/factory patterns for model, embedding, and retrieval choices.
- Bounded retries, timeouts, and provider fallback.
- Cost and latency tracking for every LLM call.

## Day 11: EXPLAIN ANALYZE

Exercise: `../exercises/day11_explain_analyze.py`

Build:

- A local table with enough rows to make plans visible.
- Queries that demonstrate sequential scan, index scan, join, sort, and aggregation.
- Notes for each query plan.

Required evidence:

- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` before optimization.
- A short explanation of the bottleneck.
- A proposed index or rewrite.
- `EXPLAIN` after the change.

Capstone connection:

- Query history, user lookup, token lookup, and admin stats need predictable DB behavior.

## Day 12: Indexing Strategies

Exercise: `../exercises/day12_indexing.py`

Build:

- B-tree index for common lookups.
- Composite index where column order matters.
- Partial index for active rows.
- GIN index for JSONB or text-search-like data.
- Index size comparison.

Capstone indexes to design:

- `users.email`
- `refresh_tokens.token_hash`
- `queries.user_id, created_at`
- `provider_calls.query_id`
- `cache_entries.cache_key`
- `cache_entries.created_at`

Done when:

- You can explain each index in terms of a real query.
- You can show at least one example where an index is not worth adding.

## Day 13: Query Tuning Patterns

Exercise: `../exercises/day13_query_tuning.py`

Build:

- Rewrite a query that uses a function on an indexed column.
- Rewrite an `OR` query where separate indexes are not used well.
- Rewrite a correlated subquery as a join.
- Add pagination that does not accidentally load all rows.

Capstone connection:

- `/qa/history` and admin analytics should stay fast as query history grows.

Done when:

- Each optimization includes before/after plan evidence.
- You explain the tradeoff, not just the speedup.

## Day 14: LLM Provider Adapter

Exercise: `../exercises/day14_adapter_pattern.py`

Build in the capstone:

- `ChatProvider` or `LLMProvider` protocol/base class.
- `MockProvider` that needs no API key and is deterministic.
- `OpenAIProvider`.
- `AnthropicProvider`.
- Optional local provider such as Ollama.
- Provider factory from typed settings.

Provider response model should include:

- `text`
- `provider`
- `model`
- `input_tokens`
- `output_tokens`
- `latency_ms`
- `estimated_cost_usd`
- `finish_reason`

Done when:

- Routes call only the provider interface.
- Tests use the mock provider.
- Switching provider is an environment/config change, not an app rewrite.

## Day 15: Strategy And Factory Patterns

Exercise: `../exercises/day15_strategy_factory.py`

Build:

- Strategy for exact cache vs semantic cache.
- Strategy for hosted embedding vs mock embedding.
- Factory for provider selection.
- Factory for cache backend selection.
- Bounded retry wrapper for provider calls.

Capstone connection:

- Month 2 will add retrieval strategies. Month 1 should teach the pattern without building full RAG.

Done when:

- The capstone can run in `mock` mode with no external API key.
- Provider errors are retried only where retry is safe.
- Retry count and final status are logged.

## Weekend 3: Provider Integration And Observability

Exercise: `../exercises/weekend3_provider_observability.md`

Fold Days 11-15 into the capstone:

- Add provider call table.
- Add query history table.
- Add provider factory.
- Add mock provider tests.
- Add timeout and retry boundaries.
- Add structured logs for provider calls.
- Add an ADR for provider abstraction.

Required provider log fields:

- `request_id`
- `provider`
- `model`
- `latency_ms`
- `input_tokens`
- `output_tokens`
- `estimated_cost_usd`
- `retry_count`
- `status`
- `error_type`

## Week 3 Acceptance Gate

- [ ] Query-history schema exists.
- [ ] Provider-call schema exists.
- [ ] Provider adapter interface exists.
- [ ] Mock provider is deterministic.
- [ ] Provider choice comes from settings.
- [ ] Provider calls have timeouts.
- [ ] Safe failures are retried with a bound.
- [ ] Provider metrics are logged and persisted.
- [ ] DB indexes are justified by actual queries.

## Core Resources

| Resource | Use |
|---|---|
| https://www.postgresql.org/docs/current/using-explain.html | reading query plans |
| https://www.postgresql.org/docs/current/indexes.html | indexes |
| https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html | async database sessions |
| https://www.python-httpx.org/advanced/timeouts/ | HTTP timeouts |
| https://docs.python.org/3/library/typing.html#typing.Protocol | provider contracts |

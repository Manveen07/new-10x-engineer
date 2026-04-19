# Week 3: PostgreSQL Optimization & AI Design Patterns

## Why This Matters
Every AI system stores metadata, user queries, conversation history, and evaluation results in a relational database. Vector databases get the hype, but PostgreSQL is the backbone. This week also introduces design patterns that make your AI code maintainable and swappable — critical when LLM providers change pricing or capabilities monthly.

---

## Day-by-Day Plan

### Monday — EXPLAIN ANALYZE Deep Dive (1.5h)

**Read (45 min):**
- PostgreSQL official EXPLAIN documentation
  https://www.postgresql.org/docs/current/sql-explain.html
- Use of EXPLAIN (helpful visual tutorial)
  https://www.postgresql.org/docs/current/using-explain.html

**Read (45 min):**
- Dalibo EXPLAIN visualizer (bookmark this tool — you'll use it constantly)
  https://explain.dalibo.com
- PgMustard blog — how to read EXPLAIN ANALYZE
  https://www.pgmustard.com/docs/explain

**Key concepts:**
- `EXPLAIN` shows the plan, `EXPLAIN ANALYZE` executes and shows actual times
- Always use `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` for full detail
- Key fields: `actual time`, `rows`, `loops`, `Buffers: shared hit/read`
- Seq Scan = reading every row. Index Scan = using an index. Bitmap Index Scan = hybrid
- "Actual rows" vs "Plan rows" mismatch = bad statistics → run `ANALYZE`

**Exercise:** See `exercises/day11_explain_analyze.py`

Set up a test table with 1M+ rows. Run EXPLAIN ANALYZE on:
1. Full table scan (WHERE on unindexed column)
2. Index scan (WHERE on indexed column)
3. Join between two large tables
4. Aggregation with GROUP BY
5. Subquery vs JOIN comparison

Paste each plan into https://explain.dalibo.com and annotate the bottlenecks.

---

### Tuesday — Indexing Strategies (1.5h)

**Read (1h):**
- Percona practical guide to PostgreSQL indexes
  https://www.percona.com/blog/a-practical-guide-to-postgresql-indexes/

**Read (30 min):**
- PostgreSQL index types documentation
  https://www.postgresql.org/docs/current/indexes-types.html

**Key concepts:**
- **B-tree** (default): equality and range queries. Use for: `WHERE id = 5`, `WHERE date > '2025-01-01'`
- **GIN** (Generalized Inverted Index): full-text search, JSONB, arrays. Use for: `WHERE tags @> '{"python"}'`
- **GiST**: geometric data, range types, full-text. Use for: spatial queries
- **Partial indexes**: `CREATE INDEX ... WHERE status = 'active'` — smaller, faster, focused
- **Composite indexes**: column order matters! Put high-cardinality columns first
- **Covering indexes** (INCLUDE): avoid table lookups for frequently accessed columns

**Exercise:** See `exercises/day12_indexing.py`

On your 1M-row test table:
1. Create a B-tree index, benchmark with EXPLAIN ANALYZE
2. Create a GIN index on a JSONB column
3. Create a partial index on active records only
4. Create a composite index and show the column-order effect
5. Compare index sizes with `pg_relation_size()`

---

### Wednesday — Query Tuning Patterns (1.5h)

**Read (1h):**
- PostgreSQL wiki on performance optimization
  https://wiki.postgresql.org/wiki/Performance_Optimization
- PostgreSQL anti-patterns
  https://wiki.postgresql.org/wiki/Don%27t_Do_This

**Read (30 min):**
- Common Table Expressions (CTEs) performance considerations
  https://www.postgresql.org/docs/current/queries-with.html

**Key red flags and fixes:**
- `Seq Scan` on large table → add an index or fix the WHERE clause
- `Sort` with `external merge Disk` → add an index matching ORDER BY, or increase `work_mem`
- `Hash Join` with `Batches > 1` → increase `work_mem`
- `Nested Loop` on large tables → usually fine for small outer tables, bad for large
- `Filter: (removed X rows)` → index isn't selective enough, check partial index
- CTEs in PostgreSQL 12+ can be inlined — but `MATERIALIZED` forces isolation

**Exercise:** See `exercises/day13_query_tuning.py`

Take 3 intentionally slow queries and optimize them:
1. SELECT with function in WHERE (prevents index use) → rewrite
2. OR conditions across different columns → UNION approach
3. Correlated subquery → JOIN rewrite
Document before/after EXPLAIN ANALYZE for each.

---

### Thursday — Adapter Pattern and Provider Abstraction (1.5h)

**Read (1h):**
- Unite.AI design patterns for AI guide
  https://www.unite.ai/design-patterns-in-python-for-ai-and-llm-engineers-a-practical-guide/
- GitHub: arunpshankar/Python-Design-Patterns-for-AI
  https://github.com/arunpshankar/Python-Design-Patterns-for-AI

**Read (30 min):**
- Python abc module docs
  https://docs.python.org/3/library/abc.html

**The Adapter Pattern for LLMs:**
```
            ┌─────────────┐
            │  LLMAdapter  │  (abstract interface)
            │  .complete() │
            │  .embed()    │
            └──────┬───────┘
         ┌─────────┼─────────┐
         │         │         │
   ┌─────┴───┐ ┌──┴────┐ ┌──┴──────┐
   │ OpenAI  │ │Claude │ │ Local   │
   │ Adapter │ │Adapter│ │ Adapter │
   └─────────┘ └───────┘ └─────────┘
```

**Why this matters for AI:**
- LLM providers change pricing, rate limits, and capabilities constantly
- You need to swap providers without changing application code
- Testing: swap in a mock adapter for deterministic tests
- Fallback: if OpenAI is down, fall back to Claude automatically

**Exercise:** See `exercises/day14_adapter_pattern.py`

Build an LLM provider adapter with:
- Abstract base class: `LLMProvider` with `complete()`, `embed()`, `count_tokens()`
- OpenAI adapter
- Anthropic adapter (Claude)
- Mock adapter (for testing — returns deterministic responses)
- Factory function that creates the right adapter from config/env var
- Automatic fallback: if primary fails, try secondary

---

### Friday — Strategy Pattern and Factory Pattern for AI (1.5h)

**Read (30 min):**
- Medium: 3 essential design patterns for AI projects
  https://medium.com/@ethanbrooks42/level-up-your-python-with-3-essential-design-patterns-for-ai-and-llm-projects-525597fad295

**Read (1h):**
- AI Agents Kit code patterns
  https://aiagentskit.com/blog/ai-agent-code-patterns/
- Refactoring Guru: Strategy Pattern
  https://refactoring.guru/design-patterns/strategy/python/example

**Strategy Pattern for AI:**
```
# Different embedding strategies for different use cases
class EmbeddingStrategy(ABC):
    async def embed(self, text: str) -> list[float]: ...

class OpenAIEmbedding(EmbeddingStrategy):     # High quality, costs money
class CohereEmbedding(EmbeddingStrategy):      # Good multilingual
class LocalEmbedding(EmbeddingStrategy):       # Free, runs locally

# Different retrieval strategies
class RetrievalStrategy(ABC):
    async def retrieve(self, query: str, k: int) -> list[Document]: ...

class VectorRetrieval(RetrievalStrategy):      # Semantic similarity
class BM25Retrieval(RetrievalStrategy):        # Keyword matching
class HybridRetrieval(RetrievalStrategy):      # Both combined
```

**Factory Pattern:**
- Creates the right strategy based on configuration
- Centralizes creation logic
- Makes it easy to add new strategies without changing client code

**Exercise:** See `exercises/day15_strategy_factory.py`

Build:
1. Embedding strategy (OpenAI, Cohere placeholder, local/mock)
2. Retrieval strategy (vector, BM25, hybrid)
3. Factory that creates retrieval pipelines from a config dict
4. Pipeline that combines embedding + retrieval + generation strategies
5. Swap strategies via environment variable or config file

---

### Weekend — Integration (1-2h)

**Combine Weeks 2 and 3:**

Add to your Week 2 FastAPI project:
1. Optimized PostgreSQL queries (demonstrate index usage with EXPLAIN ANALYZE)
2. LLM provider adapter (swap providers via env var)
3. Embedding strategy (at least mock + one real provider)
4. A `/search` endpoint that uses the adapter and retrieval strategy
5. A `/admin/query-stats` endpoint that shows EXPLAIN ANALYZE output for debugging

**Done when:**
- EXPLAIN ANALYZE proves your indexes are being used
- Swapping `LLM_PROVIDER=openai` to `LLM_PROVIDER=mock` requires zero code changes
- Tests pass with the mock adapter
- The search endpoint returns relevant results

---

## Skill Checkpoint

1. Given a slow query, walk through the EXPLAIN ANALYZE output step by step and identify the bottleneck
2. When should you use a GIN index vs B-tree? Give a real example of each
3. Diagram the Adapter pattern for an LLM provider abstraction — show the interface, concrete implementations, and the factory
4. What's the difference between the Adapter and Strategy patterns? When do you use each?
5. You're building an AI app that might switch from OpenAI to Claude next month. Design the abstraction layer

---

## Core Resources

| Resource | Type | URL |
|----------|------|-----|
| PostgreSQL EXPLAIN docs | Reference | https://www.postgresql.org/docs/current/sql-explain.html |
| Dalibo EXPLAIN visualizer | Tool | https://explain.dalibo.com |
| Percona index guide | Tutorial | https://www.percona.com/blog/a-practical-guide-to-postgresql-indexes/ |
| Python Design Patterns for AI (repo) | Patterns | https://github.com/arunpshankar/Python-Design-Patterns-for-AI |
| Refactoring Guru (all patterns) | Reference | https://refactoring.guru/design-patterns |

## Supplementary Resources

- Book: *Designing Data-Intensive Applications* by Martin Kleppmann — Chapter 3 (Storage and Retrieval)
- pgMustard (paid but excellent EXPLAIN analysis tool) — https://www.pgmustard.com
- PostgreSQL Index Advisor — https://github.com/supabase/index_advisor
- The twelve-factor app methodology — https://12factor.net (context for config management)

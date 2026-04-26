# Day 25: pgvector Exact Search

## Goal

Implement exact vector search before adding ANN indexes.

## Build

- `chunks.embedding vector(...)`
- cosine-distance query ordered by nearest chunk.
- tenant filter in the same query.
- top-k parameter.
- test with deterministic vectors.

## Example Shape

```sql
SELECT id, document_id, text, embedding <=> :query_embedding AS distance
FROM chunks
WHERE tenant_id = :tenant_id
ORDER BY embedding <=> :query_embedding
LIMIT :top_k;
```

## Done When

- Exact search returns the expected chunk ordering on seeded vectors.
- You document why HNSW is deferred until after baseline metrics.

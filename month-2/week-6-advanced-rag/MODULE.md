# Week 6: Hybrid Retrieval, Reranking, And Grounded Answers

## Outcome

By the end of Week 6, the RAG API should retrieve with dense vector search, PostgreSQL full-text search, RRF fusion, and a reranker interface. It should return grounded answers with citations and preserve enough trace data to debug bad answers.

## Why This Matters

Dense retrieval misses exact keywords. Lexical retrieval misses paraphrases. Hybrid search is now standard enough that Pinecone and Weaviate both document it as the combination of semantic and keyword search. Reranking is the next quality lever after retrieval.

## Day 26: PostgreSQL Full-Text Search

Exercise: `../exercises/day26_postgres_fts.md`

Build:

- `fts tsvector` column for chunks.
- GIN index.
- query with `websearch_to_tsquery` or `plainto_tsquery`.
- ranking with `ts_rank_cd`.

Done when:

- lexical search can find exact product names, acronyms, and section titles that dense search may miss.

## Day 27: Reciprocal Rank Fusion

Exercise: `../exercises/day27_rrf_fusion.py`

Build:

- Dense result model.
- Lexical result model.
- RRF merge function.
- Deduplication by chunk ID.
- score trace explaining each final rank.

Done when:

- You can explain why a chunk ranked high after fusion.

## Day 28: Reranking

Exercise: `../exercises/day28_reranking.py`

Build:

- `Reranker` interface.
- Mock reranker for tests.
- Optional local cross-encoder.
- Optional Cohere reranker.
- benchmark pre-rerank vs post-rerank.

Done when:

- Reranking is a configurable stage and never hardcoded into retrieval.

## Day 29: Query API

Exercise: `../exercises/day29_query_api.md`

Build:

- `POST /v1/search`
- `POST /v1/answer`
- `RetrievalConfig` with top_k, alpha, rerank_top_k, filters, chunking profile, model names.
- Config hash stored in logs and retrieval runs.

Done when:

- `/search` returns chunk IDs, scores, source metadata, and trace info.

## Day 30: Citations And Grounded Answers

Exercise: `../exercises/day30_citations_grounding.md`

Build:

- context assembly from retrieved chunks.
- citation IDs in the prompt.
- answer response with citation list.
- "I don't know" behavior when context is insufficient.

Done when:

- `/answer` never returns an unsupported answer without showing citations.

## Weekend 6: Hybrid Retrieval Benchmark

Exercise: `../exercises/weekend6_hybrid_benchmark.md`

Build a report comparing:

- dense only
- lexical only
- dense + lexical + RRF
- RRF + reranker

Metrics:

- Precision@5
- Recall@10
- MRR@10
- NDCG@10
- p95 retrieval latency

## Week 6 Acceptance Gate

- [ ] Dense search works.
- [ ] PostgreSQL FTS works.
- [ ] RRF fusion works.
- [ ] Reranker interface works.
- [ ] `/search` returns traceable scores.
- [ ] `/answer` returns grounded citations.
- [ ] Hybrid or reranked retrieval improves at least one metric.

## Core Resources

| Resource | Use |
|---|---|
| https://www.postgresql.org/docs/current/textsearch-controls.html | FTS query/ranking controls |
| https://docs.pinecone.io/guides/search/hybrid-search | hybrid retrieval design |
| https://docs.weaviate.io/weaviate/concepts/search/hybrid-search | hybrid retrieval fusion |
| https://docs.cohere.com/docs/rerank | reranking concept |

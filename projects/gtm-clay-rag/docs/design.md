# Project 2 Design - GTM/Clay RAG

Status: draft.

## Objective

Build a RAG system for GTM/Clay operator knowledge that answers questions with citations and measures retrieval quality separately from answer quality.

## Corpus

Planned sources:

- Clay docs.
- Clay University style content.
- Consented and attributed community notes/posts.
- Personal GTM workflow notes where safe to publish.

Every document should store source, attribution, timestamp when available, and content hash.

## Chunking

Plan:

- Normalize Markdown/HTML into plain structured text.
- Keep source metadata on every chunk.
- Track chunk ID, document ID, order, token count, content hash, and chunking config hash.
- Add 50-100 token contextual summaries before embedding and lexical indexing when using manual contextual retrieval.

## Retrieval Stack

- Dense retrieval over embeddings in Postgres + pgvector.
- Lexical retrieval using BM25 or PostgreSQL full-text search.
- Reciprocal Rank Fusion for hybrid ranking.
- Reranker behind an interface.
- FastAPI endpoint or callable service for search and answer.

## Eval Plan

Retrieval evals:

- Generate about 150 query-chunk pairs.
- Measure recall@10/20, MRR, and NDCG@10.
- Compare pure dense, pure lexical, hybrid RRF, and hybrid plus rerank.

Generation evals:

- Faithfulness.
- Answer relevance.
- Context precision.
- Calibration against about 30 hand-labeled examples.

## Ablation Table

README must include:

| Variant | recall@10 | MRR | NDCG@10 | Notes |
|---|---:|---:|---:|---|
| Dense | TBD | TBD | TBD | |
| Lexical | TBD | TBD | TBD | |
| Hybrid RRF | TBD | TBD | TBD | |
| Hybrid + rerank | TBD | TBD | TBD | |

## Observability

Trace these steps:

- Ingestion.
- Chunking/contextualization.
- Embedding.
- Dense retrieval.
- Lexical retrieval.
- Fusion.
- Reranking.
- Generation.
- Eval run.

## Deployment

Target: Modal FastAPI service.

README must include live URL, run instructions, eval commands, ablation results, cost/query, latency p50/p95, and failure modes.

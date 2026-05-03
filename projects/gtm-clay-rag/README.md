# GTM/Clay RAG

Timeline: Months 3-4.

## Problem

Ingest Clay/GTM knowledge and answer operator questions with grounded citations while measuring retrieval quality separately from generation quality.

## Build Standard

- FastAPI.
- Postgres + pgvector.
- Dense retrieval plus BM25 or PostgreSQL full-text search.
- RRF hybrid fusion.
- Contextual retrieval preprocessing.
- Reranker behind an interface.
- Langfuse traces.
- Modal deployment.

## Eval Standard

- About 150 synthetic query-chunk eval pairs.
- recall@10/20, MRR, and NDCG.
- Ablation table: dense vs lexical vs hybrid vs hybrid plus rerank.
- Faithfulness, answer relevance, and context precision evals.
- Generation judges calibrated against about 30 hand-labeled examples.
- Cost-per-query and latency p50/p95.

## README Sections To Fill

- Corpus and attribution.
- Architecture.
- Retrieval pipeline.
- Eval methodology.
- Ablation results.
- Cost and latency.
- Where it fails.
- Deployment.

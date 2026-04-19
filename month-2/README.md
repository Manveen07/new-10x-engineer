# Month 2 Capstone: Retrieval Engineering Platform

A production-caliber retrieval engineering platform focused on measuring retrieval quality, benchmarking architectural tradeoffs, and building a resilient ingestion-to-query pipeline.

## Architectural Baseline
*   **Vector Store**: `pgvector`-first (Exact search baseline, HNSW for ANN experiments).
*   **Lexical Baseline**: PostgreSQL Full-Text Search (FTS) using `tsvector` and `ts_rank_cd`. 
*   **Fusion**: Reciprocal Rank Fusion (RRF).
*   **Deployment**: 
    *   **Query Service**: Google Cloud Run Service.
    *   **Ingestion/Backfills**: Google Cloud Run Jobs.

## Local Development

```bash
# Start dependencies
docker-compose up -d

# Initial migration
cd month-2/capstone/rag-api
alembic upgrade head

# Run smoke benchmark
make benchmark-smoke
```

## Reproducible Benchmarking
Every search run is governed by a versioned and hashable `RetrievalConfig` containing all parameters (top_k, models, chunking strategy). Every chunk carries a `retrieval_config_hash` and `content_sha256`.

## Performance Gates
* **Week 1 Smoke Gate**: Non-zero NDCG@10 on seeded mini-corpus.
* **Regression Gate**: PRs must not regress NDCG@10 by more than 5%.

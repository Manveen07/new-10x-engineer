# Day 29: Query API

## Goal

Define the API contract before adding more retrieval tricks.

## Build

- `POST /v1/search`
- `POST /v1/answer`
- `RetrievalConfig`
- retrieval trace response.

## RetrievalConfig Fields

- `top_k`
- `dense_top_k`
- `lexical_top_k`
- `rerank_top_k`
- `alpha`
- `rrf_k`
- `filters`
- `embedding_model`
- `reranker_model`
- `chunking_profile`

## Done When

- Config hash is returned in every response and stored in retrieval logs.

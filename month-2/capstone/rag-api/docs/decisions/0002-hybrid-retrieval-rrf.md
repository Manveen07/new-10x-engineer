# 0002: Hybrid Retrieval With RRF

## Status

Draft

## Decision

Use dense pgvector retrieval plus PostgreSQL full-text search, then fuse rankings with Reciprocal Rank Fusion.

## Rationale

Dense search handles semantic similarity. Lexical search handles exact terms, acronyms, and section names. RRF is simple and does not require dense and lexical scores to share a scale.

## Consequences

The API must store dense, lexical, fused, and final ranks for debugging.

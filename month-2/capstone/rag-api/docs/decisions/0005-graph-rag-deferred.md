# 0005: Graph RAG Deferred

## Status

Draft

## Decision

Defer graph retrieval until dense, lexical, hybrid, reranked retrieval, and evals are stable.

## Rationale

Graph RAG can help entity-heavy corpora, but it adds extraction, storage, and ranking complexity. It should be an experiment, not the Month 2 backbone.

## Consequences

Graph work must be optional and benchmarked against the hybrid baseline.

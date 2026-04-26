# 0003: Reranking Interface

## Status

Draft

## Decision

Put reranking behind an interface with mock, local, and hosted implementations.

## Rationale

Rerankers improve quality but add latency and cost. They should be configurable and benchmarked against the no-reranker baseline.

## Consequences

Every benchmark should show pre-rerank and post-rerank metrics.

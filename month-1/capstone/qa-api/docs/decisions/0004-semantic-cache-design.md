# 0004: Semantic Cache Design

## Status

Draft

## Decision

Use exact cache first, semantic cache second, and provider call only on miss.

## Rationale

Exact cache is safe and cheap. Semantic cache can save more latency and cost, but it needs threshold tuning to avoid wrong answers.

## Consequences

The API must log `exact_hit`, `semantic_hit`, or `miss`, and the threshold must be documented with a small benchmark.

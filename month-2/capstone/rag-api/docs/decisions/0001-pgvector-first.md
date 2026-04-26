# 0001: pgvector First

## Status

Draft

## Decision

Use PostgreSQL + pgvector as the default Month 2 vector store.

## Rationale

Month 1 already uses PostgreSQL. pgvector keeps application data, metadata, tenant filters, retrieval logs, and vectors in one operational system. Exact search gives a reliable baseline before approximate indexes are introduced.

## Consequences

Managed vector stores remain benchmark targets, not the default implementation.

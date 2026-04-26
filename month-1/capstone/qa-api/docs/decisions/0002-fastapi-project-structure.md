# 0002: FastAPI Project Structure

## Status

Draft

## Decision

Use explicit routers, schemas, services, repositories, providers, and clients instead of putting logic directly in route handlers.

## Rationale

This keeps request handling, business logic, persistence, and external provider code independently testable.

## Consequences

There are more files early, but Month 2 can reuse the same structure for RAG endpoints without rewriting the API foundation.

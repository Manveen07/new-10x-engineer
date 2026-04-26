# 0005: Cloud Run Deployment Target

## Status

Draft

## Decision

Package the Month 1 API as a container that can run locally with Docker Compose and later deploy to Cloud Run.

## Rationale

Cloud Run fits a small async API well and keeps the deployment target simple enough for Month 1.

## Consequences

The app needs health checks, environment-based settings, structured logs to stdout, and no local-only assumptions.

# Day 37: Production Ingestion Job

## Goal

Make ingestion safe to run as a job, not only through an API request.

## Build

- CLI entrypoint.
- batch size config.
- dry-run mode.
- idempotency.
- failure report.
- Cloud Run Job config.

## Done When

- Ingestion can be run independently from the API service.

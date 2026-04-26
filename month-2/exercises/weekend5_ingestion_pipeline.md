# Weekend 5: Ingestion Pipeline

## Goal

Build an idempotent ingestion pipeline for the seed corpus.

## Build

- CLI: `uv run python scripts/ingest_cli.py datasets/seed_corpus`.
- parse -> normalize -> chunk -> embed -> write documents/chunks.
- skip unchanged documents by content hash.
- delete/rebuild chunks when content changes.
- write ingestion summary.

## Done When

- Running ingestion twice does not duplicate documents or chunks.
- Summary includes documents created, skipped, updated, chunks written, failures, and elapsed time.

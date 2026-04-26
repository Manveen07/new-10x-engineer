# Day 21: Corpus Builder

## Goal

Create a small but realistic corpus that can be ingested repeatedly and evaluated.

## Build

- `datasets/seed_corpus/`
- 20+ documents across Markdown, HTML, PDF text export, and JSON.
- `manifest.jsonl` with `document_id`, `tenant_id`, `source_uri`, `title`, `content_sha256`, and metadata.

## Done When

- Running the builder twice produces the same IDs and checksums.
- At least five documents have section headings.
- At least five questions in the future eval set require exact terms or acronyms.

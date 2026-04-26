# Week 5: Corpus, Chunking, Embeddings, And pgvector

## Outcome

By the end of Week 5, the RAG API should be able to ingest a small reproducible corpus, normalize documents, split them into chunks, embed them in mock or hosted mode, store them in PostgreSQL + pgvector, and run exact vector search.

## Why This Matters

Junior AI Engineer roles do not need you to invent vector search. They need you to build reliable ingestion and retrieval pipelines. pgvector is the right default here because it keeps vectors, document metadata, tenant filters, query logs, and joins in one database while you learn the retrieval fundamentals.

## Day 21: Corpus Builder

Exercise: `../exercises/day21_corpus_builder.md`

Build:

- A seeded corpus under `capstone/rag-api/datasets/seed_corpus/`.
- At least 20 documents across Markdown, HTML, PDF/text-export, and JSON.
- Stable document IDs.
- `source_uri`, title, tenant ID, content SHA-256, and metadata.

Done when:

- Re-running the corpus builder produces the same document IDs and checksums.

## Day 22: Parsing And Normalization

Exercise: `../exercises/day22_parsing_normalization.md`

Build:

- Markdown parser.
- HTML text extraction.
- PDF/text-export loader.
- JSON loader.
- Normalization rules for whitespace, boilerplate, headings, and metadata.

Done when:

- Every document becomes a normalized text record with metadata and checksum.

## Day 23: Chunking Experiments

Exercise: `../exercises/day23_chunking_experiments.py`

Build:

- Fixed-size chunker.
- Heading-aware Markdown chunker.
- Recursive character/token chunker.
- Sweep chunk sizes and overlaps.

Record:

- chunk count
- average tokens
- max tokens
- overlap percentage
- lost heading/context notes

## Day 24: Embedding Providers

Exercise: `../exercises/day24_embedding_providers.py`

Build:

- `EmbeddingProvider` interface.
- Deterministic mock provider for tests.
- Hosted OpenAI provider as optional.
- Local model experiment option for BGE-M3 or Nomic.
- Embedding metadata: provider, model, dimension, cost, latency.

Done when:

- Ingestion and tests work with mock embeddings and no API key.

## Day 25: pgvector Exact Search

Exercise: `../exercises/day25_pgvector_exact_search.md`

Build:

- `documents` and `chunks` tables.
- `embedding vector(...)` column.
- exact nearest-neighbor query using cosine distance.
- tenant filter before retrieval.
- tests for top-k ordering on seeded vectors.

Do not add HNSW yet. Exact search is the baseline.

## Weekend 5: Ingestion Pipeline

Exercise: `../exercises/weekend5_ingestion_pipeline.md`

Build:

- CLI: `uv run python scripts/ingest_cli.py datasets/seed_corpus`.
- Idempotent ingestion by tenant + content hash.
- Chunk rows with retrieval config hash.
- Batch embedding.
- Ingestion summary report.

## Week 5 Acceptance Gate

- [ ] Seed corpus is reproducible.
- [ ] Ingestion is idempotent.
- [ ] Chunks have metadata, content hash, token count, and config hash.
- [ ] Mock embeddings work without API keys.
- [ ] Exact pgvector search returns expected chunks.
- [ ] README explains why ANN indexes are delayed until after exact baseline.

## Core Resources

| Resource | Use |
|---|---|
| https://github.com/pgvector/pgvector | pgvector search and indexing |
| https://www.postgresql.org/docs/current/textsearch-intro.html | PostgreSQL text-search concepts |
| https://platform.openai.com/docs/guides/embeddings | hosted embeddings |
| https://huggingface.co/BAAI/bge-m3 | local/open embedding option |
| https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 | local/open embedding option |

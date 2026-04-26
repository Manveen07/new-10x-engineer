# Week 8: Production RAG Capstone

## Outcome

By the end of Week 8, the Month 2 capstone should be a reviewer-ready RAG API: ingest documents, retrieve context, answer with citations, log retrieval traces, run benchmarks, and explain tradeoffs.

## Day 36: End-To-End RAG Flow

Exercise: `../exercises/day36_e2e_rag_flow.md`

Build:

- ingest seed corpus.
- search indexed chunks.
- generate answer from retrieved context.
- return citations.
- persist query and retrieval run metadata.

Done when:

- A single demo command can show ingest -> search -> answer.

## Day 37: Production Ingestion Job

Exercise: `../exercises/day37_ingestion_job.md`

Build:

- Cloud Run Job-ready CLI.
- backfill-safe idempotency.
- batch size config.
- failure report.
- retry behavior.

Done when:

- Ingestion can be run as a separate job from the API.

## Day 38: Load And Latency Testing

Exercise: `../exercises/day38_latency_testing.md`

Build:

- p50/p95 dense search latency.
- p50/p95 hybrid search latency.
- p50/p95 answer latency.
- cache-hit vs cache-miss comparison.

Done when:

- README reports latency with caveats.

## Day 39: Security And Tenancy

Exercise: `../exercises/day39_tenancy_security.md`

Build:

- tenant filters on all document/chunk/retrieval queries.
- admin-only ingestion.
- source deletion behavior.
- no cross-tenant retrieval leakage tests.

Done when:

- Retrieval cannot return another tenant's chunks.

## Day 40: Capstone Polish

Exercise: `../capstone/CAPSTONE.md`

Build:

- README.
- architecture docs.
- benchmark reports.
- ADRs.
- demo script.
- final test pass.

## Weekend 8: Public Proof Of Work

Create:

- screenshots of `/docs`, benchmark output, and example answer with citations.
- `docs/demo-script.md`.
- `docs/architecture.md`.
- `docs/benchmarks/retrieval-quality.md`.
- `docs/benchmarks/latency.md`.
- ADRs for pgvector, hybrid retrieval, reranking, evals, and graph deferral.

## Week 8 Acceptance Gate

- [ ] `/v1/search` works.
- [ ] `/v1/answer` works.
- [ ] seeded corpus ingests.
- [ ] benchmarks run.
- [ ] answer includes citations.
- [ ] retrieval trace is persisted.
- [ ] docs are reviewer-ready.
- [ ] Month 3 agents can call the RAG API as a tool.

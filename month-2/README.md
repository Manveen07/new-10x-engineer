# Month 2 - Retrieval Engineering And Production RAG

## Goal

Build a realistic retrieval engineering platform on top of the Month 1 API foundation. By the end of Month 2, you should have a RAG API that ingests documents, chunks them, embeds them, stores them in PostgreSQL + pgvector, retrieves with dense and lexical search, fuses results with RRF, reranks candidates, generates grounded answers with citations, and measures retrieval quality.

Month 2 is where the roadmap becomes visibly "AI Engineer" instead of generic backend. The job-ready signal is not "I used a RAG framework." The signal is: **I can build, measure, debug, and improve a retrieval system.**

## Research Basis

Current AI engineering/RAG roles emphasize end-to-end RAG workflows, document ingestion, vector databases, low-latency APIs, monitoring, tracing, and evaluation. The technical research also points in a consistent direction:

- pgvector keeps vectors in PostgreSQL and supports exact and approximate nearest-neighbor search. Its docs explicitly frame exact search as the default with perfect recall, while HNSW/IVFFlat trade recall for speed.
- PostgreSQL full-text search gives a practical lexical baseline with `tsvector`, `tsquery`, ranking, and indexes.
- Pinecone and Weaviate documentation both treat hybrid retrieval as the combination of dense semantic search and sparse/keyword search.
- Ragas exposes RAG metrics such as context precision, context recall, response relevancy, and faithfulness.
- Modern embedding and reranking stacks include hosted embeddings, open model cards such as BGE-M3 and Nomic Embed, and rerankers such as Cohere Rerank.

## How Month 2 Compounds Month 1

Reuse Month 1 patterns instead of rebuilding them:

| Month 1 skill | Month 2 use |
|---|---|
| FastAPI structure | RAG query and ingestion API |
| Pydantic schemas/settings | retrieval configs, ingest requests, eval configs |
| Auth/RBAC | tenant-safe documents and admin-only ingestion |
| Async PostgreSQL | documents, chunks, embeddings, retrieval runs, eval results |
| Redis cache | answer cache and short-lived benchmark/run cache |
| Provider adapter | generation and embedding provider boundaries |
| structlog + request IDs | query-level retrieval telemetry |
| pytest/respx | tests without live provider calls |
| ADRs | explain retrieval tradeoffs |

## Month 2 Stack

| Area | Default | Why |
|---|---|---|
| API | FastAPI from Month 1 | Keep backend patterns consistent |
| Vector store | PostgreSQL + pgvector | One operational data plane, exact search first |
| Lexical search | PostgreSQL Full Text Search | Strong baseline before adding another search service |
| Hybrid fusion | Reciprocal Rank Fusion | Simple, explainable, framework-independent |
| Embeddings | mock/local first, OpenAI hosted optional, BGE-M3/Nomic experiment | Tests stay free; experiments teach tradeoffs |
| Reranking | mock first, local cross-encoder or Cohere optional | Quality improvement after retrieval baseline |
| Evaluation | BEIR-style metrics + Ragas-style answer metrics | Separates retrieval quality from generation quality |
| Observability | structlog + retrieval run records | Debug failed answers by inspecting retrieved chunks |
| Deployment | Cloud Run service + Cloud Run Job-ready container | API and ingestion/backfills have different runtime shapes |

## Month Structure

| Week | Theme | Main deliverable |
|---|---|---|
| 5 | Corpus, chunking, embeddings, pgvector | reproducible ingestion and exact vector search |
| 6 | Hybrid retrieval and reranking | dense + FTS + RRF + reranker benchmark |
| 7 | Evaluation and retrieval observability | golden set, metrics, regression gates, optional graph extension |
| 8 | Production RAG capstone | deployed-ready RAG API with docs, ADRs, benchmarks, and demo |

## Daily Exercise Map

| Day | Exercise | File or folder | Required output |
|---|---|---|---|
| 21 | Corpus builder | `exercises/day21_corpus_builder.md` | seeded docs with IDs, metadata, checksums |
| 22 | Parsing and normalization | `exercises/day22_parsing_normalization.md` | Markdown/HTML/PDF text extraction rules |
| 23 | Chunking experiments | `exercises/day23_chunking_experiments.py` | chunk-size/overlap sweep |
| 24 | Embedding providers | `exercises/day24_embedding_providers.py` | mock + hosted/local embedding interface |
| 25 | pgvector exact search | `exercises/day25_pgvector_exact_search.md` | exact nearest-neighbor query and tests |
| Weekend 5 | Ingestion pipeline | `exercises/weekend5_ingestion_pipeline.md` | idempotent ingestion job |
| 26 | PostgreSQL FTS | `exercises/day26_postgres_fts.md` | lexical search with `tsvector` and ranking |
| 27 | RRF fusion | `exercises/day27_rrf_fusion.py` | merge dense and lexical rankings |
| 28 | Reranking | `exercises/day28_reranking.py` | reranker interface and benchmark |
| 29 | Query API | `exercises/day29_query_api.md` | `/search` and `/answer` contracts |
| 30 | Citations and grounded answers | `exercises/day30_citations_grounding.md` | answer format with chunk citations |
| Weekend 6 | Hybrid retrieval benchmark | `exercises/weekend6_hybrid_benchmark.md` | dense vs lexical vs hybrid vs reranked report |
| 31 | Golden evaluation set | `exercises/day31_golden_eval_set.md` | 30-50 labeled questions |
| 32 | Retrieval metrics | `exercises/day32_retrieval_metrics.py` | precision@k, recall@k, MRR, NDCG |
| 33 | Ragas-style answer evals | `exercises/day33_ragas_answer_evals.md` | faithfulness/context metrics plan |
| 34 | Retrieval telemetry | `exercises/day34_retrieval_telemetry.md` | retrieval run schema and logs |
| 35 | Optional graph extension | `exercises/day35_optional_graph_extension.md` | measured graph-RAG experiment plan |
| Weekend 7 | Regression gate | `exercises/weekend7_regression_gate.md` | benchmark threshold and CI gate |
| 36 | End-to-end RAG flow | `exercises/day36_e2e_rag_flow.md` | ingest -> retrieve -> answer -> log |
| 37 | Production ingestion job | `exercises/day37_ingestion_job.md` | Cloud Run Job-ready CLI |
| 38 | Load and latency testing | `exercises/day38_latency_testing.md` | p50/p95 search and answer latency |
| 39 | Security and tenancy | `exercises/day39_tenancy_security.md` | tenant filters and admin-only ingestion |
| 40 | Capstone polish | `capstone/CAPSTONE.md` | README, ADRs, benchmarks, demo script |

## Weekly Acceptance Gates

### Week 5 Gate

- [ ] Seed corpus is reproducible.
- [ ] Ingestion is idempotent by content hash.
- [ ] Chunks store text, metadata, token count, content hash, and config hash.
- [ ] Embeddings can run in mock mode without API keys.
- [ ] pgvector exact search works before ANN indexes are introduced.

### Week 6 Gate

- [ ] PostgreSQL FTS search works.
- [ ] Dense and lexical retrievers are benchmarked separately.
- [ ] RRF fusion works and is explainable.
- [ ] Reranker runs behind an interface.
- [ ] Hybrid or reranked retrieval improves at least one metric on the seeded eval set.

### Week 7 Gate

- [ ] Golden set has answerable and unanswerable questions.
- [ ] Retrieval metrics include precision@k, recall@k, MRR, and NDCG.
- [ ] Answer metrics include faithfulness and context precision/recall plan.
- [ ] Retrieval run logs include config hash, chunk IDs, scores, latency, and model names.
- [ ] Regression threshold is documented.

### Week 8 Gate

- [ ] `/search` returns ranked chunks with scores and retrieval trace.
- [ ] `/answer` returns answer plus citations.
- [ ] `/ingest` or ingestion CLI can load seeded documents.
- [ ] Benchmarks are reproducible.
- [ ] README and ADRs explain retrieval decisions.
- [ ] Month 3 agents can consume the RAG API as a tool.

## Not Doing In Month 2

- Multi-agent workflows.
- MCP.
- Fine-tuning.
- Vendor-only vector database dependency.
- Graph RAG as the primary path.
- Complex UI.

These come later or remain optional experiments.

## Final Month 2 Checklist

- [ ] `uv run ruff check .` passes.
- [ ] `uv run mypy app` passes.
- [ ] `uv run pytest` passes.
- [ ] `docker compose up -d` starts PostgreSQL + pgvector and Redis.
- [ ] Seed corpus ingests.
- [ ] Exact vector search works.
- [ ] PostgreSQL FTS works.
- [ ] Hybrid RRF works.
- [ ] Reranker path works.
- [ ] Retrieval metrics run from a command.
- [ ] `/search` and `/answer` work in mock mode.
- [ ] README, ADRs, architecture diagram, and benchmark report exist.

## Sources Used

- pgvector README: https://github.com/pgvector/pgvector
- PostgreSQL full text search docs: https://www.postgresql.org/docs/current/textsearch-intro.html
- Pinecone hybrid search docs: https://docs.pinecone.io/guides/search/hybrid-search
- Weaviate hybrid search docs: https://docs.weaviate.io/weaviate/concepts/search/hybrid-search
- Ragas metrics docs: https://docs.ragas.io/en/stable/concepts/metrics/
- BGE-M3 model card: https://huggingface.co/BAAI/bge-m3
- Nomic Embed model card: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
- Cohere Rerank docs: https://docs.cohere.com/docs/rerank

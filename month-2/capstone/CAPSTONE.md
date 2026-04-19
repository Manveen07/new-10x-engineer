# Month 2 Capstone: Production RAG Pipeline

## Deliverable
A complete, evaluated, deployable RAG system that ingests documents, retrieves relevant context using hybrid search, generates grounded answers with citations, and tracks quality metrics.

## Architecture
```
┌─── Ingestion (offline) ───────────────────────────────────────────┐
│ Documents → Parse → Chunk (recursive) → Embed (batch) → pgvector │
│            → Entity Extract → Neo4j (optional)                    │
│            → Metadata → PostgreSQL                                │
└───────────────────────────────────────────────────────────────────┘

┌─── Query (real-time) ─────────────────────────────────────────────┐
│ Query → Cache Check → Query Transform (HyDE if vague)            │
│       → Hybrid Retrieval (BM25 + Vector + RRF)                   │
│       → Rerank (cross-encoder)                                   │
│       → Context Assembly → LLM Generation → Citation Extraction  │
│       → Cache Store → Log → Return                               │
└───────────────────────────────────────────────────────────────────┘

┌─── Evaluation (continuous) ───────────────────────────────────────┐
│ Ragas: faithfulness, context_precision, context_recall, relevancy │
│ Monitoring: latency, cache hit rate, cost per query               │
└───────────────────────────────────────────────────────────────────┘
```

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /ingest | Upload and process documents |
| POST | /query | Ask a question (main RAG endpoint) |
| GET | /query/history | User's past queries |
| GET | /documents | List ingested documents |
| DELETE | /documents/{id} | Remove a document (and its chunks) |
| GET | /eval/metrics | Current evaluation metrics |
| GET | /health | Service health |

## Evaluation Targets
- Faithfulness: >0.8
- Context Precision: >0.7
- Context Recall: >0.7
- Answer Relevancy: >0.8
- p95 Latency: <3s
- Cache hit rate: >40% after 100 queries

## Test Dataset
Create 20 question-answer pairs covering:
- 10 straightforward factual questions
- 5 multi-hop reasoning questions
- 3 questions requiring specific document sections
- 2 unanswerable questions (to test graceful "I don't know")

## Stack
- FastAPI + async PostgreSQL (from Month 1)
- pgvector for vector storage
- Redis for semantic caching (from Month 1)
- LLM adapter pattern (from Month 1)
- Ragas + DeepEval for evaluation
- Docker Compose for deployment

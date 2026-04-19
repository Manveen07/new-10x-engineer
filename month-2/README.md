# Month 2 — RAG Pipelines & Vector Data Engineering

## Goal
Build production-quality Retrieval-Augmented Generation systems. By month's end you'll have a full RAG pipeline with hybrid search, reranking, evaluation metrics, and a knowledge graph layer.

## Weekly Breakdown

| Week | Topic | Key Deliverable |
|------|-------|----------------|
| 5 | Vector Databases & Indexing | Document search API with pgvector benchmarks |
| 6 | Advanced RAG Techniques | HyDE, hybrid search, reranking implementations |
| 7 | Graph RAG & Production Architecture | Graph + vector hybrid retrieval system |
| 8 | Production RAG Capstone | Evaluated, deployed RAG pipeline |

## Prerequisites (from Month 1)
- Working FastAPI project with auth, database, caching
- LLM provider adapter pattern
- Docker Compose fluency
- Async Python proficiency

## New Tools This Month
```bash
pip install pgvector psycopg[binary] langchain langchain-openai langchain-community
pip install chromadb sentence-transformers rank-bm25 cohere
pip install neo4j llama-index ragas
pip install tiktoken unstructured pdf2image pytesseract
```

## Progress Tracker
- [ ] Week 5: Vector Databases
- [ ] Week 6: Advanced RAG
- [ ] Week 7: Graph RAG
- [ ] Week 8: Production RAG Capstone

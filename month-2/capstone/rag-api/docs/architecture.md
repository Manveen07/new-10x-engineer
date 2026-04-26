# Month 2 RAG API Architecture

```mermaid
flowchart LR
    Source[Source documents] --> Ingest[Ingestion job]
    Ingest --> Normalize[Parse and normalize]
    Normalize --> Chunk[Chunking profile]
    Chunk --> Embed[Embedding provider]
    Embed --> PG[(PostgreSQL + pgvector)]
    Chunk --> FTS[Postgres FTS tsvector]
    FTS --> PG
    Query[Query] --> API[FastAPI]
    API --> Dense[Dense retrieval]
    API --> Lexical[Lexical retrieval]
    Dense --> Fusion[RRF fusion]
    Lexical --> Fusion
    Fusion --> Rerank[Reranker]
    Rerank --> Context[Context assembly]
    Context --> Generator[LLM provider adapter]
    Generator --> Response[Answer + citations]
    API --> Logs[Retrieval trace logs]
```

## Design Notes

- pgvector is the default vector store.
- Exact vector search is the first baseline.
- PostgreSQL FTS is the lexical baseline.
- Hybrid search uses RRF so dense and lexical scores do not need the same scale.
- Reranking is optional and benchmarked.
- Graph retrieval is optional after baseline metrics are stable.

# Week 8: Production RAG Pipeline Capstone

## Why This Matters
This is where theory becomes a deployable system. You'll build an end-to-end RAG pipeline, evaluate it with real metrics, and make it production-ready. This project becomes your portfolio piece and the foundation for Month 3's agent layer.

---

## Day-by-Day Plan

### Monday — End-to-End Pipeline with Evaluation (1.5h)

**Read (1h):**
- Weaviate: Advanced RAG Techniques ebook
  https://weaviate.io/ebooks/advanced-rag-techniques

**Read (30 min):**
- Redis: 10 techniques to improve RAG accuracy
  https://redis.io/blog/10-techniques-to-improve-rag-accuracy/

**Plan your capstone pipeline:**
- What documents are you using? (Pick a domain you care about — technical docs, legal, medical, etc.)
- What chunking strategy?
- Which embedding model?
- What retrieval pipeline? (hybrid + rerank recommended)
- How will you evaluate?

---

### Tuesday — Build the Ingestion Pipeline (1.5h)

**Implement:**
1. Document loading: handle PDF, Markdown, plain text
   - Use `unstructured` library or `pypdf2` for PDFs
   - Use front-matter extraction for metadata
2. Chunking: recursive text splitting with semantic boundaries
   - 400-500 tokens per chunk, 50 token overlap
   - Preserve section headers as metadata
3. Embedding: batch processing with rate limiting
   - Use your adapter pattern from Month 1
   - Batch size: 100 texts per API call
4. Storage: pgvector with metadata columns
   - Store: content, embedding, source_file, section, page_number, chunk_index
5. Handle duplicates: hash content to detect re-ingestion

**Exercise:** Ingest at least 50 documents (200+ chunks).

---

### Wednesday — Build the Retrieval Pipeline (1.5h)

**Implement:**
1. Query embedding using your adapter
2. Hybrid search: BM25 + vector with RRF fusion
3. Reranking: cross-encoder or Cohere Rerank
4. Context assembly:
   - Deduplicate overlapping chunks
   - Order by relevance
   - Truncate to fit context window (leave room for system prompt + answer)
5. Semantic cache integration (from Month 1 Week 4)
6. Query transformation: HyDE for ambiguous queries

---

### Thursday — Build the Generation Pipeline (1.5h)

**Implement:**
1. System prompt with instructions for citation
2. Context + query → LLM generation
3. Structured output with Pydantic:
   ```python
   class RAGResponse(BaseModel):
       answer: str
       citations: list[Citation]
       confidence: float  # 0-1
       sources_used: int
   ```
4. Streaming responses (SSE for long answers)
5. Fallback: "I don't have enough information" when context is insufficient
6. Token counting: track input/output for cost monitoring

---

### Friday — Evaluation and Optimization (1.5h)

**Setup evaluation:**
```bash
pip install ragas deepeval
```

**Create test dataset:**
- 20 question-answer pairs with ground truth
- Include: easy factual, hard multi-hop, unanswerable (no context)

**Measure with Ragas:**
| Metric | What it measures | Target |
|--------|-----------------|--------|
| Faithfulness | Is the answer grounded in context? | >0.8 |
| Context Precision | Are retrieved chunks relevant? | >0.7 |
| Context Recall | Did we find all relevant chunks? | >0.7 |
| Answer Relevancy | Does the answer address the question? | >0.8 |

**Iterate:**
1. Run evaluation
2. Identify weakest metric
3. Adjust the relevant pipeline stage
4. Re-evaluate
5. Repeat until targets met

---

### Weekend — Polish and Document (2h)

1. Write README with architecture diagram
2. Add performance benchmarks (latency, throughput, cost)
3. Docker Compose deployment (FastAPI + PostgreSQL/pgvector + Redis + Neo4j optional)
4. Create a simple demo script or Streamlit UI

**Done when:**
- Ragas faithfulness >0.8, context precision >0.7
- API handles concurrent requests
- Documented with architecture diagram and benchmarks
- Deployable with `docker compose up`

---

## Month 2 Capstone Specification

See `capstone/CAPSTONE.md` for the full project spec.

---

## Skill Checkpoint

1. Walk through your pipeline end-to-end. What's the p95 latency? Where are the bottlenecks?
2. Your faithfulness score is 0.6. What do you change?
3. Your context recall is low but precision is high. What does this tell you?
4. How would you scale this to 10x the document corpus?
5. What's the monthly cost to run this system for 1000 queries/day?

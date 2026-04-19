# Week 6: Advanced RAG Techniques

## Why This Matters
Naive RAG (embed query → find similar chunks → send to LLM) works for demos but fails in production. Users ask vague questions, documents are poorly chunked, and the retrieved context is often wrong. This week teaches you the techniques that close the gap between demo and production.

---

## Day-by-Day Plan

### Monday — RAG From Scratch Foundations (1.5h)

**Watch/Read (1.5h):**
- freeCodeCamp: Mastering RAG From Scratch (first 1.5h of 2.5h course)
  https://www.freecodecamp.org/news/mastering-rag-from-scratch/
- Companion repo (follow along):
  https://github.com/langchain-ai/rag-from-scratch

**The RAG Pipeline (what you're building):**
```
                    INDEXING (offline)
    ┌────────────────────────────────────────────┐
    │ Documents → Chunk → Embed → Store in VectorDB │
    └────────────────────────────────────────────┘

                    RETRIEVAL (at query time)
    ┌────────────────────────────────────────────────────┐
    │ Query → [Transform?] → Embed → Search → [Rerank?] │
    └──────────────────────────┬─────────────────────────┘
                               │
                    GENERATION │
    ┌──────────────────────────┴─────────────────────────┐
    │ Retrieved Context + Query → LLM → Answer + Citations│
    └────────────────────────────────────────────────────┘
```

**Key insight from this session:**
- Indexing quality determines retrieval ceiling — bad chunks = bad retrieval, period
- Query transformation can dramatically improve results on vague queries
- The generation step should be the simplest part — retrieval is where the magic happens

**Exercise:**
Build a minimal RAG pipeline from scratch (no framework):
1. Load 10 Wikipedia articles
2. Chunk with RecursiveTextSplitter (500 tokens, 50 overlap)
3. Embed with OpenAI or mock embeddings
4. Store in pgvector (from Week 5)
5. Query → embed → search → concatenate context → send to LLM
Test with 5 questions. How often does it return the right information?

---

### Tuesday — HyDE and Query Transformation (1.5h)

**Finish (1h):**
- RAG From Scratch course (remaining portion)

**Read (30 min):**
- HyDE paper (abstract + method section)
  https://arxiv.org/abs/2212.10496

**HyDE (Hypothetical Document Embeddings):**
```
Traditional:  "What causes rain?" → embed question → search
                                     ↑ Problem: question embeddings ≠ answer embeddings

HyDE:         "What causes rain?"
                    │
              ┌─────▼──────┐
              │ LLM: Write  │
              │ a hypothetical│
              │ answer       │
              └─────┬──────┘
                    │
              "Rain is caused by water vapor condensing..."
                    │
              embed this hypothetical answer → search
              ↑ Now the search embedding matches document style!
```

**Why it works:** Questions and answers live in different embedding spaces. "What causes rain?" is far from "Water vapor rises, cools, and condenses into droplets." HyDE bridges this gap by converting the question into answer-space before searching.

**When to use HyDE:**
- Vague or abstract queries ("tell me about machine learning")
- When questions and documents are stylistically different
- NOT for specific factual lookups ("What is the capital of France?")

**Exercise:**
Implement HyDE in your pipeline:
1. Query → LLM generates hypothetical answer (cheap, fast model)
2. Embed the hypothetical answer
3. Search with that embedding
4. Compare retrieval quality: direct query embedding vs HyDE embedding
Test on 10 queries. Measure precision@5 for each approach.

---

### Wednesday — Hybrid Search and Reranking (1.5h)

**Read (1h):**
- Superlinked: Optimizing RAG with hybrid search + reranking
  https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking

**Read (30 min):**
- Dasroot: Advanced RAG with hybrid search
  https://dasroot.net/posts/2025/12/advanced-rag-techniques-hybrid-search/

**Hybrid Search Architecture:**
```
Query: "PostgreSQL JSONB performance optimization"

    ┌──── BM25 (keyword) ────┐     ┌──── Vector (semantic) ────┐
    │ Finds exact matches:    │     │ Finds meaning matches:     │
    │ - "JSONB" appears       │     │ - "JSON data types"        │
    │ - "PostgreSQL" appears  │     │ - "database query tuning"  │
    │ - "optimization"        │     │ - "NoSQL in Postgres"      │
    └────────┬────────────────┘     └────────┬──────────────────┘
             │                                │
             └──────── Reciprocal Rank Fusion ─┘
                              │
                    Combined ranked list
                              │
                     ┌────────▼─────────┐
                     │ Cross-Encoder     │
                     │ Reranker          │
                     │ (e.g., Cohere)    │
                     └────────┬─────────┘
                              │
                     Top-k reranked results
```

**Reciprocal Rank Fusion (RRF):**
```
RRF_score(doc) = Σ (1 / (k + rank_in_method_i))

k=60 is standard. This elegantly combines results from different methods
without needing to normalize scores (which is hard across methods).
```

**Reranking:**
- Initial retrieval is fast but approximate (bi-encoder: embed independently)
- Reranking is slow but precise (cross-encoder: embed query+doc together)
- Pattern: retrieve 50 candidates fast → rerank to top 5 precisely

**Target improvement:** MAP from ~0.5 (vector only) to ~0.8 (hybrid + rerank)

**Exercise:**
1. Implement BM25 retrieval using `rank-bm25` library
2. Implement vector retrieval (from Week 5)
3. Combine with RRF
4. Add Cohere Rerank (or a cross-encoder from sentence-transformers)
5. Measure: precision@5 for vector-only, BM25-only, hybrid, hybrid+rerank

---

### Thursday — RAPTOR Hierarchical Retrieval (1.5h)

**Read (45 min):**
- RAPTOR paper (focus on method section)
  https://arxiv.org/pdf/2401.18059.pdf

**Study (45 min):**
- FareedKhan-dev RAPTOR implementation
  https://github.com/FareedKhan-dev/rag-with-raptor

**RAPTOR Concept:**
```
Level 3:  [Summary of entire corpus]           ← "What is this about?"
              │
Level 2:  [Topic A summary] [Topic B summary]  ← "What are the main themes?"
              │                    │
Level 1:  [Cluster 1] [Cluster 2] [Cluster 3]  ← "What are the subtopics?"
              │    │       │           │
Level 0:  [chunk] [chunk] [chunk] [chunk] [chunk]  ← raw document chunks
```

**How it works:**
1. Chunk documents (Level 0)
2. Embed chunks, cluster similar ones (k-means or UMAP + GMM)
3. Summarize each cluster → Level 1 nodes
4. Embed Level 1 nodes, cluster again, summarize → Level 2
5. Repeat until you have a single root summary

**At query time:** Search across ALL levels. Detail queries match Level 0 chunks. Broad queries match higher-level summaries.

**When to use:**
- Document corpus with hierarchical structure (textbooks, legal codes, manuals)
- Mix of specific and broad queries
- NOT for simple fact lookup

**Exercise:**
Implement a simplified RAPTOR:
1. Chunk 5 documents
2. Cluster chunks using simple cosine similarity
3. Summarize each cluster with an LLM
4. Store all levels in pgvector
5. Query and observe: broad queries hit summaries, specific queries hit chunks

---

### Friday — Chunking Strategies Comparison (1.5h)

**Read (45 min):**
- Weaviate: Chunking strategies for RAG
  https://weaviate.io/blog/chunking-strategies-for-rag

**Read (45 min):**
- LangCopilot: Practical chunking guide
  https://langcopilot.com/posts/2025-10-11-document-chunking-for-rag-practical-guide

**Chunking Methods Compared:**

| Method | How | Pros | Cons | Use When |
|--------|-----|------|------|----------|
| **Fixed-size** | Split every N tokens | Simple, predictable | Breaks mid-sentence | Uniform docs, speed priority |
| **Recursive** | Split by separators (\n\n, \n, .) | Respects structure | May create uneven chunks | General purpose (good default) |
| **Semantic** | Split when embedding similarity drops | Preserves meaning | Expensive, complex | Quality-critical applications |
| **Document-aware** | Split by headers, sections | Preserves document structure | Requires structured docs | Markdown, HTML, PDFs |
| **Late chunking** | Embed full doc, then chunk embeddings | Best context preservation | Needs long-context embedder | When context matters most |

**The right chunk size matters:**
- Too small (100 tokens): loses context, more retrieval needed
- Too large (2000 tokens): dilutes relevance, wastes LLM context
- Sweet spot: **300-500 tokens** with 50-100 token overlap for most use cases

**Exercise:**
Take the same 5 documents. Chunk with 4 strategies:
1. Fixed-size (512 tokens)
2. Recursive text splitting (500 tokens, 50 overlap)
3. Semantic chunking (similarity threshold)
4. Document-aware (by sections/headers)

For each: count chunks, measure average chunk size, and test retrieval quality on 10 queries.

---

### Weekend — Advanced RAG Notebook (1-2h)

**Work through 3-4 notebooks from:**
- NirDiamant/RAG_Techniques repo
  https://github.com/NirDiamant/RAG_Techniques

**Recommended notebooks:**
1. HyDE implementation
2. Hybrid search with reranking
3. Contextual chunking
4. Multi-query retrieval

**Done when:** You have working implementations of at least 3 advanced RAG techniques and can explain the trade-off each one makes (quality vs latency vs cost).

---

## Skill Checkpoint

1. Given a domain (legal documents), recommend: chunking strategy, embedding model, retrieval approach. Justify each.
2. Explain why reranking after initial retrieval improves precision. What's the compute trade-off?
3. When does HyDE help vs hurt? Give an example of each.
4. Your RAG system answers "I don't know" too often. Walk through your debugging process.
5. Design a chunking strategy for a codebase (code + docs mixed).

---

## Core Resources

| Resource | Type | URL |
|----------|------|-----|
| RAG From Scratch | Course | https://github.com/langchain-ai/rag-from-scratch |
| NirDiamant/RAG_Techniques | Implementations | https://github.com/NirDiamant/RAG_Techniques |
| rank-bm25 | Library | https://github.com/dorianbrown/rank_bm25 |
| Cohere Rerank | API | https://docs.cohere.com/docs/reranking |
| sentence-transformers CrossEncoder | Library | https://www.sbert.net/docs/cross_encoder/usage/usage.html |

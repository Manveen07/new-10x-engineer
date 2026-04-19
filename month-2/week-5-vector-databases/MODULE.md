# Week 5: Vector Databases & Indexing Algorithms

## Why This Matters
Every RAG system, every semantic search, every recommendation engine is built on vector similarity search. Understanding HOW it works at the algorithmic level — not just calling an API — separates AI engineers from API callers. When your search returns bad results, you need to know if the problem is your index parameters, your embedding model, or your chunking strategy.

---

## Day-by-Day Plan

### Monday — HNSW Algorithm Deep Dive (1.5h)

**Read (45 min):**
- Pinecone HNSW guide (excellent visuals and intuition)
  https://www.pinecone.io/learn/series/faiss/hnsw/

**Read (45 min):**
- TigerData HNSW basics
  https://www.tigerdata.com/blog/vector-database-basics-hnsw

**The HNSW Mental Model:**
```
Layer 2 (sparse):    A ─────────── D          (long-range "highway" links)
                     │             │
Layer 1 (medium):    A ── B ────── D ── E     (medium-range links)
                     │    │        │    │
Layer 0 (dense):     A ─ B ─ C ─ D ─ E ─ F   (short-range, all nodes)
```

- **Hierarchical**: multiple layers, top layers are sparse (long jumps), bottom is dense (fine-grained)
- **Navigable**: start at top layer, greedily move toward query vector, drop down layers
- **Small World**: any node reachable in O(log N) hops

**Key Parameters:**
| Parameter | What it controls | Trade-off |
|-----------|-----------------|-----------|
| `M` | Max connections per node | Higher = better recall, more memory |
| `ef_construction` | Search width during build | Higher = better graph, slower build |
| `ef_search` | Search width during query | Higher = better recall, slower query |

**Start with**: M=16, ef_construction=200, ef_search=100. Tune from there.

**Exercise:**
Draw the HNSW layered graph by hand for 10 sample vectors. Trace a query search from the top layer down. Explain why this is O(log N) not O(N).

---

### Tuesday — IVF Indexing and Comparison (1.5h)

**Read (45 min):**
- Medium: IVF, HNSW, and Product Quantization explained
  https://medium.com/@kiranvutukuri/95-vector-database-indexing-methods-ivf-hnsw-and-product-quantization-c4a6243929db

**Read (45 min):**
- MyScale HNSW vs IVF comparison
  https://www.myscale.com/blog/hnsw-vs-ivf-explained-powerful-comparison/

**IVF Mental Model:**
```
Step 1: Cluster all vectors into buckets (Voronoi cells)

    Cluster 1: [v1, v4, v7, v12]     ← centroid c1
    Cluster 2: [v2, v5, v8, v13]     ← centroid c2
    Cluster 3: [v3, v6, v9, v10]     ← centroid c3
    ...

Step 2: To search, find nearest centroids, then search only those clusters

    Query q → nearest centroids: c2, c3 (nprobe=2)
    → Only search vectors in clusters 2 and 3
    → Skip all other clusters (massive speedup!)
```

**Comparison Table:**

| Factor | HNSW | IVFFlat |
|--------|------|---------|
| Memory | O(N × M) — high | O(N) — lower |
| Build time | Slow (graph construction) | Fast (k-means clustering) |
| Query speed | O(log N) — fast | Depends on nprobe |
| Recall | Very high (>95%) | Depends on nprobe |
| Updates | Good (incremental) | Bad (requires rebuild) |
| Best for | Read-heavy, high recall | Memory constrained, large datasets |

**Rule of thumb**: Use HNSW unless you're memory constrained. For most AI applications, recall matters more than memory.

**Exercise:**
Create a comparison table for your specific use case. When would you choose IVFFlat? (Answer: datasets > 10M vectors where memory is a constraint, or when you need faster builds and can accept slightly lower recall.)

---

### Wednesday — pgvector Hands-on (1.5h)

**Read (45 min):**
- pgvector HNSW vs IVFFlat study
  https://medium.com/@bavalpreetsinghh/pgvector-hnsw-vs-ivfflat-a-comprehensive-study-21ce0aaab931

**Read (15 min):**
- pgvector GitHub README
  https://github.com/pgvector/pgvector

**Setup:**
```bash
# Docker (easiest)
docker run --name pgvector -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d pgvector/pgvector:pg16

# Or install extension on existing Postgres
# CREATE EXTENSION vector;
```

**Exercise:** See `exercises/week5_pgvector.py`

1. Create a table with a vector column
2. Insert 100K+ vectors (use random or pre-computed embeddings)
3. Create an HNSW index: `CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 200)`
4. Create an IVFFlat index: `CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)`
5. Benchmark both:
   - Query latency (p50, p95, p99)
   - Recall@10 vs brute-force
   - Index build time
   - Index size on disk

**Target benchmarks (100K vectors, 1536 dimensions):**
- HNSW: <10ms p95, >95% recall
- IVFFlat (nprobe=10): <5ms p95, >85% recall

---

### Thursday — Vector Database Comparison (1.5h)

**Read (45 min):**
- Firecrawl: Best vector databases comparison
  https://www.firecrawl.dev/blog/best-vector-databases

**Read (45 min):**
- Liveblocks practical guide
  https://liveblocks.io/blog/whats-the-best-vector-database-for-building-ai-products

**Decision Matrix:**

| Database | Best For | Hosting | Cost Model |
|----------|----------|---------|------------|
| **pgvector** | Teams with existing Postgres, simplicity | Self-hosted or any Postgres provider | Free (extension) |
| **Pinecone** | Managed service, zero ops, rapid prototyping | Cloud only | Per-vector pricing |
| **Qdrant** | High performance, Rust-based, filtering | Self-hosted or cloud | Open source + cloud |
| **Milvus** | Large scale (billions), enterprise | Self-hosted or Zilliz cloud | Open source |
| **Weaviate** | GraphQL API, multi-modal, built-in vectorization | Self-hosted or cloud | Open source + cloud |
| **Chroma** | Prototyping, in-process, Python-native | In-process or Docker | Open source |

**For this plan: pgvector is the default.** You already know PostgreSQL, it's free, it handles metadata queries natively (no separate DB), and it's good enough for 90% of production use cases up to ~10M vectors.

**When to upgrade:**
- >10M vectors and need sub-10ms latency → Qdrant or Milvus
- Zero ops budget → Pinecone
- Need multi-modal (image + text) → Weaviate

---

### Friday — Embedding Models Landscape (1.5h)

**Read (45 min):**
- KDnuggets: Top 5 embedding models for RAG
  https://www.kdnuggets.com/top-5-embedding-models-for-your-rag-pipeline

**Read (45 min):**
- Encord: Complete guide to embeddings
  https://encord.com/blog/complete-guide-to-embeddings-in-2026/
- MTEB Leaderboard (bookmark — check before choosing a model)
  https://huggingface.co/spaces/mteb/leaderboard

**Embedding Model Decision Guide:**

| Model | Dims | Quality | Speed | Cost | Best For |
|-------|------|---------|-------|------|----------|
| text-embedding-3-small (OpenAI) | 1536 | Good | Fast | $0.02/1M tokens | General purpose, cost-effective |
| text-embedding-3-large (OpenAI) | 3072 | Better | Medium | $0.13/1M tokens | When quality matters |
| BGE-M3 (BAAI) | 1024 | Very good | Medium | Free (local) | Multilingual, open-source |
| Qwen3-Embedding-8B | 4096 | SOTA | Slow | Free (local) | Highest quality, if you have GPU |
| Cohere embed-v3 | 1024 | Very good | Fast | $0.10/1M tokens | Multilingual, search-optimized |
| all-MiniLM-L6-v2 | 384 | Decent | Very fast | Free (local) | Prototyping, speed priority |

**Key insight**: The embedding model affects retrieval quality MORE than the vector index. A great index with bad embeddings will always lose to a mediocre index with great embeddings.

**Exercise:**
Pick 2 embedding models. Embed 20 test queries and 100 documents with each. Compare retrieval quality (precision@5) for the same queries. Document which model works better for your domain.

---

### Weekend — Build a Vector Search Engine (1-2h)

See `exercises/weekend5_vector_search.py`

**Build a document search API:**
1. FastAPI + pgvector backend
2. Ingest 500+ text chunks (use Wikipedia articles or your own data)
3. Create both HNSW and IVFFlat indexes
4. Expose search endpoint: `POST /search {"query": "...", "k": 5, "index": "hnsw"}`
5. Benchmark endpoint:
   - recall@10 for both index types
   - p95 latency
   - throughput (requests/second)

**Done when:**
- Search returns relevant results with <100ms p95 latency
- You can articulate why you chose specific index parameters
- You have benchmark numbers comparing HNSW vs IVFFlat

---

## Skill Checkpoint

1. Explain HNSW's layered graph structure to someone who knows binary search but not vector search
2. What's the recall-latency trade-off when tuning `ef_search`? Draw the curve.
3. When would you choose IVFFlat over HNSW? Give a concrete scenario.
4. Your search returns irrelevant results. Walk through your debugging process: is it the embeddings, the index, or the data?
5. You have 50M documents. Design the vector search architecture.

---

## Core Resources

| Resource | Type | URL |
|----------|------|-----|
| pgvector GitHub | Library | https://github.com/pgvector/pgvector |
| MTEB Leaderboard | Benchmarks | https://huggingface.co/spaces/mteb/leaderboard |
| Pinecone learning center | Tutorials | https://www.pinecone.io/learn/ |
| FAISS wiki (Meta) | Deep dive | https://github.com/facebookresearch/faiss/wiki |

## Supplementary Resources
- Paper: "Efficient and Robust Approximate Nearest Neighbor Search" (original HNSW paper)
  https://arxiv.org/abs/1603.09320
- Ann-benchmarks (algorithm comparison): http://ann-benchmarks.com
- Vicki Boykis: "What are embeddings?" (excellent intuition builder)
  https://vickiboykis.com/what_are_embeddings/

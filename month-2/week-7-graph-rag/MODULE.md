# Week 7: Graph RAG & Production RAG Architecture

## Why This Matters
Vector search finds similar content but misses relationships. "Who reports to the CEO?" requires traversing org structure, not finding similar text. Graph RAG captures entities and their connections — when combined with vector search, you get the best of both worlds.

---

## Day-by-Day Plan

### Monday — Knowledge Graphs for RAG (1.5h)

**Read (1h):**
- Neo4j: RAG tutorial
  https://neo4j.com/blog/developer/rag-tutorial/

**Read (30 min):**
- Analytics Vidhya: GraphRAG guide
  https://www.analyticsvidhya.com/blog/2024/11/graphrag-with-neo4j/

**Setup:**
```bash
# Neo4j via Docker
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:5

# Python driver
pip install neo4j
```

**Why Graphs + Vectors:**
```
Vector Search:   "Tell me about Alice's projects"
                 → Finds chunks mentioning "Alice" and "projects"
                 → Might miss projects where Alice isn't mentioned by name

Graph Traversal: "Tell me about Alice's projects"
                 → MATCH (alice:Person {name: "Alice"})-[:WORKS_ON]->(p:Project)
                 → Returns ALL projects, even if Alice's name isn't in the description

Combined:        Best of both — use graph for structure, vectors for semantics
```

**Knowledge Graph Basics:**
```
(Entity)--[RELATIONSHIP]->(Entity)

(Alice:Person)--[:WORKS_ON]-->(Project_A:Project)
(Alice:Person)--[:REPORTS_TO]-->(Bob:Person)
(Project_A:Project)--[:USES]-->(Python:Technology)
(Bob:Person)--[:MANAGES]-->(Team_X:Team)
```

**Exercise:**
1. Start Neo4j, open browser at http://localhost:7474
2. Create a small knowledge graph (10 entities, 15 relationships)
3. Run Cypher queries: pattern matching, path finding, aggregation
4. Understand when graph queries give different answers than text search

---

### Tuesday — Build a GraphRAG Pipeline (1.5h)

**Follow (1.5h):**
- Neo4j GraphAcademy: Knowledge Graph RAG course
  https://graphacademy.neo4j.com/knowledge-graph-rag/
- neo4j-graphrag-python package
  https://github.com/neo4j/neo4j-graphrag-python

**The GraphRAG Pipeline:**
```
Documents → Entity Extraction (LLM) → Knowledge Graph Construction
                                              │
                                              ▼
                                    ┌──── Neo4j ────┐
                                    │ Entities       │
                                    │ Relationships  │
                                    │ Properties     │
                                    └───────┬───────┘
                                            │
Query → Intent Classification → ┌───────────┤
                                │ Factual → │ Graph Query (Cypher)
                                │ Semantic → │ Vector Search
                                │ Complex → │ Both + LLM synthesis
                                └───────────┘
```

**Entity Extraction Prompt (for building the graph):**
```
Given this text, extract entities and relationships.
Return as JSON:
{
  "entities": [{"name": "...", "type": "...", "properties": {...}}],
  "relationships": [{"source": "...", "target": "...", "type": "..."}]
}
```

**Exercise:**
1. Take 5 articles/documents
2. Use an LLM to extract entities and relationships
3. Load them into Neo4j
4. Build a query interface that accepts natural language
5. Use LLM to generate Cypher queries from natural language

---

### Wednesday — Microsoft GraphRAG Exploration (1.5h)

**Study (1h):**
- Microsoft GraphRAG repo
  https://github.com/microsoft/graphrag

**Run (30 min):**
- Quickstart on a sample dataset

**Microsoft's GraphRAG Pipeline:**
```
1. ENTITY EXTRACTION
   Documents → LLM extracts entities + relationships
   "Alice works at Contoso on Project X" →
     (Alice:Person), (Contoso:Company), (Project_X:Project)
     Alice-[:WORKS_AT]->Contoso, Alice-[:WORKS_ON]->Project_X

2. COMMUNITY DETECTION
   Use Leiden algorithm to find clusters of related entities
   Cluster 1: {Alice, Bob, Project_X} — "Core team"
   Cluster 2: {Contoso, FY2024, Budget} — "Company operations"

3. HIERARCHICAL SUMMARIZATION
   Summarize each community at multiple levels
   Level 0: Individual entity descriptions
   Level 1: Community summaries
   Level 2: Cross-community themes

4. SEARCH MODES
   LOCAL search: Start from specific entities, traverse nearby
   GLOBAL search: Query across all community summaries
```

**Local vs Global:**
- Local: "What does Alice work on?" → Find Alice entity → traverse relationships
- Global: "What are the main themes?" → Search community summaries

**Exercise:**
Run GraphRAG on a set of 10+ documents. Compare local vs global search results. Note when each mode gives better answers.

---

### Thursday — RAG Pipeline Architecture (1.5h)

**Read (1h):**
- LlamaIndex: Production RAG guide
  https://developers.llamaindex.ai/python/framework/optimizing/production_rag/

**Read (30 min):**
- Building production RAG systems architecture guide
  https://brlikhon.engineer/blog/building-production-rag-systems-in-2026-complete-architecture-guide

**Production RAG Architecture:**
```
┌─────────────────── INGESTION PIPELINE (async, batch) ──────────────────┐
│                                                                         │
│  Sources → Document Loader → Chunker → Embedder → Vector Store         │
│  (PDFs,     (unstructured,   (recursive,  (batched,   (pgvector,       │
│   APIs,      pdf2image)       semantic)    parallel)    with metadata)  │
│   DBs)                                                                  │
│                                                                         │
│  → Entity Extractor → Knowledge Graph (Neo4j, optional)                │
│  → Metadata Extractor → PostgreSQL (dates, authors, categories)        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────── QUERY PIPELINE (real-time) ─────────────────────────┐
│                                                                         │
│  Query → Semantic Cache Check                                           │
│           ├─ HIT → Return cached answer                                │
│           └─ MISS ↓                                                     │
│                                                                         │
│  Query Transformation (HyDE, multi-query, decomposition)               │
│           ↓                                                             │
│  Hybrid Retrieval (BM25 + Vector + Graph)                              │
│           ↓                                                             │
│  Reranking (cross-encoder)                                             │
│           ↓                                                             │
│  Context Assembly (dedup, order, truncate to fit context window)       │
│           ↓                                                             │
│  Generation (LLM with structured output)                               │
│           ↓                                                             │
│  Post-processing (citation extraction, confidence scoring)             │
│           ↓                                                             │
│  Cache Result → Return to User                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────── EVALUATION (continuous) ────────────────────────────┐
│  Ragas metrics, user feedback, latency monitoring, cost tracking       │
└─────────────────────────────────────────────────────────────────────────┘
```

**Exercise:**
Diagram YOUR production RAG system architecture. Be specific:
- Which embedding model? Why?
- Which vector DB? Why?
- What chunking strategy? Why?
- What retrieval pipeline? Why?

---

### Friday — LlamaIndex vs LangChain for RAG (1.5h)

**Read (45 min):**
- Galileo AI: LlamaIndex complete guide
  https://galileo.ai/blog/llamaindex-complete-guide-rag-data-workflows-llms

**Read (45 min):**
- Meilisearch: LlamaIndex RAG tutorial
  https://www.meilisearch.com/blog/llamaindex-rag

**When to use which:**

| Feature | LlamaIndex | LangChain |
|---------|------------|-----------|
| Focus | Data ingestion + retrieval | Agent orchestration + chains |
| RAG support | First-class, deeply optimized | Good but more generic |
| Agents | Supported | First-class (LangGraph) |
| Learning curve | Moderate | Steeper |
| Customization | Good for data pipelines | Better for complex workflows |
| Best for | RAG-focused applications | Agent-heavy applications |

**Recommendation for this plan:**
- Use LlamaIndex when building RAG pipelines (Months 2)
- Use LangGraph when building agents (Month 3)
- For production: you'll often use both (LlamaIndex for data, LangGraph for agents)

---

### Weekend — Graph + Vector Hybrid (1-2h)

**Build a query router:**
1. Extend your Week 5 vector search API with a Neo4j graph layer
2. Implement intent classification (is this a factual/relationship/semantic query?)
3. Route queries:
   - Factual/entity queries → Graph traversal
   - Semantic/similarity queries → Vector search
   - Complex queries → Both, then merge results
4. Test with 10 queries of each type

**Done when:** System correctly routes queries and returns more relevant results than vector-only search for relationship queries.

---

## Skill Checkpoint

1. When does GraphRAG outperform standard vector RAG? Give 3 examples.
2. Design an ingestion pipeline for a 10GB document corpus — chunking, embedding, indexing strategy.
3. How would you handle documents that update frequently? (Hint: incremental ingestion)
4. Your RAG system has great retrieval but poor answers. Where do you look?
5. Compare the cost of running Neo4j + pgvector vs a single vector database.

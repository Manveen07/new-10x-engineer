# Week 11 — Lock the docsight Stack + Postgres/pgvector in Docker Compose

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Weeks 9–10. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-3--rag-fundamentals--docsight-design-your-1-red-zone). Spec: [../PROJECTS.md](../PROJECTS.md#project-2--docsight-months-34).

**Window:** Mon 2026-08-03 → Sun 2026-08-09
**Time budget:** 8–10 hours
**Position:** Month 3, Week 11 of 24

## Why this week matters

docsight reuses the production scaffold you built once on leadlens (Docker, Modal, Langfuse, eval-CI) — that's the whole point of doing the simpler project first. This week you stand up the *new* piece: a real vector store. Postgres + pgvector in Docker Compose, retrieving end-to-end on your corpus, with BM25 alongside dense so hybrid is possible. No reranker yet — that's Month 4.

**The single must-do:** `docker compose up` brings up Postgres + pgvector, your corpus is ingested, and a query returns ranked chunks via both dense **and** BM25 — committed.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-08-03 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-08-04 | Read pgvector + Postgres FTS docs → recall: "how does pgvector index (HNSW vs IVFFlat)?" | 20 min |
| Wed eve | 2026-08-05 | **LeetCode ×1** | 20 min |
| Thu eve | 2026-08-06 | Skim a BM25 explainer → recall: "what does BM25 reward that cosine ignores?" | 20 min |
| Fri eve | 2026-08-07 | Rest or skim | 0–20 min |
| **Sat** | 2026-08-08 | **Big build**: Docker Compose (Postgres 16 + pgvector) → ingest corpus → dense retrieval working via SQL | **3.5 hrs** |
| **Sun** | 2026-08-09 | **Build**: add Postgres full-text (BM25-ish) retrieval path → confirm both return chunks for the same query → `git mv gtm-clay-rag docsight` → PROGRESS | **3 hrs** |

## Saturday — pgvector up (3.5 hrs)
- `docker-compose.yml`: Postgres 16 with the `pgvector` extension. A `chunks` table: `id, text, context_blurb, embedding vector(1024), tsv tsvector`.
- Ingestion script: chunk the corpus (recursive ~512-tok), generate contextual blurbs (from Week 9), embed with Voyage, insert. Build an HNSW index.
- A `retrieve_dense(query, k)` returning top-k by cosine. Verify on 3 queries.

## Sunday — BM25 path + rename (3 hrs)
- Add `retrieve_bm25(query, k)` using Postgres `tsvector`/`ts_rank` (or `pg_search` if you install it).
- Same query → both paths return results; eyeball where each wins (BM25 nails the exact API name dense missed in Week 9).
- `git mv projects/gtm-clay-rag projects/docsight`; update README header + any imports. Commit the rename separately.

## Behind if
- pgvector not retrieving end-to-end.
- Only one retrieval path (no BM25 → can't do hybrid in Month 4).
- Rename not done (docsight still named gtm-clay-rag).

## Next week
→ [week-12.md](./week-12.md): docsight `DESIGN.md` (eval plan first), open the OSS PR, blog post 3.

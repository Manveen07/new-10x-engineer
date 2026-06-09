# Week 13 — docsight: Ingestion + Contextual Retrieval + Hybrid (RRF) + 150 Eval Pairs

> 📝 **PROVISIONAL draft (2026-06-09, ~9 weeks early).** Refine the weekend before, anchored on the docsight DESIGN.md and what Month 3 actually stood up. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-4--ship-docsight-the-ablation-table--merge-oss-pr--mercor). Spec: [../PROJECTS.md](../PROJECTS.md#project-2--docsight-months-34).

**Window:** Mon 2026-08-17 → Sun 2026-08-23
**Time budget:** 8–10 hours
**Position:** Month 4, Week 13 of 24

## Why this week matters

The ablation table is docsight's headline artifact — and you can't build it without (a) all the retrieval variants wired and (b) a labeled eval set to measure them on. This week you build the variants (contextual + hybrid RRF on top of last month's dense + BM25) and generate the **150 synthetic query–chunk pairs** that every ablation row gets scored against. Jason Liu's trick: you can have an eval set on day one with zero hand labels — the LLM generates plausible queries from known chunks, you hand-verify a sample.

**The single must-do:** 150 query–chunk eval pairs committed + a hybrid (RRF) retriever returning results — by Sunday.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-08-17 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-08-18 | Read on Reciprocal Rank Fusion → recall: "how does RRF combine two ranked lists without score normalization?" | 20 min |
| Wed eve | 2026-08-19 | **LeetCode ×1** | 20 min |
| Thu eve | 2026-08-20 | Hand-verify 20 of the auto-generated eval pairs → tune the generation prompt | 30 min |
| Fri eve | 2026-08-21 | Rest or skim | 0–20 min |
| **Sat** | 2026-08-22 | **Big build**: contextual-retrieval preprocessing over the full corpus + hybrid retriever (dense + BM25 fused via RRF) | **3.5 hrs** |
| **Sun** | 2026-08-23 | **Build**: generate 150 query–chunk pairs (LLM-gen, hand-verify a sample) → commit `data/retrieval-eval.jsonl` → PROGRESS | **3.5 hrs** |

## Saturday — build the variants (3.5 hrs)
- Run contextual-retrieval preprocessing across the whole corpus (the per-chunk situating blurb from Month 3, now at scale). Re-embed.
- Implement `retrieve_hybrid(query, k)`: pull top-N from dense + top-N from BM25, fuse with RRF (`score = Σ 1/(k+rank)`, k≈60). This is the workhorse retriever the ablation measures.
- Sanity-check on the Week-9 exact-term query: hybrid should now catch what dense missed.

## Sunday — the eval set (3.5 hrs)
- For ~150 chunks, prompt an LLM: "write a question this chunk answers." Store `(query, gold_chunk_id)`.
- **Hand-verify ~20** — fix or drop the bad ones, tune the prompt, regenerate if needed. (Garbage eval pairs = a garbage ablation table.)
- Commit `data/retrieval-eval.jsonl`. This is the measuring stick for everything in Week 14.

## Behind if
- No 150-pair eval set (or unverified).
- Hybrid retriever not working.
- Contextual preprocessing not run on the full corpus.

## Next week
→ [week-14.md](./week-14.md): add the reranker, build the segmented ablation table (recall@10, MRR, NDCG@10).

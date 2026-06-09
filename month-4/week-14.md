# Week 14 — docsight: Reranker + The Ablation Table (Segmented)

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 13's eval set + retrievers. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-4--ship-docsight-the-ablation-table--merge-oss-pr--mercor).

**Window:** Mon 2026-08-24 → Sun 2026-08-30
**Time budget:** 8–10 hours
**Position:** Month 4, Week 14 of 24

## Why this week matters

This is **the** artifact. Hiring managers and Mercor reviewers screen for "did they actually measure retrieval, or `np.dot()` and call it RAG?" — the ablation table answers in 30 seconds. The deepest lesson lands here too: **segment, don't average.** A 70% overall recall can hide 40% recall on your hardest query type (exact API names, multi-hop). Report per-segment, not just the headline.

**The single must-do:** a committed ablation table with 5 rows × {recall@10, MRR, NDCG@10}, segmented by query type — by Sunday.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-08-24 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-08-25 | Read on cross-encoder reranking → recall: "why retrieve 20–50 then rerank to 5–10?" | 20 min |
| Wed eve | 2026-08-26 | **LeetCode ×1** | 20 min |
| Thu eve | 2026-08-27 | Tag each eval query with a segment (exact-term / conceptual / multi-hop) | 30 min |
| Fri eve | 2026-08-28 | Rest or skim | 0–20 min |
| **Sat** | 2026-08-29 | **Big build**: add reranker (Cohere Rerank 4 / Voyage Rerank 2.5 / zerank-2, or local bge for cheap) → write the metric harness (recall@k, MRR, NDCG@10) → run all 5 variants | **3.5 hrs** |
| **Sun** | 2026-08-30 | **Build**: segment the metrics, find where rerank *hurts* and why, write the ablation table + the one-paragraph reading of it → PROGRESS | **3.5 hrs** |

## Saturday — reranker + metric harness (3.5 hrs)
- Add `rerank(query, candidates)` (Cohere Rerank 4 / Voyage Rerank 2.5 / ZeroEntropy zerank-2 — current 2026 leaders — or a local `bge-reranker` for the cheap path). Pattern: retrieve 30 → rerank → top 10.
- Write the metric harness over `data/retrieval-eval.jsonl`: `recall@5/@10`, `MRR`, `NDCG@10`.
- Run all 5 variants: pure dense / BM25 / hybrid-RRF / hybrid+rerank / hybrid+rerank+contextual. Record every cell.

## Sunday — segment + interpret (3.5 hrs)
- Break each metric down by query segment. This is the senior move — look for the segment where the headline number lies.
- Find at least one case where **rerank hurt** (it happens on short exact-term queries) and explain why. A README that admits this reads as someone who measured, not marketed.
- Commit the ablation table (markdown + a chart PNG) + the one-paragraph interpretation.

## Behind if
- Ablation table missing rows or metrics.
- Only overall numbers (no segmentation).
- Can't explain when rerank hurts.

## Next week
→ `week-15.md`: cited generation + calibrated Ragas (faithfulness, answer-relevance, context-precision) + land the OSS PR.

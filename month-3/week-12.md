# Week 12 — docsight DESIGN.md (Eval-Plan-First) + Open the OSS PR + Blog Post 3

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 11 (what's actually retrieving). Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-3--rag-fundamentals--docsight-design-your-1-red-zone).

**Window:** Mon 2026-08-10 → Sun 2026-08-16
**Time budget:** 8–10 hours
**Position:** Month 3, Week 12 of 24 — **Month 3 ship week.**

## Why this week matters

You design the measurement before the pipeline (Hamel's rule) — the `DESIGN.md` you write this week is the spec the Month-4 ablation table fills in. And you open the OSS PR: Mercor's interview is *exclusively* your OSS contributions, so getting a real one in motion now (not Month 5) is the highest-leverage non-project move you make all plan.

**The single must-do:** docsight `DESIGN.md` committed (with the retrieval-eval plan) + an OSS PR opened (draft is fine) + blog post 3 published — by Sunday.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-08-10 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-08-11 | Draft docsight DESIGN §1–4 (problem, corpus, schema, retrieval paths) | 20 min |
| Wed eve | 2026-08-12 | Work the OSS issue locally (reproduce it, read the surrounding code) | 30 min |
| Thu eve | 2026-08-13 | **LeetCode ×1** + draft docsight DESIGN §5–7 (eval plan, metrics, deploy) | 30 min |
| Fri eve | 2026-08-14 | Outline blog post 3 OR rest | 15–30 min |
| **Sat** | 2026-08-15 | **Big build**: finish docsight `DESIGN.md` (eval-plan-first) + architecture diagram + push the OSS PR (tests + a useful change, not a typo fix) | **3.5 hrs** |
| **Sun** | 2026-08-16 | **Build**: write + publish blog post 3 "What I set up before writing a line of RAG code" + PROGRESS + Month-3 review | **3 hrs** |

## Saturday — DESIGN.md + OSS PR (3.5 hrs)
docsight `DESIGN.md` must contain, in this order (measurement first):
1. Problem + corpus (Anthropic SDK + LangGraph + LiteLLM docs/issues/changelogs — public, mixed prose/code).
2. **Retrieval-eval plan:** ~150 synthetic query–chunk pairs (LLM-gen, hand-verify a sample); metrics recall@5/@10, MRR, NDCG@10; the ablation rows (dense / BM25 / hybrid-RRF / +rerank / +contextual).
3. Generation-eval plan: Ragas faithfulness + answer-relevance + context-precision, calibrated vs ~30 hand labels.
4. Schema, retrieval paths, reranker choice, deploy (Modal + Docker + Langfuse), cost/latency targets.

OSS PR: push a real change to your chosen repo — a cookbook example using docsight/leadlens, an adapter, or a fix with tests. One PR with a maintainer thank-you > five drive-by typo fixes.

## Sunday — blog post 3 (3 hrs)
"What I set up before writing a line of RAG code" — the eval-plan-first discipline, the corpus choice and why, the ablation table you're *about* to fill. Publish on your domain + LinkedIn + X. Fill PROGRESS Month-3 review.

## Behind if
- No DESIGN.md, or it leads with pipeline instead of measurement.
- No OSS PR opened.
- Blog post 3 not published.
- Can't explain hybrid-beats-dense in 30 sec.

## Month 3 "done" bar
- [ ] pgvector retrieving end-to-end (dense + BM25).
- [ ] docsight `DESIGN.md` (eval-plan-first) committed; project renamed.
- [ ] OSS PR opened (Mercor asset in motion).
- [ ] Blog post 3 published.
- [ ] Can explain hybrid + contextual retrieval in 30 sec each.

## Next month
→ [../month-4/README.md](../month-4/README.md) — ship docsight (the ablation table) + merge OSS PR + apply to Mercor.

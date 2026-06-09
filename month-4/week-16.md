# Week 16 — docsight: Deploy + Blog Post 4 + Apply to Mercor

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 15's calibrated numbers (they go into the README + post + Mercor profile). Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-4--ship-docsight-the-ablation-table--merge-oss-pr--mercor).

**Window:** Mon 2026-09-07 → Sun 2026-09-13
**Time budget:** 8–10 hours
**Position:** Month 4, Week 16 of 24 — **Month 4 ship week + first major application.**

## Why this week matters

docsight goes live, and with a merged OSS PR + two deployed eval-backed projects, you now meet Mercor's bar — whose interview is *exclusively* your open-source contributions. This is the first week the portfolio starts doing the job-search work for you. Reuse the leadlens deploy scaffold wholesale (Docker + Modal + Langfuse + CI) — that's why you built it first.

**The single must-do:** docsight live at a public Modal URL with README to standard + Loom, blog post 4 published, **and the Mercor application submitted** — by Sunday.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-09-07 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-09-08 | Draft README "where it fails" (the rerank-hurts case from Week 14) | 20 min |
| Wed eve | 2026-09-09 | **LeetCode ×1** | 20 min |
| Thu eve | 2026-09-10 | Draft the Mercor profile (OSS PR front and center) | 30 min |
| Fri eve | 2026-09-11 | Outline blog post 4 OR rest | 15–30 min |
| **Sat** | 2026-09-12 | **Big build**: FastAPI + Docker + Modal deploy → live URL + $/query + p50/p95 from Langfuse + CI gate on retrieval metrics | **3.5 hrs** |
| **Sun** | 2026-09-13 | **Build**: README to standard + 3-min Loom + blog post 4 + **submit Mercor** + 5 HN/YC/Wellfound apps + Month-4 review | **4 hrs** |

## Saturday — deploy (3.5 hrs)
- FastAPI `POST /query` (question → cited answer + chunks). Docker. Modal deploy (load index/clients once at startup). Live URL, hit from incognito.
- Capture $/query + p50/p95 from Langfuse over a query set.
- CI gate: `pytest` fails the build if recall@10 on the eval set drops below the docsight threshold.

## Sunday — ship + apply (4 hrs)
- README to standard (7 portfolio questions): the ablation table is the centerpiece; "where it fails" names the rerank-hurts segment; Loom at top.
- Blog post 4: **"Contextual retrieval on real OSS docs — a measured ablation."** Show the table, name the corpus, share the failure case. Publish + cross-post.
- **Mercor application** with portfolio in hand (OSS PR is the headline). + 5 applications to HN/YC/Wellfound listings.
- Fill PROGRESS Month-4 review + Demo Day Loom. Advance [START_HERE.md](../START_HERE.md) pointer to Month 5 / Week 17.

## Behind if
- No live docsight URL; no ablation table in README.
- Ragas uncalibrated in the README claims.
- OSS PR not merged; Mercor application not submitted.
- No Loom; blog post 4 not published.

## Month 4 "done" bar
- [ ] docsight live at a public Modal URL.
- [ ] Segmented ablation table + calibrated Ragas in README.
- [ ] OSS PR **merged** (Mercor headline asset).
- [ ] Mercor application submitted + 5 other applications.
- [ ] 3-min Loom + blog post 4 published.

## Next month
→ [../month-5/README.md](../month-5/README.md) — reposcout (agent + MCP) + outbound funnel goes live.

# Week 10 — RAG Complexity + LlamaIndex/Pinecone Vocabulary Spikes

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 9. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-3--rag-fundamentals--docsight-design-your-1-red-zone).

**Window:** Mon 2026-07-27 → Sun 2026-08-02
**Time budget:** 8–10 hours (graduation month — weekends protected)
**Position:** Month 3, Week 10 of 24

## Why this week matters

You'll deploy pgvector for docsight, but JDs name LlamaIndex and Pinecone at almost every India RAG role — you need to *speak* to both without grinding them. This week: deepen the "when is RAG the wrong tool / how do I make it better" judgment (Jason Liu), then two 30-min vocabulary spikes so interviews don't catch you flat.

**The single must-do:** one LlamaIndex ingestion+query notebook and one Pinecone sandbox, each with a 3-line "what it's good at / when I'd skip it" note.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-07-27 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-07-28 | Read [Jason Liu — Systematically Improving RAG](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/) → 3 notes | 20 min |
| Wed eve | 2026-07-29 | **LlamaIndex spike** (30-min ingestion+query notebook) | 30 min |
| Thu eve | 2026-07-30 | **Pinecone spike** (30-min sandbox: upsert + query) | 30 min |
| Fri eve | 2026-07-31 | **LeetCode ×1** OR rest | 0–20 min |
| **Sat** | 2026-08-01 | **Big build**: RAG-vs-long-context experiment — same Qs via stuffed context vs retrieval; measure cost + answer quality; write the decision rule | **3.5 hrs** |
| **Sun** | 2026-08-02 | **Build**: start drafting the docsight retrieval-eval plan (what you'll measure) + OSS issue comment to open the conversation + PROGRESS | **3 hrs** |

## Saturday — the interview favorite: RAG vs long-context (3.5 hrs)
- Take 5 questions over your corpus. Answer each twice: (a) stuff the whole doc into context, (b) retrieve top-k. Compare cost, latency, answer quality.
- Write the decision rule in `notes/fundamentals.md`: when long-context wins (small corpus, cross-doc reasoning), when retrieval wins (large/changing corpus, cost, citations).

## Sunday — docsight eval plan + open the OSS conversation (3 hrs)
- Draft the *measurement* before the pipeline (Hamel's rule): which retrieval metrics (recall@k, MRR, NDCG@10), how you'll generate ~150 query-chunk pairs, what the ablation rows will be.
- On your chosen OSS repo: comment on the issue / open a draft PR to get maintainer feedback early. Low-stakes first contact.

## Behind if
- Can't say in 30 sec when you'd choose long-context over RAG.
- No LlamaIndex/Pinecone notes (interview gap stays open).
- No contact made on the OSS repo.

## Next week
→ [week-11.md](./week-11.md): stand up Postgres + pgvector in Docker Compose; lock the docsight stack.

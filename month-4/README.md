# Month 4 - Ship The GTM/Clay RAG System

## Goal

Build, measure, and deploy the Project 2 RAG system. The job-ready signal is the ablation table: you can show what dense retrieval, lexical retrieval, hybrid fusion, contextual retrieval, and reranking each contributed on your own data.

Canonical output by the end of the month:

- Deployed Project 2.
- Contextual retrieval implemented or explicitly replaced by a context-aware embedding option.
- Hybrid dense + lexical retrieval with RRF.
- Reranker path.
- About 150 synthetic query-chunk eval pairs.
- Ablation table with recall@10, MRR, and NDCG@10.
- Cited generation layer.
- Calibrated generation evals.
- Cost and latency analysis.
- Public post 4 published.
- Lightning-talk proposal submitted or scheduled.

Existing hardening/portfolio exercises in this folder remain useful support material, but Month 4 is now focused on shipping Project 2.

## Week Plan

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| 13 | 8h | Contextual retrieval, hybrid retrieval, synthetic query generation | retrieval pipeline and 150 query-chunk pairs |
| 14 | 8h | Reranking and ablation measurement | dense vs lexical vs hybrid vs hybrid+rerank table |
| 15 | 8h | Cited generation and generation eval calibration | faithfulness/relevance/context eval report |
| 16 | 8h | Modal deployment, Langfuse traces, cost analysis, public write-up | deployed Project 2 and post 4 |

## Build Requirements

- Ingestion CLI or job.
- Document/chunk storage in Postgres + pgvector.
- Dense retriever.
- Lexical retriever.
- RRF fusion.
- Reranker interface.
- `/search` endpoint or callable search function.
- `/answer` endpoint or callable answer function with citations.
- Langfuse traces for ingestion, retrieval, rerank, generation, and eval runs.
- Modal deployment or equivalent live URL.

## Eval Requirements

- About 150 synthetic query-chunk pairs.
- Retrieval metrics: recall@10/20, MRR, NDCG@10.
- Ablation table:
  - pure dense.
  - pure BM25/full-text.
  - hybrid RRF.
  - hybrid plus rerank.
- Generation metrics:
  - faithfulness.
  - answer relevance.
  - context precision.
- Calibration set of about 30 hand-labeled examples.
- README explains where metrics are weak or noisy.

## Monthly Checklist

- [ ] Contextual retrieval implemented or replacement justified.
- [ ] Dense retrieval works.
- [ ] Lexical retrieval works.
- [ ] RRF hybrid fusion works.
- [ ] 150 query-chunk pairs generated.
- [ ] Reranking works.
- [ ] Ablation table created.
- [ ] Cited generation works.
- [ ] Generation judges calibrated.
- [ ] Cost-per-query and latency p50/p95 measured.
- [ ] Deployment works.
- [ ] Langfuse traces linked or screenshotted.
- [ ] Post 4 published: "Contextual retrieval on Clay docs: a measured ablation."
- [ ] Lightning-talk proposal submitted or scheduled.

## Interview Skill Added

You should be able to answer "Design a doc Q&A system" with a concrete architecture, retrieval ablation results, calibration caveats, and operating-cost tradeoffs.

## Behind If

- The retrieval ablation table is missing.
- Ragas-style metrics are used without calibration.
- No talk has been proposed or scheduled.

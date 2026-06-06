# Month 4 — Ship docsight + Merge OSS PR + Apply to Mercor

## Goal

Build, evaluate, deploy docsight. Land the OSS PR. Apply to Mercor with portfolio in hand. By Sunday 2026-09-13 your GitHub profile shows two deployed projects with eval suites + one merged PR + a Mercor application in flight.

**Pace:** 8–10 hrs/week. Recovery month if Month 3 slipped due to exams.
**Window:** 2026-08-17 → 2026-09-13.

## Outcome by end of month

- `projects/docsight/` deployed on Modal at a public URL.
- Ingestion + chunking + contextual retrieval preprocessing.
- Hybrid retrieval (dense via Voyage + BM25 via Postgres FTS) with RRF.
- Reranker layer (Cohere or Voyage rerank, or local `bge-reranker` as cheap fallback).
- ~150 synthetic query-chunk eval pairs (hand-verified subset of 30).
- **Ablation table** in README: pure dense vs BM25 vs hybrid vs hybrid+rerank vs hybrid+rerank+contextual.
- Metrics: recall@5, recall@10, MRR, NDCG@10 per row.
- Cited generation. Ragas faithfulness + answer relevance + context precision, calibrated against 30 hand labels.
- Docker + Docker Compose for local dev. Modal deploy.
- $/query + p50/p95 latency in README.
- 3-min Loom walkthrough.
- Blog post 4 published: "Contextual retrieval on real OSS docs: a measured ablation."
- **OSS PR merged** (with maintainer thank-you screenshot for portfolio).
- **Mercor application submitted** at [work.mercor.com](https://work.mercor.com/).
- 5 HN/YC/Wellfound applications submitted.

## Week themes

| Week | Window | Theme |
|---|---|---|
| 13 | Aug 17 – Aug 23 | Ingestion + contextual retrieval prep + hybrid retrieval + 150 eval pairs |
| 14 | Aug 24 – Aug 30 | Reranker + ablation table + retrieval metrics |
| 15 | Aug 31 – Sep 6 | Cited generation + Ragas calibration + land OSS PR |
| 16 | Sep 7 – Sep 13 | Docker + Modal deploy + Loom + blog post 4 + Mercor + first apps |

Week files arrive ~3 days before each week.

## docsight corpus

Recommended: **Anthropic SDK docs + LangGraph docs + LiteLLM docs + their respective recent GitHub release notes + selected GitHub issues.** Why this corpus:
- Public, no auth needed.
- Mixes prose + code blocks + changelogs — tests contextual retrieval honestly.
- Demonstrates immediate utility — the deployed URL is something other engineers will actually use.
- Future employers are building with these stacks.

Alternative if you want a domain twist: a single OSS company's full docs (e.g. Modal, Replicate, Hugging Face). Pick by end of Week 12.

## Required reading carried into builds

- Contextual Retrieval (re-read with implementation open).
- Lost in the Middle (Liu et al. 2023) — figures only.
- Hamel on RAG evals.

## Monthly checklist

See [EXERCISES.md](../EXERCISES.md) Month 4 section.

## Interview skill added

You can **walk a hiring manager through your ablation table in 90 seconds** with specific numbers ("hybrid + rerank moved recall@10 from 67% to 89%; adding contextual retrieval added another 3 points but doubled ingestion cost; here's the cost vs quality trade-off chart"). This is the artifact that separates "I read about RAG" from "I shipped RAG."

## Behind if

- No deployment.
- No ablation table.
- Uncalibrated Ragas (using default prompts).
- OSS PR not merged.
- Mercor application not submitted.

## Next month

→ [../month-5/README.md](../month-5/README.md) — Ship reposcout (agent + MCP) + outbound funnel goes live.

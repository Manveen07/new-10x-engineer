# Week 22 — Funnel: System-Design Mocks + Project Deep-Dive + Keep the Volume

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on which interviews are actually landing. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-6--run-the-funnel-as-an-evaluation-problem). Track in [interview-tracker.md](./interview-tracker.md); drill [../interview_prep_qa.md](../interview_prep_qa.md).

**Window:** Mon 2026-10-19 → Sun 2026-10-25
**Time budget:** 8–10 hours
**Position:** Month 6, Week 22 of 24

## Why this week matters

First rounds are landing — now the bottleneck is interview fluency, not portfolio. The two things US AI-eng interviews test that you can rehearse: **system design** (doc-Q&A, classifier-with-handoff, eval-harness, MCP-server, agent — each whiteboardable in <10 min) and the **project deep-dive** (5 min on a real system you shipped, with the failure modes as the spine). You have real production-failure stories — F-003 hardcoded confidence, F-006 scam under-call, the 2/10 label-error discovery — which are the #1 differentiator.

**The single must-do:** 2 system-design mocks + 1 project deep-dive mock done (recorded or with a peer) + 10 more applications — by Sunday.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-10-19 | Plan review + drill [interview_prep_qa.md](../interview_prep_qa.md) Cluster (evals) to 🟢 | 30 min |
| Tue eve | 2026-10-20 | Drill RAG cluster + reply to all outbound/interview responses <24h | 30 min |
| Wed eve | 2026-10-21 | Apply to 5 listings; draft 6 STAR stories (the failure modes are the spine) | 30 min |
| Thu eve | 2026-10-22 | Drill agents + cost-modeling clusters; apply to 5 more | 30 min |
| Fri eve | 2026-10-23 | Cost-modeling reps (estimate a 10-turn agent loop live) OR rest | 15–30 min |
| **Sat** | 2026-10-24 | **Block**: 2 system-design mocks (doc-Q&A RAG; classifier-with-handoff) — whiteboard + record yourself, self-critique | **3.5 hrs** |
| **Sun** | 2026-10-25 | **Block**: 1 project deep-dive mock (leadlens or docsight, 5 min, no notes) + refine STAR stories + PROGRESS | **3 hrs** |

## Saturday — system-design mocks (3.5 hrs)
- Mock 1: "Design a doc-Q&A system" — talk through ingestion, chunking, hybrid retrieval, reranking, eval, cost. You built this (docsight); narrate it as design.
- Mock 2: "Design a classifier with human handoff" — leadlens shape: schema, judge, CI gate, confidence thresholds for handoff.
- Record both; watch back; cut the rambling. Cost-on-the-whiteboard is a screen — practice estimating $/request live.

## Sunday — project deep-dive (3 hrs)
- 5 min, no notes, on one project: problem → architecture → how you knew it was good → what failed and what you changed → cost/latency → what's next. Pull the artifacts on screen.
- Refine the 6 STAR stories so each lands in <90 sec.

## Behind if
- No recorded mocks (untested fluency).
- Can't cost a 10-turn agent loop on the spot.
- Stopped applying / replying (funnel stalls).

## Next week
→ `week-23.md`: paper-list skim, 50 more outbound (150 total), blog post 6.

# Month 1 — Code Rebuild + Eval Foundations + leadlens Design

## Goal

Two things at once:

1. **Rebuild Python fluency** that AI tools eroded — daily no-AI keyboard reps, modern stack (`uv` / `ruff` / `pytest`), threaded through every project block. By end of month you can write a Pydantic model + Instructor extraction + a test for it, without AI, in 10 minutes.
2. **Build the eval-first foundation** on your existing 50 staffing-firm classifier traces — open coding → axial coding → calibrated LLM-as-judge → design doc for **leadlens** (Project 1). This is the single highest-leverage portfolio skill in 2026.

Month 1 is not about shipping a large app. It's about earning the right to ship one in Month 2.

**Pace:** 8–10 hrs/week. Self-paced. Sunday `PROGRESS.md` updates are the only forcing function.

**Window:** 2026-05-25 → 2026-06-21.

## Outcome by end of month

- Daily no-AI 30-min coding kata habit (20+ sessions logged).
- Modern Python stack installed and used (`uv`, `ruff`, `pytest`, `pre-commit`).
- Personal portfolio site live at your domain.
- AsanaBot + PresentAI READMEs refreshed.
- All 50 traces open-coded with one-line notes (extends your existing Saturday-notes start).
- Failure taxonomy with 4–7 named categories. (Started on the 50 staffing-firm traces; after the JD pivot the live taxonomy is **F-003 hardcoded confidence, F-004 thin-stack extraction, F-006 scam under-call** — see `failure-taxonomy.md` + [DESIGN.md](../projects/business-classification-pipeline/DESIGN.md).)
- Lightweight annotation viewer (Streamlit or FastHTML).
- Calibrated LLM-as-judge prototype with >90% agreement against hand labels.
- leadlens design doc at `projects/business-classification-pipeline/DESIGN.md`.
- Blog post 1 published.

## Week files

Open the file for the week you're in. Don't skim ahead — each week's content adapts to what you learned last week.

> **The Month 1 close-out (Weeks 3–4) is driven by [FINISH-PLAN.md](./FINISH-PLAN.md).** It reconciles what's already shipped (you're ahead — fundamentals, patterns, DESIGN.md, judge v1 all done) and sequences the remaining work: `failure-taxonomy.md` → judge TNR ≥0.90 → blog post 1. The `week-3.md` / `week-4.md` files are kept for kata + code detail only.

| Week | File | Window | Outcome |
|---|---|---|---|
| 1 | [week-1.md](./week-1.md) | 2026-05-25 → 2026-05-31 | No-AI rebuild + portfolio site live + AsanaBot/PresentAI READMEs refreshed |
| 2 | [week-2.md](./week-2.md) | 2026-06-01 → 2026-06-07 | All 50 traces open-coded with Three Gulfs + annotation viewer running |
| 3 | [week-3.md](./week-3.md) | 2026-06-08 → 2026-06-14 | Axial taxonomy + first LLM-as-judge + first iteration to >85% agreement |
| 4 | [week-4.md](./week-4.md) | 2026-06-15 → 2026-06-21 | Judge calibrated to >90% + leadlens DESIGN.md + blog post 1 published |

## leadlens DESIGN.md — committed; the canonical spec

✅ **Already written** (post-JD-pivot): [projects/business-classification-pipeline/DESIGN.md](../projects/business-classification-pipeline/DESIGN.md). leadlens classifies an **AI-engineering job description**, not a company. Summary of what it contains:

- **Input contract:** one JD per record (`title`, `company`, `url`, `location`, `description`).
- **Output schema** (Pydantic): `seniority`, `ai_authenticity` (real_ai_role / ai_adjacent / ai_washed / non_ai), `core_stack` + `stack_unspecified`, `remote_status`, `comp_signal`, `red_flags`, `confidence_reasoning` (min_length=100), `fit_for_manveen`. Each field exists because it's measurable and/or forces a dimension a failure mode hides in (schema-as-eval-spec).
- **Eval:** category accuracy vs `expected_category` (CI gate ≥75%) + a calibrated scam judge (critique-shadowing, TPR/TNR — TPR 1.0 / TNR ≥0.90).
- **Failure taxonomy:** F-003 hardcoded confidence, F-004 thin-stack extraction, F-006 scam under-call.
- **Deployment + observability:** Gemini 2.5 Flash + Instructor; Modal + Langfuse; cost ~$0.00085/JD; latency target from p50/p95.

## Interactivity rules for this month

- **Read+Drill pairs:** every reading triggers one 30-min build. No reading allowed without a build chaser. Examples:
  - Read Hamel `llm-judge` → write a 20-line LLM judge in a notebook the same evening.
  - Read Eugene Yan on critique shadowing → run it on 3 traces immediately.
- **Daily no-AI 30 min:** before any AI-paired session, do a no-AI warm-up. See [START_HERE.md](../START_HERE.md) for the rotation.
- **Sunday log is non-negotiable.** Even a 5-line update beats silence.

## Interview skill added by end of month

You should be able to answer **"How do you build an eval?"** in three concise sentences using your own classifier as the example:

> "I open-coded real classifier traces by hand and named the recurring failure modes — hardcoded confidence, thin extraction, under-called scams — then killed each *by construction* with a schema field (e.g. a `min_length=100` reasoning field so the model can't emit a default confidence), and built a critique-shadowing scam judge calibrated on TPR/TNR (TPR 1.0, TNR ≥0.90) that runs in CI."

If you can say that fluently and pull up the artifacts on screen, that's a senior-junior signal in 60 seconds.

## Behind if

- Fewer than 15 no-AI katas logged.
- Portfolio site not live by end of Week 1.
- Fewer than 50 traces open-coded by end of Week 2.
- Judge agreement <85% by end of Week 4.
- Blog post 1 not published by 2026-06-21.
- Two consecutive Sunday `PROGRESS.md` updates missed.

## Next month

→ [../month-2/README.md](../month-2/README.md) — Ship leadlens: turn the design + judge into a deployed classifier with 100-example golden dataset, Loom walkthrough, blog post 2.

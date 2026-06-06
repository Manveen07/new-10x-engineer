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
- Failure taxonomy with 4–7 named categories (you already have 3 — `false executive-search signal`, `mixed-boundary ambiguity`, `schema drift` — extend).
- Lightweight annotation viewer (Streamlit or FastHTML).
- Calibrated LLM-as-judge prototype with >90% agreement against hand labels.
- leadlens design doc at `projects/business-classification-pipeline/DESIGN.md`.
- Blog post 1 published.

## Week files

Open the file for the week you're in. Don't skim ahead — each week's content adapts to what you learned last week.

| Week | File | Window | Outcome |
|---|---|---|---|
| 1 | [week-1.md](./week-1.md) | 2026-05-25 → 2026-05-31 | No-AI rebuild + portfolio site live + AsanaBot/PresentAI READMEs refreshed |
| 2 | [week-2.md](./week-2.md) | 2026-06-01 → 2026-06-07 | All 50 traces open-coded with Three Gulfs + annotation viewer running |
| 3 | [week-3.md](./week-3.md) | 2026-06-08 → 2026-06-14 | Axial taxonomy + first LLM-as-judge + first iteration to >85% agreement |
| 4 | [week-4.md](./week-4.md) | 2026-06-15 → 2026-06-21 | Judge calibrated to >90% + leadlens DESIGN.md + blog post 1 published |

## leadlens DESIGN.md — what it must contain by end of Week 4

- **Input contract:** company name, domain, optional location.
- **Output schema** (Pydantic, nested): operating status, segment (e.g. `executive_search` / `general_staffing` / `mixed`), signals[] with evidence + confidence, citations[].
- **Retrieval/evidence path:** web search (Tavily or Google CSE), Maps lookups, prior known data — fallback chain if primary fails.
- **Golden dataset plan:** how you'll hand-label 100 companies in Month 2 (sourcing, ambiguity sampling, label rubric).
- **Eval dimensions:** segment correctness, signal correctness, evidence support quality, confidence calibration.
- **Judge plan:** binary judge per dimension, critique shadowing pattern, agreement target >90%.
- **Failure taxonomy reference:** link to `failure-taxonomy.md`.
- **Deployment target + observability:** Modal + Langfuse + cost target + p50/p95 target.

Location: [projects/business-classification-pipeline/DESIGN.md](../projects/business-classification-pipeline/) (create file in Week 4).

## Interactivity rules for this month

- **Read+Drill pairs:** every reading triggers one 30-min build. No reading allowed without a build chaser. Examples:
  - Read Hamel `llm-judge` → write a 20-line LLM judge in a notebook the same evening.
  - Read Eugene Yan on critique shadowing → run it on 3 traces immediately.
- **Daily no-AI 30 min:** before any AI-paired session, do a no-AI warm-up. See [START_HERE.md](../START_HERE.md) for the rotation.
- **Sunday log is non-negotiable.** Even a 5-line update beats silence.

## Interview skill added by end of month

You should be able to answer **"How do you build an eval?"** in three concise sentences using your own classifier as the example:

> "Pulled 50 real traces from my staffing-firm classifier, open-coded them by hand to discover three failure modes — false executive-search signal, mixed-boundary ambiguity, schema drift — then built a binary LLM-as-judge with critique shadowing and iterated the prompt three times until it agreed with my hand labels at 92%. The judge then runs in CI."

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

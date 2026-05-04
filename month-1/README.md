# Month 1 - Evals Foundations And Project 1 Design

## Goal

Build the eval-first foundation for the six-month roadmap. Month 1 is not about shipping a large app. It is about learning how to look at LLM outputs rigorously, turning real classifier traces into a failure taxonomy, and designing Project 1 before implementation pressure starts.

**Path:** self-paced from the free Hamel/Shreya canon (no Maven cohort). Sunday `PROGRESS.md` updates are the only forcing function. Do not skip them.

Window: 2026-05-04 to 2026-05-31.

Canonical output by the end of the month:

- 50 real classifier traces reviewed with open-coding notes.
- Failure taxonomy for the winery/HVAC-style classifier work.
- Lightweight annotation viewer or annotation workflow.
- Calibrated LLM-as-judge prototype on a sample of the 50 traces.
- Project 1 design doc.
- Personal site or portfolio repo live.
- Public post 1 published.

Existing `week-*`, `exercises/`, and `capstone/` material in this folder is reusable drill material from the older backend plan. Use it only when it helps the monthly outcome.

## Week Plan

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| 1 | 8h | Set up portfolio repo/site (Quarto or Astro), read Hamel `evals-faq`, pull 50 real classifier traces, repackage one old Clay/winery script with `uv`, `ruff`, `pytest`, and Pydantic models | portfolio shell live, traces dumped, Python tooling reboot |
| 2 | 8h | Apply Three Gulfs framework, open-code the 50 traces, read Eugene Yan LLM patterns | open-coding notes |
| 3 | 8h | Open coding to axial coding, failure taxonomy, build annotation viewer, read Hamel `llm-judge` | taxonomy and annotation workflow |
| 4 | 8h | LLM-as-judge calibration with critique shadowing on a trace sample, Project 1 design doc, draft post 1 | design doc and post draft |

## Daily Plan — Week 1 (May 4 to May 10)

Day 0 prereqs from `MASTER_PLAN.md` are folded in. Order is flexible, but keep prereqs (Mon-Wed) before the trace-pulling and Saturday reading.

| Day | Date | Task | Time |
|---|---|---|---|
| Mon | 2026-05-04 | Modal hello world deployed at a public URL | 30 min |
| Mon | 2026-05-04 | Langfuse free cloud account, API keys saved | 15 min |
| Tue | 2026-05-05 | Pydantic + Instructor speedrun: nested `Company` extraction in a notebook | 90 min |
| Wed | 2026-05-06 | Confirm GitHub repo public; buy personal domain if needed; install `uv` and `ruff` | 45 min |
| Thu | 2026-05-07 | Pull 50 real classifier traces into `notes/traces-week-1.md` (or `.jsonl`) | 90 min |
| Thu | 2026-05-07 | Repackage one old Clay/winery script: `uv` venv, `ruff` lint, one `pytest` test, Pydantic input/output models | 60 min |
| Fri | 2026-05-08 | Pick Quarto or Astro in 30 min; deploy one-page portfolio site to your domain | 2 hrs |
| Sat | 2026-05-09 | Read Hamel `evals-faq` + Eugene Yan LLM patterns, with traces open in another tab; jot 10 failure-mode notes | 2.5 hrs |
| Sun | 2026-05-10 | Update `PROGRESS.md` (honest hours, what shipped, what slipped, Week 2 plan) | 30 min |

Total: ~8 hours. If a task overruns 2x its budget, stop and log it in `PROGRESS.md` instead of pushing through.

## Daily Plan — Weeks 2 to 4

Daily breakdowns for Weeks 2 to 4 will be added at each Sunday review when planning the upcoming week. Keep the Week column above as your guide until then.

## Project 1 Design Requirements

The design doc should define:

- Input contract: company name, domain, optional location/context.
- Output schema: operating status, ICP fit, sub-segment, signals, confidence, citations.
- Retrieval/evidence path: web, Maps-style sources, prior data where available.
- Golden dataset plan: 100 companies across pass/fail/edge cases.
- Eval dimensions: operating status correctness, ICP-fit correctness, evidence support, confidence calibration.
- Judge plan: binary judge checks, critique shadowing, agreement target above 90%.
- Failure taxonomy from the 50 reviewed traces.
- Deployment target and observability plan.

Suggested location: `projects/business-classification-pipeline/docs/design.md`.

## Monthly Checklist

- [ ] Hamel `evals-faq`, Eugene Yan LLM patterns, and Hamel `llm-judge` posts read.
- [ ] Portfolio site or repo is live.
- [ ] One old Clay/winery script repackaged with `uv`, `ruff`, `pytest`, and Pydantic models.
- [ ] 50 traces reviewed.
- [ ] Open-coding notes committed or summarized.
- [ ] Failure taxonomy created.
- [ ] Annotation viewer/workflow exists.
- [ ] LLM-as-judge calibrated to >90% agreement on a trace sample.
- [ ] Project 1 design doc exists.
- [ ] Post 1 published: "Open coding 50 LLM traces from a real classification pipeline."
- [ ] `PROGRESS.md` updated every Sunday.

## Interview Skill Added

By the end of this month, you should be able to answer "How do you build an eval?" in three concise sentences using a real classifier example.

## Behind If

- You have reviewed fewer than 50 traces.
- You do not have a portfolio site or public repo live.
- You have missed two consecutive Sunday `PROGRESS.md` updates.

# Month 1 — Evals Foundations and Project 1 Design

## Goal

Build the eval-first foundation for the six-month roadmap. Month 1 is not about shipping a large app. It is about learning how to look at LLM outputs rigorously, turning real classifier traces into a failure taxonomy, and designing Project 1 before implementation pressure starts.

**Path:** self-paced from the free Hamel/Shreya canon (no Maven cohort). Sunday `PROGRESS.md` updates are the only forcing function. Do not skip them.

**Window:** 2026-05-04 to 2026-05-31.

## Outcome by end of month

- 50 real classifier traces reviewed with open-coding notes.
- Failure taxonomy for the winery/HVAC-style classifier work.
- Lightweight annotation viewer.
- Calibrated LLM-as-judge prototype with >90% agreement against hand labels.
- Project 1 design doc at `projects/business-classification-pipeline/docs/design.md`.
- Personal portfolio site live.
- Public blog post 1 published.

## Week Files

Each week has its own daily plan, deliverable checklist, and "behind if" markers. Open the file for the week you are in.

| Week | File | Window | Outcome |
|---|---|---|---|
| 1 | [week-1.md](./week-1.md) | 2026-05-04 → 2026-05-10 | Tooling done, 50 traces pulled, portfolio site live |
| 2 | [week-2.md](./week-2.md) | 2026-05-11 → 2026-05-17 | All 50 traces open-coded with Three Gulfs |
| 3 | [week-3.md](./week-3.md) | 2026-05-18 → 2026-05-24 | Failure taxonomy + annotation viewer + 50 traces tagged |
| 4 | [week-4.md](./week-4.md) | 2026-05-25 → 2026-05-31 | LLM-as-judge >90% agreement, Project 1 design doc, blog post 1 published |

## Project 1 Design Doc — Required Sections

By end of Week 4 the design doc must define:

- Input contract: company name, domain, optional location.
- Output schema (Pydantic): operating status, ICP fit, sub-segment, signals, confidence, citations.
- Retrieval/evidence path: web search, Maps-style sources, prior data.
- Golden dataset plan: 100 companies across pass/fail/edge cases (built in Month 2).
- Eval dimensions: status correctness, ICP-fit correctness, evidence support, confidence calibration.
- Judge plan: binary judge checks, critique shadowing, agreement target above 90%.
- Failure taxonomy reference: link to `failure-taxonomy.md`.
- Deployment target and observability plan.

Location: [projects/business-classification-pipeline/docs/design.md](../projects/business-classification-pipeline/docs/design.md).

## Monthly Checklist

- [ ] Hamel `evals-faq`, Eugene Yan LLM patterns, and Hamel `llm-judge` posts read.
- [ ] Portfolio site live at your domain.
- [ ] 50 traces pulled and committed under `projects/business-classification-pipeline/data/`.
- [ ] All 50 traces open-coded with one-line notes.
- [ ] Failure taxonomy with 4–7 named categories at `projects/business-classification-pipeline/docs/failure-taxonomy.md`.
- [ ] Annotation viewer (Streamlit or FastHTML) runs locally.
- [ ] All 50 traces tagged with a taxonomy category.
- [ ] LLM-as-judge agreement >90% with hand labels after ≥3 prompt iterations.
- [ ] Judge iteration log committed.
- [ ] Project 1 design doc complete.
- [ ] Blog post 1 published: "Open coding 50 LLM traces from a real classification pipeline."
- [ ] LinkedIn cross-post made.
- [ ] `PROGRESS.md` updated every Sunday + monthly review filled.

## Interview Skill Added

By end of month, you should be able to answer **"How do you build an eval?"** in three concise sentences using your own classifier as the example: pull 50 real traces, open-code them, cluster into a taxonomy, build a critique-shadowed LLM judge, calibrate to >90% agreement.

## Behind If

- Fewer than 50 traces have been reviewed.
- Portfolio site is not live.
- Two consecutive Sunday `PROGRESS.md` updates have been missed.
- Blog post 1 is not published by 2026-05-31.

## Next month

→ [../month-2/README.md](../month-2/README.md) — Project 1 ship: convert eval discipline into a deployed classification pipeline with a 100-example golden dataset.

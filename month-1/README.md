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
| 1 | 8h | Set up portfolio repo/site (Quarto or Astro), read Hamel `evals-faq`, pull 50 real classifier traces | portfolio shell live, traces dumped |
| 2 | 8h | Apply Three Gulfs framework, open-code the 50 traces, read Eugene Yan LLM patterns | open-coding notes |
| 3 | 8h | Open coding to axial coding, failure taxonomy, build annotation viewer, read Hamel `llm-judge` | taxonomy and annotation workflow |
| 4 | 8h | LLM-as-judge calibration with critique shadowing on a trace sample, Project 1 design doc, draft post 1 | design doc and post draft |

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

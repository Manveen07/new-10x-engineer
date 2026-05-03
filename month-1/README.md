# Month 1 - Evals Foundations And Project 1 Design

## Goal

Build the eval-first foundation for the six-month roadmap. Month 1 is not about shipping a large app. It is about learning how to look at LLM outputs rigorously, turning real classifier traces into a failure taxonomy, and designing Project 1 before implementation pressure starts.

Canonical output by the end of the month:

- Maven AI Evals enrollment and Week 1-3 work completed.
- 50 real classifier traces reviewed with open-coding notes.
- Failure taxonomy for the winery/HVAC-style classifier work.
- Lightweight annotation viewer or annotation workflow.
- Project 1 design doc.
- Personal site or portfolio repo live.
- Public post 1 published.

Existing `week-*`, `exercises/`, and `capstone/` material in this folder is reusable drill material from the older backend plan. Use it only when it helps the monthly outcome.

## Week Plan

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| 1 | 8h | Enroll in Maven AI Evals, set up portfolio repo/site, skim Chip Huyen Ch. 1-2 if needed | portfolio shell and course plan |
| 2 | 8h | Maven Week 1, Three Gulfs framework, review 50 traces | open-coding notes |
| 3 | 8h | Maven Week 2, open coding to axial coding, failure taxonomy | taxonomy and annotation workflow |
| 4 | 8h | Maven Week 3, LLM-as-judge calibration, critique shadowing, Project 1 design | design doc and post draft |

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

- [ ] Maven AI Evals enrollment completed.
- [ ] Portfolio site or repo is live.
- [ ] 50 traces reviewed.
- [ ] Open-coding notes committed or summarized.
- [ ] Failure taxonomy created.
- [ ] Annotation viewer/workflow exists.
- [ ] Project 1 design doc exists.
- [ ] Post 1 published: "Open coding 50 LLM traces from a real classification pipeline."
- [ ] `PROGRESS.md` updated every Sunday.

## Interview Skill Added

By the end of this month, you should be able to answer "How do you build an eval?" in three concise sentences using a real classifier example.

## Behind If

- You have not enrolled in the Maven cohort.
- You have reviewed fewer than 50 traces.
- You do not have a portfolio site or public repo live.

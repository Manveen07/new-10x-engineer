# Month 2 - Ship The Business Classification Pipeline

## Goal

Convert Month 1 eval work into a deployed, defensible project. The deliverable is not a prompt demo; it is a classification pipeline with structured outputs, a golden dataset, calibrated judge checks, traces, and honest failure-mode documentation.

Canonical output by the end of the month:

- Project 1 deployed.
- 100-company hand-labeled golden dataset.
- Pydantic schema and structured-output pipeline.
- LLM-as-judge checks calibrated against labels.
- Confusion matrix.
- Cost and latency analysis.
- README to the common project standard.
- Public post 2 published.

Existing RAG exercises in this folder are useful later, but Month 2 is now focused on Project 1.

## Week Plan

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| 5 | 8h | Maven Week 4, synthetic data, RAG/agent evals, CI/CD integration | course homework patterns folded into Project 1 |
| 6 | 8h | Schema design, Instructor structured outputs, Langfuse instrumentation, label collection | working classifier skeleton and 100 labels |
| 7 | 8h | Judge calibration, critique shadowing, confusion matrix, failure fixes | eval harness with more than 90% judge agreement target |
| 8 | 8h | Modal deployment, README, architecture diagram, iteration log, post | deployed Project 1 and blog post 2 |

## Build Requirements

- Python package with repeatable local setup.
- Pydantic schema for classification output.
- Provider boundary for OpenAI/Anthropic or mock mode.
- Evidence collection path with source/citation fields.
- Langfuse tracing around retrieval, model calls, judge calls, and final decisions.
- Tests that run without live LLM calls.
- Deployment path on Modal or equivalent.

## Eval Requirements

- 100 hand-labeled companies.
- Mix of clear pass, clear fail, ambiguous, stale-web, multilingual, and name-collision cases.
- Binary pass/fail judge checks per major dimension.
- Critique-shadowing examples in the judge prompt.
- Judge prompt iteration log.
- Confusion matrix in README.
- "Where it fails" section tied to observed examples.

## Monthly Checklist

- [ ] Project 1 package scaffolded.
- [ ] Structured output schema implemented.
- [ ] Mock provider path exists.
- [ ] Evidence/citation fields implemented.
- [ ] Langfuse trace points added.
- [ ] 100-company golden dataset committed.
- [ ] Judge checks implemented.
- [ ] Judge prompt iterated at least three times.
- [ ] Confusion matrix created.
- [ ] Cost-per-call and latency p50/p95 measured.
- [ ] Deployment works.
- [ ] README meets project standard.
- [ ] Post 2 published: "Auditing my own classifier."

## Interview Skill Added

You should be able to walk through one full eval-first LLM project end to end: data, labels, failure taxonomy, judge calibration, fixes, deployment, and operating cost.

## Behind If

- Project 1 is only a localhost demo.
- The 100-example golden dataset is missing.
- Fewer than two public posts exist.

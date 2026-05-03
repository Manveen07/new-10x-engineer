# ICP Research Agent

Timeline: Month 5.

## Problem

Given a natural-language ICP, produce a ranked, enriched, validated company list with confidence scores and evidence.

Example:

```text
HVAC distributors in Texas with more than 50 employees doing residential work.
```

## Build Standard

- Workflow-first orchestration.
- Raw Python unless a framework becomes clearly necessary.
- Pydantic tool I/O.
- Search, Maps-style lookup, enrichment API, and LLM judge tools.
- Step budget capped at 20.
- Idempotency tokens for tool calls.
- Langfuse traces.
- Modal deployment.

## Eval Standard

- 30 reference ICPs.
- Golden expected tool paths.
- Trajectory judge.
- Final-output precision/recall.
- State-transition matrix.
- Cost/task, steps/task, and escalation rate.

## README Sections To Fill

- Workflow vs agent boundary.
- Tool registry.
- Safety and approval policy.
- Trajectory evals.
- Final-output evals.
- Cost and latency.
- Where it fails.
- Deployment.

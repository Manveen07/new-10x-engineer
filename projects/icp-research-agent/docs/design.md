# Project 3 Design - ICP Research Agent

Status: draft.

## Objective

Given a natural-language ICP, produce a ranked, enriched, validated company list with evidence, confidence scores, and bounded tool use.

## Workflow-First Boundary

Default to deterministic workflow steps:

1. Parse ICP into structured criteria.
2. Generate search queries.
3. Retrieve candidate companies.
4. Enrich candidates.
5. Validate candidates against criteria.
6. Rank candidates.
7. Produce final result with evidence.

The only agentic node should be the search-and-validate step if the next action genuinely depends on returned evidence.

## Input Schema

- `icp_description`.
- `geography`.
- `industry`.
- `employee_range`.
- `required_signals`.
- `excluded_signals`.
- `max_results`.

## Tool Registry

Planned tools:

- Web search.
- Maps/business lookup.
- Enrichment provider.
- Website evidence extraction.
- LLM validation judge.

Every tool needs:

- Input schema.
- Output schema.
- Risk level.
- Timeout.
- Retry policy.
- Idempotency key.

## Controls

- Step budget capped at 20.
- Stop conditions for enough evidence, low confidence, duplicate candidates, and repeated failed tools.
- Tool output validation on every call.
- No high-risk write actions without approval.
- Taint/safety notes for attacker-controlled web content.

## Eval Plan

Trajectory evals:

- 30 reference ICPs.
- Golden expected tool paths.
- Trajectory judge prompt.
- State-transition matrix.

Final-output evals:

- Precision and recall where a labeled company set exists.
- Evidence support.
- Ranking reasonableness.
- Escalation/uncertainty correctness.

Operating metrics:

- Cost/task.
- Steps/task.
- Tool failure rate.
- Escalation rate.
- Latency p50/p95.

## Deployment

Target: Modal API or job endpoint.

README must include architecture, workflow vs agent boundary, eval results, state-transition matrix, cost/task, latency, and failure modes.

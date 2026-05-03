# Month 5 - ICP Research Agent And Portfolio Polish

## Goal

Build Project 3: an ICP research agent that starts as a deterministic workflow and adds agentic behavior only where the next action genuinely depends on returned evidence. The deliverable must be bounded, observable, testable, and deployable.

Canonical output by the end of the month:

- Deployed ICP research agent.
- Workflow-first design document.
- Typed tool I/O with Pydantic.
- Step budget capped at 20.
- Idempotency tokens for tool calls.
- 30 golden ICP trajectories.
- Trajectory judge and state-transition matrix.
- Final-output precision/recall evals.
- All three project READMEs polished.
- LinkedIn and portfolio site updated.
- Public post 5 published.

## Week Plan

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| 17 | 8h | Read Anthropic agent guidance and context engineering. Sketch workflow-first design. | design doc and agent boundary decision |
| 18 | 8h | Build raw orchestration, typed tools, step budget, idempotency tokens | working ICP research workflow/agent |
| 19 | 8h | Add trajectory evals, golden paths, trajectory judge, state-transition matrix | eval harness and dashboard/report |
| 20 | 8h | Deploy, write up, polish all project READMEs, update LinkedIn/portfolio | deployed Project 3 and post 5 |

## Project 3 Design Requirements

The design doc should define:

- ICP input schema.
- Workflow steps that are deterministic.
- The specific node where agentic search/validation is justified.
- Tool registry and risk levels.
- Step budget and stop conditions.
- Idempotency token strategy.
- Evidence and confidence model.
- Taint/safety assumptions for web content.
- Trajectory eval methodology.
- Final-output eval methodology.

Suggested location: `projects/icp-research-agent/docs/design.md`.

## Build Requirements

- Raw Python orchestration by default.
- Pydantic schemas for ICP input, tool calls, tool outputs, and final result.
- Tool validation on every output.
- Search, Maps-style lookup, enrichment, and judge tools behind interfaces.
- Step budget capped at 20.
- Structured traces for each run and tool call.
- Deployment on Modal or equivalent.

## Eval Requirements

- 30 reference ICPs.
- Golden path of expected tool calls for each reference ICP.
- LLM-as-judge for trajectory accuracy.
- Precision/recall on final company list where labels exist.
- State-transition matrix.
- Cost/task, steps/task, and escalation rate.

## Monthly Checklist

- [ ] Anthropic agent guidance read.
- [ ] Workflow-first design doc written.
- [ ] Agentic node justified.
- [ ] Tool registry implemented.
- [ ] Step budget implemented.
- [ ] Idempotency tokens implemented.
- [ ] Tool output validation implemented.
- [ ] 30 golden ICP trajectories created.
- [ ] Trajectory judge implemented.
- [ ] State-transition matrix/report created.
- [ ] Final-output evals implemented.
- [ ] Deployment works.
- [ ] All three project READMEs polished.
- [ ] LinkedIn headline/About updated.
- [ ] Portfolio site updated.
- [ ] Post 5 published: "Workflows beat agents until they do not: a step-budgeted ICP researcher."

## Interview Skill Added

You should be able to explain workflow vs agent, step budgets, tool surface area, idempotency, trajectory evals, and why the system does not have unbounded autonomy.

## Behind If

- A framework was used without being able to explain the underlying SDK calls.
- You cannot explain workflow vs agent in 30 seconds.
- The three projects do not read as one coherent portfolio.

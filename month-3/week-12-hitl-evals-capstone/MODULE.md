# Week 12: HITL, Evaluation, Red Teaming, And Capstone

## Outcome

Ship the Month 3 capstone: a controlled agentic RAG system with human approval gates, task evals, red-team tests, traces, and a recruiter-readable README.

## Day 56: HITL Approvals

Exercise: `../exercises/day56_hitl_approvals.md`

Build:

- approval request schema.
- approve/reject decision.
- pause/resume graph state.
- audit trail.

## Day 57: Agent Eval Set

Exercise: `../exercises/day57_agent_eval_set.md`

Build:

- 25 task cases.
- expected tools.
- expected citation behavior.
- unsafe tasks that require refusal or approval.

## Day 58: Agent Metrics

Exercise: `../exercises/day58_agent_metrics.py`

Implement:

- task success.
- tool-call accuracy.
- groundedness.
- approval precision.
- cost and latency.

## Day 59: Red-Team Tests

Exercise: `../exercises/day59_red_team_tests.md`

Test:

- prompt injection in retrieved context.
- tool misuse.
- tenant data leakage.
- approval bypass attempts.

## Day 60: Capstone Polish

Exercise: `../capstone/CAPSTONE.md`

Finish:

- README.
- ADRs.
- demo script.
- eval report.
- trace screenshots/examples.

## Week 12 Acceptance Gate

- [ ] risky actions pause for approval.
- [ ] eval suite runs.
- [ ] red-team cases are documented.
- [ ] agent trace explains every tool call.
- [ ] Month 4 can harden and package the system.

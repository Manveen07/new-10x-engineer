# Week 19 — reposcout: Trajectory Evals + State-Transition Matrix + 50 Emails Total

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 18's working loop. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-5--ship-reposcout-agent--mcp--outbound-funnel-goes-live).

**Window:** Mon 2026-09-28 → Sun 2026-10-04
**Time budget:** 8–10 hours
**Position:** Month 5, Week 19 of 24

## Why this week matters

This is the agent equivalent of the leadlens/docsight eval work — and the key lesson: **output-only evals pass 20–40% more cases than the trajectory warrants.** A right answer reached by a broken path will break on the next input. So you score the *path*, not just the answer: 30 golden trajectories, a trajectory judge, and a state-transition matrix that surfaces loops and dead-ends.

**The single must-do:** 30 golden trajectories + a trajectory judge running + a state-transition matrix that catches at least one real loop — by Sunday. Outbound at 50 total.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-09-28 | Plan review + reply to any outbound responses (<24h rule starts) | 25 min |
| Tue eve | 2026-09-29 | Hand-curate 10 golden topics + their "good answer" repo lists | 30 min |
| Wed eve | 2026-09-30 | Hand-curate 10 more golden topics | 30 min |
| Thu eve | 2026-10-01 | Send 15 Insight Emails (40 total); curate final 10 topics | 30 min |
| Fri eve | 2026-10-02 | Send 10 more (50 total) OR rest | 15–30 min |
| **Sat** | 2026-10-03 | **Big build**: trajectory judge (expected tool path vs actual) + final-output precision/recall on repo lists + run all 30 | **3.5 hrs** |
| **Sun** | 2026-10-04 | **Build**: state-transition matrix from the 30 runs → find loops/dead-ends/spikes → fix one → re-run → PROGRESS | **3.5 hrs** |

## Saturday — trajectory + output evals (3.5 hrs)
- For each of the 30 topics, define the reasonable expected tool path. An LLM-as-judge scores "did the trajectory match a sensible shape?" (reuse critique-shadowing).
- Final-output eval: precision/recall of returned repo lists vs your hand-curated good answers.
- Run all 30; record cost/task, steps/task, escalation rate.

## Sunday — state-transition matrix (3.5 hrs)
- Build a matrix of state→state transitions across the 30 runs. Visualize it (counts per edge).
- Find a loop (same tool called repeatedly), a dead-end, or a failure spike. Fix one (tighten a tool result, add a guard). Re-run, show the matrix improved.
- PROGRESS update.

## Behind if
- Output-only evals (no trajectory scoring).
- No state-transition view (can't see loops).
- Fewer than 50 outbound sent cumulatively.

## Next week
→ `week-20.md`: deploy reposcout, register the MCP server (demoable from Claude Desktop), Loom, blog post 5, lightning talk.

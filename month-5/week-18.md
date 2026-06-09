# Week 18 — reposcout: Raw Orchestration + leadlens/docsight as MCP Tools + First 25 Emails

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 17's DESIGN.md. Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-5--ship-reposcout-agent--mcp--outbound-funnel-goes-live).

**Window:** Mon 2026-09-21 → Sun 2026-09-27
**Time budget:** 8–10 hours
**Position:** Month 5, Week 18 of 24

## Why this week matters

You build the agent the disciplined way — a raw `while` loop with typed tool calls, a hard step budget, and idempotency — *before* reaching for any framework. And you make MCP real: leadlens + docsight become tools any MCP client (Claude Desktop, Cursor) can call. "I built an agent that uses my own classifier and RAG via MCP" is the memorable final-round story. Outbound goes from list to *sends*.

**The single must-do:** reposcout runs end-to-end on one topic via raw orchestration with a 20-step budget, calling at least one tool over MCP — by Sunday. First 25 Insight Emails sent.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-09-21 | Plan review + read the [MCP docs](https://modelcontextprotocol.io) server quickstart | 25 min |
| Tue eve | 2026-09-22 | **LeetCode ×1** (near the end of the 60–80 arc) | 20 min |
| Wed eve | 2026-09-23 | Draft 5 Insight Emails (one observation + one specific 2-week trial offer each) | 30 min |
| Thu eve | 2026-09-24 | Send first 10 emails; draft 10 more | 30 min |
| Fri eve | 2026-09-25 | Send 15 more (25 total this week) OR rest | 15–30 min |
| **Sat** | 2026-09-26 | **Big build**: raw orchestration loop — Pydantic tool I/O, step budget (20), idempotency tokens, structured outputs, tool-arg validation; GitHub API signal tool | **3.5 hrs** |
| **Sun** | 2026-09-27 | **Build**: expose leadlens + docsight as MCP tools via FastMCP 3.x or the official `mcp` SDK; have reposcout call one over MCP; Langfuse trace per tool call → PROGRESS | **3.5 hrs** |

## Saturday — raw orchestration (3.5 hrs)
- A `while steps < 20` loop: model proposes a tool call → validate args against the Pydantic schema → execute → append result → repeat until done or budget hit.
- Idempotency tokens on every external call (GitHub API, tools) so a retry doesn't double-fetch.
- The GitHub signal tool: stars, last-commit recency, open/closed issue ratio, maintainer response time.
- Langfuse: one trace per run, one span per tool call.

## Sunday — MCP server (3.5 hrs)
- Wrap leadlens + docsight as MCP tools using FastMCP 3.x (Jan 2026, decorator-based) or the official `mcp` SDK (typed tool definitions + handlers).
- reposcout calls at least one over MCP (not a direct import) — proving the composition is real.
- Verify the server lists its tools to an MCP client.

## Behind if
- Agent has no step budget or idempotency (an uncontrolled loop).
- Tools called by direct import, not over MCP.
- Fewer than 25 Insight Emails sent.

## Next week
→ [week-19.md](./week-19.md): 30 golden trajectories + trajectory judge + state-transition matrix; next 25 emails (50 total).

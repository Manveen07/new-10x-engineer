# Month 5 — Ship reposcout (Agent + MCP) + Outbound Funnel Goes Live

## Goal

Ship the third project — an agent that composes leadlens + docsight as tools via MCP — and *simultaneously* turn on the US-remote outbound funnel that your GTM-engineer skill is uniquely suited for.

By Sunday 2026-10-11 you have three deployed projects, an MCP server demoable from Claude Desktop, a lightning talk delivered or recorded, and 50 cold-outreach Insight Emails sent to US AI founders with specific 2-week trial offers.

**Pace:** 8–10 hrs/week.
**Window:** 2026-09-14 → 2026-10-11.

## Outcome by end of month

### Project (Track 4)
- `projects/reposcout/` (renamed from `icp-research-agent` via `git mv`) deployed on Modal.
- Agent reads Anthropic *Building Effective Agents* discipline: workflow first, identified one agentic node.
- leadlens + docsight wired as **MCP tools** using FastMCP 3.x or the official `mcp` SDK.
- Step budget capped at 20. Idempotency tokens on all external tool calls.
- 30 golden reference topics with hand-curated "good" repo lists.
- Trajectory judge prompt + state-transition matrix.
- Precision/recall evals on final repo lists.
- MCP server registered + demoable from Claude Desktop (GIF in README).
- 3-min Loom walkthrough including MCP demo in Claude Desktop.
- Blog post 5 published: "Workflow first, agent second, MCP always."

### Outbound channel (Track 6)
- 50 just-raised US AI startups researched (sourced from TechCrunch funding announcements last 90 days).
- 50 Insight Emails sent — each with a *specific* 2-week trial offer for their context (not "looking for a job").
- Outbound tracker live (Google Sheet or a small Streamlit dashboard). Bonus: build the tracker as a meta-portfolio piece.
- All replies answered within 24 hours.

### Public (Track 5)
- 1 lightning talk delivered or recorded — Latent Space Discord demo night, AI Tinkerers, or local meetup.
- LinkedIn headline + About updated: "AI engineer | LLM systems with evals | MCP servers | open to remote contracts."
- X bio updated with portfolio link.
- 3 substantive X posts/week.

## Week themes

| Week | Window | Theme |
|---|---|---|
| 17 | Sep 14 – Sep 20 | Anthropic agents reading + reposcout `DESIGN.md` + outbound list build (50 targets) |
| 18 | Sep 21 – Sep 27 | Raw orchestration + MCP server skeleton + first 25 Insight Emails sent |
| 19 | Sep 28 – Oct 4 | Trajectory evals + state-transition matrix + next 25 Insight Emails (50 total) |
| 20 | Oct 5 – Oct 11 | Deploy + Loom + blog post 5 + lightning talk + README polish across all 3 projects |

Week files arrive ~3 days before each week. Provisional drafts exist — refine each the weekend before it starts: [week-17.md](./week-17.md) · [week-18.md](./week-18.md) · [week-19.md](./week-19.md) · [week-20.md](./week-20.md).

## Required reading

- **Anthropic — *Building Effective Agents*** (Dec 2024). Workflow vs agent. The five workflow patterns. Frames every architecture decision in reposcout.
- **Anthropic — *Effective Context Engineering for AI Agents*** (Sept 2025).
- **Anthropic SDK — MCP docs** at [modelcontextprotocol.io](https://modelcontextprotocol.io).
- Skim **PydanticAI** + **Letta** README (one example notebook each).

## Outbound playbook (Track 6 — your unfair advantage)

This is the work you already do at Precise Leads. The only difference is the target ICP and the offer.

**Sourcing:**
- TechCrunch funding category + Pitchbook Twitter alerts for last-90-day raises of AI startups Seed–Series A.
- Filter: 5–30 employees + at least one engineer post on LinkedIn + active GitHub.
- Find CTO/founding eng on LinkedIn → enrich with email via Hunter or Apollo (you use these at Precise Leads).
- Save to a sheet with `company, founder, raise_date, raise_amount, product_one_liner, observation, offer`.

**Insight Email structure (5 sentences):**
1. One specific observation about their product/blog/launch (the "warm" part — never skip).
2. One belief about a problem they probably have (RAG quality, agent reliability, eval discipline, MCP integration).
3. One specific 2-week trial offer: "I'd build X for free, and if you find it useful we can talk about a paid engagement." Pick from: build their eval suite, wrap their product as an MCP server, instrument Langfuse traces, ship a focused classifier, port a feature to a cheaper model.
4. One line of credibility — link to one of your three project READMEs + Loom.
5. One question to make replying easy ("worth a 15-min call this week or next?").

**Don't:**
- Don't open with "I'm a final-year student looking for opportunities." This is a job-board email; they get 200/day.
- Don't pitch yourself as a generalist. Pitch one specific outcome.
- Don't follow up more than twice — bump after 3 days, polite close after 7. Move on.

**Volume:**
- 12–13 messages/day × 4 days/week = 50/week.
- Replies expected: ~3–5/50 (industry standard). All replies answered within 24 hrs.

## Monthly checklist

See [EXERCISES.md](../EXERCISES.md) Month 5 section.

## Interview skill added

You can **demo your MCP server live in Claude Desktop** in a final-round screen-share, narrating workflow-vs-agent design choices in 90 seconds, with a state-transition matrix on screen explaining a loop you caught. That's a Sarvam FDE / Sierra agent eng / Mercor calibration win in 5 minutes.

## Behind if

- No MCP server demoable from Claude Desktop.
- Fewer than 30 outbound Insight Emails sent.
- No lightning talk delivered or recorded.
- Blog post 5 not published.

## Next month

→ [../month-6/README.md](../month-6/README.md) — Run the funnel: applications, mocks, conversion.

# Week 17 — reposcout: Workflow-First Design + Find the One Agentic Node + Outbound List

> 📝 **PROVISIONAL draft (2026-06-09, ~13 weeks early).** Refine the weekend before, anchored on having leadlens + docsight deployed (reposcout composes them as tools). Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-5--ship-reposcout-agent--mcp--outbound-funnel-goes-live). Spec: [../PROJECTS.md](../PROJECTS.md#project-3--reposcout-month-5).

**Window:** Mon 2026-09-14 → Sun 2026-09-20
**Time budget:** 8–10 hours
**Position:** Month 5, Week 17 of 24

## Why this week matters

The 2026 differentiator is agents — but the senior signal is *restraint*: "I built a workflow and used an agent only at the one node that needed it." This week you read Anthropic's two canonical pieces and sketch reposcout as a **workflow first**, identifying the single node that genuinely needs dynamic decisions. In parallel, outbound prep starts — your unfair advantage gets pointed at your own funnel.

**The single must-do:** a reposcout `DESIGN.md` with a workflow diagram + the one agentic node circled and justified — by Sunday. Plus 50 just-raised US AI startups sourced.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-09-14 | Plan review + read [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) → note the 5 workflow patterns | 25 min |
| Tue eve | 2026-09-15 | Read [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) → recall: "what is context rot?" | 25 min |
| Wed eve | 2026-09-16 | **LeetCode ×1** (graph — relevant to trajectory state) | 20 min |
| Thu eve | 2026-09-17 | Source 25 just-raised US AI startups (TechCrunch funding → CTO/founding-eng on LinkedIn/X) | 30 min |
| Fri eve | 2026-09-18 | Source 25 more (50 total) into a sheet OR rest | 15–30 min |
| **Sat** | 2026-09-19 | **Big build**: reposcout `DESIGN.md` — workflow sketch (topic → GitHub signals → leadlens/docsight tools → ranked report); circle the ONE agentic node; define tool I/O contracts | **3.5 hrs** |
| **Sun** | 2026-09-20 | **Build**: define the eval plan (30 golden topics, trajectory + final-output metrics) + finish outbound list with enrichment → PROGRESS | **3 hrs** |

## Saturday — workflow-first DESIGN.md (3.5 hrs)
- Sketch reposcout as deterministic steps: input topic → GitHub API signals (stars, recent activity, issue quality, maintainer responsiveness) → call **leadlens** (classify repos/roles) + **docsight** (knowledge over docs) as tools → rank → evidence-backed report.
- **Circle the one node that needs an agent** (e.g. deciding which follow-up searches to run when signal is thin) and justify why a workflow can't do it. Everything else stays deterministic.
- Define each tool's Pydantic I/O contract + the 20-step budget + idempotency tokens.

## Sunday — eval plan + outbound list (3 hrs)
- Eval plan in DESIGN.md: 30 golden reference topics with hand-curated "good answer" repo lists; trajectory evals (expected tool path) + final-output precision/recall + a state-transition view.
- Outbound: 50 just-raised seed/Series-A US AI startups, CTO/founding-eng enriched (Hunter/Apollo — your Precise Leads stack). Save to a sheet for Week 18 sends.

## Behind if
- DESIGN.md leads with "agent" instead of workflow.
- Can't name the one node that needs dynamism (and why).
- Fewer than 50 outbound targets sourced.

## Next week
→ [week-18.md](./week-18.md): raw orchestration + wire leadlens/docsight as MCP tools + first 25 Insight Emails.

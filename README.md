# Manveen's 6-Month AI Engineer Roadmap

**Mission:** Be hireable as a junior **GenAI / LLM Application Engineer** by November 2026 — through three shipped public projects, four to six written posts, one OSS contribution, and an MCP server, while rebuilding hands-on coding fluency that AI tools eroded.

**Pace:** 8–10 hours/week. Sustainable, college-compatible, designed to finish — not to look impressive on a Notion page.

**Window:** 2026-05-25 → 2026-11-08 (24 weeks).

---

## ▶ Start here every day

→ **[START_HERE.md](./START_HERE.md)**

That file tells you exactly what week you are in and what to do today. Bookmark it. Open it every working session. You should never have to ask "what now?".

---

## Who this plan is for (you)

- Final-year BTech CS at MSIT, graduating Aug 2026
- AI/ML intern at Caprae Capital (Sasquatch data pipelines) + current GTM Engineer at Precise Leads (n8n + scraping + lead enrichment)
- Shipped projects: **AsanaBot** (Vision Transformers + MediaPipe for yoga pose feedback) and **PresentAI** (Next.js SaaS + Gemini for slide generation)
- Comfortable with Python basics; rusty on async, typing, Pydantic, modern tooling because AI writes most of your code now
- Targeting **US-remote** as primary funnel via four channels — Mercor, HN/YC/Wellfound, direct outbound to US AI founders, and curated remote boards — with **India product startups** as the realistic safety. Your existing GTM-engineer outbound skill (Slack scraping → qualification → outreach at Precise Leads) is your biggest single advantage and is what makes US-remote the *right* primary, not just the ambitious one.

## What you're building toward (Nov 2026 readiness bar)

1. **Three deployed projects** — classifier with evals, production RAG, agent + MCP server.
2. **Four to six technical blog posts** on your own domain, each with a real failure mode you found.
3. **One merged OSS pull request** to a known LLM/AI repo.
4. **One MCP server** — registered, demoable from Claude Desktop or Cursor.
5. **A README portfolio** any hiring manager can scan in 90 seconds and conclude "yes, this person ships."
6. **An interview funnel actually open** — 25+ applications, 5+ first rounds, 1+ offer cycle in motion.

## Positioning (your wedge)

"GenAI app engineer who ships LLM systems with evals and an MCP server, not just a chatbot demo."

You're the rare junior who has (a) shipped a full-stack GenAI SaaS (PresentAI), (b) a CV/PyTorch project (AsanaBot), and (c) production-flavored data/automation experience from two internships. Most fresher candidates show ML coursework *or* a GenAI tutorial demo, not both plus eval-first thinking. The plan turns that cross-section into something hiring managers see immediately.

## Repository map

**Strategy** (read once, re-skim monthly)
- This file — one-screen positioning.
- [MASTER_PLAN.md](./MASTER_PLAN.md) — full strategy, skill audit, target roles, anti-patterns, resources.

**Plan** (read at the start of each month)
- [ROADMAP.md](./ROADMAP.md) — 24-week month-by-month table.
- [PROJECTS.md](./PROJECTS.md) — three flagship project specs: leadlens, docsight, reposcout.
- [EXERCISES.md](./EXERCISES.md) — monthly execution checklist.

**Execution** (open every working day)
- [START_HERE.md](./START_HERE.md) — daily landing page.
- [month-1/](./month-1/README.md) → [month-6/](./month-6/README.md) — per-month overviews + per-week daily plans.
- [PROGRESS.md](./PROGRESS.md) — weekly Sunday log. The single forcing function.
- [projects/business-classification-pipeline/](./projects/business-classification-pipeline/) — leadlens (Months 1–2). Already has your 50 traces.
- [projects/gtm-clay-rag/](./projects/gtm-clay-rag/) — will be renamed to **docsight** in Month 3.
- [projects/icp-research-agent/](./projects/icp-research-agent/) — will be renamed to **reposcout** in Month 5.

## The six tracks

Every hour goes into one of these. Rebalance monthly.

1. **Code fluency rebuild** — daily no-AI keyboard warm-ups, weekly build blocks, modern Python stack.
2. **Eval-first development** — open coding, golden datasets, calibrated judges, CI gates.
3. **RAG / retrieval engineering** — hybrid search, contextual retrieval, reranking, retrieval evals.
4. **Agent engineering + MCP** — workflow-first, step budgets, scoped tools, trajectory evals, MCP server.
5. **Public footprint (US-resonant)** — blog, GitHub, X, LinkedIn, OSS contribution, Loom walkthroughs, community presence.
6. **Outbound channel (your unfair advantage)** — sourcing US AI founders, Insight-Email outreach, Mercor + HN + Wellfound + direct outbound funnel. Light in Months 3–4, ramps in Months 5–6.

## The three projects

| # | Codename | Months | What it proves | Folder |
|---|---|---|---|---|
| 1 | **leadlens** | 1–2 | Eval-first development on a real classifier | [projects/business-classification-pipeline](./projects/business-classification-pipeline/) |
| 2 | **docsight** | 3–4 | Production RAG with measured retrieval quality | [projects/gtm-clay-rag](./projects/gtm-clay-rag/) |
| 3 | **reposcout** | 5 | Agent design + MCP server + trajectory evals | [projects/icp-research-agent](./projects/icp-research-agent/) |

Each project must include a live URL, README to standard, eval dataset, eval results table, cost-per-call, latency p50/p95, Langfuse traces, and a "Where it fails" section. Full specs in [PROJECTS.md](./PROJECTS.md).

## Standing rules (re-read every Sunday for first three months)

1. **Eval before scale.** Every project gets a golden dataset before optimization.
2. **One framework or none.** Raw SDK + Pydantic + Instructor is the default; add LangGraph only at the node that genuinely needs it.
3. **Workflow before agent.** Default to deterministic code; agentic dynamism only where required.
4. **Type the code yourself before asking AI.** 5-minute hand-coded warm-up daily, no AI. Then AI is a pair, not a crutch.
5. **Ship in public weekly.** Even a commit, a tweet, a README diff. Hidden work doesn't compound.
6. **Production thinking lives in the README.** "Where it fails," cost-per-call, latency p50/p95, eval results table — no exceptions.

Full anti-patterns list in [MASTER_PLAN.md](./MASTER_PLAN.md) §7.

## Start here

Open **[START_HERE.md](./START_HERE.md)**. It tells you the current week and what to do today.

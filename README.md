# Avi's AI Engineer Roadmap

A six-month, 8-hours-per-week roadmap for becoming job-ready as an AI engineer by building on real production LLM and GTM automation experience.

The goal is not to restart from beginner material. The goal is to close specific gaps that hiring managers screen for: evals, retrieval measurement, production deployment, agent reliability, and clear public proof of work.

---

## ▶ Start here every day

→ **[START_HERE.md](./START_HERE.md)**

That file tells you exactly what week you are in, what to do today, and which file to open next. Bookmark it. Open it every working session. You should never have to ask "what now?".

---

## Positioning

AI engineer specializing in LLM-powered data and GTM systems.

Current wedge:

- LLM classification pipelines for noisy business data.
- Clay, Smartlead, enrichment, web-search, and MCP-based GTM workflows.
- Real failure-mode experience: hallucination audits, fallback retrieval, API/tool auth failures, cost and repeatability constraints.
- Bengaluru and Clay operator community context.

By the end of Month 6, this repo should support active interviewing with:

- Three production-grade portfolio projects.
- Eval suites with golden datasets and calibrated judge logic.
- Live deployments, Langfuse traces, cost/latency notes, and failure-mode sections.
- Six public posts on your own domain.
- A visible warm-intro and application funnel for GTM-AI, Bengaluru AI, and applied AI roles.

## Repository Map

**Strategy** (read once, re-skim quarterly)
- [START_HERE.md](./START_HERE.md) — daily landing page.
- [MASTER_PLAN.md](./MASTER_PLAN.md) — full strategy, skill audit, target roles, anti-patterns, resources.

**Plan** (read at the start of each month)
- [ROADMAP.md](./ROADMAP.md) — six-month week-by-week table.
- [PROJECTS.md](./PROJECTS.md) — three flagship project specs and common standard.
- [EXERCISES.md](./EXERCISES.md) — monthly execution checklist.

**Execution** (read every working day)
- [month-1/](./month-1/README.md) → [month-6/](./month-6/README.md) — per-month overviews + per-week daily plans.
- [PROGRESS.md](./PROGRESS.md) — weekly Sunday log.
- [projects/business-classification-pipeline/](./projects/business-classification-pipeline/) — Project 1 home (Months 1–2).
- [projects/gtm-clay-rag/](./projects/gtm-clay-rag/) — Project 2 home (Months 3–4).
- [projects/icp-research-agent/](./projects/icp-research-agent/) — Project 3 home (Month 5).

## The Five Tracks

Every hour goes into one of these:

1. **Production fluency** — deployed services, traces, cost and latency reasoning.
2. **Eval-first development** — open coding, golden datasets, calibrated judges, CI gates.
3. **RAG and retrieval engineering** — hybrid search, contextual retrieval, reranking, retrieval evals.
4. **Agent engineering** — workflow-first design, step budgets, scoped tools, trajectory evals.
5. **Public footprint** — writing, project READMEs, OSS contribution, Bengaluru and Clay network.

## The Three Projects

| # | Project | Months | Folder |
|---|---|---|---|
| 1 | Business classification pipeline + eval harness | 1–2 | [projects/business-classification-pipeline](./projects/business-classification-pipeline/) |
| 2 | RAG over GTM/Clay knowledge with retrieval evals | 3–4 | [projects/gtm-clay-rag](./projects/gtm-clay-rag/) |
| 3 | ICP research agent with trajectory evals | 5 | [projects/icp-research-agent](./projects/icp-research-agent/) |

Each project must include a live URL, README, architecture diagram, eval dataset, eval results table, cost-per-call analysis, latency p50/p95, Langfuse traces, and a "Where it fails" section.

## Rules

- Eval before scale.
- Workflow before agent.
- One framework or none unless the system genuinely needs more.
- Public proof beats private learning.
- No fake claims.
- No demo without evals.
- Lean into the GTM and Clay wedge instead of trying to look like a generic SWE candidate.

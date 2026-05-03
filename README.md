AI Engineer Roadmap

A six-month, 8-hours-per-week roadmap for becoming job-ready as an AI engineer by building on real production LLM and GTM automation experience.

The goal is not to restart from beginner material. The goal is to close specific gaps that hiring managers screen for: evals, retrieval measurement, production deployment, agent reliability, and clear public proof of work.

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
- Around six public posts or project updates.
- A visible warm-intro and application funnel for GTM-AI, Bengaluru AI, and applied AI roles.

## Canonical Files

Start here:

1. [MASTER_PLAN.md](./MASTER_PLAN.md) - strategy, skill audit, target roles, anti-patterns, resources. **Read this first.**
2. [ROADMAP.md](./ROADMAP.md) - the six-month plan, week by week.
3. [PROJECTS.md](./PROJECTS.md) - the three flagship project specs and standards.
4. [EXERCISES.md](./EXERCISES.md) - monthly execution checklist.
5. [PROGRESS.md](./PROGRESS.md) - weekly tracking template.

Monthly folders:

- [month-1](./month-1/README.md) - eval foundations and Project 1 design.
- [month-2](./month-2/README.md) - ship the business classification pipeline.
- [month-3](./month-3/README.md) - RAG fundamentals and Project 2 design.
- [month-4](./month-4/README.md) - ship the GTM/Clay RAG system.
- [month-5](./month-5/README.md) - ship the ICP research agent and polish portfolio.
- [month-6](./month-6/README.md) - job search execution and interview loop.

## The Five Tracks

Every hour goes into one of these tracks:

1. **Production fluency** - deployed services, traces, cost and latency reasoning.
2. **Eval-first development** - open coding, golden datasets, calibrated judges, CI gates.
3. **RAG and retrieval engineering** - hybrid search, contextual retrieval, reranking, retrieval evals.
4. **Agent engineering** - workflow-first design, step budgets, scoped tools, trajectory evals.
5. **Public footprint** - writing, project READMEs, OSS contribution, Bengaluru and Clay network.

## The Three Projects

1. **Business classification pipeline with eval harness** - Months 1-2.
2. **RAG over GTM/Clay knowledge with retrieval evals** - Months 3-4.
3. **ICP research agent with trajectory evals** - Month 5.

Each project must include a live URL, README, architecture diagram, eval dataset, eval results table, cost-per-call analysis, latency p50/p95, Langfuse traces, and a "Where it fails" section.

## Rules

- Eval before scale.
- Workflow before agent.
- One framework or none unless the system genuinely needs more.
- Public proof beats private learning.
- No fake claims.
- No demo without evals.
- Lean into the GTM and Clay wedge instead of trying to look like a generic SWE candidate.

## Existing Material

Some existing `week-*`, `exercises/`, and `capstone/` folders came from the earlier four-month backend/RAG/agent curriculum. Keep them as reusable drills and implementation material, but treat the new monthly READMEs and root roadmap as canonical.

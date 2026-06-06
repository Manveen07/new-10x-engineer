# New 10x Engineer

A practical, truth-first log of becoming a job-ready production AI engineer.

This repo is built around my **real, current** skill set and the specific gaps I'm closing. It is not a generic AI roadmap and it does not claim experience I don't have.

## Current profile

I build production AI and automation systems for GTM — lead generation, enrichment, research, and outbound. I'm a GTM / Automation Engineer at Precise Leads and was an AI/ML intern at Caprae Capital.

**What I can currently demonstrate (with proof, not claims):**

- **Eval engineering** — I built a calibrated, claim-level **faithfulness eval** for a production cold-email system: error analysis → failure taxonomy, LLM-as-judge calibrated to **100% agreement** on a 20-email / 124-claim golden set, scored across **300 emails** with a committed report. The eval caught a recurring bug class that became a code-level writing rule. *(This is the rarest skill on the 2026 bar, and I did it on real data.)*
- **Multi-agent orchestration** — a cold-outbound system where parallel agents research each lead across web/LinkedIn/firmographic sources and draft evidence-grounded emails (Claude Code orchestration + TypeScript tools).
- **GTM automation** — n8n workflows, Slack-community lead discovery, enrichment + validation pipelines, CRM sync.
- **Production instincts** — cost, reliability, retries, credit burn, anti-hallucination controls.
- **Prior dev** — Python, TypeScript, full-stack (Next.js/Prisma/Postgres), Vision Transformers.

## What I'm still closing (the honest gaps)

Ranked by ROI for an AI-engineer role:

1. **RAG retrieval quality** — not "use a vector DB," but measuring retrieval (recall@k, MRR, NDCG), hybrid search + reranking, contextual retrieval, calibrated RAG-triad evals. *(My #1 red zone; RAG is the most in-demand 2026 skill.)*
2. **Backend deployment** — FastAPI services, Docker, CI/CD, observability (Langfuse), cloud deploy with a live URL.
3. **Clean Python rigor** — typing, tests (pytest), packaging, logging, config — making every repo an exemplar.
4. **Cost modeling** — estimating $/task for LLM systems at production scale.
5. **Agent evaluation** — trajectory evals + runtime guardrails on systems I already build.

## How this repo works

- **[`ROADMAP.md`](./ROADMAP.md)** — the staged plan (Phase 1 package & deploy the eval system → Phase 2 RAG → Phase 3 agent rigor → Phase 4 polish + funnel), with a technique-reference appendix per domain. Research-grounded (Hamel/Shreya on evals, Anthropic on agents, Jason Liu on RAG), sources cited.
- **[`study_curriculum.md`](./study_curriculum.md)** — the ordered, active-reading learning track: what to read, what to extract, exercises, and interview self-tests.
- **[`PROJECTS.md`](./PROJECTS.md)** — the three portfolio projects.
- **[`interview_prep_qa.md`](./interview_prep_qa.md)** — Q&A bank for the 5 interview clusters (evals, RAG, agents, LLMOps, cost modeling); drilled in Phase 4.
- **[`PROGRESS.md`](./PROGRESS.md)** — weekly honest log (the only forcing function).

## Target outcome

Three deployed, eval-backed projects (eval system + RAG app + agent system), each with a standard README, Langfuse traces, cost/latency analysis, and a public write-up — backing applications to remote **AI Engineer / Automation Engineer / GTM Engineer** roles.

## Rules for this repo

- No fake claims. No AI-generated fluff.
- Every project: a real problem, real inputs, real outputs, measurable quality checks.
- Every automation: cost, failure cases, anti-hallucination controls.
- Every project explainable in an interview.
- This repo reflects what I've actually done — and what I haven't yet.

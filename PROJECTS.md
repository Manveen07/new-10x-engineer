# Projects

Three deployed, eval-backed projects covering the 2026 portfolio standard (eval system + RAG app + agent system). Each must ship with: a live URL, a standard README (problem, architecture diagram, stack, demo, **evals**, cost/latency, lessons), Langfuse traces, and a public write-up.

> Standard, every project: measure quality with real metrics, report $/task, name the failure modes. "Recruiters ask for links" — undeployed doesn't count.

---

## Project 1 — Cold-Outbound Faithfulness Eval System *(Phase 1 — mostly built, finish + deploy)*

**Problem:** Personalized cold outbound hallucinates the personalization — fake hooks that are worse than generic. Telling the model "don't invent facts" is an instruction, not a guarantee.

**What it does:** A read-only eval harness that scores every drafted email for **faithfulness** — decomposes it into atomic claims and a calibrated LLM-as-judge labels each `supported / unsupported / contradicted` against the research evidence only. Faithfulness = supported/total; any contradicted claim auto-gates the draft.

**Status / results:** 95.5% mean faithfulness, 242/300 perfectly grounded, **0 contradicted** across 300 emails; judge calibrated to **100% agreement** on a 20-email/124-claim golden set. Caught a "count/group/name beyond evidence" bug class → became a writing rule.

**To finish (Phase 1):** clean Python (types/pytest/logging), FastAPI `POST /score` + Docker + live URL, Langfuse tracing, 2nd-axis quality rubric, GitHub Actions CI gate on faithfulness, cost-per-email, README to standard, Post 1.

**Stack:** Claude Code orchestration · Claude · TypeScript · FastAPI · Docker · Langfuse · GitHub Actions
**Repo:** `coldoutboundskills` (make public, sanitized — no client PII/keys)
**Proves:** the rare eval skill + deployment + observability + clean code.

---

## Project 2 — Hybrid RAG over GTM/Company Data *(Phase 2 — build)*

**Problem:** Answer questions over a large, changing corpus of company/GTM documents with grounded, cited answers — and *prove* the retrieval is good, not vibe it.

**What it does:** `query → (optional rewrite/HyDE) → BM25 + vector → RRF (k=60) → cross-encoder rerank → top 5–10 → cited generation`, with **contextual retrieval** at index time and auto-merging chunks. Calibrated RAG-triad / Ragas evals.

**The headline artifact:** an **ablation table** — pure dense vs BM25 vs hybrid vs hybrid+rerank — with **recall@10 / MRR / NDCG@10 measured per query-segment** (not averaged). Plus $/query and latency.

**To build:** pgvector ingestion + contextual retrieval (Wk6), 150 synthetic eval pairs + segmented metrics (Wk7), reranker + ablation (Wk8), cited generation + calibrated Ragas (Wk9), deploy + Post 2 (Wk10).

**Stack:** Python · Postgres/pgvector · BM25 · cross-encoder reranker · Ragas · FastAPI · Langfuse
**Proves:** retrieval quality + RAG evaluation — *the* most in-demand 2026 skill.

---

## Project 3 — Trajectory-Evaluated Agent System *(Phase 3 — harden + evaluate)*

**Problem:** Multi-agent systems are easy to demo and hard to trust. Output-only evaluation passes 20–40% more cases than the trajectory actually warrants.

**What it does:** Takes the cold-outbound agents, re-drawn **workflow-first** (deterministic nodes + one genuine agent loop), with Pydantic tool I/O, step budgets, and idempotency. Evaluated with **30+ golden trajectories** (a judge scores the *path*, not just the final answer) and protected with **runtime guardrails** (block contradicted outputs; max steps; HITL on irreversible actions — mapped to OWASP LLM06/LLM09).

**To build:** workflow-first redraw + typed tools (Wk11), golden trajectories + trajectory judge (Wk12), runtime guardrails + per-agent cost/latency (Wk13), deploy/document + Post 3 (Wk14).

**Stack:** Claude · TypeScript/Python · Pydantic · LangGraph (for interview fluency) · Langfuse
**Proves:** agent evaluation + production orchestration + safety — the rare "evaluate agents, don't just build them" skill.

---

## Supporting / older work (context, not portfolio centerpieces)

- **Lead Enrichment & GTM Automation Pipeline** — n8n + Python multi-source enrichment, validation, CRM sync.
- **PresentAI** — AI SaaS that auto-generates slide decks (Next.js/Prisma/Postgres/Gen AI). [live + source]
- **AsanaBot** — real-time yoga pose analysis (Vision Transformers + MediaPipe). [source]

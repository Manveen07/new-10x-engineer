# AI Engineer Interview Prep — Q&A bank (2026)

> Active-recall deck for the five clusters that cover ~90% of 2026 AI-engineer loops: **evals, RAG, agents, LLMOps/production, and LLM system design** — plus cost modeling and failure-mode fluency (the two things that separate strong candidates). Cover the answer, say yours aloud, then check. Answers are tight on purpose — interview-length, not essays. Grounded in the same research as the roadmap.

---

## How to drill this
- **Phase 4:** one cluster per session; say each answer aloud in <1 min.
- The goal isn't memorizing my words — it's being able to reconstruct the idea. If you can teach it, you know it.
- Tie every answer back to **your own systems** where you can ("on my cold-outbound eval, I…"). Production stories are the #1 differentiator.

---

## Cluster 1 — Evals

**Q: How do you evaluate an LLM feature with no ground-truth labels?**
Start with error analysis, not metrics. Sample ~100 real traces, open-code them (free-text notes on the first failure in each), then axial-code into a failure taxonomy and count per category. That tells you what to measure. Then build targeted checks: cheap deterministic assertions where possible, an LLM-as-judge for the subjective parts — calibrated against a small hand-labeled set. Generic "helpfulness 1–5" scores are a trap; they don't correlate with what matters.

**Q: Binary vs 1–5 scoring for an LLM judge — which and why?**
Binary. The gap between a 3 and a 4 is subjective and inconsistent across annotators, and people cluster at the middle to avoid hard calls. Binary forces you to define "good" and is faster. If I need gradual signal I decompose into multiple binary sub-checks — "4 of 5 expected facts present" — not one fuzzy score.

**Q: Your judge agrees with the expert 95% of the time. Is it good?**
Not necessarily — raw agreement misleads under class imbalance. If 90% of outputs are "pass," a judge that always says pass scores 90% and catches nothing. I measure true-positive and true-negative rate separately (or precision/recall) on a held-out labeled set. I care most about recall on the failure class — does it catch the bad outputs a human would?

**Q: How did you calibrate your judge?** *(your story)*
I hand-labeled 20 emails / 124 claims before looking at the judge's verdicts, then measured agreement — 100%, with 100% recall on unsupported claims. Without that step the faithfulness number is just a second model's opinion.

**Q: CI evals vs production monitoring?**
CI is a small (~100) purpose-built set with regression tests for past bugs; it runs on every push so I favor cheap deterministic checks and gate the build. Production monitoring samples live traces asynchronously, usually reference-free LLM-judge, and I track confidence intervals. When prod surfaces a new failure, I add a case back into CI.

**Q: Guardrail vs evaluator?**
A guardrail is synchronous, fast (ms), deterministic, in the request path — PII, profanity, malformed JSON, injection. An evaluator runs after/async and measures nuanced quality — factuality, completeness — feeding dashboards and regression tests. You almost never put a slow LLM judge in the synchronous path.

**Q: Your evals pass 100%. Good news?**
Usually bad — it means the eval isn't challenging the system. A ~70% pass rate is often more meaningful because it's actually stress-testing. 100% means I need harder cases.

---

## Cluster 2 — RAG

**Q: Design a RAG system for a customer-support chatbot.** *(the most common opener — have a 2-min version)*
Ingestion → chunking (recursive, ~512 tokens, auto-merging so I retrieve small but feed parent context) → **contextual retrieval** (prepend a situating blurb per chunk before indexing) → store in pgvector + a BM25 index → **hybrid retrieval** (dense + BM25 fused with RRF, k=60) → **rerank** a 20–50 candidate set down to top 5–10 with a cross-encoder → cited generation. Then the part most people skip: **evaluation** — a golden set of 50–100 queries, retrieval metrics (recall@10, MRR, NDCG) measured per query-segment, and a RAG-triad/Ragas check on generation. Monitor no-retrieval rate and hallucination rate in prod. I'd also add access-control filtering at retrieval since support data is per-account.

**Q: Why hybrid search, not pure vector?**
Vector search measures similarity, not exact relevance — it whiffs on error codes, SKUs, acronyms, and names. In support data ~35% of queries contain a specific identifier. BM25 catches those (and plural/singular via stemming); dense catches paraphrase. Hybrid gets both; I fuse with RRF because BM25 and cosine scores live on incompatible scales.

**Q: Why rerank, and how many?**
A cross-encoder scores the query and doc together, so it's much better at fine-grained relevance — but too slow for the whole corpus. So I retrieve wide (20–50) cheaply, then rerank to the top 5–10. Five risks missing the best doc; 200 burns latency for nothing. Reranking can lift nDCG substantially just by reordering the same candidates.

**Q: RAG or a 1M-token context window?**
Long context to *reason* over a bounded evidence set; retrieval to *decide* what that set is. If the knowledge base is under ~200K tokens, stable, single-user — just stuff the prompt with caching. I go RAG when the corpus is large or changing, I need citations/audit, per-user access control, or sub-3-second latency. For hard multi-doc reasoning I do hybrid: retrieve a small set, reason over it in long context. And long context isn't free recall — there's "lost in the middle."

**Q: Retrieval metrics look fine but answers are wrong. Where's the bug?**
If retrieval is good and generation is bad, it's a prompt/LLM problem — grounding instructions, context ordering, temperature — not retrieval. The discipline is measuring the two layers separately; ~70% of RAG failures are actually retrieval, so I check that first, but when it's clean I stop blaming retrieval. Also: averaged metrics hide failures — I segment queries and look at the worst segment.

**Q: What's contextual retrieval and is it worth it?**
Before embedding each chunk, prepend a 50–100 token blurb situating it in its document, so "revenue grew 3%" becomes "ACME Q2 2023 … revenue grew 3%." Applied to embeddings and BM25 it cuts retrieval failures up to ~49%, ~67% with reranking. With prompt caching the indexing cost is about a dollar per million document tokens. Usually worth it.

---

## Cluster 3 — Agents

**Q: When should you NOT use an agent?**
When you can predict the steps. Agents trade latency, cost, and compounding-error risk for flexibility — they're for open-ended tasks where you can't hardcode the path. For most things a workflow (fixed code paths with LLM calls) or even a single optimized LLM call with retrieval and examples is enough and more reliable. Simplest thing that works first.

**Q: Name the workflow patterns.**
Prompt chaining (fixed sequential steps with gates), routing (classify then send to a specialized handler — and route easy queries to a cheap model), parallelization (sectioning independent subtasks, or voting the same task N times), orchestrator-workers (a central LLM decides the subtasks at runtime), and evaluator-optimizer (generate ↔ critique loop). Production agents combine these.

**Q: Why evaluate the trajectory, not just the final answer?**
Output-only evaluation passes 20–40% more cases than trajectory evaluation reveals — it hides tool-call mistakes, retrieval misses, and loop bugs that happened to produce a fine-looking answer. I score the path: right tool, right arguments, did the loop terminate, did retries converge — with deterministic checks for tool-name/argument correctness and an LLM judge only for subjective steps. I anchor it with 30+ golden trajectories in CI.

**Q: What's context engineering?**
Managing the whole context state — system prompt, tools, history, retrieved data — to keep the smallest set of high-signal tokens. It matters because of context rot: recall degrades as the window fills (n² attention). Tactics: tight tool sets (if a human can't pick the tool, neither can the agent), just-in-time retrieval (keep identifiers, load at runtime), and for long-horizon tasks — compaction, structured note-taking, and sub-agents that work in clean contexts and return short summaries.

**Q: How do you prevent cascading agent failures?**
One tool error can trigger a hallucinated recovery plan that compounds. Guardrails: max step/iteration limits, tool-call validation (schema + required args), and human-approval gates on irreversible actions. Maps to OWASP LLM06 (excessive agency) and LLM09 (misinformation).

---

## Cluster 4 — LLMOps / production

**Q: What does tracing capture and why does it matter?**
A trace is one request's full lifecycle — the exact prompt sent, the response, token usage, latency, and every tool/retrieval step in between, with timing. It's the most important observability tool for LLM apps because behavior is non-deterministic; without the full per-request context you can't debug why one answer went wrong. I'd use Langfuse — open source, self-hostable, OTel-compatible, async flush so no added latency.

**Q: What do you monitor in an LLM app in production?**
Faithfulness/hallucination rate, no-retrieval rate, drift, cost per trace (by model/feature/user), latency per step and end-to-end, and prompt regression — I version prompts and run a golden set before shipping a new one.

**Q: How do you deploy an LLM service?**
FastAPI: stream tokens over SSE with StreamingResponse; for anything beyond a few seconds, return a job ID and process async with a Redis-backed queue (Celery/RQ) for retries; load models once at startup, not per request; Gunicorn + Uvicorn workers. Modal for GPU inference, Railway/Fly/Render for always-on APIs.

---

## Cluster 5 — Cost modeling (the underrated edge)

**Q: Estimate the cost of a 10-turn agent conversation.**
Walk the math out loud: say each turn averages 8K input + 1K output tokens, and the conversation re-sends growing history. At turn t the input is roughly the accumulated context. Take per-turn input ≈ 8K and output ≈ 1K, multiply by the model's input/output per-million-token price, sum across 10 turns. The interviewer cares that you *naturally* fold token-cost and latency budgets into the design — e.g., "history grows each turn, so I'd cap context with compaction, route simple turns to a cheaper model, and cache the stable system prompt." (Plug in current per-Mtok prices for the tier you'd use.)

**Q: How do you cut LLM cost without hurting quality?**
Route by difficulty (cheap model for easy turns, strong model for hard ones); prompt caching for stable context; cap context via compaction/JIT retrieval; rerank to send fewer, better chunks; batch where latency allows; and use a cheap judge for most evals, reserving the expensive model for the hardest cases.

---

## The two "do you actually ship" questions

**Q: Tell me about a system that broke in production and how you fixed it.** *(have 2–3 real stories ready — this is the #1 signal)*
Your cold-outbound story works: the model was inventing details that passed a casual read — "three cities" when the data had two, naming a parent company no source mentioned. I built a faithfulness eval that decomposes each email into claims and checks them against the evidence; it surfaced the pattern (counting/naming beyond evidence), I turned it into an explicit writing rule, and gated drafts on it. Measure → find the pattern → engineer it out.

**Q: How would you know if your AI feature is getting worse over time?**
Versioned prompts + a golden set run in CI on every change, async evaluators on sampled production traces with confidence intervals, and drift/cost/latency monitoring. A regression that drops faithfulness below threshold fails the build before it ships.

---

## Self-grading
For each question, rate yourself: **🟢 fluent (<1 min, with a personal example) / 🟡 shaky / 🔴 can't.** Spend Phase-4 sessions turning 🔴→🟡→🟢. When every Cluster-1/2 question is 🟢 and you have three real production-failure stories, you're interview-ready.

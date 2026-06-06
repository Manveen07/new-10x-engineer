# Study Curriculum — active-reading guide (research-grounded)

> Companion to `ROADMAP.md`. The roadmap's Part II appendices hold the *techniques*; this holds the *learning sequence*: what to read in what order, the specific things to extract from each source (so you read actively, not passively), a hands-on exercise per phase, and interview-style self-tests. Everything is free unless marked **[paid]**. Rule: never study an item without the matching build deliverable open.

---

## How to use this

- **Daily 15 min:** one source from the current phase.
- **Active reading:** each source below lists **"extract this"** — 2–3 specific things to pull out. If you finish a source and can't state them, you read passively; reread into your build.
- **One Tier-1 spine source open at all times.** Don't read ahead of your build.
- **If you buy one thing:** Chip Huyen, *AI Engineering* — the single best structured spine. Everything else has a strong free path (see end).

---

## Phase 1 — Evals & Production

*Build target: deploy your eval system (FastAPI + Langfuse + CI).*

### Read-first (~4h)

**[Hamel — LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)** · blog · 1.5h
*Extract:* (1) the error-analysis loop — open coding → axial coding → count per category → saturation; (2) why **binary judges beat 1–5 Likert**; (3) CI (cheap deterministic checks) vs production monitoring (async LLM-judge). *This is the eval bible; you already did the loop on real data — read to name what you did.*

**[Hamel — LLM-as-a-Judge / Critique Shadowing](https://hamel.dev/blog/posts/llm-judge/)** · blog · 1h
*Extract:* (1) the 7-step critique-shadowing method (one expert → pass/fail + written critique → critiques as few-shot → iterate to >90% agreement); (2) **calibrate with TPR/TNR, not raw agreement** (raw agreement misleads under class imbalance); (3) the two-step synthetic-data trick (tuples → separate prompt → natural query).

**[Langfuse — Observability overview](https://langfuse.com/docs/observability/overview)** · docs · 45m
*Extract:* (1) what a trace logs (exact prompt, response, tokens, latency, every tool step); (2) traces→sessions→observations data model; (3) async flush = no added latency. *Unlocks your Week-2 deploy.*

**[Pragmatic Engineer — guide to LLM evals](https://newsletter.pragmaticengineer.com/p/evals)** · article · 45m
*Extract:* the dev-facing framing of evals you'll reuse in interviews ("eval methodology is the new system design").

### Go deeper (optional)
- **[Hamel + Shreya — AI Evals for Engineers & PMs](https://maven.com/parlance-labs/evals)** **[paid]** — the definitive course (taught 700+).
- **W&B evaluation courses** (free) — fastest free eval reps.
- **[Three Gulfs primer](https://www.davidokpare.com/blog/a-primer-to-evals)** — Comprehension / Specification / Generalization mental model.

### Hands-on exercise (do alongside the build)
On your eval repo: (a) run open→axial coding on 30 of your 300 emails, produce a 5-category taxonomy with counts; (b) convert your faithfulness judge to also emit a **binary ship/no-ship**; (c) compute **TPR and TNR** of the judge against your 20-email golden labels (not just agreement). Write the numbers in the README.

### Self-test (answer aloud in <1 min each)
1. Why is binary scoring better than 1–5 for an LLM judge?
2. Your judge shows 95% agreement with the expert — why might that still be a bad judge?
3. What's the difference between a guardrail and an evaluator?
4. Why is a ~70% eval pass rate often healthier than ~100%?

**Done with Phase-1 study when** you can answer all four cold.

---

## Phase 2 — RAG (your #1 red zone; read the most here)

*Build target: hybrid RAG with an ablation table + calibrated RAG-triad.*

### Read-first (~6h)

**[Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)** · blog · 1h
*Extract:* (1) the technique — prepend a 50–100 token situating blurb before embedding *and* BM25; (2) the numbers — **−35%** (embeddings), **−49%** (+ contextual BM25), **−67%** (+ rerank) failure rate; (3) prompt caching makes it ~$1/M doc tokens. *Drives your Week-6 build.*

**[Jason Liu — Systematically Improving RAG](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/)** · blog · 2h
*Extract:* (1) **synthetic Q&A per chunk** = day-one eval with zero labels; (2) **segment, don't average** (70% overall recall hides 5% on your critical queries); (3) retrieval metrics are *leading* indicators — change → measure segmented → keep if significant. *This is the RAG mindset that separates pros.*

**[Building & Evaluating Advanced RAG (DeepLearning.AI)](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag)** · free course · 1.5h
*Extract:* (1) the **RAG triad** (context relevance, groundedness, answer relevance); (2) **sentence-window** + **auto-merging** retrieval; (3) how to wire TruLens evals.

**[Hybrid Search for RAG 2026](https://www.buildmvpfast.com/blog/hybrid-search-rag-vector-keyword-reranking-2026)** · guide · 45m
*Extract:* (1) why vector misses exact matches (codes/SKUs/acronyms — ~35% of support queries); (2) **RRF with k=60**; (3) **retrieve 20–50 → rerank → top 5–10**, with reranker options (Cohere / zerank-2 / open ms-marco-MiniLM <50ms CPU).

**[Ragas docs](https://docs.ragas.io/)** · docs · 45m
*Extract:* the 4 metrics + rough targets — faithfulness ~0.75, answer-relevancy ~0.8, context-precision ~0.7, context-recall ~0.8.

### Interview-prep reading (~1.5h) — direct 2026 topics
- **[RAG vs Long Context decision framework](https://open-techstack.com/blog/rag-vs-long-context-2026/)** — *"long context to reason over a bounded set; retrieval to decide the set"*; <200K-token KB → just stuff the prompt.
- **[Advanced RAG techniques (Atlan)](https://atlan.com/know/advanced-rag-techniques/)** — HyDE, CRAG, Self-RAG, GraphRAG, Agentic RAG: know each + when.

### Hands-on exercise
Build the ablation incrementally and record each row's numbers: (1) pure dense → (2) +BM25 hybrid (RRF k=60) → (3) +contextual retrieval → (4) +reranker. Measure recall@10 / MRR / NDCG@10 **per query-segment** (split your queries by type: exact-match vs conceptual vs multi-hop). The story "hybrid+rerank beat dense by X on segment Y" *is* your Post 2.

### Self-test (<1 min each)
1. When do you choose RAG over a 1M-token context window? When the reverse?
2. Why does hybrid beat pure vector — give a concrete query type each handles.
3. Why rerank a pre-filtered 20–50, not the whole corpus?
4. Retrieval metrics look fine but answers are wrong — where's the bug?
5. What does contextual retrieval fix, and roughly how much?

**Done with Phase-2 study when** you can answer all five and your ablation table has real per-segment numbers.

---

## Phase 3 — Agents (you build them; learn to evaluate them)

*Build target: trajectory-evaluated, guardrailed version of your cold-outbound agents.*

### Read-first (~4h)

**[Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** · blog · 1h
*Extract:* (1) workflow vs agent (and "find the simplest thing that works"); (2) the **5 workflow patterns** (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer); (3) the augmented-LLM building block + "poka-yoke" tools.

**[Anthropic — Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** · blog · 45m
*Extract:* (1) "smallest set of high-signal tokens"; (2) **context rot** (n² attention, recall degrades with length); (3) the three long-horizon techniques — compaction, note-taking, sub-agents (return 1–2k-token summaries).

**[Anthropic — Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** · blog · 45m
*Extract:* token-efficient, unambiguous tools; the "if a human can't pick the tool, neither can the agent" test.

**[AI Agents in LangGraph (DeepLearning.AI)](https://www.deeplearning.ai/courses/ai-agents-in-langgraph)** · free course · 2h
*Extract:* enough LangGraph (state, nodes, edges, persistence, HITL) to discuss it in interviews — it's the most-named framework in 2026 JDs.

**[OWASP — Top 10 for LLM Apps](https://owasp.org/www-project-top-10-for-large-language-model-applications/)** · reference · 30m
*Extract:* name **LLM06 (excessive agency)** and **LLM09 (misinformation)** + your mitigations (max steps, tool validation, HITL gates).

### Hands-on exercise
On your cold-outbound agents: (a) write **30 golden trajectories** (expected tool-call sequence per lead type); (b) build a trajectory judge that scores path correctness separately from final-output quality; (c) show the gap — how many cases pass on output but fail on trajectory (research says output-only over-passes by 20–40%).

### Self-test (<1 min each)
1. When should you NOT use an agent?
2. What's context rot and how do you fight it on a long-horizon task?
3. Why eval the trajectory, not just the final answer?
4. Name three guardrails against cascading agent failures.

**Done with Phase-3 study when** you can answer all four and your trajectory eval shows the output-vs-trajectory gap.

---

## Always-on (across all phases)

- **[Eugene Yan — Patterns for Building LLM Systems](https://eugeneyan.com/writing/llm-patterns/)** — the patterns reference; reread per phase.
- **[Chip Huyen — aie-book repo](https://github.com/chiphuyen/aie-book)** — free curated resource list + book support.
- **[Anthropic Engineering blog](https://www.anthropic.com/engineering)** — highest-signal eng writing in the space.
- **[50 AI Engineer interview questions 2026](https://www.interviewcoder.co/blog/ai-engineer-interview-questions)** — self-quiz weekly in Phase 4; explain aloud, don't memorize.

---

## Core papers (1 per phase, optional, compounding)

| Paper | Phase | Why |
|---|---|---|
| **Lost in the Middle** (Liu et al., arXiv 2307.03172) | 2 | why long-context degrades mid-prompt — the case for retrieval + reranking |
| **RAG** (Lewis et al., 2020) | 2 | the original; know where it started |
| **Who Validates the Validators?** (Shankar et al., 2404.12272) | 1 | criteria drift — why your eval criteria shift once you start grading |
| **ReAct** (Yao et al.) | 3 | reason+act loop — the base agent pattern |
| **Reflexion** (Shinn et al.) | 3 | self-reflection / retry loops |

Skim for the idea and the result, not every equation. One evening each.

---

## The minimal free path (budget = 0)

The entire roadmap is doable free. The only **[paid]** items (Chip Huyen's book, the Maven evals course) are accelerators. Free stack:
- **Spine:** aie-book repo + Eugene Yan + Anthropic eng blog.
- **Evals:** Hamel's blog + W&B free eval courses.
- **RAG:** Jason Liu's blog + DeepLearning.AI advanced-RAG + Ragas docs.
- **Agents:** Anthropic eng posts + DeepLearning.AI LangGraph.
- **LLMOps:** Langfuse docs.

That covers the full 2026 bar at zero cost. Buy the book only when you want one organized reference.

---

## Weekly study rhythm (fits 8h/week)

- **~2h reading** (the daily 15-min habit + one longer block) — always *into* the current build.
- **~6h building** — the deliverable is the point.
- **Sunday:** log what you read **and what it changed in your build.** If a source changed nothing, you read it passively — reread into the work.

*The deepest "studying" here is shipping a thing the source taught you to build, then writing publicly about what broke. read → build → measure → write is the whole curriculum.*

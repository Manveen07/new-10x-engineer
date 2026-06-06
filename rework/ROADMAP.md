# Roadmap v4 — Production AI Engineer (deep, research-grounded)

> Built from current (2025–2026) primary sources: Hamel Husain + Shreya Shankar on evals, Anthropic engineering (agents, context engineering, contextual retrieval), Jason Liu on RAG, and 2026 hiring/interview write-ups. Every technique below is specific and sourced; full source list at the end. This is both a **plan** (Part I) and a **technique reference you'll keep coming back to** (Part II — Appendices).

**Pace:** 8 hrs/week baseline; exams done, so at **12–15 hrs/week** the 18-week plan compresses to **~11–13 weeks**. Week-counts are "weeks at 8h," not calendar law.

**Mission:** Turn real production GTM + LLM experience into a **deployed, eval-backed, publicly documented** portfolio that clears the 2026 AI-engineer bar — and run the job funnel in parallel.

---

## The 2026 bar (what hiring actually rewards)

- **Eval literacy is the #1 "this person actually built with LLMs" signal.** "Eval methodology is the new system design" — expect ≥1 interview round on building a golden set, running LLM-as-judge, and catching regressions before prod.
- **RAG is the baseline, not a niche.** *"Design a RAG system for a customer-support chatbot"* is the single most common opening interview question.
- **Production ownership is the #1 differentiator** — not model knowledge. Strong candidates have *stories* about systems breaking (drift, bad retrieval, latency spikes, cascading tool failures) and how they fixed them. "If a candidate has no stories about systems breaking in production, they haven't run systems in production."
- **Cost modeling is underrated in interviews, over-indexed on the job.** Be able to estimate a 10-turn agent loop's cost at 8K-in/1K-out per turn.
- **Recruiters ask for links, not resumes.** Deploy every project to a public URL; 2–3 polished deployed projects beat 10 unfinished.

Your three projects map onto this exactly: **eval system (Phase 1) + RAG app (Phase 2) + agent system (Phase 3)** — and the eval system gives you the rare skill most applicants lack.

---

## Already banked (demonstrate, don't re-learn)

| Skill | Proof |
|---|---|
| Error analysis + failure taxonomy (the most-skipped eval step) | count/group/name bug → Rule 17 |
| **Calibrated** LLM-as-judge | 100% agreement on 20-email/124-claim golden set |
| Golden dataset + faithfulness scoring | 300-email run, committed report |
| Structured outputs, tool use, multi-agent orchestration | cold-outbound system |
| Production GTM automation | Precise Leads + Caprae |

Hamel/Shreya spend **60–80% of dev time on error analysis + eval** and call it "the most important activity in evals." You've done it on real data. That's ahead of most applicants — the plan banks it and redirects to your real gaps: **RAG, deployment/Python rigor, cost modeling.**

---

# PART I — THE PHASE PLAN

## Phase 1 — Package & Deploy the Eval System

**Weeks 1–4.** Convert the eval work you already built into a deployed, traced, tested, public Project 1. Fastest credibility because the substance exists.

**Study (light — reinforce + deploy):** Hamel `evals-faq` + `llm-judge` (re-read with your harness open); Chip Huyen *AI Engineering* eval+deploy chapters; FastAPI docs; Langfuse observability overview. → *Appendix A (evals), D (deploy).*

| Wk | Build / ship | Concrete spec (from research) | Done when |
|---|---|---|---|
| 1 | Backfill `PROGRESS.md`; refactor eval module to clean Python. | type hints, pydantic schemas, `pytest` on scoring+gating, structured logging, config. Add a **binary "ship/no-ship" judge head** beside the 3-label faithfulness (Hamel: binary > Likert). | tests green, module typed |
| 2 | Wrap as **FastAPI** `POST /score`; Docker; deploy → live URL. | add **Langfuse tracing** to every judge call: log exact prompt, response, token usage, latency, tool steps. SDK flushes async (no added latency). | public URL scores; traces visible |
| 3 | Add **2nd axis** quality rubric + **GitHub Actions CI gate**; add **cost-per-email**. | CI dataset = small (~100 ex) + regression tests for past bugs; favor cheap deterministic checks in CI, LLM-judge async/nightly. Fail build if faithfulness drops. Re-validate judge with **TPR + TNR on a held-out set** (not raw agreement). | CI runs on push; cost reported |
| 4 | README to standard + **Post 1**. | problem, architecture diagram, failure modes, eval+calibration results (TPR/TNR), cost/latency, iteration log, demo GIF. | repo public, README done, post live |

**Deliverable:** Project 1 — deployed, traced, tested, documented eval system.
**Interview concepts to own:** error analysis as the core activity; binary vs graded judges; calibration via TPR/TNR (why raw agreement misleads under class imbalance); guardrails (sync, ms, deterministic) vs evaluators (async, nuanced); cost-per-task; why a ~70% eval pass rate is healthier than ~100%.
**Behind if:** no live URL, no CI gate, no Langfuse traces, repo not public by Wk 4.
**Closes:** deployment, Python testing rigor, observability, public footprint — four gaps in one phase.

---

## Phase 2 — RAG, Done Properly (your #1 red zone)

**Weeks 5–10.** RAG is *the* most in-demand 2026 skill and your weakest. Goal: **measure retrieval quality and defend every design choice.** Anchor to your real GTM/Clay data. This phase is deliberately read-heavy.

**Study (read before building):** Anthropic *Contextual Retrieval*; Jason Liu *Systematically Improving RAG*; DeepLearning.AI *Building & Evaluating Advanced RAG* (the RAG triad); Ragas docs. → *Appendix B (the full RAG playbook).*

The default production pipeline you're building toward (Appendix B has the detail):
`query → (optional rewrite/HyDE) → [BM25 top-20] + [vector top-20] → RRF merge (k=60) → ~top-30 → cross-encoder rerank → top 5–10 → LLM`, with **contextual retrieval** at index time and **auto-merging chunks** (~512–800 tokens, minimal overlap). Adds ~200–400ms.

| Wk | Build / ship | Concrete spec | Done when |
|---|---|---|---|
| 5 | Postgres + **pgvector**; ingest a real corpus; clean ingestion. | recursive chunking ~512 tokens (the systematic default); **skip overlap** (Jan-2026 analysis: no measurable benefit, raises cost); log everything to Langfuse. | retrieve top-k end-to-end |
| 6 | **Contextual retrieval** + **hybrid (dense + BM25, RRF k=60)**. | contextual retrieval prepends a 50–100 tok situating blurb before embedding → up to **−35%** retrieval failures (embeddings) / **−49%** (+ contextual BM25); use prompt caching to contextualize at **~$1/M doc tokens**. Hybrid is the default, not an upgrade. | both paths return + logged |
| 7 | **150 synthetic query–chunk eval pairs** (LLM-gen, hand-verify a sample). Measure **recall@10, MRR, NDCG@10** per variant — **segment, don't average** (Jason Liu). | measure retrieval **first** (~70% of RAG failures are retrieval, not the LLM). Targets: precision@5 > 0.6, recall@10 > 0.8, MRR > 0.5, NDCG@10 > 0.7. | metrics reproducible *per query-segment* |
| 8 | Add a **cross-encoder reranker**; build the **ablation table**. | **retrieve 20–50 → rerank → top 5–10** (the sweet spot; 5 misses best, 200 wastes latency). Reranking alone took Anthropic's failure rate to **−67%**; on hard sets it 3×'d nDCG by reordering the *same* candidates. Cohere (battle-tested) or open `ms-marco-MiniLM-L-6-v2` (<50ms CPU, free). | table: dense vs BM25 vs hybrid vs +rerank |
| 9 | **Cited generation** + the **RAG triad / Ragas**, calibrated against ~30 hand labels. | triad = context relevance + groundedness + answer relevance (reference-free). Ragas targets: faithfulness ~0.75, answer-relevancy ~0.8, context-precision ~0.7, context-recall ~0.8. Decompose answer → atomic claims → per claim "supported/contradicted/silent." | answers cite sources; judge calibrated |
| 10 | Deploy (FastAPI + Langfuse + **cost analysis**); **Post 2: the ablation post.** | report $/query + latency; two-tier eval (CI golden set <$0.10 + nightly Ragas). | live URL + ablation post; tag Clay community |

**Deliverable:** Project 2 — deployed hybrid RAG with a defensible ablation table and calibrated generation evals.
**Interview concepts to own:** the **RAG-vs-long-context decision** (long context to reason over a bounded set; retrieval to *decide* the set; RAG wins on multi-user/permissions/changing-data/citations/sub-3s); why hybrid beats pure dense (exact-match: codes, SKUs, acronyms — ~35% of support queries); why rerank a pre-filtered set; contextual retrieval; segment-don't-average; the retrieval-vs-generation diagnosis matrix.
**Behind if:** no ablation table, uncalibrated Ragas, or you can't explain in 30s why hybrid+rerank beat dense on *your* data.
**Closes:** retrieval quality, embeddings/vector search, RAG evaluation — the core of the bar.

---

## Phase 3 — Agent Rigor (evaluate what you already build)

**Weeks 11–14.** You already *build* multi-agent systems — the gap is **evaluating and hardening** them. Don't learn agents from zero; learn trajectory evals, context engineering, and orchestration discipline on a system you run.

**Study:** Anthropic *Building Effective Agents* + *Effective Context Engineering* + *Writing Tools for Agents*; DeepLearning.AI *AI Agents in LangGraph*; OWASP LLM Top 10. → *Appendix C (agents).*

| Wk | Build / ship | Concrete spec | Done when |
|---|---|---|---|
| 11 | Re-draw the cold-outbound system **workflow-first** (which nodes are deterministic; which one truly needs an agent). Add **Pydantic tool I/O, step budget, idempotency tokens**. | "agents are LLMs autonomously using tools in a loop" — use only where you can't predict the steps. Apply **context engineering**: smallest set of high-signal tokens; trim each agent's context; "poka-yoke" tools (e.g., force absolute paths). | orchestration typed, bounded, idempotent |
| 12 | Define **30+ golden trajectories**; build a **trajectory judge** + state-transition view; precision/recall on final output. | output-only eval passes **20–40% more cases than trajectory eval reveals** — score the *path* (right tool? right args? loop terminated?). Deterministic checks for tool-name/arg correctness (no LLM needed); LLM-judge only for subjective steps. ≥30 golden cases in CI. | trajectory eval scores paths |
| 13 | **Runtime guardrails** (promote the offline grounding gate to block contradicted outputs pre-queue); per-agent cost/latency. | name the mitigations: **max step limits, tool-call validation, human-approval gates for irreversible actions**; map to OWASP **LLM06 (excessive agency)** + **LLM09 (misinformation)**. | a contradicted output is blocked live |
| 14 | Deploy/document Project 3; **Post 3: trajectory evals.** | README + Langfuse traces of agent runs; one paragraph on cascading-failure prevention. | live/documented + post |

**Deliverable:** Project 3 — a trajectory-evaluated, guardrailed agent system.
**Interview concepts to own:** the 5 workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) and when each applies; workflow-vs-agent (when *not* to use an agent); context engineering (context rot, compaction, note-taking, sub-agents returning 1–2k-token summaries); trajectory vs output eval; cascading failures + guardrails.
**Behind if:** can't explain workflow-vs-agent in 30s, or the agent has no trajectory eval.
**Closes:** agent evaluation, guardrails/safety, production orchestration.

---

## Phase 4 — Portfolio Polish + Funnel Intensive

**Weeks 15–18.** Three deployed, eval-backed projects exist. Make them one coherent story; convert to interviews.

| Wk | Build / ship | Done when |
|---|---|---|
| 15 | Polish 3 READMEs to one standard; manveen.me shows all 3 above the fold; resume + LinkedIn + site use identical anchor phrases. | surfaces aligned |
| 16 | **2 AI system-design mocks + 1 project deep-dive.** Drill: design-a-RAG-system, design-an-eval-pipeline, design-an-agent, **cost math on a 10-turn loop**, the cold-outbound walkthrough. Self-quiz with the "50 questions 2026" list. | can whiteboard each in <10 min |
| 17 | 10 applications; 5 warm-intro asks; **Post 4: "What N weeks of part-time AI engineering looked like."** | 10 apps + 5 asks + post live |
| 18 | Interview buffer, follow-ups, negotiation; extend funnel if needed. | active pipeline |

---

## Job-search funnel (parallel from Week 1)

Your resume/positioning is done; the profile is interview-ready now. "Recruiters ask for links," so prioritize shipping deployed projects — but apply throughout.
- **Wk 1–4:** make `coldoutboundskills` public (sanitized — no client PII/keys), pin it + the case-study PDF to LinkedIn Featured. **5 apps/week** — Wellfound (Indian startups), Built In / Wellfound remote (international), Upwork + Clay community (freelance).
- **Wk 5–10:** 3–5 apps/week; one build-in-public post per phase; reply in Clay/LinkedIn threads (inbound > cold).
- **Wk 11–18:** intensify — warm intros, mocks, 10 apps/week, "open to work."

**Three markets, three angles:** freelance → "production GTM automation + evals" (fastest cash); Indian startups → shipped systems, ₹8–12 LPA realistic; international remote → lead with the eval/measurement story (push hardest after Phase 2).

---

## Weekly cadence (the operating system)

- **Daily 15 min:** one primary source (a Hamel / Jason Liu / Anthropic post or book section).
- **2× / week, 2h blocks:** the phase's build deliverable — anchored to a *shippable artifact*, never a topic.
- **Weekend block:** the harder build or the writing.
- **Every Sunday:** update `PROGRESS.md` — honest hours, what shipped **with a link**, what slipped, next 3 focuses, confidence check. **Missing two Sundays in a row is the canary.** Log what you *read* and what it *changed in your build* — if a source changed nothing, you read it passively.
- **Monthly:** self-review, publish/update, one community action, refresh LinkedIn.

**Rule: the post is the deadline, not the code.** If it can't be explained publicly, it isn't done.

---

## Confidence baseline (track the red zones)

| Axis | Now | Target | Where hours go |
|---|---:|---:|---|
| Evals | 4 | 5 | binary head + CI (P1) |
| RAG / retrieval | 1–2 | 4 | **primary focus (P2)** |
| Agents | 3 | 4 | trajectory evals (P3) |
| Production / deploy | 2 | 4 | **deploy + Langfuse every project** |
| Clean Python rigor | 2 | 4 | **tests/types/CI every repo** |
| Cost modeling | 1 | 3 | **$/task in every project** |
| Public footprint | 2 | 4 | one post per phase |
| Interview readiness | 3–4 | 5 | mocks (P4) |

---

## Readiness bar (v4 definition of "job-ready")

- [ ] **Three deployed projects**, each with eval suites, standard READMEs, Langfuse traces, cost/latency analysis, live URLs.
- [ ] Eval system: calibrated faithfulness (TPR/TNR) + quality rubric + CI gate.
- [ ] RAG system: ablation table + segmented retrieval metrics + calibrated RAG-triad/Ragas + reranking.
- [ ] Agent system: trajectory evals + runtime guardrails + cost-per-task.
- [ ] **Four public posts** on your domain; all surfaces aligned.
- [ ] Clean, typed, tested, CI'd code in every repo.
- [ ] Can explain in <1 min each: error analysis, judge calibration, RAG-vs-long-context, hybrid+rerank, workflow-vs-agent, trajectory eval, cost-per-task.
- [ ] **25+ applications, 5+ first-rounds**, 1+ warm intro.

---

# PART II — TECHNIQUE REFERENCE (the depth, by domain)

*Keep these open while building each phase. Every item is sourced in the list at the end.*

## Appendix A — Evals (Hamel + Shreya canon)

**The error-analysis loop (the core skill):**
1. **Dataset** — gather representative traces; bootstrap with synthetic data if you have none.
2. **Open coding** — a domain expert reads each trace and writes free-text notes ("journaling"). **Note the *first* failure** (upstream errors cascade).
3. **Axial coding** — group notes into a failure taxonomy; **count per category** ("the most important step"). LLM may assist grouping — *validate it* (it wrongly merges distinct issues).
4. **Iterate to theoretical saturation** — stop when ~20 traces in a row reveal no new category.
- **Cadence:** 30 min reviewing 20–50 outputs on any significant change; ≥100 fresh traces per cycle every 2–4 weeks; 10–20 traces weekly between cycles. Open-code 30–50 yourself before letting an LLM first-pass the grouping.
- **Smart sampling:** sort by length/latency/tool-call-count and review extremes; user-feedback signals; stratified by dimension; embedding clusters (oversample small ones for edge cases).

**LLM-as-judge — binary, not Likert:** adjacent Likert points (3 vs 4) are subjective and inconsistent; annotators cluster at the middle; binary forces you to define "good." Track gradual progress via **multiple binary sub-checks** ("4 of 5 expected facts present"), not a 1–5 score.
**Critique shadowing (7 steps):** pick one "benevolent dictator" domain expert → build dataset → expert gives **pass/fail + a written critique** → fix obvious bugs first → build the judge iteratively using critiques as **few-shot examples** (judge writes critique *then* verdict) → error-analyze the judge → add specialized judges only where needed. Honeycomb hit **>90% expert agreement in 3 iterations**.
**Calibration:** under class imbalance, raw agreement misleads — measure **TPR and TNR** (or precision/recall) on a held-out labeled set. Same model for task and judge is usually fine. Judge-prompt mistakes: no/terse critiques, missing external context, non-diverse examples.

**Synthetic eval data — structure with dimensions:** define axes (Hamel's B2C: **Features × Scenarios × Personas**); write ~20 tuples by hand first; **two-step generation** (LLM makes structured tuples → separate prompt turns each into a natural query) to avoid repetitive phrasing; only synthesize the *inputs*, run them through your real system. Start a judge dataset at ~30 examples; LLM-judge evaluators need 100+ labels + weekly upkeep.

**Three Gulfs (Shankar/Husain):** Comprehension (you↔data: read traces, open/axial code), Specification (intent↔prompt: always-do/never-do, schemas, examples), Generalization (prompt↔diverse inputs: RAG, decomposition, fallbacks). The loop: **Analyze → Measure → Improve → Repeat.** Common trap: mistaking a specification problem for a generalization one.

**CI vs monitoring:** CI = small (~100 ex) purpose-built set with regression tests for past bugs; favor cheap deterministic checks. Monitoring = async on sampled prod traces, reference-free LLM-judge, track confidence intervals. When prod surfaces a new failure, add it to CI. **Guardrails** (sync, ms, deterministic — PII/JSON/injection) ≠ **evaluators** (async, nuanced — factuality/completeness).
**Common mistakes:** optimizing for ~100% pass (aim ~70% to stress-test); generic off-the-shelf metrics; similarity metrics (ROUGE/BERTScore) for app outputs; eval-driven development (write evals for failures you *discover*, not imagine); outsourcing annotation; an LLM doing the initial open coding.
**Tools:** Ragas (RAG eval), DeepEval (pytest-style, 50+ metrics, CI), Langfuse (OSS observability), Braintrust (experiment/regression), LangSmith (LangChain), Phoenix (OTel). Highest-ROI: a **custom annotation UI** (hotkeys, domain rendering, progress) — teams with one iterate ~10× faster. Store prompts in **Git**, not a vendor UI.

## Appendix B — RAG (the production playbook)

**Chunking:** recursive splitter is the default (preserves structure); **auto-merging/hierarchical** (small chunks to *find*, parent chunks to *understand*) is the most-adopted production pattern. Start ~512 tokens; Anthropic used ~800. A Jan-2026 analysis: **overlap gave no measurable benefit**; a **"context cliff" ~2,500 tokens**; sentence chunking ≈ semantic up to ~5k tokens at lower cost. Always evaluate per corpus.
**Contextual retrieval (Anthropic):** prepend a 50–100 token situating blurb to each chunk before embedding *and* BM25 indexing. Failure-rate (1−recall@20) cuts: embeddings **−35%**, + contextual BM25 **−49%**, + reranking **−67%**. Cost ~**$1.02/M doc tokens** with prompt caching (load doc into cache once, reference per chunk).
**Hybrid search:** vector misses exact matches (error codes, SKUs, acronyms, names — ~35% of support queries); BM25 catches them (k1=1.2, b=0.75). Combine with **RRF (k=60)** — rank-based, avoids incompatible-scale problems — or weighted (start 0.7 vector / 0.3 keyword, normalize first; better: shift toward keyword when a code/SKU pattern is detected).
**Reranking:** cross-encoders score (query, doc) jointly; **retrieve 20–50 → rerank → top 5–10.** Measured: Success@1 +17%, nDCG@10 +15% (Weaviate/BEIR); 3× nDCG on reasoning-heavy sets. Cohere (battle-tested), ZeroEntropy zerank-2 (fast/cheap), or open `ms-marco-MiniLM-L-6-v2` (<50ms CPU, free). Pipeline adds ~200–400ms.
**Embeddings (2026 MTEB leaders):** Gemini Embedding 001 (#1 English, 768/1536/3072 dims), Qwen3-Embedding-8B (#1 multilingual, self-host), Voyage-3-large, OpenAI text-embedding-3-small (best price/perf). Matryoshka dims let you trade accuracy for storage.
**Evaluation:** measure **retrieval first** (~70% of failures are retrieval). Retrieval metrics + targets: precision@5 > 0.6, recall@10 > 0.8, MRR > 0.5, NDCG@10 > 0.7, hit rate. Generation: **RAG triad** (context relevance, groundedness, answer relevance — reference-free) or **Ragas** (faithfulness ~0.75, answer-relevancy ~0.8, context-precision ~0.7, context-recall ~0.8). **Diagnosis matrix:** low retrieval+low gen → fix retrieval; high retrieval+low gen → prompt/LLM problem. **Two-tier CI:** golden 50–100 queries (precision/recall, <$0.10, <2 min) + nightly full Ragas with a cheap judge ($2–5).
**RAG vs long context:** <200K-token KB → just stuff the prompt (Anthropic's own rule) with caching; large/changing/multi-user/needs-citations → RAG; hard multi-doc reasoning → hybrid (retrieve a small set, reason over it in long context). Beware "lost in the middle."
**Advanced patterns:** **HyDE** (LLM drafts a hypothetical answer, embed *that* — +20–40% precision on dense corpora; "if you add one thing, add HyDE"); **CRAG** (grade retrieved docs, re-query or web-fallback if weak — high-stakes domains); **Self-RAG** (reflection tokens; needs fine-tuning); **GraphRAG** (entities+relations, multi-hop); **Agentic RAG** (decision loop: sufficient? re-query? tool?). **Query rewriting/expansion** is the first-line fix for vocabulary mismatch.
**Vector DBs:** **pgvector** is the right default for ~70% of agent workloads (<10M vectors, already on Postgres); Qdrant (fastest filtered), Weaviate (best native hybrid via one `alpha`), Pinecone (zero-ops), Milvus (billion-scale).
**Jason Liu's flywheel:** synthetic Q&A per chunk = day-one eval with zero labels; **segment, don't average** (70% overall recall hides 5% on critical multi-hop/date queries); retrieval metrics are *leading* indicators; change → measure segmented metrics → keep if significant.

## Appendix C — Agents (Anthropic canon)

**Workflow vs agent:** workflows = LLMs/tools on predefined code paths (predictable); agents = LLMs dynamically directing their own tool use in a loop (flexible, costlier). Rule: find the simplest thing that works; "for many apps, a single optimized LLM call with retrieval + examples is enough." Agents only where steps are unpredictable and the environment is trusted/sandboxed.
**5 workflow patterns:** (1) **prompt chaining** (fixed sequential steps + gates), (2) **routing** (classify → specialized handler; route easy→cheap model, hard→strong model), (3) **parallelization** (sectioning = independent subtasks; voting = same task ×N), (4) **orchestrator-workers** (central LLM decides subtasks at runtime), (5) **evaluator-optimizer** (generate ↔ critique loop). Build agents from the **augmented LLM** (retrieval + tools + memory). Invest in the **agent-computer interface** as much as the prompt; "poka-yoke" tools (Anthropic forced absolute filepaths to kill relative-path errors).
**Context engineering:** "the smallest set of high-signal tokens that maximize the desired outcome." **Context rot** — recall degrades as tokens grow (n² attention). System prompts at the "right altitude" (between brittle if-else and vague). Bloated tool sets are the most common failure ("if a human can't pick the tool, neither can the agent"). **JIT retrieval** — keep lightweight identifiers (paths/queries), load at runtime (Claude Code uses glob/grep, not pre-loaded dumps). Long-horizon: **compaction** (summarize a near-full window, keep decisions/unresolved bugs + recent files), **structured note-taking** (write to `NOTES.md` outside context), **sub-agents** (clean context each, return 1–2k-token summaries).
**Agent evaluation:** output-only eval passes **20–40% more cases than trajectory eval reveals.** Need both: trajectory (right tool? right args? loop terminate?) + final-response quality. **Golden trajectories** = expected tool-call sequence + intermediate responses; ≥30 hand-curated cases in CI per PR, 50–100 as an anchor set. Tool-call accuracy = deterministic checks (no LLM); benchmarks BFCL (function calling), TRAJECT-Bench. LLM-judge only for subjective dimensions, with a rubric + task description + full trajectory.
**Frameworks 2026:** **LangGraph** (stateful production, persistence, HITL — learn it for interviews even if you prefer your own orchestration); **CrewAI** (fast role-based prototyping); **AutoGen/AG2** (research/multi-agent conversations); **OpenAI Agents SDK** (GPT-centric, native sandboxing/MCP); **Pydantic AI** (type-safe, FastAPI-style). **7 patterns** (combined in production): ReAct, tool use, planning, reflection, multi-agent, agentic RAG, human-in-the-loop.

## Appendix D — LLMOps, deployment, interviews

**Tracing:** a trace = one request's full lifecycle (exact prompt, response, tokens, latency, every tool/retrieval step), nested as traces→sessions→observations; group multi-turn as sessions; split dev/staging/prod; SDKs flush async (no latency). **Tools:** Langfuse (MIT, most permissive OSS, self-host <30 min, OTel), Phoenix (OSS, OTel-native), LangSmith (closed, LangChain-native), Braintrust (closed, eval-first regression), W&B Weave (closed, prompt versioning). **Monitor:** hallucination rate (faithfulness), no-retrieval rate, drift, cost/trace, latency, prompt regression (version prompts, run golden sets before shipping).
**Deployment (FastAPI for LLM apps):** stream tokens via SSE + `StreamingResponse`; long jobs return a job ID and process async (Redis + Celery/RQ for retries/queues); **load models once at startup** (not per request); Gunicorn + Uvicorn workers. Platforms: **Modal** (AI-first, GPU, HF→endpoint in minutes), **Railway** (persistent containers, workers, autoscale), **Fly.io/Render** (managed supervision).
**Interviews:** 5 clusters cover ~90% — LLM/transformer basics, RAG architecture, agentic systems, prompt-eng + evals, LLM system design. "Design a RAG system for X" is the most common opener — be fluent on ingestion→chunking→embedding→retrieval→reranking→eval. "Eval methodology is the new system design." Weave **token-cost estimation + latency budgets** into whiteboard architecture. Strong-candidate signals: production-failure stories, cost modeling (estimate a 10-turn loop), failure-mode fluency (cascading failures + max-step/validation/HITL guardrails). Prep: ship one end-to-end RAG app; be fluent in one agent framework + one eval tool and actually run faithfulness checks on real outputs.

---

## The honest rule (the point of this repo)

No fake claims. No AI fluff. Every project: a real problem, real inputs, real outputs, measurable quality checks. Every automation: cost, failure cases, anti-hallucination controls. Every project explainable in an interview. *This roadmap reflects what you've actually done — and what you haven't yet.*

---

## Sources

**Evals:** [Hamel — evals FAQ](https://hamel.dev/blog/posts/evals-faq/) · [Hamel — LLM-as-Judge (Critique Shadowing)](https://hamel.dev/blog/posts/llm-judge/) · [Hamel — Field Guide](https://hamel.dev/blog/posts/field-guide/) · [Three Gulfs primer](https://www.davidokpare.com/blog/a-primer-to-evals) · [Who Validates the Validators? (criteria drift)](https://arxiv.org/abs/2404.12272) · [Hamel + Shreya AI Evals course](https://maven.com/parlance-labs/evals)
**RAG:** [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) · [Jason Liu — Systematically Improving RAG](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/) · [Hybrid Search for RAG 2026](https://www.buildmvpfast.com/blog/hybrid-search-rag-vector-keyword-reranking-2026) · [RAG Evaluation 2026](https://www.buildmvpfast.com/blog/rag-evaluation-retrieval-quality-answer-accuracy-2026) · [TruLens RAG triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) · [Ragas docs](https://docs.ragas.io/) · [RAG vs Long Context 2026](https://open-techstack.com/blog/rag-vs-long-context-2026/) · [Advanced RAG (Atlan)](https://atlan.com/know/advanced-rag-techniques/) · [Vector DB benchmarks 2026](https://callsphere.ai/blog/vector-database-benchmarks-2026-pgvector-qdrant-weaviate-milvus-lancedb)
**Agents:** [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) · [Anthropic — Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Anthropic — Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) · [Confident AI — agent eval guide](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) · [LangChain — trajectories vs outputs](https://www.langchain.com/articles/llm-evaluation-framework) · [Agent frameworks compared 2026](https://www.channel.tel/blog/ai-agent-frameworks-compared-2026-what-ships)
**LLMOps/deploy:** [Langfuse — observability](https://langfuse.com/docs/observability/overview) · [Observability platforms 2026](https://laminar.sh/article/2026-04-23-top-6-agent-observability-platforms) · [FastAPI for LLMs](https://www.zignuts.com/blog/fastapi-deploy-llms-guide) · [LLMOps roadmap 2026](https://machinelearningmastery.com/the-roadmap-for-mastering-llmops-in-2026/)
**Books/canon:** [Chip Huyen — AI Engineering](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) · [aie-book repo](https://github.com/chiphuyen/aie-book) · [Eugene Yan — LLM patterns](https://eugeneyan.com/writing/llm-patterns/)
**Hiring/interviews:** [Digital Applied — 2026 skills](https://www.digitalapplied.com/blog/ai-developer-hiring-skills-that-matter-2026) · [AI engineer interview questions 2026](https://www.interviewcoder.co/blog/ai-engineer-interview-questions) · [RAG interview questions](https://www.datacamp.com/blog/rag-interview-questions) · [5 portfolio projects that get hired](https://dev.to/klement_gunndu/5-ai-portfolio-projects-that-actually-get-you-hired-in-2026-5bpl) · [AI system design guide](https://github.com/ombharatiya/ai-system-design-guide)

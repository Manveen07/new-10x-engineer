# Plan — Months 2 to 6 (detailed feedback + thought process)

Companion to [ROADMAP.md](./ROADMAP.md). Month 1's day-by-day lives in [month-1/FINISH-PLAN.md](./month-1/FINISH-PLAN.md). This file holds the **detailed forward plan for Months 2–6 plus the reasoning behind it** — so future-you knows not just *what* to do but *why*, and remembers where the thinking came from. Months 2–6 stay principle-led, not date-locked; each month gets its own day-by-day file (like FINISH-PLAN) only when you reach it, built from what actually shipped the month before.

---

## Where we came from (the thought process, preserved)

Decisions made and *why*, so the plan never drifts back into the old shape:

1. **Original plan was for the wrong person.** v1 targeted a senior Bengaluru GTM engineer ("Avi") with years of Clay production traces. Manveen is a final-year BTech with shipped GenAI projects (PresentAI, AsanaBot) + two internships + rusty hands-on coding. Rebuilt around *that*.
2. **Target role = GenAI / LLM Application Engineer with agent tilt.** Highest-volume junior bucket in 2026; only bucket where a Tier-2 fresher with a strong public portfolio competes against MS/IIT ML candidates. Bar is "ship working LLM features with evals," not "derive backprop."
3. **Funnel = US-remote primary, India backup.** Manveen raised this himself; research validated it — his GTM-engineer outbound skill (Precise Leads) is a wedge most AI candidates lack. Mercor (interview = your OSS contributions) + HN/Wellfound/YC + direct outbound to just-raised US AI founders.
4. **Three flagship projects:** leadlens (classifier + evals, M1–2) → docsight (production RAG, M3–4) → reposcout (agent + MCP, M5). Each deployed, eval-backed, documented.
5. **leadlens pivoted staffing-firm → AI-JD classifier** (Manveen's call). Reason: the 50 staffing traces were 50/50 pass — no hard failures, low engagement. JD classification = real failures + a tool he'll actually use for his own Month 6 funnel (dogfood).
6. **The discovered pattern — schema-as-eval-spec.** Every recurring failure mode has a corresponding Pydantic field that forces the model to type the dimension explicitly, killing the failure by construction. Proven 3×: `min_length` on reasoning (F-003 hardcoded confidence), `stack_unspecified: bool` (F-004 thin extraction), `min_length` on judge critique (critique-shadowing). **This is Manveen's signature technique — lead with it in interviews and the blog.**
7. **Learning is the point, not the calendar.** Manveen pushed back twice on task-mode rushing. Every session runs revise → build → recall. Compounding over deadlines.

**The compounding thesis:** you are not learning five separate things. You are learning **one discipline — measure-first, eval-driven engineering — in five shapes.** Classifier evals (M1–2) → retrieval evals (M3–4) → agent trajectory evals (M5) → funnel-as-eval (M6). The schema-as-eval-spec instinct carries through all of them.

---

## Month 2 — Ship leadlens (deploy + observe + scale the golden set)

**Window:** ~2026-06-22 → 2026-07-19. **Theme:** turn the working-on-laptop classifier into a deployed, observed, production-shaped artifact.

**Why this month:** every 2026 JD says "end-to-end deployment, not a demo" and "recruiters ask for links." A classifier that only runs locally is invisible. The deepest concept here: **what actually separates "runs on my laptop" from "runs in production"? Answer = observability + reliability + a public URL.**

**Learning goals (concepts to own):**
- Observability: what a trace captures (prompt, response, tokens, latency, every step) and why non-deterministic systems are undebuggable without it.
- Deployment shapes: serverless (Modal) vs always-on container; cold starts; load-once-at-startup.
- Two-tier eval: cheap deterministic CI gate + nightly LLM-judge.
- Golden-set discipline: stratified sampling, label hygiene (you already learned 2/10 first-pass labels were wrong).

**Build deliverables:**
- Expand golden set 20 → 100 JDs (source real ones from HN/Wellfound/YC as they post).
- Wrap classifier + judge as a FastAPI `POST /classify` + `POST /judge`; Docker; deploy on Modal → live URL.
- Langfuse tracing on every model call (replace the local `jd-metrics.jsonl` hand-roll).
- `pytest` eval suite that runs the golden set + asserts category-accuracy ≥ threshold = CI gate (GitHub Actions).
- README to standard: architecture diagram, "where it fails," eval table, $/call, p50/p95 latency.
- 3-min Loom walkthrough.
- Blog post 2: "Deploying leadlens — what laptop→production actually costs."

**Blind spots closed:** FastAPI, Docker, Modal deploy, Langfuse, CI/CD, async parallel calls (use the kata-02 `asyncio.gather` to drop the 5.4s/JD serial latency).

**Study (researched):** [FastAPI docs](https://fastapi.tiangolo.com/), [Modal examples](https://modal.com/docs/examples), [Langfuse observability](https://langfuse.com/docs/observability/overview), DeepLearning.AI *Building Evaluations of LLM Apps*.

**Success bar:** live URL anyone can hit; 100-JD golden set; CI gate green; Langfuse traces visible; Loom + post 2 live.

**Compounds into M3:** the deploy + Langfuse + eval-CI muscle gets reused wholesale on docsight. You build the production scaffold once on the simpler project, reuse it on the harder one.

---

## Month 3 — RAG fundamentals + docsight design (your #1 red zone)

**Window:** ~2026-07-20 → 2026-08-16. **Theme:** learn the retrieval stack deeply *before* building. RAG is the most-asked 2026 interview topic ("design a RAG system for X") and Manveen's weakest area (self-rated 1–2/5). Graduation lands mid-month — keep weekends protected, weekdays light.

**Why this month:** "design a RAG system" is the single most common interview opener. You can't fake it. And the lesson that separates juniors from pros: **~70% of RAG failures are retrieval, not the LLM — so measure retrieval first.**

**Learning goals (concepts to own):**
- Chunking strategies (recursive default ~512 tok; auto-merging; why overlap often adds nothing).
- Why hybrid beats pure dense (BM25 catches exact codes/SKUs/acronyms vector misses — ~35% of queries).
- Contextual retrieval (Anthropic: prepend situating blurb → −49% retrieval failures, −67% with rerank).
- Reranking (cross-encoder; retrieve 20–50 → rerank → top 5–10).
- RAG-vs-long-context decision (the interview favorite).
- **Learning frame: build RAG by failing.** Start with `np.dot(query, chunks)` simplest possible, watch it miss exact matches, then layer BM25 → RRF → rerank → contextual, each layer earning its place by killing a *measured* failure. Don't copy a tutorial pipeline.

**Build deliverables:**
- Pick a real corpus (recommended: Anthropic SDK + LangGraph + LiteLLM docs — public, mixed prose/code/changelogs, useful to other engineers).
- Postgres + pgvector running in Docker Compose.
- docsight `DESIGN.md` (retrieval eval plan first, per Hamel — design the measurement before the pipeline).
- `git mv projects/gtm-clay-rag projects/docsight`.
- Open the OSS PR (Mercor's interview is your OSS contributions — start early). Target: Instructor / Langfuse / Ragas / simonw/llm / LiteLLM / PydanticAI.
- Blog post 3: "What I set up before writing a line of RAG code."

**Blind spots closed:** embeddings + vector search, chunking, pgvector, BM25, hybrid fusion, contextual retrieval, the 30-min LlamaIndex + 30-min Pinecone spikes (vocabulary for interviews even though you deploy pgvector).

**Study (researched):** [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval), [Jason Liu — Systematically Improving RAG](https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/), DeepLearning.AI *Building & Evaluating Advanced RAG*, [Ragas docs](https://docs.ragas.io/), [REFERENCE.md](./REFERENCE.md) Appendix B (your own cheat-sheet with the numbers).

**Success bar:** docsight DESIGN.md committed; pgvector retrieving end-to-end; OSS PR opened; can explain hybrid-beats-dense in 30 sec; post 3 live.

**Compounds into M4:** the retrieval-eval design you write here is what M4's ablation table measures.

---

## Month 4 — Ship docsight (the ablation table) + merge OSS PR + Mercor

**Window:** ~2026-08-17 → 2026-09-13. **Theme:** build, measure, deploy docsight. The headline artifact = a **defensible ablation table.**

**Why this month:** the ablation table is the single artifact that proves "I measured retrieval" vs "I vibed a vector DB." Hiring managers and Mercor reviewers screen for exactly this. The deepest lesson: **segment, don't average** — 70% overall recall can hide 5% recall on your critical query type.

**Learning goals (concepts to own):**
- Retrieval metrics: recall@k, MRR, NDCG@10 — and reading them *per query-segment*.
- The ablation discipline: pure dense vs BM25 vs hybrid vs +rerank vs +contextual, each row measured.
- Generation evals: RAG triad / Ragas (faithfulness, answer-relevance, context-precision), calibrated against ~30 hand labels (reuse the critique-shadowing + TPR/TNR muscle from leadlens judge v1).
- The retrieval-vs-generation diagnosis matrix (where's the bug?).

**Build deliverables:**
- Ingestion + contextual retrieval + hybrid (RRF) + reranker.
- 150 synthetic query–chunk eval pairs (LLM-gen, hand-verify a sample — the Jason Liu day-one-eval-with-zero-labels trick).
- The ablation table with segmented metrics.
- Cited generation + calibrated Ragas.
- Deploy on Modal (Docker + FastAPI + Langfuse). $/query + latency.
- Merge the OSS PR (get the maintainer thank-you screenshot for portfolio).
- **Apply to Mercor** with portfolio in hand. + 5 HN/YC/Wellfound applications.
- Blog post 4: "Contextual retrieval on real OSS docs — a measured ablation."

**Blind spots closed:** retrieval measurement, RAG evaluation, reranking, Ragas calibration — the core of the 2026 bar.

**Study:** same as M3 carried forward + [Lost in the Middle](https://arxiv.org/abs/2307.03172) (figures only), Hamel on RAG evals.

**Success bar:** deployed docsight + ablation table + calibrated Ragas + OSS PR merged + Mercor application in. Can explain in 30 sec why hybrid+rerank beat dense *on your data*.

**Compounds into M5:** retrieval becomes a *tool* the agent calls. docsight gets wrapped as an MCP tool inside reposcout.

---

## Month 5 — Ship reposcout (agent + MCP) + outbound funnel goes live

**Window:** ~2026-09-14 → 2026-10-11. **Theme:** an agent that composes leadlens + docsight as tools via MCP. The 2026 differentiator. Outbound funnel turns on in parallel.

**Why this month:** agents are the highest comp ceiling; MCP servers are table-stakes in 2026 JDs (Sarvam FDE lists them). The lesson: **agents are compositions of what you already built — don't learn LangGraph for its own sake.** Start with a raw `while loop + tool calls`, find the ONE node that genuinely needs dynamic decisions, only then reach for a framework.

**Learning goals (concepts to own):**
- Workflow vs agent (Anthropic: "find the simplest thing that works"); the 5 workflow patterns.
- Trajectory evals — output-only eval passes 20–40% more cases than the trajectory warrants; score the *path*, not just the answer (reuse your eval muscle, new target).
- Context engineering: context rot, compaction, sub-agents, JIT retrieval.
- MCP: how a server exposes tools to Claude Desktop / Cursor.
- Guardrails: step budgets, idempotency, HITL gates (OWASP LLM06/LLM09).

**Build deliverables:**
- reposcout `DESIGN.md` — workflow-first sketch; identify the one agentic node.
- Raw orchestration: Pydantic tool I/O, step budget (20), idempotency tokens.
- Wire leadlens + docsight as MCP tools via the `mcp` Python SDK.
- 30 golden trajectories + a trajectory judge + state-transition view.
- Deploy + register MCP server (demoable from Claude Desktop — GIF in README).
- Blog post 5: "Workflow first, agent second, MCP always."
- **Outbound goes live:** 50 just-raised US AI startups sourced; 50 Insight Emails sent (your Precise Leads skill, pointed at your own funnel). 1 lightning talk recorded.

**Blind spots closed:** agent design, trajectory evaluation, MCP servers, context engineering, runtime guardrails, one agent framework (LangGraph) for interview fluency.

**Study (researched):** [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents), [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [MCP docs](https://modelcontextprotocol.io), Anthropic Academy *Agentic AI*, [REFERENCE.md](./REFERENCE.md) Appendix C.

**Success bar:** MCP server demoable from Claude Desktop; trajectory eval scoring paths; 50 outbound sent; lightning talk recorded; post 5 live.

**Compounds into M6:** three deployed eval-backed projects + MCP + OSS PR = the portfolio the funnel sells. Outbound mechanics already warm.

---

## Month 6 — Run the funnel (as an evaluation problem)

**Window:** ~2026-10-12 → 2026-11-08. **Theme:** portfolio is the asset; convert it to interviews + offers.

**Why this month:** the funnel is not apply-and-wait. The reframe that makes it work: **treat the job search like another eval problem** — instrument response rate per channel, A/B test pitch versions, look at *segmented* conversion (which channel, which pitch, which role-type converts). Apply the measure-first discipline you built on leadlens to your own career funnel.

**Learning goals (concepts to own):**
- System-design interviews: doc-Q&A, classifier-with-handoff, eval-harness, MCP-server, agent — each whiteboardable in <10 min.
- Cost modeling live (estimate a 10-turn agent loop) — interviewers screen for this.
- Production-failure storytelling — you have real ones (F-003 hardcoded confidence, F-006 scam under-call, the 2/10 label-error discovery). The #1 differentiator.
- Funnel instrumentation: channel → response → call → trial → offer, measured.

**Build / execute deliverables:**
- Resume rewritten around the 3 projects + production-eval framing (outcome language: "TPR 1.0 on a calibrated scam judge," not "used LangChain").
- 100+ outbound messages (cumulative); 25+ applications; reply to all responses <24h.
- 2 system-design mocks + 1 project deep-dive mock.
- 6 STAR stories drafted (the failure modes you actually found are the spine).
- Blog post 6: "What 6 months of part-time AI engineering actually looked like."
- Profiles updated: GitHub README, LinkedIn, X, Mercor — all "open to remote."

**Blind spots closed:** interview fluency, system design, cost-on-the-whiteboard, negotiation, funnel discipline.

**Study:** interview_prep_qa.md (drill all 5 clusters to 🟢), REFERENCE.md Appendix D, mock-interview practice.

**Success bar (the readiness bar):** 3 deployed eval-backed projects + MCP + merged OSS PR + 6 posts + GitHub daily-ish 6-month graph + 100+ outbound + 25+ apps + 5+ first-rounds + 1+ active offer cycle. Can explain in <1 min each: error analysis, judge calibration, RAG-vs-long-context, hybrid+rerank, workflow-vs-agent, trajectory eval, cost-per-task, schema-as-eval-spec.

---

## The through-line (re-read when lost)

| Month | Project | The one concept, in a new shape |
|---|---|---|
| 1 | leadlens | classifier evals — schema-as-eval-spec, critique-shadowing, TPR/TNR |
| 2 | leadlens deployed | production = observability + reliability + a URL |
| 3 | docsight design | measure retrieval *first*; build by failing |
| 4 | docsight shipped | segment, don't average — the ablation table |
| 5 | reposcout | agents = composition; trajectory evals; MCP |
| 6 | the funnel | the job search is itself an eval problem |

Measure-first, eval-driven engineering — learned once, applied six times. That consistency *is* the portfolio narrative, and the answer to "tell me how you work."

---

## How to use this file

- Re-read the top section ("Where we came from") whenever the plan feels like it's drifting — it's the anti-drift anchor.
- At the start of each month, turn that month's section into a day-by-day file like [month-1/FINISH-PLAN.md](./month-1/FINISH-PLAN.md), built from what actually shipped the prior month.
- Months are principle-led, not date-locked. If a month runs long, it carries — never skip the learning to hit a date. Compounding beats calendar.

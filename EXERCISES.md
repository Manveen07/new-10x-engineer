# Monthly Execution Checklist

Tick boxes as you go. End of each month, copy your unchecked items into the next month's "carry-over" section in [PROGRESS.md](./PROGRESS.md) and decide: do or drop.

The checklist is opinionated about *minimum* viable monthly output. If you finish more, great. If you finish less, the "Behind if" rows in [ROADMAP.md](./ROADMAP.md) tell you what's load-bearing vs nice-to-have.

---

## Month 1 — Code rebuild + eval foundations + leadlens design

**Window:** 2026-05-25 → 2026-06-21.

### Code rebuild (Track 1)
- [ ] Daily 30-min no-AI Python kata (Mon–Fri, 4 weeks = 20 sessions). Log in [PROGRESS.md](./PROGRESS.md).
- [ ] Install + use `uv`, `ruff`, `pytest`, `pre-commit`. Set up one Python project from scratch with all four.
- [ ] Write one nested Pydantic model + one Instructor extraction without AI (build muscle).
- [ ] Write three short scripts using `asyncio` / `httpx.AsyncClient` for parallel API calls.
- [ ] Write five pytest tests for an existing function in one of your old projects.
- [ ] Set up Cursor + Claude Code together as paired IDEs. Configure to refuse silent code writes (use chat, not in-line "accept all").

### Portfolio + writing setup
- [ ] Personal domain live (Quarto or Astro).
- [ ] Refresh AsanaBot README — problem, screenshots, live demo gif, "where it fails."
- [ ] Refresh PresentAI README — same treatment + screenshot of the running app.
- [ ] GitHub profile README with positioning + 3 pinned repos (AsanaBot, PresentAI, this roadmap repo for now — will become leadlens by Month 2).

### Eval foundations (Track 2)
- [ ] Re-read Hamel `evals-faq` end-to-end with your 50 traces open.
- [ ] Read Eugene Yan *Patterns for Building LLM-based Systems & Products*.
- [ ] Read Hamel `llm-judge`.
- [ ] Apply Three Gulfs framework to all 50 traces (open coding).
- [ ] Convert open-coding notes into an axial failure taxonomy (≥3 named failure modes).
- [ ] Build a Streamlit or FastHTML annotation viewer (~2 hrs).
- [ ] Calibrate first LLM-as-judge against your labels — target >90% agreement.

### leadlens design (Track 2/3)
- [ ] Draft `projects/business-classification-pipeline/DESIGN.md` (1–2 pages: schema, judges, eval plan, deployment shape).
- [ ] Sketch the architecture diagram (excalidraw → PNG → commit).

### Public footprint (Track 5)
- [ ] Publish blog post 1: "Open-coding 50 traces from a real classifier."
- [ ] Tweet thread + LinkedIn post when the blog post ships.

### Outbound prep (Track 6 — light)
- [ ] Follow 20 US AI engineers + 10 US AI founders on X. Reply substantively to 3 posts.

### Discipline
- [ ] Update [PROGRESS.md](./PROGRESS.md) every Sunday (non-negotiable).
- [ ] End-of-month review on the last Sunday.

---

## Month 2 — Ship leadlens

**Window:** 2026-06-22 → 2026-07-19.

### Code (Track 1, threaded)
- [ ] Continue daily 30-min no-AI kata.
- [ ] Use type hints throughout leadlens — `mypy --strict` runs clean.

### Build (Track 2)
- [ ] Watch DLAI *Improving Accuracy of LLM Applications* (1–2 hrs).
- [ ] Pydantic + Instructor schema for leadlens.
- [ ] Langfuse instrumentation from line one.
- [ ] Hand-label 100-JD golden dataset.
- [ ] First end-to-end run; confusion matrix v1.
- [ ] Three judge prompt iterations to >90% agreement.
- [ ] Cost + latency p50/p95 instrumentation.

### Ship (Track 1 + Track 5)
- [ ] Deploy on Modal. Live URL committed to README.
- [ ] README to standard (architecture, "where it fails," eval table, cost, latency).
- [ ] Record 3-min Loom walkthrough; link at top of README.
- [ ] Publish blog post 2: "Auditing my own LLM classifier."
- [ ] LinkedIn + X announcement with eval table screenshot.

### Outbound prep (Track 6)
- [ ] Save a list of 30 US AI founders/CTOs to a "future outreach" sheet. Don't email yet.

### Discipline
- [ ] Weekly `PROGRESS.md` updates.
- [ ] End-of-month review + Demo Day Loom.

---

## Month 3 — RAG fundamentals + docsight design + OSS PR opened

**Window:** 2026-07-20 → 2026-08-16. Mind exam load — see [ROADMAP.md](./ROADMAP.md).

### Read + Drill (Track 3)
- [ ] Anthropic *Contextual Retrieval* (Sept 2024) — read + implement on toy corpus.
- [ ] Greg Kamradt — *5 Levels of Text Splitting* notebook, run all five.
- [ ] Jason Liu — RAG complexity + search improvements posts.
- [ ] Hamel — RAG eval guidance.
- [ ] **30-min LlamaIndex spike** — one ingestion + one query notebook.
- [ ] **30-min Pinecone spike** — sign up, ingest 100 vectors, query.

### Design (Track 3)
- [ ] docsight stack decision committed to repo `STACK.md`.
- [ ] Local Postgres + pgvector running via Docker Compose.
- [ ] docsight `DESIGN.md` — corpus choice, chunking strategy, eval plan, deployment shape.
- [ ] `git mv projects/gtm-clay-rag projects/docsight`.

### OSS (Track 5)
- [ ] Pick OSS target repo (Instructor / Langfuse / Ragas / simonw/llm / LiteLLM / PydanticAI).
- [ ] Lurk in their issues + Discord for 1 week.
- [ ] Open a draft PR or an issue proposing the contribution. Get maintainer feedback.

### Public (Track 5)
- [ ] Publish blog post 3: "What I'm setting up before writing a line of RAG code."
- [ ] Announce on LinkedIn + X.

### Outbound prep (Track 6)
- [ ] Build the outbound target list infrastructure (Clay/Smartlead/n8n or simpler: a Google Sheet). Don't send yet.

### Discipline
- [ ] Weekly updates. Allow lighter weeks during exams; recover in Month 4.

---

## Month 4 — Ship docsight + merge OSS PR + Mercor application

**Window:** 2026-08-17 → 2026-09-13.

### Build (Track 3)
- [ ] Ingestion pipeline (chunking + contextual retrieval preprocessing).
- [ ] Dense retrieval + BM25.
- [ ] Hybrid via RRF.
- [ ] Generate 150 synthetic query-chunk eval pairs; hand-verify a 30-sample subset.
- [ ] Add reranker (Cohere or Voyage or local `bge-reranker`).
- [ ] Ablation table: pure dense vs BM25 vs hybrid vs hybrid+rerank vs hybrid+rerank+contextual.
- [ ] Measure recall@10, MRR, NDCG@10.
- [ ] Cited generation pipeline.
- [ ] Ragas faithfulness + answer relevance + context precision. Calibrate against 30 labels.
- [ ] $/query + p50/p95 latency.

### Ship (Track 1 + Track 5)
- [ ] Docker Compose for local dev (Postgres + pgvector + FastAPI).
- [ ] Deploy on Modal. Live URL.
- [ ] README to standard with ablation table prominent.
- [ ] Record 3-min Loom.
- [ ] Publish blog post 4: "Contextual retrieval on real OSS docs: a measured ablation."

### OSS (Track 5)
- [ ] Land OSS PR. Get a maintainer thank-you on Discord or in the merge comment — screenshot for portfolio.

### Outbound + funnel (Track 6)
- [ ] **Apply to Mercor** (work.mercor.com — Applied AI Engineer, India).
- [ ] Apply to 5 HN/YC/Wellfound listings.

### Discipline
- [ ] Weekly updates + end-of-month Demo Day Loom.

---

## Month 5 — Ship reposcout (agent + MCP) + outbound starts

**Window:** 2026-09-14 → 2026-10-11.

### Read (Track 4)
- [ ] Anthropic *Building Effective Agents* (Dec 2024).
- [ ] Anthropic *Effective Context Engineering for AI Agents* (Sept 2025).
- [ ] Skim Letta and PydanticAI README + one example notebook.

### Build (Track 4)
- [ ] reposcout `DESIGN.md` — workflow-first sketch, identified agentic node.
- [ ] Raw orchestration: Pydantic tool I/O, step budget = 20, idempotency tokens.
- [ ] Wire leadlens + docsight as MCP tools using `mcp` Python SDK.
- [ ] GitHub API integration (`PyGithub` or `httpx`).
- [ ] 30 golden reference topics.
- [ ] Trajectory judge prompt + state-transition matrix.
- [ ] Precision/recall evals on final repo lists.

### Ship (Track 1 + Track 5)
- [ ] Deploy on Modal.
- [ ] Register MCP server; demoable from Claude Desktop.
- [ ] Loom of MCP server in Claude Desktop.
- [ ] `git mv projects/icp-research-agent projects/reposcout`.
- [ ] README to standard. Workflow vs agent explainer included.
- [ ] Publish blog post 5: "Workflow first, agent second, MCP always."

### Outbound goes live (Track 6)
- [ ] Outbound list = 50 US AI startup founders/CTOs (just-raised, last 90 days).
- [ ] **Send 50 Insight Emails** with specific 2-week trial offers. Track in your sheet.
- [ ] Reply to all responses within 24 hrs.

### Public (Track 5)
- [ ] 1 lightning talk delivered or recorded (Latent Space Discord demo night, AI Tinkerers, or local meetup).
- [ ] Update LinkedIn headline + About.
- [ ] Update X bio with portfolio link.

### Discipline
- [ ] Weekly updates + Demo Day Loom.

---

## Month 6 — Job-search execution

**Window:** 2026-10-12 → 2026-11-08.

### Resume + funnel (Track 6)
- [ ] Rewrite resume around three projects + production-eval framing. Outcome language (numbers), not stack language.
- [ ] Apply to 10 HN/YC/Wellfound listings.
- [ ] Apply to 5 India product startups (Sarvam, Razorpay, Postman, Atlan, Eka).
- [ ] **Send 50 more Insight Emails** (100 total cumulative).
- [ ] Reply to all responses within 24 hrs.

### Interview prep
- [ ] 2 system-design mocks (doc Q&A; classifier with human handoff).
- [ ] 1 project deep-dive mock (leadlens or docsight).
- [ ] Drill the [MASTER_PLAN.md](./MASTER_PLAN.md) interview-readiness checklist.
- [ ] STAR stories drafted for: WIRLS-style hallucination audit (use your Caprae 35% blocked records), one shipped project win, one production failure + recovery.

### Week 23 push
- [ ] Apply to 10 more roles.
- [ ] **Send next 50 outbound** (150 total).
- [ ] Publish blog post 6: "What 6 months of part-time AI engineering actually looked like."

### Week 24
- [ ] Interview buffer + contract trial negotiation + follow-ups.
- [ ] If no offers active: extend funnel into Nov–Dec with more outbound volume + 25 more applications.
- [ ] Update LinkedIn / X / GitHub profile to "open to remote contracts and FT."

---

## Monthly self-review (last Sunday of every month)

Answer in [PROGRESS.md](./PROGRESS.md):

- Did I ship something this month that didn't exist last month? *(If no — what blocked, honestly?)*
- Can I explain one new concept in 60 seconds? *(Test it in a tweet.)*
- Is my GitHub commit graph visibly green?
- Is my blog up to date?
- Did I attend or watch one community event?
- How many no-AI Python katas did I actually do?
- Did I send the outbound messages planned?
- If a US founder opened my portfolio today, would the eval table + Loom + Mercor-grade GitHub be visible in 60 seconds?
- What did I cut from the plan, and was the cut honest?

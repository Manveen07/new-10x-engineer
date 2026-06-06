# Flagship Projects

Three deep projects beat ten demos. Each must be deployed, evaluated, documented, and *honest* about where it fails.

Each project's README is also a sales artifact for the US-remote outbound funnel. A founder should be able to (a) understand the problem in 30 seconds, (b) watch a 3-min Loom and see it working, (c) read your eval table and see you measure things. If a README can't do all three, it isn't done.

## Common standard (every project)

- [ ] **Live deployed URL** — Modal preferred (free $30/mo credits), Fly.io or HF Spaces acceptable.
- [ ] **README to standard:**
  - Problem statement (3 sentences)
  - Architecture diagram (use [excalidraw.com](https://excalidraw.com), commit as PNG)
  - Fresh-venv run instructions (someone with `uv` + Docker can run it in 5 minutes)
  - **"Where it fails" section** with named failure modes — non-negotiable
  - Eval results table with numbers, not vibes
  - Cost-per-call (₹ and $)
  - Latency p50 / p95
  - Stack list with rationale ("chose pgvector over Pinecone because…")
- [ ] **Eval dataset committed to the repo** as CSV/JSONL with labels.
- [ ] **Langfuse traces** — screenshots in README, link to public dashboard if possible.
- [ ] **Visible iteration history** — commits show v1 → v2 → v3, not one big initial dump.
- [ ] **3-min Loom video walkthrough** linked at the top of the README. Problem → architecture → live demo → eval table → "where it fails." Re-record until ≤3 min.
- [ ] **One blog post** with failure-mode honesty (not "I built a cool thing").
- [ ] **GitHub repo** is public, has tests (`pytest`), a `Makefile` or `justfile`, type hints, ruff-clean.
- [ ] **Founder-facing one-liner** in the README header: "what could a CTO hire me to do based on this?"

---

## Project 1 — leadlens (Months 1–2)

**Folder:** [projects/business-classification-pipeline](./projects/business-classification-pipeline/)
**Codename change:** the directory stays the same; in code, README, and posts we call it **leadlens**. Add a `RENAMING.md` note if needed.

### What it is
An LLM classifier that takes a company name + domain and returns structured fields: operating status, segment, signals detected with evidence, confidence, citations. Built around your existing 50-trace staffing-firm dataset, expanded to 100 hand-labeled examples.

### Why this project
- You're already 25% in (50 traces + open-coding notes + Modal/Langfuse accounts).
- Classification is the cleanest surface to learn eval-first development on.
- Direct extension of Caprae + Precise Leads work — interview story already exists.
- Founders hiring for "I need an LLM pipeline that's actually reliable on my noisy data" instantly recognize this shape.

### Stack
- Python 3.12+ + `uv` + `ruff` + `pytest`
- Pydantic + Instructor (structured output)
- Anthropic Claude as primary model; OpenAI GPT-4.1 as judge
- Web search + DuckDuckGo / Google CSE / Tavily for evidence collection
- Langfuse tracing (from line one, not bolted on at the end)
- Modal deployment
- Docker for local dev

### Eval standard
- 100 hand-labeled companies covering pass / fail / edge cases.
- Binary pass/fail LLM-as-judge per classification dimension (not 1–5 — see Hamel).
- Judge calibrated to **>90% agreement with your labels.**
- At least three judge-prompt iterations visible in commits.
- Confusion matrix in README.
- Failure taxonomy from open-coding notes (you already have v1 of this — extend it).
- Cost-per-call table + p50 / p95 latency table.

### Founder-facing one-liner
*"Built an LLM classifier with a 100-example golden dataset, calibrated LLM-as-judge, and a confusion matrix. Identified three failure modes — false executive-search signal, mixed-boundary ambiguity, schema drift — and walked the precision back to 91%."*

### Public write-up
**"Auditing my own LLM classifier"** — blog post 2. Walk through one trace, the failure mode it exposed, what you changed in the prompt/schema, the new eval numbers.

---

## Project 2 — docsight (Months 3–4)

**Folder:** [projects/gtm-clay-rag](./projects/gtm-clay-rag/) (rename to `docsight` in Month 3 — `git mv`).

### What it is
A production-grade RAG system over a real OSS corpus — recommended: **the Anthropic SDK + LangGraph + LiteLLM documentation, GitHub issues, and recent release notes.** Answers questions like *"how do I implement contextual retrieval with hybrid search in LangGraph?"* with citations + measured retrieval quality + measured generation quality, separately tracked.

### Why this corpus (not Clay docs)
The previous plan used Clay docs as a private corpus. You don't have Clay access at that depth, and Clay docs change. The Anthropic/LangGraph/LiteLLM corpus is (a) public, (b) what your *own future employers* are building with, (c) varied enough (code blocks + prose + issues + changelogs) to test contextual retrieval honestly, (d) demonstrates immediate utility — the deployed URL is something other engineers will actually use.

### Stack
- FastAPI + Pydantic
- Postgres 16 + pgvector + Postgres full-text search (BM25 via `pg_search` or hand-rolled)
- Voyage embeddings (`voyage-3` or `voyage-3-large`)
- Cohere Rerank 3.5 (or Voyage Rerank 2.5, or a local `bge-reranker` as the cheap path)
- Anthropic Contextual Retrieval preprocessing (Sept 2024 prompt — implement exactly)
- Ragas for generation evals; custom retrieval metrics for retrieval evals
- Langfuse traces
- Docker + Docker Compose for local dev
- Modal deployment
- **Bonus knowledge spike:** 30-min LlamaIndex notebook + 30-min Pinecone notebook so you can speak to both in interviews even though you don't deploy either.

### Eval standard
- **Retrieval evals:** ~150 synthetic query-chunk pairs (generated from the corpus with an LLM, hand-verified).
  - Metrics: recall@5, recall@10, MRR, NDCG@10.
  - **Ablation table** (this is the artifact founders and hiring managers screen for):
    - pure dense
    - BM25 only
    - hybrid (RRF) — dense + BM25
    - hybrid + rerank
    - hybrid + rerank + contextual retrieval preprocessing
- **Generation evals:** Ragas faithfulness, answer relevance, context precision. Judges calibrated against ~30 hand labels.
- Cited generation — every claim has a chunk citation.
- Cost-per-query + latency p50 / p95.

### Founder-facing one-liner
*"Built a production RAG over Anthropic + LangGraph docs with hybrid retrieval, contextual chunking, and a calibrated Ragas pipeline. The ablation table shows contextual + hybrid + rerank moves recall@10 from 67% to 91% — and the README explains why each layer matters."*

### Public write-up
**"Contextual retrieval on real OSS docs: a measured ablation"** — blog post 4. Show the ablation table, name the corpus, share a failure case where rerank actually hurt and why.

### Mercor and outbound asset
This is your strongest "I can ship production RAG" artifact. Mercor reviewers and US founders both screen for "have they actually measured retrieval quality, or did they just `np.dot()` and call it RAG?" — the ablation table answers that in 30 seconds.

---

## Project 3 — reposcout (Month 5)

**Folder:** [projects/icp-research-agent](./projects/icp-research-agent/) (rename to `reposcout` in Month 5 — `git mv`).

### What it is
An agent that takes a topic ("agent memory libraries" / "RAG eval tools" / "MCP servers in Python") and produces a ranked, evidence-backed report of OSS repos worth contributing to or watching — using **leadlens as a classifier tool**, **docsight as a knowledge tool** (if docs are in corpus), and the GitHub API for live signals (stars, recent activity, issue quality, maintainer responsiveness).

Wrapped as an **MCP server** so it's usable from Claude Desktop, Cursor, or any MCP-compatible client. This is the artifact that says "I get 2026 agent engineering."

### Why this project
- Composes Project 1 + Project 2 as *tools* — proves you understand agent composition, not just "use LangChain to chain prompts."
- MCP server is **table-stakes in 2026 JDs** (Sarvam FDE lists it; HN listings increasingly require it).
- Directly useful to you: you'll actually use reposcout to find the right OSS repo to contribute to (recursive: the agent helps you build the very portfolio that gets you hired).
- The "I built an agent that uses my own classifier and RAG via MCP" story is memorable in final-round interviews.

### Stack
- Raw Python orchestration first — agentic dynamism only at the one node that needs it
- Pydantic + Instructor for tool I/O validation
- Anthropic Claude (Sonnet primary, Haiku for cheap subtasks)
- GitHub API (`PyGithub` or raw `httpx`)
- leadlens (called as a local tool)
- docsight (called as an MCP tool)
- MCP server via `mcp` Python SDK (Anthropic's official)
- **Step budget capped at 20** (Anthropic's *Building Effective Agents* discipline)
- Idempotency tokens for all external tool calls
- Langfuse trace per agent run + per tool call
- Modal deployment + MCP server registration

### Eval standard
- **30 golden reference topics** with hand-curated "good answer" repo lists.
- **Trajectory evals:** golden expected tool paths per topic. LLM-as-judge for "did the agent's trajectory match a reasonable shape?"
- **Final-output evals:** precision/recall on returned repo lists vs golden.
- **State-transition matrix** to identify loops, dead-ends, failure spikes.
- Cost/task + steps/task + escalation rate.
- An "MCP demo" GIF or video showing it called from Claude Desktop.

### Founder-facing one-liner
*"Built an agent that composes my classifier + my RAG via MCP, with a 20-step budget, trajectory evals on 30 reference topics, and a state-transition matrix to catch loops. The MCP server runs in Claude Desktop. The README explains workflow vs agent — and where I chose workflow."*

### Public write-up
**"Workflow first, agent second, MCP always: shipping reposcout"** — blog post 5. Frame around the Anthropic *Building Effective Agents* discipline. Show the state-transition matrix. Name two real loops you caught.

### Mercor and outbound asset
Final piece. By Month 5 your GitHub has three pinned repos + an MCP server + an OSS PR. Mercor's "interview is exclusively your open-source contributions" rule starts to work in your favor. US founders see one engineer who has actually shipped what their JD asks for — not someone who has read about it.

---

## Portfolio rule

Each README must answer these in interview-ready language *without* you having to be there:

- What did the system do?
- What data did it run on?
- How did you know it was good?
- What failed and what did you change?
- What did it cost? How slow was it?
- How would you run it in production (Docker? cron? queue? scale-to-zero?)
- What would you do next if you had two more weeks?

If the README answers those, the interview is half-done before the call starts.

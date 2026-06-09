# Week 9 — RAG by Failing: Contextual Retrieval on a Toy Corpus + Pick OSS Target

> 📝 **PROVISIONAL draft (written 2026-06-09, ~6 weeks early).** Months 3–6 describe work on docsight/reposcout, which don't exist yet — treat these as scaffolding to refine the weekend before each week, anchored on what actually shipped. Detailed month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-3--rag-fundamentals--docsight-design-your-1-red-zone). Project spec: [../PROJECTS.md](../PROJECTS.md#project-2--docsight-months-34).

**Window:** Mon 2026-07-20 → Sun 2026-07-26
**Time budget:** 8–10 hours (graduation lands this month — protect weekends, keep weekdays light)
**Position:** Month 3, Week 9 of 24

## Why this week matters

RAG is your weakest area (self-rated 1–2/5) and the single most-asked 2026 interview topic ("design a RAG system for X"). The lesson that separates juniors from pros: **~70% of RAG failures are retrieval, not the LLM — so measure retrieval first, and build by failing.** This week you start with the dumbest possible retriever and feel where it breaks, then read Anthropic's Contextual Retrieval and implement it on a toy corpus.

**The single must-do:** a notebook where `np.dot(query, chunks)` visibly misses an exact-term query, and contextual-retrieval preprocessing fixes it — committed with a one-paragraph writeup.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-07-20 | Plan review + **LeetCode ×1** (continue 60–80 arc) | 20 min |
| Tue eve | 2026-07-21 | Read [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (full) — 3 notes in `notes/fundamentals.md` | 20 min |
| Wed eve | 2026-07-22 | Read Greg Kamradt on text splitting → recall: "when does chunk overlap add nothing?" | 20 min |
| Thu eve | 2026-07-23 | **LeetCode ×1** + skim 3 candidate OSS repos' "good first issue" lists | 20 min |
| Fri eve | 2026-07-24 | Rest or skim (graduation buffer) | 0–20 min |
| **Sat** | 2026-07-25 | **Big build**: toy corpus → `np.dot` retriever → watch it miss exact terms → add Contextual Retrieval preprocessing → measure the difference | **3.5 hrs** |
| **Sun** | 2026-07-26 | **Build + decide**: chunking experiments (512-tok recursive vs auto-merge) + **pick the OSS target repo** (Instructor / Langfuse / Ragas / simonw-llm / LiteLLM / PydanticAI) + PROGRESS | **3 hrs** |

## Saturday — build RAG by failing (3.5 hrs)
- Tiny corpus (~30 chunks from the Anthropic/LangGraph docs you'll use for docsight). Embed with Voyage (or any embedder), retrieve with cosine.
- Pose an **exact-term query** (an API name, an error code) — watch dense retrieval miss it. *Feel* the failure; that's why hybrid exists.
- Implement Contextual Retrieval (prepend a situating blurb per chunk via an LLM call, then embed). Re-measure. Note the improvement. (Anthropic reports −49% retrieval failures, −67% with rerank — see if your toy shows the direction.)

## Sunday — chunking + pick OSS target (3 hrs)
- Chunking: compare recursive ~512-tok vs auto-merging on the same queries. Recall: why overlap often adds nothing.
- **Pick ONE OSS repo** to contribute to (Mercor's interview = your OSS contributions — start now). Criteria: responsive maintainer, a `good first issue` you understand, repo you'll actually use. Write the pick + the candidate issue in `notes/oss-target.md`.

## Behind if
- No notebook showing the dense-miss → contextual-fix.
- Can't explain in 30 sec why hybrid beats pure dense.
- No OSS repo picked.

## Next week
→ `week-10.md`: Jason Liu on systematically improving RAG; 30-min LlamaIndex + 30-min Pinecone vocabulary spikes.

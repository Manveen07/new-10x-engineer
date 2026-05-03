# Month 3 - RAG Fundamentals And Project 2 Design

## Goal

Build enough retrieval depth to design Project 2 properly before shipping it. Month 3 is reading-heavy by design, but it must still produce working code: contextualization on a toy corpus, local Postgres/pgvector setup, and the first ingestion pipeline for GTM/Clay knowledge.

Canonical output by the end of the month:

- Contextual retrieval prototype on a small corpus.
- Project 2 stack decision.
- Local Postgres + pgvector running.
- Initial ingestion pipeline.
- Retrieval eval plan.
- Project 2 design doc.
- Public post 3 published.
- One Bengaluru/community event attended or watched.

Existing agent exercises in this folder are useful in Month 5, but Month 3 is now focused on RAG design.

## Week Plan

| Week | Time | Focus | Deliverable |
|---|---:|---|---|
| 9 | 8h | Read Anthropic Contextual Retrieval and Greg Kamradt text splitting | toy contextual retrieval implementation |
| 10 | 8h | Read Jason Liu and Hamel RAG eval guidance | retrieval notes and eval principles |
| 11 | 8h | Pick stack, set up Postgres + pgvector, skim AI Engineering Ch. 6 | local retrieval data layer |
| 12 | 8h | DLAI accuracy/evals course, begin Clay/GTM ingestion, write design doc | Project 2 design doc and post |

## Project 2 Design Requirements

The design doc should define:

- Corpus sources and attribution/consent rules.
- Document model and chunk metadata.
- Chunking strategy and contextualization prompt.
- Dense retrieval provider.
- Lexical retrieval choice: BM25 or PostgreSQL full-text search.
- Hybrid fusion method, defaulting to RRF.
- Reranker interface.
- Retrieval eval dataset generation plan.
- Metrics: recall@10/20, MRR, NDCG, context precision.
- Generation eval plan and calibration set.
- Deployment and tracing plan.

Suggested location: `projects/gtm-clay-rag/docs/design.md`.

## Monthly Checklist

- [ ] Anthropic Contextual Retrieval read.
- [ ] Greg Kamradt text-splitting notes taken.
- [ ] Jason Liu RAG articles read.
- [ ] Hamel RAG eval guidance read.
- [ ] Toy contextual retrieval prototype works.
- [ ] Postgres + pgvector running locally.
- [ ] Project 2 stack decision written.
- [ ] Ingestion pipeline started.
- [ ] Retrieval eval design written.
- [ ] One Bengaluru/community event attended or watched.
- [ ] Post 3 published: "How I'm setting up retrieval evals before writing a single line of RAG code."

## Interview Skill Added

You should be able to explain why hybrid retrieval beats pure dense retrieval, why retrieval evals should be separated from generation evals, and why Ragas-style metrics need calibration.

## Behind If

- No Project 2 code exists.
- You cannot explain hybrid retrieval in two sentences.
- The retrieval eval plan is missing.

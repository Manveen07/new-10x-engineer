# Six-Month Roadmap

Target pace: 8 hours per week, about 32 hours per month, 192 hours total.

Mission: become job-ready as an AI engineer by turning existing GTM and LLM production experience into a portfolio that proves eval-first, production-grade AI engineering.

## Month Overview

| Month | Theme | Main outcome |
|---|---|---|
| 1 | Evals foundations and Project 1 design | Maven evals work, open-coding notes, annotation workflow, Project 1 design doc, first post |
| 2 | Project 1 ship | Business classifier with schema, golden dataset, LLM-as-judge, deployment, README, second post |
| 3 | RAG fundamentals and Project 2 design | Contextual retrieval prototype, modern RAG reading, stack choice, ingestion skeleton, third post |
| 4 | Project 2 ship | Hybrid RAG with contextual retrieval, reranking, ablation table, Ragas calibration, deployment, fourth post |
| 5 | Project 3 and portfolio polish | ICP research agent with step budget, trajectory evals, deployment, fifth post, portfolio polish |
| 6 | Job search execution | Resume, warm intros, applications, mock interviews, sixth post, active interview pipeline |

## Month 1 - Foundations, Evals Self-Paced, Project 1 Design

Theme: learn evals from the free Hamel/Shreya canon and apply them to existing classification work. No Maven cohort — self-paced. Sunday `PROGRESS.md` updates are the only forcing function, so do not skip them.

Window: 2026-05-04 to 2026-05-31.

| Week | Time | Goals |
|---|---:|---|
| 1 | 8h | Set up GitHub portfolio repo and personal site (Quarto or Astro, pick in 30 min). Read Hamel's `evals-faq` post end-to-end. Skim Chip Huyen *AI Engineering* Ch. 1-2 if needed. Pull 50 real classifier traces from past Clay/winery/HVAC runs. |
| 2 | 8h | Apply the Three Gulfs framework (specification / generalization / comprehension) to the 50 traces. Open-code by hand. Read Eugene Yan's "Patterns for Building LLM-based Systems & Products" end-to-end. |
| 3 | 8h | Convert open-coding notes into an axial failure taxonomy. Build a simple annotation viewer (FastHTML or Streamlit, ~2 hrs). Read Hamel's `llm-judge` post. |
| 4 | 8h | Calibrate an LLM-as-judge with critique shadowing on a sample of the 50 traces. Target >90% agreement with your labels. Write Project 1 design doc. |

Public ship: blog post 1, "Open coding 50 LLM traces from a real classification pipeline."

Behind if: fewer than 50 reviewed traces, no failure taxonomy, no live personal site, or two consecutive missed Sunday `PROGRESS.md` updates.

## Month 2 - Ship Project 1

Theme: convert eval learning into a shipped classification system.

Window: 2026-06-01 to 2026-06-28.

| Week | Time | Goals |
|---|---:|---|
| 5 | 8h | Read DLAI *Improving Accuracy of LLM Applications* (1-2 hrs). Convert your taxonomy and judge work into Project 1 scaffolding. |
| 6 | 8h | Build Project 1 schema with Pydantic and Instructor. Add Langfuse instrumentation from the start. Hand-label 100 companies. |
| 7 | 8h | Build calibrated LLM-as-judge checks. Iterate to more than 90% agreement with labels. Add confusion matrix, cost, and latency analysis. |
| 8 | 8h | Deploy on Modal. Finish README with architecture diagram, failure modes, eval results, and iteration log. Publish blog post 2. |

Public ship: deployed Project 1, GitHub README to standard, blog post 2, LinkedIn/X announcement.

Behind if: no deployment, no 100-example golden dataset, or fewer than two published posts.

## Month 3 - RAG Fundamentals and Project 2 Design

Theme: learn the retrieval stack deeply before building the full RAG system.

Window: 2026-06-29 to 2026-07-26.

| Week | Time | Goals |
|---|---:|---|
| 9 | 8h | Read Anthropic Contextual Retrieval. Implement contextualization on a toy corpus. Read Greg Kamradt on text splitting. |
| 10 | 8h | Read Jason Liu on RAG complexity, search improvements, and context engineering. Read Hamel's RAG eval guidance. |
| 11 | 8h | Choose stack: Postgres + pgvector, hybrid lexical/dense retrieval, reranker, FastAPI, Modal, Langfuse. Set up local Postgres with pgvector. |
| 12 | 8h | Take one short DLAI accuracy/evals course. Begin Clay/GTM ingestion pipeline. Write Project 2 design doc. |

Public ship: blog post 3, "How I'm setting up retrieval evals before writing a single line of RAG code."

Behind if: no Project 2 code, or unable to explain why hybrid retrieval beats pure dense retrieval.

## Month 4 - Ship Project 2

Theme: build, evaluate, and deploy the GTM/Clay RAG system.

Window: 2026-07-27 to 2026-08-23.

| Week | Time | Goals |
|---|---:|---|
| 13 | 8h | Implement contextual retrieval or use a context-aware embedding option. Add hybrid retrieval with RRF. Generate 150 synthetic query-chunk eval pairs. |
| 14 | 8h | Add reranking. Build ablation table: pure dense vs BM25 vs hybrid vs hybrid plus rerank. Measure recall@10, MRR, and NDCG@10. |
| 15 | 8h | Add cited generation. Use Ragas-style metrics for faithfulness, answer relevance, and context precision. Calibrate judges against about 30 hand labels. |
| 16 | 8h | Deploy on Modal with FastAPI and Langfuse. Add cost analysis. Publish Project 2 and blog post 4. Submit a lightning-talk proposal. |

Public ship: deployed Project 2, RAG ablation post, LinkedIn post tagged for the Clay community.

Behind if: no retrieval ablation table, uncalibrated Ragas usage, or no talk scheduled/proposed.

## Month 5 - Project 3 and Portfolio Polish

Theme: build agents the production way: workflow first, agent only where dynamic search/validation needs it.

Window: 2026-08-24 to 2026-09-20.

| Week | Time | Goals |
|---|---:|---|
| 17 | 8h | Read Anthropic agent guidance and context engineering. Sketch the ICP researcher as a workflow first. Identify the one agentic node. |
| 18 | 8h | Build raw orchestration with Pydantic tool I/O, step budget, idempotency tokens, structured outputs, and tool validation. |
| 19 | 8h | Define 30 golden ICP trajectories. Build trajectory judge prompt and state-transition matrix. Add precision/recall evals for final company lists. |
| 20 | 8h | Deploy Project 3. Publish blog post 5. Polish all three READMEs. Update LinkedIn headline/About and portfolio site. |

Public ship: deployed Project 3, blog post 5, portfolio site with all three projects above the fold.

Behind if: cannot explain workflow vs agent in 30 seconds, or the three projects do not read as one coherent portfolio.

## Month 6 - Job Search Execution

Theme: run the funnel. The portfolio is the asset; now the work is applying, interviewing, and getting warm intros.

Window: 2026-09-21 to 2026-10-18.

| Week | Time | Goals |
|---|---:|---|
| 21 | 8h | Rewrite resume around the three projects and production experience. Apply to 10 Circle 1 roles and 5 Circle 2 roles. Ask 5 Clay contacts for warm intros. |
| 22 | 8h | Run 2 system-design mocks and 1 project deep-dive mock. Drill doc Q&A, classifier, enrichment pipeline, and eval harness designs. |
| 23 | 8h | Skim the paper list. Apply to 10 more roles. Publish blog post 6: "What 6 months of part-time AI engineering actually looked like." |
| 24 | 8h | Interview buffer, negotiation, follow-ups. If no offers are active, extend into Months 7-8 with more shipping and funnel volume. |

Public ship: blog post 6 and "actively looking" LinkedIn post with the three project links.

Behind if: fewer than 25 applications, fewer than 3 first-round interviews, or no warm-intro asks.

## Weekly Cadence

- Daily: 15 minutes of AI engineering news or primary-source reading.
- Twice weekly: 2-hour project blocks.
- Weekend: one longer project or writing block.
- Sunday: update [PROGRESS.md](./PROGRESS.md), read one substantive post, triage next week.
- Last Sunday monthly: self-review, publish/update, attend or watch one community event, update LinkedIn.

## Readiness Bar

By the end of Month 6:

- [ ] Three deployed projects with eval suites, READMEs, cost/latency analysis, and live URLs.
- [ ] At least five posts on your own domain.
- [ ] One useful OSS contribution merged.
- [ ] One lightning talk delivered or recorded.
- [ ] LinkedIn updated around AI engineer positioning.
- [ ] 25+ role applications and 5+ first-round interviews.
- [ ] At least one warm intro from the Clay or Bengaluru network.

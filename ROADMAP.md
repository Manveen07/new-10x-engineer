# Six-Month Roadmap

**Pace:** 8–10 hours/week. ~36 hours/month, ~216 hours total over 24 weeks.

**Mission:** Become hireable as a junior GenAI / LLM Application Engineer by Nov 2026 through three deployed projects, an MCP server, one OSS PR, four to six blog posts, and a US-remote outbound funnel actually open.

**Window:** 2026-05-25 → 2026-11-08 (24 weeks).

> **Status (2026-06-09):** Week 3 in progress, **ahead of plan** (judge v1 shipped early, TPR=1.0/TNR=0.882). All 24 weeks below now link to their day-by-day files. Weeks 5–24 are drafted — Month 2 from real Week 1–3 results, Months 3–6 provisional (refine each the weekend before it starts, per [PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md)). Right now: [month-1/FINISH-PLAN.md](month-1/FINISH-PLAN.md) wins on sequencing. DSA reps live in [dsa/](dsa/README.md) from Week 5.

---

## Calendar at a glance

| Month | Window | Theme | Public ship |
|---|---|---|---|
| 1 | 2026-05-25 → 2026-06-21 | Code rebuild + leadlens design + eval foundations | Live portfolio site + first blog post |
| 2 | 2026-06-22 → 2026-07-19 | Ship leadlens (classifier + evals + deploy) | Deployed leadlens + post 2 + Loom |
| 3 | 2026-07-20 → 2026-08-16 | RAG fundamentals + docsight design + OSS PR | Post 3 + OSS PR opened |
| 4 | 2026-08-17 → 2026-09-13 | Ship docsight (hybrid RAG + ablation) | Deployed docsight + post 4 + OSS PR merged + Mercor application |
| 5 | 2026-09-14 → 2026-10-11 | Ship reposcout (agent + MCP server) + outbound starts | Deployed reposcout + post 5 + first 50 outbound contacts + 1 lightning talk |
| 6 | 2026-10-12 → 2026-11-08 | Job-search execution (US-remote primary, India secondary) | Post 6 + 100+ outbound messages sent + 5+ first rounds + India apps in parallel |

⚠ **You graduate in August 2026, mid-Month 3.** Exams are already done (confirmed); no need to thin Month 3. Graduation week itself may need a lighter Saturday — log on PROGRESS.md when it lands.

---

## Month 1 — Code rebuild, eval foundations, leadlens design

**Window:** 2026-05-25 → 2026-06-21. Theme: rebuild Python fluency without AI, then aim that rebuilt muscle at evals on your existing 50 traces. Project 1 (leadlens) gets a real design doc.
**Month files:** [overview](month-1/README.md) · [FINISH-PLAN.md](month-1/FINISH-PLAN.md) (day-by-day close-out — wins on sequencing).

| Week | Date window | Time | Goals |
|---|---|---:|---|
| [1](month-1/week-1.md) | May 25 – May 31 | 8–10h | **No-AI code rebuild block.** Daily 30-min hand-coded Python katas. Set up modern stack (`uv`, `ruff`, `pytest`). Stand up portfolio site (Quarto or Astro). Refresh AsanaBot + PresentAI READMEs. |
| [2](month-1/week-2.md) | Jun 1 – Jun 7 | 8–10h | **Open-code your 50 traces** with Three Gulfs framework. Re-read Hamel `evals-faq`. Build a simple Streamlit/FastHTML annotation viewer. |
| [3](month-1/week-3.md) | Jun 8 – Jun 14 | 8–10h | **Axial-code into a failure taxonomy** (`failure-taxonomy.md`, 4–7 named categories). Read Hamel `llm-judge`. Judge v1 already built (TPR=1.0/TNR=0.882) — push calibration to **>85% now, >90% by Week 4**. Slack from being ahead → draft blog post 1 early. |
| [4](month-1/week-4.md) | Jun 15 – Jun 21 | 8–10h | **leadlens design doc.** Pydantic schemas, golden-dataset plan, deployment shape. Publish blog post 1: "Open-coding 50 traces from a real classifier." |

**Public ship:** live portfolio site + first blog post + refreshed AsanaBot/PresentAI READMEs.
**Behind if:** fewer than 50 traces reviewed; no failure taxonomy; no live site; two consecutive missed Sunday `PROGRESS.md` updates.

## Month 2 — Ship leadlens

**Window:** 2026-06-22 → 2026-07-19. Theme: convert eval learning into a shipped, deployed, observed classifier.
**Month files:** [overview](month-2/README.md) · reasoning: [PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md#month-2--ship-leadlens-deploy--observe--scale-the-golden-set).

| Week | Date window | Time | Goals |
|---|---|---:|---|
| [5](month-2/week-5.md) | Jun 22 – Jun 28 | 8–10h | Watch DLAI *Improving Accuracy of LLM Applications* (1–2 hrs). Build leadlens scaffolding: Pydantic models + Instructor + Langfuse tracing from line one. |
| [6](month-2/week-6.md) | Jun 29 – Jul 5 | 8–10h | Hand-label 100 companies (golden dataset). First end-to-end classification run. Compare to labels — confusion matrix v1. |
| [7](month-2/week-7.md) | Jul 6 – Jul 12 | 8–10h | Iterate prompt + schema based on failures. Calibrate judge to >90% agreement. Add cost + latency p50/p95 instrumentation. |
| [8](month-2/week-8.md) | Jul 13 – Jul 19 | 8–10h | Deploy on Modal. Write README to standard (architecture diagram, "where it fails," eval table, cost, latency). **Record 3-min Loom.** Publish blog post 2. Tweet thread + LinkedIn announcement. |

**Public ship:** deployed leadlens + README to standard + Loom + blog post 2.
**Behind if:** no deployment; <100 golden examples; no confusion matrix in README; no Loom.

## Month 3 — RAG fundamentals + docsight design + first OSS PR

**Window:** 2026-07-20 → 2026-08-16. Theme: learn the retrieval stack deeply before building docsight. Open the first OSS PR.
**Month files:** [overview](month-3/README.md) · reasoning: [PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md#month-3--rag-fundamentals--docsight-design-your-1-red-zone).

| Week | Date window | Time | Goals |
|---|---|---:|---|
| [9](month-3/week-9.md) | Jul 20 – Jul 26 | 8–10h | Read Anthropic *Contextual Retrieval*. Implement on a toy corpus. Read Greg Kamradt on text splitting. Pick OSS target repo (Instructor / Langfuse / Ragas / simonw/llm / LiteLLM). |
| [10](month-3/week-10.md) | Jul 27 – Aug 2 | 8–10h | Read Jason Liu on RAG complexity. Spike LlamaIndex + Pinecone (30-min sandbox each — for vocabulary). |
| [11](month-3/week-11.md) | Aug 3 – Aug 9 | 8–10h | Pick docsight stack: Postgres + pgvector + BM25 + reranker + FastAPI + Modal + Langfuse. Set up local Postgres + pgvector. |
| [12](month-3/week-12.md) | Aug 10 – Aug 16 | 8–10h | docsight design doc. Begin OSS PR (open issue or draft PR — get maintainer feedback). Publish blog post 3: "What I'm setting up before writing a line of RAG code." |

**Public ship:** blog post 3 + draft OSS PR opened + docsight design committed.
**Behind if:** no design doc; no OSS PR opened; can't explain why hybrid retrieval beats pure dense.

## Month 4 — Ship docsight + merge OSS PR + Mercor application

**Window:** 2026-08-17 → 2026-09-13. Theme: build, evaluate, deploy docsight. Land the OSS PR. Apply to Mercor with portfolio in hand.
**Month files:** [overview](month-4/README.md) · reasoning: [PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md#month-4--ship-docsight-the-ablation-table--merge-oss-pr--mercor).

| Week | Date window | Time | Goals |
|---|---|---:|---|
| [13](month-4/week-13.md) | Aug 17 – Aug 23 | 8–10h | Build ingestion. Implement contextual retrieval. Add hybrid (BM25 + dense with RRF). Generate 150 synthetic query-chunk eval pairs. |
| [14](month-4/week-14.md) | Aug 24 – Aug 30 | 8–10h | Add reranker. Build ablation table: pure dense vs BM25 vs hybrid vs hybrid+rerank. Measure recall@10, MRR, NDCG@10. |
| [15](month-4/week-15.md) | Aug 31 – Sep 6 | 8–10h | Cited generation. Ragas faithfulness + answer relevance + context precision. Calibrate judges against ~30 hand labels. Land OSS PR. |
| [16](month-4/week-16.md) | Sep 7 – Sep 13 | 8–10h | Deploy on Modal (Docker, FastAPI, Langfuse). Add $/query analysis. **Record Loom.** Publish blog post 4. **Apply to Mercor.** Apply to 5 HN/YC/Wellfound listings. |

**Public ship:** deployed docsight + README to standard + Loom + blog post 4 + OSS PR merged + Mercor application submitted.
**Behind if:** no ablation table; uncalibrated Ragas; no OSS PR merged; no Mercor application.

## Month 5 — Ship reposcout (agent + MCP) + outbound funnel starts

**Window:** 2026-09-14 → 2026-10-11. Theme: workflow-first agent that uses leadlens + docsight as tools. Wraps as MCP server. Outbound channel goes live.
**Month files:** [overview](month-5/README.md) · reasoning: [PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md#month-5--ship-reposcout-agent--mcp--outbound-funnel-goes-live).

| Week | Date window | Time | Goals |
|---|---|---:|---|
| [17](month-5/week-17.md) | Sep 14 – Sep 20 | 8–10h | Read Anthropic *Building Effective Agents* + *Effective Context Engineering for AI Agents*. Sketch reposcout as a workflow first. Identify the one node that genuinely needs agentic dynamism. Build outbound target list (50 just-raised US AI startups). |
| [18](month-5/week-18.md) | Sep 21 – Sep 27 | 8–10h | Raw orchestration: Pydantic tool I/O, step budget (20), idempotency tokens, structured outputs, tool validation. Wire leadlens + docsight as MCP tools. Send first 25 Insight Emails. |
| [19](month-5/week-19.md) | Sep 28 – Oct 4 | 8–10h | 30 golden ICP trajectories. Trajectory judge prompt + state-transition matrix. Add precision/recall on final repo lists. Send next 25 Insight Emails (50 total). |
| [20](month-5/week-20.md) | Oct 5 – Oct 11 | 8–10h | Deploy reposcout. Register MCP server. **Record Loom.** Publish blog post 5. Polish all three project READMEs. Update LinkedIn + X. **Give or record 1 lightning talk** (Latent Space Discord, AI Tinkerers, or local meetup). |

**Public ship:** deployed reposcout + MCP server demoable from Claude Desktop + Loom + blog post 5 + lightning talk + 50 outbound contacts.
**Behind if:** can't explain workflow vs agent in 30 sec; MCP server not demoable; fewer than 50 outbound contacts.

## Month 6 — Run the funnel

**Window:** 2026-10-12 → 2026-11-08. Theme: portfolio is the asset; now the work is outreach, applications, interviews, conversion.
**Month files:** [overview](month-6/README.md) · [interview-tracker.md](month-6/interview-tracker.md) · reasoning: [PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md#month-6--run-the-funnel-as-an-evaluation-problem).

| Week | Date window | Time | Goals |
|---|---|---:|---|
| [21](month-6/week-21.md) | Oct 12 – Oct 18 | 8–10h | Rewrite resume around the three projects + production-eval framing. Apply to 10 HN/YC/Wellfound. Send 50 more outbound (100 total). Apply to 5 India product startups (Sarvam, Razorpay, Postman, Atlan, Eka). |
| [22](month-6/week-22.md) | Oct 19 – Oct 25 | 8–10h | 2 system-design mocks (doc Q&A; classifier with handoff). 1 project deep-dive mock. Apply to 10 more roles. Reply to all outbound responses within 24 hours. |
| [23](month-6/week-23.md) | Oct 26 – Nov 1 | 8–10h | Skim paper list. Send next 50 outbound (150 total). Apply to 5 more India roles. Publish blog post 6: "What 6 months of part-time AI engineering actually looked like." |
| [24](month-6/week-24.md) | Nov 2 – Nov 8 | 8–10h | Interview buffer, contract trial negotiation, follow-ups. If no offers active, extend funnel into Nov–Dec with more outbound volume. |

**Public ship:** post 6 + "open to remote" updated on GitHub/X/LinkedIn/Mercor/Wellfound + interview pipeline live.
**Behind if:** fewer than 100 outbound messages sent; fewer than 25 applications; fewer than 3 first-round interviews; no India safety apps in parallel.

---

## Weekly cadence (job-shaped: light weekdays, heavy weekends)

You work at Precise Leads Mon–Fri, so the plan is weekend-loaded.

| Day | What | Time |
|---|---|---|
| Mon eve | Open week file. Copy 2–3 main goals to sticky note. **Kata 1 (no AI).** | 15 min |
| Tue / Wed / Thu eve | One kata each evening (no AI), **committed to `katas/` that same night** — daily green squares are a Mercor screen filter (§9), so treat the commit as part of the rep. | 15 min × 3 |
| Fri eve | Kata 5 OR rest if Friday's exhausting. Skim one post (Hamel / Eugene / Latent Space). | 15–30 min |
| **Sat** | **Big build block.** Project work, deployments, builds. The week's deliverable lives here. | **3–4 hrs** |
| **Sun** | **Reading + writing block.** Reading, blog drafting, refactor cleanup. End with 30-min `PROGRESS.md` update + `START_HERE.md` pointer update + plan next week. | **3–4 hrs** |
| Last Sun of month | +30 min for monthly self-review + Demo Day Loom recording. | +30 min |

Total target: 8–10 hours/week (roughly 75 min weekdays + 6–8 hrs weekends). If you drop below 6 hrs total for two weeks in a row, the Sunday log will tell you — read the "Behind if" markers and recover.

**Job-day exhaustion rule:** if a weekday after work is brutal, skip that night's kata — but cap skips at 1/week. Two skipped katas in a row → catch up Saturday morning before the build block.

**DSA standing rule (from Month 2):** Month 1 stays no-AI Python rebuild. From Month 2 onward, swap **2 of the weekday katas for 2 LeetCode problems/week** (arrays / hash maps / strings / graphs — not DP/trees grinding). Target **60–80 problems total by Month 6**, committed to a `dsa/` folder. Rationale: live-coding screens can land the moment outbound opens (Month 5), so 80 problems crammed into Month 6 ([Week 22](#month-6--run-the-funnel)) is too late — spread them. (See [MASTER_PLAN.md §3](MASTER_PLAN.md#L62).)

## Skill ladder — how the 7 axes climb month by month

Same seven axes you rate every Sunday in [PROGRESS.md](PROGRESS.md). Baseline = your Week-1 self-rating. Each cell = where that axis should sit by month-end; the **bold** cells mark the month that axis is the focus. Two Sundays in a row below the current month's row → treat as "behind" and recover before advancing.

| Axis (1–5) | W1 baseline | M1 | M2 | M3 | M4 | M5 | M6 | What moves it |
|---|---|---|---|---|---|---|---|---|
| Python fluency (no AI) | 3 | **3.5** | **4** | 4 | 4 | 4.5 | 4.5 | daily katas → [dsa/](dsa/README.md) LeetCode arc |
| Evals | 3 | **4** | **4.5** | 4.5 | 5 | 5 | 5 | open/axial coding → judge calibration → CI gate → Ragas → trajectory |
| RAG | 2 | 2 | 2 | **3.5** | **4.5** | 4.5 | 4.5 | build-by-failing → hybrid+rerank+contextual → ablation table |
| Agents | 3 | 3 | 3 | 3 | 3 | **4.5** | 4.5 | workflow-first reposcout → MCP server → trajectory evals |
| Production / deploy | 4 | 4 | **4.5** | 4.5 | **5** | 5 | 5 | Modal + FastAPI + Docker + Langfuse + CI, reused 3× |
| Public footprint | 2 | **2.5** | 3 | 3.5 | 4 | **4.5** | 5 | blog post per month + Looms + OSS PR + lightning talk |
| Outbound funnel | 3 | 3 | 3 | 3 | 3.5 | **4** | **5** | list-building (M2–4, passive) → 50 sends (M5) → 100+ & interviews (M6) |

The through-line stays one discipline in five shapes — measure-first, eval-driven engineering ([PLAN-MONTHS-2-6.md](PLAN-MONTHS-2-6.md#the-through-line-re-read-when-lost)). No axis is ever dormant: even off-focus months hold maintenance reps (katas/DSA daily, one public push weekly, PROGRESS every Sunday).

## Readiness bar (Nov 8, 2026)

- [ ] Three deployed projects (leadlens, docsight, reposcout) with eval suites, READMEs to standard, $/call + latency p50/p95, live URLs, Loom walkthroughs.
- [ ] One MCP server demoable from Claude Desktop or Cursor.
- [ ] One merged OSS PR to a recognized LLM/AI repo.
- [ ] Four to six published blog posts on your own domain.
- [ ] GitHub profile: 4–6 months of daily-ish activity + pinned repos + profile README.
- [ ] X profile: portfolio bio + 30+ substantive posts/replies + 200+ followers (organic — don't game it).
- [ ] LinkedIn updated, "open to remote."
- [ ] **Funnel:** 100+ outbound messages sent + 25+ application submissions + 5+ first-round interviews + Mercor active + at least one India safety app in flight.
- [ ] One lightning talk delivered or recorded.

If 7+ are checked by 2026-11-08, you are ready. Offers from there are a function of funnel volume + iteration on what's not converting.

# Master Plan — Avi's AI Engineer Roadmap

**Mission:** Become job-ready as an AI engineer in ~6 months at 8 hours/week by turning existing production GTM/LLM work into a defensible portfolio. Not starting over — closing specific gaps hiring managers screen for.

**Positioning:** AI engineer specializing in LLM-powered data and GTM systems. Real production experience with LLM classification pipelines, MCP servers, enrichment automation. Bengaluru-based, embedded in Clay operator community. Wedge: most AI-eng candidates are SWEs who built a chatbot — you're a GTM operator who shipped LLM systems that move revenue.

**Target by Month 6:** Actively interviewing with 3 production-grade projects, ~6 public posts, eval-first thinking, warm-intro funnel into Bengaluru AI startups and the Clay/GTM ecosystem.

---

## Start Here — Week 1 (begins Mon 2026-05-04)

This is the only thing you need to do this week. Don't read further until these are done.

1. **Set up the portfolio site** (3 hrs). Quarto or Astro. Pick in 30 min, don't overthink. Live URL by Sunday.
2. **Pull 50 real classifier traces** from past Clay/winery/HVAC runs (2 hrs). Dump into a single file or notebook.
3. **Read the free Hamel/Shreya material** (2 hrs): [hamel.dev/blog/posts/evals-faq](https://hamel.dev/blog/posts/evals-faq/) end-to-end + Eugene Yan's [LLM patterns post](https://eugeneyan.com/writing/llm-patterns/).
4. **Update [PROGRESS.md](./PROGRESS.md) Sunday night.** Honest hours, what shipped, what slipped.

After this week, switch to the monthly cadence in [ROADMAP.md](./ROADMAP.md).

---

## Repo Map — read in this order

| File | Purpose |
|---|---|
| [README.md](./README.md) | One-screen positioning |
| **MASTER_PLAN.md** (this file) | Strategy, audit, target roles, anti-patterns, resources |
| [ROADMAP.md](./ROADMAP.md) | Week-by-week plan with deliverables and "behind if" markers |
| [PROJECTS.md](./PROJECTS.md) | Specs and standards for the 3 flagship projects |
| [EXERCISES.md](./EXERCISES.md) | Monthly checklist (tick boxes as you go) |
| [PROGRESS.md](./PROGRESS.md) | Weekly log — update every Sunday |
| `month-1/` … `month-6/` | Per-month READMEs and any drill material |
| `projects/business-classification-pipeline/` | Project 1 home |
| `projects/gtm-clay-rag/` | Project 2 home |
| `projects/icp-research-agent/` | Project 3 home |

**Ignore:** the older `compass_artifact_wf-378304b4-...md` (backend/async foundations plan) and the `week-*` subfolders inside each month. Those came from an earlier four-month curriculum that's been superseded by this plan. Keep them as drill material only — do not treat them as canonical.

---

## 1. Honest Skill Audit

What you can defend in interviews **today** vs. what's missing.

### What you can already defend (cite these in every interview)

| Project | What it proves |
|---|---|
| Winery operating-status classifier | Prompt design, schema-driven extraction, business-context judgment, dealing with noisy real-world web data |
| HVAC distributor segmentation | Classification at scale, ICP-style reasoning encoded in prompts, edge cases and refusal handling |
| WIRLS enrichment sprint | Coordinating parallel LLM workstreams under deadline; **a hallucination audit** (exactly what hiring managers screen for); web search as fallback when MCP servers failed with auth errors |
| MCP server work in Clay/Smartlead pipelines | 2025-standard agent integration protocol that 90% of candidates have only read about |
| Clay Cup 2026 Bengaluru Nomination Round | Operator community credibility — relevant for FDE / DevRel / Solutions roles |

**Translate into hiring-manager language:**
- "Built LLM classification pipelines processing X records with prompt-driven extraction and validation"
- "Designed enrichment workflows with fallback retrieval when primary tool calls failed"
- "Ran a hallucination audit on a multi-pipeline output — caught Y% defect rate before delivery"

### What you cannot yet defend

| Gap | Why it matters | Where this gets fixed |
|---|---|---|
| Eval harnesses with golden datasets and aligned LLM-as-judge | Hamel Husain's hiring lens explicitly screens for this. "Did you look at your data?" is the canonical question. | Self-paced eval work (Month 1) + every project after |
| Retrieval-quality measurement (recall@k, MRR, NDCG, faithfulness) | RAG roles test this directly. Jason Liu: "RAG is just a recommendation system squeezed between two LLMs — improve search first." | Project 2 |
| Production deployment (Modal, Langfuse traces, cost/latency budget) | Demo on localhost ≠ shipped. | Every project deployed on Modal or Fly.io with Langfuse instrumentation |
| Agent reliability patterns — step budgets, tool surface area, trajectory evals | Agent engineering is the highest-paid sub-specialization in 2026. | Project 3 |
| Python fluency rebuild — async, typing, Pydantic, pytest, packaging | You don't need beginner Python; you need to be fast and idiomatic again. | Ambient via every project |
| Public technical writing | Eugene Yan and Hamel built careers on writing. Zero posts = invisible. | Monthly post starting Month 2 |
| Spoken AI engineering vocabulary | You can do the work; can you explain trade-offs in 2 sentences? | Mock interviews from Month 5 |

**Honest framing:** You're not transitioning *into* AI engineering. You're already doing parts of it without the title. The 6 months are about closing specific gaps and packaging existing work so hiring managers see what's there.

---

## 2. Target Roles and Companies

Three concentric circles. Don't restrict yourself early.

### Circle 1 — GTM-flavored AI engineer (your strongest wedge)

Where your production experience reads as senior-level immediately. Category exploded 11.4× in 2025. Demand outpaces supply at ~2.1 jobs per technical candidate.

- **Clay.com** — Forward-Deployed and internal GTMEs. You're already in this community.
- **Decagon, Sierra, 11x.ai, Artisan, Regie.ai, AiSDR** — sales/CS agent companies. 11x posts $150K–$220K for Agent Engineer.
- **Apollo.io, Common Room, Default, Persana** — GTM platforms hiring AI engineers who understand the actual work.
- **Hebbia, Glean, Mendable** — adjacent doc-Q&A companies that hire FDEs.

### Circle 2 — Bengaluru/India AI-native and remote roles

- **Sarvam AI** — Forward-Deployed Software Engineer / Strategic Deployment Engineer. JD almost custom-fit for your background.
- **Atlan** — context layer for data and AI; remote-first; agent governance and AI eng roles.
- **Postman** — growth and AI engineers building agents over their API knowledge graph.
- **Krutrim, Fractal, Razorpay AI** — local options. Krutrim has documented culture issues (NDTV Dec 2024, Blind reviews); apply with eyes open.
- **Remote-for-US Series A/B** via Mercor, Turing, or direct application — senior remote from Bengaluru reaches ₹60–80 LPA equivalent.

### Circle 3 — Applied AI / FDE at frontier and enterprise AI companies

- **Anthropic** — Applied AI Engineer, Forward Deployed Engineer (Boston/SF/NYC/London/Paris). JD requires "production experience with LLMs including advanced prompt engineering, agent development, evaluation frameworks."
- **OpenAI** — Research Engineer, Applied AI Engineering.
- **Harvey** ($180K–$280K SF), **Cresta**, **Cognition**, **Cursor (Anysphere)** — higher coding/DSA bar for the latter two.

### What to optimize for

Your 6-month target is a **first solid AI engineering offer**, not the absolute top of the market.

> **Technical-adjacent background + part-time prep = 4–6 months focused effort.** Plan for 6 months. Budget for 9.

Recruiter quote that defines the market (KORE1, 2026 LLM Engineer Hiring Guide): *"Three of every five resumes hitting our queue for an LLM engineering req right now are not, in any practical sense, LLM engineers. They are software engineers who shipped a LangChain demo."* The bar is lower than fear suggests — if you have shipped evidence with evals.

---

## 3. The Five Tracks

Every hour over six months goes into one of these. Re-balance monthly.

1. **Production fluency** — shipping projects on Modal/Fly with Langfuse instrumentation, cost/latency reasoning, live URLs.
2. **Eval-first development** — error analysis, golden datasets, aligned LLM-as-judge, regression tests in CI. Highest-leverage skill in 2026 hiring.
3. **RAG and retrieval engineering** — hybrid retrieval, contextual retrieval (Anthropic, Sept 2024), reranking, retrieval evals. Deepest and most-tested sub-skill.
4. **Agent engineering** — workflows vs agents (Anthropic distinction), step budgets, tool surface area, trajectory evals. Highest comp ceiling.
5. **Public footprint** — writing, OSS contributions, Bengaluru community presence, LinkedIn cadence, GitHub readability. Hireability multiplier.

Will *not* spend significant time on: building an LLM from scratch, deep DSA grind, classical ML refreshers, math from scratch, multiple agent frameworks. Explicit cuts — see Section 7.

---

## 4. The Three Flagship Projects

Three deep projects beat ten demos. Full specs in [PROJECTS.md](./PROJECTS.md). One-line summary:

| # | Project | Months | Project folder |
|---|---|---|---|
| 1 | Business classification pipeline + eval harness | 1–2 | [projects/business-classification-pipeline](./projects/business-classification-pipeline/) |
| 2 | RAG over GTM/Clay knowledge with retrieval evals | 3–4 | [projects/gtm-clay-rag](./projects/gtm-clay-rag/) |
| 3 | ICP research agent with trajectory evals | 5 | [projects/icp-research-agent](./projects/icp-research-agent/) |

**Common standard, every project:**
- Live deployed URL (Modal, Fly.io, or HF Spaces).
- README with: problem statement, architecture diagram, fresh-venv run instructions, **"Where it fails" section**, eval results table, cost-per-call, latency p50/p95.
- Eval dataset committed to repo.
- Iteration history in commits (not one giant initial commit).
- Langfuse trace screenshots in README.
- One public write-up with failure-mode honesty.

Standard comes from `alexeygrigorev/ai-engineering-field-guide` (analyzed 2,445 JDs and 100+ candidate take-homes Q4 2025–Q1 2026): eval suite + production thinking shows up in 39.6% of AI-First role responsibilities.

---

## 5. Six-Month Plan (Calendar)

Full week-by-week table is in [ROADMAP.md](./ROADMAP.md). Monthly anchors:

| Month | Window | Theme |
|---|---|---|
| 1 | 2026-05-04 → 2026-05-31 | Eval foundations + Project 1 design |
| 2 | 2026-06-01 → 2026-06-28 | Ship Project 1 (classification + evals) |
| 3 | 2026-06-29 → 2026-07-26 | RAG fundamentals + Project 2 design |
| 4 | 2026-07-27 → 2026-08-23 | Ship Project 2 (RAG + ablation) |
| 5 | 2026-08-24 → 2026-09-20 | Ship Project 3 (ICP agent) + portfolio polish |
| 6 | 2026-09-21 → 2026-10-18 | Job search execution |

### Month 1 substitution — free path (no Maven cohort)

The original plan assumed enrolling in Hamel Husain & Shreya Shankar's Maven AI Evals course (~$1,800). You're skipping the cohort. Free substitute:

- **Read** the Hamel/Shreya O'Reilly book *Evals for AI Engineers* (or the equivalent free posts on hamel.dev — `evals-faq`, `field-guide-to-rapidly-improving-ai-products`, `llm-judge`).
- **Read** Eugene Yan's [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/).
- **Apply Three Gulfs** (specification / generalization / comprehension) to 50 real classifier traces — open-coding by hand.
- **Self-pace with weekly deliverables** mirroring the Maven cohort weeks (open coding → axial coding → judge calibration).

Risk: no forced pacing. Mitigation: Sunday `PROGRESS.md` updates are non-negotiable. Slipping two Sundays in a row is the canary.

---

## 6. Interview Readiness Checklist

If you can't speak confidently and concisely on each, drill it.

### Foundations
- [ ] Tokenization, embeddings, attention at the conceptual level (Alammar's Illustrated Transformer or Karpathy's "Intro to LLMs" 3.5-hr video — pick one).
- [ ] Prompt patterns: zero-shot, few-shot, chain-of-thought, structured outputs.
- [ ] Function calling vs JSON mode vs Instructor vs BAML — when to use which.
- [ ] Cost and latency reasoning per model (Sonnet vs Haiku vs GPT-4o vs GPT-5 mini).

### Evals (interview-critical)
- [ ] Three Gulfs framework explained in 60 seconds.
- [ ] Open coding → axial coding → failure taxonomy walkthrough.
- [ ] LLM-as-judge calibration: critique shadowing, binary > Likert, agreement metrics (TPR/TNR/balanced accuracy).
- [ ] When LLM-as-judge fails (HaluEval's 58.5% number; Soboroff's "Don't use LLMs to make relevance judgments" for IR ground truth).
- [ ] Ragas metrics and their failure modes.

### RAG (deep)
- [ ] Five levels of chunking with when to use each.
- [ ] Anthropic's Contextual Retrieval prompt and the −67% retrieval-failure number.
- [ ] Hybrid retrieval — why BM25 still matters (technical identifiers, exact match, code symbols).
- [ ] Reranker landscape — Cohere 3.5 vs Voyage Rerank 2.5 vs zerank-1.
- [ ] When NOT to use RAG — long-context (<200k tokens, static corpus), structured DB queries, fine-tuning for style.

### Agents
- [ ] Workflow vs agent distinction (Anthropic's framing).
- [ ] The five workflow patterns + agent pattern.
- [ ] Step budgets, tool surface area, idempotency tokens, taint tracking.
- [ ] Trajectory evals vs final-output evals.
- [ ] Why multi-agent uses 10–15× more tokens (Anthropic's number) and when it's worth it.
- [ ] Lethal trifecta (Simon Willison).

### System design prompts to drill (each in 45 minutes)
- [ ] Design a doc Q&A system.
- [ ] Design a customer-support classifier with handoff to human.
- [ ] Design an ICP research agent.
- [ ] Design an LLM-powered enrichment pipeline with fallback retrieval.
- [ ] Design an evaluation harness for an LLM product.

### Coding fluency (modest by SWE standards, focused)
- [ ] Write a Pydantic model for a non-trivial nested structured output without lookup.
- [ ] Write a pytest suite that runs LLM-judge evals on a golden dataset.
- [ ] Implement BM25 + dense hybrid with RRF in <50 lines.
- [ ] Use async/await for parallel LLM calls without deadlocks.
- [ ] Cursor / Claude Code use is fluent.

### DSA stance
Most AI-native startups (Circles 1 and 2) test ML implementation and system design more than classic LeetCode. **Cursor, OpenAI, Anthropic** are exceptions — higher DSA bar. If you target those, budget separate prep; otherwise drill 30–40 LeetCode mediums total over Months 5–6, focused on arrays, hash maps, graphs.

---

## 7. Rules and Anti-Patterns

Re-read this every Sunday for the first three months.

### Rules
1. **Eval before scale.** Every project gets a golden dataset before you optimize anything else.
2. **Workflow before agent.** Default to deterministic code; add agentic dynamism only at the node where it's genuinely needed.
3. **One framework or none.** Raw SDK + Pydantic + Instructor is the default. Add LangGraph or PydanticAI only when state/cycles genuinely require it.
4. **Production thinking shows up in the README.** "Where it fails," cost-per-call, latency p50/p95, eval results table. No exceptions.
5. **Public > private.** Ship to a URL. Write the post. Tag people. Hidden work doesn't count.
6. **Lean into your wedge.** GTM domain expertise + Clay community + production LLM experience is your unfair advantage. Don't talk yourself out of it to look more like a generic SWE candidate.

### Anti-patterns to refuse
1. **Tutorial-finishing.** Watching DLAI courses without shipping is procrastination dressed up as learning.
2. **Framework collecting.** "I learned LangChain, LlamaIndex, CrewAI, AutoGen, LangGraph" reads as beginner. "I shipped three projects with raw SDK + LangGraph at the one node that needed it" reads as senior.
3. **Fake claims.** Don't say "I built an agent" if you wrote a single LLM call. Hiring managers see through this in 90 seconds. Use precise vocabulary (workflow vs agent, classification vs extraction, retrieval vs generation evals).
4. **Demo without evals.** A Streamlit chatbot wrapper is a 2023 portfolio. In 2026 it's a negative signal.
5. **Generic LLM-as-judge** — running Ragas with default prompts and trusting the numbers. Calibrate against your own labels or the score is noise.
6. **Hype-posting on LinkedIn.** Don't post "the future of AI is exciting." Post your specific eval table with the failure mode you found.
7. **Ignoring the Bengaluru network.** Indian AI hiring runs on warm intros and LinkedIn. You already have community via Clay Cup. Use it.
8. **Optimizing for the wrong roles.** Don't grind LeetCode for FAANG when your strongest fit is a Clay-adjacent GTM-AI startup. Pick the funnel that matches your wedge.

### Things to deliberately skip
- Building an LLM from scratch (40–60 hrs, ~zero hireability for AI eng vs ML eng).
- Deep DSA grind unless targeting Cursor/OpenAI/Anthropic SWE.
- Multiple agent frameworks. Pick one (or none — raw SDK).
- fast.ai, full Andrew Ng ML specialization, math from scratch.
- Daily paper-of-the-day. Skim Latent Space's curated list once a quarter.

---

## 8. Public Footprint Plan

### Blog
- Personal site at your own domain. Quarto (Hamel's stack) or Astro. Don't overthink. Ship in Week 1.
- Cadence: 1 post/month minimum, with one big push at end of Month 6.
- Cross-post the announcement on LinkedIn and X. Canonical version on your domain.
- **Do not use Medium or dev.to** — they signal beginner in 2026 AI engineering circles.

### GitHub
- Pinned repos: the three flagship projects with READMEs to standard.
- Profile README naming the positioning ("AI engineer building LLM-powered data and GTM systems") and linking to the three projects + blog.
- Commit history visible — show iteration, not single dumps.

### LinkedIn (highest-ROI surface for India hiring)
- Headline updated by Month 5: *"AI engineer | LLM pipelines for GTM data | Bengaluru"*.
- Post every project ship + every blog post + every meetup attended.
- Don't post AI hype; post specific work and what you learned. Bangalore AI recruiters live here.

### X / Twitter
- Optional but useful for technical credibility. Follow Hamel, Eugene Yan, Jason Liu, Simon Willison, Harrison Chase, Swyx. Reply with substance occasionally; don't post hot takes.
- Canonical writing on your domain — X external links are penalized 30–50% since March 2025.

### Open-source contributions (low time budget, high signal)
Pick **one** repo and make a real contribution:
- **Instructor** (jxnl/instructor) — cookbook example for a GTM use case. Jason Liu is responsive.
- **Langfuse** — framework adapter or eval pipeline example.
- **Ragas** — domain-specific metric or dataset adapter.
- **simonw/llm** — write a plugin (lowest barrier, high visibility).

One merged PR with a useful README addition and tests > five drive-by typo fixes.

### Bengaluru community
- 1 meetup/month from Month 3. Lightning talk by Month 4 or 5 — recordings are permanent portfolio assets.
- **Recommended groups:** Bangalore AI Developers Group (AICamp); Bangalore MLOps Community; AgentsNexus India / GenAI Bangalore; BangPypers; TensorFlow User Group Bangalore; Build Club India.
- **Conferences worth attending in 2026:** Warpspeed by Lightspeed; The Great Bengaluru Hackathon (Sarvam x HackCulture); Hugging Face × Inferless × Sequoia Generative AI Meetup; ConfAI at Plaksha; CASML at IISc; BDA at IIIT-Bangalore; IEEE Bangalore Section Agentic AI Summit.
- **Clay operator network is your wedge.** You co-organized Clay Cup 2026 Bengaluru — a credential most candidates can't claim. Mention it in cover letters to GTM-AI companies.

---

## 9. Curated Resources

### Books (priority order)
1. **Chip Huyen, *AI Engineering* (O'Reilly, 2025)** — Ch. 1, 3, 5, 6, 10 deeply; skim 7, 9. ~15 hrs.
2. **Eugene Yan + Hamel + Jason + Shreya + Bryan + Charles, *What We've Learned From a Year of Building with LLMs*** ([applied-llms.org](https://applied-llms.org)) — free, ~3 hrs. **Non-negotiable.**
3. **Hamel Husain & Shreya Shankar, *Evals for AI Engineers* (O'Reilly, 2025)** — replaces the Maven cohort for you.
4. **Jay Alammar, *Hands-On Large Language Models*** — selectively, for tokenization/embeddings/semantic search.
5. **Skip:** Sebastian Raschka's *Build an LLM From Scratch* (excellent but career-irrelevant for API-layer AI eng — save for after the offer).

### Courses (free / cheap)
1. **DeepLearning.AI short courses (free, 1–2 hrs each)** — *Evaluating AI Agents*, *Functions/Tools/Agents with LangChain*, *Improving Accuracy of LLM Applications*, *AI Agents in LangGraph*. Cherry-pick 3–4.
2. **Karpathy's "Deep Dive into LLMs like ChatGPT"** (3.5 hrs, free, YouTube) — for intuition.
3. **improvingrag.com** — Jason Liu's RAG framework, free.
4. **Skip:** Stanford CS336 (cherry-pick 1–2 lectures only), full Karpathy Zero-to-Hero, fast.ai, full ML specializations. Research-engineer paths, not AI-engineer paths.

### Blogs (subscribe; batch-read Sunday)
- **hamel.dev** — eval-driven development; the FAQ post is gold.
- **eugeneyan.com** — patterns, evaluation, the canonical voice.
- **applied-llms.org** — group blog, definitive.
- **jxnl.co** — RAG and agent flywheels.
- **simonwillison.net** — daily LLM news and primary-source links.
- **anthropic.com/news + /research** — Contextual Retrieval, Building Effective Agents, MCP.
- **Latent Space (latent.space)** — Swyx; the 2025 AI Engineering Reading List is meta-canon.
- **Ahead of AI (Sebastian Raschka)** — best paper summaries.

### Papers — skim only, ~5–8 hrs total over six months
- *Attention Is All You Need* (2017) — 15-min skim.
- *RAG* (Lewis et al., 2020) — abstract + figure 1.
- *Chain-of-Thought* (Wei et al., 2022) — 5-min skim.
- *ReAct* (Yao et al., 2022) — 10-min skim.
- *Lost in the Middle* (Liu et al., 2023) — figures, 10 min. Implication for RAG chunk ordering.
- *LLM-as-Judge with MT-Bench* (Zheng et al., 2023) — abstract.
- *Anthropic Contextual Retrieval* (Sept 2024) — full read, 30 min. Implement in Project 2.
- *Building Effective Agents* (Anthropic, Dec 2024 + 2025 expansion) — full read.
- *DeepSeek-R1* (Jan 2025) — Raschka's literature review, not the paper.
- *Effective context engineering for AI agents* (Anthropic, Sept 2025) — full read.

### Tools
- **Cursor** ($20/mo) — daily IDE.
- **Claude Code** — for complex multi-file work; pair with Cursor.
- **Modal** — deploy. $30/mo free credits.
- **Langfuse** (self-host or free cloud, 50K obs/mo) — tracing from line one.
- **Instructor** — default structured-output choice.
- **Ragas** — RAG evals.
- **pgvector + Postgres** — default vector store. Don't pay for Pinecone unless you have to.

---

## 10. Notes to Self

### Your Bengaluru context is real
- Local market pays ₹35–60 LPA at GenAI specialist mid level, ₹65 LPA–₹1.2 Cr total comp at FAANG India per shifttotech and taggd 2026 data. Remote-for-US from Bengaluru reaches ₹60–80 LPA equivalent.
- Sarvam's FDSE role reads almost custom-fit for your profile. Apply when ready, even if you feel under-qualified — JDs in 2026 over-list.
- Krutrim has documented culture concerns. Don't ignore signals just because the role looks shiny.
- LinkedIn is the recruiter platform in Bangalore. Prioritize over X for the job search.

### Your Clay community is your wedge — use it deliberately
- Clay Cup 2026 Bengaluru Nomination Round is on your CV. Most AI engineering candidates don't have community-organizing credentials. Forward-deployed and solutions-engineering hiring managers value this directly.
- The Clay operator network includes people at or who know hiring managers at Clay, Common Room, Apollo, Default, 11x. Your warm-intro funnel into GTM-AI roles is wider than 95% of candidates'. Build the bridge before you need to walk it.
- Applying to Clay-adjacent companies (Decagon, Sierra, 11x, Hebbia)? Open with what you've shipped on Clay and MCP — shared vocabulary they don't have to translate.

### Your GTM background is a feature, not a bug
- "GTM Engineer" grew 11.4× in 2025 (Steven Moody benchmark) and pays $137K–$252K in the US. Companies hiring this title explicitly want operators who can code, not SWEs learning sales.
- Hamel and Eugene's writing repeatedly emphasizes domain expertise as the biggest predictor of useful AI products. You have GTM domain expertise. That's worth more than a CS degree to any AI company building for the GTM market.
- "Tell me about a hard production LLM failure" — you have the WIRLS hallucination audit. Stronger than 90% of candidates can give.

### Your biggest risk is drift, not capability
- 8 hrs/week sounds like a lot until weeks 5–8 when project work gets hard and writing feels optional. **Without the Maven cohort's forced pacing, Sunday `PROGRESS.md` updates are your only insurance.** Don't skip even one.
- Cost of finishing a month behind is not catastrophic. Cost of three months of silent drift is.

### Be willing to go faster if you can
- Strong week? Push to Project 2 design earlier. Month boundaries are guides, not laws.
- Bengaluru company posts a role that fits *now* — apply now. Don't wait until Month 6. Funnels take time; you can interview while still building.
- Great speaking slot at a meetup in Month 3? Take it even if the project isn't fully polished. Talks recorded in March become permanent assets by June.

### One last thing
You're not switching careers. You're upgrading the title on work you're already doing. The next six months are the smallest, most leveraged version of that upgrade. Stay specific, ship visibly, and protect the eight hours.

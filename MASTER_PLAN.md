# Master Plan — Manveen's AI Engineer Roadmap

**Mission:** Be hireable as a junior **GenAI / LLM Application Engineer** by November 2026, on 8–10 hours/week, with three deployed projects, an MCP server, and an OSS contribution that prove eval-first thinking.

**Window:** 2026-05-25 → 2026-11-08 (24 weeks). Currently: pre-Week 1 reset.

**Wedge:** Final-year BTech who has *already* shipped a full-stack GenAI SaaS (PresentAI) and a CV/PyTorch project (AsanaBot), plus production-flavored automation experience from Caprae and Precise Leads internships. Add an eval-first portfolio + MCP server + OSS contribution on top and you skip the entire "looks-like-every-other-fresher" pile.

---

## 1. Why this plan replaces the old one

The previous plan was written for a different persona — a Bengaluru-based senior GTM engineer with years of Clay/winery/HVAC production traces and a Clay Cup community position. You don't have that profile. You have a *better-for-juniors* profile (real shipped GenAI app + CV project + two internships + active GTM role), and the plan now reflects it.

**What carries forward from your last three weeks:**
- 50 staffing-firm classifier traces in [projects/business-classification-pipeline/data/traces-week-1.jsonl](./projects/business-classification-pipeline/data/traces-week-1.jsonl)
- Saturday open-coding notes in [notes/week-1-saturday-notes.md](./notes/week-1-saturday-notes.md) (genuinely good thinking — three named failure modes)
- Modal hello-world + Instructor speedrun in [month-1/test files/](./month-1/test%20files/)
- Awareness of Hamel's evals canon and the Three Gulfs framework

**What changes:** the project shapes are no longer Clay/winery/HVAC-themed; the project codenames are now `leadlens` / `docsight` / `reposcout`; Week 1 is a code-rebuild week (not a tooling-setup week); MCP server is explicit in Project 3; the funnel is India-product + India-remote primary, US/EU-remote stretch.

## 2. Target role recommendation

After the research brief, the recommendation is **GenAI / LLM Application Engineer with an agent tilt**. Reasoning:

| Why this role | Why not the others |
|---|---|
| Highest-volume junior hiring bucket in 2026 — most JDs in this category | ML Engineer wants MS or strong publications; very hard at fresher level |
| Bar is "ship working LLM features + evals," not "derive backprop" — winnable | MLOps Platform wants 2+ yrs SWE infra; you don't have that yet |
| Directly compounds what you've already built (PresentAI ≈ this work, AsanaBot proves PyTorch literacy on the side) | Forward-Deployed Engineer wants 2–3 yrs customer-facing; door opens after 1st job |
| Indian product startups (Sarvam, Razorpay, Postman, Atlan, Eka, Glean BLR, Sprinklr) actively hire juniors for this | Pure agent-engineer roles exist but small junior market |
| Same portfolio also qualifies for US-remote stretch (Sierra, Decagon, 11x India ICs) | |

**You can re-target later** — once you have a junior offer in hand, the next jump to FDE / agent engineer / ML eng is much easier than the first one is now.

## 3. Honest skill audit (Manveen, May 2026)

### What you can already defend in interviews
| Asset | What it proves |
|---|---|
| **PresentAI** (Next.js + Gemini + Clerk + Prisma + PostgreSQL) | Full-stack GenAI app shipping; auth + DB + state; prompt-driven generation; SaaS-shaped thinking. *Most fresher candidates don't have this.* |
| **AsanaBot** (Vision Transformers + MediaPipe + OpenCV) | PyTorch literacy, real-time video, model selection, deployment-shaped thinking |
| **Caprae internship** (Sasquatch data pipelines) | Production data pipelines, validation layers, "blocked 35% of erroneous records" = quality-aware engineering |
| **Precise Leads** (n8n + scraping + Slack) | Workflow orchestration in production, multi-source data joins, "40% manual time reduction" = outcome framing |
| **50 staffing-firm classifier traces + open-coding notes** | You've already started eval-first thinking — three named failure modes on real data |

### What you cannot yet defend (the 24-week target list)
| Gap | Why it matters | Where it gets closed |
|---|---|---|
| **Modern Python fluency** — async, typing, Pydantic, uv, ruff, pytest | Every junior screen tests live coding; AI-written code on your CV with no muscle behind it is a major risk | Month 1, Week 1 code-rebuild block + threaded daily warm-ups |
| **Eval harnesses with golden datasets + calibrated LLM-as-judge** | The single highest-signal junior portfolio artifact in 2026 (research confirms) | Project 1 (leadlens), Months 1–2 |
| **Retrieval-quality measurement** (recall@k, MRR, NDCG, faithfulness, context precision) | RAG roles test this directly; you don't have this yet | Project 2 (docsight), Months 3–4 |
| **Production deployment story** (Modal, Langfuse traces, p50/p95, $/call) | "Runs on my laptop" reads as student in 2026; deployed + observed reads as engineer | Every project deployed |
| **Agent reliability patterns** — step budgets, tool surface area, idempotency, trajectory evals | Highest comp ceiling, only hire-able after a junior offer but worth credentialing now | Project 3 (reposcout), Month 5 |
| **MCP server literacy** | Table-stakes in 2026 — Anthropic open-sourced Nov 2024, by mid-2026 it's the way tools are exposed to Claude/ChatGPT/Cursor | Project 3 |
| **Public technical writing** | Most juniors don't have any — even one well-written post moves you up the stack | 4–6 posts across 24 weeks |
| **One merged OSS PR to a known LLM repo** | Signals you can read others' code, hold a PR conversation, ship inside someone else's codebase | Month 3 or 4 (Instructor, Langfuse, Ragas, simonw/llm, LiteLLM — pick one) |

### What you don't need to grind (but should still be able to *speak* to)
- **Build-an-LLM-from-scratch (nanoGPT).** Watch Karpathy once. Skip the grind.
- **400 LeetCode problems.** Junior AI-eng interviews at AI-native startups lean lighter on DSA. 60–80 problems focused on arrays/hash maps/strings/graphs is enough. (GCC + Razorpay-style platform roles weight DSA heavier — add 30 more if you target those.)
- **Full Andrew Ng ML specialization or Stanford CS231n.** Tangential to LLM-app work. You already know enough classical ML to talk about it.
- **fast.ai.** Excellent but not on the critical path.
- **Daily paper-of-the-day.** Replace with one weekly deep-read (Latent Space + AI News).
- **Heavy MLOps (Kubeflow, MLflow, Airflow).** Not a junior AI-eng signal anymore.

### Things you must *be able to speak to* even if you don't deep-build with them
Live JD evidence (Sarvam FDE, Thiranmi AI Backend, multiple LinkedIn India listings, May 2026) shows these are explicitly listed across postings. You'll spend 30–60 min on a notebook for each, then move on.

- **CrewAI + AutoGen** — try one 30-min notebook each in Month 5. Know when each is the wrong choice vs LangGraph.
- **LlamaIndex** — try one ingestion + query notebook in Month 3 alongside your raw RAG build. Listed at almost every India RAG JD alongside LangChain.
- **Pinecone** — one 30-min sandbox in Month 3. Default to pgvector in your project, but JDs still ask about Pinecone.
- **AWS Bedrock + Lambda basics** — one tutorial each in Month 4 or 5. Increasingly mentioned in India JDs.
- **Docker + Compose** — actually use it in Project 2 deployment. Not optional anymore.
- **Celery / Kafka basics** — conceptual + one minimal Celery setup in Month 4 (async tasks for ingestion). RabbitMQ/SQS = same vocabulary.
- **Guardrails + LLM safety basics** — Anthropic Skills docs + Guardrails AI repo skim, 1 hr in Month 5.

## 4. Target funnel (US-remote primary, India backup)

You raised it directly: India fresher AI-eng hiring is brutal (most JDs ask 2–5 yrs and screen on college tier and DSA), and you already do outbound for a living at Precise Leads. Pointing that exact skill at US founders/CTOs is your wedge — most AI-eng candidates can't do outbound. The funnel inverts accordingly.

### Primary funnel — US-remote (3 channels, run all three in parallel from Month 4)

**Channel A — Curated remote job boards** (apply weekly, the "warm portal" path)
- [HN "Who is Hiring?" monthly thread](https://hnhiring.com/locations/remote) — first Tuesday of each month. Filter for "AI / LLM / RAG / agents." Junior-friendly + founder-written JDs.
- [YC Work at a Startup](https://www.workatastartup.com/) — filter: AI + remote + open to junior. 51 India HQ + ~hundreds remote-friendly.
- [Wellfound](https://wellfound.com/) (formerly AngelList) — startup-heavy, often founder-screened.
- [WeWorkRemotely](https://weworkremotely.com/) and [Arc.dev](https://arc.dev/remote-jobs/llm).
- Direct careers pages: Sierra, Decagon, 11x.ai, Harvey, Hebbia, Cresta, Glean — they hire India ICs for some roles.

**Channel B — Talent marketplaces** (apply once, get matched)
- **[Mercor](https://www.mercor.com/) — highest priority.** Their interview is *exclusively on your open-source contributions*. The OSS PR in this plan is no longer a checkbox; it's the *primary asset* for this route. Apply in Month 4 once the PR is merged. Hiring takes ~60 days; payouts weekly via Stripe Connect, USD-denominated.
- [Turing](https://www.turing.com/jobs/remote-ai-jobs) — assessment-heavy. Lower selectivity than direct apps, lower pay ceiling than Mercor.
- A.Team, Pesto, Pallet, Crossover — secondary; only after Channels A and C are running.

**Channel C — Direct outbound to US founders** (your unfair advantage)
- Target: post-Seed / Series A AI startups that *just raised* but haven't hired AI engineers yet (lag is usually 2–6 weeks between raise announcement and posting). Find via [TechCrunch funding announcements](https://techcrunch.com/category/venture/), [Stripe Atlas weekly digest](https://stripe.com/atlas), [Pitchbook](https://pitchbook.com/) Twitter alerts, and YC Bookface RSS if you have access.
- Volume math (research confirms): **100–200 personalized messages → 5–10 qualified conversations → 1–3 trial contracts → 1 FT-equivalent**. Doable over Months 5–6 at 1 hr/day on outreach.
- Pitch shape (Insight Email, then Specific Offer): one observation about their product/blog/launch + one specific 2-week trial you'd do for them (build their internal RAG eval suite; ship a customer-facing classifier; instrument their existing agent with Langfuse traces; build them an MCP server). Not "I'm looking for a job." Not "I have these skills."
- This is exactly what you do at Precise Leads. The only difference is the target ICP is "US AI startup CTO who just raised," not staffing firms.

**Compensation expectations (May 2026 live data):**
- Indian remote AI eng cost to US employers: $500–950/week ($26k–49k/year) all-inclusive. (F5 Hiring Solutions, May 2026.)
- Contract entry rate: $30–50/hr for a fresher with shipped portfolio.
- Reasonable 12-month trajectory: contract trial → FT-remote at $50–80k USD with equity.
- "4–6 weeks from purposeful start to first dollar" is aggressive but documented as achievable.

### Secondary funnel — India product startups + India remote (the safety)
Run this in parallel from Month 5 so November isn't all-or-nothing.

**AI-native:** Sarvam, Krutrim (apply with eyes open — documented culture issues), Fractal AI Labs, Razorpay (Magic), Postman (AI features), Atlan, Eka.care, Glean Bangalore, Sprinklr AI, Yellow.ai, Haptik, Setu, Zluri, BrowserStack AI, Uniphore, Rocketlane, Observe.AI, Peakflo (YC, RAG-heavy, hiring 0.5–2 yr range).
**GCC AI teams (floor option):** Microsoft India, Google India (Gemini eng), Adobe AI, Salesforce, ServiceNow.
**TC band, fresher / 0–1 yr (directional, May 2026):** ₹10–25 LPA at startups; ₹18–30 LPA at top-tier product startups; ₹8–14 LPA at GCC AI-aliased roles.

### What the same portfolio buys you in each funnel
| Funnel | What lands you a first round |
|---|---|
| **US-remote — direct outbound** | A *specific* 2-week trial offer + 1 deployed project demoable in 30 seconds + a Loom walkthrough + a personalized observation about their work. Eval table on the project doubles reply rate. |
| **US-remote — Mercor** | 1 merged OSS PR + GitHub profile with 4–6 months of daily-ish activity + 3 deployed projects in pinned repos. **The PR is the interview.** |
| **US-remote — HN/Wellfound/YC apply** | Same portfolio + a sharp blog post (one that gets shared) + a Loom video walkthrough. |
| **India product startup** | 2 deployed LLM apps + public eval suite + blog post + GitHub graph + warm intro through OSS or local meetup. Lighter DSA. |
| **India GCC AI** | Same as above + a leetcode-easy DSA round + cleaner README presentation. |

## 5. The six tracks

Every hour goes into one of these. Rebalance monthly.

1. **Code fluency rebuild** — daily 5-min no-AI warm-ups, weekly 2–3 hr build blocks, modern Python stack. The most-underrated track for someone whose AI dependency has grown.
2. **Eval-first development** — Hamel/Shreya canon, open coding, golden datasets, calibrated LLM-as-judge, CI gates. The single highest-leverage skill in 2026 hiring.
3. **RAG / retrieval engineering** — chunking, hybrid (BM25 + dense), Anthropic Contextual Retrieval, rerankers, Ragas-style generation evals. The deepest sub-skill tested in interviews.
4. **Agent engineering + MCP** — workflow-first, step budgets, idempotency, trajectory evals, plus an MCP server. The highest comp ceiling.
5. **Public footprint** — blog (own domain, not Medium/dev.to), LinkedIn, GitHub readability, OSS contribution, community presence. The hireability multiplier.
6. **Outbound channel & US-funnel hygiene (your unfair advantage)** — sourcing US AI founders/CTOs from funding announcements, HN, YC, Twitter; Insight-Email outreach in volume; Loom video walkthroughs as the standard demo; building public credibility in US-resonant vocabulary (X, GitHub, Latent Space/AI Tinkerers Discord), not Indian-recruiter vocabulary. **You don't need to learn this — you do it for a living. You need to *point* it.** Starts light in Month 3, ramps Months 5–6.

## 6. The three flagship projects

Three deep projects beat ten demos. Full specs in [PROJECTS.md](./PROJECTS.md). One-line summary:

| # | Codename | Months | What it proves |
|---|---|---|---|
| 1 | **leadlens** | 1–2 | Eval-first development on a real classifier (evolves your existing staffing-firm work) |
| 2 | **docsight** | 3–4 | Production RAG with measured retrieval quality, hybrid search, reranking |
| 3 | **reposcout** | 5 | Agent design + MCP server + trajectory evals, composing 1 + 2 as tools |

**Common standard, every project:**
- Live deployed URL (Modal preferred — $30/mo free credits).
- README with: problem statement, architecture diagram, fresh-venv run instructions, **"Where it fails" section**, eval results table, $/call, latency p50/p95.
- Eval dataset committed to repo.
- Iteration history visible in commits (not one big initial dump).
- Langfuse trace screenshots in README.
- One public blog post with failure-mode honesty.
- A 3-minute Loom walkthrough linked from the README (US-remote funnel ROI).

## 7. Anti-patterns to refuse (re-read every Sunday for first three months)

1. **Letting AI write everything.** Your single biggest risk. Code without typing it rots fluency, and live coding interviews will expose it in 15 minutes. Hand-code warm-up daily, AI is a pair after that.
2. **Tutorial-finishing.** Watching DLAI / HF Learn / Anthropic courses without shipping is procrastination dressed as learning. Each course module triggers one small build.
3. **Framework collecting.** "I learned LangChain, LlamaIndex, CrewAI, AutoGen, LangGraph" reads as beginner. "I shipped three projects with raw SDK + LangGraph at the one node that needed it" reads as senior.
4. **Fake claims.** Don't say "I built an agent" if you wrote a single LLM call. Don't say "I deployed to production" if it's localhost. Hiring managers see through this in 90 seconds.
5. **Demo without evals.** A Streamlit chatbot wrapper was a 2023 portfolio. In 2026 it's a negative signal.
6. **Generic LLM-as-judge.** Running Ragas with default prompts and trusting the numbers. Calibrate against your own labels or the score is noise.
7. **Hype-posting on LinkedIn.** Don't post "the future of AI is exciting." Post your specific eval table with the failure mode you found.
8. **Pinning identity to the GTM angle.** That was the previous plan's wedge. Yours is "fresher who ships full-stack GenAI + has eval discipline" — let GTM be background, not headline.
9. **Skipping the code-rebuild because the AI projects feel more fun.** Project 1 needs you typing real code into real files. Resist the urge to vibe-code your way through it.

## 8. Interactive learning curriculum (your explicit ask)

Eight passive video hours teach less than two interactive build hours. The plan threads these mechanisms into every week:

- **Daily 5-min no-AI keyboard warm-up.** Tiny exercises (Python tricks, type hints, Pydantic snippets). Goal: hands-on-keyboard reps to rebuild muscle.
- **Weekly "Build Block" (2–3 hrs).** Hands-on coding only. No reading allowed. The actual project moves forward.
- **Weekly "Read+Drill" (1–2 hrs).** Short reading then a 30-min exercise applying it. No reading without a build.
- **Weekly Public Push.** A commit, a tweet, a README diff, a screenshot — something visible weekly.
- **Monthly "Demo Day Loom."** Record a 3-min walkthrough of what shipped that month. Post on LinkedIn + GitHub README. Builds the on-camera muscle hiring managers test in final rounds.
- **The "Stuck Box" rule.** When stuck >20 min, log the symptom in `PROGRESS.md`, *then* ask AI. Never silently struggle two hours, never silently let AI write three files. Both are failure modes.
- **Weekly Sunday `PROGRESS.md` update.** Non-negotiable. The single forcing function for self-paced work.

### Resources prioritized for interactivity (use these, skip the rest)

**Hands-on / build-along (priority):**
- [Anthropic Courses (GitHub)](https://github.com/anthropics/courses) — prompt engineering, tool use, RAG, MCP. All notebook-based.
- [Hugging Face Learn](https://huggingface.co/learn) — Agents Course + LLM Course are the best free interactive curricula in 2026.
- [DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/) — pick four: *Building Agentic RAG with LlamaIndex*, *AI Agents in LangGraph*, *Building Evaluations of LLM Apps*, *Building MCP Apps*. Skip the rest.
- [Jason Liu — Instructor docs](https://python.useinstructor.com/) + his free RAG content.
- [Hamel Husain blog](https://hamel.dev/blog/posts/evals/) — eval-driven development; the FAQ post is gold.
- [Modal Labs examples repo](https://modal.com/docs/examples) — best way to learn serverless GPU inference by doing.
- [OpenAI Cookbook](https://cookbook.openai.com/) — task-oriented notebooks.
- [LangChain Academy](https://academy.langchain.com/) — free LangGraph course.

**Passive video (one-shot only, do not loop):**
- Karpathy "Intro to LLMs" + "Deep Dive into LLMs" — watch once, mid Month 1.
- Latent Space podcast — weekly background, while commuting/eating.

**Books (priority order):**
1. Chip Huyen, *AI Engineering* (O'Reilly 2025) — Ch 1, 3, 5, 6, 10 deeply; skim 7, 9.
2. [applied-llms.org](https://applied-llms.org) — free, ~3 hrs. Non-negotiable.
3. Hamel & Shreya, *Evals for AI Engineers* (O'Reilly 2025).
4. Jay Alammar, *Hands-On Large Language Models* — selectively, tokenization + embeddings sections.

**Papers — skim list, ~5 hrs over 24 weeks:**
- *Attention Is All You Need* (15-min skim)
- *RAG* — Lewis et al. 2020 (abstract + Fig 1)
- *Chain-of-Thought* — Wei et al. 2022 (5 min)
- *ReAct* — Yao et al. 2022 (10 min)
- *Lost in the Middle* — Liu et al. 2023 (figures, 10 min)
- *Anthropic Contextual Retrieval* — Sept 2024 (full read, 30 min — implement in Project 2)
- *Building Effective Agents* — Anthropic, Dec 2024 (full read — frames Project 3)
- *Effective context engineering for AI agents* — Anthropic, Sept 2025 (full read)

**Tools:**
- **Claude Code + Cursor** — paired daily IDEs. Claude Code for multi-file work, Cursor for fast edits.
- **Modal** ($30/mo free credits) — default deploy.
- **Langfuse** (free cloud, 50K obs/mo) — tracing from Day 1 of each project.
- **Instructor** — default structured-output choice.
- **Ragas** — RAG evals.
- **pgvector + Postgres** — default vector store. Don't pay for Pinecone.
- **uv** — replaces pip + venv. Faster, modern.
- **ruff** — replaces black + flake8 + isort. One tool.

## 9. Public footprint plan (US-resonant from Day 1)

The audience to optimize for is **US AI founders/CTOs and engineering leads at AI startups**, not Indian recruiters. Different audience, different vocabulary, different surfaces. India recruiters will *also* find this footprint — but the reverse is not true.

### Blog
- Personal site on your own domain. **Quarto** (Hamel's stack) or **Astro**. Pick in 30 min, ship in Week 1.
- Cadence: 1 post/month from Month 2 onward.
- Cross-post the announcement on LinkedIn + X. **Canonical version on your domain.**
- Voice: failure-mode honesty, specific numbers, screenshots of eval tables and traces. Not "5 tips for prompting." Not "the future of AI is exciting."
- Do not use Medium or dev.to — they signal beginner in 2026 AI engineering circles.

### GitHub (the *first* place a US founder or Mercor reviewer looks)
- Pinned repos: leadlens, docsight, reposcout — with READMEs to standard.
- Profile README with positioning ("AI engineer | LLM systems with evals | MCP servers | open to remote contracts") + project links + blog link + Loom links.
- Commit graph visible. Show iteration, not single dumps. **Daily-ish activity for 4–6 months is a Mercor screen filter** — treat green squares as a job artifact, not vanity.
- Each project repo has a 3-min Loom video walkthrough linked at the top of the README.

### X / Twitter (much higher leverage for US audience than India audience)
- Move from "optional" to "secondary surface." Bio: positioning + portfolio link.
- Follow Hamel, Eugene Yan, Jason Liu, Simon Willison, Harrison Chase, Swyx, Shreya Shankar, Andrej Karpathy, Greg Kamradt, Logan Kilpatrick.
- 3 posts/week minimum from Month 3: build-in-public progress, eval table screenshots, "here's the bug I hit and how I fixed it." Reply to 3 substantive threads/week.
- Canonical writing on your domain — X external links are penalized 30–50% since March 2025, so post the meat in the thread itself + link to long version.

### LinkedIn (the India backup channel)
- Headline updated by Month 4: *"AI engineer | LLM systems with evals | MCP servers | open to remote"*.
- Post every project ship, every blog post, every OSS PR merged.
- Don't post AI hype. Post your specific eval table with the failure mode you found.

### Open-source contribution (high leverage; Mercor-mandatory)
Pick **one** repo and make a real contribution by **end of Month 4** (not Month 5 — earlier is better, especially for Mercor):
- **Instructor** (jxnl/instructor) — cookbook example using one of your projects. Jason Liu is responsive.
- **Langfuse** — framework adapter or eval pipeline example. They use Discord; ask first.
- **Ragas** — domain-specific metric or dataset adapter.
- **simonw/llm** — write a plugin (lowest barrier, high visibility). Simon is responsive.
- **LiteLLM** — provider/adapter PR.
- **Bonus targets:** PydanticAI (lower competition), Letta (memory), Helicone (observability), Outlines (structured output).

One merged PR with a useful README addition + tests + a Discord/Twitter thank-you from a maintainer > five drive-by typo fixes.

### Loom video walkthroughs (a 2026 US-remote standard — non-optional)
- Every project README: 3-min Loom embedded at the top. Show: problem → architecture → live demo → eval table → "where it fails."
- Record once, link everywhere (GitHub, blog, LinkedIn, X bio, Mercor profile, outbound emails).
- Practice ahead — first take is bad. Re-record until ≤3 min.

### Community (where founders and engineers actually hang out)
- **[Latent Space Discord](https://discord.gg/latent-space)** — Swyx's community. AI engineers, founders, hiring managers all present. Reply substantively 2×/week.
- **[AI Tinkerers](https://aitinkerers.org/)** — local + virtual chapters. Founders attend. Demo nights are recruiting events in disguise.
- **[Maven AI Evals Discord](https://maven.com/parlance-labs/evals)** — Hamel/Shreya's community.
- **[Hugging Face Discord](https://huggingface.co/join/discord)** — broader, but #agents and #applied channels are valuable.
- **Build Club India**, **AgentsNexus India / GenAI Bangalore** — secondary; useful for warm intros to India startups but not US founders.
- 1 lightning talk by Month 5 or 6 (5 min, recorded). Builds the on-camera muscle Mercor and US founders test in final rounds.

### Outbound funnel (Track 6 — your unfair advantage)
The detailed playbook is built out in Months 5–6 weekly files. Headline elements:
- **Sourcing:** TechCrunch funding → just-raised seed/Series A AI startups → find CTO/founding eng on LinkedIn/X → enrich with email via Hunter/Apollo (you already know these tools).
- **Cadence:** ~50 contacts/week in Months 5–6 = 200/month. Steady, not spammy.
- **Email structure:** Insight + Specific Offer. One observation from their product/blog/launch + one specific 2-week trial you'd build for them. Cold email research consistently shows 5–10 min/prospect with one sharp hook beats 30 min of generic personalization.
- **Tracking:** the same Clay/Smartlead/n8n stack you use at Precise Leads, applied to your own funnel. Build it as a meta-project in Month 5 — itself a portfolio piece (you can show it on calls).

## 10. Notes to self (re-read monthly)

- **You are not behind.** You're three weeks into the *wrong* plan. The work you did (50 traces, Saturday notes, tooling setup) carries forward. You're at Week 1 of the right plan now, not at Week -3.
- **The Aug 2026 graduation hits mid-Month 3.** Account for final exams + project submissions. If you have specific exam windows, tell me — I'll insert lighter weeks around them. Default assumption: ~2 lighter weeks in Month 3, recovered in Month 4 or Month 6.
- **8–10 hrs/week is the budget.** Stuffing 15 hrs of work into a 10-hr week is the most common failure mode for self-paced plans. Slipping two Sundays in a row is the canary — reset, don't pretend.
- **Your PresentAI and AsanaBot are not invisible.** Refresh both READMEs in Month 1 Week 1 with one-paragraph problem statements + screenshots + live links. They double the apparent portfolio in 30 minutes of writing.
- **US-remote is now the primary funnel.** India product startups are the safety. Your GTM-engineer skill (outbound, qualification, enrichment) is the biggest single asset most fresher candidates don't have — point it at US AI founders, not just at job boards. Mercor + HN + Wellfound + direct outbound is the four-channel funnel; portfolio is the same across all four.
- **One last thing.** You don't have to become a different person to do this. You already ship. The next 24 weeks are about packaging what you do + adding the eval / RAG / agent / MCP layer on top so hiring managers see what's there.

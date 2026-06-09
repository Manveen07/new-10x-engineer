# Start Here

**Bookmark this file. Open it every time you sit down to work.**

It tells you exactly where you are and what to do today. Nothing else needs to be in your head.

---

## Today is in: **Month 1 close-out** (2026-06-08 → 2026-06-21)

→ Open: **[month-1/FINISH-PLAN.md](./month-1/FINISH-PLAN.md)** — the single day-by-day plan for finishing Month 1. Its **Status block** tells you exactly what's done and what's next.

**Where you are (2026-06-09): ahead.** Done — fundamentals green, Eugene Yan 7 patterns, leadlens `DESIGN.md`, judge v1 (TPR=1.0/TNR=0.882). Remaining — `failure-taxonomy.md` → judge TNR ≥0.90 → **publish blog post 1** → Anthropic Academy prompt course → interview Cluster 1 self-test → Demo Day Loom → PROGRESS monthly review.

The per-week files [week-3.md](./month-1/week-3.md) / [week-4.md](./month-1/week-4.md) hold extra kata + code detail, but FINISH-PLAN.md wins on sequencing.

**Advance to Month 2 only when the Month 1 done-bar hits ≥7/9 — including blog post 1 published.** Then point this section at [month-2/README.md](./month-2/README.md) (Week 5). Don't skip the blog post to move faster — it's *the* Month 1 asset, the thing 90% of fresher applicants don't have.

---

## How the repo is laid out

Three layers, each shorter than the last.

### Layer 1 — Strategy (read once, re-skim monthly)
- [README.md](./README.md) — one-screen positioning.
- [MASTER_PLAN.md](./MASTER_PLAN.md) — full strategy: target funnel (US-remote primary), skill audit, anti-patterns, resources, public footprint plan.

### Layer 2 — Plan (read at the start of each month)
- [ROADMAP.md](./ROADMAP.md) — six-month week-by-week table.
- [PLAN-MONTHS-2-6.md](./PLAN-MONTHS-2-6.md) — detailed forward plan + the thought process behind every decision (anti-drift anchor; "where we came from").
- [PROJECTS.md](./PROJECTS.md) — three flagship project specs (leadlens, docsight, reposcout).
- [EXERCISES.md](./EXERCISES.md) — monthly checklist (tick boxes as you go).
- [month-1/README.md](./month-1/README.md) … [month-6/README.md](./month-6/README.md) — per-month overviews.
- [month-1/FINISH-PLAN.md](./month-1/FINISH-PLAN.md) — Month 1 day-by-day close-out (weekend-loaded, fundamentals drip).
- [REFERENCE.md](./REFERENCE.md) — technique cheat-sheet (eval / RAG / agent / LLMOps specifics + sources). Open while building.
- [interview_prep_qa.md](./interview_prep_qa.md) — interview Q&A bank for the 5 clusters (evals, RAG, agents, LLMOps, cost modeling).

### Layer 3 — Execution (open every working day)
- `month-N/week-N.md` — daily plan for the week you're in.
- [PROGRESS.md](./PROGRESS.md) — Sunday log. The single forcing function.
- [katas/](./katas/README.md) — daily no-AI Python reps; one line per rep in [LEARNINGS.md](./katas/LEARNINGS.md).
- [dsa/](./dsa/README.md) — LeetCode arc (2/week from Month 2, weeks 5–20 mapped).
- `notes/` — running learning notes: [fundamentals.md](./notes/fundamentals.md), [llm-patterns.md](./notes/llm-patterns.md), leadlens iteration logs, Saturday open-coding notes.
- `projects/business-classification-pipeline/` — leadlens (Months 1–2): [README](./projects/business-classification-pipeline/README.md) · [DESIGN.md](./projects/business-classification-pipeline/DESIGN.md). Already has your 50 traces.
- `projects/gtm-clay-rag/` → renames to `projects/docsight/` in Month 3.
- `projects/icp-research-agent/` → renames to `projects/reposcout/` in Month 5.

That is the whole repo. There is nothing else.

---

## The daily question: "what do I do right now?"

You should never have to ask this. The answer is always:

1. Open `START_HERE.md` (this file).
2. Click the link to the current week file.
3. Find today's row in the Daily Plan table.
4. Set a 30-min timer. Start.

If you've been "studying" for 30 minutes and haven't written code, opened your traces, or saved progress — stop. You're in passive mode. Reset.

---

## The daily 5-min warm-up (no AI)

Before the day's task, **open a blank `.py` file** and write one of the following without AI help. Five minutes, your fingers on the keyboard. Then start the day.

Rotate through these:
- A nested Pydantic model + parse a dict into it
- A 3-line `asyncio.gather` over 3 fake API calls
- A `@dataclass` with `__post_init__` validation
- A `pytest` fixture + one assertion
- A list comprehension turned into a generator expression
- Type-hint a function with `Callable[[str], Awaitable[int]]`
- A context manager via `@contextlib.contextmanager`

The point is reps, not novelty. Hand-coded muscle is what gets tested in live coding rounds.

---

## The weekly rhythm (job-shaped: light weekdays, heavy weekends)

You work at Precise Leads Mon–Fri, so the plan is weekend-loaded. Weekdays are maintenance only.

| Day | What | Time |
|---|---|---|
| Mon eve | 5 min: open week file, copy 2–3 goals to sticky note. Kata 1 (no AI). | 15 min |
| Tue eve | Kata 2 (no AI). | 15 min |
| Wed eve | Kata 3 (no AI). | 15 min |
| Thu eve | Kata 4 (no AI). | 15 min |
| Fri eve | Kata 5 (no AI) OR rest day if Fri's exhausting. | 15 min |
| **Sat** | **Big build block.** Project work, builds, deployments. | **3–4 hrs** |
| **Sun** | **Reading + writing block.** Reading, blog post drafting, refactor cleanup. End with 30-min PROGRESS update + plan next week. | **3–4 hrs** |

Total: ~8–10 hours/week. Weekday touches keep the muscle warm (5 katas = 75 min). Weekends are where the actual project moves forward.

**Two habits baked into the weekday katas:**
- **Commit each kata the night you write it** (to `katas/`). Daily green squares are a Mercor screen filter — the commit is part of the rep, not optional.
- **From Month 2:** swap 2 weekday katas/week for **2 LeetCode problems** (arrays/hash maps/strings/graphs), committed to `dsa/`. Target 60–80 by Month 6 so live-coding screens never catch you cold. Month 1 stays pure no-AI Python.

**If a weekday is exhausting after work, skip the kata that night — but cap skips at 1/week.** Two skipped katas in a row → catch up Saturday morning before the build block.

If you drop below 6 hrs total for two weeks, the Sunday log will tell you — read the "Behind if" section in [ROADMAP.md](./ROADMAP.md) and recover.

---

## Standing rules (re-read every Sunday for first 3 months)

1. **Eval before scale.** Every project gets a golden dataset before optimization.
2. **One framework or none.** Raw SDK + Pydantic + Instructor is the default; add LangGraph only at the node that genuinely needs it.
3. **Workflow before agent.** Default to deterministic code; agentic dynamism only where required.
4. **Type the code yourself before asking AI.** Daily 5-min warm-up, no AI. Then AI is a pair, not a crutch.
5. **Ship in public weekly.** A commit, a tweet, a README diff. Hidden work doesn't compound.
6. **Production thinking lives in the README.** "Where it fails," cost-per-call, latency p50/p95, eval table.

Anti-patterns to refuse: letting AI write everything, tutorial-finishing, framework collecting, fake claims, demo without evals, hype-posting. Full list in [MASTER_PLAN.md](./MASTER_PLAN.md) §7.

---

## The Stuck Box rule

When stuck >20 min:
1. Open `PROGRESS.md`, scroll to current week, add a line: "stuck on X — symptom is Y."
2. *Then* ask AI (Claude Code, Cursor, ChatGPT).
3. Never silently struggle 2 hours. Never silently let AI write 3 files. Both are failure modes.

---

## When something breaks

- **Stuck on tooling:** check [MASTER_PLAN.md](./MASTER_PLAN.md) §8 Tools — likely already covered.
- **Behind on the week:** read the "Behind if" markers in [ROADMAP.md](./ROADMAP.md). Recover the must-have item before starting next week.
- **Two Sundays missed in a row:** that's the canary. Reset on the next Sunday with a smaller, honest plan. Don't pretend.
- **Lost or overwhelmed:** close every file except this one. Open the current week file. Pick the easiest task. Set a timer. Start.

---

## What success looks like (end of Month 6 — Nov 8, 2026)

- Three deployed projects (leadlens, docsight, reposcout) with eval suites, READMEs to standard, $/call + latency, live URLs, Loom walkthroughs.
- One MCP server demoable from Claude Desktop.
- One merged OSS PR.
- 4–6 published blog posts on your own domain.
- GitHub: 4–6 months of daily-ish activity, pinned repos, profile README.
- X profile actively contributing, LinkedIn updated.
- Funnel: 100+ outbound + 25+ applications + 5+ first rounds + Mercor active + India safety apps in parallel.
- One lightning talk delivered or recorded.

If 7+ are checked by 2026-11-08, you are ready. Offers from there are a function of funnel volume.

---

**Now: open [month-1/week-1.md](./month-1/week-1.md) and do today's task.**

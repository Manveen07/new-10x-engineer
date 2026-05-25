# Progress Log

Update every Sunday. Honest hours. Specific.

This is your single forcing function (no Maven cohort, no boss). Skipping two Sundays in a row is the canary — see [MASTER_PLAN.md](./MASTER_PLAN.md) §10.

---

## Day 0 — Reset (2026-05-23 / 2026-05-24)

Tooling is already done from your previous three weeks (Modal hello-world, Instructor speedrun, Langfuse account, GitHub repo). Carry forward.

- [x] Modal hello-world deployed — done previously, file at [month-1/test files/hello.py](./month-1/test%20files/hello.py)
- [x] Pydantic + Instructor speedrun — done previously, [month-1/test files/instructor_test.py](./month-1/test%20files/instructor_test.py)
- [x] 50 classifier traces pulled — [projects/business-classification-pipeline/data/traces-week-1.jsonl](./projects/business-classification-pipeline/data/traces-week-1.jsonl)
- [x] Saturday open-coding notes (3 failure modes named) — [notes/week-1-saturday-notes.md](./notes/week-1-saturday-notes.md)
- [x] Langfuse keys saved to password manager (confirm)
- [x] Personal domain owned (if not yet — buy this weekend, Quarto/Astro setup needs it Week 1)
- [x] Tell the plan author your final-exam / project-submission windows (so Month 3 can be thinned)

### Anything that hurt more than expected (carry-over insights from old plan)
- *(Add notes here from your last three weeks if relevant — e.g., where Modal deploy stalled, what was unclear in Hamel's post.)*

---

## Week 1 — Week of 2026-05-25 (Month 1, Week 1)

### Focus this week
1. Weekend block pulled forward to Sun May 24 — stack, portfolio, READMEs, Hamel re-read.
2. Daily no-AI Python katas Mon–Fri evenings.

### Hours spent (Sunday weekend block)
- Project work: 3.5 hrs
- Reading: 1 hr (Three Gulfs)
- Writing / community: 30 min (tweet + LinkedIn)
- No-AI katas: 0/5 (Mon–Fri ahead)
- Outbound: 0
- Total Sunday: 5 hrs / weekend budget 7 hrs

### Shipped this week (Sunday)
- uv + ruff + pytest + pre-commit installed in `katas/`
- `CLAUDE.md` at repo root (project rules for Claude Code)
- manveen.me live on Vercel (DNS swapped from GitHub Pages → `76.76.21.21`)
- AsanaBot README refreshed (9 asanas, ViT-Base, 3 named failure modes)
- PresentAI README refreshed
- Cursor configured (Tab off, User Rules)
- Claude Code CLI verified (2.1.47)
- `notes/week-1-saturday-notes-v2.md` — Three Gulfs internalized, 3 leadlens design decisions locked
- First public push: tweet + LinkedIn

### What I learned
All 3 named failure modes (`false_executive_search_signal`, `mixed_boundary_ambiguity`, `schema_drift`) map to the Specification gulf. No Generalization issues yet → Month 2 = prompt iteration + few-shot + schema additions, not fine-tuning or model swap. Also adding `segment_strength: float | None` to schema and reasoning-before-confidence prompt pattern.

### What slipped
- 4 deferred evals-faq Qs not re-read (moved to next Saturday morning, 30 min slot before Week 2 build block).
- 5 weekday katas still ahead (Mon–Fri).

### Next week's focus (Week 2)
1. Open-code all 50 traces with Three Gulfs framework (Sat–Sun build block).
2. Build Streamlit annotation viewer.
3. Daily no-AI katas Mon–Fri.

### Stuck Box
- Hamel's "Field Guide to Rapidly Improving AI Products" URL returned 404. Used David Okpare primer + Aayush Garg lifecycle post as substitutes. Lesson: don't grind on a 404, check 2 secondary sources by framework name.

### Confidence check (1–5)
- Python fluency (no AI): 3 (read fine, write is the gap)
- Evals knowledge: 3 (Three Gulfs internalized, no judges built yet)
- RAG knowledge: 2 (CV background, no RAG production experience)
- Agents knowledge: 3 (MCP/LangGraph not used yet)
- Production / deploy: 4 (Modal + Vercel + Docker exposure)
- Public footprint: 2 (1 tweet, no blog posts, no Loom)
- Outbound funnel readiness: 3 (Precise Leads mechanics, no leadlens-shaped artifact yet)

---

## Weekly template (copy this for each new week)

```markdown
## Week N — Week of YYYY-MM-DD (Month X, Week Y)

### Focus this week
1.
2.
3.

### Hours spent
- Project work:
- Reading / course:
- Writing / community:
- No-AI katas (days completed out of 5):
- Outbound (messages sent, replies received):
- Total: __ / 10 target

### Shipped this week
-

### What I learned
One specific paragraph.

### What slipped
-

### Next week's focus
1.
2.
3.

### Stuck Box (log items where you were stuck >20 min)
-

### Confidence check (1–5)
- Python fluency (no AI):
- Evals knowledge:
- RAG knowledge:
- Agents knowledge:
- Production / deploy:
- Public footprint:
- Outbound funnel readiness:
```

---

## Monthly review template

### Month N — YYYY-MM

- Shipped:
- Public post/update:
- Community / network action:
- Outbound numbers (cumulative messages, replies, calls):
- Biggest failure mode found:
- Biggest cut from the plan (and was it honest?):
- Next month adjustment:
- Demo Day Loom URL:

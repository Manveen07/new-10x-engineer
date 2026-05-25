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

### Mon May 25 — holiday, Week 2 work pulled forward
- Project work: ~4.5 hrs
- Kata 1 done (nested Pydantic + parse_company + 3 pytest tests, all green, no AI for model + tests)
- Annotation viewer shipped (`projects/business-classification-pipeline/annotator.py`)
- 50 traces annotated (22 hand-coded via calibration pairing + 22 stratified-sampled auto-tag via `filter_traces.py` + 6 boundary cases hand-coded)
- Bulk-save script (`bulk_save_notes.py`) merged hand annotations into `data/notes.jsonl` (50/50 entries)
- v2 taxonomy locked in `notes/week-1-saturday-notes-v2.md`: F-003 (hardcoded confidence) promoted to highest priority, F-001 demoted (model handles), F-004 (thin-evidence) added new, F-002 kept medium
- Commit pushed: `0baea8b` — 11 files, 1556 insertions

#### Mon learnings
- Filter-then-hand-code is correct open-coding methodology once pattern stability hits (~20 traces). Don't grind through pass-only cases.
- Pre-commit hook caught + auto-formatted 4 files on first commit attempt → blocked. Re-stage with `git add -u`, re-commit succeeded. Pattern locked.
- Self-vocab gap surfaced ("retainer search" = retained exec search, not "casual/on-demand"). Comprehension gulf on labeler side. Judge prompt needs this term defined.
- Filter false-positive rate ~33% on boundary-marker heuristic (2 of 6 hits were connective grammar). Tune marker list before reuse.

#### Mon stuck box
- (none — clean session)

### Remaining Week 1 work
- Katas 2–5 (Tue–Fri evenings, 15 min each, no AI)
- 4 deferred Hamel evals-faq Qs (Sat May 30 morning, 30 min)
- Next Sat May 30 weekend block now has slack since trace open-coding done. Reading + writing focus, or pull Week 3 axial-coding forward.

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

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

## Week 2 — Week of 2026-06-01 (Month 1, Week 2)

> **Stub — git-reconciled, 2026-06-09.** "Shipped" is pulled from commit history (facts). Fill in hours, learnings, slipped, confidence honestly before this counts as a real log.

### Focus this week
1. _(fill in — what you set out to do)_
2.
3.

### Hours spent
- Project work: _(fill in)_
- Reading / course: _(fill in)_
- Writing / community: _(fill in)_
- No-AI katas (days completed out of 5): _(katas 02–05 committed 2026-06-06 — confirm count)_
- Outbound (messages sent, replies received): _(fill in)_
- Total: __ / 10 target

### Shipped this week (from git — verify)
- Katas 02–05 (no-AI) — commit `week-1 wip` 2026-06-06
- leadlens v0.1 schema + runner + 10-JD corpus — 2026-06-06
- leadlens v0.1 **iteration 1**: `stack_unspecified` field, label hygiene, 75% category match — 2026-06-06
- leadlens v0.1 **iteration 2**: 20-JD corpus + cost/latency instrumentation; F-006 surfaced — 2026-06-06
- leadlens v0.1 **judge v1**: critique-shadowing scam detector, **TPR=1.0 / TNR=0.882** — 2026-06-07
- `month-1/FINISH-PLAN.md` (day-by-day close-out) — 2026-06-07
- `PLAN-MONTHS-2-6.md` (forward plan + thought process) — 2026-06-07
- Fundamentals: tokens / embeddings / attention to green + tiktoken demo; recall-test results — 2026-06-07

### What I learned
_(fill in — one specific paragraph)_

### What slipped
- _(fill in)_

### Next week's focus (Week 3)
1. Axial taxonomy → `failure-taxonomy.md` (4–7 named categories)
2. _(see week-3.md — note judge v1 already shipped, so adjust)_
3.

### Stuck Box
- _(fill in)_

### Confidence check (1–5)
- Python fluency (no AI): _(fill in)_
- Evals knowledge:
- RAG knowledge:
- Agents knowledge:
- Production / deploy:
- Public footprint:
- Outbound funnel readiness:

---

## Week 3 — Week of 2026-06-08 (Month 1, Week 3) — IN PROGRESS

> **Stub — git-reconciled, 2026-06-09.** Week still running. Update at Sunday review (2026-06-14).

### Focus this week
1. Axial taxonomy committed as `failure-taxonomy.md` (must-do per week-3.md)
2. _(judge v1 already built 2026-06-07 — ahead of plan; decide what replaces the Sunday judge-build block)_
3.

### Hours spent
- Project work: _(fill in)_
- Reading / course: _(fill in)_
- Writing / community: _(fill in)_
- No-AI katas (days completed out of 5): _(fill in)_
- Outbound (messages sent, replies received): _(fill in)_
- Total: __ / 10 target

### Shipped this week (from git — verify, week ongoing)
- Fundamentals: all 5 retention slips closed to green (two-softmaxes, 0x80→hybrid/TF-IDF/BM25) — 2026-06-08
- Patterns: Eugene Yan 7 LLM patterns learned + mapped to leadlens / docsight / reposcout — 2026-06-08
- leadlens: `DESIGN.md` eval-first design doc consolidating v0.1 — 2026-06-08

### What I learned
_(fill in at Sunday review)_

### What slipped
- _(fill in)_

### Next week's focus (Week 4)
1.
2.
3.

### Stuck Box
- _(fill in)_

### Confidence check (1–5)
- Python fluency (no AI): _(fill in)_
- Evals knowledge:
- RAG knowledge:
- Agents knowledge:
- Production / deploy:
- Public footprint:
- Outbound funnel readiness:

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

## Monthly review — Month 1 (2026-05 → 2026-06)

**Shipped:**
- Python rebuild: 5 no-AI katas (Pydantic, async/httpx, context managers, pytest, typing).
- Fundamentals to green: tokens/BPE, embeddings/cosine, full attention pipeline (Q·K → √d_k → mask → softmax → weighted-sum-V), two-softmaxes, transformer chain. Closed the interview blind spot.
- Eugene Yan 7 LLM patterns, mapped to own projects.
- leadlens classifier (Pydantic + Instructor + Gemini): schema, runner, cost/latency instrumentation.
- Scaled golden set 10 → 20 → **72 real JDs** (merge + dedupe; added `ml_training` 5th category).
- Scam judge v1 (critique-shadowing) → v2 (few-shot + tightened rule).
- **Caught + fixed eval label-leak (F-007):** descriptions leaked the answer; cleaned → honest TPR 0.818 / TNR 1.0.
- leadlens DESIGN.md + failure-taxonomy.md committed.

**Public post/update:** Blog post 1 live — manveen.me/writing/schema-as-eval-spec (v2: schema-as-eval-spec + the eval-leak discovery).

**Community / network action:** none yet (deferred — amplify post on LinkedIn/X in Month 2).

**Outbound numbers:** 0 (funnel starts Month 5-6).

**Biggest failure mode found:** F-007 — the eval was grading its own crib notes. Found by reading the data, not the dashboard. The lower honest number (0.818) beats the fake 1.0.

**Biggest cut from the plan (honest?):** Pivoted leadlens staffing → AI-JD classifier (Manveen's call); skipped Anthropic Academy cert + Demo Day Loom so far. Honest — depth on evals + the published post mattered more than ticking those.

**Confidence re-rate (Week 1 → end Month 1):**
- Python fluency (no AI): 3 → 3 (real code, still building confidence)
- Evals knowledge: 3 → 4 (2 judges built + calibrated + caught a leak)
- Fundamentals (new axis): → 3 (transformer end-to-end; intricacies still fuzzy)
- RAG knowledge: 2 → 2 (Month 3 work)
- Agents knowledge: 3 → 3 (Month 5 work)
- Production / deploy: 4 → 4 (not yet deployed leadlens — Month 2)
- Public footprint: 2 → 4 (post published)
- Outbound readiness: 3 → 3

**Next month adjustment:** Month 2 = deploy leadlens (FastAPI + Modal + Langfuse) → the live-URL milestone. Already ahead (golden-set scaling was a Month 2 item, done early). Don't rush — deliberate start.

**Demo Day Loom URL:** _(not recorded yet — optional)_

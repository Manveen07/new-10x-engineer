# Project — 6-month AI Engineer Roadmap

## What this repo is
Personal 24-week curriculum + 3 projects (leadlens, docsight, reposcout) + Sunday log. Owner: Manveen Singh. Plan in `MASTER_PLAN.md`. Daily landing: `START_HERE.md`.

## How to help me here

### Code-writing rules
- I am rebuilding Python fluency. AI wrote too much of my code before.
- If I say "kata" or "no AI" — DO NOT write code. Answer questions only.
- Otherwise: explain approach in 3 sentences, propose one diff, no alternative implementations.
- Python 3.11+, type hints everywhere, Pydantic v2, `uv` not pip+venv, `ruff` for lint/format, `pytest` for tests.
- No try/except around impossible failures. No defensive coding for hypothetical errors.
- Prefer stdlib. Don't add a dep for a 5-line function.

### Project structure
- `projects/business-classification-pipeline/` = leadlens (Months 1–2). Existing artifacts: `data/traces-week-1.jsonl` (50 staffing-firm classifier traces), open-coding notes in `notes/`.
- `projects/gtm-clay-rag/` → renames to `docsight/` Month 3.
- `projects/icp-research-agent/` → renames to `reposcout/` Month 5.
- `katas/` = daily no-AI Python kata folder. Hands off unless I ask explicitly.

### Comms style
- I prefer terse. Drop pleasantries.
- Surface trade-offs in one sentence. Don't hedge.
- Use file:line refs when pointing at code.

### When asked "what next" or "what today"
- Default to `START_HERE.md` → current week file → today's row.
- Don't pull future-week work forward without asking.
- Don't propose new features beyond the week's scope.

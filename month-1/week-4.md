# Week 4 — Calibrated Judge + leadlens DESIGN.md + Blog Post 1

> ⚠ **Superseded for sequencing by [FINISH-PLAN.md](./FINISH-PLAN.md).** `DESIGN.md` is already committed (Jun 8) — ignore the Wed/Thu "write DESIGN.md" cells here. The live remaining work is judge → TNR ≥0.90 and **publish blog post 1**; FINISH-PLAN's Status block sequences it.

**Window:** Mon 2026-06-15 → Sun 2026-06-21
**Time budget:** 8–10 hours
**Position:** Month 1, Week 4 of 24

## Why this week matters

Three artifacts shipped this week. Each is a portfolio-grade asset:

1. **Calibrated LLM-as-judge at >90% agreement** — the artifact that distinguishes you from 90% of fresher applicants.
2. **leadlens `DESIGN.md`** — proves you design before you build, which is what hiring managers screen for in system-design interviews.
3. **Blog post 1 published** — your first piece of public work in 2026 voice. Compounds for the next 24 weeks.

**The single must-do:** blog post 1 published by Sunday night. Even if everything else is rough.

## At-a-glance daily plan (weekday-light, weekend-heavy)

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-06-15 | Plan review + **kata 14** (pytest parametrize for evals, no AI) | 15 min |
| Tue eve | 2026-06-16 | **Kata 15** (argparse CLI, no AI) | 15 min |
| Wed eve | 2026-06-17 | **Kata 16** (one judge prompt iteration, no AI for code) | 15 min |
| Thu eve | 2026-06-18 | **Kata 17** (small refactor, no AI) | 15 min |
| Fri eve | 2026-06-19 | Skim one post OR rest | 15 min |
| **Sat** | 2026-06-20 | **Big build block**: judge v3 to >90% agreement + second judge for `mixed_boundary_ambiguity` + draft blog post 1 in Quarto | **3.5 hrs** |
| **Sun** | 2026-06-21 | **Big block**: leadlens `DESIGN.md` (8 sections + architecture diagram) + edit + publish blog post 1 + LinkedIn + X + Demo Day Loom (3 min) + Month 1 monthly review | **4 hrs** |

Total: ~10 hours.

**Note:** body sections below were drafted with the old cadence and will be rewritten the weekend before Week 4 starts. The daily-plan table above is the source of truth.

---

## Monday — Judge v3 to >90% + kata 13 (90 min)

### Iterate (60 min)

Read every Saturday-Week-3 disagreement note. Patterns? Re-write `judge/judge_v1.md` → `judge/judge_v2.md`. Add:

- **2 worked examples** (one PASS, one FAIL) — Hamel's posts cite this as the single biggest agreement booster.
- **A "borderline" instruction** — what to do when evidence is partial: lean PASS, explain in critique.
- **Explicit definition reminder** at the *end* of the prompt as well as the start (anchor effect helps).

Run on all 50. Target: >90% agreement on `false_executive_search_signal` failure mode.

If still <90% after this iteration: read the remaining disagreements, decide if your *labels* are inconsistent. Re-label 1–3 traces if so. Then re-run.

### Kata 13 — `pytest` parametrize + fixture for LLM evals (30 min, NO AI)

In `katas/kata_13_eval_test.py`, write a pytest file that:

```python
import pytest
from pathlib import Path
import json

@pytest.fixture
def golden_examples() -> list[dict]:
    """Load 5 hand-picked (input, expected_judge_label) pairs."""
    return [
        {"trace": {...}, "expected": "FAIL"},
        ...
    ]

@pytest.mark.parametrize("example", [...])  # use fixture by indirect param
def test_judge_v2_on_golden(example, golden_examples):
    # call judge, assert label == expected
    ...
```

The point: setting up the muscle for CI-grade eval tests in Month 2.

---

## Tuesday — Second judge + kata 14 (90 min)

Pick `mixed_boundary_ambiguity` or `schema_drift` (whichever feels easier). Write `judge/judge_v0_mixed.md` then `judge_v1_mixed.md`. Same critique-shadowing pattern.

Run on 20 traces. Iterate once. Target: >80% agreement on the second judge (harder failure mode; full calibration is Month 2 work).

### Kata 14 — `argparse` for a CLI eval runner (30 min, NO AI)

In `katas/kata_14_cli.py`, write a CLI:

```bash
uv run python kata_14_cli.py --judge judge_v2 --traces data/traces-week-1.jsonl --limit 20
```

It loads, runs, prints a summary. Use `argparse`. No `click`, no `typer` — exercise stdlib.

---

## Wednesday — leadlens DESIGN.md sections 1–4 (90 min)

Create `projects/business-classification-pipeline/DESIGN.md`. Sections 1–4 today.

```markdown
# leadlens — Design Doc v1

Codename for the staffing-firm classifier project. Months 1–2 build; production-style by end of Month 2.

## 1. Problem
Given a company name + domain, classify the firm's segment (executive_search / general_staffing / mixed) with structured signals, confidence, and citations. Output must be reliable enough that a downstream outbound system uses it directly without human review for ≥85% of cases.

## 2. Input contract
- `name: str` (required)
- `domain: str | None`
- `location: str | None` (city, state, country)
- `prior_data: dict | None` (any known signals from upstream sources)

## 3. Output schema (Pydantic)
[paste the actual Pydantic model]

class Signal(BaseModel):
    name: Literal["executive_keyword", "leadership_focus", "junior_listings", ...]
    evidence: str = Field(min_length=20)
    confidence: float = Field(ge=0.0, le=1.0)
    source_url: str | None

class Classification(BaseModel):
    name: str
    domain: str | None
    segment: Literal["executive_search", "general_staffing", "mixed"]
    segment_confidence: float = Field(ge=0.0, le=1.0)
    segment_strength: float | None  # for "mixed" — 0..1, where 1 = strongly executive
    signals: list[Signal]
    citations: list[HttpUrl]

## 4. Retrieval / evidence path
1. Domain → fetch homepage + /about + /services pages (cap 5 pages)
2. Web search via Tavily — "{name} staffing services" + "{name} executive search"
3. Optional: Google Maps API for business category + reviews (later, if signal exists)

Fallback chain: if homepage fetch fails (timeout, 403), fall back to Tavily search only.
```

---

## Thursday — DESIGN.md sections 5–8 + diagram (90 min)

### Sections 5–8

```markdown
## 5. Golden dataset plan
- Source: union of (a) your existing 50 trace inputs, (b) 50 net-new sourced via Crunchbase staffing-firm exports, (c) deliberate edge cases (boutique firms, regional players, generalist + executive divisions).
- 100 examples total. Stratified: 30 executive_search, 30 general_staffing, 30 mixed, 10 edge cases (closed, ambiguous, multi-brand).
- Hand-label every example. Time budget: 4 hrs (~2.5 min/example).
- Commit: `data/golden-100.jsonl` with `name, domain, expected_segment, expected_strength, hard_or_easy, notes`.

## 6. Eval dimensions + judges
For each example: 4 binary judge checks.
- Judge A — segment correctness (PASS if classifier's segment matches expected)
- Judge B — false_executive_search_signal (FAIL if applies)
- Judge C — mixed_boundary_ambiguity (FAIL if applies and expected has clear lean)
- Judge D — evidence support quality (PASS if every Signal's evidence string ≥ 50 chars + actually supports the signal claim)

All four calibrated to >90% agreement with hand labels. Critique shadowing pattern.

## 7. Deployment + observability
- Modal serverless FastAPI endpoint
- Langfuse traces per request (input, output, judge results, latency, cost)
- Cost target: <$0.02 per classification (Sonnet primary, Haiku for judge if affordable)
- p50 target: <8 sec end-to-end (web fetch + LLM inference); p95: <20 sec

## 8. Stack with rationale
- Anthropic Claude Sonnet (primary) — better at structured reasoning over noisy evidence
- OpenAI GPT-4.1 (judge) — cross-model judge is the canonical pattern; reduces own-model bias
- Instructor for structured output (battle-tested with Pydantic, cleaner than raw `response_format`)
- Tavily for web search (cleaner than scraping; ~$0.005/query)
- Modal for deploy ($30 free credits, scale-to-zero)
- pgvector + Postgres (Modal volume) for caching domain → fetched content
- Langfuse cloud free tier (50K obs/mo enough for Month 2)
```

### Architecture diagram (30 min)

Open [excalidraw.com](https://excalidraw.com). Draw: input → enrichment chain (homepage → about → search) → LLM extraction (Instructor + Pydantic) → output → judge fanout → Langfuse trace → response.

Export PNG, save to `projects/business-classification-pipeline/docs/architecture.png`, embed in DESIGN.md.

---

## Friday — Blog post 1 draft (2 hrs)

**Title:** "Open-coding 50 LLM traces from a real classifier — what I found and built"

**Audience:** US AI founders and engineers (X / Hacker News). Voice: specific, no hype, eval table screenshots, one named failure mode with example.

**Outline (paste into `site/posts/open-coding-50-traces.qmd`):**

```markdown
---
title: "Open-coding 50 LLM traces from a real classifier — what I found and built"
date: 2026-06-21
description: "Open coding + axial coding + a calibrated LLM-as-judge on a staffing-firm classifier, in 4 weeks of part-time work."
---

## The setup
I had 50 traces from a staffing-firm classifier I built for [Caprae / Precise Leads]. I knew it was wrong sometimes. I didn't know *how* it was wrong, systematically. So I opened all 50 by hand.

## Three Gulfs in practice
[1–2 paragraphs on the framework + how I assigned each trace]

## What open-coding surfaced
Three named failure modes:
- `false_executive_search_signal` — model picks up marketing keyword, misses that the firm doesn't actually do that work.
- `mixed_boundary_ambiguity` — firm leans 80/20 but model collapses to "mixed."
- `schema_drift` — confidence values hardcoded at 0.95 across 50 traces. The model isn't actually reasoning about confidence — it's defaulting.

Trace 3 example: [paste a redacted JSON snippet]

## Building the judge
[The critique-shadowing pattern; one prompt v1 → v2 → v3 with the agreement numbers at each step]

## Numbers
Judge agreement with my hand labels:
- v1: 68%
- v2: 81%
- v3: 92%

## What's next
Building this into a deployed system (leadlens) over the next month. Pydantic + Instructor + Modal + Langfuse. Open eval dataset on the repo.

## Repo
[github link]
```

Aim for 1200–1800 words. Don't over-edit — Saturday is for edit + publish.

---

## Saturday — Edit, publish, announce, Loom (2 hrs)

### Edit (45 min)

- Cut 20% of the words. First drafts are always too long.
- Add the eval table as a screenshot (not text — visual signals "this person actually ran experiments").
- Add the architecture diagram if it fits.
- One CTA at the bottom: "I'm building leadlens publicly. Follow on X / GitHub for the next post."

### Publish (15 min)

```powershell
cd site
quarto publish gh-pages
```

Verify the live URL works in incognito.

### Cross-post (30 min)

- **LinkedIn:** post the article with a 2-paragraph teaser + the eval table screenshot.
- **X:** thread of 5–7 tweets. Lead with the most surprising finding ("hardcoded 0.95 confidence across 50 traces was the most embarrassing thing I caught in my own code this year"). Link to canonical post.
- **r/MachineLearning** weekly self-promo thread (Saturdays) — short summary + link.
- **Hacker News:** consider — only if you have time to sit with it the first hour. Don't post and run.

### 60-second Loom (30 min)

Record yourself walking through the blog post on screen. Why you did it, the surprising finding, the next step. Embed at the top of the blog post and post on X with the Loom link.

---

## Sunday — Monthly review + Demo Day Loom + Month 2 plan (60 min)

### Demo Day Loom (3 min, 20 min total)

Record a clean 3-min Loom: "Month 1 demo day. Here's what I built." Walk through:
- Portfolio site (15s)
- AsanaBot + PresentAI READMEs (30s)
- The annotator running (30s)
- Judge v3 output with 92% agreement (60s)
- DESIGN.md (30s)
- Blog post live (15s)

Re-record once. Post on LinkedIn + X with "month 1 of 6 — done."

### Update files

- [PROGRESS.md](../PROGRESS.md) Week 4 + Monthly Review for Month 1.
- [START_HERE.md](../START_HERE.md) — change pointer to Month 2 Week 5.
- Open [../month-2/README.md](../month-2/README.md), copy the Month 2 monthly checklist into a sticky note.

### Confidence check

Re-rate yourself on the seven dimensions in `PROGRESS.md`. Compare to Week 1's ratings. You should see movement on: Python fluency, Evals knowledge, Public footprint.

---

## Behind if

- Judge v3 below 88% agreement.
- DESIGN.md missing any of the 8 sections.
- Blog post not published.
- No Loom.
- PROGRESS Month 1 review not filled.

These are recoverable in Month 2 Week 5 if needed, but each one delays the Month 2 build.

## Going faster?

- Start hand-labeling the 100-example golden dataset (Month 2 Week 6 work).
- Sketch the Modal endpoint shape for leadlens — `modal.fastapi_endpoint` + Pydantic body.
- Read DLAI *Improving Accuracy of LLM Applications* (Month 2 Week 5 reading).

## Next month
→ [../month-2/README.md](../month-2/README.md) — ship leadlens (deploy + observe + 100-JD golden set). Week 5 day-by-day: [../month-2/week-5.md](../month-2/week-5.md). Gate: advance only at Month-1 done-bar ≥7/9 incl. blog post 1 (see [FINISH-PLAN.md](./FINISH-PLAN.md)).

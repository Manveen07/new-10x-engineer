# Week 4 — Calibrated LLM-as-Judge and Project 1 Design Doc

**Window:** Mon 2026-05-25 → Sun 2026-05-31
**Time budget:** 8 hours
**Position in plan:** Month 1, Week 4 of 24

## Why this week matters

You have 50 traces labeled with a taxonomy. This week you build an LLM that scores new classifier outputs and iterate its prompt until it agrees with your hand labels >90% of the time. That's the calibration step that turns "vibes-based eval" into something hiring managers respect.

You also write the Project 1 design doc — the spec you'll build against in Month 2. Don't skip it. Designing on paper before coding catches half the failure modes for free.

By Sunday you publish your first blog post. **This is the deliverable that converts a private learning month into a public artifact.** Don't move to Month 2 without it.

## Daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon | 2026-05-26 | First-pass judge prompt: takes a trace, returns one of your taxonomy categories, no critiques yet | 90 min |
| Tue | 2026-05-27 | Run the judge over all 50 traces; compute agreement % vs your hand labels; expect <70% on first try | 60 min |
| Wed | 2026-05-28 | Add critique shadowing: include 2–3 example critiques per category in the prompt; re-run; target >90% agreement | 90 min |
| Thu | 2026-05-29 | Project 1 design doc draft in `projects/business-classification-pipeline/docs/design.md` (template below) | 90 min |
| Fri | 2026-05-30 | Draft blog post 1 in your portfolio site repo: "Open coding 50 LLM traces from a real classification pipeline" | 90 min |
| Sat | 2026-05-31 | Polish post; publish; cross-post to LinkedIn (one paragraph + link); update Month 1 self-review in `PROGRESS.md` | 90 min |
| Sun | 2026-06-01 | Monthly review in `PROGRESS.md`; plan Month 2 Week 5 | 30 min |

Total: ~8 hours.

## Judge prompt structure

Critique-shadowing pattern from Hamel's `llm-judge` post. Skeleton:

```
You are evaluating a classification produced by another LLM.

The taxonomy is:
- ok: output is correct or correctly hedged
- hallucinated_address: model invented a location not in source evidence
- stale_evidence: model used pre-2024 data as if current
- ... (your full taxonomy here)

Examples (critique shadowing):
TRACE: {"output": {"status": "operating", "evidence": ["123 Fake St"]}}
ANALYSIS: The address "123 Fake St" does not appear in any retrieved evidence.
LABEL: hallucinated_address

TRACE: {"output": {"status": "operating", "confidence": 0.4, "evidence": ["site live, last updated 2019"]}}
ANALYSIS: Output is hedged with low confidence; evidence is older but model
flagged uncertainty correctly.
LABEL: ok

Now evaluate this trace. Return JSON: {"analysis": "...", "label": "..."}.
TRACE: {trace_json}
```

## Calibration loop

```
1. Run judge over 50 traces → store predicted_label per trace.
2. Compare to hand_label → compute agreement rate.
3. Find disagreements → read 5–10 → ask "is the human wrong, or the prompt?"
4. If human wrong: re-label hand. If prompt wrong: edit prompt, add a critique example.
5. Re-run. Target >90% agreement after ≤3 iterations.
```

Log each iteration in `projects/business-classification-pipeline/docs/judge-iterations.md`:
- iteration N: agreement %, what changed, what disagreement pattern was caught.

## Project 1 design doc — template

Create at `projects/business-classification-pipeline/docs/design.md`:

```markdown
# Project 1 Design Doc — Business Classification Pipeline

## Problem
Given a company name and domain, output a structured classification with
operating status, ICP fit, sub-segment, signals, confidence, citations.

## Input contract
- company_name: str (required)
- domain: str | None
- location: str | None

## Output schema (Pydantic)
- status: Literal["operating", "closed", "uncertain"]
- icp_fit: Literal["yes", "no", "maybe"]
- sub_segment: str | None
- signals: list[Signal]   # name, evidence_snippet, source_url
- confidence: float        # 0..1
- citations: list[str]     # source URLs

## Evidence pipeline
- web search (primary)
- maps lookup (secondary)
- prior-data DB (if available)
- fallback: search API → scraping → LLM extraction

## Golden dataset plan
- 100 companies
- mix: 40 clean pass, 30 clean fail, 30 ambiguous edge cases
- collected from past Clay/winery/HVAC runs + ~20 fresh hand-picked

## Eval dimensions
- status correctness (binary)
- icp_fit correctness (binary)
- evidence support (binary: every claim has a citation)
- confidence calibration (continuous: are 0.9 outputs right 90% of the time?)

## Judge plan
- one binary judge per dimension
- critique-shadowing prompts
- target >90% agreement against hand labels
- iteration log in judge-iterations.md

## Failure taxonomy
Link: ../docs/failure-taxonomy.md

## Deployment target
Modal, public URL, FastAPI endpoint.

## Observability
Langfuse traces on every: search call, LLM call, judge call, final decision.

## Not in scope
- multi-tenant auth
- rate limiting beyond Modal defaults
- custom UI (CLI + JSON only)
```

## Blog post 1 — outline

Title: **Open coding 50 LLM traces from a real classification pipeline**

Three sections:
1. **What I did and why.** One paragraph: I have a winery/HVAC classifier in production. Most candidates skip eval. I spent a month looking at 50 of its outputs.
2. **The taxonomy I found.** List your 4–7 categories with one example each. This is the meat.
3. **What I'm building next.** One paragraph linking to the Project 1 design doc.

500–800 words. No fluff. Write it like you're explaining to a senior engineer over coffee.

## Resources used this week

- [hamel.dev/blog/posts/llm-judge](https://hamel.dev/blog/posts/llm-judge/) — re-reference during Mon/Wed work.
- [hamel.dev/blog/posts/field-guide](https://hamel.dev/blog/posts/field-guide-to-rapidly-improving-ai-products/) — optional, deeper dive on iteration.

## Deliverable checklist

- [ ] Judge prompt v3+ achieves >90% agreement with hand labels on 50 traces.
- [ ] `projects/business-classification-pipeline/docs/judge-iterations.md` shows ≥3 iterations with notes.
- [ ] `projects/business-classification-pipeline/docs/design.md` exists and matches the template above.
- [ ] Blog post 1 published at your domain.
- [ ] LinkedIn cross-post made.
- [ ] `PROGRESS.md`: Week 4 block + Month 1 monthly review filled in.

## Behind if

- Judge agreement is below 85%.
- Design doc is missing or skips the evals section.
- Blog post 1 is not published.

## What unlocks next month

Month 2 Week 5 (start of Project 1 build) needs the design doc as its spec. The judge prototype from this week becomes the seed for Project 1's eval harness. Without those two artifacts, Month 2 starts on the wrong foot.

## Next file

→ [../month-2/README.md](../month-2/README.md) — Project 1 ship month overview. The Week 5 daily file (`month-2/week-5.md`) will be written during your Sunday review on 2026-06-01.

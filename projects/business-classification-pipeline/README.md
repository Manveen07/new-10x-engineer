# leadlens

> **Canonical spec: [DESIGN.md](./DESIGN.md).** This README is the pre-deploy placeholder; the README-to-standard (architecture diagram, eval table, "where it fails", $/call, p50/p95, Loom) lands in Month 2 Week 8 when leadlens deploys.

Folder name stays `business-classification-pipeline`; the project is called **leadlens** in code, posts, and docs.

## What it is

An LLM classifier that reads an **AI-engineering job description** and returns a structured, evidence-grounded fit assessment — built eval-first, dogfooded on Manveen's own US-remote job funnel (Month 6).

*(Pivoted from a staffing-firm classifier — the original 50 staffing traces were ~50/50 pass with no hard failures. JD classification has real failures and is a tool he'll actually use. The schema-as-eval-spec method ported cleanly. See [PLAN-MONTHS-2-6.md §5](../../PLAN-MONTHS-2-6.md).)*

## Output schema (Pydantic — `leadlens_v01.py`)

`seniority` · `ai_authenticity` (real_ai_role / ai_adjacent / ai_washed / non_ai) · `core_stack` + `stack_unspecified` · `remote_status` · `location_signal` · `comp_signal` · `red_flags` · `confidence_reasoning` (min_length=100) · `fit_for_manveen`. Each field is measurable and/or forces a dimension a failure mode hides in.

## Stack

- Python 3.12+ · `uv` · `ruff` · `pytest`
- Pydantic + Instructor (structured output; schema = eval spec)
- **Gemini 2.5 Flash** (primary) — cheap, fast; ~$0.00085/JD
- Langfuse tracing (Month 2), Modal deploy (Month 2)

## Eval standard

- 100-JD hand-labeled golden set (stratified across categories + edge cases).
- Classifier metric: category accuracy vs `expected_category` (CI gate ≥75%).
- Scam judge (F-006), critique-shadowing, calibrated on **TPR/TNR** (not raw accuracy — class imbalance). Target TPR ≥0.75, TNR ≥0.90. (v0.1: TPR 1.0 / TNR 0.882.)
- Failure taxonomy: F-003 hardcoded confidence, F-004 thin-stack extraction, F-006 scam under-call.
- DeepEval (pytest-native) recommended for the judge-in-CI gate.

## Status

v0.1 — classifier + scam judge running locally on a 20-JD golden set. Not yet deployed. See [DESIGN.md §9](./DESIGN.md) for what's next.

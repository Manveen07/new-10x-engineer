# leadlens — Design Doc

> An LLM classifier that reads an AI-engineering job posting and returns a structured, evidence-grounded assessment of fit for a junior India-based, US-remote-targeting candidate (Manveen). Built eval-first: every recurring failure mode is killed by a schema field that forces the model to expose the dimension (the "schema-as-eval-spec" pattern).
>
> Status: v0.1 — classifier + calibrated scam judge running locally on a 20-JD golden set. Not yet deployed (Month 2).

---

## 1. Problem

Job boards are noisy. "AI Engineer" in a title can mean a real LLM-engineering role, an ML/training role, an AI-adjacent infra role, an AI-washed sales role, or an outright partnership scam. Manually triaging which postings are worth applying to is slow and error-prone. leadlens classifies each posting into a structured assessment so the funnel (Month 6) only spends effort on real, fit roles.

**Dogfood:** Manveen will use leadlens on his own US-remote funnel. The tool that gets him hired is itself the portfolio piece.

## 2. Input contract

One JD per record (JSONL):
- `id`, `title`, `company`, `url`, `location` (raw string), `description` (the JD text).
- `expected_category` + `is_edge_case` are **labels** (for eval), not model inputs.

## 3. Output schema (Pydantic — `leadlens_v01.py`)

Each field exists because it is **measurable** and/or because it **forces the model to expose a dimension that a failure mode hides in.**

| Field | Type | Why this field exists |
|---|---|---|
| `seniority` | Literal[intern…lead, unclear] | measurable exact-match; `unclear` prevents guessing |
| `ai_authenticity` | Literal[real_ai_role, ai_adjacent, ai_washed, non_ai] | the core classification; measurable |
| `core_stack` | list[str] | named frameworks/libs; measurable by overlap |
| `stack_unspecified` | bool | **F-004 fix.** Separates "source named no frameworks" (True) from "model missed frameworks that were there" (empty list, False). Without it both look like `[]` and the failure is invisible/unmeasurable. |
| `remote_status` | Literal[…] | measurable; key for India-remote fit |
| `location_signal` | str \| None | region restriction (US only / India OK / global) |
| `comp_signal` | str \| None | raw comp string if present; None if absent (also a red flag) |
| `red_flags` | list[str] | **Guardrail pattern.** Enumerates issues (no comp, partnership, seniority mismatch) — countable, surfaces scams |
| `confidence_reasoning` | str, **min_length=100** | **F-003 fix.** Forces evidence-grounded reasoning BEFORE any verdict — the model can't emit a hardcoded/default confidence without typing 100 chars of quoted evidence first. Critique-before-verdict by construction. |
| `fit_for_manveen` | Literal[strong, medium, weak, skip] | personalized triage; measurable |

## 4. Eval methodology

- **Golden set:** 20 JDs (10 real from HN + 10 synthesized from real archetypes), stratified across all categories + edge cases. `expected_category` hand-labeled. Label hygiene matters — 2/10 first-pass labels were wrong; re-checked after first model run.
- **Classifier metric:** category accuracy vs `expected_category` (≈70% on real labels; 2 legit borderlines, 0 hard model failures).
- **Judge (`judge_v1.py`):** a separate LLM-as-judge for the highest-cost failure mode (F-006: under-calling scams). Critique-shadowing — judge writes critique (min_length=80) THEN binary `is_scam` verdict.
- **Judge calibration:** measured **TPR / TNR**, not raw agreement (class imbalance: only 3/20 positive → an always-no baseline scores 0.85 raw). v1: **TPR 1.0, TNR 0.882.**

## 5. Named failure modes (the taxonomy)

| ID | Name | Fix | Status |
|---|---|---|---|
| F-003 | hardcoded confidence | `min_length=100` on confidence_reasoning | fixed by construction |
| F-004 | thin-stack extraction | `stack_unspecified: bool` companion | fixed by construction |
| F-006 | under-call ai_washed (scams) | dedicated critique-shadowing judge | TPR 1.0 / TNR 0.882; v2 to push TNR ≥ 0.90 |

(F-001/F-002/F-005 originated on the prior staffing-classifier domain; the schema-as-eval-spec method ported cleanly across domains.)

## 6. Metrics + thresholds

- Category accuracy target: ≥ 75% on real labels (CI gate, Month 2).
- Judge: TPR ≥ 0.75 (catch scams — high cost if missed), TNR ≥ 0.90 (don't flag real roles).
- Cost: $0.00085 / JD (Gemini 2.5 Flash). 100-JD run ≈ $0.085.
- Latency: ~5.4 s / JD serial → asyncio.gather batch in v0.2.

## 7. Stack + rationale

- **Gemini 2.5 Flash** — cheap, fast, generous free tier; structured output via Instructor solid. (No fine-tuning — prompt + schema is enough; correctly-skipped Fine-tuning pattern.)
- **Pydantic + Instructor** — schema = eval spec; structured output enforced.
- **Local JSONL** for golden set + outputs + metrics — Langfuse replaces hand-rolled metrics in Month 2.

## 8. Deployment plan (Month 2)

FastAPI `POST /classify` + `POST /judge` → Docker → Modal live URL. Langfuse tracing on every call. GitHub Actions CI gate runs the golden set, fails build if category accuracy or judge TPR/TNR drops. README to standard + 3-min Loom.

## 9. What I'd do next

- judge v2: few-shot examples (1 MIIGO positive, 1 Sumble negative) → push TNR 0.882 → 0.90+.
- Split `ai_washed` into `is_scam` vs `ai_in_title_only` (the category-design lesson: wide categories collapse signal).
- Expand golden set 20 → 100 with real JDs.
- Add `compensation_structure: Literal[...]` to make scam comp-shapes visible by category.

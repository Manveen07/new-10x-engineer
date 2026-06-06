# leadlens v0.1 — iteration 1 findings (Sat 2026-05-30 → Sun 2026-05-31)

10 stratified JDs sourced from HN Who-Is-Hiring May 2026. Schema in `projects/business-classification-pipeline/leadlens_v01.py`. Runner `runner_v01.py` (Gemini 2.5 Flash via Instructor).

## Patterns held / fixed / found

| Pattern | v1 | v2 | Status |
|---|---:|---:|---|
| F-003 hardcoded confidence | 0/10 | 0/10 | **STAYS FIXED** — `min_length=100` on `confidence_reasoning` forces evidence-before-score cross-domain |
| F-004 thin-stack (staffing-style "model failure") | 4/10 | 4/10 | **REFRAMED** — added `stack_unspecified: bool`; now distinguishes source-thin from model-failure |
| JSON output duplication | 1/10 (jd_002) | 0/10 | one-off Gemini glitch, non-reproducible |
| Labeler errors (mine) | 2/10 | 0/10 | re-labeled jd_004 → real_ai_role, jd_008 → non_ai |
| Schema-taxonomy mismatch | — | 2/10 (009, 010) | **NEW** — `expected_category="edge_case"` not in `ai_authenticity` Literal; fix in next iter |

## Category accuracy (after label fix)

6/8 = 75% on real categories. 2 borderlines (jd_006 Bayesian = ML?, jd_007 "uses AI extensively" = ai_adjacent or ai_washed?) — legitimate disagreement, not failure.

## Schema lessons (cross-domain)

- **`min_length=N` on reasoning field = portable F-003 fix.** Worked on staffing classifier (would have) and JD classifier. Schema-as-eval-spec is real.
- **Boolean companion field for ambiguous-empty fields.** `stack_unspecified: bool` next to `core_stack: list[str]` lets you tell "source thin" from "model missed." Pattern: any empty-able list should have a `_unspecified` or `_missing_from_source` companion.
- **Label vocab must match schema vocab.** `expected_category` used "edge_case" — not a category, a stratification meta-tag. Fix: drop from label, add `is_edge_case: bool` on input side.

## Sharper red_flags emergent (v2)

- "location mismatch for Manveen" (jd_004, jd_009)
- "seniority mismatch for junior AI engineer" (jd_009)
- "years gap mismatch" (jd_007 — 5-10 yrs req, junior candidate)

Personalization (`fit_for_manveen`) field is doing real work. Skip/weak rate = 9/10 → correct (Manveen is India-based junior, most US-remote senior roles legitimately don't fit).

## Open questions for next iteration

1. **Drop `edge_case` from `expected_category`** in jds-v0.jsonl. Add `is_edge_case: bool` on input.
2. **Add a v2 vs v1 ablation script** — diff per-field across iterations, log which prompt/schema changes moved which metric.
3. **Synthetic Q-A test?** — generate 20 more JDs covering rare cases (Indian remote, partnership scams, contract-with-comp).
4. **Cost + latency** not measured yet — instrument next.

## Process learnings

- **First-iteration label hygiene matters.** 2/10 of my expected labels were wrong on first source — would have polluted any "accuracy" metric. Always re-check labels after first model run.
- **Cross-domain schema reuse works.** Staffing taxonomy (F-001 ... F-004) ported to JD domain cleanly. Same gulfs, same fixes, same wins.

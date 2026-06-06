# Hamel evals re-read — 2026-05-24

## Three Gulfs (cheat sheet)

- **Comprehension** — don't understand own data. Fix: open coding, axial coding.
- **Specification** — prompt doesn't capture intent. Fix: rewrite prompt, few-shot, decompose, RAG context.
- **Generalization** — model can't handle input variety even with good prompt. Fix: more data, fine-tune. Last resort.

Sources: David Okpare primer, Aayush Garg lifecycle.

## My 3 failure modes mapped

| Mode | Gulf | Fix |
|---|---|---|
| `false_executive_search_signal` | Specification | Few-shot bad examples; FAIL when only keyword evidence |
| `mixed_boundary_ambiguity` | Specification + Comprehension | Add `segment_strength: float` field; prompt requires estimate when segment=mixed |
| `schema_drift` (0.95 hardcoded) | Specification | Reasoning-before-confidence: list signals first, then emit confidence |

**All 3 = Specification gulf. No generalization issues → no fine-tuning, no model swap.**

## leadlens design decisions locked

1. Month 2 = prompt iteration + few-shot. Not data collection, not fine-tuning.
2. Add `segment_strength: float | None` to schema (mixed segment only).
3. Reasoning-before-confidence pattern in prompt.

## Deferred — do next Saturday before Week 2 block (30 min)

4 evals-faq Qs not yet re-read:
- Build evaluators for every failure mode? → which of 3 modes gets a judge
- How to surface problematic traces beyond user feedback? → sampling strategy
- Same model for task + judge? → validates Sonnet + GPT-4.1 plan
- How often re-run error analysis? → Month 2 cadence

---

## Open-coding 50 traces (Mon 2026-05-25, pulled forward from Week 2)

Method: hand-coded traces 0–21 (22 traces) with calibration partner. Stratified-sampled remaining 28 via `filter_traces.py` — 6 surfaced as interesting, 22 auto-tagged as same-pattern. Annotation viewer at `projects/business-classification-pipeline/annotator.py`.

### Findings by pattern (all 50)

| Pattern | Count | Verdict |
|---|---:|---|
| 0.95 confidence | **50/50** | Definitive hardcoded default. **Highest-priority Specification gulf.** Confidence reasoning is non-existent. |
| Thin-evidence string (<30 chars) | **4/50** (idx 7, 13, 22, 32) | Recurring real pattern. Promote to taxonomy as **F-004: thin_evidence_capture**. |
| F-001 false_executive_search resistance | **5/50** (idx 4, 8, 16, 24, 49) | Model has working discriminator. **Don't waste Month 2 fixing F-001.** |
| F-002 mixed_boundary collapse | **1/50** (idx 10) | Less common than Sat-1 v1 estimated. Schema fix (`segment_strength`) still right but lower priority than confidence. |
| F-002 inverse (model under-called exec) | **1/50** (idx 32 borderline) | One case where model collapsed mixed → general_staffing despite Controller/CFO mention. Subtle. |
| F-002 inverse resistance | **1/50** (idx 15) | Model can also discriminate the other way correctly. |
| Hard failure (label ≠ ground_truth) | **0/50** | Sample biased toward easy cases. Month 2 golden dataset must seek harder cases. |

### Taxonomy update — v2

| ID | Name | Status | Priority |
|---|---|---|---|
| F-001 | false_executive_search_signal | **Demote** — 5 resistance cases, 0 confirmed failures in sample. Model handles. | Low |
| F-002 | mixed_boundary_ambiguity | Keep. 1 confirmed + 1 inverse. Schema fix needed. | Medium |
| F-003 | schema_drift / hardcoded_confidence | **Promote to highest** — 50/50 confirmed. | High |
| F-004 | thin_evidence_capture | **New** — 4/50 confirmed. Prompt fix needed. | Medium |

### leadlens design decisions — locked v2

1. **Month 2 priority 1: fix confidence.** Reasoning-before-confidence prompt pattern. Or move confidence calculation out of LLM entirely (rule-based on signal count + diversity).
2. **Month 2 priority 2: fix evidence capture.** Prompt must require ≥50-char evidence string per signal AND require multiple supporting quotes when available.
3. **Schema add: `segment_strength: float | None` for mixed only** (from v1, still valid).
4. **Skip F-001 work in Month 2.** Model already discriminates. Don't add complexity that doesn't move the metric.
5. **Golden dataset stratification:** Month 2 hand-labels must oversample boundary cases and harder firms — current 50 traces all passed, real production failure rate is likely higher.

### Process learnings (for future open-coding)

- Hand-code first ~20 traces, then filter by stratified criteria. Don't grind through pure-pass cases.
- Filter false-positive rate ~33% (2 of 6 boundary-marker hits were just connective grammar). Tune marker list next time.
- Vocab gap "retainer search" surfaced — comprehension gulf on labeler side, not model side. Judge prompt needs this term defined.

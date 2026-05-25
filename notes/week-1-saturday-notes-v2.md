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

# Week 7 — leadlens: Iterate to Threshold + Judge to TNR ≥0.90 + Instrumentation

> 📝 **Draft written 2026-06-09, ahead of the window.** Refine before Week 7 starts, anchored on Week 6's confusion matrix (which category was weakest decides this week's prompt/schema work). leadlens = AI **JD** classifier (Gemini 2.5 Flash). Spec: [../projects/business-classification-pipeline/DESIGN.md](../projects/business-classification-pipeline/DESIGN.md).

**Window:** Mon 2026-07-06 → Sun 2026-07-12
**Time budget:** 8–10 hours
**Position:** Month 2, Week 7 of 24

## Why this week matters

Week 6 told you *where* leadlens fails. Week 7 you fix it — the right way: each fix is a **measured** change (prompt iteration or a new schema field), re-run on the 100, accept only if the number moved. This is the schema-as-eval-spec loop at full speed. By Sunday: category accuracy ≥75% (CI gate green), scam judge TNR ≥0.90, and cost/latency instrumented for the README.

**The single must-do:** scam judge at **TNR ≥0.90 (TPR still 1.0)** on the 100-JD set, committed, with the iteration visible in commits.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-07-06 | Plan review + **kata 22** (`pytest.mark.parametrize` over 5 golden cases, no AI) | 15 min |
| Tue eve | 2026-07-07 | **Kata 23** (refactor: extract `run_judge_eval() -> (tpr, tnr)`, no AI) | 15 min |
| Wed eve | 2026-07-08 | **LeetCode ×1** (intervals/stack) → `dsa/` | 20 min |
| Thu eve | 2026-07-09 | **LeetCode ×1** (graph BFS/DFS intro) → `dsa/` | 20 min |
| Fri eve | 2026-07-10 | Read Hamel on iterating judges OR rest | 15–30 min |
| **Sat** | 2026-07-11 | **Big build**: fix the weakest category (prompt + maybe a new schema field) → re-run 100 → keep only if accuracy moved; add `asyncio.gather` batch + cost/latency capture | **3.5 hrs** |
| **Sun** | 2026-07-12 | **Big build**: judge v2 (few-shot MIIGO/Sumble) → TNR ≥0.90 → re-run CI → PROGRESS + public push | **3.5 hrs** |

Total: ~9 hours.

---

## Saturday — iterate the classifier + instrument (3.5 hrs)

### Revise (15 min)
Re-read your Week-6 open-coding notes for the weakest category. Name the failure mode out loud. Decide *before coding*: is this a prompt problem (wording), a schema problem (no field forces the dimension), or a label problem (your labels are inconsistent)? The fix differs.

### Build A — fix one category, measured (90 min)
- Apply **one** change at a time (the discipline that makes the eval interpretable):
  - Prompt: add a worked example or a sharper category boundary.
  - Schema (the leadlens signature): if a failure hides in an untyped dimension, add a field that forces it — e.g. `compensation_structure: Literal[...]` to make scam comp-shapes visible (DESIGN §9), or split `ai_washed` into `is_scam` vs `ai_in_title_only` (wide categories collapse signal).
- Re-run all 100. **Accept the change only if category accuracy went up.** Revert if not — a change that doesn't move the number is noise. Commit each accepted iteration separately (visible v1→v2→v3 history).

### Build B — async batch + cost/latency (60 min)
- Implement the `asyncio.gather` batch (kata 19): ~5.4 s/JD serial → concurrent. Capture p50/p95 from Langfuse over the 100-run.
- Confirm cost/JD from Langfuse (~$0.00085) and write the README cost table: per-JD + per-100-run.

### Recall (15 min)
*"Which fix moved the number, and was it prompt or schema?"* The answer is a blog-post paragraph and an interview story.

## Sunday — judge v2 to TNR ≥0.90 (3.5 hrs)

### Build (2.5 h)
- Add 2 few-shot examples to the scam judge: 1 positive (MIIGO archetype) + 1 negative (Sumble — vague but real product ≠ scam). Tighten the "vague + real product is NOT a scam" instruction.
- Re-run the judge CI eval (`tests/test_judge.py`) on the 100. Target **TNR ≥0.90, TPR = 1.0**.
- If TNR still short: read the false-positives, decide if a label is wrong (re-label 1–3) or the prompt needs a borderline rule. Re-run.
- Commit judge v1 → v2 as separate commits.

### Close (45 min)
- PROGRESS update + confidence re-rate.
- **Public push:** tweet the before/after — "scam judge: TNR 0.882 → 0.91 with two few-shot examples. Calibrated on TPR/TNR, not accuracy — here's why that matters with 15% positives."

## Behind if
- Category accuracy below the 75% CI gate.
- Judge TNR below 0.90.
- Iterations dumped in one commit (no visible v1→v2→v3).
- No p50/p95 + cost numbers captured.

## Next week
→ `week-8.md`: Modal deploy, README to standard, 3-min Loom, blog post 2 — leadlens goes live.

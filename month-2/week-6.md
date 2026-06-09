# Week 6 — leadlens: 100-JD Golden Set + First Full Run + Confusion Matrix

> 📝 **Draft written 2026-06-09, ahead of the window.** Refine the weekend before Week 6 starts, anchored on what Week 5 actually shipped (Langfuse wired? judge in CI? candidates sourced?). leadlens = AI **job-description** classifier (Gemini 2.5 Flash). Spec: [../projects/business-classification-pipeline/DESIGN.md](../projects/business-classification-pipeline/DESIGN.md).

**Window:** Mon 2026-06-29 → Sun 2026-07-05
**Time budget:** 8–10 hours
**Position:** Month 2, Week 6 of 24

## Why this week matters

You can't improve what you can't measure, and you can't measure a classifier without a labeled set bigger than 20. This week you take the golden set from 20 → **100 hand-labeled JDs**, run leadlens across all 100, and produce the first **confusion matrix + per-category breakdown**. That matrix is the artifact that tells you *which* category leadlens is weak on — and it's a README centerpiece hiring managers screen for.

**The single must-do:** 100 JDs labeled in `data/golden-100.jsonl` + a confusion matrix committed (image or table) by Sunday.

**Label hygiene is the skill here.** You already learned 2/10 first-pass labels were wrong. Labeling 100 means your *own consistency* is now an eval target — write the rubric down before you label, not after.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-06-29 | Plan review + **kata 20** (`Enum` + `match/case` over `ai_authenticity` categories, no AI) | 15 min |
| Tue eve | 2026-06-30 | **Kata 21** (Pydantic `field_validator` that rejects `confidence_reasoning` < 100 chars, no AI) | 15 min |
| Wed eve | 2026-07-01 | **LeetCode ×1** (hash-map/counting) → `dsa/` | 20 min |
| Thu eve | 2026-07-02 | **LeetCode ×1** (two-pointer/sliding-window) → `dsa/` | 20 min |
| Fri eve | 2026-07-03 | Write the labeling rubric (1 page) OR rest | 15–30 min |
| **Sat** | 2026-07-04 | **Big build**: finish labeling 100 JDs against the rubric (calibration-pair the ambiguous ones) | **3.5 hrs** |
| **Sun** | 2026-07-05 | **Big build**: run leadlens on all 100 → confusion matrix + per-category accuracy → open-code the misses → PROGRESS + public push | **3.5 hrs** |

Total: ~9 hours.

---

## Friday — the labeling rubric (do this BEFORE Saturday)

One page in `data/LABELING-RUBRIC.md`. For each `ai_authenticity` value, write the decision boundary in one sentence + one example:
- `real_ai_role` — builds/ships LLM or ML systems as the core job. *(e.g. "fine-tune and serve retrieval models")*
- `ai_adjacent` — AI-touching but not core (data eng for an AI team, AI-product PM-eng).
- `ai_washed` — "AI" in the title/marketing, but the actual work isn't. *(the F-006 danger zone)*
- `non_ai` — no real AI content.
- Edge cases: scam/partnership posts, vague-but-real-product, seniority mismatch → how each is labeled.

Recall: *"What's the boundary between `ai_adjacent` and `ai_washed`?"* If you can't state it crisply, your labels will be noisy.

## Saturday — label 100 JDs (3.5 hrs)

- Start from Week 5's `golden-candidates.jsonl` + your existing 20.
- Label against the rubric. For any JD you hesitate on >30 sec, mark `is_edge_case=true` and note *why* — those are the calibration-pair cases that teach the most.
- Stratify so no category is starved: aim ≥15 per main category, ~10 edge cases.
- Commit `data/golden-100.jsonl`: full input contract + `expected_category`, `expected_is_scam`, `is_edge_case`, `label_note`.

> Use the annotator you built in Month 1 (`annotator.py`) — don't hand-edit JSONL. The tool exists; use it.

## Sunday — first full run + confusion matrix (3.5 hrs)

### Build (2 h)
- Run leadlens on all 100 (use the `asyncio.gather` batch if Week 5 landed it — otherwise serial, ~9 min, fine).
- Compute **category accuracy** overall + **per category** (this is where "segment, don't average" first bites — overall 75% can hide 50% on `ai_washed`).
- Build a confusion matrix (`sklearn.metrics.confusion_matrix` + a `matplotlib` heatmap, or a markdown table). Save `docs/confusion-matrix.png`.
- Run the scam judge over the 100; recompute TPR/TNR on the larger set (your CI test from Week 5 now has real teeth).

### Open-code the misses (1 h) — the learning core
For every misclassification: one line — *which category, what the model saw, why it went wrong, which failure mode (F-003/4/6 or new)*. This is the exact Month-1 muscle, now on 100 rows. New failure modes get an F-00x id and go in `failure-taxonomy.md`.

### Recall + close (30 min)
- Recall: *"Which category is leadlens weakest on, and is it a prompt, schema, or label problem?"*
- PROGRESS update + tweet the confusion matrix ("100-JD eval: here's where my classifier is actually weak").

## Behind if
- Fewer than 80 JDs labeled.
- No confusion matrix.
- Misses not open-coded (you have numbers but no diagnosis).
- Scam-judge CI test not re-run on the 100.

## Next week
→ `week-7.md`: iterate prompt + schema on the worst category, push scam judge to TNR ≥0.90, add async-batch + cost/latency instrumentation.

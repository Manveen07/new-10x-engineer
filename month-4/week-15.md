# Week 15 — docsight: Cited Generation + Calibrated Ragas + Land the OSS PR

> 📝 **PROVISIONAL draft (2026-06-09).** Refine the weekend before, anchored on Week 14's ablation winner (you generate on top of the best retriever). Month reasoning: [../PLAN-MONTHS-2-6.md](../PLAN-MONTHS-2-6.md#month-4--ship-docsight-the-ablation-table--merge-oss-pr--mercor).

**Window:** Mon 2026-08-31 → Sun 2026-09-06
**Time budget:** 8–10 hours
**Position:** Month 4, Week 15 of 24

## Why this week matters

Retrieval feeds generation — now you measure the *answer*, not just the chunks. And you reuse the exact calibration muscle from leadlens (critique-shadowing, TPR/TNR): Ragas with default prompts and no calibration is noise, so you calibrate the generation judges against ~30 hand labels. You also land the OSS PR you opened in Month 3 — the Mercor asset goes from "in motion" to "merged."

**The single must-do:** cited generation working + Ragas (faithfulness, answer-relevance, context-precision) calibrated against ~30 hand labels — by Sunday. OSS PR merged (or in final review) this week.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-08-31 | Plan review + **LeetCode ×1** | 20 min |
| Tue eve | 2026-09-01 | Read [Ragas docs](https://docs.ragas.io/) on the metric definitions → recall: "faithfulness vs answer-relevance — what does each catch?" | 20 min |
| Wed eve | 2026-09-02 | Respond to OSS PR review comments | 30 min |
| Thu eve | 2026-09-03 | **LeetCode ×1** + hand-label 10 of the 30 generation eval cases | 30 min |
| Fri eve | 2026-09-04 | Hand-label the remaining 20 OR rest | 15–30 min |
| **Sat** | 2026-09-05 | **Big build**: cited generation (every claim → chunk citation) + run Ragas + calibrate judges vs your 30 labels (critique-shadowing, measure agreement) | **3.5 hrs** |
| **Sun** | 2026-09-06 | **Build**: tighten until Ragas agrees with your labels; land the OSS PR; capture the maintainer thank-you screenshot → PROGRESS | **3.5 hrs** |

## Saturday — cited generation + calibrate Ragas (3.5 hrs)
- Generation prompt: answer **only** from retrieved chunks, every claim carries a `[chunk_id]` citation; refuse if context is insufficient (don't hallucinate).
- Run Ragas faithfulness + answer-relevance + context-precision on a question set.
- **Calibrate:** compare Ragas verdicts to your 30 hand labels. If they disagree, the default judge prompt is wrong for your domain — adjust it (the leadlens lesson: an uncalibrated judge is noise). Measure agreement.

## Sunday — close the loop + OSS merge (3.5 hrs)
- Iterate generation/judge until Ragas tracks your labels. Record the calibrated numbers for the README.
- **Land the OSS PR**: address the last review notes, get it merged. Screenshot the merge + any maintainer thanks → `notes/oss-pr.md` (Mercor portfolio asset).
- PROGRESS update.

## Behind if
- Generation isn't cited (claims without chunk ids).
- Ragas run but uncalibrated (numbers you can't trust).
- OSS PR still unmerged with no clear path to merge.

## Next week
→ [week-16.md](./week-16.md): deploy docsight on Modal, $/query, Loom, blog post 4, **apply to Mercor**.

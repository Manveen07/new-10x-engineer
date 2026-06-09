# Month 2 — Ship leadlens

## Goal

Convert Month 1's eval discipline into a *deployed, observed, eval-instrumented* **JD classifier**. By Sunday 2026-07-19 you have a live URL on Modal, a 100-JD golden dataset, a category-accuracy CI gate + a calibrated scam judge (TPR ≥0.75 / TNR ≥0.90), a confusion matrix in the README, a 3-min Loom, and blog post 2 published.

**Pace:** 8–10 hrs/week.
**Window:** 2026-06-22 → 2026-07-19.

## Outcome by end of month

- `projects/business-classification-pipeline/` (leadlens) is a deployed Modal endpoint at a public URL.
- 100-JD hand-labeled golden dataset committed.
- Category-accuracy CI gate (≥75% on real labels) + calibrated scam judge (TPR ≥0.75 / TNR ≥0.90); add judges for other dimensions (e.g. evidence support) as needed.
- README to standard (architecture diagram, "where it fails," eval table, cost-per-call, p50/p95 latency, Loom embed).
- Langfuse traces wired from line one of every code path; trace screenshots in README.
- 3-min Loom walkthrough recorded and linked.
- Blog post 2 published: "Auditing my own LLM classifier."
- LinkedIn + X announcement with eval-table screenshot.
- Outbound prep: 30 US AI founders saved to a future-outreach sheet (not contacted yet).

## Week themes

| Week | Window | Theme |
|---|---|---|
| 5 | Jun 22 – Jun 28 | Scaffolding + Langfuse + DLAI accuracy course + judge port |
| 6 | Jun 29 – Jul 5 | Hand-label 100 JDs → first full end-to-end run → confusion matrix v1 + per-category breakdown |
| 7 | Jul 6 – Jul 12 | Iterate prompt + schema on failures; push scam judge to TNR ≥0.90; async-batch + cost/latency instrumentation |
| 8 | Jul 13 – Jul 19 | Modal deploy; README to standard; Loom; blog post 2; X+LinkedIn announce |

Week files (`week-5.md` through `week-8.md`) get written ~3 days before each week begins, anchored on what you actually shipped the prior week. See [the cadence note below](#why-week-files-arrive-just-in-time). ([week-5.md](./week-5.md) · [week-6.md](./week-6.md) · [week-7.md](./week-7.md) · [week-8.md](./week-8.md) have early drafts — refine each the weekend before it starts, anchored on what actually shipped the prior week.)

### Carry-forward — already shipped in Month 1 (you finished ahead). Week 5 starts here; don't rebuild it.

- **leadlens v0.1**: Pydantic schema + Instructor runner + 20-JD corpus → Week 5 "scaffolding" largely exists.
- **Judge v1** (critique-shadowing, TPR=1.0 / TNR=0.882) → Week 5 "judge port" is lift-and-calibrate, not a rebuild.
- **Cost/latency instrumentation** already surfaced (F-006) → Week 7 instrumentation has a head start.
- **leadlens `DESIGN.md`** committed.

So Month 2's real weight shifts forward to: the **100-example golden dataset** (Week 6), pushing **all 4 judges to >90%** (Week 7), and **Modal deploy + README-to-standard + blog post 2** (Week 8). Week 5 absorbs forward instead of repeating Month 1.

## Build standard (from PROJECTS.md)

By end of Week 8, leadlens README answers all seven portfolio questions ([PROJECTS.md](../PROJECTS.md) — "Portfolio rule"):

- What did the system do?
- What data did it run on?
- How did you know it was good?
- What failed and what did you change?
- What did it cost? How slow?
- How would you run it in production?
- What would you do next with two more weeks?

## Monthly checklist

See [EXERCISES.md](../EXERCISES.md) Month 2 section.

## Interview skill added

By end of month you can answer **"Walk me through a real LLM system you shipped end-to-end with evals"** for 5 minutes without notes, with a live URL + Loom + eval-table screenshot you can pull up on screen.

That single sentence is the entry ticket for every US-remote AI-engineer interview in 2026. Most fresher candidates can't deliver it. You will.

## Behind if

- No deployment by end of Week 8.
- Fewer than 80 golden examples labeled.
- No confusion matrix in README.
- No Loom recorded.
- Blog post 2 not published.

## Why week files arrive just-in-time

Old-plan approach: write all 24 week files upfront, follow them rigidly. Doesn't survive contact with real progress.

New approach: each week file is written ~3 days before the week starts, informed by what *actually* shipped the prior week. If Week 5 lands faster than expected, Week 6 absorbs Week 7 work. If Week 5 slips, Week 6 recovers. This is a feature — pre-committed daily plans for weeks you haven't lived yet are usually wrong.

If at any point you want a draft of an upcoming week ahead of time, ask. The plan flexes.

## Next month

→ [../month-3/README.md](../month-3/README.md) — RAG fundamentals + docsight design + first OSS PR.

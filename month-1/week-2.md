# Week 2 — Open Coding 50 Traces with Three Gulfs

**Window:** Mon 2026-05-11 → Sun 2026-05-17
**Time budget:** 8 hours
**Position in plan:** Month 1, Week 2 of 24

## Why this week matters

You have 50 real traces from Week 1. This week you look at every single one and write a one-line note about what's right or wrong with it. This is "open coding" — the foundational eval skill that hiring managers screen for in 90 seconds. Skipping this is the single most common AI-engineer-candidate failure mode.

The Three Gulfs framework (Hamel Husain & Shreya Shankar) gives you the categories to look for: **specification gulf** (the prompt is unclear), **generalization gulf** (the model can't handle this case), **comprehension gulf** (you don't understand the output yet).

## Daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon | 2026-05-11 | Re-read your 10 trace notes from Saturday Week 1; pick a notes format (markdown table or `notes` column in JSONL) | 45 min |
| Tue | 2026-05-12 | Open-code traces 1–15 — one line per trace describing what you see | 90 min |
| Wed | 2026-05-13 | Read Eugene Yan "Patterns for Building LLM-based Systems & Products" if not done | 60 min |
| Thu | 2026-05-14 | Open-code traces 16–30 | 90 min |
| Fri | 2026-05-15 | Open-code traces 31–50 | 90 min |
| Sat | 2026-05-16 | Re-read all 50 notes; flag the obvious clusters (3–5 categories emerging?) | 90 min |
| Sun | 2026-05-17 | Update `PROGRESS.md`; plan Week 3 | 30 min |

Total: ~8 hours.

## Open coding rules

- **One line per trace.** If you write more than one sentence, you're slowing yourself down. "Hallucinated industry tag" beats a paragraph.
- **Plain language first, jargon never.** "Said the winery was operating but the website is down" is fine. Don't pre-cluster.
- **Tag the gulf if obvious:** `[spec]` / `[gen]` / `[comp]`. If unclear, leave blank.
- **Do not iterate yet.** No edits to the prompt this week. Only observation.

Example notes column entries:

```
trace_007: confident "operating" but website returned 404 last month [gen]
trace_012: ambiguous case — site exists but no recent activity, output marked "operating" with 0.4 confidence — looks fine
trace_023: hallucinated address, model invented street name not in source [gen]
trace_031: prompt didn't specify what to do with parent-company / subsidiary cases [spec]
```

## Resources used this week

- [hamel.dev/blog/posts/evals-faq](https://hamel.dev/blog/posts/evals-faq/) — re-read the open-coding section if it didn't land in Week 1.
- [eugeneyan.com/writing/llm-patterns](https://eugeneyan.com/writing/llm-patterns/) — finish if not done.
- Three Gulfs framework — covered in Hamel's evals-faq, no separate link needed.

## Deliverable checklist

- [ ] All 50 traces have a one-line note.
- [ ] At least 30 notes carry a `[spec]`, `[gen]`, or `[comp]` tag.
- [ ] Saturday cluster pass: 3–5 emerging categories written down at the top of the file.
- [ ] Eugene Yan post read.
- [ ] `PROGRESS.md` Week 2 block filled in.

## Behind if

- Fewer than 50 traces have notes.
- You haven't tried to cluster yet (Saturday step skipped).
- You started editing the prompt this week instead of just observing.

## What unlocks next week

Week 3 turns these 50 unstructured notes into a formal failure taxonomy — a named, finite list of failure modes you can build judges against. That requires having the raw notes done first.

## Next file

→ [week-3.md](./week-3.md) — failure taxonomy and annotation viewer.

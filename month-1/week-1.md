# Week 1 — Setup, Day 0 Prereqs, Pull Real Traces

**Window:** Mon 2026-05-04 → Sun 2026-05-10
**Time budget:** 8 hours
**Position in plan:** Month 1, Week 1 of 24

## Why this week matters

You cannot do eval-first work on imaginary data. This week exists to get tooling out of the way and put 50 real LLM traces in front of you, so the reading on Saturday connects to your actual classifier outputs — not someone else's tutorial.

If you finish nothing else, finish item #4 (50 traces pulled). It unblocks Weeks 2–4.

## Daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon | 2026-05-04 | Modal hello world deployed at a public URL | 30 min |
| Mon | 2026-05-04 | Langfuse free cloud account, API keys saved | 15 min |
| Tue | 2026-05-05 | Pydantic + Instructor speedrun: nested `Company` extraction in a notebook | 90 min |
| Wed | 2026-05-06 | Confirm GitHub repo public; buy personal domain if needed; install `uv` + `ruff` | 45 min |
| Thu | 2026-05-07 | Pull 50 real classifier traces into `projects/business-classification-pipeline/data/traces-week-1.jsonl` | 90 min |
| Fri | 2026-05-08 | Pick Quarto or Astro in 30 min; deploy one-page portfolio site to your domain | 2 hrs |
| Sat | 2026-05-09 | Read Hamel `evals-faq` + Eugene Yan LLM patterns; jot 10 failure-mode notes against your traces | 2.5 hrs |
| Sun | 2026-05-10 | Update `PROGRESS.md`; plan Week 2 | 30 min |

Total: 8 hours. If a task overruns 2× its budget, stop and log it instead of pushing through.

## Resources used this week

- [modal.com](https://modal.com) — sign up with GitHub, run their hello-world example.
- [langfuse.com](https://langfuse.com) — free cloud tier, 50K observations/month.
- [python.useinstructor.com](https://python.useinstructor.com/) — Instructor docs intro.
- [hamel.dev/blog/posts/evals-faq](https://hamel.dev/blog/posts/evals-faq/) — Saturday reading.
- [eugeneyan.com/writing/llm-patterns](https://eugeneyan.com/writing/llm-patterns/) — Saturday reading.
- [quarto.org](https://quarto.org/) **or** [astro.build](https://astro.build/) — pick one in 30 min on Friday.

## Deliverable checklist

By Sunday night, the following should exist and be linkable:

- [ ] Modal: a deployed function returning JSON at a public URL.
- [ ] Langfuse: account live, API keys stored in a password manager.
- [ ] Notebook: one Pydantic `Company` model with nested `Signal` items, populated by Instructor from a paragraph of text.
- [ ] GitHub: this repo is public.
- [ ] Domain: yourname.com (or .dev) registered.
- [ ] `uv` and `ruff` installed (`uv --version` and `ruff --version` both print).
- [ ] `projects/business-classification-pipeline/data/traces-week-1.jsonl` (or `.md`) committed with 50 entries.
- [ ] Portfolio site live at your domain with a real homepage (one paragraph + three project placeholders is enough).
- [ ] Notes file with ~10 one-line failure-mode observations connecting Hamel/Eugene's frameworks to your own traces.
- [ ] `PROGRESS.md` Week 1 block filled in honestly (hours, shipped, slipped, Week 2 focus).

## Trace format guideline

When you pull traces on Thursday, use this minimal JSONL schema. One trace per line:

```json
{"id": "trace_001", "input": {"company_name": "Acme Wines", "domain": "acmewines.com"}, "output": {"status": "operating", "confidence": 0.85, "evidence": ["..."]}, "ground_truth": "operating", "notes": ""}
```

Don't analyze yet. Just gather. Notes column stays empty until Week 2.

## Behind if

- You haven't pulled 50 traces.
- Your portfolio site is not live.
- You haven't read either Hamel `evals-faq` or Eugene Yan's LLM patterns post.

## What unlocks next week

Week 2 (open coding 50 traces with the Three Gulfs framework) is impossible without the 50 traces and the Hamel reading from this week. If either is missing on Sunday, finish them before starting Week 2.

## Next file

→ [week-2.md](./week-2.md) — open coding and failure analysis.

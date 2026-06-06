# Week 1 — Saturday reading notes

Reading: Hamel `evals-faq` + Eugene Yan LLM patterns, with the 50 staffing-firm classifier traces open.

## Core insight from Hamel's opening

Manual error analysis comes before automated eval — because automation without understanding optimizes for the wrong thing. You can't build an LLM judge that catches failures you haven't named yet.

The loop is: look at traces by hand → name the failure modes → *then* automate the patterns you found.

## Failure modes spotted in my own traces

1. **False executive-search signal.** A firm lists "executive search" on their website as a marketing keyword but doesn't actually do it (or does it only nominally, one or two C-suite placements). The classifier sees the keyword and labels it `executive_search` or `mixed` when in practice the firm is general staffing. Candidates to inspect in Week 2: traces where evidence is one short keyword string and the firm name doesn't suggest seniority focus.

2. **Mixed-boundary ambiguity.** Firms that do both senior and junior placements get labeled `mixed`, but the real-world signal often leans heavily one way. A firm that's 80% executive and 20% staffing should probably be `executive_search`. The classifier collapses everything in the middle into `mixed` without a strength signal.

3. **Format / schema drift.** Output not always in the expected shape — confidence values that look hardcoded at 0.95 across all 50 traces, evidence strings that vary wildly in length and structure. Worth checking whether the model is actually reasoning about confidence or just defaulting.

## What this changes about Project 1

Before any prompt changes or "fixes," Week 2 will go through these 50 traces manually and tag each one as correct / wrong / ambiguous, then group the wrongs by failure mode. Only after that do we touch the prompt or the schema.

## Error analysis methodology (from Hamel)

**Open coding.** Read each trace and write a free-form note describing what you see — what's right, what's wrong, what's interesting. No pre-built categories. Let the labels emerge from the data, not the other way around. Skipping this step means you only ever find failures you were already expecting.

**Axial coding.** After all 50 traces are open-coded, group the notes that say similar things. Each cluster becomes a *failure mode* with a short name (e.g. "shallow evidence", "keyword false positive", "mixed-boundary ambiguity"). Now you have a taxonomy that's grounded in your actual data.

**Order matters: open first, axial second.** Building categories before reading traces makes you confirm your priors instead of discovering the real patterns.

## Why binary pass/fail, not 1–5

1–5 scales produce noise — boundaries are fuzzy, ratings vary across people and across time. Binary forces a shipping decision ("would I ship this?") that's easier to make consistently. Binary labels are also actionable: "fail — missed the executive search signal" tells you exactly what to fix. A "3/5" tells you nothing.

Evals are decisions, not grades.

## Cost-aware thresholds

There is no universal "good enough" number. Each failure mode has its own cost. Some get driven to zero (e.g. wrong-firm-type in a GTM workflow → wrong outbound email). Others can be tolerated. The question to ask before any threshold conversation: *what's the downstream cost of each kind of failure?*

For my staffing classifier specifically — both error directions are roughly equally costly: a `general_staffing` firm wrongly labeled `executive_search` means an offer hits the wrong inbox; the reverse means a real ICP gets skipped entirely. Neither is cheap.

## Deferred from Saturday Week 1 — pick up in Week 2

Did not read end-to-end. Bring these into Week 2 alongside the open-coding work — each one has direct relevance to what we'll be doing:

- **Hamel "Q: How do I surface problematic traces for review beyond user feedback?"** — relevant before sampling new traces.
- **Hamel "Q: How often should I re-run error analysis on my production system?"** — relevant for the Project 1 deployment story.
- **Hamel "Q: Should I build automated evaluators for every failure mode I find?"** — directly relevant once Week 2 produces failure-mode clusters.
- **Hamel "Q: Can I use the same model for both the main task and evaluation?"** — relevant when we wire up the first LLM judge.
- **Hamel "Three Gulfs" framework** — not on this page, lives in Hamel's "A Field Guide to Rapidly Improving AI Products." Read before Week 2's axial coding.

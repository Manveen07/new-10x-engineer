# leadlens — failure taxonomy

Named failure modes found while building the JD classifier + scam judge. Each = how it showed up, the fix, and current status. The through-line: **schema-as-eval-spec** — most failures got killed by a schema field that forces the model to expose the dimension it was hiding in.

| ID | Name | How it showed up | Fix | Status |
|---|---|---|---|---|
| F-003 | hardcoded confidence | classifier emitted the same `confidence` value every time — defaulting, not reasoning | `confidence_reasoning: str = Field(min_length=100)` — must write evidence before any score | fixed by construction |
| F-004 | invisible thin extraction | `core_stack` came back empty; couldn't tell "source named nothing" from "model missed it" | `stack_unspecified: bool` companion field — model must declare which case | fixed by construction |
| F-006 | scam under-call (ai_washed) | classifier over-trusts the word "AI"; flags fake roles as real | dedicated critique-shadowing judge (critique before binary verdict) | judge TPR 0.818 / TNR 1.0 on 72 (honest) |
| F-007 | eval label leak | golden-set JD **descriptions** had editorial hints baked in ("zero technical AI work"); the judge read my answer and echoed it → inflated 1.0 | `clean_descriptions.py` strips editorial tells, leaving only real posting text | fixed; honest TPR fell 1.0 → 0.818 |

## The most important one — F-007

Not a parser/regex bug. The *input* leaked the *label*. The headline 1.0 was the eval grading its own crib notes — I'd written how-I-judge-it into the description, so the judge followed my notes and returned my score. Stripping the hints gave the honest number (0.818). **The lower number is the trustworthy one; the higher number was fake.** A failure in the measurement looks like success, which is what makes it dangerous.

## Open frontier (judge v3 targets)
The 2 scams that slip on clean inputs are the genuinely ambiguous shapes:
- "Director of Partnerships (Legal AI)" at a real AI company — sounds like a real role, is sales.
- "AI Trainer" coding-gig (DataAnnotation) — real coding, but piecework annotation, not a job.
Both fool a fast human read too. Next iteration: few-shot these exact shapes.

## Method note
Found via: open-coding outputs by hand (not aggregate metrics), naming patterns, then fixing the cheapest layer first (schema > prompt > judge). 60-80% of the value was reading the data, not the dashboards.

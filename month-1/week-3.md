# Week 3 — Axial Taxonomy + First LLM-as-Judge

**Window:** Mon 2026-06-08 → Sun 2026-06-14
**Time budget:** 8–10 hours
**Position:** Month 1, Week 3 of 24

## Why this week matters

Open coding (Week 2) tells you what you see. Axial coding (Week 3) turns that into a taxonomy — a small set of named failure modes that you can build automated checks for. Then you write your first LLM-as-judge and iterate it until it agrees with your hand labels >85% (Week 4 will push to >90%).

This is the exact pipeline Hamel and Shreya teach in their Maven AI Evals cohort. By Sunday, you have the same artifact a $1,800 course produces — for free, on your own data.

**The single must-do:** a `failure-taxonomy.md` with 4–7 named categories committed to the repo by Friday.

## At-a-glance daily plan (weekday-light, weekend-heavy)

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-06-08 | Plan review + **kata 10** (Enum + match/case, no AI) | 15 min |
| Tue eve | 2026-06-09 | **Kata 11** (Pydantic field validation, no AI) | 15 min |
| Wed eve | 2026-06-10 | **Kata 12** (async LLM calls with `AsyncAnthropic`, no AI) | 15 min |
| Thu eve | 2026-06-11 | **Kata 13** (small refactor of one kata, no AI) | 15 min |
| Fri eve | 2026-06-12 | Skim one post OR rest | 15 min |
| **Sat** | 2026-06-13 | **Big build block**: draft taxonomy + tag all 50 traces in annotator + read Hamel `llm-judge` + sketch first judge prompt | **3.5 hrs** |
| **Sun** | 2026-06-14 | **Big block**: build judge v1, run on 20 traces, iterate to v2, run on all 50, commit `failure-taxonomy.md` + disagreement notes + tweet + PROGRESS | **3.5 hrs** |

Total: ~9 hours.

**Note:** body sections below were drafted with the old cadence and will be rewritten the weekend before Week 3 starts. The daily-plan table above is the source of truth.

---

## Monday — Taxonomy draft + kata 10 (90 min)

**Goal:** A first cut of 4–7 named failure modes, named precisely enough that you could explain each in 1 sentence to a hiring manager.

### Draft taxonomy (60 min)

Open `notes/week-2-saturday.md` (your clusters). For each cluster, give it a 2–4 word name and a 1-sentence definition. Aim for 4–7.

You already have a head start from your Saturday Week 1 notes:
- `false_executive_search_signal` — firm has "executive search" as a marketing keyword but doesn't actually do it; model picks up the keyword.
- `mixed_boundary_ambiguity` — firm does both senior + junior placements; lean is significant but model collapses to `mixed` without strength signal.
- `schema_drift` — output shape inconsistent; confidence values appear hardcoded; evidence string length varies wildly.

Add 1–4 more from this week's open coding. Commit to:

`projects/business-classification-pipeline/failure-taxonomy.md`:

```markdown
# leadlens failure taxonomy

v1 — built from open-coding 50 staffing-firm classifier traces, Weeks 1–3 of Month 1.

| ID | Name | One-sentence definition | Example trace # | Severity |
|---|---|---|---|---|
| F-001 | false_executive_search_signal | Model labels firm as `executive_search` based on marketing keyword without supporting evidence. | 3, 7, 22 | High |
| F-002 | mixed_boundary_ambiguity | Firm leans 80/20 but model returns `mixed` without strength signal. | 14, 19, 28 | Medium |
| F-003 | schema_drift | Output schema inconsistent (e.g., confidence hardcoded at 0.95, evidence strings vary in length wildly). | 1, 5, 11, 38 | High |
| F-004 | … | … | … | … |

## How these were found
Open coding of 50 traces with Three Gulfs framework (Week 2), then axial clustering (Week 3).
```

### Kata 10 — `Enum` + match/case (30 min, NO AI)

```python
# katas/kata_10_enum.py
from enum import StrEnum

class FailureMode(StrEnum):
    FALSE_EXECUTIVE_SEARCH = "false_executive_search_signal"
    MIXED_BOUNDARY = "mixed_boundary_ambiguity"
    SCHEMA_DRIFT = "schema_drift"
    OTHER = "other"

def severity(mode: FailureMode) -> str:
    # use match/case
    ...
```

Plus a test that covers all 4 enum values.

---

## Tuesday — Tag all 50 traces + kata 11 (90 min)

### Extend the annotator (30 min)

Add a `taxonomy: list[str]` field to your `notes.jsonl` schema (allow multiple categories per trace). Add a `st.multiselect` widget reading from `failure-taxonomy.md`.

### Re-tag all 50 (45 min)

For each trace, select the failure modes that apply (0 to many). 90s per trace. Bias toward tagging more rather than less — Week 4 judge will care about every signal.

### Kata 11 — JSON schema validation (30 min, NO AI)

In `katas/kata_11_schema.py`:

```python
from pydantic import BaseModel, Field, ValidationError

class ClassifierOutput(BaseModel):
    segment: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str = Field(min_length=20)
    signals: list[str]

def validate_output(raw: dict) -> tuple[ClassifierOutput | None, list[str]]:
    """Return (parsed, list_of_errors). Catch ValidationError, return errors."""
    ...
```

Test: 1 valid, 2 invalid (confidence out of range, evidence too short).

---

## Wednesday — Hamel `llm-judge` + sketch first judge (90 min)

### Read (60 min)

Read [Hamel's llm-judge post](https://hamel.dev/blog/posts/llm-judge/) end-to-end. Take notes specifically on:

- **Critique shadowing** — judge produces a critique *before* the binary pass/fail
- **Binary > Likert** — why 1–5 scales are noise
- **Agreement metrics** — TPR / TNR / balanced accuracy vs your hand labels
- **When LLM-as-judge fails** — known limits

### Sketch judge prompt v0 (30 min)

In `projects/business-classification-pipeline/judge/judge_v0.md`, draft a prompt for one of your failure modes (start with `false_executive_search_signal`):

```markdown
You are an evaluator for a staffing-firm classifier. Read the input company info and the model's classification. Determine whether the failure mode "false_executive_search_signal" applies.

Definition of failure: the model labeled the firm `executive_search` or `mixed` based on a keyword in marketing copy, but the evidence does not support that the firm actually does executive search work.

Process:
1. Write a 2-sentence critique of the model's reasoning. What's their stated evidence? Does the evidence support the label?
2. Output a binary label: PASS (failure mode does not apply) or FAIL (failure mode applies).
3. If FAIL, give a 1-sentence reason.

Format your output as JSON: {"critique": "...", "label": "PASS" | "FAIL", "reason": "..."}
```

Save to `judge/judge_v0.md`. This is v0 of one judge. Week 4 will make it v3+ and add judges for the other failure modes.

---

## Thursday — Build judge v1 + run on 20 traces + kata 12 (2 hrs)

### Build (75 min)

Create `judge/judge_v1.py`:

```python
"""Run judge_v0 prompt against trace samples. Compare to hand labels."""
from pathlib import Path
import json
import instructor
from anthropic import Anthropic
from pydantic import BaseModel
from typing import Literal

class JudgeOutput(BaseModel):
    critique: str
    label: Literal["PASS", "FAIL"]
    reason: str = ""

client = instructor.from_anthropic(Anthropic())
PROMPT = Path("judge/judge_v0.md").read_text()

def judge_trace(trace: dict, failure_mode: str = "false_executive_search_signal") -> JudgeOutput:
    msg = f"{PROMPT}\n\nINPUT:\n{json.dumps(trace.get('input'))}\n\nMODEL OUTPUT:\n{json.dumps(trace.get('output'))}"
    return client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": msg}],
        response_model=JudgeOutput,
    )

if __name__ == "__main__":
    traces = [json.loads(line) for line in Path("data/traces-week-1.jsonl").read_text().splitlines()][:20]
    notes = {json.loads(line)["idx"]: json.loads(line) for line in Path("data/notes.jsonl").read_text().splitlines()}

    correct = 0
    total = 0
    for i, trace in enumerate(traces):
        human_label = "FAIL" if "false_executive_search_signal" in notes.get(i, {}).get("taxonomy", []) else "PASS"
        judge = judge_trace(trace)
        agree = judge.label == human_label
        correct += int(agree)
        total += 1
        print(f"{i}: human={human_label} judge={judge.label} {'OK' if agree else 'X'} — {judge.reason}")
    print(f"\nAgreement: {correct}/{total} = {correct/total:.1%}")
```

Run on first 20 traces. Expect 60–80% agreement on the first run — that's normal. Don't be discouraged. Iteration is the point.

### Save the agreement output (15 min)

Copy the terminal output into `judge/judge-v1-run.md` with a note: "v1 agreement: X/20. Disagreement patterns: [3 lines]." This is your iteration log.

### Kata 12 — async LLM calls (30 min, NO AI)

In `katas/kata_12_async_llm.py`, write an async version of `judge_trace` that calls the API concurrently for a list of 10 traces using `asyncio.gather`. Use `anthropic.AsyncAnthropic`.

---

## Friday — Judge v2 + run on all 50 + commit taxonomy (90 min)

### Iterate prompt (45 min)

Read your 4–6 disagreements from Thursday. For each, decide: was the judge wrong, or was the prompt unclear? Add 1–3 concrete clarifications to `judge_v0.md` → save as `judge/judge_v1.md` (note: v1 of the *prompt*, distinct from v1 of the script).

Common clarifications you'll likely need:
- "FAIL means the failure mode applies. PASS means it does not apply. Do not confuse 'good output' with 'PASS for this failure mode.'"
- "If you cannot determine, choose PASS and explain in the critique."
- 1–2 worked examples (one PASS, one FAIL).

### Run on all 50 (30 min)

Update `judge_v1.py` to point at `judge/judge_v1.md`. Run on all 50 traces. Log to `judge/judge-v2-run.md`.

Target: >75% agreement after one iteration. >85% is great. >90% is for Week 4.

### Commit taxonomy (15 min)

`failure-taxonomy.md` is final-ish for the month. Commit explicitly:

```powershell
cd projects/business-classification-pipeline
git add failure-taxonomy.md judge/ data/notes.jsonl
git commit -m "leadlens: taxonomy v1 + judge v1 prompt at X% agreement on 50 traces"
git push
```

---

## Saturday — Disagreement deep-dive + iteration log (90 min)

For every trace where v2 still disagrees with your label, write 2 sentences in `judge/iteration-log.md`:
- Why did the judge land where it did?
- Was the judge right and *your* label wrong? (Happens — re-label if so.)

If 5+ disagreements all share a pattern → that's a Week 4 prompt clarification opportunity.

### Public push: tweet

> "Built first LLM-as-judge on my staffing-firm classifier. v1 of the prompt got 68% agreement with my hand labels. v2 got 81%. Iterating to 90+ next week. Critique shadowing helps more than I expected."

Attach screenshot of agreement output.

---

## Sunday — PROGRESS, plan Week 4, tweet (30 min)

Standard rhythm. Update START_HERE pointer to Week 4. Open [week-4.md](./week-4.md).

---

## Behind if

- `failure-taxonomy.md` not committed by Friday.
- Judge v2 agreement <70% on 50 traces.
- Fewer than 3 katas done.
- No tweet.

## Going faster?

- Start drafting the leadlens `DESIGN.md` (Week 4 deliverable).
- Implement a second judge for one of your other failure modes (e.g. `mixed_boundary_ambiguity`).

# Week 5 — leadlens: Langfuse Tracing + Judge-to-CI + Golden-Set Sourcing

> 📝 **Draft written 2026-06-09, ahead of the just-in-time window.** Refine the weekend before this week starts (2026-06-21) based on your Month 1 close-out outcomes — final judge TNR, anything the blog post surfaced, and whether `failure-taxonomy.md` landed. The daily-plan table is the source of truth; bodies below are guidance.

**Window:** Mon 2026-06-22 → Sun 2026-06-28
**Time budget:** 8–10 hours
**Position:** Month 2, Week 5 of 24

## Why this week matters

Month 1 proved you can *evaluate*. Month 2 proves you can ship a **deployed, observed, eval-instrumented** system — the one sentence that opens every US-remote AI-eng interview ("walk me through a real LLM system you shipped end-to-end with evals").

Week 5 is the foundation for that. Because **leadlens v0.1 already exists** (schema + Instructor runner + judge v1 + cost/latency from Month 1 — see [carry-forward](./README.md#carry-forward--already-shipped-in-month-1-you-finished-ahead-week-5-starts-here-dont-rebuild-it)), this week is **harden + instrument**, not build-from-scratch:

1. **Langfuse tracing on every code path** — so you can show trace screenshots in the README and debug failures by replay, not print statements.
2. **Judge promoted from a markdown prompt → a CI-grade pytest eval** — the artifact that makes "the judge runs in CI" true instead of aspirational.
3. **100-company golden dataset sourced** (not labeled yet) — so Week 6 is pure labeling, not hunting for companies.

**The single must-do:** leadlens runs end-to-end with a Langfuse trace on every call, committed, with one trace screenshot saved to the repo — by Sunday.

## At-a-glance daily plan (weekday-light, weekend-heavy)

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-06-22 | Plan review + **kata 18** (typed `pydantic-settings` config from env vars, no AI) | 15 min |
| Tue eve | 2026-06-23 | **Kata 19** (`asyncio.gather` over 3 fake calls with a per-call `asyncio.timeout`, no AI) | 15 min |
| Wed eve | 2026-06-24 | **Kata 20** (`pytest.mark.parametrize` over 4 golden `(input, expected)` cases, no AI) | 15 min |
| Thu eve | 2026-06-25 | **Kata 21** (refactor: extract the judge call into one typed `def judge(trace) -> JudgeResult`, no AI) | 15 min |
| Fri eve | 2026-06-26 | Skim DLAI *Improving Accuracy of LLM Applications* outline OR rest | 15–30 min |
| **Sat** | 2026-06-27 | **Big build**: wire Langfuse into every leadlens path + port judge v1 prompt into a pytest CI eval + run on the 50 traces | **3.5 hrs** |
| **Sun** | 2026-06-28 | **Big build**: DLAI accuracy course (watch + drill) + source 100-company golden-set candidates (stratified) + PROGRESS + public push | **3.5 hrs** |

Total: ~9 hours. (Katas committed nightly to `katas/` — green-square habit.)

---

## Monday — Langfuse mental model + kata 18 (15 min + light setup)

### Revise (5 min, no build)
Before any tracing code, lock the three Langfuse nouns so the dashboard isn't noise:
- **Trace** = one end-to-end request (one company → one classification).
- **Span** = a step inside it (homepage fetch, web search, LLM call).
- **Generation** = a span that is specifically an LLM call (captures model, prompt, tokens, cost).

Recall test: *"What's the difference between a span and a generation?"* If you can't answer, re-read the Langfuse "concepts" page before Saturday.

### Kata 18 — `pydantic-settings` (no AI)
In `katas/kata_18_settings.py`, write a typed settings class that reads `ANTHROPIC_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` from env with validation. This is the exact pattern leadlens needs Saturday — the kata *is* the prep.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    anthropic_api_key: str
    langfuse_public_key: str
    langfuse_secret_key: str
```

---

## Tuesday–Thursday — katas 19–21 (15 min each, no AI)

Each kata builds muscle you'll use this month:
- **Kata 19** — `asyncio.gather` + `asyncio.timeout`: the shape of enriching N companies concurrently without one hang stalling the batch.
- **Kata 20** — `pytest.mark.parametrize`: the shape of the judge-in-CI eval you write Saturday.
- **Kata 21** — extract `judge(trace) -> JudgeResult`: turn the inline judge call into one typed, testable function. (This refactor *is* step 1 of Saturday's port.)

Log one line per kata in `katas/LEARNINGS.md`. If a kata takes >15 min, that's the signal of where your fluency is still thin — note it.

---

## Saturday — Trace everything + judge-to-CI (3.5 hrs)

### Revise (15 min)
Re-read your `DESIGN.md` §7 (deployment + observability). Restate aloud the cost + latency targets you wrote (<$0.02/classification, p50 <8s). You're about to make them *measurable*, so know the numbers you're aiming at.

### Build A — Langfuse on every path (90 min)
Wire tracing into the leadlens runner. The `@observe()` decorator is the lowest-friction entry point:

```python
from langfuse import observe, get_client

langfuse = get_client()

@observe()                      # creates the trace
def classify_company(name: str, domain: str | None) -> Classification:
    evidence = fetch_evidence(name, domain)   # @observe() this too -> span
    result = run_extraction(evidence)          # @observe() -> generation
    return result
```

> ⚠ Verify the import/decorator names against the **current Langfuse Python SDK docs** — the SDK moved to an OpenTelemetry-based API and the surface changes. The mental model (trace → span → generation) is stable; the exact call may not be.

Acceptance: run leadlens on 3 companies → see 3 traces in the Langfuse dashboard, each with the fetch span + the LLM generation showing token count + cost. Screenshot one trace → save to `projects/business-classification-pipeline/docs/langfuse-trace.png`.

### Build B — judge → pytest CI eval (75 min)
Promote the judge from a prompt you run by hand into a test that fails the build when accuracy regresses. This is the artifact behind "the judge runs in CI."

```python
# tests/test_judge.py
import json, pytest
from pathlib import Path
from leadlens.judge import judge   # the typed fn from kata 21

GOLDEN = [json.loads(l) for l in Path("data/judge-golden.jsonl").read_text().splitlines()]

@pytest.mark.parametrize("case", GOLDEN, ids=[c["id"] for c in GOLDEN])
def test_judge_agrees_with_hand_label(case):
    result = judge(case["trace"])
    assert result.label == case["expected_label"], case["id"]
```

Pull 10–15 hand-labeled traces into `data/judge-golden.jsonl` as the fixture. Run it. Some will fail — that's the point; the gap *is* your remaining calibration work, now visible on every `pytest` run instead of forgotten.

### Recall (15 min)
Explain to me (or aloud): *"Why does an LLM-as-judge belong in CI, and what does it catch that a unit test can't?"* If you can answer in 60 sec, Build B landed.

---

## Sunday — DLAI accuracy course + golden-set sourcing (3.5 hrs)

### Read + drill — DLAI *Improving Accuracy of LLM Applications* (90 min)
Watch with a notebook open. For each technique it covers (prompt iteration, few-shot, eval-driven loops, fine-tuning trade-offs), write one line in `notes/fundamentals.md`: *"this applies to leadlens at ___."* No passive watching — the note is the drill.

Recall: name the course's decision rule for *when fine-tuning beats prompting*. (You almost certainly stay in prompt-land for leadlens — be able to say why.)

### Build — source the 100-company golden dataset (90 min)
You're not labeling yet (that's Week 6) — you're *assembling candidates* so Week 6 is pure judgment, not hunting.

Target stratification (from `DESIGN.md` §5):
- 30 `executive_search`, 30 `general_staffing`, 30 `mixed`, 10 edge cases (closed firms, multi-brand, regional-only).
- Sources: your existing 50 trace inputs + net-new from a Crunchbase/Apollo staffing-firm export (you have these tools at Precise Leads — point them here).
- Commit `data/golden-candidates.csv` with columns: `name, domain, source, provisional_segment_guess, hard_or_easy`. Leave the *real* label blank — that's Week 6.

### Close the week (30 min)
- [PROGRESS.md](../PROGRESS.md): hours, what shipped, what slipped, confidence re-rate, next-week focus.
- **Public push:** tweet the Langfuse trace screenshot — "leadlens now traces every classification: token cost + latency per call, visible." One image, specific, no hype.

---

## Behind if
- leadlens doesn't produce a Langfuse trace per call (the must-do).
- Judge isn't a runnable `pytest` eval (still a copy-paste-the-prompt manual step).
- Fewer than 60 golden-set candidates sourced.
- Two consecutive missed Sunday PROGRESS updates.

These are recoverable in Week 6, but each delays the 100-example labeling that Week 6 depends on.

## Going faster?
- Start hand-labeling the golden candidates (pull Week 6 work forward) — but only after the must-do (tracing) is committed.
- Sketch the Modal endpoint shape: `@modal.fastapi_endpoint` + a Pydantic request body wrapping your `classify_company` input contract. (Week 8 deploy prep.)
- Add a second judge (`evidence_support_quality` from `DESIGN.md` §6) as a second parametrized test.

## Next week
→ `week-6.md` (written the weekend before Week 6): hand-label the 100, first full end-to-end run, confusion matrix v1.

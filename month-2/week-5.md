# Week 5 — leadlens: Langfuse Tracing + Judge-to-CI + Golden-Set Sourcing

> 📝 **Draft written 2026-06-09, ahead of the just-in-time window.** Refine the weekend before this week starts (2026-06-21) based on your Month 1 close-out — final scam-judge TNR, whether `failure-taxonomy.md` landed, anything blog post 1 surfaced. The daily-plan table is the source of truth; bodies are guidance.
>
> **leadlens = AI job-description classifier** (Gemini 2.5 Flash + Instructor). Not the old staffing-firm framing. Canonical spec: [../projects/business-classification-pipeline/DESIGN.md](../projects/business-classification-pipeline/DESIGN.md).

**Window:** Mon 2026-06-22 → Sun 2026-06-28
**Time budget:** 8–10 hours
**Position:** Month 2, Week 5 of 24

## Why this week matters

Month 1 proved you can *evaluate*. Month 2 proves you can ship a **deployed, observed, eval-instrumented** system — the one sentence that opens every US-remote AI-eng interview ("walk me through a real LLM system you shipped end-to-end with evals").

Week 5 is the foundation. Because **leadlens v0.1 already exists** (schema + Instructor runner + scam judge + cost/latency on 20 JDs — see [carry-forward](./README.md#carry-forward--already-shipped-in-month-1-you-finished-ahead-week-5-starts-here-dont-rebuild-it)), this week is **harden + instrument**, not build-from-scratch:

1. **Langfuse tracing on every model call** — replaces the hand-rolled `jd-metrics.jsonl`; gives you trace screenshots for the README and replay-debugging instead of print statements.
2. **Scam judge promoted from a script → a CI-grade pytest eval** — makes "the judge runs in CI" true, asserting on **TPR/TNR** (not raw agreement — class imbalance makes raw misleading).
3. **100-JD golden dataset sourced** (not labeled yet) — so Week 6 is pure labeling, not hunting for postings.

**The single must-do:** leadlens runs end-to-end with a Langfuse trace on every classify + judge call, committed, with one trace screenshot in the repo — by Sunday.

## At-a-glance daily plan (weekday-light, weekend-heavy)

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-06-22 | Plan review + **kata 18** (typed `pydantic-settings` config from env vars, no AI) | 15 min |
| Tue eve | 2026-06-23 | **Kata 19** (`asyncio.gather` over 3 fake calls with `asyncio.timeout`, no AI) | 15 min |
| Wed eve | 2026-06-24 | **LeetCode ×1** (arrays/hash-map, e.g. Two Sum / Group Anagrams) — commit to `dsa/` | 20 min |
| Thu eve | 2026-06-25 | **LeetCode ×1** (strings, e.g. Valid Anagram / Longest Substring) — commit to `dsa/` | 20 min |
| Fri eve | 2026-06-26 | Skim DLAI *Building Evaluations of LLM Apps* outline OR rest | 15–30 min |
| **Sat** | 2026-06-27 | **Big build**: wire Langfuse into every leadlens call + port `judge_v1.py` into a pytest CI eval asserting TPR/TNR on a JD fixture | **3.5 hrs** |
| **Sun** | 2026-06-28 | **Big build**: DLAI evals course (watch + drill) + source 100-JD golden candidates (stratified) + PROGRESS + public push | **3.5 hrs** |

Total: ~9 hours. (Reps committed nightly — green-square habit. Per the Month-2 DSA rule, 2 of the weekday slots are now LeetCode, not katas.)

---

## Monday — Langfuse mental model + kata 18 (15 min + light setup)

### Revise (5 min, no build)
Lock the three Langfuse nouns so the dashboard isn't noise:
- **Trace** = one end-to-end request (one JD → one classification, optionally + judge).
- **Span** = a step inside it (the Instructor call; the judge call).
- **Generation** = a span that is specifically an LLM call (captures model, prompt, tokens, cost).

Recall: *"What's the difference between a span and a generation?"*

### Kata 18 — `pydantic-settings` (no AI)
`katas/kata_18_settings.py` — a typed settings class reading `GEMINI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` from env with validation. This is the exact config leadlens needs Saturday — the kata *is* the prep.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    gemini_api_key: str
    langfuse_public_key: str
    langfuse_secret_key: str
```

---

## Tue / Wed / Thu — kata 19 + 2 LeetCode (15–20 min each, no AI)

- **Kata 19** — `asyncio.gather` + `asyncio.timeout`: the shape of classifying N JDs concurrently to kill the ~5.4 s/JD serial latency (DESIGN §6, the v0.2 fix).
- **LeetCode ×2** — start the 60–80-problem arc (Month 2 DSA rule). This week: 1 array/hash-map + 1 string. Commit each to `dsa/` with a one-line "what pattern" comment. No AI — these are interview reps.

Log one line per rep in `katas/LEARNINGS.md`.

---

## Saturday — Trace everything + judge-to-CI (3.5 hrs)

### Revise (15 min)
Re-read `DESIGN.md` §6 (metrics + thresholds). Restate aloud: category-accuracy target (≥75%), judge targets (TPR ≥0.75 / TNR ≥0.90), cost ($0.00085/JD), latency (~5.4 s serial). You're about to make these *observable*.

### Build A — Langfuse on every call (90 min)
Wire tracing into the classifier + judge. The `@observe()` decorator is the lowest-friction entry:

```python
from langfuse import observe, get_client
langfuse = get_client()

@observe()                       # the trace
def classify_jd(jd: dict) -> Classification:   # Classification = your leadlens_v01 schema
    return run_instructor(jd)    # the generation: model, tokens, cost captured

@observe()
def judge_scam(jd: dict, result: Classification) -> JudgeResult:
    ...
```

> ⚠ Verify import/decorator names against the **current Langfuse Python SDK docs** — the SDK moved to an OpenTelemetry base and the call surface changes. The trace→span→generation model is stable; the exact API may not be. (If Instructor wraps the Gemini client, check the Langfuse–Instructor/OpenAI-compat integration for auto-capture of token+cost.)

Acceptance: run leadlens on 3 JDs → 3 traces in Langfuse, each showing the classify generation (tokens + cost) and, for flagged ones, the judge span. Screenshot one → `projects/business-classification-pipeline/docs/langfuse-trace.png`.

### Build B — scam judge → pytest CI eval (75 min)
Promote `judge_v1.py` from a script you run by hand into a test that fails the build when calibration regresses.

```python
# tests/test_judge.py
import json, pytest
from pathlib import Path
from leadlens.judge_v1 import judge_scam   # your existing judge

GOLD = [json.loads(l) for l in Path("data/judge-golden.jsonl").read_text().splitlines()]

def test_scam_judge_calibration():
    tp = fp = tn = fn = 0
    for case in GOLD:                       # case: {jd, classification, expected_is_scam}
        pred = judge_scam(case["jd"], case["classification"]).is_scam
        exp = case["expected_is_scam"]
        tp += pred and exp;  fp += pred and not exp
        tn += (not pred) and (not exp);  fn += (not pred) and exp
    tpr = tp / (tp + fn);  tnr = tn / (tn + fp)
    assert tpr >= 0.75, f"TPR {tpr}"        # catch scams
    assert tnr >= 0.90, f"TNR {tnr}"        # don't flag real roles
```

Use your 20-JD golden set (3 positives) as the fixture. It may fail at TNR 0.882 — that's the point; the gap is visible on every `pytest` run instead of forgotten. (Closing it to ≥0.90 is Week 7; few-shot MIIGO/Sumble per DESIGN §9.)

### Recall (15 min)
Explain aloud: *"Why calibrate this judge on TPR/TNR instead of accuracy, given 3/20 positives?"* (Answer: an always-"not scam" baseline scores 0.85 accuracy while catching zero scams — accuracy hides the failure the judge exists to catch.)

---

## Sunday — DLAI evals course + golden-set sourcing (3.5 hrs)

### Read + drill — DLAI *Building Evaluations of LLM Apps* (90 min)
Watch with a notebook open. For each technique, write one line in `notes/fundamentals.md`: *"this applies to leadlens at ___."* The note is the drill — no passive watching.

### Build — source the 100-JD golden dataset (90 min)
Not labeling (that's Week 6) — *assembling candidates* so Week 6 is pure judgment.

Stratify across `ai_authenticity` so every category and the edge cases are represented:
- real_ai_role, ai_adjacent, ai_washed, non_ai — plus deliberate edge cases (scam/partnership posts, vague-but-real-product like the MIIGO archetype, seniority-mismatch).
- Sources: scrape real postings from **HN "Who is Hiring", Wellfound, YC Work-at-a-Startup** (you have the scraping muscle from Precise Leads — point it here; this also seeds your Month-6 funnel list).
- Commit `data/golden-candidates.jsonl`: `id, title, company, url, location, description, provisional_category, is_edge_case`. Leave the *confirmed* label for Week 6.

### Close the week (30 min)
- [PROGRESS.md](../PROGRESS.md): hours, shipped, slipped, confidence re-rate, next-week focus.
- **Public push:** tweet the Langfuse trace screenshot — "leadlens now traces every JD classification: token cost + latency per call, visible." One image, specific, no hype.

---

## Behind if
- leadlens doesn't produce a Langfuse trace per call (the must-do).
- Scam judge isn't a runnable `pytest` eval asserting TPR/TNR.
- Fewer than 60 golden-JD candidates sourced.
- Two consecutive missed Sunday PROGRESS updates.

## Going faster?
- Start confirming labels on the golden candidates (pull Week 6 forward) — only after the must-do (tracing) is committed.
- Sketch the Modal endpoint: `@modal.fastapi_endpoint` + a Pydantic request body wrapping the JD input contract (Week 8 deploy prep).
- Implement the `asyncio.gather` batch from kata 19 in the real runner — turn ~5.4 s/JD serial into a concurrent batch.

## Next week
→ [week-6.md](./week-6.md) (written the weekend before Week 6): hand-label the 100 JDs, first full end-to-end run, confusion matrix v1 + per-category breakdown.

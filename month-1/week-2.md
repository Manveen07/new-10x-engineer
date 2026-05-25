# Week 2 — Open-Code All 50 Traces with Three Gulfs

**Window:** Mon 2026-06-01 → Sun 2026-06-07
**Time budget:** 8–10 hours
**Position:** Month 1, Week 2 of 24

## Why this week matters

You have 50 real staffing-firm classifier traces. This week you look at every one and write a one-line note about what's right or wrong. This is **open coding** — the foundational eval skill that hiring managers screen for in the first 90 seconds of any eval-flavored interview. Most fresher AI engineering candidates have never done this. You will.

The **Three Gulfs framework** (Hamel Husain & Shreya Shankar) gives you the categories:
- **Specification gulf** — the prompt is unclear or underspecified for this case.
- **Generalization gulf** — the model can't handle this kind of input even with a better prompt.
- **Comprehension gulf** — you don't yet understand what "good output" looks like for this case.

**The single must-do:** every one of the 50 traces gets a one-line note by Saturday night. Volume + honesty beat perfectionism.

## At-a-glance daily plan (weekday-light, weekend-heavy)

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-06-01 | Plan review + **kata 6** (JSONL reader, no AI) | 15 min |
| Tue eve | 2026-06-02 | **Kata 7** (dataclass + `__post_init__`, no AI) | 15 min |
| Wed eve | 2026-06-03 | **Kata 8** (generator expr vs list comp, no AI) | 15 min |
| Thu eve | 2026-06-04 | **Kata 9** (Path operations + summary script, no AI) | 15 min |
| Fri eve | 2026-06-05 | Skim one post (Hamel / Eugene / Latent Space) OR rest | 15 min |
| **Sat** | 2026-06-06 | **Big build block**: build annotation viewer (Streamlit, ~1 hr) + open-code traces 1–25 (~2.5 hrs) | **3.5 hrs** |
| **Sun** | 2026-06-07 | **Big block**: read Eugene Yan LLM patterns (~1.5 hr) + open-code traces 26–50 (~1.5 hr) + Saturday-style cluster flag + tweet + PROGRESS update | **3.5 hrs** |

Total: ~9 hours.

**Note:** the body sections below were drafted with the old weeknight-heavy cadence and will be rewritten the weekend before Week 2 starts. For now, the daily-plan table above is the source of truth.

---

## Monday — Annotation viewer + kata 6 (90 min)

**Goal:** A simple Streamlit page that shows one trace at a time + a text box for your note + save-to-disk. Then your first kata of the week.

### Build the annotation viewer (60 min)

Why build instead of using a spreadsheet? Because (a) shipping a Streamlit app counts as a portfolio artifact later, (b) it teaches you to consume your own JSONL data, (c) it's a 60-min build you'll use 100 times this month.

In `projects/business-classification-pipeline/`:

```powershell
cd "C:\Users\Manveen\Desktop\new_things_to_mess_araound\new 10x engineer\projects\business-classification-pipeline"
uv init . --no-pin-python
uv add streamlit pydantic
```

Create `annotator.py`:

```python
"""Streamlit trace annotator. Reads JSONL traces, writes notes JSONL."""
import json
from pathlib import Path
import streamlit as st

TRACES = Path("data/traces-week-1.jsonl")
NOTES = Path("data/notes.jsonl")

@st.cache_data
def load_traces() -> list[dict]:
    return [json.loads(line) for line in TRACES.read_text().splitlines()]

def load_notes() -> dict[int, dict]:
    if not NOTES.exists():
        return {}
    return {json.loads(line)["idx"]: json.loads(line) for line in NOTES.read_text().splitlines()}

def save_note(idx: int, note: str, gulf: str, label: str) -> None:
    existing = load_notes()
    existing[idx] = {"idx": idx, "note": note, "gulf": gulf, "label": label}
    NOTES.write_text("\n".join(json.dumps(v) for v in existing.values()))

traces = load_traces()
notes = load_notes()

st.title("leadlens trace annotator")
idx = st.number_input("Trace #", 0, len(traces) - 1, 0)
st.json(traces[idx])

existing = notes.get(idx, {})
note = st.text_area("One-line note (what's right or wrong?)", existing.get("note", ""))
gulf = st.selectbox("Gulf", ["specification", "generalization", "comprehension", "n/a"],
                    index=["specification", "generalization", "comprehension", "n/a"].index(existing.get("gulf", "n/a")))
label = st.selectbox("Pass/fail/ambiguous", ["pass", "fail", "ambiguous"],
                     index=["pass", "fail", "ambiguous"].index(existing.get("label", "ambiguous")))

if st.button("Save"):
    save_note(idx, note, gulf, label)
    st.success(f"Saved trace {idx}")

st.divider()
st.metric("Traces annotated", f"{len(notes)} / {len(traces)}")
```

Run:
```powershell
uv run streamlit run annotator.py
```

**Done when:** you can navigate traces 0..49, type a note, save, and see the count update.

### Kata 6 — JSONL reader + writer (30 min, NO AI)

In `katas/kata_06_jsonl.py`, without AI:

```python
from pathlib import Path

def read_jsonl(path: Path) -> list[dict]:
    ...

def write_jsonl(path: Path, items: list[dict]) -> None:
    ...

def append_jsonl(path: Path, item: dict) -> None:
    ...
```

Plus three tests. Use the JSONL file from your traces as test fixture.

---

## Tuesday — Open-code traces 1–15 + kata 7 (90 min)

**Goal:** First 15 traces have a note + a gulf label + a pass/fail/ambiguous label.

### Open-code (60 min)

Open the annotator (`uv run streamlit run annotator.py`). For each trace 0..14:

- Read input + model output carefully.
- In one line, say what's right or wrong. Be specific: "model labels `mixed` but evidence string only mentions executive search — false_executive_search_signal." Not: "looks wrong."
- Pick the gulf: spec / generalization / comprehension / n/a.
- Pick label: pass / fail / ambiguous.

Some patterns will already emerge by trace 5. Resist naming categories yet — that's Week 3's axial coding. For now: just describe what you see.

**Honest target:** ~3 min/trace. 15 traces in ~45 min. Speed matters; perfectionism hurts.

### Kata 7 — dataclass with `__post_init__` (30 min, NO AI)

In `katas/kata_07_dataclass.py`:

```python
from dataclasses import dataclass

@dataclass
class TraceNote:
    idx: int
    note: str
    gulf: str  # validate in __post_init__: one of {"specification","generalization","comprehension","n/a"}
    label: str  # validate: one of {"pass","fail","ambiguous"}
```

Raise `ValueError` for invalid values. Test with 3 tests (1 valid, 2 invalid).

---

## Wednesday — Eugene Yan LLM patterns (90 min)

**Goal:** End-to-end read of [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/). With your in-progress notes file open.

### Read

The post covers seven patterns: Evals, RAG, Fine-tuning, Caching, Guardrails, Defensive UX, Collect feedback. For this week, focus on **Evals** and **Defensive UX**.

After each section, write one sentence in `notes/week-2-eugene-yan-notes.md`: "this changes X about my leadlens design."

### Mini-build (15 min at end)

Add one **Guardrail** to your kata 1 `parse_company()`: if `confidence` for any signal is `> 0.95` but the `evidence` string is shorter than 20 characters, raise a warning (don't fail). This is a real failure mode you spotted in your Saturday notes ("confidence values that look hardcoded at 0.95").

---

## Thursday — Open-code traces 16–30 + kata 8 (90 min)

Same pattern as Tuesday. By end of day: traces 0..29 annotated.

### Kata 8 — generator expression vs list comprehension (30 min, NO AI)

In `katas/kata_08_gen.py`:

```python
from collections.abc import Iterator

def passing_traces(notes: list[dict]) -> list[dict]:
    """Return notes where label == 'pass'."""
    ...

def passing_traces_lazy(notes: list[dict]) -> Iterator[dict]:
    """Same but as a generator. Use when notes might be 100k+."""
    ...
```

Write a test that asserts both return the same items but `passing_traces_lazy` doesn't materialize a list (check via `sys.getsizeof` or just by type).

---

## Friday — Open-code traces 31–50 + kata 9 (2 hrs)

Finish all 50. By end of Friday: every trace has a note + gulf + label saved in `notes.jsonl`.

If a trace stumps you, mark `label: ambiguous` and move on. The point is coverage, not perfection.

### Kata 9 — Path operations + a real script (30 min, NO AI)

In `katas/kata_09_paths.py`, write a script that:
1. Reads `data/notes.jsonl`
2. Prints a small summary: total / passing / failing / ambiguous, plus gulf distribution
3. Writes a CSV version to `data/notes.csv` (use `csv` stdlib, not pandas — exercise the stdlib)

This script is *actually useful* — you'll run it Saturday to see your week's data.

---

## Saturday — Re-read all 50 notes, flag clusters (90 min)

**Goal:** Spot 3–5 recurring patterns ("clusters") without naming them yet.

### Process

1. Run kata 9: `uv run python katas/kata_09_paths.py`. Look at the gulf distribution + pass/fail ratio. Write the numbers in `notes/week-2-saturday.md`.
2. Open the annotator and skim all 50 notes back-to-back (30 min).
3. In `notes/week-2-saturday.md`, write 3–5 lines like:
   - "Pattern: short evidence string + high confidence → mostly fail. Spotted in traces 3, 7, 14, 22, 38."
   - "Pattern: firms with `International` in name → often mislabeled. Traces 12, 19, 33."

Don't name these patterns yet — Week 3 is axial coding where you'll formalize them into a taxonomy.

### Public push: short tweet

> "Open-coded 50 LLM classifier traces this week. 3 gulfs, 50 one-line notes, 4 emerging failure patterns. Writing them up properly next week."

Attach a screenshot of the annotator or the gulf-distribution output from kata 9.

---

## Sunday — PROGRESS, plan Week 3, tweet (30 min)

1. Fill [PROGRESS.md](../PROGRESS.md) Week 2.
2. Update [START_HERE.md](../START_HERE.md) pointer to Week 3.
3. Open [week-3.md](./week-3.md), copy goals to sticky note.

---

## Behind if

- Fewer than 40 traces annotated by Sunday.
- Annotation viewer doesn't run.
- Eugene Yan post not finished.
- Fewer than 3 katas done.
- No Saturday tweet.

If any: recover Monday/Tuesday of Week 3, then continue.

## Going faster?

- Read Hamel's *A Field Guide to Rapidly Improving AI Products* and write 1 paragraph on Three Gulfs in your own words. Useful for the blog post.
- Sketch the failure taxonomy in `failure-taxonomy.md` (Week 3 work) — but only if all 50 traces are annotated *and* katas are done.

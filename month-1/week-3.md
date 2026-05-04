# Week 3 — Failure Taxonomy and Annotation Viewer

**Window:** Mon 2026-05-18 → Sun 2026-05-24
**Time budget:** 8 hours
**Position in plan:** Month 1, Week 3 of 24

## Why this week matters

Open-coding notes are useful but unstructured. This week you turn them into a **failure taxonomy** — a named, finite list of failure modes (typically 4–7 categories). The taxonomy is what you build LLM-as-judge prompts against next week. Without it, the judge has nothing to score.

You also build a tiny annotation viewer this week. The point is not engineering polish — it's iteration speed. Hamel's reported number: teams with custom annotation viewers iterate ~10× faster than teams scrolling JSON.

## Daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon | 2026-05-19 | Read all 50 trace notes again; do axial coding: cluster the open codes into 4–7 named categories | 90 min |
| Tue | 2026-05-20 | Write the taxonomy as a markdown file: name + definition + 2 example trace IDs per category | 60 min |
| Wed | 2026-05-21 | Read Hamel `llm-judge` post end-to-end | 60 min |
| Thu | 2026-05-22 | Annotation viewer scaffold: Streamlit or FastHTML, list view + detail view, no styling | 90 min |
| Fri | 2026-05-23 | Annotation viewer polish: add the taxonomy as a dropdown, persist tag selections to JSONL | 90 min |
| Sat | 2026-05-24 | Re-tag all 50 traces using the viewer with the taxonomy categories — should take <60 min if Friday went well | 90 min |
| Sun | 2026-05-25 | Update `PROGRESS.md`; plan Week 4 | 30 min |

Total: ~8 hours.

## Axial coding guideline

Axial coding = grouping open codes into named categories. Rules:

- **4–7 categories total.** More than 7 means your buckets aren't carrying weight; fewer than 4 means you're hand-waving.
- **Each category gets a one-line definition** that anyone could apply consistently.
- **Each category gets 2 example trace IDs** so future-you (or a hiring manager) can sanity-check it.
- **One special bucket: "ok" or "no_failure".** Most of your traces will land here — that's fine. Don't force failures.

Example taxonomy for a winery classifier:

```
1. hallucinated_address — model invented a location not in the source. e.g. trace_023, trace_041
2. stale_evidence — used cached or pre-2024 web data and called it current. e.g. trace_007, trace_019
3. multilingual_confusion — site is non-English, model assumed English and got it wrong. e.g. trace_034
4. confident_wrong_entity — confused two businesses with similar names. e.g. trace_012, trace_038
5. underspecified_input — prompt didn't define how to handle parent/subsidiary cases. e.g. trace_031
6. ok — output is correct or correctly hedged. e.g. trace_001, trace_005, ...
```

## Annotation viewer — minimum viable

```python
# viewer.py — Streamlit, ~30 lines
import streamlit as st, json, pathlib

TRACES_PATH = pathlib.Path("projects/business-classification-pipeline/data/traces-week-1.jsonl")
TAXONOMY = ["ok", "hallucinated_address", "stale_evidence", "multilingual_confusion",
            "confident_wrong_entity", "underspecified_input"]

def load(): return [json.loads(line) for line in TRACES_PATH.read_text().splitlines() if line]
def save(data):
    TRACES_PATH.write_text("\n".join(json.dumps(t) for t in data))

traces = load()
idx = st.number_input("trace #", 0, len(traces)-1, 0)
t = traces[idx]
st.json(t)
new_tag = st.selectbox("category", TAXONOMY, index=TAXONOMY.index(t.get("category", "ok")))
notes = st.text_area("note", value=t.get("note", ""))
if st.button("save"):
    t["category"] = new_tag
    t["note"] = notes
    save(traces)
    st.success("saved")
```

Run with `streamlit run viewer.py`. That's the whole tool.

## Resources used this week

- [hamel.dev/blog/posts/llm-judge](https://hamel.dev/blog/posts/llm-judge/) — Wednesday reading, sets up Week 4.
- Streamlit docs ([docs.streamlit.io](https://docs.streamlit.io/)) — only if Streamlit is new to you, otherwise skip.

## Deliverable checklist

- [ ] `projects/business-classification-pipeline/docs/failure-taxonomy.md` exists with 4–7 named categories, definitions, examples.
- [ ] `viewer.py` runs locally and shows trace data.
- [ ] All 50 traces tagged with one taxonomy category (saved to JSONL).
- [ ] Hamel `llm-judge` post read.
- [ ] `PROGRESS.md` Week 3 block filled in.

## Behind if

- Taxonomy has 1, 2, or more than 8 categories.
- The viewer doesn't run.
- Fewer than 50 traces have a category tag.

## What unlocks next week

Week 4 builds an LLM-as-judge that scores classifier outputs against this taxonomy. Without the taxonomy, the judge has no target. Without the JSONL category labels, the judge has nothing to be calibrated against.

## Next file

→ [week-4.md](./week-4.md) — calibrated LLM-as-judge and Project 1 design doc.

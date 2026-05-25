"""Streamlit trace annotator for leadlens.

Reads `data/traces-week-1.jsonl`, shows one trace at a time, lets you
write a note + tag a Three-Gulfs gulf + binary label, saves to
`data/notes.jsonl`. Re-runs are idempotent — re-opens to last saved state.
"""

import json
from pathlib import Path

import streamlit as st

TRACES = Path("data/traces-week-1.jsonl")
NOTES = Path("data/notes.jsonl")

GULFS = ["specification", "generalization", "comprehension", "n/a"]
LABELS = ["pass", "fail", "ambiguous"]


def load_traces() -> list[dict]:
    return [
        json.loads(line)
        for line in TRACES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_notes() -> dict[int, dict]:
    if not NOTES.exists():
        return {}
    return {
        json.loads(line)["idx"]: json.loads(line)
        for line in NOTES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def save_note(idx: int, note: str, gulf: str, label: str) -> None:
    existing = load_notes()
    existing[idx] = {"idx": idx, "note": note, "gulf": gulf, "label": label}
    NOTES.write_text(
        "\n".join(
            json.dumps(v) for v in sorted(existing.values(), key=lambda x: x["idx"])
        ),
        encoding="utf-8",
    )


def main() -> None:
    st.set_page_config(page_title="leadlens annotator", layout="wide")
    st.title("leadlens — trace annotator")

    traces = load_traces()
    notes = load_notes()

    st.metric("Annotated", f"{len(notes)} / {len(traces)}")

    idx = st.number_input(
        "Trace #", min_value=0, max_value=len(traces) - 1, value=0, step=1
    )
    trace = traces[idx]

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.subheader(f"Trace {idx}")
        st.json(trace)
    with col_right:
        existing = notes.get(idx, {})
        st.subheader("Annotation")
        note = st.text_area(
            "One-line note (what's right or wrong?)",
            value=existing.get("note", ""),
            height=150,
        )
        gulf = st.selectbox(
            "Gulf", GULFS, index=GULFS.index(existing.get("gulf", "n/a"))
        )
        label = st.selectbox(
            "Label", LABELS, index=LABELS.index(existing.get("label", "ambiguous"))
        )

        if st.button("Save", type="primary"):
            save_note(idx, note, gulf, label)
            st.success(f"Saved trace {idx}")
            st.rerun()


if __name__ == "__main__":
    main()

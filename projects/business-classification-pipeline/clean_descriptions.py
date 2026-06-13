"""Strip label-leaking editorial sentences from golden-set descriptions.

The golden JDs were hand-written with meta-commentary baked into the
`description` field ("Judge must catch this", "Non-AI control", "tests
whether...", "Edge case: ...", references to Manveen). That LEAKS the label
into the model's input — the judge/classifier reads the hint instead of
judging a raw posting, inflating accuracy.

Fix: descriptions should contain ONLY what a real job posting says. The
editorial meta belongs in expected_category / is_edge_case (the label side),
never the input side.

This drops any sentence containing a leak marker. Reads golden-jds.jsonl,
writes golden-jds-clean.jsonl, prints before/after samples.

Run once:  uv run python clean_descriptions.py
"""

import json
import re
from pathlib import Path

SRC = Path("data/golden-jds.jsonl")
OUT = Path("data/golden-jds-clean.jsonl")

# A sentence is dropped if it contains any of these (case-insensitive).
LEAK_MARKERS = [
    "edge case",
    "non-ai control",
    "control to",
    "control in",
    "control;",
    "control,",
    "balance the negative",
    "negative class",
    "negative-fit",
    "good negative",
    "tests whether",
    "tests the",
    "test the",
    "testing the",
    "distractor",
    "judge must",
    "judge should",
    "classic ai-washed",
    "classic scam",
    "textbook scam",
    "textbook ai-washed",
    "manveen",
    "soft red flag",
    "useful for testing",
    "close to",
    "strong fit",
    "boundary case",
    "sits on the",
    "sits between",
    "analyst-vs-engineer",
    "data-eng-near-ai",
    "ai engineering role.",  # trailing meta like "tests whether X reads as an AI role"
    "reads as",
    "poor fit",
    "negative-fit test",
]


def clean(desc: str) -> str:
    # split into sentences on ". " keeping it simple
    parts = re.split(r"(?<=[.!])\s+", desc)
    kept = []
    for s in parts:
        low = s.lower()
        if any(m in low for m in LEAK_MARKERS):
            continue
        kept.append(s)
    return " ".join(kept).strip()


def main() -> None:
    rows = [
        json.loads(line)
        for line in SRC.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    cleaned = []
    shown = 0
    for jd in rows:
        before = jd["description"]
        after = clean(before)
        jd["description"] = after
        cleaned.append(jd)
        if before != after and shown < 6:
            print(f"--- {jd['id']} {jd['company']} ---")
            print(f"BEFORE: {before}")
            print(f"AFTER:  {after}\n")
            shown += 1

    OUT.write_text("\n".join(json.dumps(jd) for jd in cleaned), encoding="utf-8")
    changed = sum(1 for jd, orig in zip(cleaned, rows))  # noqa
    n_changed = sum(
        1
        for orig_line, jd in zip(SRC.read_text(encoding="utf-8").splitlines(), cleaned)
        if json.loads(orig_line)["description"] != jd["description"]
    )
    print(f"Cleaned {n_changed}/{len(rows)} descriptions -> {OUT.name}")
    # flag any that got suspiciously short
    short = [jd["id"] for jd in cleaned if len(jd["description"]) < 40]
    if short:
        print(f"WARNING - very short after cleaning (review): {short}")


if __name__ == "__main__":
    main()

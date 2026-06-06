"""Filter remaining traces (22..49) for interesting cases worth hand-annotating.

After 22/22 clean passes, marginal value of reading every trace = near zero.
Stratified sample: surface traces that break the established pattern.

Interesting criteria (any one fires):
  - output.status != ground_truth                                (real disagreement)
  - confidence != 0.95                                            (variance from default)
  - len(evidence text) < 30                                       (thin-evidence pattern)
  - notes contain boundary markers ("however", "but", "despite")  (judgment ambiguity)

Non-interesting traces get auto-tagged as `same pattern` so notes.jsonl is complete
without 28 redundant hand-saves.
"""

import json
from pathlib import Path

TRACES = Path("data/traces-week-1.jsonl")
NOTES = Path("data/notes.jsonl")
START_IDX = 22  # already hand-annotated 0..21


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


def is_interesting(t: dict) -> tuple[bool, list[str]]:
    reasons = []
    if t["output"]["status"] != t["ground_truth"]:
        reasons.append("DISAGREEMENT")
    if t["output"]["confidence"] != 0.95:
        reasons.append(f"confidence={t['output']['confidence']}")
    evidence_text = " ".join(t["output"].get("evidence", []))
    if len(evidence_text) < 30:
        reasons.append(f"thin-evidence ({len(evidence_text)} chars)")
    notes = t.get("notes", "").lower()
    for marker in ("however", "but ", "despite", "although"):
        if marker in notes:
            reasons.append(f"boundary-marker: {marker.strip()}")
            break
    return (bool(reasons), reasons)


def main() -> None:
    traces = load_traces()
    notes = load_notes()

    interesting_traces = []
    auto_tag_count = 0

    for idx in range(START_IDX, len(traces)):
        t = traces[idx]
        flag, reasons = is_interesting(t)
        if flag:
            interesting_traces.append((idx, t, reasons))
        else:
            notes[idx] = {
                "idx": idx,
                "note": "Same pattern as traces 0-21: clean classification, 0.95 default confidence, evidence supports label. No new failure mode.",
                "gulf": "n/a",
                "label": "pass",
                "auto_tagged": True,
            }
            auto_tag_count += 1

    NOTES.write_text(
        "\n".join(
            json.dumps(v) for v in sorted(notes.values(), key=lambda x: x["idx"])
        ),
        encoding="utf-8",
    )

    print(f"Auto-tagged {auto_tag_count} traces as 'same pattern'.")
    print(f"Interesting traces needing hand annotation: {len(interesting_traces)}")
    print()
    for idx, t, reasons in interesting_traces:
        print(f"  idx={idx} id={t['id']} name={t['input']['company_name']!r}")
        print(f"    reasons: {', '.join(reasons)}")


if __name__ == "__main__":
    main()

"""Bulk-save the 28 hand-annotated notes from the calibration pairing session.

Preserves existing entries in notes.jsonl (the 22 auto-tagged from filter_traces.py),
merges in the 22 + 6 = 28 hand annotations from the chat transcript.

Run once. Idempotent — re-running overwrites same idx entries cleanly.
"""

import json
from pathlib import Path

NOTES = Path("data/notes.jsonl")

HAND_ANNOTATIONS: list[dict] = [
    {
        "idx": 0,
        "note": "Correct label. Evidence string quotes both 'executive search' and 'contract staffing' — justifies mixed. Confidence 0.95 may be default (Sat-1 pattern).",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 1,
        "note": "Correct general_staffing label. Evidence lists 'temporary, contract, temp-to-direct, direct-hire' — all general staffing vocab, no exec search language. Confidence 0.95 — third trace at this exact value, hardcoded pattern continuing.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 2,
        "note": "Strong pass. Evidence cites placement function, not just keyword.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 3,
        "note": "Pass. Evidence quotes both segments verbatim.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 4,
        "note": "Pass. Model resisted false_executive_search keyword bait — strong other signals (IT/eng/mfg + contract). Contrast case for Sat-1 failure mode F-001.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 5,
        "note": "Pass. Industry-specific exec search firm. Evidence explicit.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 6,
        "note": "Pass. Clean general staffing vocab, no exec signals.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 7,
        "note": "Pass label. Evidence string thin — only 2 short phrases captured; richer signal exists per notes. Flag: thin-evidence pattern.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 8,
        "note": "Pass. Second contrast case — model resisted exec search keyword bait. Strong general staffing signals dominated.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 9,
        "note": "Pass. Clean mixed — both segments quoted explicitly.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 10,
        "note": "Pass on label match, but mixed_boundary_ambiguity (F-002) visible — firm leans general, rule forces 'mixed' because schema lacks segment_strength. Schema-level Specification gulf.",
        "gulf": "specification",
        "label": "pass",
    },
    {
        "idx": 11,
        "note": "Pass. Mixed cleanly justified. Industry niche (medical) doesn't change segmentation.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 12,
        "note": "Pass. Mixed cleanly justified — broad function scope + exec mention.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 13,
        "note": "Pass. Thin-evidence pattern again — niche correct, fuller signal in notes not captured. Second instance.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 14,
        "note": "Pass. Both segments quoted explicitly.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 15,
        "note": "Pass. Inverse of F-002 — model resisted mixed-collapse despite mid-level mention, correctly chose exec_search based on dominant focus.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 16,
        "note": "Pass. Third F-001 resistance case — 'retainer search' present but main work (light industrial) dominated. Model's discriminator working.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 17,
        "note": "Pass. Multi-mode staffing for creative niche. No exec signals.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 18,
        "note": "Pass. Both segments quoted; multi-mode staffing + exec search.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 19,
        "note": "Pass. Clean mixed — both segments + role-level range from C-suite to entry-level.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 20,
        "note": "Pass. Clean mixed — temp + direct + exec search all named.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 21,
        "note": "Pass. Clean general staffing — no exec signals at all.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 22,
        "note": "Pass. Thin-evidence 3rd instance — full operation in notes not surfaced.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 24,
        "note": "Pass. F-001 resistance #4 — model correctly dismissed exec-search keyword in favor of general staffing description.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 32,
        "note": "Pass on label, but borderline. Thin evidence 4th instance + missed senior-accounting component (Controllers/CFO permanent placements). Quiet F-002-inverse — model under-called exec presence.",
        "gulf": "specification",
        "label": "ambiguous",
    },
    {
        "idx": 34,
        "note": "Pass. Clean mixed — both segments explicit. Filter false-positive (boundary marker was connective).",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 47,
        "note": "Pass. Clean mixed — explicit entry-to-exec range. Filter false-positive.",
        "gulf": "n/a",
        "label": "pass",
    },
    {
        "idx": 49,
        "note": "Pass. F-001 resistance #5 — keyword vs description discrimination working.",
        "gulf": "n/a",
        "label": "pass",
    },
]


def load_existing() -> dict[int, dict]:
    if not NOTES.exists():
        return {}
    return {
        json.loads(line)["idx"]: json.loads(line)
        for line in NOTES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def main() -> None:
    existing = load_existing()
    print(f"Existing notes: {len(existing)}")

    for entry in HAND_ANNOTATIONS:
        existing[entry["idx"]] = entry

    NOTES.write_text(
        "\n".join(
            json.dumps(v) for v in sorted(existing.values(), key=lambda x: x["idx"])
        ),
        encoding="utf-8",
    )

    print(f"After merge: {len(existing)} notes (target: 50)")
    if len(existing) == 50:
        print("OK — all 50 traces annotated.")
    else:
        missing = sorted(set(range(50)) - existing.keys())
        print(f"WARNING — missing idx: {missing}")


if __name__ == "__main__":
    main()

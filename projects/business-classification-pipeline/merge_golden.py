"""Merge all JD sources into one deduped, renumbered golden set.

Sources (priority order — earlier wins on a dedup conflict so the newest,
best-labeled set takes precedence):
  1. golden-jds.jsonl        (the 40 hand-sourced India-market JDs — priority)
  2. jds-v0-expansion.jsonl  (Sarvam/MIIGO/Crypto/HN batch)
  3. jds-v0.jsonl            (original 10 AI JDs)

Dedup key = lowercase(company) + lowercase(title[:40]). First occurrence wins.
Output: golden-jds-merged.jsonl, renumbered jd_001..jd_N.

Run once:  uv run python merge_golden.py
"""

import json
from pathlib import Path

SOURCES = [
    Path("data/golden-jds.jsonl"),
    Path("data/jds-v0-expansion.jsonl"),
    Path("data/jds-v0.jsonl"),
]
OUT = Path("data/golden-jds-merged.jsonl")


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def dedup_key(jd: dict) -> str:
    return f"{jd.get('company', '').strip().lower()}|{jd.get('title', '').strip().lower()[:40]}"


def main() -> None:
    seen: dict[str, dict] = {}
    counts_per_source = {}
    dupes = []

    for src in SOURCES:
        rows = load(src)
        counts_per_source[src.name] = len(rows)
        for jd in rows:
            key = dedup_key(jd)
            if key in seen:
                dupes.append((jd.get("company"), jd.get("title"), src.name))
            else:
                seen[key] = jd

    merged = list(seen.values())
    # renumber clean
    for i, jd in enumerate(merged, start=1):
        jd["id"] = f"jd_{i:03d}"

    OUT.write_text("\n".join(json.dumps(jd) for jd in merged), encoding="utf-8")

    print("Source counts:")
    for name, n in counts_per_source.items():
        print(f"  {name}: {n}")
    print(f"\nDeduped: {len(dupes)} dropped")
    for company, title, src in dupes:
        print(f"  - {company} / {title[:40]} (from {src})")
    print(f"\nMerged total: {len(merged)} unique JDs -> {OUT.name}")

    # category breakdown
    from collections import Counter

    cats = Counter(jd.get("expected_category") for jd in merged)
    print("\nCategory breakdown:")
    for cat, n in cats.most_common():
        print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()

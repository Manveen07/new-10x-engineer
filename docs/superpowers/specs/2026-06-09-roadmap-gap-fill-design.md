# Design — Roadmap gap-fill (2026-06-09)

## Context

Roadmap core was rebuilt 2026-06-07 and all week files (5–24) were drafted + resource-verified earlier on 2026-06-09 (commits `57ec210`, `5949782`, `d602180`, `5f4630a`). Audit found the plan complete and followable. Two execution gaps remain.

## Scope (approved)

1. **`dsa/` scaffold.** Week 5 (starts 2026-06-22) requires LeetCode commits to `dsa/` from Wed Jun 24. Build:
   - `dsa/README.md` — rules (no AI, ~20 min, commit same night, one-line pattern comment), a curated problem arc mapped to weeks 5–20 (2/week core = 32 problems), plus a stretch bank to reach the 60–80 target, and a tracking table.
   - `dsa/_template.py` — solution file format (docstring with pattern + complexity, `assert`-based self-test under `__main__`).
2. **EXERCISES.md reconciliation.** Tick only Month-1 items verifiable from git history / PROGRESS.md. Judgment-call items stay unticked. Header note marks the reconciliation.

## Out of scope

- PROGRESS.md Week 2–3 stubs (owner fills honestly).
- Any change to ROADMAP.md / PLAN-MONTHS-2-6.md / week files — current, verified 2 days old.
- New resources or restructuring — plan already live-verified.

## Problem-arc design

Patterns follow the roadmap's DSA rule (arrays / hash maps / strings / graphs, no DP grinding): arrays & hashing → two pointers → sliding window → stack → binary search → strings → linked list → tree-BFS/DFS as graph warm-up → graphs → heap. Easy→medium within each pattern; hards only as marked stretch.

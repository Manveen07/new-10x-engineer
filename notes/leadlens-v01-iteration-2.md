# leadlens v0.1 — iteration 2 findings (Sun 2026-05-31)

Doubled corpus to 20 JDs (added 10 expansion JDs covering Indian remote, partnership scams, contract gigs). Instrumented runner with per-call latency + cost.

## Aggregate metrics (20 JDs)

| Metric | Value |
|---|---|
| Avg latency | 5,446 ms |
| Total cost (20 JDs) | $0.017 |
| Avg cost / JD | $0.00085 |
| Tokens in / out | 14,326 / 5,095 |

Projection: **100-JD golden set run ≈ $0.085**. Gemini 2.5 Flash via Instructor: cheap and good enough for v0.1.

Latency 5.4s/JD = serial. Parallel via `asyncio.gather` (kata 02 pattern) → 10x speedup feasible. Defer to v0.2.

## Category accuracy v3

**14/20 = 70%** on `expected_category`.

| Expected | Hits | Misses |
|---|---|---|
| real_ai_role | 11/13 | — |
| ai_adjacent | 0/3 | 005/006/019 upgraded to real_ai_role (defensible, lossy) |
| ai_washed | 1/3 | **016/017 leaked — NEW failure mode F-006** |
| non_ai | 1/1 | — |

## 3 high-signal wins

1. **First STRONG fit_for_manveen match: jd_011 Sarvam FDE.** Real_ai_role + India OK + 2-5 yrs + LangGraph/MCP/Kafka stack. Personalization field doing real work.
2. **Comp extraction: 6/6 when present.** Across formats: `$80-105/hour USD`, `INR 18L/yr`, `INR 12-18 LPA + ESOPs`, `$90-140k OTE`, `INR 5,000-15,000/month`, `$2,500 USD`, `$180k-220k`.
3. **Sharp red_flags emerging.** Verbatim "Company culture concerns" (jd_018), "unpaid internship + performance-based stipend" (jd_013), "role involves zero AI engineering, no coding required" (jd_020).

## New failure mode — F-006: under-call ai_washed for scam patterns

**jd_016 MIIGO partnership** → labeled `ai_adjacent` (should be `ai_washed`).
Source: *"Not a job - it's a partnership opportunity. No salary - revenue share. Reply with thumbs-up emoji."*

**jd_017 Crypto x AI** → labeled `real_ai_role` (should be `ai_washed`).
Source: *"Equity-only role 1-3%. No salary for first 6 months. Vague on what we're actually building - will explain on a call. Telegram-first communication."*

**Pattern:** model treats AI-vocabulary as sufficient signal for real_ai_role, even when surrounding context (partnership, no salary, vague, Telegram-first) screams scam.

**Schema gap. Two fix candidates for v0.2:**
- Prompt clarification: "If description has 'partnership' / 'no salary' / 'revenue share' / 'equity only for first N months' / 'will explain on a call' — lean toward `ai_washed` regardless of AI vocabulary."
- **Better:** add `compensation_structure: Literal["salaried", "contract_hourly", "equity_only", "revenue_share", "partnership", "unclear"]`. Forces the model to type comp shape — makes scams visible by category. Same pattern as `stack_unspecified` fix worked for F-004.

## Stable wins from v2 still holding (cross-iteration)

| Check | v2 | v3 | Status |
|---|---:|---:|---|
| F-003 hardcoded confidence | 0/10 | 0/20 | STAYS FIXED |
| stack_unspecified accurate flag | 4/10 | 8/20 | All justified by source thinness |
| JSON duplication (v1 jd_002) | 0/10 | 0/20 | One-off Gemini glitch, fully gone |

## Schema-as-eval-spec — the deeper lesson

Three Specification gulfs killed by construction so far:
1. `min_length=100` on `confidence_reasoning` → kills hardcoded confidence (F-003)
2. `stack_unspecified: bool` companion to `core_stack: list[str]` → distinguishes source-thin from model-missed (F-004)
3. Next iter: `compensation_structure: Literal[...]` → will distinguish real-job from partnership-scam (F-006)

**Pattern:** every recurring failure mode has a corresponding schema field that forces the model to type the dimension explicitly, killing the failure by construction. Cheaper than prompt iteration, more measurable than judge calibration.

## Open items for v0.2

1. Add `compensation_structure` field per F-006 fix.
2. Add `asyncio.gather` parallel batch run — drop avg latency from 5s/JD to ~1s for 10-JD batch.
3. Pull 10 more REAL JDs (not synthesized) from HN June 2026 thread when it lands.
4. Sample 30 outputs by hand → calibrate first LLM-as-judge against my hand-labels (Hamel critique-shadowing pattern).
5. Wrap into a `pytest` eval suite that runs golden set + asserts category-accuracy ≥ 75% — CI gate.

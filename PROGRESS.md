# Progress Log

Update every Sunday. Honest hours. Specific. Log what you shipped **with a link**, and what you read **and what it changed in your build**.

Missing two Sundays in a row is the canary.

---

## Week of 2026-06-01 — Eval harness shipped (backfilled)

### Focus this week
1. Build a grounding/faithfulness eval for the cold-outbound system.
2. Calibrate the judge against human labels.
3. Run it on the full showcase set and find what it surfaces.

### Hours spent
- Project work: ~10
- Reading / course: ~1 (Hamel evals-faq, re-read into the build)
- Writing / community: 0 (← gap: no public post yet)
- Applications / interviews: 0
- Total: ~11

### Shipped this week
- Read-only eval harness (`eval/` in `coldoutboundskills`): claim decomposition → LLM-as-judge (supported/unsupported/contradicted) → faithfulness scoring → report. Isolated from the writing pipeline (zero pipeline edits).
- Full 300-email run: **95.5% mean faithfulness, 242/300 perfectly grounded, 0 contradicted.**
- **Judge calibration:** hand-labeled 20 emails / 124 claims → **100% agreement**, 100% recall on unsupported.
- Eval-discovered bug class ("count/group/name beyond evidence") → **Rule 17** baked into the writer prompt.
- Committed + pushed: harness, `SHOWCASE-300-REPORT.md`, `CALIBRATION-REPORT.md`, `DESIGN.md`, `README.md`.

### What I learned
Error analysis is the load-bearing eval activity — the value came from the 78 flagged claims clustering into one real pattern (counting/naming beyond the dossier), not from the aggregate number. The harness separates fabrications (0 contradictions) from soft inferences (78 unsupported), and caught miscounts a human would miss across 300. This maps to the Hamel/Shreya canon I'd only read about — now I've done it on real data.

### What slipped
- No public write-up yet (the eval story is a strong build-in-public post — do it in Phase 1).
- Not yet deployed (no FastAPI/live URL); no Langfuse tracing; no CI gate; no quality-rubric 2nd axis.
- `PROGRESS.md` had been the empty template until now.

### Next week's focus (Phase 1, Week 1)
1. Refactor the eval module to clean Python: types, pytest, logging, config.
2. Add a binary ship/no-ship judge head; re-validate judge with TPR/TNR (not raw agreement).
3. Start the FastAPI wrapper for the deploy.

### Confidence check (1-5)
- Evals knowledge: 4
- RAG knowledge: 1–2
- Agents knowledge: 3
- Production / deploy: 2
- Clean Python rigor: 2
- Cost modeling: 1
- Public footprint: 2
- Interview readiness: 3–4

---

## Weekly Template (copy this for each new week)

```markdown
## Week of YYYY-MM-DD — <one-line theme>

### Focus this week
1.
2.
3.

### Hours spent
- Project work:
- Reading / course:
- Writing / community:
- Applications / interviews:
- Total: __ / 8 target

### Shipped this week
- (link each item)

### What I learned
One specific paragraph — and what it changed in the build.

### What slipped
-

### Next week's focus
1.
2.
3.

### Confidence check (1-5)
- Evals knowledge:
- RAG knowledge:
- Agents knowledge:
- Production / deploy:
- Clean Python rigor:
- Cost modeling:
- Public footprint:
- Interview readiness:
```

---

## Monthly Review Template

### Month N - YYYY-MM
- Shipped (with links):
- Public post/update:
- Community/network action:
- Biggest failure mode found:
- Biggest cut from the plan:
- Next month adjustment:

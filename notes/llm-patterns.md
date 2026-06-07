# Eugene Yan's 7 LLM patterns — recall + project connections

The vocabulary for "how do you build LLM apps" (interview frame). Source: eugeneyan.com/writing/llm-patterns. Each = what it is + where in my projects.

| # | Pattern | What it is | In my projects |
|---|---|---|---|
| 1 | **Evals** | measure YOUR task's quality on YOUR golden set (not model-vs-model benchmarks) | ✅ leadlens judge v1 — critique-shadowing, TPR 1.0 / TNR 0.882 |
| 2 | **RAG** | retrieve relevant docs → stuff in prompt → grounded answer, fewer hallucinations, citations | = docsight (M3-4). Hybrid (vector+BM25) handles the 0x80 exact-match problem |
| 3 | **Fine-tuning** | retrain a general model for a narrow task/style | ✅ lived it — AsanaBot: ViT-Base, swapped output head, retrained on asana dataset. **leadlens correctly SKIPS it** (prompt+schema enough). Skill = knowing when not to. |
| 4 | **Caching** | store + reuse expensive call results → save $ + latency. Semantic caching = similarity-match the cache | leadlens: cache by JD hash; semantic cache for near-dup JDs. Relevant at scale. |
| 5 | **Guardrails** | deterministic checks around the LLM — PII, JSON format, safety, policy | ✅ leadlens red_flags + scam (ai_washed) judge + Pydantic schema validation |
| 6 | **Defensive UX** | design the UI assuming the model WILL be wrong — citations, show confidence, easy correction, constrained inputs, disclaimers | leadlens: surface confidence_reasoning, let user override; don't show category as absolute truth |
| 7 | **Collect feedback** | capture thumbs/corrections from real users → feed back into evals → improve (the flywheel) | leadlens: "this was wrong" button → new golden-set cases → recalibrate judge |

## The insight
leadlens already instantiates 3 patterns (Evals, Guardrails, correctly-skipped Fine-tuning). docsight adds RAG. reposcout adds more Guardrails. **Not random tricks — a system built from named patterns.** This framing IS the answer to "how do you build LLM apps."

## Recall result (Sun block)
6/7 named cold + connected 4 to own work (Evals→judge, Fine-tuning→AsanaBot, Guardrails→red_flags, Caching→semantic). Defensive UX was the only blank → filled. All 7 🟢.

## Re-test in 2 days
- Name all 7 cold.
- Defensive UX — the one that was blank: what is it + 2 tactics?
- Which patterns does leadlens already use vs which are future?

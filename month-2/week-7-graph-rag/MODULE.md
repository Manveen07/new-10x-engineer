# Week 7: Evaluation, Observability, And Optional Graph Extension

## Outcome

By the end of Week 7, the RAG system should have a golden evaluation set, retrieval metrics, answer-quality metrics, retrieval telemetry, and a regression gate. Graph RAG is treated as an optional measured extension, not the main dependency chain.

## Why This Matters

The job-ready skill is not "I tried GraphRAG." The job-ready skill is "I can prove retrieval improved and debug why an answer failed." Evals and observability are now core AI engineering skills.

## Day 31: Golden Evaluation Set

Exercise: `../exercises/day31_golden_eval_set.md`

Build:

- 30-50 questions over the seed corpus.
- answerable factual questions.
- multi-hop questions.
- section-specific questions.
- unanswerable questions.
- expected relevant chunk IDs.

Done when:

- Retrieval can be scored without relying only on LLM judgment.

## Day 32: Retrieval Metrics

Exercise: `../exercises/day32_retrieval_metrics.py`

Build:

- Precision@k.
- Recall@k.
- MRR@k.
- NDCG@k.
- benchmark runner that loads golden set + retrieval results.

Done when:

- A JSON/CSV benchmark report is produced.

## Day 33: Ragas-Style Answer Evals

Exercise: `../exercises/day33_ragas_answer_evals.md`

Build:

- evaluation plan for faithfulness, response relevancy, context precision, and context recall.
- small sample run in mock mode or hosted judge mode.
- documentation of judge-model limitations.

Done when:

- You can distinguish retrieval failure from generation failure.

## Day 34: Retrieval Telemetry

Exercise: `../exercises/day34_retrieval_telemetry.md`

Build:

- `retrieval_runs` table or log schema.
- fields for config hash, query, tenant, retriever stages, chunk IDs, scores, latency, and model names.
- structured logs for every `/search` and `/answer`.

Done when:

- A bad answer can be debugged from stored retrieval trace data.

## Day 35: Optional Graph Extension

Exercise: `../exercises/day35_optional_graph_extension.md`

Build only if the baseline is stable:

- entity extraction over chunks.
- lightweight `entities` and `entity_mentions` tables, or a Neo4j experiment.
- graph-boosted retrieval as an experiment flag.

Done when:

- Graph retrieval is benchmarked against baseline and can be turned off.

## Weekend 7: Regression Gate

Exercise: `../exercises/weekend7_regression_gate.md`

Build:

- benchmark command.
- metric thresholds.
- failure criteria for regressions.
- CI-ready smoke gate.

## Week 7 Acceptance Gate

- [ ] Golden set exists.
- [ ] Retrieval metrics run.
- [ ] Answer eval plan exists.
- [ ] Retrieval telemetry is stored.
- [ ] Regression threshold is documented.
- [ ] Optional graph work is measured, not assumed.

## Core Resources

| Resource | Use |
|---|---|
| https://docs.ragas.io/en/stable/concepts/metrics/ | RAG answer metrics |
| https://github.com/pgvector/pgvector | exact vs ANN tradeoffs |
| https://www.postgresql.org/docs/current/textsearch-controls.html | lexical search evidence |

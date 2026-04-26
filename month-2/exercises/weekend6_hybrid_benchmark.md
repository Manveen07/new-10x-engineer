# Weekend 6: Hybrid Retrieval Benchmark

## Goal

Compare retrieval strategies instead of guessing.

## Compare

- dense only.
- lexical only.
- dense + lexical + RRF.
- RRF + reranker.

## Metrics

- Precision@5.
- Recall@10.
- MRR@10.
- NDCG@10.
- p95 retrieval latency.

## Done When

- `docs/benchmarks/retrieval-quality.md` contains a table and short decision.

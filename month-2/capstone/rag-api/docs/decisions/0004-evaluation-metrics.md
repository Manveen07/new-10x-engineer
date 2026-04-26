# 0004: Evaluation Metrics

## Status

Draft

## Decision

Use retrieval metrics for chunk selection and Ragas-style metrics for answer quality.

## Rationale

Retrieval quality and answer quality fail differently. Precision@k, recall@k, MRR, and NDCG score retrieved chunk IDs. Faithfulness and context metrics score how generation uses retrieved context.

## Consequences

Benchmarks must report retrieval and answer metrics separately.

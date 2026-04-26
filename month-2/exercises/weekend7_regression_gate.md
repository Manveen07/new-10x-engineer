# Weekend 7: Regression Gate

## Goal

Prevent retrieval quality from silently getting worse.

## Build

- benchmark command.
- smoke dataset.
- metric thresholds.
- JSON report.
- CI-ready pass/fail behavior.

## Example Gate

- NDCG@10 must not drop by more than 5%.
- Recall@10 must stay above 0.75 on the smoke set.
- p95 retrieval latency must stay below the documented threshold.

# Day 34: Retrieval Telemetry

## Goal

Make every retrieval debuggable.

## Required Fields

- `request_id`
- `tenant_id`
- `query`
- `retrieval_config_hash`
- `embedding_provider`
- `embedding_model`
- `dense_top_k`
- `lexical_top_k`
- `rerank_top_k`
- `chunk_ids`
- `dense_scores`
- `lexical_scores`
- `fused_scores`
- `rerank_scores`
- `latency_ms_by_stage`

## Done When

- A bad answer can be explained from one retrieval trace.

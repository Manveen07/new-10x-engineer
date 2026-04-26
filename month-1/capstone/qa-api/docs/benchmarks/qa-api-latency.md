# Q&A API Latency

| Scenario | p50 ms | p95 ms | Notes |
|---|---:|---:|---|
| Exact cache hit | TBD | TBD | Should be fastest path |
| Semantic cache hit | TBD | TBD | Embedding/search overhead |
| Mock provider miss | TBD | TBD | Local deterministic path |
| Hosted provider miss | TBD | TBD | Optional; requires API key |

## Command

```bash
uv run pytest tests/test_qa.py
```

Add a small load/smoke script later if needed.

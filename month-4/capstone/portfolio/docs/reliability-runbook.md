# Reliability Runbook

## Checks

- API liveness.
- API readiness.
- database connectivity.
- Redis connectivity.
- provider timeout rate.
- retrieval benchmark smoke result.
- agent eval smoke result.

## Common Failures

| Failure | First check | Expected mitigation |
|---|---|---|
| DB down | readiness logs | fail writes, alert, restore DB |
| Redis down | readiness logs | degrade cache, monitor latency |
| Provider timeout | provider traces | retry bounded, fallback provider |
| Retrieval regression | benchmark report | inspect chunking/retrieval config |
| Agent loop | agent trace | max step stop and red-team test |

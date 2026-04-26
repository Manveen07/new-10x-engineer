# Cost Report

| Area | Driver | Control |
|---|---|---|
| LLM generation | input/output tokens | cache, concise prompts |
| embeddings | document chunks and queries | batch ingest, mock/local dev |
| reranking | candidate count | rerank only top candidates |
| retries | provider failures | bounded retry policy |
| observability | trace volume | sample where appropriate |

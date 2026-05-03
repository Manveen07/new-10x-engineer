# Flagship Projects

Three deep projects beat ten demos. Each project must be deployed, evaluated, documented, and honest about failure modes.

## Common Standard

Every project must include:

- [ ] Live deployed URL on Modal, Fly.io, HF Spaces, or equivalent.
- [ ] README with problem statement, architecture diagram, fresh-venv run instructions, eval results, cost-per-call, latency p50/p95, and "Where it fails."
- [ ] Eval dataset committed to the repo.
- [ ] Langfuse traces or trace screenshots.
- [ ] A visible iteration history.
- [ ] One public write-up focused on what failed and what improved.

## Project 1 - Business Classification Pipeline

Timeline: Months 1-2.

Core spec: given a company name and domain, return structured classification fields:

- Operating status.
- ICP fit.
- Sub-segment.
- Signals detected.
- Confidence.
- Citations or evidence references.

Recommended stack:

- Python.
- Pydantic.
- Instructor.
- OpenAI or Anthropic as the primary model.
- Web search and Maps-style retrieval tools.
- Langfuse tracing.
- Modal deployment.

Eval standard:

- 100 hand-labeled companies across pass, fail, and edge cases.
- Binary pass/fail LLM-as-judge per classification dimension.
- Judge calibrated to target more than 90% agreement with labels.
- At least three judge-prompt iterations.
- Confusion matrix in README.
- Failure taxonomy from open-coding notes.

Public write-up: "Auditing my own LLM classifier."

Target project folder: [projects/business-classification-pipeline](./projects/business-classification-pipeline/README.md).

## Project 2 - RAG Over GTM/Clay Knowledge

Timeline: Months 3-4.

Core spec: ingest Clay docs, university content, and attributed/consented community knowledge. Answer operator questions with citations while tracking retrieval quality and generation quality separately.

Recommended stack:

- FastAPI.
- Postgres + pgvector.
- BM25 or PostgreSQL full-text search alongside dense retrieval.
- Contextual retrieval preprocessing.
- Voyage or similar embeddings.
- Cohere/Voyage reranking or a local reranker behind an interface.
- Ragas-style generation evals.
- Langfuse tracing.
- Modal deployment.

Eval standard:

- About 150 synthetic query-chunk pairs for retrieval evals.
- recall@10/20, MRR, and NDCG.
- Generation evals for faithfulness, answer relevance, and context precision.
- Ragas judges calibrated against about 30 hand-labeled examples.
- Ablation table: pure dense vs BM25 vs hybrid RRF vs hybrid plus rerank.

Public write-up: "Contextual retrieval on Clay docs: a measured ablation."

Target project folder: [projects/gtm-clay-rag](./projects/gtm-clay-rag/README.md).

## Project 3 - ICP Research Agent

Timeline: Month 5.

Core spec: given a natural-language ICP, produce an enriched, validated, ranked company list with confidence scores.

Example input: "HVAC distributors in Texas with more than 50 employees doing residential work."

Recommended stack:

- Raw Python orchestration first.
- Pydantic and Instructor for tool I/O validation.
- Web search, Maps-style lookup, enrichment APIs, and LLM judge tools.
- Step budget capped at 20.
- Idempotency tokens for tool calls.
- Langfuse tracing.
- Modal deployment.

Eval standard:

- 30 reference ICPs.
- Golden expected tool paths for trajectory evals.
- LLM-as-judge for trajectory accuracy.
- Precision/recall on final company lists.
- State-transition matrix to identify loops and failure spikes.
- Cost/task, steps/task, and escalation rate.

Public write-up: "Workflows beat agents until they do not: a step-budgeted ICP researcher."

Target project folder: [projects/icp-research-agent](./projects/icp-research-agent/README.md).

## Portfolio Rule

Each README should answer these interview questions without extra explanation:

- What did the system do?
- What data did it run on?
- How did you know it was good?
- What failed?
- What did you change after looking at failures?
- What did it cost?
- How would you operate it in production?

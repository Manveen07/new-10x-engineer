# Day 30: Citations And Grounded Answers

## Goal

Generate answers that cite retrieved chunks and refuse unsupported answers.

## Build

- context assembly with chunk IDs.
- prompt that requires citations.
- response schema with `answer`, `citations`, `retrieval_trace_id`.
- insufficient-context behavior.

## Done When

- Every factual claim in the answer maps to at least one chunk citation.
- Unanswerable eval questions return a clear "I don't know" style answer.

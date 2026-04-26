# Day 31: Golden Evaluation Set

## Goal

Create a retrieval eval set that does not depend only on LLM-as-judge.

## Build

- 30-50 questions.
- reference answers.
- relevant chunk IDs.
- unanswerable cases.
- tags for factual, section-specific, multi-hop, and unanswerable.

## Done When

- Retrieval metrics can run from the golden set without calling an LLM.

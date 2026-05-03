# Business Classification Pipeline

Timeline: Months 1-2.

## Problem

Given a company name and domain, classify the business with structured fields that are useful in GTM workflows:

- Operating status.
- ICP fit.
- Sub-segment.
- Signals detected.
- Confidence.
- Citations/evidence.

## Build Standard

- Python + Pydantic.
- Instructor for structured outputs.
- OpenAI or Anthropic primary model.
- Web-search and Maps-style evidence collection.
- Langfuse traces.
- Modal deployment.

## Eval Standard

- 100 hand-labeled companies.
- Failure taxonomy from at least 50 open-coded traces.
- Binary judge checks per dimension.
- Judge calibrated to more than 90% label agreement.
- Confusion matrix.
- Cost-per-call and latency p50/p95.

## README Sections To Fill

- Architecture.
- Data and labels.
- Eval results.
- Cost and latency.
- Where it fails.
- Deployment.
- Iteration log.

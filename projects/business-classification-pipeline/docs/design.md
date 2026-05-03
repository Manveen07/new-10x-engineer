# Project 1 Design - Business Classification Pipeline

Status: draft.

## Objective

Given a company name and domain, produce a structured business classification with evidence that can be defended in an interview and audited with a golden dataset.

## Input Contract

- `company_name`: required.
- `domain`: required when available.
- `location`: optional.
- `known_context`: optional notes from Clay, CRM, or prior enrichment.

## Output Schema

- `operating_status`.
- `icp_fit`.
- `sub_segment`.
- `signals_detected`.
- `confidence`.
- `evidence`.
- `uncertainties`.

## Evidence Collection

Planned sources:

- Company website.
- Search snippets/results.
- Maps/business listing style data.
- Existing GTM/enrichment data where available.

Every classification should preserve enough evidence to explain why the system chose its label.

## Golden Dataset

Target: 100 hand-labeled companies.

Coverage:

- Clear operating businesses.
- Closed/inactive businesses.
- Ambiguous or stale websites.
- Similar-name collisions.
- Multilingual or sparse websites.
- ICP-fit edge cases.

## Eval Plan

- Binary pass/fail judge for operating status.
- Binary pass/fail judge for ICP fit.
- Binary pass/fail judge for evidence support.
- Confidence calibration review.
- Judge agreement target: more than 90% against hand labels.
- At least three judge-prompt iterations.
- Confusion matrix in README.

## Failure Taxonomy

Seed from Month 1 open-coding notes:

- Ambiguous web evidence.
- Stale or missing business pages.
- Similar company names.
- Confident wrong outputs.
- Evidence does not support the final label.
- Unclear ICP boundary.

## Observability

Trace these steps:

- Input normalization.
- Evidence retrieval.
- Classification model call.
- Judge model call.
- Final decision.
- Cost and latency.

## Deployment

Target: Modal API or job endpoint.

README must include:

- Setup.
- Run instructions.
- Eval command.
- Deployment command.
- Cost/latency notes.
- Where it fails.

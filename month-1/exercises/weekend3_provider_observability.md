# Weekend 3: Provider Integration And Observability

## Goal

Fold Week 3 exercises into the capstone. By the end of this weekend the app should have a real provider boundary and useful telemetry.

## Build

- `app/providers/base.py` with request and response models.
- `app/providers/mock.py` deterministic provider.
- `app/providers/openai.py` hosted provider adapter.
- `app/providers/anthropic.py` hosted provider adapter.
- `app/providers/registry.py` provider factory from settings.
- Timeout and retry wrapper around provider calls.
- `provider_calls` table and repository.
- Structured provider-call logs.
- Query history writes include cache outcome and provider-call ID where available.
- Tests for provider factory and mock provider.
- ADR: `docs/decisions/0003-provider-adapter-pattern.md`.

## Required Provider Response Fields

- `text`
- `provider`
- `model`
- `input_tokens`
- `output_tokens`
- `estimated_cost_usd`
- `latency_ms`
- `finish_reason`

## Required Log Fields

- `request_id`
- `provider`
- `model`
- `latency_ms`
- `input_tokens`
- `output_tokens`
- `estimated_cost_usd`
- `retry_count`
- `status`
- `error_type`

## Done When

- The app can run in mock provider mode with no API keys.
- Route code does not import OpenAI or Anthropic SDKs directly.
- Provider failures are tested.
- Provider timeout behavior is tested.

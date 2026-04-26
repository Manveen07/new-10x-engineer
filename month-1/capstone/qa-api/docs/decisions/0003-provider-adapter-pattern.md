# 0003: Provider Adapter Pattern

## Status

Draft

## Decision

Routes call a provider interface. Concrete providers implement mock, OpenAI, Anthropic, and optional local model behavior behind that interface.

## Rationale

Providers change pricing, models, SDKs, rate limits, and availability. The app should not depend on one provider SDK inside route handlers.

## Consequences

Every provider response must map to one internal response shape with text, provider, model, tokens, latency, cost, and finish reason.

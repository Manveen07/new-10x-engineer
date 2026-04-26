# 0001: Tooling Choices

## Status

Draft

## Decision

Use `uv`, Ruff, mypy, pytest, pytest-asyncio, respx, structlog, and stamina for Month 1.

## Rationale

- `uv` keeps environment and dependency setup reproducible.
- Ruff handles linting and formatting quickly.
- mypy makes provider/cache/database boundaries explicit.
- pytest and pytest-asyncio cover async API behavior.
- respx lets provider HTTP calls be tested without live API keys.
- structlog gives structured logs for request and provider telemetry.
- stamina gives bounded retry behavior with less custom retry code.

## Consequences

The setup is stricter than a quick script, but it creates a portfolio artifact that looks like production Python.

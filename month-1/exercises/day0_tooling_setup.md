# Day 0: Modern Python Tooling Setup

## Goal

Set the project standard before writing application code. This exercise exists so the rest of Month 1 uses the same commands, formatting, tests, and dependency workflow.

## Build

Inside `month-1/capstone/qa-api/`:

1. Use Python 3.12+.
2. Use `uv` for dependency management.
3. Keep dependencies in `pyproject.toml`.
4. Configure Ruff.
5. Configure mypy.
6. Configure pytest and pytest-asyncio.
7. Add dev tools for real API work: `respx` for HTTP mocking, `syrupy` for snapshots, and `pytest-cov` for coverage.
8. Add production helpers: `structlog` for structured logs, `stamina` for bounded retries, and `httpx`.
9. Create `.env.example`.
10. Create `docs/decisions/0001-tooling-choices.md`.

## Commands

```bash
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

## ADR Prompt

Write 150-300 words answering:

- Why `uv`?
- Why Ruff?
- Why mypy?
- Why pytest?
- Why HTTP/provider calls must be mocked in tests?
- Why `structlog` and retry instrumentation matter for AI APIs?
- What tradeoff did you accept by making this stricter than a quick script?

## Done When

- The commands above run.
- The capstone README uses `uv` commands.
- You can explain the local development workflow without improvising.

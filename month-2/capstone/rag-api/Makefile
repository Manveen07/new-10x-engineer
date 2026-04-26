.PHONY: install dev test lint format typecheck build benchmark-smoke

install:
	uv sync --extra dev

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8081

test:
	uv run pytest -v

lint:
	uv run ruff check .

typecheck:
	uv run mypy app

format:
	uv run ruff check --fix .
	uv run ruff format .

# Benchmark commands
benchmark-smoke:
	uv run python -m benchmarks.run_retrieval_eval --config benchmarks/configs/smoke.yaml

.PHONY: install dev test lint build

install:
	pip install -e .[dev]

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8081

test:
	pytest -v

lint:
	ruff check .
	mypy app

format:
	ruff check --fix .
	ruff format .

# Benchmark commands
benchmark-smoke:
	python -m benchmarks.run_retrieval_eval --config benchmarks/configs/smoke.yaml

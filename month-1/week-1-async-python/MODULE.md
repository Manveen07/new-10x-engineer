# Week 1: Tooling And Advanced Async Python

## Outcome

By the end of Week 1 you should be able to write async Python that is safe under real API pressure: bounded concurrency, backpressure, retries, cancellation, clean shutdown, and structured logs. You will also set up the tooling standard used by the Month 1 capstone.

## What This Week Teaches

- `uv` project setup, Ruff, mypy, pytest, and ADR habits.
- `async def`, `await`, the event loop, and coroutine scheduling.
- `asyncio.gather`, `asyncio.as_completed`, and `TaskGroup`.
- Semaphores for concurrency limits.
- Queues for producer-consumer pipelines and backpressure.
- Retry boundaries, timeouts, and cancellation behavior.
- Structured logs for async pipelines.

## Day 0: Modern Python Tooling

Exercise: `../exercises/day0_tooling_setup.md`

Build:

- Create or verify a `pyproject.toml`-based Python 3.12 project.
- Use `uv` for environment and dependency management.
- Configure `ruff check`, `ruff format`, `mypy`, and `pytest`.
- Add `docs/decisions/0001-tooling-choices.md` in the capstone explaining why this stack is used.

Done when:

- `uv run ruff check .` passes.
- `uv run ruff format --check .` passes.
- `uv run pytest` runs.
- You can explain why this repo does not use ad hoc `pip install` notes as the main workflow.

## Day 1: Coroutines And The Event Loop

Exercise: `../exercises/day1_coroutines.py`

Build:

- Small async functions that simulate network-bound work.
- Timing comparison between sequential and async execution.
- Notes explaining what `await` does and why async is not the same as threads.

Capstone connection:

- LLM calls, Redis calls, database calls, and HTTP clients all depend on this model.

## Day 2: Concurrent Execution

Exercise: `../exercises/day2_gather.py`

Build:

- Concurrent work with `asyncio.gather`.
- Ordered results with `gather`.
- First-finished processing with `as_completed`.
- Failure handling with and without `return_exceptions`.

Capstone connection:

- Later provider calls and batch embedding calls need controlled concurrent execution.

## Day 3: Semaphores And Rate Limits

Exercise: `../exercises/day3_semaphores.py`

Build:

- Fetch or simulate 20+ tasks while allowing only N concurrent operations.
- Implement a token-bucket style limiter.
- Show evidence that concurrency and rate are different controls.

Capstone connection:

- `/qa/ask` is expensive. Provider calls and embedding calls need both timeout and rate boundaries.

## Day 4: Producer-Consumer Queues

Exercise: `../exercises/day4_queue.py`

Build:

- Producer-consumer workflow using `asyncio.Queue(maxsize=N)`.
- Backpressure when producers outrun consumers.
- Clean shutdown with sentinels or cancellation.

Capstone connection:

- Month 2 ingestion will reuse this pattern. Month 1 uses it to understand API work queues and cache warmups.

## Day 5: TaskGroup, Cancellation, And Errors

Exercise: `../exercises/day5_taskgroup.py`

Build:

- Structured concurrency with `TaskGroup`.
- A failure case where one task fails and sibling tasks are cancelled.
- A cleanup path that still runs after cancellation.

Capstone connection:

- Lifespan-managed clients and background tasks must shut down cleanly.

## Weekend 1: Async Scraper / Enrichment Pipeline

Exercise: `../exercises/weekend1_scraper_pipeline.py`

Build a small pipeline that looks like a simplified AI data-enrichment job:

- Producers load URLs or company names.
- Workers fetch data with bounded concurrency.
- Consumers parse and normalize results.
- Retries are bounded and logged.
- Queue size prevents runaway memory growth.
- Final output includes success count, failure count, latency summary, and error reasons.

Required structured log fields:

- `request_id` or `item_id`
- `stage`
- `status`
- `attempt`
- `latency_ms`
- `error_type`

## Week 1 Acceptance Gate

- [ ] Tooling is configured with uv, Ruff, mypy, and pytest.
- [ ] You can explain event loop scheduling.
- [ ] You can show bounded concurrency with a semaphore.
- [ ] You can show backpressure with a bounded queue.
- [ ] You can explain `gather` vs `TaskGroup`.
- [ ] The weekend pipeline processes 50+ items without crashing on partial failures.
- [ ] The pipeline emits structured logs that would be useful in production.

## Core Resources

| Resource | Use |
|---|---|
| https://docs.astral.sh/uv/ | uv project workflow |
| https://docs.astral.sh/ruff/ | linting and formatting |
| https://docs.python.org/3/library/asyncio.html | asyncio reference |
| https://docs.python.org/3/library/asyncio-task.html#task-groups | TaskGroup reference |
| https://realpython.com/async-io-python/ | async walkthrough |

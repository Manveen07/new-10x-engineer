"""
Week 1 - Day 5: TaskGroup and Error Handling
==============================================

EXERCISES — Structured concurrency and graceful failures.
Requires Python 3.11+
Run with: python day5_taskgroup.py
"""

import asyncio
import random
import time


# ──────────────────────────────────────────────
# Exercise 1: Basic TaskGroup
# Refactor Exercise 2 from Day 1 using TaskGroup.
# Fetch user, posts, and comments concurrently.
# ──────────────────────────────────────────────

async def fetch_user():
    await asyncio.sleep(1)
    return {"id": 1, "name": "Alice"}

async def fetch_posts():
    await asyncio.sleep(2)
    return [{"id": 1, "title": "Hello"}]

async def fetch_comments():
    await asyncio.sleep(1.5)
    return [{"id": 1, "body": "Nice!"}]

async def fetch_all_with_taskgroup():
    """
    Use async with asyncio.TaskGroup() to run all three concurrently.
    Collect results from each task.
    Print results and elapsed time.
    """
    start = time.perf_counter()
    # YOUR CODE HERE
    # Hint: tg.create_task() returns a Task; access .result() after the group exits
    elapsed = time.perf_counter() - start
    print(f"TaskGroup: {elapsed:.2f}s")


# ──────────────────────────────────────────────
# Exercise 2: TaskGroup Error Propagation
# One task fails — observe how TaskGroup handles it.
# Compare behavior with gather(return_exceptions=True).
# ──────────────────────────────────────────────

async def reliable_task(name: str, delay: float):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def failing_task(name: str, delay: float):
    await asyncio.sleep(delay)
    raise ValueError(f"{name} failed!")

async def taskgroup_error_demo():
    """
    Run 3 reliable tasks and 1 failing task in a TaskGroup.
    Catch the ExceptionGroup and print:
    - Which tasks completed
    - Which tasks were cancelled
    - The exception(s) that occurred

    Key insight: TaskGroup CANCELS all other tasks when one fails.
    This is different from gather!
    """
    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(reliable_task("Task1", 0.5))
            t2 = tg.create_task(reliable_task("Task2", 3.0))  # would take 3s
            t3 = tg.create_task(failing_task("Task3", 1.0))   # fails at 1s
            t4 = tg.create_task(reliable_task("Task4", 2.0))
    except* ValueError as eg:
        # YOUR CODE HERE — handle the ExceptionGroup
        # Print which tasks completed, cancelled, or failed
        pass


# ──────────────────────────────────────────────
# Exercise 3: Graceful Shutdown with asyncio.Event
# Build a long-running service that:
# - Processes items from a queue
# - Shuts down gracefully when signaled
# - Finishes processing the current item before stopping
# ──────────────────────────────────────────────

async def graceful_worker(
    queue: asyncio.Queue,
    shutdown_event: asyncio.Event,
    worker_id: int,
):
    """
    Process items until shutdown_event is set.
    When shutdown is signaled:
    1. Finish the current item
    2. Don't pick up new items
    3. Print "Worker {worker_id}: shutting down gracefully"
    """
    processed = 0
    while not shutdown_event.is_set():
        try:
            # Use wait_for with a timeout so we can check shutdown_event
            item = await asyncio.wait_for(queue.get(), timeout=0.5)
            # YOUR CODE HERE — process the item
            processed += 1
            queue.task_done()
        except asyncio.TimeoutError:
            continue  # Check shutdown_event again
    print(f"Worker {worker_id}: shut down after processing {processed} items")


async def graceful_shutdown_demo():
    """
    1. Start 3 workers
    2. Feed items into the queue
    3. After 2 seconds, signal shutdown
    4. Wait for all workers to finish their current item
    """
    queue = asyncio.Queue()
    shutdown = asyncio.Event()

    # YOUR CODE HERE
    pass


# ──────────────────────────────────────────────
# Exercise 4: Resilient TaskGroup
# Build a TaskGroup wrapper that doesn't cancel everything
# when one task fails. Instead, it logs the error and continues.
# This is useful for batch processing where individual failures
# are acceptable.
# ──────────────────────────────────────────────

async def resilient_batch_process(tasks_data: list[dict]):
    """
    Process a list of tasks. Some may fail.
    Requirements:
    - Process all tasks concurrently
    - If a task fails, log the error but continue others
    - Return: (successes: list, failures: list)

    Hint: Wrap each task in a try/except within a helper coroutine,
    then use TaskGroup to run them all.
    """
    successes = []
    failures = []

    async def safe_process(item: dict):
        """Wrapper that catches errors for individual tasks."""
        try:
            # Simulate processing
            if item.get("will_fail"):
                raise RuntimeError(f"Processing failed for {item['id']}")
            await asyncio.sleep(random.uniform(0.1, 0.5))
            successes.append({"id": item["id"], "status": "success"})
        except Exception as e:
            failures.append({"id": item["id"], "error": str(e)})

    # YOUR CODE HERE — use TaskGroup to run safe_process for each item
    return successes, failures


async def resilient_demo():
    tasks = [
        {"id": 1, "will_fail": False},
        {"id": 2, "will_fail": True},
        {"id": 3, "will_fail": False},
        {"id": 4, "will_fail": True},
        {"id": 5, "will_fail": False},
    ]
    successes, failures = await resilient_batch_process(tasks)
    print(f"Successes: {len(successes)}, Failures: {len(failures)}")
    for f in failures:
        print(f"  FAILED: {f}")


# ──────────────────────────────────────────────
# Exercise 5: Shield critical operations
# asyncio.shield() prevents a coroutine from being cancelled.
# Build a scenario where this matters.
# ──────────────────────────────────────────────

async def save_to_database(data: dict) -> bool:
    """Critical operation that MUST complete even during cancellation."""
    print(f"  DB: saving {data['id']}...")
    await asyncio.sleep(1)  # simulate DB write
    print(f"  DB: saved {data['id']} successfully")
    return True

async def process_with_shield(item: dict, timeout: float = 0.5):
    """
    Process an item with a timeout.
    If processing takes too long, cancel it — BUT the database
    save must still complete (use asyncio.shield).

    Steps:
    1. Do some quick processing
    2. Save to database (shielded — cannot be cancelled)
    3. Do some slow post-processing (can be cancelled)
    """
    try:
        # Quick processing
        await asyncio.sleep(0.1)

        # Critical: save to DB — MUST complete
        await asyncio.shield(save_to_database(item))

        # Slow post-processing — cancellable
        await asyncio.sleep(2)
        print(f"Post-processing done for {item['id']}")

    except asyncio.CancelledError:
        print(f"Process cancelled for {item['id']}, but DB save was shielded")
        raise


async def shield_demo():
    """
    Run process_with_shield with a 1.5s timeout.
    The DB save (1s) should complete.
    The post-processing (2s) should be cancelled.
    """
    item = {"id": "important-record-42"}
    try:
        await asyncio.wait_for(process_with_shield(item), timeout=1.5)
    except asyncio.TimeoutError:
        print("Overall operation timed out (but DB save completed!)")


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Basic TaskGroup")
    print("=" * 50)
    # asyncio.run(fetch_all_with_taskgroup())

    print("\n" + "=" * 50)
    print("Exercise 2: Error Propagation")
    print("=" * 50)
    # asyncio.run(taskgroup_error_demo())

    print("\n" + "=" * 50)
    print("Exercise 3: Graceful Shutdown")
    print("=" * 50)
    # asyncio.run(graceful_shutdown_demo())

    print("\n" + "=" * 50)
    print("Exercise 4: Resilient Batch Processing")
    print("=" * 50)
    # asyncio.run(resilient_demo())

    print("\n" + "=" * 50)
    print("Exercise 5: Shield Critical Operations")
    print("=" * 50)
    # asyncio.run(shield_demo())

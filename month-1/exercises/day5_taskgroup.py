"""
Day 5: TaskGroup, Cancellation, And Cleanup

Goal:
    Practice structured concurrency. Provider calls, Redis clients, DB sessions,
    and background jobs must shut down cleanly when something fails.

Capstone output:
    Use this thinking in FastAPI lifespan cleanup and provider fallback tests.

Run:
    python day5_taskgroup.py
"""

import asyncio


async def dependency_check(name: str, should_fail: bool = False) -> str:
    try:
        await asyncio.sleep(0.1)
        if should_fail:
            raise ConnectionError(f"{name} is unavailable")
        return f"{name}:ok"
    finally:
        print(f"cleanup for {name}")


async def readiness_probe() -> list[str]:
    """Exercise: make this power /health/ready later."""
    results: list[str] = []
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(dependency_check("postgres")),
            group.create_task(dependency_check("redis")),
            group.create_task(dependency_check("provider")),
        ]
    for task in tasks:
        results.append(task.result())
    return results


async def failing_probe() -> None:
    """Observe how TaskGroup cancels sibling work when one dependency fails."""
    async with asyncio.TaskGroup() as group:
        group.create_task(dependency_check("postgres"))
        group.create_task(dependency_check("redis", should_fail=True))
        group.create_task(dependency_check("provider"))


async def main() -> None:
    print(await readiness_probe())
    try:
        await failing_probe()
    except* ConnectionError as errors:
        print(f"readiness failed with {len(errors.exceptions)} dependency error(s)")

    print("\nExercise: map dependency failures into /health/ready response details.")


if __name__ == "__main__":
    asyncio.run(main())

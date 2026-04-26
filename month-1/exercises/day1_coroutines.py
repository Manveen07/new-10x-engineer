"""
Day 1: Coroutines And The Event Loop

Goal:
    Understand the async execution model used by FastAPI, httpx, Redis,
    SQLAlchemy async, and LLM provider calls.

Capstone output:
    Add a short note to docs/decisions/0001-tooling-choices.md explaining
    why the API will use async IO for provider, cache, and database calls.

Run:
    python day1_coroutines.py
"""

import asyncio
import time


async def simulated_provider_call(question: str, latency_seconds: float = 0.2) -> str:
    """Simulate a network-bound LLM provider call."""
    await asyncio.sleep(latency_seconds)
    return f"answer:{question}"


async def simulated_cache_lookup(key: str, latency_seconds: float = 0.05) -> str | None:
    """Simulate a Redis cache lookup."""
    await asyncio.sleep(latency_seconds)
    return None if key == "miss" else f"cached:{key}"


async def sequential_flow() -> list[str | None]:
    """Exercise: run these calls sequentially and measure total time."""
    start = time.perf_counter()
    results = [
        await simulated_cache_lookup("miss"),
        await simulated_provider_call("what is async python?"),
        await simulated_cache_lookup("followup"),
    ]
    elapsed = time.perf_counter() - start
    print(f"sequential_flow took {elapsed:.3f}s")
    return results


async def concurrent_flow() -> list[str | None]:
    """Exercise: run independent IO concurrently and compare wall-clock time."""
    start = time.perf_counter()
    results = await asyncio.gather(
        simulated_cache_lookup("miss"),
        simulated_provider_call("what is async python?"),
        simulated_cache_lookup("followup"),
    )
    elapsed = time.perf_counter() - start
    print(f"concurrent_flow took {elapsed:.3f}s")
    return list(results)


async def main() -> None:
    await sequential_flow()
    await concurrent_flow()
    print("\nExplain why concurrent_flow is closer to the slowest single call than the sum.")


if __name__ == "__main__":
    asyncio.run(main())

"""
Day 2: Concurrent Execution Patterns

Goal:
    Practice gather, as_completed, and exception handling for batches of
    provider/cache/database-like calls.

Capstone output:
    Reuse these patterns when batching cache warmups or provider health checks.

Run:
    python day2_gather.py
"""

import asyncio
import random
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderResult:
    request_id: str
    ok: bool
    text: str | None
    latency_ms: float
    error: str | None = None


async def fake_provider_request(request_id: str, fail: bool = False) -> ProviderResult:
    start = time.perf_counter()
    await asyncio.sleep(random.uniform(0.05, 0.2))
    latency_ms = (time.perf_counter() - start) * 1000

    if fail:
        raise TimeoutError(f"provider timeout for {request_id}")

    return ProviderResult(
        request_id=request_id,
        ok=True,
        text=f"mock response for {request_id}",
        latency_ms=latency_ms,
    )


async def ordered_batch() -> list[ProviderResult | BaseException]:
    """Exercise 1: keep result order and capture failures."""
    tasks = [
        fake_provider_request("q-1"),
        fake_provider_request("q-2", fail=True),
        fake_provider_request("q-3"),
    ]
    return list(await asyncio.gather(*tasks, return_exceptions=True))


async def stream_as_completed() -> list[ProviderResult]:
    """Exercise 2: process fastest results first."""
    tasks = [
        fake_provider_request("fast-or-slow-1"),
        fake_provider_request("fast-or-slow-2"),
        fake_provider_request("fast-or-slow-3"),
    ]
    results: list[ProviderResult] = []
    for completed in asyncio.as_completed(tasks):
        results.append(await completed)
        print(f"received {results[-1].request_id} after {results[-1].latency_ms:.1f}ms")
    return results


async def main() -> None:
    print("ordered_batch:")
    for item in await ordered_batch():
        print(f"- {item!r}")

    print("\nstream_as_completed:")
    await stream_as_completed()

    print("\nExercise: map exceptions into the capstone error envelope.")


if __name__ == "__main__":
    asyncio.run(main())

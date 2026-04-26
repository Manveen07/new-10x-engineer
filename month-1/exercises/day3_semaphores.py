"""
Day 3: Semaphores And Rate Limits

Goal:
    Learn the difference between concurrency limits and rate limits. AI systems
    need both: concurrency protects your process, rate limits protect providers
    and cost.

Capstone output:
    Add a bounded provider-call wrapper and a tiered /qa/ask rate-limit design.

Run:
    python day3_semaphores.py
"""

import asyncio
import time
from dataclasses import dataclass


@dataclass
class RateLimitDecision:
    allowed: bool
    wait_seconds: float
    remaining_tokens: float


class TokenBucket:
    """Simple token bucket for learning. Production can use Redis buckets."""

    def __init__(self, capacity: int, refill_per_second: float) -> None:
        self.capacity = capacity
        self.refill_per_second = refill_per_second
        self.tokens = float(capacity)
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> RateLimitDecision:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated_at
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_second)
            self.updated_at = now

            if self.tokens >= 1:
                self.tokens -= 1
                return RateLimitDecision(True, 0.0, self.tokens)

            wait_seconds = (1 - self.tokens) / self.refill_per_second
            return RateLimitDecision(False, wait_seconds, self.tokens)


async def provider_call(task_id: int, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
        print(f"start provider_call task={task_id}")
        await asyncio.sleep(0.1)
        print(f"done provider_call task={task_id}")
        return f"answer-{task_id}"


async def run_bounded_concurrency() -> None:
    semaphore = asyncio.Semaphore(3)
    await asyncio.gather(*(provider_call(index, semaphore) for index in range(10)))


async def run_token_bucket() -> None:
    bucket = TokenBucket(capacity=2, refill_per_second=2)
    for index in range(8):
        decision = await bucket.acquire()
        if not decision.allowed:
            print(f"rate limited request={index}, sleeping {decision.wait_seconds:.2f}s")
            await asyncio.sleep(decision.wait_seconds)
        print(f"allowed request={index}")


async def main() -> None:
    print("Bounded concurrency:")
    await run_bounded_concurrency()
    print("\nToken bucket:")
    await run_token_bucket()
    print("\nExercise: implement the same token bucket with Redis for /qa/ask.")


if __name__ == "__main__":
    asyncio.run(main())

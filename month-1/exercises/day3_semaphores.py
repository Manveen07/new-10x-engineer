"""
Week 1 - Day 3: Semaphores and Backpressure
=============================================

EXERCISES — Rate limiting and concurrency control.
Run with: python day3_semaphores.py

Pre-req: pip install aiohttp
"""

import asyncio
import time
import aiohttp


# ──────────────────────────────────────────────
# Exercise 1: Basic Semaphore
# Fetch 20 URLs but limit to 5 concurrent requests.
# Print timestamps to PROVE only 5 run at a time.
# ──────────────────────────────────────────────

URLS = [f"https://httpbin.org/delay/1?id={i}" for i in range(20)]


async def fetch_with_semaphore(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    task_id: int,
) -> dict:
    """
    Fetch a URL while respecting the semaphore limit.
    Print: "[{elapsed:.1f}s] Task {task_id} START" when acquiring
    Print: "[{elapsed:.1f}s] Task {task_id} DONE" when releasing
    """
    # YOUR CODE HERE
    pass


async def limited_fetch(urls: list[str], max_concurrent: int = 5):
    """Fetch all URLs with a concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    start = time.perf_counter()
    # YOUR CODE HERE
    pass


# ──────────────────────────────────────────────
# Exercise 2: Rate Limiter
# Build a token-bucket rate limiter that allows
# N requests per second (not just N concurrent).
# This is what real API rate limiters look like.
# ──────────────────────────────────────────────

class TokenBucketRateLimiter:
    """
    Token bucket rate limiter.
    - Bucket holds `max_tokens` tokens
    - Tokens refill at `refill_rate` per second
    - Each request consumes 1 token
    - If no tokens available, wait until one refills
    """

    def __init__(self, max_tokens: int = 10, refill_rate: float = 5.0):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = max_tokens
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Wait until a token is available, then consume it."""
        # YOUR CODE HERE
        # Hint: refill tokens based on elapsed time, then check availability
        pass

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, *args):
        pass


async def rate_limited_fetching():
    """
    Fetch 30 URLs with a rate limit of 5 requests/second.
    Time the total execution — should take ~6 seconds (30 / 5).
    """
    limiter = TokenBucketRateLimiter(max_tokens=5, refill_rate=5.0)
    urls = [f"https://httpbin.org/get?id={i}" for i in range(30)]
    start = time.perf_counter()

    # YOUR CODE HERE

    elapsed = time.perf_counter() - start
    print(f"30 requests at 5/sec rate limit: {elapsed:.2f}s (expected ~6s)")


# ──────────────────────────────────────────────
# Exercise 3: Bounded Semaphore vs Regular Semaphore
# Demonstrate the difference. A BoundedSemaphore raises
# ValueError if you release() more than you acquire().
# Write code that shows this behavior.
# ──────────────────────────────────────────────

async def demonstrate_bounded_vs_regular():
    """
    1. Create a regular Semaphore(2) — release 3 times, acquire 3 times (works but buggy!)
    2. Create a BoundedSemaphore(2) — release 3 times, should raise ValueError
    Show why BoundedSemaphore is safer for catching bugs.
    """
    # YOUR CODE HERE
    pass


# ──────────────────────────────────────────────
# Exercise 4: Adaptive Concurrency
# Build a system that adjusts its concurrency level
# based on response times. If responses slow down,
# reduce concurrency. If fast, increase it.
# This is an advanced pattern used in production systems.
# ──────────────────────────────────────────────

class AdaptiveSemaphore:
    """
    A semaphore that adjusts its limit based on response latency.
    - If avg latency > high_threshold: decrease limit (min 1)
    - If avg latency < low_threshold: increase limit (max max_limit)
    - Check every `check_interval` requests
    """

    def __init__(
        self,
        initial: int = 5,
        max_limit: int = 20,
        low_threshold: float = 0.5,
        high_threshold: float = 2.0,
        check_interval: int = 10,
    ):
        self.current_limit = initial
        self.max_limit = max_limit
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.check_interval = check_interval
        self._semaphore = asyncio.Semaphore(initial)
        self._latencies: list[float] = []
        self._request_count = 0
        # YOUR CODE HERE — finish the implementation

    async def acquire(self):
        await self._semaphore.acquire()

    def release(self, latency: float):
        """Release the semaphore and record the latency."""
        self._semaphore.release()
        self._latencies.append(latency)
        self._request_count += 1
        # YOUR CODE HERE — check if we should adjust
        pass


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Basic Semaphore")
    print("=" * 50)
    # asyncio.run(limited_fetch(URLS, max_concurrent=5))

    print("\n" + "=" * 50)
    print("Exercise 2: Rate Limiter")
    print("=" * 50)
    # asyncio.run(rate_limited_fetching())

    print("\n" + "=" * 50)
    print("Exercise 3: Bounded vs Regular")
    print("=" * 50)
    # asyncio.run(demonstrate_bounded_vs_regular())

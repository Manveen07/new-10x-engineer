"""
Week 1 - Day 2: asyncio.gather and Concurrent Execution
=========================================================

EXERCISES — Build each one, benchmark the speedup.
Run with: python day2_gather.py

Pre-req: pip install aiohttp
"""

import asyncio
import time
import aiohttp


# ──────────────────────────────────────────────
# Exercise 1: Concurrent URL Fetching
# Fetch these 10 URLs concurrently using aiohttp + asyncio.gather
# Compare wall-clock time vs sequential fetching
# Target: demonstrate 5-10x speedup
# ──────────────────────────────────────────────

URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]


async def fetch_one(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch a single URL and return the JSON response."""
    async with session.get(url) as resp:
        return await resp.json()
    # YOUR CODE HERE
    pass


async def fetch_sequential(urls: list[str]) -> list:
    """Fetch all URLs one at a time. Measure total time."""
    start = time.perf_counter()
    results = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            result = await fetch_one(session, url)
            results.append(result)
    # YOUR CODE HERE
    elapsed = time.perf_counter() - start
    print(f"Sequential: {elapsed:.2f}s for {len(urls)} URLs")
    return results


async def fetch_concurrent(urls: list[str]) -> list:
    """Fetch all URLs concurrently with gather. Measure total time."""
    start = time.perf_counter()
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    # YOUR CODE HERE — use asyncio.gather
    elapsed = time.perf_counter() - start
    print(f"Concurrent: {elapsed:.2f}s for {len(urls)} URLs")
    return results


# ──────────────────────────────────────────────
# Exercise 2: Error Handling with gather
# One of these URLs will fail. Use return_exceptions=True
# and handle the error gracefully.
# ──────────────────────────────────────────────

URLS_WITH_ERROR = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/status/500",  # This will fail
    "https://httpbin.org/delay/1",
    "https://this-domain-does-not-exist-12345.com/",  # This will fail
    "https://httpbin.org/delay/1",
]


async def fetch_with_error_handling(urls: list[str]) -> list:
    """
    Fetch all URLs concurrently.
    - Use return_exceptions=True
    - Filter out errors from results
    - Print which URLs failed and why
    - Return only successful results
    """
    start = time.perf_counter()
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results, pending  = await asyncio.gather(*tasks, return_exceptions=True)
    # YOUR CODE HERE
    for result in results:
        if isinstance(result, Exception):
            print(f"Failed: {result}")
        else:
            results.append(result)
    elapsed = time.perf_counter() - start
    print(f"Concurrent: {elapsed:.2f}s for {len(urls)} URLs")
    return results


# ──────────────────────────────────────────────
# Exercise 3: asyncio.as_completed
# Sometimes you want to process results AS they arrive,
# not wait for all of them.
# Fetch these URLs and print each result as it completes.
# ──────────────────────────────────────────────

URLS_VARIED_DELAY = [
    "https://httpbin.org/delay/3",  # slow
    "https://httpbin.org/delay/1",  # fast
    "https://httpbin.org/delay/2",  # medium
    "https://httpbin.org/delay/0",  # instant
]


async def fetch_as_completed(urls: list[str]):
    """
    Fetch URLs and process results in completion order (not input order).
    Print: "Completed: {url} in {elapsed:.2f}s"
    Hint: use asyncio.as_completed()
    """
    start = time.perf_counter()
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        for result in asyncio.as_completed(tasks):
            results.append(result)
    # YOUR CODE HERE
    elapsed = time.perf_counter() - start
    print(f"Concurrent: {elapsed:.2f}s for {len(urls)} URLs")
    return results


# ──────────────────────────────────────────────
# Exercise 4: asyncio.wait with FIRST_COMPLETED
# Build a "fastest mirror" selector:
# Given multiple mirror URLs, return the result from
# whichever responds first and cancel the rest.
# ──────────────────────────────────────────────

MIRRORS = [
    "https://httpbin.org/delay/3",  # slow mirror
    "https://httpbin.org/delay/1",  # fast mirror
    "https://httpbin.org/delay/5",  # very slow mirror
]


async def fastest_mirror(urls: list[str]) -> str:
    """
    Race all URLs. Return the response from the fastest one.
    Cancel all other pending requests.
    Hint: use asyncio.wait(return_when=asyncio.FIRST_COMPLETED)
    """
    # YOUR CODE HERE
    start = time.perf_counter()
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # YOUR CODE HERE
    elapsed = time.perf_counter() - start
    print(f"Concurrent: {elapsed:.2f}s for {len(urls)} URLs")
    return results


# ──────────────────────────────────────────────
# Exercise 5: Batched concurrent requests
# You have 50 URLs but want to fetch them in batches of 10.
# This is a stepping stone to Wednesday's semaphore lesson.
# ──────────────────────────────────────────────

ALL_URLS = [f"https://httpbin.org/get?id={i}" for i in range(50)]


async def fetch_in_batches(urls: list[str], batch_size: int = 10) -> list:
    """
    Fetch URLs in batches of `batch_size`.
    Each batch runs concurrently, but batches run sequentially.
    Print progress: "Batch {n}: fetching {batch_size} URLs..."
    """
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            tasks = [fetch_one(session, url) for url in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
    # YOUR CODE HERE
    return results


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Sequential vs Concurrent")
    print("=" * 50)
    # asyncio.run(fetch_sequential(URLS))
    # asyncio.run(fetch_concurrent(URLS))

    print("\n" + "=" * 50)
    print("Exercise 2: Error Handling")
    print("=" * 50)
    # asyncio.run(fetch_with_error_handling(URLS_WITH_ERROR))

    print("\n" + "=" * 50)
    print("Exercise 3: As Completed")
    print("=" * 50)
    # asyncio.run(fetch_as_completed(URLS_VARIED_DELAY))

    print("\n" + "=" * 50)
    print("Exercise 4: Fastest Mirror")
    print("=" * 50)
    # asyncio.run(fastest_mirror(MIRRORS))

    print("\n" + "=" * 50)
    print("Exercise 5: Batched Fetching")
    print("=" * 50)
    # asyncio.run(fetch_in_batches(ALL_URLS, batch_size=10))

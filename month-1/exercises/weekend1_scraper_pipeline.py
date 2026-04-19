"""
Week 1 - Weekend: Async Web Scraper Pipeline
==============================================

INTEGRATION PROJECT — Combines everything from Week 1.
This is your first "real" async system.

Run with: python weekend1_scraper_pipeline.py

Architecture:
    [Producer 1] ──┐
    [Producer 2] ──┤──> Queue(maxsize=10) ──┤──> [Consumer 1] ──> [Results]
    [Producer 3] ──┘                        └──> [Consumer 2]

Requirements:
    - 3 producers fetch pages from URL_LIST
    - Semaphore(5) for rate limiting HTTP requests
    - Queue(maxsize=10) for backpressure between fetch and parse
    - 2 consumers extract page titles and links
    - TaskGroup for lifecycle management
    - Graceful shutdown on Ctrl+C via asyncio.Event
    - Retry logic: 3 attempts with exponential backoff
    - Process 50+ pages
    - Handle failures gracefully (log and skip, don't crash)

Pre-req: pip install aiohttp beautifulsoup4 lxml
"""

import asyncio
import signal
import time
from dataclasses import dataclass, field

import aiohttp
# from bs4 import BeautifulSoup  # uncomment when implementing


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
MAX_CONCURRENT_REQUESTS = 5
QUEUE_MAX_SIZE = 10
NUM_PRODUCERS = 3
NUM_CONSUMERS = 2
MAX_RETRIES = 3
BACKOFF_BASE = 0.5  # seconds

# 50+ URLs to scrape (using httpbin for predictability during dev,
# replace with real URLs when ready)
URL_LIST = [
    f"https://httpbin.org/html" for _ in range(20)
] + [
    f"https://httpbin.org/get?page={i}" for i in range(20)
] + [
    f"https://httpbin.org/anything?id={i}" for i in range(15)
]


# ──────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────
@dataclass
class FetchResult:
    url: str
    status: int
    html: str
    fetch_time: float


@dataclass
class ParsedPage:
    url: str
    title: str
    links: list[str]
    word_count: int


@dataclass
class PipelineStats:
    urls_fetched: int = 0
    urls_failed: int = 0
    pages_parsed: int = 0
    retries: int = 0
    start_time: float = field(default_factory=time.time)

    @property
    def elapsed(self) -> float:
        return time.time() - self.start_time

    def summary(self) -> str:
        return (
            f"\n{'='*50}\n"
            f"Pipeline Summary\n"
            f"{'='*50}\n"
            f"URLs fetched: {self.urls_fetched}\n"
            f"URLs failed:  {self.urls_failed}\n"
            f"Pages parsed: {self.pages_parsed}\n"
            f"Total retries: {self.retries}\n"
            f"Total time:   {self.elapsed:.2f}s\n"
            f"Throughput:   {self.pages_parsed / max(self.elapsed, 0.01):.1f} pages/s\n"
        )


# ──────────────────────────────────────────────
# YOUR IMPLEMENTATION BELOW
# ──────────────────────────────────────────────

async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    stats: PipelineStats,
) -> FetchResult | None:
    """
    Fetch a URL with retry logic.
    - Use the semaphore to limit concurrency
    - Retry up to MAX_RETRIES times with exponential backoff
    - Return FetchResult on success, None on final failure
    - Update stats.retries on each retry
    """
    # YOUR CODE HERE
    pass


async def producer(
    producer_id: int,
    urls: list[str],
    queue: asyncio.Queue,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    shutdown: asyncio.Event,
    stats: PipelineStats,
):
    """
    Fetch assigned URLs and put results in the queue.
    Stop early if shutdown is signaled.
    """
    for url in urls:
        if shutdown.is_set():
            break
        result = await fetch_with_retry(session, url, semaphore, stats)
        if result:
            stats.urls_fetched += 1
            await queue.put(result)
        else:
            stats.urls_failed += 1
    print(f"Producer {producer_id}: finished")


async def consumer(
    consumer_id: int,
    queue: asyncio.Queue,
    results: list[ParsedPage],
    shutdown: asyncio.Event,
    stats: PipelineStats,
):
    """
    Consume FetchResults from the queue, parse them, store ParsedPages.
    Use poison pill (None) to know when to stop.
    """
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            if shutdown.is_set():
                break
            continue

        if item is None:
            queue.task_done()
            break

        # YOUR CODE HERE — parse the HTML, create ParsedPage, append to results
        # For now, a simple extraction is fine (don't need BeautifulSoup)
        stats.pages_parsed += 1
        queue.task_done()

    print(f"Consumer {consumer_id}: finished")


async def run_pipeline():
    """
    Orchestrate the full pipeline:
    1. Split URLs among producers
    2. Start producers and consumers in a TaskGroup
    3. Handle Ctrl+C for graceful shutdown
    4. Print summary stats
    """
    shutdown = asyncio.Event()
    stats = PipelineStats()
    queue = asyncio.Queue(maxsize=QUEUE_MAX_SIZE)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    results: list[ParsedPage] = []

    # Split URLs among producers
    chunk_size = len(URL_LIST) // NUM_PRODUCERS
    url_chunks = [
        URL_LIST[i * chunk_size : (i + 1) * chunk_size]
        for i in range(NUM_PRODUCERS)
    ]
    # Give remainder to last producer
    url_chunks[-1].extend(URL_LIST[NUM_PRODUCERS * chunk_size :])

    # Set up Ctrl+C handler
    def signal_handler():
        print("\n[!] Shutdown requested...")
        shutdown.set()

    loop = asyncio.get_event_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, signal_handler)
    except NotImplementedError:
        # Windows doesn't support add_signal_handler
        pass

    # YOUR CODE HERE — run the pipeline with TaskGroup
    # 1. Start consumers
    # 2. Start producers
    # 3. Wait for producers to finish
    # 4. Send poison pills (one None per consumer)
    # 5. Wait for consumers to finish
    # 6. Print stats

    print(stats.summary())
    print(f"Collected {len(results)} parsed pages")


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("Async Web Scraper Pipeline")
    print("=" * 50)
    print(f"URLs: {len(URL_LIST)}")
    print(f"Producers: {NUM_PRODUCERS}, Consumers: {NUM_CONSUMERS}")
    print(f"Concurrency limit: {MAX_CONCURRENT_REQUESTS}")
    print(f"Queue size: {QUEUE_MAX_SIZE}")
    print("=" * 50)
    asyncio.run(run_pipeline())

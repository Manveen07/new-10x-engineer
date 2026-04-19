"""
Week 1 - Day 4: Producer-Consumer with asyncio.Queue
======================================================

EXERCISES — Pipeline patterns that you'll use in every AI backend.
Run with: python day4_queue.py
"""

import asyncio
import random
import time


# ──────────────────────────────────────────────
# Exercise 1: Basic Producer-Consumer
# 1 producer generates 20 items (with random delay)
# 1 consumer processes them (with random delay)
# Use queue.join() to wait for completion
# ──────────────────────────────────────────────

async def producer(queue: asyncio.Queue, n_items: int = 20):
    """Generate n_items and put them in the queue."""
    for i in range(n_items):
        item = {"id": i, "data": f"item_{i}", "timestamp": time.time()}
        # YOUR CODE HERE — put item, simulate delay
        pass
    print(f"Producer: done generating {n_items} items")


async def consumer(queue: asyncio.Queue, name: str):
    """Consume items from the queue until receiving None (poison pill)."""
    processed = 0
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        # YOUR CODE HERE — process item, simulate work, call task_done()
        processed += 1
    print(f"Consumer {name}: processed {processed} items")


async def basic_pipeline():
    queue = asyncio.Queue()
    # YOUR CODE HERE — run producer and consumer, use poison pill to stop
    pass


# ──────────────────────────────────────────────
# Exercise 2: Multiple Producers, Multiple Consumers
# 3 producers, each generating 10 items (30 total)
# 2 consumers processing items
# Queue maxsize=10 for backpressure
# Track: total items produced, consumed, processing time
# ──────────────────────────────────────────────

async def multi_producer(queue: asyncio.Queue, producer_id: int, n_items: int = 10):
    """Generate items tagged with producer_id."""
    for i in range(n_items):
        item = {
            "id": f"p{producer_id}_item{i}",
            "producer": producer_id,
            "created_at": time.time(),
        }
        await queue.put(item)
        await asyncio.sleep(random.uniform(0.01, 0.05))
    print(f"Producer {producer_id}: finished")


async def multi_consumer(queue: asyncio.Queue, consumer_id: int, results: list):
    """Consume items and append to results list."""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        # Simulate processing
        await asyncio.sleep(random.uniform(0.02, 0.08))
        results.append(item)
        queue.task_done()
    print(f"Consumer {consumer_id}: finished")


async def multi_pipeline():
    """
    Run 3 producers (10 items each) and 2 consumers.
    Queue maxsize=10 for backpressure.
    Print total items processed and total time.
    """
    queue = asyncio.Queue(maxsize=10)
    results = []
    # YOUR CODE HERE
    # Hint: send one None per consumer as poison pill
    pass


# ──────────────────────────────────────────────
# Exercise 3: Pipeline with transformation stages
# Stage 1: Raw data producer
# Stage 2: Transformer (enriches data)
# Stage 3: Writer (stores results)
# Each stage connected by a queue.
#
# This is exactly how AI ingestion pipelines work:
# [Load docs] → [Chunk & embed] → [Store in vector DB]
# ──────────────────────────────────────────────

async def stage_loader(output_queue: asyncio.Queue, n_docs: int = 15):
    """Stage 1: Load raw documents."""
    for i in range(n_docs):
        doc = {"id": i, "raw_text": f"Document {i} content here " * 10}
        await output_queue.put(doc)
        await asyncio.sleep(0.01)
    await output_queue.put(None)  # signal done
    print("Loader: done")


async def stage_transformer(
    input_queue: asyncio.Queue,
    output_queue: asyncio.Queue,
):
    """
    Stage 2: Transform documents.
    - Read from input_queue
    - Add word_count, char_count fields
    - Simulate embedding generation (sleep 0.05s)
    - Put enriched doc in output_queue
    """
    count = 0
    while True:
        doc = await input_queue.get()
        if doc is None:
            await output_queue.put(None)
            input_queue.task_done()
            break
        # YOUR CODE HERE — enrich the doc
        count += 1
        input_queue.task_done()
    print(f"Transformer: processed {count} docs")


async def stage_writer(input_queue: asyncio.Queue, storage: list):
    """
    Stage 3: Write results to storage.
    - Read from input_queue
    - Simulate DB write (sleep 0.02s)
    - Append to storage list
    """
    count = 0
    while True:
        doc = await input_queue.get()
        if doc is None:
            input_queue.task_done()
            break
        # YOUR CODE HERE
        count += 1
        input_queue.task_done()
    print(f"Writer: stored {count} docs")


async def three_stage_pipeline():
    """
    Connect all three stages with queues.
    Print: total docs processed, total time, docs/second throughput.
    """
    q1 = asyncio.Queue(maxsize=5)
    q2 = asyncio.Queue(maxsize=5)
    storage = []
    start = time.perf_counter()

    # YOUR CODE HERE — run all stages concurrently

    elapsed = time.perf_counter() - start
    print(f"Pipeline: {len(storage)} docs in {elapsed:.2f}s ({len(storage)/elapsed:.1f} docs/s)")


# ──────────────────────────────────────────────
# Exercise 4: Queue with timeout
# What happens when a consumer is slower than a producer
# and the queue is full? Add monitoring.
# ──────────────────────────────────────────────

async def monitored_pipeline():
    """
    Producer: generates 1 item every 0.01s
    Consumer: processes 1 item every 0.1s (10x slower!)
    Queue: maxsize=5

    Add a monitor coroutine that prints queue size every 0.5s.
    Observe the backpressure in action — the producer will be
    forced to slow down to match the consumer.
    """
    queue = asyncio.Queue(maxsize=5)
    stop_event = asyncio.Event()

    async def fast_producer():
        for i in range(50):
            await queue.put(i)
            # Notice: put() will BLOCK when queue is full!
            await asyncio.sleep(0.01)
        await queue.put(None)

    async def slow_consumer():
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            await asyncio.sleep(0.1)  # 10x slower than producer
            queue.task_done()

    async def monitor():
        while not stop_event.is_set():
            print(f"  [Monitor] Queue size: {queue.qsize()}/{queue.maxsize}")
            await asyncio.sleep(0.5)

    # YOUR CODE HERE — run all three, set stop_event when done
    pass


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Basic Producer-Consumer")
    print("=" * 50)
    # asyncio.run(basic_pipeline())

    print("\n" + "=" * 50)
    print("Exercise 2: Multi Producer-Consumer")
    print("=" * 50)
    # asyncio.run(multi_pipeline())

    print("\n" + "=" * 50)
    print("Exercise 3: Three-Stage Pipeline")
    print("=" * 50)
    # asyncio.run(three_stage_pipeline())

    print("\n" + "=" * 50)
    print("Exercise 4: Monitored Pipeline (Backpressure)")
    print("=" * 50)
    # asyncio.run(monitored_pipeline())

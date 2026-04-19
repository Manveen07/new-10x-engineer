# Week 1: Advanced Async Python Patterns

## Why This Matters
The entire AI backend stack — LLM API calls, vector database queries, embedding generation, agent tool execution — runs on async Python. You cannot build performant AI systems without fluency in asyncio. Every week after this assumes you can write async code without thinking about it.

---

## Day-by-Day Plan

### Monday — Coroutines and the Event Loop (1.5h)

**Read (45 min):**
- Python official asyncio conceptual overview
  https://docs.python.org/3/library/asyncio.html
- Real Python async walkthrough (first half)
  https://realpython.com/async-io-python/

**Key concepts to internalize:**
- A coroutine is a function defined with `async def` — calling it returns a coroutine object, not a result
- `await` suspends the coroutine and gives control back to the event loop
- The event loop is a single-threaded scheduler — it runs one coroutine at a time but switches between them at `await` points
- `asyncio.run()` creates the event loop and runs the top-level coroutine

**Exercise (45 min):** See `exercises/day1_coroutines.py`

**Additional resource:**
- Python asyncio library reference (bookmark this — you'll use it all month)
  https://docs.python.org/3/library/asyncio.html

---

### Tuesday — asyncio.gather and Concurrent Execution (1.5h)

**Read (25 min):**
- Krython tutorial on gather and wait patterns
  https://krython.com/tutorial/python/asyncio-patterns-gather-and-wait/

**Read (20 min):**
- SuperFastPython guide to asyncio.gather
  https://superfastpython.com/asyncio-gather/

**Key concepts:**
- `asyncio.gather(*coros)` runs coroutines concurrently and returns results in order
- `return_exceptions=True` prevents one failure from canceling everything
- `asyncio.wait()` gives more control: FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED
- `asyncio.as_completed()` yields results as they finish (not in order)
- Wall-clock time with gather ≈ slowest task, not sum of all tasks

**Exercise (45 min):** See `exercises/day2_gather.py`

**Additional resource:**
- asyncio.TaskGroup (Python 3.11+) — the modern replacement for gather
  https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup

---

### Wednesday — Semaphores and Backpressure (1.5h)

**Read (45 min):**
- Better Stack guide on async programming (focus on concurrency control section)
  https://betterstack.com/community/guides/scaling-python/python-async-programming/

**Read (30 min):**
- SuperFastPython guide to asyncio.Semaphore
  https://superfastpython.com/asyncio-semaphore/

**Key concepts:**
- `asyncio.Semaphore(n)` limits concurrent access to n — essential for rate-limited APIs
- `BoundedSemaphore` prevents releasing more than you acquired (catches bugs)
- Backpressure = slowing producers when consumers can't keep up
- Without backpressure, you'll OOM on large workloads or get rate-limited/banned
- Pattern: `async with semaphore: await fetch(url)` — simple and correct

**Exercise (45 min):** See `exercises/day3_semaphores.py`

**Additional resource:**
- Real-world rate limiting patterns
  https://docs.aiohttp.org/en/stable/client_advanced.html#limiting-connection-pool-size

---

### Thursday — Producer-Consumer with asyncio.Queue (1.5h)

**Read (30 min):**
- DEV Community producer-consumer tutorial
  https://dev.to/xsub/how-to-implement-the-producer-consumer-concurrency-design-pattern-with-asyncio-coroutines-23gj

**Read (30 min):**
- Python docs on asyncio.Queue
  https://docs.python.org/3/library/asyncio-queue.html

**Key concepts:**
- `asyncio.Queue(maxsize=N)` — when full, `put()` blocks the producer (backpressure!)
- `queue.join()` waits until all items are processed (every `get()` needs a `task_done()`)
- Producer-consumer decouples data generation from processing — critical for pipelines
- Multiple producers + multiple consumers = parallelism without shared state
- Poison pill pattern: producers send `None` to signal consumers to stop

**Exercise (30 min):** See `exercises/day4_queue.py`

**Additional resource:**
- Trio (alternative async library) for comparison
  https://trio.readthedocs.io/en/stable/

---

### Friday — TaskGroup and Error Handling (1.5h)

**Read (1h):**
- DEV Community: Mastering Python Async Patterns in 2026
  https://dev.to/shehzan/mastering-python-async-patterns-a-complete-guide-to-asyncio-in-2026-10o6

**Read (30 min):**
- Python 3.11 TaskGroup documentation
  https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup

**Key concepts:**
- `TaskGroup` (3.11+) is structured concurrency — all tasks in the group are managed together
- If one task raises, all others are cancelled and the exception propagates
- This is SAFER than `gather` — no orphaned tasks
- `asyncio.Event` for signaling between coroutines (e.g., graceful shutdown)
- `asyncio.shield()` protects critical operations from cancellation
- Exception groups (`ExceptionGroup`) collect multiple errors from TaskGroup

**Exercise (30 min):** See `exercises/day5_taskgroup.py`

---

### Weekend — Integration Exercise (1-2h)

**Build: Async Web Scraper Pipeline**

See `exercises/weekend1_scraper_pipeline.py` for the full spec.

**Architecture:**
```
[Producer 1] ──┐
[Producer 2] ──┤──> asyncio.Queue(maxsize=10) ──┤──> [Consumer 1]
[Producer 3] ──┘                                 └──> [Consumer 2]
                                                         │
                                                    [Results Store]
```

**Requirements:**
- 3 producers fetching pages from a list of URLs
- Semaphore(5) for rate limiting
- Queue(maxsize=10) for backpressure
- 2 consumers extracting titles and links
- TaskGroup for lifecycle management
- Graceful shutdown on Ctrl+C via asyncio.Event
- Retry logic (3 attempts with exponential backoff)
- Process 50+ pages concurrently

**Done when:**
- Pipeline handles 50+ URLs without crashing
- Handles network failures gracefully (retries, then skips)
- Shuts down cleanly on Ctrl+C (no orphaned tasks)
- You can explain every async primitive used and why

---

## Skill Checkpoint

Answer these without looking at notes:

1. What's the difference between `asyncio.gather()` and `TaskGroup`? When would you use each?
2. When would you use a `Semaphore` vs setting `Queue(maxsize=N)`? (They solve different problems!)
3. Write a producer-consumer where one producer crashing doesn't kill the others
4. What happens if you forget `task_done()` and call `queue.join()`?
5. Explain the event loop to someone who knows threads but not async

---

## Core Resources (Bookmark These)

| Resource | Type | URL |
|----------|------|-----|
| Python asyncio docs | Reference | https://docs.python.org/3/library/asyncio.html |
| Real Python async walkthrough | Tutorial | https://realpython.com/async-io-python/ |
| SuperFastPython asyncio guides | Deep dives | https://superfastpython.com/python-asyncio/ |
| aiohttp docs | Library | https://docs.aiohttp.org/en/stable/ |
| Python Concurrency with asyncio (book) | Book | Manning Publications, Matthew Fowler |

## Supplementary Resources (If You Want More)

- Talk: import asyncio by David Beazley (YouTube) — the classic live-coding talk
- Lynn Root: Advanced asyncio (YouTube) — patterns for production
- asyncio cheatsheet: https://www.pythonsheets.com/notes/python-asyncio.html
- Trio vs asyncio comparison (for context on structured concurrency philosophy)
  https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/

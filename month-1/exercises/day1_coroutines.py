"""
Week 1 - Day 1: Coroutines and the Event Loop
================================================

EXERCISES — Complete each one before moving to the next.
Run with: python day1_coroutines.py
"""

import asyncio
import time


# ──────────────────────────────────────────────
# Exercise 1: Basic Coroutine
# Write a coroutine `greet(name)` that:
# - Prints "Hello, {name}!"
# - Waits 1 second (simulate work)
# - Prints "Goodbye, {name}!"
# Then run it with asyncio.run()
# ──────────────────────────────────────────────

async def greet(name: str):
    print("Hello--")
    await asyncio.sleep(1)
    print("Goodbye--")



# ──────────────────────────────────────────────
# Exercise 2: Sequential vs Concurrent
# Write 3 coroutines that simulate API calls:
#   - fetch_user() → waits 1s, returns {"id": 1, "name": "Alice"}
#   - fetch_posts() → waits 2s, returns [{"id": 1, "title": "Hello"}]
#   - fetch_comments() → waits 1.5s, returns [{"id": 1, "body": "Nice!"}]
#
# Part A: Call them sequentially and time it (~4.5s)
# Part B: Call them concurrently with gather and time it (~2s)
# ──────────────────────────────────────────────

async def fetch_user():
    await asyncio.sleep(1)
    print("user fetched")
    return {"id": 1, "name": "Alice"}

async def fetch_posts():
    await asyncio.sleep(2)
    print("posts fetched")
    return [{"id": 1, "title": "Hello"}]

async def fetch_comments():
    await asyncio.sleep(1.5)
    print("comments fetched")
    return [{"id": 1, "body": "Nice!"}]

async def sequential():
    """Call all three sequentially. Should take ~4.5s."""
    start = time.perf_counter()
    await fetch_user()
    await fetch_posts()
    await fetch_comments()
    # YOUR CODE HERE
    elapsed = time.perf_counter() - start
    print(f"Sequential: {elapsed:.2f}s")

async def concurrent():
    """Call all three concurrently. Should take ~2s."""
    start = time.perf_counter()
    await asyncio.gather(fetch_user(), fetch_posts(), fetch_comments())
    # YOUR CODE HERE
    elapsed = time.perf_counter() - start
    print(f"Concurrent: {elapsed:.2f}s")


# ──────────────────────────────────────────────
# Exercise 3: Understanding await
# What happens if you call a coroutine WITHOUT await?
# Uncomment the function below and run it. Read the warning.
# Then fix it.
# ──────────────────────────────────────────────

async def broken_example():
    fetch_user()  # <-- What's wrong here?
    print("Done")


# ──────────────────────────────────────────────
# Exercise 4: Return values from coroutines
# Write a coroutine `compute(x, y)` that:
# - Waits 0.5s (simulate computation)
# - Returns x + y
# Then write `main()` that:
# - Calls compute(3, 4) and compute(10, 20) concurrently
# - Prints both results
# ──────────────────────────────────────────────

async def compute(x: int, y: int) -> int:
    await asyncio.sleep(0.5)
    return x + y

async def main_exercise4():
    await asyncio.gather(compute(3, 4), compute(10, 20))
    # YOUR CODE HERE
    pass


# ──────────────────────────────────────────────
# Exercise 5: Event loop internals
# Run this and observe the output order. Then explain WHY
# the prints appear in this order (write your answer as a comment).
# ──────────────────────────────────────────────

async def task_a():
    print("A: start")
    await asyncio.sleep(2)
    print("A: end")

async def task_b():
    print("B: start")
    await asyncio.sleep(1)
    print("B: end")

async def task_c():
    print("C: start")
    await asyncio.sleep(0)  # yields control but resumes immediately
    print("C: end")

async def main_exercise5():
    await asyncio.gather(task_a(), task_b(), task_c())

# EXPLAIN THE OUTPUT ORDER HERE:
# ...  abccba


# ──────────────────────────────────────────────
# Run all exercises
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Basic Coroutine")
    print("=" * 50)
    asyncio.run(greet("World"))

    print("\n" + "=" * 50)
    print("Exercise 2: Sequential vs Concurrent")
    print("=" * 50)
    asyncio.run(sequential())
    asyncio.run(concurrent())

    print("\n" + "=" * 50)
    print("Exercise 4: Return Values")
    print("=" * 50)
    asyncio.run(main_exercise4())

    print("\n" + "=" * 50)
    print("Exercise 5: Event Loop Order")
    print("=" * 50)
    asyncio.run(main_exercise5())

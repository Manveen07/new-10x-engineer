"""
Day 4: Producer-Consumer Queues

Goal:
    Build an async pipeline with backpressure. This is the same shape as
    cache warmups, ingestion jobs, lead enrichment, and future RAG indexing.

Capstone output:
    Use the pattern for any background cache warmup or provider smoke-test job.

Run:
    python day4_queue.py
"""

import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkItem:
    item_id: str
    question: str


@dataclass(frozen=True)
class ProcessedItem:
    item_id: str
    normalized_question: str


async def producer(queue: asyncio.Queue[WorkItem], questions: list[str]) -> None:
    for index, question in enumerate(questions):
        item = WorkItem(item_id=f"q-{index}", question=question)
        await queue.put(item)
        print(f"produced {item.item_id}; queue_size={queue.qsize()}")


async def consumer(name: str, queue: asyncio.Queue[WorkItem], results: list[ProcessedItem]) -> None:
    while True:
        item = await queue.get()
        try:
            normalized = " ".join(item.question.lower().split())
            await asyncio.sleep(0.05)
            results.append(ProcessedItem(item.item_id, normalized))
            print(f"{name} processed {item.item_id}")
        finally:
            queue.task_done()


async def run_pipeline() -> list[ProcessedItem]:
    queue: asyncio.Queue[WorkItem] = asyncio.Queue(maxsize=3)
    results: list[ProcessedItem] = []
    questions = [
        "What is Async Python?",
        "Explain FastAPI Depends",
        "What is semantic caching?",
        "How do JWT refresh tokens work?",
        "What is Redis used for?",
    ]

    consumers = [asyncio.create_task(consumer(f"worker-{i}", queue, results)) for i in range(2)]
    await producer(queue, questions)
    await queue.join()

    for task in consumers:
        task.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)
    return results


async def main() -> None:
    results = await run_pipeline()
    print(f"\nprocessed={len(results)}")
    print("Exercise: add retries and structured logs with item_id/stage/status.")


if __name__ == "__main__":
    asyncio.run(main())

"""
Weekend 1: Async Enrichment Pipeline

Goal:
    Build the async pipeline pattern used by real AI systems before adding
    FastAPI. This models lead enrichment, cache warmup, and future RAG ingestion.

Capstone output:
    Reuse the retry, bounded concurrency, queue, and structured log patterns
    in provider calls and background jobs.

Run:
    python weekend1_scraper_pipeline.py
"""

import asyncio
import random
import time
from dataclasses import dataclass, field
from typing import Literal


Status = Literal["ok", "failed"]


@dataclass(frozen=True)
class EnrichmentInput:
    item_id: str
    company_name: str
    domain: str


@dataclass(frozen=True)
class EnrichmentOutput:
    item_id: str
    status: Status
    summary: str | None
    latency_ms: float
    attempts: int
    error_type: str | None = None


@dataclass
class PipelineStats:
    ok: int = 0
    failed: int = 0
    latencies_ms: list[float] = field(default_factory=list)

    def record(self, output: EnrichmentOutput) -> None:
        if output.status == "ok":
            self.ok += 1
        else:
            self.failed += 1
        self.latencies_ms.append(output.latency_ms)


def log_event(**fields: object) -> None:
    """Learning version of structured logs. Capstone should use JSON logs."""
    print(fields)


async def fake_external_lookup(item: EnrichmentInput) -> str:
    await asyncio.sleep(random.uniform(0.03, 0.12))
    if random.random() < 0.10:
        raise TimeoutError("simulated upstream timeout")
    return f"{item.company_name} builds software at {item.domain}"


async def enrich_with_retry(
    item: EnrichmentInput,
    semaphore: asyncio.Semaphore,
    max_attempts: int = 3,
) -> EnrichmentOutput:
    start = time.perf_counter()
    async with semaphore:
        for attempt in range(1, max_attempts + 1):
            try:
                log_event(item_id=item.item_id, stage="lookup", status="start", attempt=attempt)
                summary = await fake_external_lookup(item)
                latency_ms = (time.perf_counter() - start) * 1000
                output = EnrichmentOutput(item.item_id, "ok", summary, latency_ms, attempt)
                log_event(
                    item_id=item.item_id,
                    stage="lookup",
                    status="ok",
                    attempt=attempt,
                    latency_ms=latency_ms,
                )
                return output
            except TimeoutError as error:
                log_event(
                    item_id=item.item_id,
                    stage="lookup",
                    status="retry",
                    attempt=attempt,
                    error_type=type(error).__name__,
                )
                await asyncio.sleep(0.05 * attempt)

    latency_ms = (time.perf_counter() - start) * 1000
    return EnrichmentOutput(
        item_id=item.item_id,
        status="failed",
        summary=None,
        latency_ms=latency_ms,
        attempts=max_attempts,
        error_type="TimeoutError",
    )


async def producer(queue: asyncio.Queue[EnrichmentInput], items: list[EnrichmentInput]) -> None:
    for item in items:
        await queue.put(item)
        log_event(item_id=item.item_id, stage="queue", status="produced", queue_size=queue.qsize())


async def worker(
    name: str,
    queue: asyncio.Queue[EnrichmentInput],
    semaphore: asyncio.Semaphore,
    stats: PipelineStats,
) -> None:
    while True:
        item = await queue.get()
        try:
            output = await enrich_with_retry(item, semaphore)
            stats.record(output)
            log_event(worker=name, item_id=item.item_id, stage="done", status=output.status)
        finally:
            queue.task_done()


async def run_pipeline() -> PipelineStats:
    items = [
        EnrichmentInput(f"item-{index}", f"Company {index}", f"company{index}.com")
        for index in range(50)
    ]
    queue: asyncio.Queue[EnrichmentInput] = asyncio.Queue(maxsize=10)
    semaphore = asyncio.Semaphore(5)
    stats = PipelineStats()

    workers = [asyncio.create_task(worker(f"worker-{i}", queue, semaphore, stats)) for i in range(3)]
    await producer(queue, items)
    await queue.join()

    for task in workers:
        task.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    return stats


async def main() -> None:
    stats = await run_pipeline()
    avg_latency = sum(stats.latencies_ms) / len(stats.latencies_ms)
    print({"ok": stats.ok, "failed": stats.failed, "avg_latency_ms": round(avg_latency, 2)})
    print("\nExercise: replace print logs with capstone structured logging.")


if __name__ == "__main__":
    asyncio.run(main())

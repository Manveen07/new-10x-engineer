"""
Day 17: Semantic Cache

Goal:
    Build the cache API used by /qa/ask: exact lookup first, semantic lookup
    second, provider call only on miss.

Capstone output:
    app/services/cache.py with get/set/stats behavior and tests.
"""

import hashlib
import math
import time
from dataclasses import dataclass, field
from typing import Literal


CacheOutcome = Literal["exact_hit", "semantic_hit", "miss"]


@dataclass(frozen=True)
class CacheEntry:
    normalized_question: str
    answer: str
    embedding: list[float]
    namespace: str
    created_at: float
    ttl_seconds: int
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class CacheResult:
    outcome: CacheOutcome
    answer: str | None
    matched_query: str | None
    similarity: float | None
    latency_ms: float


def normalize_question(question: str) -> str:
    return " ".join(question.lower().strip().split())


def exact_cache_key(namespace: str, question: str) -> str:
    digest = hashlib.sha256(normalize_question(question).encode("utf-8")).hexdigest()
    return f"qa:{namespace}:{digest}"


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right, strict=False))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


class InMemorySemanticCache:
    """Learning implementation. Replace storage with Redis in the capstone."""

    def __init__(self, threshold: float = 0.88) -> None:
        self.threshold = threshold
        self.entries: list[CacheEntry] = []
        self.hits = 0
        self.misses = 0

    async def get(self, question: str, namespace: str = "default") -> CacheResult:
        start = time.perf_counter()
        normalized = normalize_question(question)
        query_embedding = mock_embed(normalized)

        for entry in self.entries:
            if entry.namespace == namespace and entry.normalized_question == normalized:
                self.hits += 1
                return CacheResult(
                    "exact_hit",
                    entry.answer,
                    entry.normalized_question,
                    1.0,
                    (time.perf_counter() - start) * 1000,
                )

        best_entry: CacheEntry | None = None
        best_score = 0.0
        for entry in self.entries:
            if entry.namespace != namespace:
                continue
            score = cosine_similarity(query_embedding, entry.embedding)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry and best_score >= self.threshold:
            self.hits += 1
            return CacheResult(
                "semantic_hit",
                best_entry.answer,
                best_entry.normalized_question,
                best_score,
                (time.perf_counter() - start) * 1000,
            )

        self.misses += 1
        return CacheResult("miss", None, None, best_score or None, (time.perf_counter() - start) * 1000)

    async def set(
        self,
        question: str,
        answer: str,
        namespace: str = "default",
        ttl_seconds: int = 3600,
        metadata: dict[str, object] | None = None,
    ) -> None:
        normalized = normalize_question(question)
        self.entries.append(
            CacheEntry(
                normalized_question=normalized,
                answer=answer,
                embedding=mock_embed(normalized),
                namespace=namespace,
                created_at=time.time(),
                ttl_seconds=ttl_seconds,
                metadata=metadata or {},
            )
        )

    def stats(self) -> dict[str, object]:
        total = self.hits + self.misses
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / total if total else 0.0,
            "entries": len(self.entries),
            "threshold": self.threshold,
        }


def mock_embed(text: str, dimensions: int = 32) -> list[float]:
    vector = [0.0] * dimensions
    for token in text.split():
        index = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16) % dimensions
        vector[index] += 1.0
    return vector


async def demo() -> None:
    cache = InMemorySemanticCache(threshold=0.75)
    await cache.set("What is async Python?", "Async Python handles IO without blocking.")
    print(await cache.get("what is async python?"))
    print(await cache.get("Explain async python"))
    print(cache.stats())
    print("\nExercise: replace InMemorySemanticCache storage with Redis.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(demo())

"""
Day 28: Reranking

Goal:
    Put reranking behind an interface so you can test mock/local/hosted rerankers.
"""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RerankCandidate:
    chunk_id: str
    text: str
    initial_score: float


@dataclass(frozen=True)
class RerankResult:
    chunk_id: str
    rerank_score: float
    rank: int


class Reranker(Protocol):
    async def rerank(self, query: str, candidates: list[RerankCandidate]) -> list[RerankResult]: ...


class MockReranker:
    async def rerank(self, query: str, candidates: list[RerankCandidate]) -> list[RerankResult]:
        ordered = sorted(candidates, key=lambda item: item.initial_score, reverse=True)
        return [
            RerankResult(candidate.chunk_id, candidate.initial_score, rank)
            for rank, candidate in enumerate(ordered, start=1)
        ]


if __name__ == "__main__":
    print("Exercise: benchmark pre-rerank vs post-rerank Precision@5 and MRR@10.")

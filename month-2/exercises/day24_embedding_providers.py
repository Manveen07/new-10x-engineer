"""
Day 24: Embedding Providers

Goal:
    Build an embedding interface with deterministic mock mode and optional
    hosted/local implementations.
"""

import hashlib
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class EmbeddingRequest:
    texts: list[str]
    input_type: str
    model: str


@dataclass(frozen=True)
class EmbeddingResponse:
    vectors: list[list[float]]
    provider: str
    model: str
    dimensions: int
    latency_ms: float
    estimated_cost_usd: float


class EmbeddingProvider(Protocol):
    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse: ...


def mock_embed(text: str, dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    for token in text.lower().split():
        index = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16) % dimensions
        vector[index] += 1.0
    return vector


if __name__ == "__main__":
    print(mock_embed("search query: what is pgvector?", dimensions=8))
    print("Exercise: add MockEmbeddingProvider and optional OpenAI/local providers.")

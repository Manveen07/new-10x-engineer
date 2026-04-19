"""
Week 4 - Day 2: Build a Semantic Cache from Scratch
=====================================================

Build a semantic cache that stores LLM responses and returns
cached results for semantically similar queries.

Pre-req:
  pip install redis numpy openai
  Docker: redis/redis-stack running on port 6379

Run with: python day17_semantic_cache.py
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass

import numpy as np

# Redis imports — install with: pip install redis
# import redis.asyncio as redis


# ──────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────

@dataclass
class CacheEntry:
    query: str
    response: str
    embedding: list[float]
    metadata: dict
    created_at: float
    ttl_seconds: int


@dataclass
class CacheResult:
    hit: bool
    response: str | None
    similarity: float
    cached_query: str | None
    latency_ms: float


# ──────────────────────────────────────────────
# Exercise 1: Embedding Function
# In production, use OpenAI or another provider.
# For development, use a simple hash-based mock.
# ──────────────────────────────────────────────

class EmbeddingProvider:
    """Generates embeddings for text."""

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.dimension = 256  # mock dimension (OpenAI uses 1536)

    async def embed(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.

        Mock mode: creates a deterministic vector from text hash.
        Production: calls OpenAI text-embedding-3-small.
        """
        if self.use_mock:
            return self._mock_embed(text)
        # YOUR CODE HERE — add real embedding call
        raise NotImplementedError("Add real embedding provider")

    def _mock_embed(self, text: str) -> list[float]:
        """
        Deterministic mock embedding.
        Similar texts should produce similar vectors.

        Strategy: normalize text, hash character n-grams,
        accumulate into a fixed-size vector, normalize to unit length.
        """
        # Normalize text
        text = text.lower().strip()

        # Initialize vector
        vec = np.zeros(self.dimension)

        # Hash character trigrams and accumulate
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            h = int(hashlib.md5(trigram.encode()).hexdigest(), 16)
            idx = h % self.dimension
            vec[idx] += 1.0

        # Normalize to unit vector
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        return vec.tolist()


# ──────────────────────────────────────────────
# Exercise 2: Cosine Similarity
# ──────────────────────────────────────────────

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    Returns value between -1 and 1 (1 = identical, 0 = orthogonal).

    YOUR CODE HERE
    """
    pass


# ──────────────────────────────────────────────
# Exercise 3: The Semantic Cache
# ──────────────────────────────────────────────

class SemanticCache:
    """
    A semantic cache that stores LLM responses and returns
    cached results for semantically similar queries.

    For simplicity, this version uses in-memory storage.
    Exercise 4 upgrades it to Redis.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        similarity_threshold: float = 0.85,
        default_ttl: int = 3600,  # 1 hour
        namespace: str = "default",
    ):
        self.embedder = embedding_provider
        self.threshold = similarity_threshold
        self.default_ttl = default_ttl
        self.namespace = namespace
        self._cache: list[CacheEntry] = []

        # Stats
        self.hits = 0
        self.misses = 0

    async def get(self, query: str) -> CacheResult:
        """
        Look up a query in the cache.

        Steps:
        1. Embed the query
        2. Compare against all cached embeddings
        3. If best match > threshold AND not expired → return cached response
        4. Otherwise → cache miss

        YOUR CODE HERE
        """
        pass

    async def set(
        self,
        query: str,
        response: str,
        metadata: dict | None = None,
        ttl: int | None = None,
    ) -> None:
        """
        Store a query-response pair in the cache.

        Steps:
        1. Embed the query
        2. Create a CacheEntry
        3. Store it

        YOUR CODE HERE
        """
        pass

    def clear(self, namespace: str | None = None) -> int:
        """Clear cache entries. Returns count of removed entries."""
        # YOUR CODE HERE
        pass

    @property
    def hit_rate(self) -> float:
        """Return the cache hit rate as a percentage."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0

    @property
    def stats(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{self.hit_rate:.1f}%",
            "entries": len(self._cache),
            "namespace": self.namespace,
        }


# ──────────────────────────────────────────────
# Exercise 4: Redis-Backed Cache (upgrade)
# Replace in-memory storage with Redis vectors.
# Only attempt this if Redis Stack is running.
# ──────────────────────────────────────────────

class RedisSemanticCache(SemanticCache):
    """
    Redis-backed semantic cache using vector similarity search.

    Requires Redis Stack (includes RediSearch with vector support).

    YOUR CODE HERE — override get() and set() to use Redis
    instead of self._cache list.

    Hints:
    - Use HSET to store entries with vector field
    - Use FT.SEARCH with KNN query for similarity search
    - Or use the redisvl library for a higher-level API
    """
    pass


# ──────────────────────────────────────────────
# Exercise 5: Cache-Wrapped LLM
# Combine the cache with an LLM provider.
# ──────────────────────────────────────────────

class CachedLLM:
    """
    Wraps an LLM with semantic caching.

    Usage:
        llm = CachedLLM(provider, cache)
        response = await llm.ask("What is Python?")
        # First call: hits LLM, caches result
        # Second similar call: returns cached result instantly
    """

    def __init__(self, cache: SemanticCache):
        self.cache = cache

    async def ask(self, query: str) -> dict:
        """
        1. Check cache
        2. If hit → return cached response
        3. If miss → call LLM → cache result → return

        Return dict with: response, cached (bool), similarity, latency_ms

        YOUR CODE HERE
        """
        pass


# ──────────────────────────────────────────────
# Demo and Testing
# ──────────────────────────────────────────────

async def demo():
    embedder = EmbeddingProvider(use_mock=True)
    cache = SemanticCache(embedder, similarity_threshold=0.85)

    # Test similar queries
    test_queries = [
        # Group 1: Python questions (should cache-hit each other)
        "What is Python programming language?",
        "What's Python?",
        "Tell me about Python",
        "Explain Python programming",

        # Group 2: JavaScript questions (should cache-hit each other)
        "What is JavaScript?",
        "Tell me about JavaScript",
        "Explain JavaScript to me",

        # Group 3: Unrelated (should NOT hit)
        "What is the weather today?",
        "How do I cook pasta?",
    ]

    print("Populating cache with initial responses...")
    await cache.set(
        "What is Python programming language?",
        "Python is a high-level, interpreted programming language known for its simplicity.",
    )
    await cache.set(
        "What is JavaScript?",
        "JavaScript is a dynamic programming language used primarily for web development.",
    )

    print("\nTesting cache hits/misses:")
    print("-" * 60)

    for query in test_queries:
        result = await cache.get(query)
        status = "HIT" if result.hit else "MISS"
        sim = f"{result.similarity:.3f}" if result.similarity > 0 else "N/A"
        print(f"[{status}] (sim={sim}) {query[:50]}")
        if result.hit:
            print(f"       → {result.response[:60]}...")

    print(f"\nCache stats: {cache.stats}")


if __name__ == "__main__":
    asyncio.run(demo())

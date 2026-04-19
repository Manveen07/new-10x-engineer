"""
Week 3 - Day 5: Strategy Pattern & Factory Pattern for AI
===========================================================

Strategy: swap algorithms at runtime (embedding model, retrieval method)
Factory: centralize object creation (build pipelines from config)

These two patterns together let you build AI systems where changing
from OpenAI to Cohere embeddings, or from vector search to hybrid
search, is a config change — not a code change.

Pre-req: pip install numpy

Run with: python day15_strategy_factory.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import asyncio
import hashlib
import random
import time
from typing import Any

import numpy as np


# ══════════════════════════════════════════════
# Data Models
# ══════════════════════════════════════════════

@dataclass
class Document:
    id: str
    content: str
    metadata: dict = field(default_factory=dict)
    embedding: list[float] | None = None


@dataclass
class SearchResult:
    document: Document
    score: float
    method: str  # Which strategy found this


# ══════════════════════════════════════════════
# Exercise 1: Embedding Strategy
# ══════════════════════════════════════════════
#
# Different embedding models for different use cases:
# - OpenAI: highest quality, costs money, requires API
# - Cohere: good multilingual, different pricing
# - Local: free, runs locally, lower quality
# - Mock: for testing, deterministic, no dependencies

class EmbeddingStrategy(ABC):
    """Abstract base: all embedding strategies must implement embed()."""

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Convert text to a vector."""
        ...

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Convert multiple texts to vectors (efficient batching)."""
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        """The dimension of the output vectors."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for logging."""
        ...


class MockEmbedding(EmbeddingStrategy):
    """
    Deterministic mock embeddings for testing.
    Similar texts produce similar vectors (using character n-grams).
    """

    def __init__(self, dim: int = 256):
        self._dim = dim

    async def embed(self, text: str) -> list[float]:
        text = text.lower().strip()
        vec = np.zeros(self._dim)
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            h = int(hashlib.md5(trigram.encode()).hexdigest(), 16)
            vec[h % self._dim] += 1.0
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm > 0 else vec.tolist()

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(t) for t in texts]

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def name(self) -> str:
        return "mock"


class OpenAIEmbedding(EmbeddingStrategy):
    """
    OpenAI text-embedding-3-small.
    High quality, 1536 dimensions, ~$0.02 per 1M tokens.

    YOUR CODE HERE — implement or leave as placeholder:
    """

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self._dim = 1536

    async def embed(self, text: str) -> list[float]:
        # In production:
        # from openai import AsyncOpenAI
        # client = AsyncOpenAI()
        # response = await client.embeddings.create(input=text, model=self.model)
        # return response.data[0].embedding

        # Placeholder: return mock
        mock = MockEmbedding(self._dim)
        return await mock.embed(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        # OpenAI supports batch embedding in a single API call — much more efficient
        return [await self.embed(t) for t in texts]

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def name(self) -> str:
        return f"openai/{self.model}"


# YOUR CODE HERE: Add CohereEmbedding class (same interface, different provider)


# ══════════════════════════════════════════════
# Exercise 2: Retrieval Strategy
# ══════════════════════════════════════════════
#
# Different retrieval approaches for different needs:
# - Vector: semantic similarity (good for meaning)
# - BM25: keyword matching (good for exact terms)
# - Hybrid: combines both (best overall quality)

class RetrievalStrategy(ABC):
    """Abstract base: all retrieval strategies must implement retrieve()."""

    @abstractmethod
    async def retrieve(
        self,
        query: str,
        documents: list[Document],
        k: int = 5,
    ) -> list[SearchResult]:
        """Retrieve top-k documents matching the query."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...


class VectorRetrieval(RetrievalStrategy):
    """
    Semantic similarity using cosine distance.
    Best for: "What does this mean?" style queries.
    """

    def __init__(self, embedding_strategy: EmbeddingStrategy):
        self.embedder = embedding_strategy

    async def retrieve(
        self,
        query: str,
        documents: list[Document],
        k: int = 5,
    ) -> list[SearchResult]:
        # Embed the query
        query_vec = np.array(await self.embedder.embed(query))

        # Ensure all documents have embeddings
        for doc in documents:
            if doc.embedding is None:
                doc.embedding = await self.embedder.embed(doc.content)

        # Compute cosine similarity with each document
        results = []
        for doc in documents:
            doc_vec = np.array(doc.embedding)
            similarity = float(np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec) + 1e-8
            ))
            results.append(SearchResult(document=doc, score=similarity, method="vector"))

        # Sort by score descending, return top k
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:k]

    @property
    def name(self) -> str:
        return f"vector({self.embedder.name})"


class BM25Retrieval(RetrievalStrategy):
    """
    BM25 keyword matching.
    Best for: exact keyword queries, technical terms, names.

    BM25 formula (simplified):
    score = sum(IDF(term) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl/avgdl)))

    YOUR CODE HERE — implement a simple BM25:
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b

    async def retrieve(
        self,
        query: str,
        documents: list[Document],
        k: int = 5,
    ) -> list[SearchResult]:
        import math

        query_terms = query.lower().split()
        doc_lengths = [len(doc.content.lower().split()) for doc in documents]
        avg_dl = sum(doc_lengths) / len(doc_lengths) if doc_lengths else 1
        n_docs = len(documents)

        results = []
        for i, doc in enumerate(documents):
            doc_terms = doc.content.lower().split()
            dl = doc_lengths[i]
            score = 0.0

            for term in query_terms:
                # Term frequency in this document
                tf = doc_terms.count(term)
                # Document frequency (how many docs contain this term)
                df = sum(1 for d in documents if term in d.content.lower())
                # IDF
                idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
                # BM25 term score
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / avg_dl)
                score += idf * (numerator / denominator)

            results.append(SearchResult(document=doc, score=score, method="bm25"))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:k]

    @property
    def name(self) -> str:
        return "bm25"


class HybridRetrieval(RetrievalStrategy):
    """
    Combines vector and BM25 retrieval with Reciprocal Rank Fusion (RRF).
    This is the gold standard for production RAG systems.

    RRF score = sum(1 / (k + rank_i)) for each retrieval method

    YOUR CODE HERE:
    """

    def __init__(
        self,
        vector_strategy: VectorRetrieval,
        bm25_strategy: BM25Retrieval,
        rrf_k: int = 60,
        vector_weight: float = 0.6,
    ):
        self.vector = vector_strategy
        self.bm25 = bm25_strategy
        self.rrf_k = rrf_k
        self.vector_weight = vector_weight

    async def retrieve(
        self,
        query: str,
        documents: list[Document],
        k: int = 5,
    ) -> list[SearchResult]:
        # Get results from both methods
        vector_results = await self.vector.retrieve(query, documents, k=k*2)
        bm25_results = await self.bm25.retrieve(query, documents, k=k*2)

        # Reciprocal Rank Fusion
        rrf_scores: dict[str, float] = {}
        for rank, result in enumerate(vector_results):
            doc_id = result.document.id
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + self.vector_weight / (self.rrf_k + rank + 1)
        for rank, result in enumerate(bm25_results):
            doc_id = result.document.id
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + (1 - self.vector_weight) / (self.rrf_k + rank + 1)

        # Build final results
        doc_map = {doc.id: doc for doc in documents}
        results = [
            SearchResult(document=doc_map[doc_id], score=score, method="hybrid")
            for doc_id, score in rrf_scores.items()
        ]
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:k]

    @property
    def name(self) -> str:
        return f"hybrid({self.vector.name}+{self.bm25.name})"


# ══════════════════════════════════════════════
# Exercise 3: Pipeline Factory
# ══════════════════════════════════════════════
#
# The Factory centralizes creation of retrieval pipelines
# from a configuration dictionary. This is how you'll
# configure your AI system in production.

@dataclass
class PipelineConfig:
    """Configuration for a retrieval pipeline."""
    embedding_provider: str = "mock"           # "mock", "openai", "cohere"
    embedding_dimension: int = 256
    retrieval_method: str = "hybrid"           # "vector", "bm25", "hybrid"
    vector_weight: float = 0.6                 # For hybrid: weight of vector vs bm25
    top_k: int = 5


class PipelineFactory:
    """
    Creates retrieval pipelines from configuration.

    Usage:
        config = PipelineConfig(embedding_provider="openai", retrieval_method="hybrid")
        pipeline = PipelineFactory.create(config)
        results = await pipeline.retrieve(query, documents)
    """

    @staticmethod
    def create_embedding(config: PipelineConfig) -> EmbeddingStrategy:
        """Create the right embedding strategy from config."""
        if config.embedding_provider == "mock":
            return MockEmbedding(dim=config.embedding_dimension)
        elif config.embedding_provider == "openai":
            return OpenAIEmbedding()
        # YOUR CODE HERE: add more providers
        else:
            raise ValueError(f"Unknown embedding provider: {config.embedding_provider}")

    @staticmethod
    def create_retrieval(
        config: PipelineConfig,
        embedding: EmbeddingStrategy,
    ) -> RetrievalStrategy:
        """Create the right retrieval strategy from config."""
        if config.retrieval_method == "vector":
            return VectorRetrieval(embedding)
        elif config.retrieval_method == "bm25":
            return BM25Retrieval()
        elif config.retrieval_method == "hybrid":
            return HybridRetrieval(
                vector_strategy=VectorRetrieval(embedding),
                bm25_strategy=BM25Retrieval(),
                vector_weight=config.vector_weight,
            )
        else:
            raise ValueError(f"Unknown retrieval method: {config.retrieval_method}")

    @classmethod
    def create(cls, config: PipelineConfig) -> RetrievalStrategy:
        """Create a complete retrieval pipeline from config."""
        embedding = cls.create_embedding(config)
        return cls.create_retrieval(config, embedding)


# ══════════════════════════════════════════════
# Exercise 4: Environment-Based Configuration
# ══════════════════════════════════════════════

def pipeline_from_env() -> RetrievalStrategy:
    """
    Create a pipeline from environment variables.

    Reads:
    - EMBEDDING_PROVIDER (default: "mock")
    - RETRIEVAL_METHOD (default: "hybrid")
    - VECTOR_WEIGHT (default: 0.6)
    - TOP_K (default: 5)

    YOUR CODE HERE
    """
    import os
    config = PipelineConfig(
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "mock"),
        retrieval_method=os.getenv("RETRIEVAL_METHOD", "hybrid"),
        vector_weight=float(os.getenv("VECTOR_WEIGHT", "0.6")),
        top_k=int(os.getenv("TOP_K", "5")),
    )
    return PipelineFactory.create(config)


# ══════════════════════════════════════════════
# Demo
# ══════════════════════════════════════════════

async def demo():
    # Create sample documents
    documents = [
        Document(id="1", content="Python is a high-level programming language known for its simplicity and readability"),
        Document(id="2", content="JavaScript is the language of the web, running in browsers and on servers with Node.js"),
        Document(id="3", content="Rust is a systems programming language focused on safety, speed, and concurrency"),
        Document(id="4", content="Machine learning uses statistical algorithms to learn patterns from data"),
        Document(id="5", content="Deep learning is a subset of machine learning using neural networks with many layers"),
        Document(id="6", content="PostgreSQL is a powerful open-source relational database management system"),
        Document(id="7", content="Redis is an in-memory data store used for caching and message brokering"),
        Document(id="8", content="Docker containers package applications with their dependencies for consistent deployment"),
        Document(id="9", content="Kubernetes orchestrates container deployment, scaling, and management"),
        Document(id="10", content="FastAPI is a modern Python web framework for building APIs with automatic documentation"),
    ]

    query = "What programming language is good for web development?"

    # Test each retrieval strategy
    configs = [
        PipelineConfig(retrieval_method="vector"),
        PipelineConfig(retrieval_method="bm25"),
        PipelineConfig(retrieval_method="hybrid"),
    ]

    for config in configs:
        pipeline = PipelineFactory.create(config)
        print(f"\n{'='*60}")
        print(f"Strategy: {pipeline.name}")
        print(f"{'='*60}")

        results = await pipeline.retrieve(query, documents, k=3)
        for i, result in enumerate(results, 1):
            print(f"  {i}. [{result.score:.4f}] {result.document.content[:80]}...")

    # Show how easy it is to swap — just change config
    print(f"\n{'='*60}")
    print("Swapping strategy is just a config change:")
    print(f"{'='*60}")
    print('  config = PipelineConfig(embedding_provider="openai", retrieval_method="hybrid")')
    print('  pipeline = PipelineFactory.create(config)')
    print('  # That\'s it! Zero code changes in your application.')


if __name__ == "__main__":
    asyncio.run(demo())

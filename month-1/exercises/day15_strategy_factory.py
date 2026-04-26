"""
Day 15: Strategy And Factory Patterns

Goal:
    Learn the pattern behind provider selection, cache selection, embedding
    selection, and future Month 2 retrieval selection.

Capstone output:
    Settings-driven factories for provider, cache, and embedding implementations.
"""

from dataclasses import dataclass
from typing import Literal, Protocol


ProviderName = Literal["mock", "openai", "anthropic", "ollama"]
CacheMode = Literal["exact_only", "semantic", "disabled"]
EmbeddingMode = Literal["mock", "openai"]


@dataclass(frozen=True)
class RuntimeConfig:
    provider: ProviderName = "mock"
    cache_mode: CacheMode = "semantic"
    embedding_mode: EmbeddingMode = "mock"
    semantic_threshold: float = 0.88


class CacheStrategy(Protocol):
    async def get(self, question: str) -> object: ...

    async def set(self, question: str, answer: str) -> None: ...


FACTORY_RULES = [
    "Factories read typed settings, not raw environment variables.",
    "Routes receive interfaces from dependencies, not concrete SDK clients.",
    "Mock implementations are first-class because tests and local dev need them.",
    "Each strategy must expose enough metadata for logs and query history.",
    "Do not introduce LangChain or RAG strategies in Month 1.",
]


def provider_factory_name(config: RuntimeConfig) -> str:
    """Exercise: replace this with real provider construction in the capstone."""
    return f"{config.provider}_provider"


def cache_factory_name(config: RuntimeConfig) -> str:
    """Exercise: replace this with real cache construction in the capstone."""
    return f"{config.cache_mode}_cache"


def print_exercise() -> None:
    config = RuntimeConfig()
    print("Day 15: Strategy And Factory Patterns")
    print(f"provider={provider_factory_name(config)}")
    print(f"cache={cache_factory_name(config)}")
    print("\nRules:")
    for rule in FACTORY_RULES:
        print(f"- {rule}")


if __name__ == "__main__":
    print_exercise()

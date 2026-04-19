"""
Week 3 - Day 4: Adapter Pattern for LLM Providers
====================================================

This is one of the most important patterns you'll use in AI engineering.
LLM providers change pricing, go down, or get replaced. Your application
code should NEVER directly import openai or anthropic — always go through
an adapter.

Run with: python day14_adapter_pattern.py
Pre-req: pip install openai anthropic  (optional — mock works without them)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import asyncio
import time
import random


# ──────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────

@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    provider: str


@dataclass
class EmbeddingResponse:
    embedding: list[float]
    model: str
    input_tokens: int
    provider: str


# ──────────────────────────────────────────────
# Exercise 1: Define the Abstract Interface
# This is the contract that ALL providers must implement.
# ──────────────────────────────────────────────

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    All providers must implement these methods.
    """

    @abstractmethod
    async def complete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        """Generate a chat completion."""
        ...

    @abstractmethod
    async def embed(
        self,
        text: str,
        model: str | None = None,
    ) -> EmbeddingResponse:
        """Generate an embedding for the given text."""
        ...

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text (approximate is fine)."""
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'openai', 'anthropic', 'mock')."""
        ...


# ──────────────────────────────────────────────
# Exercise 2: Mock Provider (for testing)
# This MUST work without any API keys.
# ──────────────────────────────────────────────

class MockLLMProvider(LLMProvider):
    """
    Mock provider for testing. Returns deterministic responses.
    This is critical for:
    - Unit tests (no API calls, no costs)
    - CI/CD pipelines
    - Local development without API keys
    """

    def __init__(self, default_response: str = "This is a mock response."):
        self.default_response = default_response
        self.call_count = 0

    async def complete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        # YOUR CODE HERE
        # - Simulate latency (50-200ms)
        # - Return deterministic response
        # - Track call_count
        pass

    async def embed(self, text: str, model: str | None = None) -> EmbeddingResponse:
        # YOUR CODE HERE
        # - Return a fixed-dimension vector (e.g., 1536 dimensions)
        # - Make it deterministic based on text (so same text = same embedding)
        # Hint: use hash(text) to seed random for determinism
        pass

    def count_tokens(self, text: str) -> int:
        # Approximate: ~4 chars per token
        return len(text) // 4

    @property
    def provider_name(self) -> str:
        return "mock"


# ──────────────────────────────────────────────
# Exercise 3: OpenAI Provider
# Wraps the OpenAI API behind our adapter interface.
# ──────────────────────────────────────────────

class OpenAIProvider(LLMProvider):
    """
    OpenAI adapter. Wraps the openai library.
    Falls back gracefully if openai is not installed.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._client = None
        try:
            from openai import AsyncOpenAI
            self._client = AsyncOpenAI(api_key=self.api_key)
        except ImportError:
            print("Warning: openai package not installed. Use MockLLMProvider for testing.")

    async def complete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        # YOUR CODE HERE
        # - Use self._client.chat.completions.create()
        # - Map the response to LLMResponse dataclass
        # - Measure latency
        # - Handle errors gracefully
        pass

    async def embed(self, text: str, model: str | None = None) -> EmbeddingResponse:
        # YOUR CODE HERE
        # - Use self._client.embeddings.create()
        # - Default model: "text-embedding-3-small"
        pass

    def count_tokens(self, text: str) -> int:
        # Approximate — for exact count, use tiktoken
        return len(text) // 4

    @property
    def provider_name(self) -> str:
        return "openai"


# ──────────────────────────────────────────────
# Exercise 4: Anthropic Provider (Claude)
# Same interface, different provider.
# ──────────────────────────────────────────────

class AnthropicProvider(LLMProvider):
    """
    Anthropic (Claude) adapter.
    Note: Anthropic doesn't have an embedding API — we handle this.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self._client = None
        try:
            from anthropic import AsyncAnthropic
            self._client = AsyncAnthropic(api_key=self.api_key)
        except ImportError:
            print("Warning: anthropic package not installed.")

    async def complete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        # YOUR CODE HERE
        # - Use self._client.messages.create()
        # - Note: Anthropic uses "system" differently than OpenAI
        # - Map response to LLMResponse
        pass

    async def embed(self, text: str, model: str | None = None) -> EmbeddingResponse:
        # Anthropic doesn't have embeddings — raise NotImplementedError
        # or fall back to a different provider
        raise NotImplementedError(
            "Anthropic does not provide embedding models. "
            "Use OpenAI or a local model for embeddings."
        )

    def count_tokens(self, text: str) -> int:
        return len(text) // 4

    @property
    def provider_name(self) -> str:
        return "anthropic"


# ──────────────────────────────────────────────
# Exercise 5: Provider Factory
# Creates the right provider from a config string.
# ──────────────────────────────────────────────

def create_llm_provider(provider: str = "auto") -> LLMProvider:
    """
    Factory function. Creates an LLM provider based on config.

    Args:
        provider: One of "openai", "anthropic", "mock", "auto"
                  "auto" checks for API keys and picks the best available

    Returns:
        An LLMProvider instance
    """
    # YOUR CODE HERE
    # "mock" → MockLLMProvider
    # "openai" → OpenAIProvider (if key available)
    # "anthropic" → AnthropicProvider (if key available)
    # "auto" → check env vars, pick first available, fall back to mock
    pass


# ──────────────────────────────────────────────
# Exercise 6: Provider with Automatic Fallback
# If primary provider fails, try the secondary.
# ──────────────────────────────────────────────

class FallbackProvider(LLMProvider):
    """
    Wraps multiple providers with automatic fallback.
    If the primary fails, tries secondary, then tertiary, etc.
    """

    def __init__(self, providers: list[LLMProvider]):
        if not providers:
            raise ValueError("At least one provider required")
        self.providers = providers

    async def complete(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> LLMResponse:
        """
        Try each provider in order. Return first successful response.
        Log which provider was used and any failures.
        """
        errors = []
        for provider in self.providers:
            try:
                result = await provider.complete(messages, model, temperature, max_tokens)
                if errors:
                    print(f"Fallback: {provider.provider_name} succeeded after {len(errors)} failures")
                return result
            except Exception as e:
                errors.append((provider.provider_name, str(e)))
                print(f"Fallback: {provider.provider_name} failed: {e}")
        raise RuntimeError(f"All providers failed: {errors}")

    async def embed(self, text: str, model: str | None = None) -> EmbeddingResponse:
        # YOUR CODE HERE — same fallback pattern
        pass

    def count_tokens(self, text: str) -> int:
        return self.providers[0].count_tokens(text)

    @property
    def provider_name(self) -> str:
        return f"fallback({','.join(p.provider_name for p in self.providers)})"


# ──────────────────────────────────────────────
# Demo / Test
# ──────────────────────────────────────────────

async def demo():
    # Test with mock provider (always works, no API key needed)
    print("--- Mock Provider ---")
    mock = MockLLMProvider()
    response = await mock.complete([
        {"role": "user", "content": "What is Python?"}
    ])
    print(f"Provider: {response.provider}")
    print(f"Response: {response.content}")
    print(f"Tokens: {response.input_tokens} in, {response.output_tokens} out")
    print(f"Latency: {response.latency_ms:.0f}ms")

    # Test factory
    print("\n--- Factory (auto) ---")
    provider = create_llm_provider("auto")
    print(f"Auto-selected: {provider.provider_name}")

    # Test fallback
    print("\n--- Fallback Provider ---")
    fallback = FallbackProvider([
        # OpenAIProvider(),  # might fail without key
        MockLLMProvider(default_response="Fallback response works!"),
    ])
    response = await fallback.complete([
        {"role": "user", "content": "Hello!"}
    ])
    print(f"Provider: {response.provider}")
    print(f"Response: {response.content}")


if __name__ == "__main__":
    asyncio.run(demo())

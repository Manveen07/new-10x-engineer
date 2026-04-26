"""
Day 14: LLM Provider Adapter

Goal:
    Keep application routes independent from OpenAI, Anthropic, Ollama, or any
    future provider. The capstone route should call an interface only.

Capstone output:
    Implement app/providers/base.py, mock.py, openai.py, anthropic.py, and registry.py.
"""

import asyncio
import hashlib
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ChatRequest:
    messages: list[ChatMessage]
    model: str
    temperature: float = 0.0
    max_tokens: int = 512


@dataclass(frozen=True)
class ChatResponse:
    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    estimated_cost_usd: float
    finish_reason: str


@dataclass(frozen=True)
class StreamEvent:
    type: str
    data: str | dict[str, object]


class ChatProvider(Protocol):
    name: str

    async def generate(self, request: ChatRequest) -> ChatResponse: ...

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]: ...


class MockProvider:
    name = "mock"

    async def generate(self, request: ChatRequest) -> ChatResponse:
        start = time.perf_counter()
        await asyncio.sleep(0.02)
        prompt = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
        text = f"Mock answer {digest}: {prompt[:120]}"
        return ChatResponse(
            text=text,
            provider=self.name,
            model=request.model,
            input_tokens=max(1, len(prompt) // 4),
            output_tokens=max(1, len(text) // 4),
            latency_ms=(time.perf_counter() - start) * 1000,
            estimated_cost_usd=0.0,
            finish_reason="stop",
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        response = await self.generate(request)
        for token in response.text.split():
            yield StreamEvent(type="token", data=token)
        yield StreamEvent(type="done", data={"finish_reason": response.finish_reason})


PROVIDER_TASKS = [
    "Implement MockProvider first; tests depend on it.",
    "Implement OpenAIProvider behind the same ChatProvider interface.",
    "Implement AnthropicProvider behind the same ChatProvider interface.",
    "Add provider factory from settings.default_provider.",
    "Add timeout and bounded retry wrapper outside provider SDK details.",
    "Persist ChatResponse metadata in provider_calls.",
]


async def main() -> None:
    provider = MockProvider()
    response = await provider.generate(
        ChatRequest(
            messages=[ChatMessage(role="user", content="What is provider abstraction?")],
            model="mock-chat",
        )
    )
    print(response)
    print("\nTasks:")
    for task in PROVIDER_TASKS:
        print(f"- {task}")


if __name__ == "__main__":
    asyncio.run(main())

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class ChatMessage:
    role: str
    content: str


@dataclass(slots=True)
class ChatRequest:
    messages: list[ChatMessage]
    model: str
    temperature: float = 0.0
    max_tokens: int = 512


@dataclass(slots=True)
class ChatResponse:
    text: str
    provider: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_ms: float | None = None
    estimated_cost_usd: float | None = None
    finish_reason: str | None = None


@dataclass(slots=True)
class StreamEvent:
    type: str
    data: str | dict[str, str | None]


class ChatProvider(Protocol):
    name: str

    async def generate(self, request: ChatRequest) -> ChatResponse: ...
    def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]: ...

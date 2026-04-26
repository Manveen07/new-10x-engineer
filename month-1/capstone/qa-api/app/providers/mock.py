import asyncio
import hashlib
from collections.abc import AsyncIterator

from app.providers.base import ChatMessage, ChatRequest, ChatResponse, StreamEvent


class MockChatProvider:
    """Deterministic provider for local development and tests."""

    name = "mock"

    def __init__(self, model: str = "mock-chat", latency_ms: float = 25.0) -> None:
        self.model = model
        self.latency_ms = latency_ms

    async def generate(self, request: ChatRequest) -> ChatResponse:
        await asyncio.sleep(self.latency_ms / 1000)
        user_text = _last_user_message(request.messages)
        digest = hashlib.sha256(user_text.encode("utf-8")).hexdigest()[:8]
        text = f"Mock answer for {digest}: {user_text[:120]}"

        return ChatResponse(
            text=text,
            provider=self.name,
            model=request.model or self.model,
            input_tokens=_rough_token_count(user_text),
            output_tokens=_rough_token_count(text),
            latency_ms=self.latency_ms,
            estimated_cost_usd=0.0,
            finish_reason="stop",
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[StreamEvent]:
        response = await self.generate(request)
        for token in response.text.split():
            yield StreamEvent(type="token", data=token)
        yield StreamEvent(type="done", data={"finish_reason": response.finish_reason})


def _last_user_message(messages: list[ChatMessage]) -> str:
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return messages[-1].content if messages else ""


def _rough_token_count(text: str) -> int:
    return max(1, len(text) // 4)

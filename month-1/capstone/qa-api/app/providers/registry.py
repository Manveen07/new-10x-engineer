from app.config import settings
from app.providers.base import ChatProvider
from app.providers.mock import MockChatProvider


def build_chat_provider() -> ChatProvider:
    provider_name = settings.default_provider
    if provider_name == "mock":
        return MockChatProvider(model=settings.default_model)
    if provider_name == "openai":
        raise NotImplementedError("OpenAI provider not yet implemented.")
    if provider_name == "anthropic":
        raise NotImplementedError("Anthropic provider not yet implemented.")
    if provider_name == "ollama":
        raise NotImplementedError("Ollama provider not yet implemented.")
    raise ValueError(f"Unknown provider configured: {provider_name}")

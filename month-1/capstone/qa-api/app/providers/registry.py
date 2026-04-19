from app.config import settings
from app.providers.base import ChatProvider

def build_chat_provider() -> ChatProvider:
    provider_name = settings.default_provider
    if provider_name == "openai":
        # Return generic OpenAI provider stub
        raise NotImplementedError("OpenAI provider not yet implemented.")
    elif provider_name == "anthropic":
        raise NotImplementedError("Anthropic provider not yet implemented.")
    elif provider_name == "ollama":
        raise NotImplementedError("Ollama provider not yet implemented.")
    else:
        raise ValueError(f"Unknown provider configured: {provider_name}")

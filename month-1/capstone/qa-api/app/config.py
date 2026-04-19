from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application settings
    app_env: Literal["local", "staging", "production"] = "local"
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+asyncpg://month1:month1@localhost:5432/month1"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str = "INSECURE_LOCAL_SECRET_KEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Cache Configuration
    exact_cache_ttl_seconds: int = 3600
    semantic_cache_ttl_seconds: int = 86400

    # LLM Providers
    default_provider: Literal["openai", "anthropic", "ollama"] = "openai"
    default_model: str = "gpt-3.5-turbo"
    openai_api_key: str = ""
    anthropic_api_key: str = ""


settings = Settings()

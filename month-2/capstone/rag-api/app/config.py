from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application settings
    app_name: str = "month2-rag-api"
    app_env: Literal["local", "staging", "production"] = "local"
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+asyncpg://month2:month2@localhost:5432/month2"

    # Redis
    redis_url: str = "redis://localhost:6379/1"  # Using DB 1 for Month 2

    # Security
    secret_key: str  # Required, no default
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Cache Configuration
    exact_cache_ttl_seconds: int = 3600
    semantic_cache_ttl_seconds: int = 86400

    # RAG Configuration
    vector_backend: Literal["pgvector"] = "pgvector"
    lexical_backend: Literal["postgres_fts"] = "postgres_fts"
    default_top_k: int = 10
    default_rerank_top_k: int = 5
    rrf_k: int = 60
    semantic_threshold: float = 0.93
    embedding_provider: Literal["mock", "openai", "sentence_transformers"] = "mock"
    embedding_model: str = "mock-embedding"
    embedding_dimensions: int = 1536
    reranker_provider: Literal["mock", "cohere", "cross_encoder", "disabled"] = "mock"
    reranker_model: str = "mock-reranker"

    # LLM Providers
    default_provider: Literal["mock", "openai", "anthropic", "ollama"] = "mock"
    default_model: str = "mock-chat"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None


settings = Settings()

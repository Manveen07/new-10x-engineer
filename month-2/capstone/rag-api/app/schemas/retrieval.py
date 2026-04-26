import hashlib
import json
from typing import Literal

from pydantic import BaseModel, Field


RetrievalMode = Literal["dense", "lexical", "hybrid", "hybrid_reranked"]


class RetrievalConfig(BaseModel):
    """Versioned retrieval config used for benchmark reproducibility."""

    retrieval_mode: RetrievalMode = "hybrid"
    embedding_provider: str = "mock"
    embedding_model: str = "mock-embedding"
    reranker_provider: str = "mock"
    reranker_model: str = "mock-reranker"

    top_k: int = Field(default=10, ge=1, le=50)
    dense_top_k: int = Field(default=40, ge=1, le=200)
    lexical_top_k: int = Field(default=40, ge=1, le=200)
    rerank_top_k: int = Field(default=10, ge=0, le=50)
    rrf_k: int = Field(default=60, ge=1, le=200)

    splitter_type: str = "recursive"
    chunk_size_tokens: int = Field(default=700, ge=100, le=2_000)
    chunk_overlap_tokens: int = Field(default=80, ge=0, le=500)
    corpus_version: str = "v1"

    ann_enabled: bool = False
    hnsw_ef_search: int = Field(default=64, ge=1, le=1_000)

    def to_hash(self) -> str:
        config_str = json.dumps(self.model_dump(), sort_keys=True)
        return hashlib.sha256(config_str.encode("utf-8")).hexdigest()


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2_000)
    tenant_id: str = Field(default="demo", min_length=1, max_length=120)
    config: RetrievalConfig = Field(default_factory=RetrievalConfig)


class SearchResult(BaseModel):
    chunk_id: int | str
    document_id: int | str
    text: str
    source_uri: str | None = None
    title: str | None = None
    dense_score: float | None = None
    lexical_score: float | None = None
    fused_score: float | None = None
    rerank_score: float | None = None
    final_rank: int


class SearchTrace(BaseModel):
    retrieval_config_hash: str
    dense_count: int = 0
    lexical_count: int = 0
    fused_count: int = 0
    reranked_count: int = 0
    latency_ms_by_stage: dict[str, float] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    query: str
    tenant_id: str
    results: list[SearchResult]
    trace: SearchTrace


class AnswerRequest(SearchRequest):
    answer_style: Literal["concise", "detailed"] = "concise"


class Citation(BaseModel):
    chunk_id: int | str
    document_id: int | str
    source_uri: str | None = None
    quote: str | None = None


class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation]
    search: SearchResponse
    provider: str = "mock"
    model: str = "mock-chat"
    latency_ms: float | None = None

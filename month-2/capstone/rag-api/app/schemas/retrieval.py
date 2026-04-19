import hashlib
import json
from pydantic import BaseModel, Field
from typing import Optional, Literal


class RetrievalConfig(BaseModel):
    """
    Configures the parameters for a retrieval run.
    The hash of this object is used to correlate retrieval performance
    across different strategies.
    """
    retrieval_mode: Literal["dense", "lexical", "hybrid", "hyde_hybrid"] = "dense"
    embedding_model: str = "text-embedding-3-small"
    reranker_model: Optional[str] = "cross-encoder/ms-marco-MiniLM-L6-v2"
    
    # Retrieval parameters
    top_k: int = 10
    dense_weight: float = 0.5
    lexical_weight: float = 0.5
    rrf_k: int = 60
    
    # Reranking
    reranker_enabled: bool = True
    rerank_top_k: int = 5
    
    # Chunking baseline (tracked for reproducibility)
    splitter_type: str = "recursive"
    chunk_size: int = 800
    chunk_overlap: int = 120
    
    # Indexing params
    ann_enabled: bool = False  # Start with exact search per redlines
    hnsw_ef_search: int = 64
    
    # Versioning
    corpus_version: str = "v1"

    def to_hash(self) -> str:
        """
        Generates a stable SHA256 hash of the configuration.
        """
        # Sort keys to ensure stability
        config_str = json.dumps(self.model_dump(), sort_keys=True)
        return hashlib.sha256(config_str.encode("utf-8")).hexdigest()

    def __hash__(self):
        return hash(self.to_hash())

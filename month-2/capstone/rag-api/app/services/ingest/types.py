from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class LoadedDocument(BaseModel):
    """
    Normalized shape for raw document extraction.
    """
    text: str
    source_uri: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    title: Optional[str] = None

class ChunkDraft(BaseModel):
    """
    Normalized shape for generated chunks before persistence.
    """
    text: str
    chunk_index: int
    token_count: int
    splitter_type: str
    chunk_overlap: int
    metadata: Dict[str, Any] = Field(default_factory=dict)

class IngestResult(BaseModel):
    """
    Summary result of an ingestion run.
    """
    document_id: Optional[int] = None
    chunks_created: int = 0
    status: str
    reason: Optional[str] = None

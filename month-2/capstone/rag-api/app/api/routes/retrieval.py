from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.db.models import Chunk
from app.schemas.retrieval import RetrievalConfig

router = APIRouter(prefix="/v1/retrieval", tags=["retrieval"])

@router.post("/search")
async def search(
    query: str,
    config: RetrievalConfig,
    db: AsyncSession = Depends(get_db)
):
    """
    Perform dense vector search against the indexed chunks.
    Baseline (Week 1): Exact search only.
    """
    # For Week 1: We assume the embedding is provided externally or 
    # we call our provider here. For now, this is a skeleton 
    # ensuring the route is registered and config is hashable.
    
    # Example exact search logic (to be fully implemented in Friday's logic)
    # query_embedding = await provider.embed(query)
    # stmt = select(Chunk).order_by(Chunk.embedding.cosine_distance(query_embedding)).limit(config.top_k)
    
    return {
        "query": query,
        "config_hash": config.to_hash(),
        "results": []  # Friday's implementation logic
    }

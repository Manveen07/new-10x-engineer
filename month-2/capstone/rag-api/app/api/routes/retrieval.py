import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.retrieval import (
    AnswerRequest,
    AnswerResponse,
    SearchRequest,
    SearchResponse,
    SearchTrace,
)


router = APIRouter(prefix="/v1", tags=["retrieval"])


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest, db: AsyncSession = Depends(get_db)) -> SearchResponse:
    """Search tenant chunks with the configured retrieval strategy.

    The current scaffold returns an empty traceable response. The exercises
    fill in dense pgvector, PostgreSQL FTS, RRF, and reranking stages.
    """
    _ = db
    start = time.perf_counter()
    trace = SearchTrace(
        retrieval_config_hash=request.config.to_hash(),
        latency_ms_by_stage={"scaffold_ms": (time.perf_counter() - start) * 1000},
    )
    return SearchResponse(query=request.query, tenant_id=request.tenant_id, results=[], trace=trace)


@router.post("/answer", response_model=AnswerResponse)
async def answer(request: AnswerRequest, db: AsyncSession = Depends(get_db)) -> AnswerResponse:
    """Answer with citations from retrieved chunks.

    The current scaffold intentionally answers safely until retrieval and
    generation are implemented.
    """
    search_response = await search(request, db)
    return AnswerResponse(
        answer="I don't know yet because retrieval is not implemented in this scaffold.",
        citations=[],
        search=search_response,
    )

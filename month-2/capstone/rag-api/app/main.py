import structlog
from fastapi import FastAPI, Response
from sqlalchemy import text

from app.clients.redis import get_redis_client
from app.config import settings
from app.db.session import AsyncSessionLocal
from app.lifespan import lifespan
from app.logging import setup_logging
from app.observability import setup_observability


setup_logging(settings.log_level)
logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Month 2 RAG API",
        version="0.1.0",
        description="Retrieval engineering platform with pgvector, hybrid retrieval, reranking, and evals.",
        lifespan=lifespan,
    )

    setup_observability(app)

    from app.api.routes import retrieval

    app.include_router(retrieval.router)

    @app.get("/")
    async def root() -> dict[str, str]:
        logger.info("rag_root_requested")
        return {"message": "Month 2 RAG API is running.", "status": "ready", "version": "0.1.0"}

    @app.get("/health/live")
    async def liveness() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/health/ready")
    async def readiness() -> Response | dict[str, str]:
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
        except Exception:
            logger.exception("readiness_database_failed")
            return Response(
                content='{"status": "unready", "reason": "database"}',
                status_code=503,
                media_type="application/json",
            )

        try:
            redis = get_redis_client()
            await redis.ping()
        except Exception:
            logger.exception("readiness_redis_failed")
            return Response(
                content='{"status": "unready", "reason": "redis"}',
                status_code=503,
                media_type="application/json",
            )

        return {"status": "ready"}

    return app


app = create_app()

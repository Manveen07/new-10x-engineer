from fastapi import FastAPI
import logging

from app.config import settings
from app.lifespan import lifespan
from app.logging import setup_logging
from app.observability import setup_observability

# Initialize logging before FastAPI boots
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Month 2 RAG API",
        version="0.1.0",
        description="Retrieval Engineering Platform with hybrid search and evaluation.",
        lifespan=lifespan,
    )
    
    # Initialize OpenTelemetry
    setup_observability(app)
    
    @app.get("/")
    async def root():
        return {
            "message": "Month 2 RAG API is running.",
            "status": "ready",
            "version": "0.1.0"
        }

    @app.get("/health/live")
    async def liveness():
        return {"status": "alive"}

    @app.get("/health/ready")
    async def readiness():
        from sqlalchemy import text
        from app.db.session import AsyncSessionLocal
        from app.clients.redis import get_redis_client
        
        # 1. Check DB
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
        except Exception:
            return {"status": "unready", "reason": "database"}
            
        # 2. Check Redis
        try:
            redis = get_redis_client()
            await redis.ping()
        except Exception:
            return {"status": "unready", "reason": "redis"}
            
        return {"status": "ready"}

    return app

app = create_app()

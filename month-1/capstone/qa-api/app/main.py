import structlog
from fastapi import FastAPI

from app.config import settings
from app.lifespan import lifespan
from app.logging import setup_logging
from app.observability import setup_observability

setup_logging(settings.log_level)
logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Month 1 QA API",
        version="0.1.0",
        lifespan=lifespan,
    )

    setup_observability(app)

    @app.get("/")
    async def root() -> dict[str, str]:
        logger.info("root_requested")
        return {"message": "Month 1 QA API is running."}

    return app


app = create_app()

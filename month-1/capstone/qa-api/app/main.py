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
        title="Month 1 QA API",
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # Initialize OpenTelemetry
    setup_observability(app)
    
    @app.get("/")
    async def root():
        return {"message": "Month 1 QA API is running."}

    return app

app = create_app()

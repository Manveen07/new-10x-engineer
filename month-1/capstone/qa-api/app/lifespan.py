import httpx
import redis.asyncio as redis
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from app.clients import http, redis as redis_client_module
from app.config import settings

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Initializing shared clients...")
    
    # Initialize HTTPx client
    http.http_client = httpx.AsyncClient(timeout=60.0)
    
    # Initialize Redis client
    redis_client_module.redis_client = redis.from_url(
        settings.redis_url, 
        encoding="utf-8", 
        decode_responses=True
    )

    try:
        yield
    finally:
        logger.info("Closing shared clients...")
        if http.http_client:
            await http.http_client.aclose()
        if redis_client_module.redis_client:
            await redis_client_module.redis_client.aclose()

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
import redis.asyncio as redis
import structlog
from fastapi import FastAPI

from app.clients import http
from app.clients import redis as redis_client_module
from app.config import settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("shared_clients_starting")

    http.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)
    )
    redis_client_module.redis_client = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )

    try:
        yield
    finally:
        logger.info("shared_clients_closing")
        if http.http_client is not None:
            await http.http_client.aclose()
            http.http_client = None
        if redis_client_module.redis_client is not None:
            await redis_client_module.redis_client.aclose()
            redis_client_module.redis_client = None

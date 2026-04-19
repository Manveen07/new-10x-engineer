import redis.asyncio as redis
from app.config import settings

# Shared Redis client for the application instance
redis_client: redis.Redis | None = None

def get_redis_client() -> redis.Redis:
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized. Ensure it is started via the app lifespan.")
    return redis_client

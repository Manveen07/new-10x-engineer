from collections.abc import Callable, Awaitable
from typing import TypeVar
import asyncio

T = TypeVar("T")


async def with_retry(
    fn: Callable[[], Awaitable[T]],
    attempts: int = 3,
    backoff: float = 0.5,
) -> T:
    """Call fn() up to `attempts` times. On exception: sleep `backoff` seconds,
    double backoff, retry. After all attempts fail, re-raise last exception."""
    for i in range(attempts):
        try:
            return await fn()
        except Exception:
            if i == (attempts - 1):
                raise
            else:
                await asyncio.sleep(backoff)
                backoff *= 2

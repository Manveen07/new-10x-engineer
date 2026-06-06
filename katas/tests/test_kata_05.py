import pytest
from kata_05_typing import with_retry


@pytest.mark.asyncio
async def test_succeeds_first_try():
    async def fn():
        return 42

    result = await with_retry(fn)
    assert result == 42


@pytest.mark.asyncio
async def test_retries_on_failure():
    calls = {"count": 0}

    async def flaky():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("not yet")
        return "ok"

    result = await with_retry(flaky, attempts=3, backoff=0.01)
    assert result == "ok"
    assert calls["count"] == 2


@pytest.mark.asyncio
async def test_raises_after_all_attempts():
    async def always_fails():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        await with_retry(always_fails, attempts=2, backoff=0.01)

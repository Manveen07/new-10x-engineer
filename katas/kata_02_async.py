import httpx
import asyncio


async def fetch_one(client: httpx.AsyncClient, url: str) -> dict:
    r = await client.get(url)
    return {"url": url, "status": r.status_code, "size": len(r.content)}


async def fetch_many(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        coros = [fetch_one(client, url) for url in urls]
        return await asyncio.gather(*coros)


if __name__ == "__main__":
    urls = ["https://example.com", "https://www.python.org", "https://github.com"]

    results = asyncio.run(fetch_many(urls))
    for r in results:
        print(r)

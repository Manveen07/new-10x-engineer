import httpx

# Shared HTTP client for the application instance
http_client: httpx.AsyncClient | None = None

def get_http_client() -> httpx.AsyncClient:
    if http_client is None:
        raise RuntimeError("HTTP client is not initialized. Ensure it is started via the app lifespan.")
    return http_client

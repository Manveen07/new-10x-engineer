"""
Week 2 - Day 4: Middleware, CORS, and Rate Limiting
=====================================================

Middleware is code that runs BEFORE and AFTER every request.
In AI backends, middleware handles: logging, timing, rate limiting
(critical for expensive LLM calls), CORS, and request tracing.

Pre-req: pip install fastapi uvicorn slowapi

Run with: uvicorn day9_middleware:app --reload
"""

import time
import uuid
import logging
from collections import defaultdict

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="Middleware Exercises")


# ══════════════════════════════════════════════
# Exercise 1: Request ID Middleware
# ══════════════════════════════════════════════
#
# Every request gets a unique ID. This ID appears in:
# - Response headers (X-Request-ID)
# - All log messages for this request
# - Error responses
#
# WHY: When debugging production issues, you need to trace
# a single request through your entire system. "What happened
# to request abc-123?" becomes answerable.

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID to every request.
    - Checks for incoming X-Request-ID header (from upstream proxy)
    - If none, generates a new UUID
    - Adds it to response headers
    - Makes it available to route handlers via request.state
    """

    async def dispatch(self, request: Request, call_next):
        # YOUR CODE HERE
        # 1. Check for existing X-Request-ID header
        # 2. If not present, generate UUID
        # 3. Store on request.state.request_id
        # 4. Call next middleware/handler
        # 5. Add X-Request-ID to response headers

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ══════════════════════════════════════════════
# Exercise 2: Timing Middleware
# ══════════════════════════════════════════════
#
# Measure how long each request takes.
# Add X-Process-Time header to response.
# Log slow requests (>1s) as warnings.

class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measures request processing time.
    - Adds X-Process-Time header (milliseconds)
    - Logs warnings for slow requests (>1000ms)
    """

    async def dispatch(self, request: Request, call_next):
        # YOUR CODE HERE
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"

        if duration_ms > 1000:
            logger.warning(
                f"SLOW REQUEST: {request.method} {request.url.path} "
                f"took {duration_ms:.0f}ms"
            )

        return response


# ══════════════════════════════════════════════
# Exercise 3: Request Logging Middleware
# ══════════════════════════════════════════════
#
# Log every request with: method, path, status, duration, request_id.
# This is your audit trail.
#
# Format: [request_id] METHOD /path -> STATUS (duration_ms)
# Example: [abc-123] POST /qa/ask -> 200 (1523ms)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Structured request logging.
    Logs: request_id, method, path, status_code, duration_ms.
    """

    async def dispatch(self, request: Request, call_next):
        # YOUR CODE HERE
        request_id = getattr(request.state, "request_id", "unknown")
        start = time.perf_counter()

        # Log incoming request
        logger.info(
            f"[{request_id}] --> {request.method} {request.url.path}"
        )

        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        # Log completed request
        logger.info(
            f"[{request_id}] <-- {request.method} {request.url.path} "
            f"-> {response.status_code} ({duration_ms:.0f}ms)"
        )

        return response


# ══════════════════════════════════════════════
# Exercise 4: Simple Rate Limiter
# ══════════════════════════════════════════════
#
# Limit requests per IP address per minute.
# This is CRITICAL for AI endpoints — LLM calls cost money.
# Without rate limiting, one user can burn your entire API budget.
#
# This is a simple in-memory implementation.
# Production: use Redis-backed rate limiting (Week 4).

class SimpleRateLimiter:
    """
    In-memory sliding window rate limiter.

    Tracks request timestamps per client IP.
    Rejects requests that exceed the limit with 429 Too Many Requests.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        """
        Check if the client is within rate limits.

        YOUR CODE HERE:
        1. Get current time
        2. Remove timestamps older than 60 seconds
        3. Check if count < limit
        4. If allowed, add current timestamp
        5. Return True/False
        """
        now = time.time()
        window_start = now - 60

        # Remove old timestamps
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip] if ts > window_start
        ]

        if len(self.requests[client_ip]) >= self.rpm:
            return False

        self.requests[client_ip].append(now)
        return True

    def remaining(self, client_ip: str) -> int:
        """How many requests remain in the current window."""
        now = time.time()
        window_start = now - 60
        recent = [ts for ts in self.requests[client_ip] if ts > window_start]
        return max(0, self.rpm - len(recent))


# Global rate limiter instances
default_limiter = SimpleRateLimiter(requests_per_minute=60)
expensive_limiter = SimpleRateLimiter(requests_per_minute=10)  # For LLM endpoints


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Apply rate limiting based on endpoint path.
    - /qa/* endpoints: 10 req/min (expensive LLM calls)
    - Everything else: 60 req/min
    """

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        # Choose limiter based on path
        if request.url.path.startswith("/qa"):
            limiter = expensive_limiter
        else:
            limiter = default_limiter

        if not limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": {
                        "code": "RATE_LIMITED",
                        "message": "Too many requests. Please try again later.",
                        "retry_after_seconds": 60,
                    }
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(limiter.remaining(client_ip))
        return response


# ══════════════════════════════════════════════
# Exercise 5: CORS Configuration
# ══════════════════════════════════════════════
#
# CORS (Cross-Origin Resource Sharing) is required when
# your frontend and backend are on different domains.
#
# Common AI app setup:
#   Frontend: https://app.yoursite.com (React/Next.js)
#   Backend:  https://api.yoursite.com (FastAPI)
#
# Without CORS config, the browser blocks frontend→backend requests.

app.add_middleware(
    CORSMiddleware,
    # YOUR CODE HERE — configure these:
    allow_origins=[
        "http://localhost:3000",       # Local React dev
        "http://localhost:5173",       # Local Vite dev
        "https://app.yoursite.com",    # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time", "X-RateLimit-Remaining"],
)


# ══════════════════════════════════════════════
# Register middleware (ORDER MATTERS!)
# ══════════════════════════════════════════════
#
# Middleware executes in REVERSE order of registration.
# Last added = first to execute.
#
# We want this execution order:
# 1. RequestID (first — everything else needs the ID)
# 2. Timing (wraps everything to measure total time)
# 3. Logging (logs with request ID and timing info)
# 4. RateLimit (reject before doing expensive work)
# 5. Route handler

app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIDMiddleware)


# ══════════════════════════════════════════════
# Test Endpoints
# ══════════════════════════════════════════════

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/slow")
async def slow_endpoint():
    """Simulates a slow endpoint to test timing middleware."""
    import asyncio
    await asyncio.sleep(1.5)
    return {"message": "This was slow"}


@app.post("/qa/ask")
async def ask_question(request: Request):
    """
    Simulates an expensive LLM endpoint.
    Rate limited to 10 req/min.
    """
    import asyncio
    await asyncio.sleep(0.5)  # Simulate LLM latency
    return {
        "answer": "This is a mock answer",
        "request_id": getattr(request.state, "request_id", "unknown"),
    }


# ══════════════════════════════════════════════
# Testing Guide
# ══════════════════════════════════════════════
#
# 1. Start server: uvicorn day9_middleware:app --reload
#
# 2. Check headers:
#    curl -v http://localhost:8000/health
#    → Look for X-Request-ID, X-Process-Time, X-RateLimit-Remaining
#
# 3. Test slow endpoint:
#    curl http://localhost:8000/slow
#    → Check server logs for SLOW REQUEST warning
#
# 4. Test rate limiting:
#    for i in $(seq 1 15); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/qa/ask -X POST; done
#    → First 10 should return 200, rest should return 429
#
# 5. Test CORS (from browser console):
#    fetch('http://localhost:8000/health').then(r => r.json()).then(console.log)

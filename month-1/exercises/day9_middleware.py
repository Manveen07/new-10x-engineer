"""
Day 9: Middleware, Structured Logs, And Rate Limits

Goal:
    Add production API cross-cutting behavior: request IDs, timing, structured
    logs, CORS, error envelopes, and rate limits.

Capstone output:
    Middleware and rate-limit service for the Q&A API.
"""

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class RequestLogEvent:
    request_id: str
    method: str
    path: str
    status_code: int
    latency_ms: float
    user_id: str | None = None
    extra: dict[str, object] = field(default_factory=dict)


def build_request_id(incoming_request_id: str | None = None) -> str:
    return incoming_request_id or str(uuid.uuid4())


def build_request_log(
    method: str,
    path: str,
    status_code: int,
    started_at: float,
    request_id: str,
    user_id: str | None = None,
) -> RequestLogEvent:
    return RequestLogEvent(
        request_id=request_id,
        method=method,
        path=path,
        status_code=status_code,
        latency_ms=(time.perf_counter() - started_at) * 1000,
        user_id=user_id,
    )


RATE_LIMITS = {
    "free": {"qa_per_minute": 10, "general_per_minute": 60},
    "paid": {"qa_per_minute": 100, "general_per_minute": 300},
    "admin": {"qa_per_minute": None, "general_per_minute": None},
}


def print_exercise() -> None:
    print("Day 9: Middleware")
    print("Implement in the capstone:")
    print("- Request ID middleware")
    print("- Timing middleware")
    print("- Structured request log event")
    print("- CORS with explicit origins")
    print("- Redis-backed rate limit buckets")
    print("- 429 error envelope")
    print("\nRate tiers:")
    print(RATE_LIMITS)


if __name__ == "__main__":
    print_exercise()

"""
Day 49: Tool Failure Handling
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ToolErrorPolicy:
    retryable: bool
    max_retries: int
    fallback_route: Literal["retry", "degrade", "fail", "approval"]


POLICIES = {
    "timeout": ToolErrorPolicy(True, 1, "retry"),
    "rate_limit": ToolErrorPolicy(True, 1, "degrade"),
    "permission_denied": ToolErrorPolicy(False, 0, "fail"),
    "high_risk": ToolErrorPolicy(False, 0, "approval"),
}


if __name__ == "__main__":
    print(POLICIES)

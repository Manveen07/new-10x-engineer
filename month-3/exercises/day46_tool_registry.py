"""
Day 46: Tool Registry
"""

from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    risk_level: RiskLevel
    requires_approval: bool
    timeout_seconds: float
    max_retries: int


TOOLS = [
    ToolDefinition("search_corpus", "Search tenant corpus", "low", False, 5.0, 1),
    ToolDefinition("answer_from_corpus", "Answer with citations", "low", False, 15.0, 1),
    ToolDefinition("send_external_message", "Send message outside system", "high", True, 10.0, 0),
]


if __name__ == "__main__":
    print(TOOLS)

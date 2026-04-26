"""
Day 42: LangGraph State Model

Goal:
    Define inspectable state before building graph nodes.
"""

from typing import Literal, TypedDict


class ToolCall(TypedDict):
    tool_name: str
    input: dict[str, object]
    output: dict[str, object] | None
    status: Literal["pending", "ok", "failed", "requires_approval"]


class AgentState(TypedDict):
    run_id: str
    user_id: str
    tenant_id: str
    question: str
    plan: list[str]
    tool_calls: list[ToolCall]
    citations: list[str]
    final_answer: str | None
    step_count: int
    max_steps: int
    status: Literal["running", "waiting_for_approval", "completed", "failed"]


if __name__ == "__main__":
    print("Use AgentState as the contract for every graph node.")

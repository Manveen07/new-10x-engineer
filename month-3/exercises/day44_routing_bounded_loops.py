"""
Day 44: Routing And Bounded Loops
"""

from typing import Literal


Route = Literal["retrieve_again", "request_approval", "done", "fail"]


def route_after_verify(confidence: float, step_count: int, max_steps: int, risky: bool) -> Route:
    if risky:
        return "request_approval"
    if step_count >= max_steps:
        return "fail"
    if confidence < 0.6:
        return "retrieve_again"
    return "done"


if __name__ == "__main__":
    print(route_after_verify(confidence=0.4, step_count=2, max_steps=5, risky=False))

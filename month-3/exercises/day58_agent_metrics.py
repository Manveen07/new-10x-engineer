"""
Day 58: Agent Metrics
"""


def task_success(passed: int, total: int) -> float:
    return passed / total if total else 0.0


def tool_accuracy(expected: list[str], actual: list[str]) -> float:
    if not expected:
        return 1.0 if not actual else 0.0
    matched = sum(1 for tool in actual if tool in expected)
    return matched / len(expected)


def approval_precision(correct_approvals: int, approval_requests: int) -> float:
    return correct_approvals / approval_requests if approval_requests else 1.0


if __name__ == "__main__":
    print(task_success(8, 10))
    print(tool_accuracy(["search", "answer"], ["search", "answer"]))
    print(approval_precision(4, 5))

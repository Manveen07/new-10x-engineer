"""
Day 18: Cache Tuning And Evaluation

Goal:
    Choose the semantic-cache threshold with a small evaluation set.

Capstone output:
    docs/benchmarks/cache-threshold-sweep.md
"""

THRESHOLDS = [0.80, 0.85, 0.88, 0.90, 0.95]

EVAL_CASES = [
    {
        "canonical": "What is async Python?",
        "should_hit": [
            "Explain async Python.",
            "How does asyncio work?",
            "What does await do in Python?",
        ],
        "should_miss": [
            "How do JWT refresh tokens work?",
            "What is a PostgreSQL index?",
        ],
    },
    {
        "canonical": "What is semantic caching?",
        "should_hit": [
            "Explain semantic cache.",
            "How does vector cache matching work?",
        ],
        "should_miss": [
            "How does RBAC work?",
            "What is FastAPI Depends?",
        ],
    },
]

REPORT_TEMPLATE = """
# Cache Threshold Sweep

| Threshold | Hit rate | False positives | False negatives | Avg latency saved ms | Est. cost saved USD |
|---:|---:|---:|---:|---:|---:|
| 0.80 | TBD | TBD | TBD | TBD | TBD |
| 0.85 | TBD | TBD | TBD | TBD | TBD |
| 0.88 | TBD | TBD | TBD | TBD | TBD |
| 0.90 | TBD | TBD | TBD | TBD | TBD |
| 0.95 | TBD | TBD | TBD | TBD | TBD |

Decision:
Use threshold TBD because...

Unsafe cases:
- ...
"""


def print_exercise() -> None:
    print("Day 18: Cache Tuning")
    print("Thresholds:", THRESHOLDS)
    print("\nEvaluation cases:")
    for case in EVAL_CASES:
        print(f"- {case['canonical']}")
    print("\nReport template:")
    print(REPORT_TEMPLATE)


if __name__ == "__main__":
    print_exercise()

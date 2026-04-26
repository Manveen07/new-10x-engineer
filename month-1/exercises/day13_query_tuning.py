"""
Day 13: Query Tuning Patterns

Goal:
    Learn the common rewrites that keep API endpoints fast as data grows.

Capstone output:
    Use these rewrites for /qa/history and /admin/query-stats.
"""

TUNING_CASES = [
    {
        "problem": "Function on indexed column blocks efficient range lookup",
        "bad": "WHERE DATE(created_at) = DATE '2026-04-25'",
        "better": "WHERE created_at >= '2026-04-25' AND created_at < '2026-04-26'",
    },
    {
        "problem": "Offset pagination gets slower on deep pages",
        "bad": "ORDER BY created_at DESC OFFSET 10000 LIMIT 20",
        "better": "WHERE created_at < $cursor ORDER BY created_at DESC LIMIT 20",
    },
    {
        "problem": "Route handler does analytics query repeatedly",
        "bad": "Compute expensive aggregate on every request",
        "better": "Precompute or cache admin stats with a short TTL",
    },
]


def print_exercise() -> None:
    print("Day 13: Query Tuning")
    for case in TUNING_CASES:
        print(f"\nProblem: {case['problem']}")
        print(f"Bad: {case['bad']}")
        print(f"Better: {case['better']}")
    print("\nExercise: capture before/after EXPLAIN output for each.")


if __name__ == "__main__":
    print_exercise()

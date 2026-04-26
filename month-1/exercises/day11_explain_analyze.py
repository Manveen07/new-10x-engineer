"""
Day 11: EXPLAIN ANALYZE

Goal:
    Learn to prove database decisions with query plans.

Capstone output:
    Add notes for the indexes that support auth, query history, provider calls,
    and admin analytics.
"""

CAPSTONE_QUERIES = [
    {
        "name": "login lookup",
        "query": "SELECT * FROM users WHERE email = $1",
        "why": "runs on every login",
    },
    {
        "name": "refresh token lookup",
        "query": "SELECT * FROM refresh_tokens WHERE token_hash = $1 AND revoked_at IS NULL",
        "why": "runs on every token refresh",
    },
    {
        "name": "user query history",
        "query": (
            "SELECT * FROM queries WHERE user_id = $1 "
            "ORDER BY created_at DESC LIMIT 20"
        ),
        "why": "powers /qa/history",
    },
    {
        "name": "admin provider latency",
        "query": (
            "SELECT provider, model, avg(latency_ms) "
            "FROM provider_calls GROUP BY provider, model"
        ),
        "why": "powers /admin/query-stats",
    },
]

PLAN_CHECKLIST = [
    "Run EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON).",
    "Record whether the query uses Seq Scan, Index Scan, Bitmap Scan, Sort, or HashAggregate.",
    "Compare planned rows to actual rows.",
    "Check shared hit/read buffers.",
    "Add or adjust one index.",
    "Run EXPLAIN again and write the before/after result.",
]


def print_exercise() -> None:
    print("Day 11: EXPLAIN ANALYZE")
    for item in CAPSTONE_QUERIES:
        print(f"\n{item['name']}: {item['query']}")
        print(f"Why it matters: {item['why']}")

    print("\nChecklist:")
    for step in PLAN_CHECKLIST:
        print(f"- {step}")


if __name__ == "__main__":
    print_exercise()

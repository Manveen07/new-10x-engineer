"""
Day 12: Indexing Strategies

Goal:
    Add only indexes that match real capstone queries.

Capstone output:
    Include these indexes in the first Alembic migration, then verify with
    EXPLAIN ANALYZE.
"""

INDEX_PLAN = [
    {
        "table": "users",
        "index": "unique btree(email)",
        "query": "login and registration uniqueness",
    },
    {
        "table": "refresh_tokens",
        "index": "unique btree(token_hash)",
        "query": "refresh and logout token lookup",
    },
    {
        "table": "queries",
        "index": "btree(user_id, created_at desc)",
        "query": "paginated /qa/history",
    },
    {
        "table": "provider_calls",
        "index": "btree(query_id)",
        "query": "join provider metadata to query history",
    },
    {
        "table": "provider_calls",
        "index": "btree(provider, model, created_at desc)",
        "query": "admin latency analytics",
    },
    {
        "table": "cache_entries",
        "index": "btree(namespace, cache_key)",
        "query": "cache metadata lookup",
    },
]


def print_exercise() -> None:
    print("Day 12: Indexing Strategies")
    for item in INDEX_PLAN:
        print(f"- {item['table']}: {item['index']} for {item['query']}")
    print("\nExercise: prove each index with EXPLAIN, or remove it.")


if __name__ == "__main__":
    print_exercise()

"""
Day 10: Async Database Integration

Goal:
    Design the capstone PostgreSQL layer: async sessions, migrations, tables,
    repositories, and tests that do not leak DB state.

Capstone output:
    app/clients/db.py, app/models/database.py, repositories, and first migration.
"""

TABLES = {
    "users": [
        "id uuid primary key",
        "email unique not null",
        "display_name not null",
        "hashed_password not null",
        "role user/admin",
        "tier free/paid/admin",
        "is_active boolean",
        "created_at timestamp",
    ],
    "refresh_tokens": [
        "id uuid primary key",
        "user_id foreign key",
        "token_hash unique not null",
        "expires_at timestamp",
        "revoked_at timestamp null",
    ],
    "queries": [
        "id uuid primary key",
        "user_id foreign key",
        "question text",
        "answer text",
        "cache_outcome exact_hit/semantic_hit/miss",
        "latency_ms numeric",
        "created_at timestamp",
    ],
    "provider_calls": [
        "id uuid primary key",
        "query_id foreign key null",
        "provider",
        "model",
        "input_tokens",
        "output_tokens",
        "estimated_cost_usd",
        "latency_ms",
        "status",
        "retry_count",
        "error_type",
        "created_at timestamp",
    ],
    "cache_entries": [
        "id uuid primary key",
        "namespace",
        "cache_key",
        "matched_query",
        "ttl_seconds",
        "created_at timestamp",
    ],
}

REPOSITORY_METHODS = [
    "users.create_user",
    "users.get_by_email",
    "users.get_by_id",
    "refresh_tokens.store_hash",
    "refresh_tokens.revoke",
    "queries.create",
    "queries.list_for_user",
    "provider_calls.create",
    "cache_metadata.record_entry",
]


def print_exercise() -> None:
    print("Day 10: Async Database")
    print("\nTables:")
    for table, columns in TABLES.items():
        print(f"\n{table}")
        for column in columns:
            print(f"- {column}")

    print("\nRepository methods:")
    for method in REPOSITORY_METHODS:
        print(f"- {method}")

    print("\nDone when Alembic can create these tables and repository tests pass.")


if __name__ == "__main__":
    print_exercise()

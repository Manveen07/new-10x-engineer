"""
Day 16: Redis Vector Search

Goal:
    Understand the primitive behind semantic cache: store normalized query
    vectors, search nearest neighbors, and return metadata with a score.

Capstone output:
    Implement Redis client setup and cache index design.
"""

REDIS_INDEX_FIELDS = {
    "key": "cache:{namespace}:{hash}",
    "query": "original normalized user question",
    "answer": "cached answer text",
    "embedding": "float vector bytes",
    "namespace": "cache namespace",
    "created_at": "unix timestamp",
    "ttl_seconds": "expiry",
    "provider": "provider that generated answer",
    "model": "model that generated answer",
}

VECTOR_SEARCH_TASKS = [
    "Start Redis Stack with Docker Compose.",
    "Create a vector index for cache entries.",
    "Insert at least 20 sample question/answer pairs.",
    "Search using a new query embedding.",
    "Return matched_query, answer, score, provider, model, and latency.",
    "Record which similarity threshold looks safe.",
]


def print_exercise() -> None:
    print("Day 16: Redis Vector Search")
    print("\nIndex fields:")
    for field, meaning in REDIS_INDEX_FIELDS.items():
        print(f"- {field}: {meaning}")
    print("\nTasks:")
    for task in VECTOR_SEARCH_TASKS:
        print(f"- {task}")


if __name__ == "__main__":
    print_exercise()

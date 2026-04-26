"""
Day 32: Retrieval Metrics

Goal:
    Implement metrics that score retrieved chunk IDs against relevant chunk IDs.
"""

import math


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top_k = retrieved[:k]
    return sum(1 for item in top_k if item in relevant) / k


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 1.0
    top_k = retrieved[:k]
    return sum(1 for item in top_k if item in relevant) / len(relevant)


def mrr_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    for rank, item in enumerate(retrieved[:k], start=1):
        if item in relevant:
            return 1 / rank
    return 0.0


def ndcg_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    dcg = 0.0
    for rank, item in enumerate(retrieved[:k], start=1):
        if item in relevant:
            dcg += 1 / math.log2(rank + 1)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 1.0


if __name__ == "__main__":
    retrieved_ids = ["c1", "c2", "c3", "c4"]
    relevant_ids = {"c2", "c4"}
    print("p@2", precision_at_k(retrieved_ids, relevant_ids, 2))
    print("r@4", recall_at_k(retrieved_ids, relevant_ids, 4))
    print("mrr@4", mrr_at_k(retrieved_ids, relevant_ids, 4))
    print("ndcg@4", ndcg_at_k(retrieved_ids, relevant_ids, 4))

"""
Day 27: Reciprocal Rank Fusion

Goal:
    Fuse dense and lexical rankings without depending on a RAG framework.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RankedResult:
    chunk_id: str
    rank: int
    score: float
    source: str


@dataclass
class FusedResult:
    chunk_id: str
    fused_score: float = 0.0
    contributions: dict[str, float] = field(default_factory=dict)


def reciprocal_rank_fusion(result_sets: list[list[RankedResult]], k: int = 60) -> list[FusedResult]:
    fused: dict[str, FusedResult] = {}
    for result_set in result_sets:
        for result in result_set:
            contribution = 1 / (k + result.rank)
            item = fused.setdefault(result.chunk_id, FusedResult(chunk_id=result.chunk_id))
            item.fused_score += contribution
            item.contributions[result.source] = contribution
    return sorted(fused.values(), key=lambda item: item.fused_score, reverse=True)


if __name__ == "__main__":
    dense = [RankedResult("a", 1, 0.9, "dense"), RankedResult("b", 2, 0.8, "dense")]
    lexical = [RankedResult("b", 1, 4.0, "lexical"), RankedResult("c", 2, 3.0, "lexical")]
    print(reciprocal_rank_fusion([dense, lexical]))

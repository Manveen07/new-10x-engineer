"""
Day 23: Chunking Experiments

Goal:
    Compare chunking strategies before choosing the default ingestion config.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkingConfig:
    strategy: str
    chunk_size_tokens: int
    overlap_tokens: int

    def slug(self) -> str:
        return f"{self.strategy}-{self.chunk_size_tokens}-{self.overlap_tokens}"


CONFIGS = [
    ChunkingConfig("fixed", 300, 30),
    ChunkingConfig("fixed", 500, 50),
    ChunkingConfig("heading_aware", 500, 50),
    ChunkingConfig("recursive", 700, 80),
]


def estimate_token_count(text: str) -> int:
    return max(1, len(text.split()))


def print_experiment_plan() -> None:
    print("Run these chunk configs against the seed corpus:")
    for config in CONFIGS:
        print(f"- {config.slug()}")
    print("\nRecord chunk count, avg tokens, max tokens, and retrieval metric impact.")


if __name__ == "__main__":
    print_experiment_plan()

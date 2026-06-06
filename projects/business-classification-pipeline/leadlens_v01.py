from pydantic import BaseModel, Field
from typing import Literal


class JobPosting(BaseModel):
    # input echo
    id: str
    title: str
    company: str
    url: str

    # classifier outputs — each field justifies existence by measurability
    seniority: Literal["intern", "junior", "mid", "senior", "staff", "lead", "unclear"]
    ai_authenticity: Literal["real_ai_role", "ai_adjacent", "ai_washed", "non_ai"]
    core_stack: list[str] = Field(
        max_length=20,
        description="Specific frameworks/libraries named: LangGraph, RAG, MCP, PyTorch, Postgres, etc.",
    )
    remote_status: Literal[
        "fully_remote", "hybrid", "onsite", "remote_within_region", "unclear"
    ]
    location_signal: str | None = Field(
        default=None,
        description="'US only' / 'India OK' / 'global' / 'EU only' / None if unclear",
    )
    comp_signal: str | None = Field(
        default=None,
        description="Raw comp string if mentioned, e.g. '$180k-220k', else None",
    )
    red_flags: list[str] = Field(
        default_factory=list,
        description="Issues: 'no comp', 'partnership not job', 'years gap mismatch', etc.",
    )

    # forced-reasoning before fit score — fixes F-003 by construction
    confidence_reasoning: str = Field(
        min_length=100,
        description="Must quote specific evidence from description. No score without reasoning.",
    )
    fit_for_manveen: Literal["strong", "medium", "weak", "skip"] = Field(
        description="Junior AI eng, India-based, US-remote target. Strong=real LLM/RAG role + remote-OK. Skip=onsite-only or senior-only.",
    )

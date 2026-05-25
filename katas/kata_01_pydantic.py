"""Kata 01 — nested Pydantic + parse_company with ValidationError handling."""

from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class Signal(BaseModel):
    name: str
    evidence: str | None
    confidence: float = Field(ge=0, le=1)


class Company(BaseModel):
    name: str
    domain: str | None = Field(
        default=None,
        description="if website is null maybe they don't have a website",
    )
    status: Literal["operating", "closed", "uncertain"]
    signals: list[Signal]


def parse_company(data: dict) -> Company:
    try:
        return Company.model_validate(data)
    except ValidationError as e:
        print(e)
        return Company(name="?", status="uncertain", signals=[])

"""
Day 7: Pydantic V2 Validation And Error Envelopes

Goal:
    Define schemas that protect the API boundary: input validation, output
    shaping, and consistent errors.

Capstone output:
    Add schemas for auth, users, Q&A, health, admin, and errors.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ErrorDetail(BaseModel):
    loc: list[str | int] = Field(default_factory=list)
    message: str
    type: str


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)


class ApiErrorResponse(BaseModel):
    error: ErrorEnvelope


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=1, max_length=80)

    @field_validator("password")
    @classmethod
    def password_must_not_be_common(cls, value: str) -> str:
        common = {"password1234", "letmein12345", "qwerty123456"}
        if value.lower() in common:
            raise ValueError("password is too common")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    display_name: str
    role: Literal["user", "admin"]
    tier: Literal["free", "paid", "admin"]


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2_000)
    cache_namespace: str = Field(default="default", min_length=1, max_length=80)

    @field_validator("question")
    @classmethod
    def question_must_have_signal(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if normalized in {"?", "..."}:
            raise ValueError("question is too vague")
        return normalized


class CacheInfo(BaseModel):
    outcome: Literal["exact_hit", "semantic_hit", "miss"]
    similarity: float | None = None
    matched_query: str | None = None


class ProviderInfo(BaseModel):
    name: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost_usd: float | None = None


class AnswerResponse(BaseModel):
    answer: str
    cache: CacheInfo
    provider: ProviderInfo | None = None
    latency_ms: float
    request_id: str


def print_exercise() -> None:
    print("Day 7: Pydantic Validation")
    print("Add these schema patterns to the capstone.")
    print("Exercise: wire validation errors into ApiErrorResponse.")
    print(QuestionRequest(question="  What is async Python?  ").model_dump())


if __name__ == "__main__":
    print_exercise()

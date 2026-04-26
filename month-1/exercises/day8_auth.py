"""
Day 8: Authentication And RBAC

Goal:
    Build the auth flow used by real APIs: password hashing, access tokens,
    refresh tokens, current-user dependency, and role checks.

Capstone output:
    Implement auth service, auth router, users router, and admin guard.
"""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal


Role = Literal["user", "admin"]
Tier = Literal["free", "paid", "admin"]


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_seconds: int = 900


@dataclass(frozen=True)
class AuthExerciseStep:
    name: str
    output: str


AUTH_STEPS = [
    AuthExerciseStep("register", "hash password and create user"),
    AuthExerciseStep("login", "verify password and issue access/refresh token pair"),
    AuthExerciseStep("refresh", "validate refresh token, rotate access token"),
    AuthExerciseStep("logout", "revoke refresh token"),
    AuthExerciseStep("current user", "decode bearer token and load user"),
    AuthExerciseStep("require admin", "reject non-admin users with 403"),
]


def access_token_payload(user_id: str, role: Role, tier: Tier) -> dict[str, object]:
    """Exercise: sign this payload with PyJWT in the capstone."""
    now = datetime.now(UTC)
    return {
        "sub": user_id,
        "role": role,
        "tier": tier,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=15)).timestamp()),
        "type": "access",
    }


def print_exercise() -> None:
    print("Day 8: Auth And RBAC")
    for step in AUTH_STEPS:
        print(f"- {step.name}: {step.output}")
    print("\nPayload example:")
    print(access_token_payload("user_123", "user", "free"))
    print("\nTests required: register, login, refresh, logout, /users/me, admin rejection.")


if __name__ == "__main__":
    print_exercise()

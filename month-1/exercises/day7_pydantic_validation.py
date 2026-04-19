"""
Week 2 - Day 2: Pydantic V2 Validation & Error Handling
=========================================================

Deep dive into Pydantic V2 — the validation layer that sits
between your API and your business logic. Every request and
response in your AI backends will flow through Pydantic models.

Pre-req: pip install pydantic[email] fastapi uvicorn

Run with: uvicorn day7_pydantic_validation:app --reload
"""

from datetime import datetime, date
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

app = FastAPI(title="Pydantic V2 Validation Exercises")


# ══════════════════════════════════════════════
# Part 1: Nested Models
# ══════════════════════════════════════════════
#
# Real-world APIs have deeply nested data structures.
# Pydantic validates the ENTIRE tree — if any nested
# field is invalid, you get a clear error pointing to
# the exact location.


class GeoLocation(BaseModel):
    """Geographic coordinates."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180)")


class Address(BaseModel):
    """Physical address with optional geo coordinates."""
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=50)
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$")  # US ZIP format
    country: str = Field(default="US", max_length=2)
    geo: GeoLocation | None = None


class PhoneNumber(BaseModel):
    """Phone number with type classification."""
    number: str
    type: str = Field(default="mobile", pattern=r"^(mobile|home|work)$")

    @field_validator("number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """
        Strip formatting and validate phone number.
        Accept: +1-555-123-4567, (555) 123-4567, 5551234567
        Store: +15551234567 (E.164 format)
        """
        # YOUR CODE HERE
        # 1. Strip all non-digit characters (except leading +)
        # 2. Check length (10-15 digits)
        # 3. Add country code if missing
        # 4. Return normalized format
        import re
        digits = re.sub(r"[^\d+]", "", v)
        if digits.startswith("+"):
            pure_digits = digits[1:]
        else:
            pure_digits = digits

        if not (10 <= len(pure_digits) <= 15):
            raise ValueError(f"Phone number must be 10-15 digits, got {len(pure_digits)}")

        if not digits.startswith("+"):
            if len(pure_digits) == 10:
                digits = "+1" + pure_digits  # Assume US
            else:
                digits = "+" + pure_digits

        return digits


# ──────────────────────────────────────────────
# Exercise 1: Build the UserCreate model
# ──────────────────────────────────────────────

class UserCreate(BaseModel):
    """
    User registration request.

    Requirements:
    - email: valid email format
    - username: 3-30 chars, alphanumeric + underscores only
    - password: 8+ chars, must contain uppercase, lowercase, and digit
    - full_name: 1-100 chars
    - date_of_birth: must be in the past, user must be 13+
    - address: nested Address model
    - phone_numbers: list of PhoneNumber, max 3
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    address: Address
    phone_numbers: list[PhoneNumber] = Field(default_factory=list, max_length=3)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Only allow alphanumeric characters and underscores."""
        # YOUR CODE HERE
        import re
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username must contain only letters, numbers, and underscores")
        return v.lower()  # Normalize to lowercase

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Password must contain uppercase, lowercase, and digit."""
        # YOUR CODE HERE
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_age(cls, v: date) -> date:
        """User must be at least 13 years old."""
        # YOUR CODE HERE
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        if v > today:
            raise ValueError("Date of birth cannot be in the future")
        return v

    @model_validator(mode="after")
    def validate_model(self):
        """
        Cross-field validation example:
        If country is not US, phone numbers should not have +1 prefix.
        (This is just an example of model-level validation.)
        """
        # YOUR CODE HERE — add any cross-field validations
        return self


# ──────────────────────────────────────────────
# Exercise 2: Response model (separate from request!)
# ──────────────────────────────────────────────

class UserResponse(BaseModel):
    """
    What the API returns. NEVER includes:
    - password
    - internal IDs that could be enumerated
    - sensitive PII that wasn't requested

    Uses model_config to allow creating from ORM objects.
    """
    id: int
    email: str
    username: str
    full_name: str
    date_of_birth: date
    address: Address
    phone_numbers: list[PhoneNumber]
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ══════════════════════════════════════════════
# Part 2: Structured Error Handling
# ══════════════════════════════════════════════
#
# Every error from your API should follow the SAME shape.
# This makes it easy for frontend developers and other
# consumers to handle errors programmatically.


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str
    type: str


class ErrorResponse(BaseModel):
    error: dict  # {code, message, details}


# ──────────────────────────────────────────────
# Exercise 3: Custom exception handlers
# ──────────────────────────────────────────────

class AppException(Exception):
    """Base application exception."""
    def __init__(self, status_code: int, code: str, message: str, details: list | None = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []


class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id: str | int):
        super().__init__(
            status_code=404,
            code="NOT_FOUND",
            message=f"{resource} with id '{resource_id}' not found",
        )


class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=409,
            code="CONFLICT",
            message=message,
        )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """
    Convert AppException to a consistent JSON error response.

    Response shape:
    {
        "error": {
            "code": "NOT_FOUND",
            "message": "User with id '42' not found",
            "details": []
        }
    }
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(422)  # Validation errors
async def validation_exception_handler(request: Request, exc):
    """
    Override FastAPI's default 422 response to match our error shape.
    """
    # YOUR CODE HERE — transform Pydantic validation errors
    # into our consistent ErrorResponse format
    pass


# ══════════════════════════════════════════════
# Part 3: Endpoints
# ══════════════════════════════════════════════

# In-memory "database" for this exercise
fake_db: dict[int, dict] = {}
next_id = 1


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """
    Create a new user.
    - Validates all input via Pydantic (automatic!)
    - Checks for duplicate email
    - Returns UserResponse (no password!)
    """
    global next_id

    # Check duplicate email
    for existing in fake_db.values():
        if existing["email"] == user.email:
            raise ConflictException(f"Email '{user.email}' already registered")

    # Create user (in real app: hash password, save to DB)
    user_dict = user.model_dump()
    del user_dict["password"]  # NEVER store plain text password
    user_dict.update({
        "id": next_id,
        "created_at": datetime.now(),
        "is_active": True,
        "hashed_password": f"hashed_{user.password}",  # Placeholder
    })
    fake_db[next_id] = user_dict
    next_id += 1

    return UserResponse(**user_dict)


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a user by ID."""
    if user_id not in fake_db:
        raise NotFoundException("User", user_id)
    return UserResponse(**fake_db[user_id])


# ──────────────────────────────────────────────
# Exercise 4: Add these endpoints yourself
# ──────────────────────────────────────────────

# YOUR CODE HERE:
# 1. GET /users — list all users with pagination
# 2. PATCH /users/{user_id} — update user (partial update)
# 3. DELETE /users/{user_id} — soft delete (set is_active=False)


# ══════════════════════════════════════════════
# Part 4: Advanced Pydantic Patterns
# ══════════════════════════════════════════════

# ──────────────────────────────────────────────
# Exercise 5: Discriminated unions
# Used when an endpoint accepts multiple "types" of input.
# Example: a notification system that sends email, SMS, or push.
# ──────────────────────────────────────────────

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class EmailNotification(BaseModel):
    type: str = Field("email", pattern="^email$")  # literal discriminator
    to_email: EmailStr
    subject: str = Field(..., max_length=200)
    body: str = Field(..., max_length=10000)


class SMSNotification(BaseModel):
    type: str = Field("sms", pattern="^sms$")
    to_phone: str
    message: str = Field(..., max_length=160)  # SMS character limit


class PushNotification(BaseModel):
    type: str = Field("push", pattern="^push$")
    device_token: str
    title: str = Field(..., max_length=100)
    body: str = Field(..., max_length=500)


# YOUR CODE HERE:
# Create a /notifications endpoint that accepts any of the three types.
# Hint: use Union[EmailNotification, SMSNotification, PushNotification]
# with a discriminator on the "type" field.


# ══════════════════════════════════════════════
# Test with these curl commands:
# ══════════════════════════════════════════════
#
# Valid user:
# curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{
#   "email": "alice@example.com",
#   "username": "alice_dev",
#   "password": "StrongPass1",
#   "full_name": "Alice Developer",
#   "date_of_birth": "1995-06-15",
#   "address": {
#     "street": "123 Main St",
#     "city": "San Francisco",
#     "state": "CA",
#     "zip_code": "94102"
#   },
#   "phone_numbers": [{"number": "555-123-4567", "type": "mobile"}]
# }'
#
# Invalid (bad password):
# curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{
#   "email": "bob@example.com",
#   "username": "bob",
#   "password": "weak",
#   "full_name": "Bob",
#   "date_of_birth": "2020-01-01",
#   "address": {"street": "x", "city": "y", "state": "z", "zip_code": "bad"}
# }'
# → Should return multiple validation errors in one response

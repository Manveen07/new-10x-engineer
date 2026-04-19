"""
Week 2 - Day 3: Authentication & Authorization
================================================

JWT auth with refresh tokens and Role-Based Access Control (RBAC).
This is the auth pattern used in production AI APIs — you'll reuse
this exact structure in your RAG API, agent endpoints, etc.

Pre-req: pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic[email]

Run with: uvicorn day8_auth:app --reload
"""

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

# JWT library
# from jose import JWTError, jwt

# Password hashing
# from passlib.context import CryptContext


app = FastAPI(title="Auth Exercise")


# ══════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════

SECRET_KEY = "your-secret-key-change-in-production"  # In real app: from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ══════════════════════════════════════════════
# Models
# ══════════════════════════════════════════════

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserInDB(BaseModel):
    """Internal user model (has hashed_password)."""
    id: int
    email: str
    username: str
    hashed_password: str
    role: Role = Role.USER
    is_active: bool = True


class UserResponse(BaseModel):
    """Public user model (NO password)."""
    id: int
    email: str
    username: str
    role: Role
    is_active: bool


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  # subject (user ID or email)
    role: str
    exp: datetime
    type: str  # "access" or "refresh"


# ══════════════════════════════════════════════
# Exercise 1: Password Hashing
# ══════════════════════════════════════════════
#
# NEVER store passwords in plain text.
# Use bcrypt: slow by design (prevents brute force).
#
# Uncomment and implement:

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    YOUR CODE HERE
    """
    # return pwd_context.hash(password)
    return f"hashed_{password}"  # placeholder


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password against its hash.
    YOUR CODE HERE
    """
    # return pwd_context.verify(plain, hashed)
    return hashed == f"hashed_{plain}"  # placeholder


# ══════════════════════════════════════════════
# Exercise 2: JWT Token Creation
# ══════════════════════════════════════════════
#
# JWTs contain claims (payload) signed with a secret.
# Anyone can READ the payload (it's base64, NOT encrypted).
# But only the server can VERIFY the signature.
#
# NEVER put sensitive data in JWT claims.

def create_access_token(user: UserInDB) -> str:
    """
    Create a short-lived access token.

    Payload should include:
    - sub: user email (subject)
    - role: user role
    - exp: expiration time
    - type: "access"

    YOUR CODE HERE
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user.email,
        "role": user.role.value,
        "exp": expire,
        "type": "access",
    }
    # return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"access_token_for_{user.email}"  # placeholder


def create_refresh_token(user: UserInDB) -> str:
    """
    Create a long-lived refresh token.
    Used to get new access tokens without re-entering password.

    YOUR CODE HERE
    """
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user.email,
        "role": user.role.value,
        "exp": expire,
        "type": "refresh",
    }
    # return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"refresh_token_for_{user.email}"  # placeholder


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT token.

    Must:
    - Verify signature
    - Check expiration
    - Return TokenPayload

    Raise HTTPException(401) if invalid.

    YOUR CODE HERE
    """
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     return TokenPayload(**payload)
    # except JWTError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired token",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    pass


# ══════════════════════════════════════════════
# Exercise 3: Auth Dependencies
# ══════════════════════════════════════════════
#
# These are injected into endpoints via Depends().
# They form a chain:
#   oauth2_scheme → get_current_user → require_role("admin")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Fake database
fake_users_db: dict[str, UserInDB] = {}


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDB:
    """
    Extract the current user from the JWT token.

    Steps:
    1. Decode the token
    2. Verify it's an access token (not refresh)
    3. Look up the user in the database
    4. Check user is active
    5. Return UserInDB

    YOUR CODE HERE
    """
    # This is the placeholder — implement with real JWT
    raise HTTPException(status_code=401, detail="Not implemented")


def require_role(*roles: Role):
    """
    Factory function that creates a dependency requiring specific roles.

    Usage:
        @app.get("/admin", dependencies=[Depends(require_role(Role.ADMIN))])
        async def admin_endpoint(): ...

    Or:
        @app.get("/admin")
        async def admin_endpoint(user: UserInDB = Depends(require_role(Role.ADMIN))): ...

    YOUR CODE HERE
    """
    async def role_checker(
        current_user: UserInDB = Depends(get_current_user),
    ) -> UserInDB:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {', '.join(r.value for r in roles)}",
            )
        return current_user
    return role_checker


# ══════════════════════════════════════════════
# Exercise 4: Auth Endpoints
# ══════════════════════════════════════════════

@app.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserRegister):
    """
    Register a new user.

    Steps:
    1. Check if email already exists → 409 Conflict
    2. Hash the password
    3. Create UserInDB
    4. Store in fake_users_db
    5. Return UserResponse (no password!)

    YOUR CODE HERE
    """
    if user_data.email in fake_users_db:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = UserInDB(
        id=len(fake_users_db) + 1,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )
    fake_users_db[user.email] = user
    return UserResponse(**user.model_dump())


@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and receive tokens.

    Steps:
    1. Look up user by username (form_data.username — OAuth2 spec uses "username")
    2. Verify password → 401 if wrong
    3. Create access token + refresh token
    4. Return both

    YOUR CODE HERE
    """
    # Find user by email (OAuth2 form uses "username" field)
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
    )


@app.post("/auth/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """
    Exchange a refresh token for new access + refresh tokens.

    Steps:
    1. Decode the refresh token
    2. Verify it's a refresh token (type="refresh")
    3. Look up the user
    4. Create new token pair
    5. Return both

    YOUR CODE HERE
    """
    pass


# ══════════════════════════════════════════════
# Exercise 5: Protected Endpoints
# ══════════════════════════════════════════════

@app.get("/users/me", response_model=UserResponse)
async def get_me(current_user: UserInDB = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    return UserResponse(**current_user.model_dump())


@app.get("/admin/users", response_model=list[UserResponse])
async def list_all_users(
    admin: UserInDB = Depends(require_role(Role.ADMIN)),
):
    """
    Admin-only: list all users.
    Regular users get 403 Forbidden.
    """
    return [UserResponse(**u.model_dump()) for u in fake_users_db.values()]


@app.delete("/admin/users/{user_id}")
async def deactivate_user(
    user_id: int,
    admin: UserInDB = Depends(require_role(Role.ADMIN)),
):
    """
    Admin-only: deactivate a user.
    YOUR CODE HERE
    """
    pass


# ══════════════════════════════════════════════
# Testing Guide
# ══════════════════════════════════════════════
#
# 1. Register:
#    curl -X POST http://localhost:8000/auth/register \
#      -H "Content-Type: application/json" \
#      -d '{"email":"alice@test.com","username":"alice","password":"Test1234"}'
#
# 2. Login (OAuth2 form format):
#    curl -X POST http://localhost:8000/auth/login \
#      -d "username=alice@test.com&password=Test1234"
#
# 3. Access protected route:
#    curl http://localhost:8000/users/me \
#      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
#
# 4. Try admin route as regular user (should get 403):
#    curl http://localhost:8000/admin/users \
#      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

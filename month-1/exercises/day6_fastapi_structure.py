"""
Week 2 - Day 1: FastAPI Project Structure & Dependency Injection
=================================================================

This exercise walks you through building a production-quality
FastAPI project structure from scratch.

GOAL: By the end, you'll have a project scaffold that you'll
reuse for every AI backend you build.

Pre-req: pip install fastapi uvicorn pydantic-settings

DO NOT run this file directly — it's a guided exercise.
Follow the steps below to create the project structure.
"""

# ══════════════════════════════════════════════
# STEP 1: Create the project structure
# ══════════════════════════════════════════════
#
# Create this folder layout:
#
# fastapi_starter/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py              ← FastAPI app creation + lifespan
# │   ├── config.py            ← Pydantic Settings (env vars)
# │   ├── dependencies.py      ← Shared dependencies (DB session, etc.)
# │   ├── routers/
# │   │   ├── __init__.py
# │   │   ├── users.py         ← User CRUD endpoints
# │   │   └── items.py         ← Item CRUD endpoints
# │   ├── schemas/
# │   │   ├── __init__.py
# │   │   ├── users.py         ← Pydantic models for users
# │   │   └── items.py         ← Pydantic models for items
# │   ├── services/
# │   │   ├── __init__.py
# │   │   └── user_service.py  ← Business logic
# │   └── repositories/
# │       ├── __init__.py
# │       └── user_repo.py     ← Database queries
# ├── tests/
# │   ├── __init__.py
# │   └── test_users.py
# ├── .env
# └── requirements.txt
#
# Run this command to create it all at once:
# mkdir -p fastapi_starter/app/{routers,schemas,services,repositories} fastapi_starter/tests
# touch fastapi_starter/app/__init__.py fastapi_starter/app/routers/__init__.py ...


# ══════════════════════════════════════════════
# STEP 2: Config with Pydantic Settings
# ══════════════════════════════════════════════
#
# File: app/config.py
#
# WHY: Environment variables should be validated at startup,
# not scattered across the codebase with os.getenv().
# Pydantic Settings gives you type safety, defaults, and
# validation — all in one place.

"""
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "FastAPI Starter"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./app.db"

    # Auth
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30

    # Rate limiting
    rate_limit_per_minute: int = 60

    # LLM (for later weeks)
    llm_provider: str = "mock"
    openai_api_key: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
"""


# ══════════════════════════════════════════════
# STEP 3: FastAPI App with Lifespan
# ══════════════════════════════════════════════
#
# File: app/main.py
#
# WHY: The lifespan context manager replaces the old
# @app.on_event("startup") and @app.on_event("shutdown").
# It's cleaner because resources are created and cleaned up
# in the same function — you can't forget cleanup.

"""
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings
from app.routers import users, items


@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    settings = get_settings()
    print(f"Starting {settings.app_name}...")
    # Initialize database connection pool
    # Initialize Redis connection
    # Initialize LLM provider

    yield  # App is running

    # === SHUTDOWN ===
    print("Shutting down...")
    # Close database connections
    # Close Redis connections


app = FastAPI(
    title="FastAPI Starter",
    lifespan=lifespan,
)

# Include routers with prefixes
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
"""


# ══════════════════════════════════════════════
# STEP 4: Dependency Injection
# ══════════════════════════════════════════════
#
# File: app/dependencies.py
#
# WHY: Depends() is FastAPI's killer feature. It lets you:
# - Inject database sessions into every request
# - Inject the current authenticated user
# - Inject configuration
# - Chain dependencies (auth depends on DB session)
# - Override in tests (swap real DB for test DB)
#
# Think of it as "middleware for individual endpoints."

"""
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from app.config import Settings, get_settings


# Example: Settings dependency
async def get_current_settings(
    settings: Settings = Depends(get_settings),
) -> Settings:
    return settings


# Example: Database session dependency (placeholder — Week 2 Day 5)
async def get_db():
    # In reality: async session from SQLAlchemy
    db = {"connected": True}  # placeholder
    try:
        yield db
    finally:
        pass  # Close session


# Example: Pagination dependency (reusable across all list endpoints)
class PaginationParams:
    def __init__(self, offset: int = 0, limit: int = 20):
        if limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit cannot exceed 100",
            )
        self.offset = offset
        self.limit = limit
"""


# ══════════════════════════════════════════════
# STEP 5: Schemas (Pydantic Models)
# ══════════════════════════════════════════════
#
# File: app/schemas/users.py
#
# KEY PATTERN: Separate request and response schemas.
# - Request schemas: what the client sends (includes password)
# - Response schemas: what the client receives (NEVER includes password)
# - DB schemas: what goes in the database (includes hashed_password)
#
# This prevents accidentally leaking internal data.

"""
# app/schemas/users.py
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


# --- Request schemas ---

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str  # plain text — will be hashed in service layer


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None


# --- Response schemas ---

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    is_active: bool

    # This allows creating from ORM objects: UserResponse.model_validate(db_user)
    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    offset: int
    limit: int
"""


# ══════════════════════════════════════════════
# STEP 6: Router with Dependencies
# ══════════════════════════════════════════════
#
# File: app/routers/users.py
#
# PATTERN: Routers define endpoints. Business logic lives
# in services. Database queries live in repositories.
# Routers are THIN — they validate input, call a service,
# and return the response.

"""
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.users import UserCreate, UserResponse, UserListResponse, UserUpdate
from app.dependencies import get_db, PaginationParams

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db=Depends(get_db),
):
    # YOUR CODE HERE
    # 1. Check if email already exists
    # 2. Hash password
    # 3. Create user in DB
    # 4. Return UserResponse (NOT the DB model with password hash!)
    pass


@router.get("/", response_model=UserListResponse)
async def list_users(
    pagination: PaginationParams = Depends(),
    db=Depends(get_db),
):
    # YOUR CODE HERE
    # 1. Query users with offset/limit
    # 2. Get total count
    # 3. Return paginated response
    pass


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db=Depends(get_db),
):
    # YOUR CODE HERE
    # 1. Query user by ID
    # 2. Raise 404 if not found
    # 3. Return UserResponse
    pass


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db=Depends(get_db),
):
    # YOUR CODE HERE
    # 1. Query user by ID
    # 2. Update only provided fields (exclude_unset=True)
    # 3. Return updated UserResponse
    pass
"""


# ══════════════════════════════════════════════
# STEP 7: Run and test
# ══════════════════════════════════════════════
#
# 1. Create a .env file:
#    APP_NAME=MyAPI
#    DEBUG=true
#
# 2. Run:
#    uvicorn app.main:app --reload
#
# 3. Open http://localhost:8000/docs — FastAPI auto-generates
#    interactive API documentation (Swagger UI)
#
# 4. Open http://localhost:8000/redoc — alternative docs
#
# 5. Test the health endpoint:
#    curl http://localhost:8000/health


# ══════════════════════════════════════════════
# REFLECTION QUESTIONS (answer in comments)
# ══════════════════════════════════════════════
#
# 1. Why separate schemas for request vs response?
#    Your answer:
#
# 2. What's the advantage of Depends() over just importing and
#    calling a function directly?
#    Your answer:
#
# 3. Why use Pydantic Settings instead of os.getenv()?
#    Your answer:
#
# 4. The lifespan function yields. What does that pattern remind
#    you of from Week 1? (Hint: context managers, resource management)
#    Your answer:

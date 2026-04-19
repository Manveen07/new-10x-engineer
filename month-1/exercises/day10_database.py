"""
Week 2 - Day 5: Async Database Integration
=============================================

SQLAlchemy 2.0 async with PostgreSQL (or SQLite for quick dev).
This is the database pattern you'll use in every AI backend.

Pre-req:
  pip install sqlalchemy[asyncio] aiosqlite alembic fastapi uvicorn

For PostgreSQL (production):
  pip install asyncpg
  DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname

For SQLite (quick dev — used in this exercise):
  DATABASE_URL=sqlite+aiosqlite:///./app.db

Run with: uvicorn day10_database:app --reload
"""

from datetime import datetime
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, func, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


# ══════════════════════════════════════════════
# Part 1: Database Setup
# ══════════════════════════════════════════════
#
# SQLAlchemy 2.0 uses the new "mapped_column" style.
# The async engine uses asyncpg (Postgres) or aiosqlite (SQLite).

DATABASE_URL = "sqlite+aiosqlite:///./exercise_app.db"

# The engine manages the connection pool
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries — disable in production
    # For PostgreSQL, add:
    # pool_size=20,
    # max_overflow=10,
    # pool_timeout=30,
)

# Session factory — creates new sessions for each request
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy-load issues after commit
)


# ══════════════════════════════════════════════
# Part 2: ORM Models
# ══════════════════════════════════════════════

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class UserModel(Base):
    """
    Users table.

    YOUR CODE HERE — define these columns:
    - id: integer, primary key, auto-increment
    - email: string(255), unique, not null
    - username: string(50), unique, not null
    - hashed_password: string(255), not null
    - is_active: boolean, default True
    - created_at: datetime, default now
    - updated_at: datetime, default now, update on change
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship: one user has many items
    items: Mapped[list["ItemModel"]] = relationship(back_populates="owner", lazy="selectin")


class ItemModel(Base):
    """
    Items table — related to users.

    YOUR CODE HERE — define:
    - id: integer, primary key
    - title: string(200), not null
    - description: text, nullable
    - owner_id: integer, foreign key to users.id
    - is_public: boolean, default True
    - created_at: datetime
    """
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationship back to user
    owner: Mapped["UserModel"] = relationship(back_populates="items")


# ══════════════════════════════════════════════
# Part 3: Pydantic Schemas
# ══════════════════════════════════════════════

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    is_public: bool = True

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    owner_id: int
    is_public: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel):
    items: list
    total: int
    offset: int
    limit: int
    has_more: bool


# ══════════════════════════════════════════════
# Part 4: Database Dependency
# ══════════════════════════════════════════════
#
# This is the core pattern: one session per request.
# The session is created when the request starts and
# closed when it ends (even if there's an error).

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    Session is automatically closed after the request.

    Usage in endpoints:
        async def my_endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ══════════════════════════════════════════════
# Part 5: Lifespan (create tables on startup)
# ══════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup, cleanup on shutdown."""
    # Create all tables (in production: use Alembic migrations instead)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    yield  # App runs

    # Cleanup
    await engine.dispose()
    print("Database connections closed")


app = FastAPI(title="Database Exercise", lifespan=lifespan)


# ══════════════════════════════════════════════
# Part 6: CRUD Endpoints
# ══════════════════════════════════════════════

# --- Users ---

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.

    YOUR CODE HERE:
    1. Check if email already exists
    2. Create UserModel instance
    3. Add to session
    4. Flush (to get the auto-generated ID)
    5. Return UserResponse
    """
    # Check duplicate
    result = await db.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = UserModel(
        email=user_data.email,
        username=user_data.username,
        hashed_password=f"hashed_{user_data.password}",  # Replace with real hashing
    )
    db.add(user)
    await db.flush()  # Generates the ID without committing
    await db.refresh(user)  # Reload to get defaults (created_at, etc.)

    return UserResponse.model_validate(user)


@app.get("/users", response_model=PaginatedResponse)
async def list_users(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    List users with pagination.

    YOUR CODE HERE:
    1. Count total users
    2. Fetch page of users
    3. Return paginated response
    """
    # Count total
    count_result = await db.execute(select(func.count(UserModel.id)))
    total = count_result.scalar()

    # Fetch page
    result = await db.execute(
        select(UserModel)
        .offset(offset)
        .limit(limit)
        .order_by(UserModel.created_at.desc())
    )
    users = result.scalars().all()

    return PaginatedResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        offset=offset,
        limit=limit,
        has_more=(offset + limit) < total,
    )


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a user by ID."""
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


# --- Items ---

@app.post("/users/{user_id}/items", response_model=ItemResponse, status_code=201)
async def create_item(
    user_id: int,
    item_data: ItemCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create an item owned by a user.

    YOUR CODE HERE:
    1. Verify user exists
    2. Create ItemModel
    3. Return ItemResponse
    """
    # Verify user exists
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    item = ItemModel(
        title=item_data.title,
        description=item_data.description,
        owner_id=user_id,
        is_public=item_data.is_public,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)

    return ItemResponse.model_validate(item)


@app.get("/items", response_model=PaginatedResponse)
async def list_items(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    public_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    """
    List items with optional filtering.

    YOUR CODE HERE — add filtering:
    - public_only: if True, only show public items
    - Add search by title (optional query param)
    """
    query = select(ItemModel)
    if public_only:
        query = query.where(ItemModel.is_public == True)

    count_query = select(func.count(ItemModel.id))
    if public_only:
        count_query = count_query.where(ItemModel.is_public == True)

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.offset(offset).limit(limit).order_by(ItemModel.created_at.desc()))
    items = result.scalars().all()

    return PaginatedResponse(
        items=[ItemResponse.model_validate(i) for i in items],
        total=total,
        offset=offset,
        limit=limit,
        has_more=(offset + limit) < total,
    )


# ══════════════════════════════════════════════
# Exercise: Add these endpoints
# ══════════════════════════════════════════════
#
# YOUR CODE HERE:
# 1. PATCH /users/{user_id} — update user (partial update using exclude_unset)
# 2. DELETE /users/{user_id} — soft delete (set is_active=False)
# 3. GET /users/{user_id}/items — list items for a specific user
# 4. PATCH /items/{item_id} — update item (only owner should be able to)
# 5. DELETE /items/{item_id} — hard delete item


# ══════════════════════════════════════════════
# Alembic Setup Guide
# ══════════════════════════════════════════════
#
# In production, NEVER use Base.metadata.create_all().
# Use Alembic for migrations:
#
# 1. Initialize Alembic:
#    alembic init alembic
#
# 2. Edit alembic/env.py:
#    - Set target_metadata = Base.metadata
#    - Configure async engine
#
# 3. Generate migration:
#    alembic revision --autogenerate -m "initial tables"
#
# 4. Apply migration:
#    alembic upgrade head
#
# 5. After schema changes:
#    alembic revision --autogenerate -m "add new column"
#    alembic upgrade head
#
# This gives you version-controlled, reversible schema changes.


# ══════════════════════════════════════════════
# Testing
# ══════════════════════════════════════════════
#
# curl -X POST http://localhost:8000/users -H "Content-Type: application/json" \
#   -d '{"email":"alice@test.com","username":"alice","password":"secret"}'
#
# curl http://localhost:8000/users
#
# curl -X POST http://localhost:8000/users/1/items -H "Content-Type: application/json" \
#   -d '{"title":"My First Item","description":"A test item"}'
#
# curl http://localhost:8000/items

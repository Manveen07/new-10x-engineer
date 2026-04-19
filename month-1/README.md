# Month 1 — Backend & Async Foundations for AI Systems

## Goal
Build the async Python and FastAPI muscle memory that every AI backend needs. By month's end, you'll have a production-ready Q&A API with semantic caching, async PostgreSQL, and swappable LLM providers.

## Weekly Breakdown

| Week | Topic | Key Deliverable |
|------|-------|----------------|
| 1 | Advanced Async Python | Async scraper pipeline with producers, consumers, semaphores |
| 2 | FastAPI Production Patterns | Production-ready API starter with auth, RBAC, async DB |
| 3 | PostgreSQL + AI Design Patterns | Optimized queries + LLM provider adapter pattern |
| 4 | Semantic Caching + System Design | Month capstone: AI Q&A API with caching |

## Prerequisites

- Python 3.11+ installed
- PostgreSQL 14+ running locally (or Docker)
- Redis Stack (Docker recommended)
- Node.js 18+ (for some tooling)
- A code editor (VS Code recommended)
- GitHub account
- OpenAI API key (for embeddings in week 4)

## Setup

```bash
# Create a virtual environment for month 1
python -m venv month1-env
source month1-env/bin/activate  # Linux/Mac
# or on Windows:
month1-env\Scripts\activate

# Install base dependencies (expand per week)
pip install aiohttp asyncio fastapi uvicorn sqlalchemy[asyncio] asyncpg alembic pydantic redis redisvl openai httpx pytest pytest-asyncio
```

## Daily Time Commitment
1.5 hours weekdays, 1-2 hours weekends = ~10 hours/week

## How to Use These Modules
1. Read the week's module file first for the full picture
2. Follow each day's plan — read the resource, then do the exercise
3. Complete the daily exercise file (in `exercises/`)
4. End of week: build the integration project
5. Use the skill checkpoint to self-assess

## Progress Tracker

- [ ] Week 1: Async Python
- [ ] Week 2: FastAPI
- [ ] Week 3: PostgreSQL + Patterns
- [ ] Week 4: Caching + System Design
- [ ] Month 1 Capstone

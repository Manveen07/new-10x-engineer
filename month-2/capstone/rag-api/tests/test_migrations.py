import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from alembic.config import Config
from alembic import command
import os

from app.config import settings

@pytest.mark.asyncio
async def test_migrations_run_cleanly():
    """
    Integration test that boots a fresh DB (or uses the test one),
    and applies migrations from the project root.
    """
    # Use a separate test database logic or the current one if safe
    # In CI, we usually use a dedicated ephemeral DB.
    
    # 1. Setup Alembic Config
    # Finding the path relative to this test file
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
    
    # 2. Apply Migrations
    # command.upgrade is a sync call, env.py handles the async engine internally
    # but we need to ensure the connection string is correct.
    command.upgrade(alembic_cfg, "head")
    
    # 3. Verify Vector extension and tables exist
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as conn:
        # Check vector extension
        result = await conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';"))
        assert result.scalar() == "vector"
        
        # Check tables
        result = await conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"))
        tables = [row[0] for row in result.fetchall()]
        assert "documents" in tables
        assert "chunks" in tables
        
    await engine.dispose()
    
    # 4. Downgrade to ensure cleanup works (Optional but good)
    command.downgrade(alembic_cfg, "base")

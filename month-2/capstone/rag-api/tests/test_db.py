import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Document, Chunk

@pytest.mark.asyncio
async def test_database_initialization(db_session: AsyncSession):
    # Check if pgvector is enabled
    result = await db_session.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';"))
    assert result.scalar() == 'vector'

@pytest.mark.asyncio
async def test_document_chunk_cycle(db_session: AsyncSession):
    # 1. Insert Document
    doc = Document(
        tenant_id="test_tenant",
        source_uri="http://test.uri",
        title="Test Doc",
        content_sha256="sha256_test"
    )
    db_session.add(doc)
    await db_session.flush()

    # 2. Insert Chunk
    chunk = Chunk(
        document_id=doc.id,
        tenant_id="test_tenant",
        chunk_index=0,
        text="Test chunk text",
        token_count=3,
        embedding=[0.5] * 1536
    )
    db_session.add(chunk)
    await db_session.commit()

    # 3. Verify Retrieval
    stmt = select(Chunk).where(Chunk.document_id == doc.id)
    result = await db_session.execute(stmt)
    retrieved = result.scalar_one()
    
    assert retrieved.text == "Test chunk text"
    assert retrieved.tenant_id == "test_tenant"
    assert len(retrieved.embedding) == 1536

@pytest.mark.asyncio
async def test_exact_vector_search(db_session: AsyncSession):
    # Ensure clean state
    await db_session.execute(text("TRUNCATE chunks, documents RESTART IDENTITY CASCADE;"))
    
    # 1. Insert two chunks with different embeddings
    doc = Document(tenant_id="t1", source_uri="u1", content_sha256="s1")
    db_session.add(doc)
    await db_session.flush()

    c1 = Chunk(document_id=doc.id, tenant_id="t1", chunk_index=0, text="one", token_count=1, embedding=[1.0] * 1536)
    c2 = Chunk(document_id=doc.id, tenant_id="t1", chunk_index=1, text="zero", token_count=1, embedding=[0.0] * 1536)
    db_session.add_all([c1, c2])
    await db_session.commit()

    # 2. Search for [1,1,...]
    query = [1.0] * 1536
    stmt = (
        select(Chunk)
        .order_by(Chunk.embedding.cosine_distance(query))
        .limit(1)
    )
    result = await db_session.execute(stmt)
    top_chunk = result.scalar_one()
    
    assert top_chunk.text == "one"

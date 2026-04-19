import pytest
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Document, Chunk
from app.services.ingest.loaders import PlainTextLoader
from app.services.ingest.service import IngestService

@pytest.mark.asyncio
async def test_ingest_pipeline_success(db_session: AsyncSession, tmp_path):
    # 1. Setup sample file
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test document content for ingestion.")
    
    # 2. Load
    loader = PlainTextLoader()
    docs = await loader.load(str(test_file))
    assert len(docs) == 1
    
    # 3. Ingest
    service = IngestService(db_session)
    result = await service.ingest_document(docs[0], tenant_id="t1")
    
    assert result.status == "success"
    assert result.chunks_created > 0
    
    # 4. Verify DB
    stmt = select(Document).where(Document.id == result.document_id)
    doc_record = (await db_session.execute(stmt)).scalar_one()
    assert doc_record.tenant_id == "t1"
    
    # Verify FTS
    stmt = select(Chunk).where(Chunk.document_id == doc_record.id)
    chunk_record = (await db_session.execute(stmt)).scalars().first()
    assert chunk_record.fts is not None

@pytest.mark.asyncio
async def test_ingest_dedupe(db_session: AsyncSession, tmp_path):
    test_file = tmp_path / "dedupe.txt"
    test_file.write_text("Identical content")
    
    loader = PlainTextLoader()
    docs = await loader.load(str(test_file))
    
    service = IngestService(db_session)
    
    # First ingest
    res1 = await service.ingest_document(docs[0], tenant_id="t1")
    assert res1.status == "success"
    
    # Second ingest (same content, same tenant)
    res2 = await service.ingest_document(docs[0], tenant_id="t1")
    assert res2.status == "skipped"
    assert res2.reason == "duplicate_content"
    assert res2.document_id == res1.document_id

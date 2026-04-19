import logging
from sqlalchemy import select, func, text, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.db.models import Document, Chunk
from app.services.ingest.types import LoadedDocument, ChunkDraft, IngestResult
from app.services.ingest.normalization import generate_content_hash, extract_fallback_title, normalize_text
from app.services.ingest.splitters import RecursiveSplitter, MarkdownSplitter

logger = logging.getLogger(__name__)

class IngestService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_document(
        self, 
        doc: LoadedDocument, 
        tenant_id: str,
        splitter_type: str = "recursive"
    ) -> IngestResult:
        """
        Orchestration: Normalize -> Dedupe -> Split -> Store.
        """
        # 1. Normalize
        doc.text = normalize_text(doc.text)
        content_hash = generate_content_hash(doc.text)
        
        # 2. Tenant-scoped Dedupe
        existing_stmt = select(Document.id).where(
            Document.tenant_id == tenant_id,
            Document.content_sha256 == content_hash
        )
        existing_id = (await self.db.execute(existing_stmt)).scalar_one_or_none()
        
        if existing_id:
            logger.info(f"Document already exists for tenant {tenant_id}: {content_hash}")
            return IngestResult(
                document_id=existing_id,
                status="skipped",
                reason="duplicate_content"
            )
        
        # 3. Handle Meta & Title
        title = extract_fallback_title(doc)
        
        # 4. Split
        if splitter_type == "markdown":
            splitter = MarkdownSplitter()
        else:
            splitter = RecursiveSplitter()
            
        chunk_drafts = splitter.split(doc)
        
        try:
            # 5. Atomic Persistence
            # A. Create Document
            new_doc = Document(
                tenant_id=tenant_id,
                source_uri=doc.source_uri,
                title=title,
                content_sha256=content_hash,
                meta=doc.metadata
            )
            self.db.add(new_doc)
            await self.db.flush() # Populate new_doc.id
            
            # B. Create Chunks in batch with explicit to_tsvector
            # We use a raw SQL approach for to_tsvector or sqlalchemy func
            for draft in chunk_drafts:
                new_chunk = Chunk(
                    document_id=new_doc.id,
                    tenant_id=tenant_id,
                    chunk_index=draft.chunk_index,
                    text=draft.text,
                    token_count=draft.token_count,
                    splitter_type=draft.splitter_type,
                    chunk_overlap=draft.chunk_overlap,
                    meta=draft.metadata,
                    # Populate FTS in service layer per guardrails
                    fts=func.to_tsvector('english', draft.text)
                )
                self.db.add(new_chunk)
            
            await self.db.commit()
            logger.info(f"Ingested document {new_doc.id} with {len(chunk_drafts)} chunks.")
            
            return IngestResult(
                document_id=new_doc.id,
                chunks_created=len(chunk_drafts),
                status="success"
            )
            
        except Exception as e:
            logger.error(f"Failed to ingest document: {e}")
            await self.db.rollback()
            return IngestResult(status="error", reason=str(e))

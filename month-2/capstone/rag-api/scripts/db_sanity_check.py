import asyncio
import numpy as np
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector

from app.db.session import engine, AsyncSessionLocal
from app.db.models import Document, Chunk
from app.config import settings

async def sanity_check():
    print("Starting database sanity check...")
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. Check if extension exists
            result = await session.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector';"))
            ext = result.scalar()
            if not ext:
                print("Error: pgvector extension not found!")
                return
            print("Verified: pgvector extension is present.")

            # 2. Create a dummy document
            doc = Document(
                tenant_id="test_tenant",
                source_uri="http://example.com/sanity",
                title="Sanity Check Doc",
                content_sha256="fake_sha_123",
                meta={"type": "sanity_test"}
            )
            session.add(doc)
            await session.flush()  # Get doc.id
            print(f"Created test document: ID {doc.id}")

            # 3. Create a dummy chunk with a known embedding
            # text-embedding-3-small is 1536 dims
            embedding = [0.1] * 1536
            chunk = Chunk(
                document_id=doc.id,
                tenant_id="test_tenant",
                chunk_index=0,
                text="This is a sanity check chunk.",
                token_count=10,
                embedding=embedding,
                meta={"check": True}
            )
            session.add(chunk)
            await session.commit()
            print(f"Created test chunk with embedding: ID {chunk.id}")

            # 4. Perform exact vector search using cosine distance (<=>)
            query_embedding = [0.1] * 1536
            # In SQLAlchemy, we can use the <=> operator via the column
            stmt = (
                select(Chunk)
                .filter(Chunk.tenant_id == "test_tenant")
                .order_by(Chunk.embedding.cosine_distance(query_embedding))
                .limit(1)
            )
            
            result = await session.execute(stmt)
            found_chunk = result.scalar_one_or_none()
            
            if found_chunk and found_chunk.id == chunk.id:
                print("SUCCESS: Exact vector search returned the correct chunk!")
            else:
                print("FAILURE: Exact vector search did not return the expected chunk.")

        except Exception as e:
            print(f"An error occurred: {e}")
            await session.rollback()
        finally:
            await session.close()
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(sanity_check())

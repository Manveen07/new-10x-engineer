import asyncio
import os
import argparse
from app.db.session import AsyncSessionLocal
from app.services.ingest.loaders import PlainTextLoader, MarkdownLoader
from app.services.ingest.service import IngestService

async def main():
    parser = argparse.ArgumentParser(description="Ingest documents into the RAG platform.")
    parser.add_argument("--path", type=str, required=True, help="Path to file or directory")
    parser.add_argument("--tenant-id", type=str, required=True, help="Tenant ID for the data")
    parser.add_argument("--splitter", type=str, choices=["recursive", "markdown"], default="recursive")
    
    args = parser.parse_args()
    
    # 1. Discovery
    files = []
    if os.path.isdir(args.path):
        for root, _, filenames in os.walk(args.path):
            for f in filenames:
                if f.endswith(('.txt', '.md')):
                    files.append(os.path.join(root, f))
    else:
        files.append(args.path)
        
    print(f"Found {len(files)} files to ingest.")
    
    # 2. Ingest
    async with AsyncSessionLocal() as db:
        service = IngestService(db)
        
        for file_path in files:
            print(f"Processing {file_path}...")
            
            # Select loader
            if file_path.endswith('.md'):
                loader = MarkdownLoader()
            else:
                loader = PlainTextLoader()
                
            try:
                docs = await loader.load(file_path)
                for doc in docs:
                    result = await service.ingest_document(
                        doc=doc,
                        tenant_id=args.tenant_id,
                        splitter_type=args.splitter
                    )
                    print(f"  Result: {result.status} (Chunks: {result.chunks_created})")
            except Exception as e:
                print(f"  FAILED to process {file_path}: {e}")

if __name__ == "__main__":
    asyncio.run(main())

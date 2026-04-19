import aiofiles
import os
from abc import ABC, abstractmethod
from typing import List
from app.services.ingest.types import LoadedDocument

class BaseLoader(ABC):
    @abstractmethod
    async def load(self, source: str) -> List[LoadedDocument]:
        """
        Load document(s) from a source URI (local file path for now).
        """
        pass

class PlainTextLoader(BaseLoader):
    async def load(self, source: str) -> List[LoadedDocument]:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file not found: {source}")
            
        async with aiofiles.open(source, mode='r', encoding='utf-8') as f:
            content = await f.read()
            
        return [
            LoadedDocument(
                text=content,
                source_uri=source,
                metadata={"file_size": len(content), "extension": ".txt"}
            )
        ]

class MarkdownLoader(BaseLoader):
    async def load(self, source: str) -> List[LoadedDocument]:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file not found: {source}")
            
        async with aiofiles.open(source, mode='r', encoding='utf-8') as f:
            content = await f.read()
            
        # Basic markdown metadata extraction could happen here
        return [
            LoadedDocument(
                text=content,
                source_uri=source,
                metadata={"file_size": len(content), "extension": ".md"}
            )
        ]

import tiktoken
from abc import ABC, abstractmethod
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

from app.services.ingest.types import LoadedDocument, ChunkDraft

class BaseSplitter(ABC):
    @abstractmethod
    def split(self, doc: LoadedDocument) -> List[ChunkDraft]:
        pass
    
    def _count_tokens(self, text: str, model: str = "gpt-4o") -> int:
        """
        Baseline token counting using tiktoken.
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

class RecursiveSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len, # Using characters for baseline, can switch to tokens
            is_separator_regex=False,
        )

    def split(self, doc: LoadedDocument) -> List[ChunkDraft]:
        texts = self.splitter.split_text(doc.text)
        chunks = []
        for i, text in enumerate(texts):
            chunks.append(
                ChunkDraft(
                    text=text,
                    chunk_index=i,
                    token_count=self._count_tokens(text),
                    splitter_type="recursive",
                    chunk_overlap=self.chunk_overlap,
                    metadata=doc.metadata.copy()
                )
            )
        return chunks

class MarkdownSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Headers to split on
        self.headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on
        )
        # We downstream to Recursive for large sections
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )

    def split(self, doc: LoadedDocument) -> List[ChunkDraft]:
        # 1. Split by header
        header_splits = self.header_splitter.split_text(doc.text)
        
        chunks = []
        chunk_idx = 0
        
        for split in header_splits:
            # 2. Further split by recursive if still too large
            sub_splits = self.recursive_splitter.split_text(split.page_content)
            for sub_text in sub_splits:
                # Merge header metadata into chunk metadata
                meta = doc.metadata.copy()
                meta.update(split.metadata)
                
                chunks.append(
                    ChunkDraft(
                        text=sub_text,
                        chunk_index=chunk_idx,
                        token_count=self._count_tokens(sub_text),
                        splitter_type="markdown",
                        chunk_overlap=self.chunk_overlap,
                        metadata=meta
                    )
                )
                chunk_idx += 1
                
        return chunks

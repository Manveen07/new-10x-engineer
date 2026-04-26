from abc import ABC, abstractmethod

import tiktoken

from app.services.ingest.types import ChunkDraft, LoadedDocument


class BaseSplitter(ABC):
    @abstractmethod
    def split(self, doc: LoadedDocument) -> list[ChunkDraft]:
        raise NotImplementedError

    def _count_tokens(self, text: str, model: str = "gpt-4o") -> int:
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


class RecursiveSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, doc: LoadedDocument) -> list[ChunkDraft]:
        texts = _split_with_overlap(doc.text, self.chunk_size, self.chunk_overlap)
        return [
            ChunkDraft(
                text=text,
                chunk_index=index,
                token_count=self._count_tokens(text),
                splitter_type="recursive",
                chunk_overlap=self.chunk_overlap,
                metadata=doc.metadata.copy(),
            )
            for index, text in enumerate(texts)
        ]


class MarkdownSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, doc: LoadedDocument) -> list[ChunkDraft]:
        sections = _split_markdown_sections(doc.text)
        chunks: list[ChunkDraft] = []
        chunk_index = 0

        for heading, section_text in sections:
            metadata = doc.metadata.copy()
            if heading:
                metadata["heading"] = heading
            for text in _split_with_overlap(section_text, self.chunk_size, self.chunk_overlap):
                chunks.append(
                    ChunkDraft(
                        text=text,
                        chunk_index=chunk_index,
                        token_count=self._count_tokens(text),
                        splitter_type="markdown",
                        chunk_overlap=self.chunk_overlap,
                        metadata=metadata.copy(),
                    )
                )
                chunk_index += 1
        return chunks


def _split_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_size])
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(words):
            break
    return chunks


def _split_markdown_sections(text: str) -> list[tuple[str | None, str]]:
    sections: list[tuple[str | None, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append((current_heading, current_lines))
            current_heading = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, current_lines))

    return [(heading, "\n".join(lines).strip()) for heading, lines in sections if "\n".join(lines).strip()]

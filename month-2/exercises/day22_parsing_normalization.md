# Day 22: Parsing And Normalization

## Goal

Turn messy source files into normalized document records before chunking.

## Build

- Markdown loader.
- HTML loader that removes navigation/boilerplate.
- PDF text-export loader.
- JSON loader.
- whitespace normalization.
- metadata preservation.

## Output Contract

```json
{
  "document_id": "stable id",
  "tenant_id": "demo",
  "source_uri": "datasets/seed_corpus/file.md",
  "title": "Document title",
  "text": "normalized text",
  "content_sha256": "...",
  "metadata": {}
}
```

## Done When

- Parser output is deterministic.
- Empty or near-empty documents are rejected with a clear error.

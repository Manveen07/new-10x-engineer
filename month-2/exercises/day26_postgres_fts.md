# Day 26: PostgreSQL Full Text Search

## Goal

Add lexical retrieval for exact terms, product names, acronyms, and headings.

## Build

- `fts tsvector` column.
- GIN index.
- `websearch_to_tsquery` query path.
- `ts_rank_cd` score.
- tenant filter.

## Done When

- Lexical search finds exact section titles and acronyms from the seed corpus.
- `/v1/search` can return lexical-only results for debugging.

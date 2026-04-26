# Day 48: Memory Design

## Goal

Avoid unbounded memory.

## Rules

- short-term memory lives in graph state.
- long-term memory must be explicitly written.
- sensitive data is never memorized.
- retrieval memory must be tenant-filtered.
- memory reads are logged.

## Done When

- You can explain what the agent remembers and why.

# Week 9: LangGraph Fundamentals And Bounded Agent State

## Outcome

Build a small but realistic agent graph that can plan, call the Month 2 RAG API, answer with citations, and stop safely. This week is about explicit state and control flow, not open-ended autonomy.

## Day 41: Agent Boundaries

Exercise: `../exercises/day41_agent_boundaries.md`

Define:

- agent use case.
- allowed tools.
- forbidden actions.
- risk levels.
- success criteria.
- stop conditions.

## Day 42: LangGraph State Model

Exercise: `../exercises/day42_langgraph_state.py`

Build:

- typed graph state.
- node input/output contracts.
- run IDs and trace IDs.
- max step counter.

## Day 43: Basic Graph

Exercise: `../exercises/day43_basic_graph.md`

Build graph:

```text
input -> plan -> retrieve -> answer -> verify -> done
```

## Day 44: Routing And Bounded Loops

Exercise: `../exercises/day44_routing_bounded_loops.py`

Build:

- conditional route after verify.
- retry path only when useful.
- hard `max_steps`.
- safe fallback when confidence is low.

## Day 45: RAG Tools

Exercise: `../exercises/day45_rag_tools.md`

Build wrappers for:

- Month 2 `/v1/search`.
- Month 2 `/v1/answer`.
- mock search/answer tools for tests.

## Weekend 9: Research/RAG Agent

Exercise: `../exercises/weekend9_research_agent.md`

Build:

- cited answer.
- trace of graph nodes.
- tool-call records.
- safe "I don't know" result when retrieval is insufficient.

## Week 9 Acceptance Gate

- [ ] graph state is typed.
- [ ] max steps prevent runaway loops.
- [ ] RAG tools use Month 2 contracts.
- [ ] answer includes citations.
- [ ] node trace is inspectable.

## Core Resources

| Resource | Use |
|---|---|
| https://docs.langchain.com/oss/python/langgraph/overview | LangGraph concepts |
| https://docs.langchain.com/oss/python/langgraph/persistence | checkpoints and threads |
| https://docs.langchain.com/oss/python/langgraph/durable-execution | durable/resumable workflows |

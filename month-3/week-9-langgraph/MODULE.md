# Week 9: LangGraph Fundamentals

## Why This Matters
LangGraph is the most production-ready agent framework in 2026. While simple chains handle "do A then B," real agents need conditional branching, loops, state management, memory, and error recovery. LangGraph gives you a state machine for AI workflows — each node is a step, edges define control flow, and state persists across the entire execution.

---

## Day-by-Day Plan

### Monday — LangGraph Concepts & Architecture (1.5h)

**Complete (1.5h):**
- LangChain Academy: Introduction to LangGraph (free course)
  https://academy.langchain.com/courses/intro-to-langgraph

**Core Concepts:**

```
┌────────── StateGraph ──────────────────────────────────┐
│                                                         │
│  State = TypedDict with all data flowing through graph  │
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────────┐        │
│  │  Node A  │───→│  Node B  │───→│  Node C      │        │
│  │ (function)│   │ (function)│   │  (function)   │        │
│  └─────────┘    └────┬────┘    └─────────────┘        │
│                      │                                  │
│                      ├─── conditional_edge ──→ Node D   │
│                      │                                  │
│                      └─── conditional_edge ──→ Node E   │
│                                                         │
│  Checkpointer: saves state at each step (for resume)   │
└─────────────────────────────────────────────────────────┘
```

**Key mental model:**
- **State**: A dictionary that flows through the graph. Each node reads from it and writes back to it.
- **Node**: A function that takes state, does work, returns updated state.
- **Edge**: Connects nodes. Can be unconditional (always go A→B) or conditional (if X go to B, else go to C).
- **Checkpointer**: Saves state to a database after each node. Enables resume, replay, and debugging.

**The simplest LangGraph:**
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    messages: list[dict]
    response: str

def call_llm(state: State) -> dict:
    # Call LLM with state["messages"]
    return {"response": "Hello!"}

graph = StateGraph(State)
graph.add_node("llm", call_llm)
graph.set_entry_point("llm")
graph.add_edge("llm", END)
app = graph.compile()
```

---

### Tuesday — Build Your First Stateful Agent (1.5h)

**Follow (1.5h):**
- DataCamp: LangGraph agents tutorial
  https://www.datacamp.com/tutorial/langgraph-agents

**Build a ReAct Agent:**
```
          ┌─────────────────────────────────┐
          │                                 │
          ▼                                 │
    ┌──────────┐    ┌──────────┐    ┌──────┴──────┐
    │ Reason   │───→│ Act      │───→│ Observe     │
    │ (LLM     │    │ (call    │    │ (process    │
    │  thinks) │    │  tool)   │    │  result)    │
    └──────────┘    └──────────┘    └─────────────┘
          │
          ▼ (when done reasoning)
       [END]
```

ReAct = Reason + Act. The LLM:
1. Thinks about what to do
2. Calls a tool
3. Observes the result
4. Decides: need more info? (loop) or done? (end)

**Implement:**
1. Define state with messages, tool results, iteration count
2. Create 3 tools: search, calculator, current_time
3. Build the ReAct loop with conditional edge (continue vs end)
4. Add state persistence with MemorySaver checkpointer
5. Test: ask questions requiring multiple tool calls

---

### Wednesday — Cyclic Workflows and Routing (1.5h)

**Watch (1.5h):**
- freeCodeCamp: LangGraph and Conversational AI (first portion)
  https://www.freecodecamp.org/news/learn-langgraph-and-build-conversational-ai-with-python/

**Build a Query Router:**
```
                    ┌──────────┐
                    │ Classify  │
                    │ Intent    │
                    └─────┬────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
        ┌─────▼───┐ ┌────▼────┐ ┌────▼────┐
        │ Search  │ │ Calculate│ │ Database│
        │ Tool    │ │ Tool     │ │ Query   │
        └─────┬───┘ └────┬────┘ └────┬────┘
              │           │           │
              └───────────┼───────────┘
                          │
                    ┌─────▼────┐
                    │ Generate  │
                    │ Response  │
                    └──────────┘
```

**Key pattern**: Conditional edges based on LLM classification. The router is itself an LLM call that outputs a structured decision.

---

### Thursday — Memory and Persistence (1.5h)

**Read (1h):**
- LangGraph official docs on persistence
  https://langchain-ai.github.io/langgraph/

**Types of Memory:**
| Type | Scope | Implementation | Use Case |
|------|-------|---------------|----------|
| Short-term | Within conversation | State in graph | Current task context |
| Long-term | Cross-conversation | External store (DB) | User preferences, past interactions |
| Episodic | Per interaction | Checkpointer | Resume interrupted workflows |
| Semantic | Across all users | Vector store | Company knowledge, FAQ |

**Implement:**
1. Thread-based memory: each conversation has an ID, state persists across turns
2. Cross-conversation memory: store user preferences/facts in PostgreSQL
3. Demonstrate: resume a multi-step task after "interruption"

---

### Friday — Advanced Patterns: Parallel Execution & Subgraphs (1.5h)

**Read (1h):**
- GoPubby: Building AI Agents with LangGraph 2026 Edition
  https://ai.gopubby.com/building-ai-agents-with-langgraph-2026-edition-a-step-by-step-guide-494d36e801f9

**Read (30 min):**
- Latenode: LangGraph multi-agent orchestration
  https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-ai-framework-2025-complete-architecture-guide-multi-agent-orchestration-analysis

**Patterns:**
1. **Parallel tool execution**: Call multiple tools simultaneously
2. **Subgraphs**: Encapsulate complex logic as a nested graph
3. **Map-reduce**: Fan out to multiple workers, aggregate results
4. **Supervisor pattern**: One agent delegates to specialized sub-agents

---

### Weekend — Research Agent (1-2h)

**Build a multi-step research agent:**
```
Question → Plan Search Queries → Execute Searches (parallel)
         → Synthesize Findings → Generate Structured Answer

State:
  question: str
  search_queries: list[str]
  search_results: list[dict]
  synthesis: str
  final_answer: str
  citations: list[str]
```

**Requirements:**
- Takes a research question
- Plans 3-5 search queries
- Executes searches in parallel
- Synthesizes findings (handles contradictions)
- Produces a structured answer with citations
- Uses at least 3 different tools

**Done when:** Agent can research a topic across multiple sources and produce a coherent, cited summary.

---

## Skill Checkpoint

1. Draw a LangGraph state diagram for your research agent. Explain state flow.
2. What happens when a tool call fails mid-graph? How does LangGraph handle it?
3. How does LangGraph differ from a simple sequential chain?
4. When would you use a subgraph vs a single flat graph?
5. Explain checkpointing: why is it essential for production agents?

---

## Core Resources

| Resource | Type | URL |
|----------|------|-----|
| LangGraph docs | Reference | https://langchain-ai.github.io/langgraph/ |
| LangChain Academy | Course | https://academy.langchain.com/courses/intro-to-langgraph |
| LangGraph examples | Code | https://github.com/langchain-ai/langgraph/tree/main/examples |

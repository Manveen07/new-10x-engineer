# Agentic RAG Architecture

```mermaid
flowchart LR
    User --> API[Agent API]
    API --> Graph[LangGraph StateGraph]
    Graph --> Planner[Planner Node]
    Planner --> Retriever[RAG Tool]
    Retriever --> RAG[Month 2 RAG API]
    Graph --> MCP[MCP Tool Client]
    MCP --> MCPServer[MCP Server]
    Graph --> Approval[HITL Approval Node]
    Graph --> Verifier[Verifier Node]
    Verifier --> Answer[Answer + Citations]
    Graph --> Trace[(Agent Runs and Tool Calls)]
```

## Design Rules

- Every loop has a max step count.
- Every tool call is typed and logged.
- High-risk tools require approval.
- Retrieval tools preserve tenant filters.
- Final answers must include citations or safe uncertainty.

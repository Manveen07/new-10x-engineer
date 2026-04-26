# Month 3 Capstone: Controlled Agentic RAG

## Purpose

Build a bounded, observable, resumable agent that uses the Month 2 RAG API and MCP tools to answer questions with citations.

## Required Capabilities

- LangGraph state graph.
- typed graph state.
- bounded tool loop.
- Month 2 search/answer tools.
- MCP server exposing RAG tools.
- MCP client in the agent.
- human approval for high-risk actions.
- persisted agent run traces.
- task eval suite.
- red-team tests.

## Required Endpoints Or Commands

- start agent run.
- inspect agent run trace.
- approve/reject pending action.
- resume run.
- run eval suite.

## Required Docs

```text
docs/
  architecture.md
  demo-script.md
  eval-report.md
  red-team-report.md
  decisions/
    0001-langgraph-for-controlled-agents.md
    0002-mcp-tool-boundary.md
    0003-human-approval-policy.md
    0004-agent-evaluation.md
```

## Done Means

- Agent answers from corpus with citations.
- Agent pauses on risky tools.
- Tool calls are logged.
- Eval suite runs.
- Red-team cases are documented.
- Month 4 can harden and package the system.

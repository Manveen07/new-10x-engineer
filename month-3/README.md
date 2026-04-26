# Month 3 - Controlled Agents, MCP, And Human Oversight

## Goal

Build production-shaped agentic systems on top of the Month 1 API foundation and Month 2 RAG platform. By the end of Month 3, you should have an agentic RAG service that uses LangGraph for explicit state, calls the Month 2 RAG API as a tool, exposes selected tools through MCP, pauses for human approval on risky actions, logs every tool call, and is evaluated with task-level metrics.

The job-ready signal is not "I made an agent that can do anything." The signal is: **I can build an agent that is bounded, observable, resumable, safe, and testable.**

## Research Basis

Current production-agent guidance converges on the same themes:

- LangGraph is positioned as a low-level orchestration framework for long-running, stateful agents with durable execution, streaming, persistence, and human-in-the-loop support.
- LangGraph persistence/checkpointing enables human review, replay, memory, and fault-tolerant execution.
- MCP standardizes how apps expose tools, resources, and prompts to AI systems, but tool invocation needs explicit human oversight and security controls.
- Production agent observability must capture traces, tool calls, latency, costs, quality, and failure patterns.
- Job-relevant agent systems need bounded tool loops, deterministic state transitions, approval gates, and evals, not open-ended autonomy.

## How Month 3 Compounds Months 1-2

| Earlier skill | Month 3 use |
|---|---|
| Month 1 FastAPI/auth/settings/logging | agent API, run storage, trace endpoints |
| Month 1 provider abstraction | agent model calls and structured outputs |
| Month 2 RAG API | retrieval/search/answer tools |
| Month 2 evals | task success, groundedness, tool correctness |
| Month 2 retrieval telemetry | agent traces include retrieval traces |
| PostgreSQL | agent runs, checkpoints, approvals, tool-call logs |
| Redis | rate limits, short-lived run state, queues if needed |

## Month 3 Stack

| Area | Default | Why |
|---|---|---|
| Agent orchestration | LangGraph | explicit state, routing, checkpoints, durable execution |
| Tool boundary | typed Python tools + MCP server | local correctness first, protocol integration second |
| Retrieval tool | Month 2 `/v1/search` and `/v1/answer` | agents reuse RAG instead of rebuilding it |
| State | Pydantic/TypedDict graph state | inspectable and testable |
| Persistence | PostgreSQL checkpointer/run tables | resume, replay, audit |
| Human approval | HITL approval queue | risky actions need review |
| Observability | structlog + trace table + optional LangSmith/Langfuse | inspect tool sequence, cost, latency |
| Evaluation | task suites + tool trajectory checks | measure agent behavior, not just final text |

## Month Structure

| Week | Theme | Main deliverable |
|---|---|---|
| 9 | LangGraph fundamentals and state | bounded research/RAG agent with explicit graph |
| 10 | Tools, planning, memory, and durable execution | resumable agent with tool registry and run traces |
| 11 | MCP server/client integration | MCP tools for search/answer and safe tool invocation |
| 12 | HITL, evaluation, and capstone | agentic RAG system with approvals, evals, traces, docs |

## Daily Exercise Map

| Day | Exercise | File or folder | Required output |
|---|---|---|---|
| 41 | Agent boundaries | `exercises/day41_agent_boundaries.md` | use-case, tools, non-goals, risk table |
| 42 | LangGraph state model | `exercises/day42_langgraph_state.py` | typed state and node contracts |
| 43 | Basic graph | `exercises/day43_basic_graph.md` | plan -> retrieve -> answer graph |
| 44 | Routing and bounded loops | `exercises/day44_routing_bounded_loops.py` | loop limit and stop conditions |
| 45 | RAG tools | `exercises/day45_rag_tools.md` | Month 2 search/answer tool wrappers |
| Weekend 9 | Research/RAG agent | `exercises/weekend9_research_agent.md` | cited agent answer with trace |
| 46 | Tool registry | `exercises/day46_tool_registry.py` | typed tool schemas and permissions |
| 47 | Durable execution | `exercises/day47_durable_execution.md` | checkpoint/resume design |
| 48 | Memory design | `exercises/day48_memory_design.md` | short-term vs long-term memory rules |
| 49 | Tool failure handling | `exercises/day49_tool_failure_handling.py` | retries, fallback, degraded result |
| 50 | Agent tracing | `exercises/day50_agent_tracing.md` | trace schema for runs/tool calls |
| Weekend 10 | Resumable agent | `exercises/weekend10_resumable_agent.md` | persisted run with replay notes |
| 51 | MCP concepts | `exercises/day51_mcp_concepts.md` | tools/resources/prompts boundary |
| 52 | MCP search server | `exercises/day52_mcp_search_server.md` | expose Month 2 search as MCP tool |
| 53 | MCP client | `exercises/day53_mcp_client.md` | agent calls MCP tool |
| 54 | MCP security | `exercises/day54_mcp_security.md` | allowlist, input validation, human review |
| 55 | Prompt/resource design | `exercises/day55_mcp_resources_prompts.md` | resource and prompt templates |
| Weekend 11 | MCP integration | `exercises/weekend11_mcp_integration.md` | agent uses MCP tools safely |
| 56 | HITL approvals | `exercises/day56_hitl_approvals.md` | approval queue and decisions |
| 57 | Agent eval set | `exercises/day57_agent_eval_set.md` | task suite with expected tool paths |
| 58 | Agent metrics | `exercises/day58_agent_metrics.py` | task success, tool accuracy, cost, latency |
| 59 | Red-team tests | `exercises/day59_red_team_tests.md` | prompt injection/tool misuse cases |
| 60 | Capstone polish | `capstone/CAPSTONE.md` | agentic RAG capstone docs and demo |

## Weekly Acceptance Gates

### Week 9 Gate

- [ ] Agent state is typed.
- [ ] Graph has explicit nodes and edges.
- [ ] RAG tool calls use Month 2 API contracts.
- [ ] Tool loops are bounded.
- [ ] Agent returns citations or safe uncertainty.

### Week 10 Gate

- [ ] Tool registry includes schemas, permissions, and risk levels.
- [ ] Agent run traces are persisted.
- [ ] Tool failures are handled without runaway loops.
- [ ] Durable execution/resume design is documented.
- [ ] Memory rules avoid unbounded context growth.

### Week 11 Gate

- [ ] MCP server exposes at least search and answer tools.
- [ ] MCP client can call those tools from the agent.
- [ ] Tool inputs are validated.
- [ ] High-risk tools require explicit approval.
- [ ] MCP security assumptions are documented.

### Week 12 Gate

- [ ] HITL approval flow works.
- [ ] Agent eval suite runs.
- [ ] Metrics include task success, tool-call correctness, groundedness, cost, and latency.
- [ ] Red-team cases are documented.
- [ ] README and ADRs explain why the agent is bounded and safe.

## Not Doing In Month 3

- Fully autonomous agents with unbounded tools.
- Browser/computer control without approval gates.
- Multi-agent complexity before one agent is reliable.
- Fine-tuning.
- Production UI beyond minimal approval/demo surfaces.

## Sources Used

- LangGraph overview: https://docs.langchain.com/oss/python/langgraph/overview
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- LangGraph durable execution: https://docs.langchain.com/oss/python/langgraph/durable-execution
- LangChain HITL docs: https://docs.langchain.com/oss/python/langchain/human-in-the-loop
- Anthropic MCP introduction: https://www.anthropic.com/news/model-context-protocol
- MCP tools docs: https://modelcontextprotocol.io/docs/concepts/tools
- Ragas metrics: https://docs.ragas.io/en/stable/concepts/metrics/

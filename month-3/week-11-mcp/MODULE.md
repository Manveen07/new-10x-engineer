# Week 11: Model Context Protocol Integration

## Outcome

Expose the Month 2 RAG capabilities through MCP and call them from the Month 3 agent with typed inputs, allowlisted tools, and security rules.

## Day 51: MCP Concepts

Exercise: `../exercises/day51_mcp_concepts.md`

Learn the boundaries:

- tools: model-controlled actions.
- resources: application-controlled context.
- prompts: reusable prompt templates.
- transports and clients.

## Day 52: MCP Search Server

Exercise: `../exercises/day52_mcp_search_server.md`

Build MCP tools:

- `search_corpus`.
- `answer_from_corpus`.
- `get_document`.

## Day 53: MCP Client

Exercise: `../exercises/day53_mcp_client.md`

Build:

- MCP client connection.
- tool discovery.
- tool call wrapper.
- error mapping into agent state.

## Day 54: MCP Security

Exercise: `../exercises/day54_mcp_security.md`

Define:

- tool allowlist.
- tenant filters.
- input validation.
- output size limits.
- approval rules for risky tools.

## Day 55: MCP Resources And Prompts

Exercise: `../exercises/day55_mcp_resources_prompts.md`

Build:

- resources for corpus metadata.
- prompt templates for grounded answers and citations.

## Weekend 11: MCP Integration

Exercise: `../exercises/weekend11_mcp_integration.md`

Agent calls RAG through MCP and logs every MCP tool call.

## Week 11 Acceptance Gate

- [ ] MCP server exposes search/answer tools.
- [ ] MCP client can call those tools.
- [ ] inputs are validated.
- [ ] tenant boundaries are preserved.
- [ ] tool-call audit logs exist.

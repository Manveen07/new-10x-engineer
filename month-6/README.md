# Month 6 — Run the Funnel

## Goal

Portfolio is the asset; this month is execution. By Sunday 2026-11-08 you have 100+ outbound messages sent, 25+ formal applications submitted, 5+ first-round interviews completed, a Mercor application active, and at least one India safety application in flight — with three deployed projects + MCP server + merged OSS PR + 6 blog posts as the proof layer behind all of it.

**Pace:** 8–10 hrs/week. More if the funnel responds.
**Window:** 2026-10-12 → 2026-11-08.

## Outcome by end of month

### Funnel volume
- **Outbound:** cumulative 150 Insight Emails sent (50 in Month 5 + 100 this month).
- **Applications:** 25+ across HN/YC/Wellfound + India product startups + Mercor + Turing.
- **First rounds:** 5+ conducted.
- **Active conversations:** 3+ at the trial-engagement or full-loop stage.

### Artifacts
- Resume rewritten around three projects + production-eval framing. Outcome language, not stack language.
- 6 STAR stories drafted: hallucination audit (use Caprae 35% blocked records), eval iteration win, RAG ablation finding, agent loop caught, OSS PR conversation, outbound contract trial.
- 2 system-design mocks conducted (doc Q&A, classifier with human handoff).
- 1 project deep-dive mock conducted.
- Blog post 6 published: "What 6 months of part-time AI engineering actually looked like."

### Profile updates
- LinkedIn: "open to remote contracts and FT" + "actively interviewing" tag.
- X bio: portfolio + "open to remote AI engineering work."
- GitHub profile README: emphasizes the three deployed projects + MCP server + OSS PR.
- Mercor profile: portfolio + Loom + OSS contributions visible.

## Week themes

| Week | Window | Theme |
|---|---|---|
| 21 | Oct 12 – Oct 18 | Resume rewrite + first 10 HN/YC/Wellfound apps + 50 outbound (cumulative 100) + 5 India apps |
| 22 | Oct 19 – Oct 25 | 2 system-design mocks + 1 project mock + 10 more apps + reply to all responses within 24hrs |
| 23 | Oct 26 – Nov 1 | 50 more outbound (cumulative 150) + 5 more India apps + blog post 6 published |
| 24 | Nov 2 – Nov 8 | Interview buffer + contract-trial negotiation + follow-ups |

Week files arrive ~3 days before each week — by Month 6 they're mostly funnel templates + interview drills, lightly customized. Provisional drafts exist — refine each the weekend before it starts: [week-21.md](./week-21.md) · [week-22.md](./week-22.md) · [week-23.md](./week-23.md) · [week-24.md](./week-24.md).

## Interview prep checklist

Drill these in mocks. Each should be answerable in 3 minutes.

### Foundations
- [ ] Tokenization, embeddings, attention at the conceptual level (Karpathy's *Intro to LLMs* video sufficient).
- [ ] Prompt patterns: zero-shot, few-shot, chain-of-thought, structured outputs.
- [ ] Function calling vs JSON mode vs Instructor vs BAML — when each.
- [ ] Cost/latency reasoning per model (Sonnet vs Haiku vs GPT-5 vs GPT-5-mini).

### Evals (interview-critical)
- [ ] Three Gulfs in 60 seconds.
- [ ] Open coding → axial coding → failure taxonomy walkthrough.
- [ ] LLM-as-judge calibration: critique shadowing, binary > Likert, TPR/TNR/balanced accuracy.
- [ ] When LLM-as-judge fails (HaluEval, Soboroff IR caveat).
- [ ] Ragas metrics + their failure modes.

### RAG
- [ ] Five levels of chunking + when each.
- [ ] Anthropic Contextual Retrieval + the −67% retrieval-failure number.
- [ ] Hybrid retrieval — why BM25 still matters.
- [ ] Reranker landscape — Cohere 3.5 / Voyage Rerank 2.5 / `bge-reranker`.
- [ ] When NOT to use RAG.

### Agents + MCP
- [ ] Workflow vs agent (Anthropic framing).
- [ ] Five workflow patterns + agent pattern.
- [ ] Step budgets, tool surface area, idempotency, taint tracking.
- [ ] Trajectory vs final-output evals.
- [ ] Why multi-agent uses 10–15× tokens (Anthropic number).
- [ ] Lethal trifecta (Simon Willison).
- [ ] MCP server architecture + when to expose vs not.

### System design prompts (45 min each)
- [ ] Design a doc Q&A system.
- [ ] Design a customer-support classifier with human handoff.
- [ ] Design an LLM-powered enrichment pipeline with fallback retrieval.
- [ ] Design an MCP server for a SaaS product.
- [ ] Design an eval harness for an LLM product.

### Coding fluency
- [ ] Pydantic model for a non-trivial nested output without lookup.
- [ ] Pytest suite that runs LLM-judge evals on a golden dataset.
- [ ] BM25 + dense hybrid with RRF in <50 lines.
- [ ] Async/await for parallel LLM calls without deadlocks.
- [ ] Build an MCP server skeleton in <30 lines.

### DSA (light)
60–80 LeetCode mediums across arrays/hash maps/strings/graphs. Don't grind. If targeting GCC or Razorpay platform roles, add 30 more.

## Interview tracker

Use [interview-tracker.md](./interview-tracker.md) for every conversation. Update within 24 hrs of each call.

## Funnel math (research-backed)

- Outbound: 100–200 personalized messages → 5–10 qualified conversations → 1–3 trial contracts → 1 FT-equivalent.
- HN/Wellfound/YC: 25 thoughtful apps → 4–8 first rounds → 1–2 offers.
- Mercor: 1 application + open-source PR → 1 calibration call → 1 placement (~60-day cycle).
- India product startups: 10–15 apps → 2–4 first rounds → 1 offer (lower velocity).

Total realistic outcome by end of month: 1–3 active offer cycles. If 0 active by end of Week 24, **extend funnel into Nov–Dec** with another 100 outbound + 25 apps. The portfolio is built; conversion is volume.

## Monthly checklist

See [EXERCISES.md](../EXERCISES.md) Month 6 section.

## Behind if

- Fewer than 100 outbound messages sent (cumulative).
- Fewer than 25 applications submitted.
- Fewer than 3 first-round interviews completed.
- No India safety apps in parallel.
- Blog post 6 not published.

## What "done" looks like (Nov 8, 2026)

7+ of these checked:

- [ ] 3 deployed projects with eval suites, READMEs to standard, Loom, live URLs.
- [ ] 1 MCP server demoable.
- [ ] 1 merged OSS PR.
- [ ] 4–6 blog posts on your own domain.
- [ ] GitHub: 4–6 months of daily-ish activity + pinned repos + profile README.
- [ ] X: 30+ substantive posts/replies.
- [ ] LinkedIn updated + open to remote.
- [ ] **Funnel:** 100+ outbound + 25+ applications + 5+ first rounds + Mercor active + India safety apps in flight.
- [ ] 1 lightning talk delivered or recorded.
- [ ] 1+ active offer cycle.

If 7+, you're ready. The first offer is a function of funnel volume from here — if none active, you have the artifacts; keep the funnel running into Q1 2027 with another 100 outbound + 25 apps/month.

## What's next (post-roadmap)

This is a 24-week scaffold, not a 24-week ceiling. After the first offer:

- The next 6 months: deepen one specialization (agent eng, RAG eng, or FDE) at the new role.
- 12-month horizon: jump from junior → mid-level at a frontier or fast-growing AI startup (Sierra, Decagon, 11x, Glean, Harvey — or Anthropic/OpenAI Applied if comp is the bar).
- 18-month horizon: tech-lead path inside the company you joined, or your own AI-eng consultancy if outbound was your strongest channel.

The roadmap is a launchpad, not the destination.

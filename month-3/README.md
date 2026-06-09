# Month 3 — RAG Fundamentals + docsight Design + First OSS PR Opened

## Goal

Learn the retrieval stack deeply before building docsight in Month 4. Open your first OSS PR. You graduate this month (BTech, Aug 2026) — exams already done; only graduation week itself may need a lighter Saturday.

**Pace:** 8–10 hrs/week.
**Window:** 2026-07-20 → 2026-08-16.

## Outcome by end of month

- Anthropic Contextual Retrieval implemented on a toy corpus.
- 30-min LlamaIndex notebook + 30-min Pinecone notebook done (for interview vocabulary).
- docsight stack picked + committed to `STACK.md`: Postgres + pgvector + BM25 + reranker + FastAPI + Modal + Langfuse.
- Local Postgres + pgvector running in Docker Compose.
- docsight `DESIGN.md` complete.
- `projects/gtm-clay-rag/` renamed to `projects/docsight/` via `git mv`.
- OSS target repo picked; **draft PR or issue opened with maintainer engagement** (not just `# typo fix`).
- Blog post 3 published: "What I'm setting up before writing a line of RAG code."

## Week themes

| Week | Window | Theme |
|---|---|---|
| 9 | Jul 20 – Jul 26 | Anthropic Contextual Retrieval + 5 Levels of Text Splitting + pick OSS target |
| 10 | Jul 27 – Aug 2 | Jason Liu RAG content + 30-min LlamaIndex + 30-min Pinecone |
| 11 | Aug 3 – Aug 9 | docsight stack decision + Postgres+pgvector Docker Compose |
| 12 | Aug 10 – Aug 16 | `DESIGN.md` + draft OSS PR + blog post 3 |

Week files arrive ~3 days before each week (see [month-2 README](../month-2/README.md) for the rationale). Provisional drafts exist — refine each the weekend before it starts: [week-9.md](./week-9.md) · [week-10.md](./week-10.md) · [week-11.md](./week-11.md) · [week-12.md](./week-12.md).

## Required reading

- **Anthropic — *Introducing Contextual Retrieval*** (Sept 2024). Implement the prompt verbatim.
- **Greg Kamradt — *5 Levels of Text Splitting*** notebook. Run all five splitters on one corpus.
- **Jason Liu — *Improving RAG*** + his posts on search vs retrieval. Pick 3 posts.
- **Hamel Husain — RAG eval guidance** (skim `field-guide-to-rapidly-improving-ai-products` for the retrieval-eval section).

## OSS target — pick one

(Mercor's interview is exclusively about your OSS contributions — pick well.)

- **Instructor** (jxnl/instructor) — cookbook example using leadlens. Jason Liu is responsive.
- **Langfuse** — adapter or eval example. Discord is active.
- **Ragas** — domain-specific metric or dataset adapter.
- **simonw/llm** — write a plugin. Lowest barrier, highest visibility.
- **LiteLLM** — provider adapter PR.
- **PydanticAI** — lower competition, growing.

Pick by end of Week 9. Lurk in the issue tracker + Discord for one week. Open a draft PR or proposal issue by end of Week 12.

## Monthly checklist

See [EXERCISES.md](../EXERCISES.md) Month 3 section.

## Interview skill added

You can answer **"Walk me through how you'd build a production RAG system"** in 3 minutes:
- Why hybrid retrieval beats pure dense (BM25 for technical identifiers + dense for semantics).
- Why contextual retrieval matters (Anthropic's −67% retrieval-failure number).
- Why rerank as a default stage.
- How you'd measure each layer (retrieval evals separate from generation evals).
- When you'd skip RAG entirely (long-context model + small static corpus).

## Behind if

- No `DESIGN.md` for docsight.
- No OSS PR or proposal issue opened.
- Cannot explain why hybrid retrieval beats pure dense in 30 seconds.
- Blog post 3 not published.

## Next month

→ [../month-4/README.md](../month-4/README.md) — Ship docsight + merge OSS PR + apply to Mercor.

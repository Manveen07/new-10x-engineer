# Month 1 Exercises

This folder contains the practice path for Month 1. The exercises are ordered so each small skill feeds the capstone Q&A API.

## How To Use

1. Do the daily exercise.
2. Move the useful pattern into `../capstone/qa-api/`.
3. Add or update one test.
4. Record any important tradeoff in an ADR if it affects the capstone.

## Exercise Checklist

| Day | Exercise | Output |
|---|---|---|
| 0 | `day0_tooling_setup.md` | uv, Ruff, mypy, pytest, first ADR |
| 1 | `day1_coroutines.py` | coroutine and event-loop basics |
| 2 | `day2_gather.py` | concurrent task execution |
| 3 | `day3_semaphores.py` | bounded concurrency and rate limiting |
| 4 | `day4_queue.py` | producer-consumer backpressure |
| 5 | `day5_taskgroup.py` | structured concurrency and cancellation |
| Weekend 1 | `weekend1_scraper_pipeline.py` | async pipeline |
| 6 | `day6_fastapi_structure.py` | FastAPI structure and dependency injection |
| 7 | `day7_pydantic_validation.py` | Pydantic schemas and error envelope |
| 8 | `day8_auth.py` | JWT auth and RBAC |
| 9 | `day9_middleware.py` | middleware, logging, rate limits |
| 10 | `day10_database.py` | async DB and migrations |
| Weekend 2 | `weekend2_fastapi_starter/README.md` | capstone API starter |
| 11 | `day11_explain_analyze.py` | query plan analysis |
| 12 | `day12_indexing.py` | index benchmarks |
| 13 | `day13_query_tuning.py` | slow query rewrites |
| 14 | `day14_adapter_pattern.py` | LLM provider adapter |
| 15 | `day15_strategy_factory.py` | strategies and factories |
| Weekend 3 | `weekend3_provider_observability.md` | provider integration and logs |
| 16 | `day16_redis_vectors.py` | Redis vector search |
| 17 | `day17_semantic_cache.py` | semantic cache |
| 18 | `day18_cache_tuning.py` | threshold tuning and cost report |
| 19 | `day19_ai_system_design.md` | architecture and failure modes |
| 20 | `../capstone/CAPSTONE.md` | final capstone integration |

## Completion Rule

Month 1 is complete only when the capstone can run in mock mode without paid API keys and the tests prove both cache-hit and cache-miss paths.

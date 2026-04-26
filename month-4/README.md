# Month 4 - Production Hardening, Deployment, And Portfolio

## Goal

Turn the systems from Months 1-3 into a job-ready portfolio: reliable services, CI/CD, deployment docs, observability, benchmark reports, security checks, demo scripts, resume bullets, and interview narratives.

The job-ready signal is: **I can ship, operate, explain, and defend an AI system, not just build a demo.**

## How Month 4 Compounds Months 1-3

| Earlier work | Month 4 production layer |
|---|---|
| Month 1 Q&A API | harden API, auth, logs, health, deployment |
| Month 2 RAG API | benchmark quality, latency, retrieval traces |
| Month 3 Agentic RAG | evaluate agent tasks, HITL traces, red-team cases |
| All months | root portfolio README, demos, resume bullets, interview stories |

## Month Structure

| Week | Theme | Main deliverable |
|---|---|---|
| 13 | Reliability and security | health checks, smoke tests, failure modes, threat model |
| 14 | CI/CD and deployment | GitHub Actions, Docker, Cloud Run deployment docs |
| 15 | Observability and benchmarks | metrics, traces, eval dashboards/reports, cost report |
| 16 | Portfolio and interview packaging | case studies, resume bullets, demo script, final polish |

## Daily Exercise Map

| Day | Exercise | File or folder | Required output |
|---|---|---|---|
| 61 | Production audit | `exercises/day61_production_audit.md` | system gap checklist |
| 62 | Health and smoke tests | `exercises/day62_health_smoke_tests.md` | smoke scripts for all services |
| 63 | Security threat model | `exercises/day63_security_threat_model.md` | threat model and mitigations |
| 64 | Failure drills | `exercises/day64_failure_drills.md` | Redis/DB/provider/RAG/agent outage plan |
| 65 | Secrets and config | `exercises/day65_secrets_config.md` | env/secret handling checklist |
| Weekend 13 | Reliability pack | `exercises/weekend13_reliability_pack.md` | runbook and smoke tests |
| 66 | CI pipeline | `exercises/day66_ci_pipeline.md` | lint/type/test workflow |
| 67 | Docker hardening | `exercises/day67_docker_hardening.md` | Dockerfile and compose review |
| 68 | Cloud Run deployment | `exercises/day68_cloud_run_deployment.md` | service/job deploy docs |
| 69 | Release workflow | `exercises/day69_release_workflow.md` | versioning and rollback notes |
| 70 | Environment strategy | `exercises/day70_environment_strategy.md` | local/staging/prod config |
| Weekend 14 | Deployment pack | `exercises/weekend14_deployment_pack.md` | deploy-ready docs and scripts |
| 71 | Observability schema | `exercises/day71_observability_schema.md` | metrics/logs/traces map |
| 72 | Benchmark reports | `exercises/day72_benchmark_reports.md` | quality/latency/cost reports |
| 73 | Eval dashboard plan | `exercises/day73_eval_dashboard_plan.md` | eval reporting structure |
| 74 | Cost controls | `exercises/day74_cost_controls.md` | token/cache/retry cost report |
| 75 | Red-team report | `exercises/day75_red_team_report.md` | safety and misuse report |
| Weekend 15 | Observability pack | `exercises/weekend15_observability_pack.md` | final benchmark/eval reports |
| 76 | Root README | `exercises/day76_root_readme.md` | repo-level portfolio README |
| 77 | Case studies | `exercises/day77_case_studies.md` | Month 1-3 case studies |
| 78 | Resume bullets | `exercises/day78_resume_bullets.md` | recruiter-readable bullets |
| 79 | Interview stories | `exercises/day79_interview_stories.md` | STAR stories |
| 80 | Final portfolio polish | `capstone/CAPSTONE.md` | complete portfolio package |

## Acceptance Gates

### Week 13 Gate

- [ ] smoke tests exist.
- [ ] failure modes are documented.
- [ ] threat model exists.
- [ ] secrets/config checklist exists.
- [ ] runbook explains how to debug outages.

### Week 14 Gate

- [ ] CI workflow exists.
- [ ] Docker/deployment docs exist.
- [ ] staging/prod environment strategy exists.
- [ ] rollback plan exists.

### Week 15 Gate

- [ ] benchmark reports exist.
- [ ] eval reports exist.
- [ ] cost report exists.
- [ ] observability schema maps logs, traces, metrics, and evals.

### Week 16 Gate

- [ ] root README explains the full system in under five minutes.
- [ ] capstone case studies exist.
- [ ] resume bullets exist.
- [ ] interview stories exist.
- [ ] demo script exists.

## Sources Used

- Google Cloud Run service docs: https://cloud.google.com/run/docs
- Google Cloud Run jobs docs: https://cloud.google.com/run/docs/create-jobs
- OpenTelemetry concepts: https://opentelemetry.io/docs/concepts/
- GitHub Actions docs: https://docs.github.com/actions
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/

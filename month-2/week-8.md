# Week 8 — leadlens: Deploy on Modal + README to Standard + Loom + Blog Post 2

> 📝 **Draft written 2026-06-09, ahead of the window.** Refine before Week 8, anchored on Week 7's final numbers (those numbers go straight into the README + post). leadlens = AI **JD** classifier (Gemini 2.5 Flash). Spec: [../projects/business-classification-pipeline/DESIGN.md](../projects/business-classification-pipeline/DESIGN.md).

**Window:** Mon 2026-07-13 → Sun 2026-07-19
**Time budget:** 8–10 hours
**Position:** Month 2, Week 8 of 24 — **Month 2 ship week.**

## Why this week matters

This is where leadlens stops being "runs on my laptop" and becomes a link a US founder can click. The deepest Month-2 lesson lands here: **production = a public URL + observability + a CI gate.** By Sunday you have a live Modal endpoint, a README that answers all seven [portfolio questions](../PROJECTS.md#portfolio-rule) without you in the room, a 3-min Loom, and blog post 2 published.

**The single must-do:** leadlens live at a public Modal URL with the README to standard + blog post 2 published, by Sunday night.

## At-a-glance daily plan

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-07-13 | Plan review + **kata 24** (`@modal.fastapi_endpoint` + Pydantic request body, no AI) | 15 min |
| Tue eve | 2026-07-14 | **Kata 25** (write a `Dockerfile` for a `uv` app from memory, no AI) | 15 min |
| Wed eve | 2026-07-15 | **LeetCode ×1** (graph/matrix) → `dsa/` | 20 min |
| Thu eve | 2026-07-16 | **LeetCode ×1** (review a missed one cold) → `dsa/` | 20 min |
| Fri eve | 2026-07-17 | Draft the README "where it fails" section OR rest | 15–30 min |
| **Sat** | 2026-07-18 | **Big build**: FastAPI `POST /classify` + `POST /judge` → Docker → Modal deploy → live URL + GitHub Actions CI gate green | **3.5 hrs** |
| **Sun** | 2026-07-19 | **Big build**: README to standard + 3-min Loom + blog post 2 publish + X/LinkedIn + Month-2 review | **4 hrs** |

Total: ~10 hours.

---

## Saturday — deploy + CI gate (3.5 hrs)

### Revise (15 min)
Restate the two deployment shapes (serverless scale-to-zero vs always-on container) and why Modal's scale-to-zero fits a low-traffic portfolio endpoint. Know the cold-start tradeoff before you hit it.

### Build A — FastAPI + Docker + Modal (2 h)
- `POST /classify` (JD in → `Classification` out) and `POST /judge` (JD + classification → scam verdict). Pydantic request/response models = the existing schema.
- Dockerfile for the `uv` app. Modal: `@modal.fastapi_endpoint` (or `@modal.asgi_app` wrapping FastAPI), load the model client once at startup, not per-request.
- Deploy → live URL. Hit it from `curl` / incognito. Langfuse traces still firing in prod.

### Build B — CI gate (60 min)
- GitHub Actions workflow: on push, run `pytest` over the golden set, **fail the build if category accuracy < 75% or judge TPR/TNR drops below threshold.** This is the artifact behind "the eval runs in CI" — screenshot the green check for the README.

### Recall (15 min)
*"What does your CI gate actually protect against?"* (A prompt/model change that silently regresses accuracy or starts missing scams.)

## Sunday — README + Loom + blog post 2 (4 hrs)

### README to standard (90 min) — answers all 7 portfolio questions
Problem (3 sentences) · architecture diagram (excalidraw PNG) · fresh-`uv`+Docker run instructions · **"Where it fails"** (F-003/F-004/F-006 + any new, with one real JD example) · eval table (per-category accuracy + judge TPR/TNR) · cost ($/JD + $/100-run) · latency p50/p95 · stack-with-rationale (why Gemini Flash, why schema-as-eval-spec) · founder one-liner header. Embed the confusion matrix + a Langfuse trace screenshot.

### 3-min Loom (45 min)
Problem → architecture → live demo (paste a real scam JD, show it caught) → eval table → "where it fails." Re-record until ≤3 min. Embed at top of README + the blog post.

### Blog post 2 (90 min) — "Auditing my own LLM classifier"
Walk one JD through the F-006 scam under-call, the few-shot fix, the TNR 0.882 → 0.91 move. Real numbers, failure-mode honesty, the schema-as-eval-spec angle as the spine. Publish on your domain + LinkedIn + X thread. (Run it past the [spam-word / deliverability] lens if you'll reuse any of it in outreach later.)

### Month-2 review (close)
- Fill PROGRESS Month-2 monthly review + record the Month-2 Demo Day Loom.
- **Advance [START_HERE.md](../START_HERE.md) pointer to Month 3 / Week 9** — only now, with leadlens deployed + post 2 live.

## Behind if
- No public deployment / live URL.
- README missing any of the 7 portfolio answers (esp. "where it fails").
- No Loom; blog post 2 not published.
- CI gate not green (or doesn't exist).

## Month 2 "done" bar
- [ ] leadlens live at a public Modal URL.
- [ ] 100-JD golden set committed; per-category confusion matrix in README.
- [ ] Scam judge TPR=1.0 / TNR ≥0.90, running in CI.
- [ ] README to standard (7 portfolio questions answered) + Langfuse trace screenshot.
- [ ] 3-min Loom + blog post 2 published + cross-posted.
- [ ] PROGRESS Month-2 review filled.

Hit 5/6 → Month 2 truly done. Then Month 3 (RAG fundamentals + docsight design).

## Next month
→ [../month-3/README.md](../month-3/README.md) — RAG fundamentals + docsight design + first OSS PR.

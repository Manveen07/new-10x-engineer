# Month 1 — Finish Plan (day-by-day, weekend-loaded)

The detailed close-out for Month 1. Window ends **2026-06-21**. Two weekends + weekday touches left.

**Operating rules (locked with Manveen):**
- **No blind spots.** Goal is "knows how things work + good for interviews," not just shipped artifacts.
- **Every session = revise → build → recall.** Never pure task-mode. If a session would touch 3 concepts, split into 3 sessions.
- **Weekend-loaded.** Saturday is the heaviest day (most work happens then). Sunday second. Weekdays = 15–20 min touches only (job Mon–Fri).
- **Compounding > calendar.** If a block slips, it carries; don't skip the learning to hit a date.

---

## Status — 2026-06-09 (single source of truth for the Month 1 close-out)

**This file is the operative plan for finishing Month 1.** [week-3.md](week-3.md) / [week-4.md](week-4.md) hold extra daily-kata + code detail, but when they disagree with this file on *what to do next*, this file wins.

**You're ahead of the calendar.** Git shows "Weekend 1" is essentially done already:

- [x] Fundamentals to green — tokens / embeddings / attention / transformer stack, all 5 retention slips closed (commits Jun 7–8). *Self-verify: explain attention aloud in 90 sec before ticking the done-bar box.*
- [x] Eugene Yan 7 LLM patterns read + mapped to leadlens / docsight / reposcout (Jun 8).
- [x] leadlens `DESIGN.md` committed (Jun 8).
- [~] Judge **v1** live: TPR=1.0 / TNR=0.882 (Jun 7). Built — but not yet at the TNR ≥0.90 target.

**Remaining for Month 1 (by 2026-06-21), in priority order:**
1. `failure-taxonomy.md` — formalize the v2 taxonomy into 4–7 named categories, committed.
2. Judge → **TNR ≥0.90, TPR=1.0** (the "Weekend 2" judge iteration; few-shot + borderline rule).
3. **Publish blog post 1** — the single highest-leverage Month 1 artifact (see Weekend 2 below).
4. Anthropic Academy prompt course (cert) → interview Cluster 1 self-test all 🟢 → Demo Day Loom → PROGRESS monthly review.

So your weekends are freed for **depth + the blog post**, not racing into Month 2. That is the 10x move here: bank the lead into a publishable artifact + interview-ready fundamentals, not more half-built code.

---

## The blind-spot gap this plan closes

Applied progress is strong (leadlens classifier + calibrated judge + cost/latency). **The gap is fundamentals** — being able to explain *how things work under the hood* in an interview: tokens, embeddings, attention, transformers, ML basics. Research (2026 interview guides) confirms these are the most-asked "do you actually understand LLMs" questions. Weekday micro-lessons below close this without stealing weekend build time.

---

## Study materials (researched, best-in-class, all free)

| Source | Use for | Format |
|---|---|---|
| [Karpathy — Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) | Tokens → attention → training, mechanical | 3.5h video (watch in chunks) |
| [3Blue1Brown — Neural Nets / GPT / Attention series](https://www.3blue1brown.com/topics/neural-networks) | Visual intuition for attention + transformers | ~1h video |
| [Hugging Face LLM Course](https://huggingface.co/learn/llm-course) | Transformer architecture, tokenization, fine-tuning (free cert) | Interactive notebooks |
| [Anthropic Academy](https://www.anthropic.com/learn) | Prompt engineering, building with Claude, agentic (free cert, most current) | Interactive |
| [Eugene Yan — LLM Patterns](https://eugeneyan.com/writing/llm-patterns/) | 7 reusable system patterns | Blog |
| [Hamel — evals-faq](https://hamel.dev/blog/posts/evals-faq/) | Eval canon (re-read into leadlens) | Blog |
| [REFERENCE.md](../REFERENCE.md) | Your own cheat-sheet — specific 2026 numbers for interviews | Repo |
| [interview_prep_qa.md](../interview_prep_qa.md) | 5-cluster Q&A drill | Repo |

**Rule:** never read a source without the matching build/recall open. If you finish a source and can't state its 2–3 key points, you read passively — re-read into the work.

---

## Weekday touches (Mon–Fri, 15–20 min each) — the fundamentals drip

One micro-lesson per weekday evening. **Revise** prior day's point first (60 sec recall), then **learn** today's. Log one line in `katas/LEARNINGS.md` under a new "Fundamentals" section.

### Week A weekdays
- **Mon — Tokenization.** Watch Karpathy 0:00–30:00 (tokenizer section) OR read [HF tokenizer chapter]. Recall: "what is a token, why not characters or words?"
- **Tue — Embeddings + vector space.** What turns a token into a vector; why similar meanings → near vectors; cosine similarity. Recall: "why does vector search find paraphrases but miss exact codes?" (ties to your RAG month).
- **Wed — Attention (intuition).** 3Blue1Brown attention video. Recall: "what does 'every token looks at all previous tokens' mean?"
- **Thu — Attention (mechanical).** Q/K/V in one sentence each. Recall: "what are query, key, value?"
- **Fri — Transformer stack.** Layers stack; early layers = surface patterns, late = reasoning. Recall: "why do more layers help?" Light day — OK to rest if work was brutal.

### Week B weekdays
- **Mon — ML basics vocab.** Supervised vs unsupervised, train/test split, overfitting. (You know this from AsanaBot — formalize the words.) Recall: "what is overfitting in one sentence?"
- **Tue — Temperature / sampling.** How an LLM picks the next token; temp, top-p. Recall: "what does temperature=0 vs 1 change?"
- **Wed — Context window + KV cache (concept).** Why long context costs more (n² attention). Recall: "why does a 10-turn chat get expensive?" (ties to cost modeling).
- **Thu — Prompt patterns.** zero-shot / few-shot / chain-of-thought / structured output. Recall: name all four.
- **Fri — Function calling / tool use (concept).** How an LLM "calls" a tool. Recall: "what does the model actually output when it 'uses a tool'?" Light day.

By end of weekday drips: you can answer every fundamentals question in interview_prep_qa.md Cluster 1 cold.

---

## Weekend 1 (Sat + Sun) — Fundamentals deep-dive + leadlens close

### Saturday (3.5–4 h) — THE fundamentals block
- **Revise (15 min):** the week's tokenization/embeddings/attention micro-lessons. Say each aloud.
- **Build/learn (2.5 h):**
  - Karpathy "Deep Dive into LLMs" — watch the parts you haven't (pause, take 5 notes in `notes/fundamentals.md`).
  - One hands-on: open the HF tokenizer in a notebook, tokenize 3 sentences, look at the token IDs, see how "unhappiness" splits. 20 min. *Seeing it beats watching it.*
- **Eugene Yan patterns (60 min):** read [LLM Patterns](https://eugeneyan.com/writing/llm-patterns/). For each of 7 patterns write 1 line "this changes Y in leadlens" in `notes/fundamentals.md`.
- **Recall (15 min):** explain attention to me in 90 sec, no notes. Explain 3 of Eugene Yan's patterns.

### Sunday (3–3.5 h) — leadlens DESIGN.md + judge v2
- **Revise (15 min):** what makes a good design doc (REFERENCE.md Appendix A "design first"; a design doc explains past-you's decisions to future-you).
- **Build (90 min):** write `projects/business-classification-pipeline/DESIGN.md`. Sections: Problem / Input contract / Output schema (rationale per field) / Eval methodology / Named failure modes (F-003…F-006) / Metrics + thresholds / Deployment plan. Pull from iteration-1, iteration-2, judge_v1.
- **Build (60 min):** judge v2 — add 2 few-shot examples (1 positive MIIGO, 1 negative Sumble) to the prompt; tighten "vague + real product ≠ scam." Re-run. Target TNR 0.882 → 0.90+ without dropping TPR below 1.0.
- **Recall (15 min):** explain why each Pydantic field in the schema exists. Update PROGRESS.md (Sunday log + confidence re-rate).

**Behind if:** DESIGN.md not written, or can't explain attention in 90 sec.

---

## Weekend 2 (Sat + Sun) — Blog post 1 + Month 1 review

### Saturday (3.5–4 h) — Blog post 1 (the highest-leverage Month 1 artifact)
- **Revise (15 min):** what makes a post interview-grade (REFERENCE.md "Interviews": production-failure stories + cost modeling + failure-mode fluency).
- **Build (2 h):** write "Schema-as-eval-spec: three failure modes I killed by construction in a JD classifier." Real numbers: 70% category accuracy, $0.00085/JD, judge TPR=1.0/TNR=0.90. Hook = F-006 scam-detection + the schema fix. Failure-mode honesty throughout.
- **Publish (45 min):** on your domain (manveen.me). LinkedIn cross-post + X thread.
- **Recall (15 min):** can you explain "schema-as-eval-spec" to a non-AI engineer in 90 sec? If yes, the post works.

### Sunday (3 h) — Month 1 review + Anthropic Academy + interview self-test
- **Anthropic Academy (90 min):** the Prompt Engineering course (free, current, cert). Hands-on; directly upgrades your leadlens prompts.
- **Interview self-test (45 min):** open interview_prep_qa.md Cluster 1 (evals) + the fundamentals questions. Answer each aloud, rate 🟢/🟡/🔴. Every 🔴 → note for a weekday drip.
- **Month 1 monthly review (45 min):** fill PROGRESS.md monthly-review section. Record a 3-min Demo Day Loom walking through: portfolio site → leadlens classifier → judge calibration → blog post. Post on LinkedIn.

**Behind if:** blog post not published, or >3 🔴 on Cluster 1 interview questions.

---

## Month 1 "done" bar (2026-06-21)

- [x] Fundamentals: can explain tokens, embeddings, attention, transformer stack, temperature, context-window-cost — each in <60 sec. *(retention drills green Jun 8 — verify temp + context-cost aloud)*
- [x] Eugene Yan 7 patterns read + applied to leadlens. *(Jun 8)*
- [x] leadlens DESIGN.md committed. *(Jun 8)*
- [ ] judge v2 at TNR ≥ 0.90, TPR = 1.0. *(at v1: TNR=0.882 — push remaining)*
- [ ] Blog post 1 published on own domain + cross-posted. **← single must-do remaining**
- [ ] Anthropic Academy prompt course done (cert).
- [ ] interview_prep_qa.md Cluster 1 all 🟢.
- [ ] Demo Day Loom recorded.
- [ ] PROGRESS.md monthly review filled.

Hit 7/9 → Month 1 truly done (not just calendar-done). Then Month 2 (deploy + Langfuse + 100-JD golden set) starts.

---

## Why this order compounds

Fundamentals (Wknd 1 Sat) → makes the DESIGN.md sharper (you understand *why* the schema works) → makes the blog post credible (you can explain the mechanism, not just the result) → makes the interview self-test pass (you can defend it live). One thread, four shapes. No isolated busywork.

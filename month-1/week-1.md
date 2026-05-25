# Week 1 — No-AI Code Rebuild + Portfolio Site Live

**Window:** Mon 2026-05-25 → Sun 2026-05-31
**Time budget:** 8–10 hours
**Position:** Month 1, Week 1 of 24

## Why this week matters

You said your coding has rusted because AI writes most of it. That's the single biggest risk to landing the role you want — every junior screen tests live coding, and live coding catches over-reliance on AI inside 15 minutes.

This week rebuilds the muscle. You'll write code *by hand* every day, set up the modern Python tooling that every 2026 JD lists (`uv`, `ruff`, `pytest`, `pre-commit`), refresh your two strongest existing projects (AsanaBot and PresentAI) so they read like a real portfolio, and stand up a personal site so the rest of the plan has somewhere to ship to.

**The single must-do:** all five no-AI katas, even if everything else slips. The katas are the foundation.

## At-a-glance daily plan (weekday-light, weekend-heavy)

| Day | Date | Task | Time |
|---|---|---|---|
| Mon eve | 2026-05-25 | 5-min plan review + **kata 1** (Pydantic, no AI) | 15 min |
| Tue eve | 2026-05-26 | **Kata 2** (async + httpx, no AI) | 15 min |
| Wed eve | 2026-05-27 | **Kata 3** (context manager, no AI) | 15 min |
| Thu eve | 2026-05-28 | **Kata 4** (pytest fixture + parametrize, no AI) | 15 min |
| Fri eve | 2026-05-29 | **Kata 5** (typing + retry, no AI) OR rest | 15 min |
| **Sat** | 2026-05-30 | **Big build block**: install modern Python stack (`uv`/`ruff`/`pytest`/`pre-commit`) + stand up portfolio site (Quarto) + AsanaBot README refresh | **3.5 hrs** |
| **Sun** | 2026-05-31 | **Big block**: PresentAI README refresh + Cursor/Claude Code setup + Hamel `evals-faq` re-read with traces open + first tweet + PROGRESS.md update | **3.5 hrs** |

Total: ~9 hrs (75 min weekdays + ~7 hrs weekends). If a task overruns 2× its budget, stop and log in PROGRESS.md instead of pushing through.

**The single must-do:** all five katas. Even if Saturday + Sunday get only half done, the katas keep the rebuild on track.

---

## Weekday evenings (Mon–Fri, 15 min each) — katas only

Each weekday after work: open the project, do the day's kata with **no AI**, commit, done. 15 minutes max — if you blow past that, stop and log a Stuck Box entry in PROGRESS.md rather than push through.

You don't have `uv` installed yet (Saturday job). For weekday katas this week, just use whatever Python you have:
```powershell
cd "C:\Users\Manveen\Desktop\new_things_to_mess_araound\new 10x engineer"
mkdir katas
cd katas
python -m venv .venv
.venv\Scripts\activate
pip install pydantic httpx pytest pytest-asyncio
```

Then each evening:

### Monday eve — kata 1 (nested Pydantic, no AI)
File: `katas/kata_01_pydantic.py`. Close the Cursor AI panel. Close Claude Code. Without help, write a `Company` model with: `name: str`, `domain: str | None`, `status: Literal["operating","closed","uncertain"]`, `signals: list[Signal]` where `Signal` has `name: str`, `evidence: str`, `confidence: float` constrained 0–1. Plus a `parse_company(d: dict) -> Company` that catches `ValidationError` and returns a `Company` with `status="uncertain"`. Add 3 tests in `tests/test_kata_01.py`. Run `pytest tests/test_kata_01.py -v` until green. Commit.

### Tuesday eve — kata 2 (async fetcher, no AI)
File: `katas/kata_02_async.py`. Write `fetch_one(client, url)` returning `{"url", "status", "size"}` and `fetch_many(urls)` using `asyncio.gather` over a single `httpx.AsyncClient`. One test. Run and commit.

### Wednesday eve — kata 3 (context manager, no AI)
File: `katas/kata_03_ctxmgr.py`. Write a `timed()` context manager via `@contextlib.contextmanager` that prints elapsed time on exit. Then a class-based version via `__enter__` / `__exit__`. Two tests. Commit.

### Thursday eve — kata 4 (pytest fixture + parametrize, no AI)
File: `katas/kata_04_pytest.py`. Write a `summarize(c: Company) -> str` that returns a one-line summary. In `tests/test_kata_04.py`, write a `@pytest.fixture` that yields a sample `Company`, then a `@pytest.mark.parametrize` test with 4 different inputs. Commit.

### Friday eve — kata 5 (typing + retry, no AI) OR rest
File: `katas/kata_05_typing.py`. Write an `async with_retry(fn: Callable[[], Awaitable[T]], attempts=3, backoff=0.5) -> T` that retries with exponential backoff. One async test that confirms retries happen. Commit.

If Friday after work is brutal, skip — do kata 5 first thing Saturday before the build block.

**End of every weekday:** tick the kata box in PROGRESS.md Week 1. Takes 5 seconds.

---

## Saturday — Big build block (3.5 hrs)

Block on your calendar 9 AM – 1 PM (or whenever you're freshest). Three goals:

### 1. Install modern Python stack (45 min)

```powershell
# uv — modern Python package + project manager (replaces pip + venv)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version

# Re-init the katas folder properly with uv
cd "C:\Users\Manveen\Desktop\new_things_to_mess_araound\new 10x engineer\katas"
uv init . --no-pin-python
uv add pydantic httpx pytest pytest-asyncio ruff pre-commit
uv run ruff --version
uv run pytest -v   # all 4–5 katas should still pass
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
      - id: ruff-format
```

```powershell
uv run pre-commit install
uv run pre-commit run --all-files
```

Done when: `uv run pytest` is green and `uv run ruff check .` returns clean.

### 2. Portfolio site live at your domain (1.5 hrs)

Pick Quarto (faster) or Astro (more design control). Quarto path:

```powershell
winget install Quarto.Quarto
quarto --version

cd "C:\Users\Manveen\Desktop\new_things_to_mess_araound\new 10x engineer"
quarto create-project site --type website
cd site
```

Edit `_quarto.yml`:
```yaml
project:
  type: website
website:
  title: "Manveen Singh"
  navbar:
    right:
      - href: index.qmd
        text: Home
      - href: posts/index.qmd
        text: Blog
      - icon: github
        href: https://github.com/Manveen07
format:
  html:
    theme: cosmo
```

Replace `index.qmd`:
```markdown
---
title: "Manveen Singh"
---

AI engineer building LLM systems with evals and MCP servers.
Final-year BTech CS. Open to remote contracts.

- [GitHub](https://github.com/Manveen07)
- [LinkedIn](https://linkedin.com/in/Manveen)
- [Email](mailto:manveen9650@gmail.com)

## Projects

- **AsanaBot** — real-time yoga pose feedback with Vision Transformers + MediaPipe.
- **PresentAI** — AI SaaS that auto-generates slide decks from project briefs.
- *(Coming July)* **leadlens** — LLM classifier with eval-first design.

## Blog → [All posts](posts/)
```

Create `posts/index.qmd` with a listing block + one stub post so the build doesn't break.

Deploy:
```powershell
quarto publish gh-pages
```

Pushes to `gh-pages` branch, serves at `https://manveen07.github.io/<repo>`. For your custom domain: add a `CNAME` file in the published output with your domain, then point DNS A records per [GitHub Pages docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

Done when: incognito browser shows your live site at your domain.

### 3. AsanaBot README refresh (1 hr)

Open the AsanaBot repo (separately on GitHub). Replace the top of the README:

```markdown
# AsanaBot — Real-time Yoga Pose Feedback

Real-time computer vision system that detects yoga poses from webcam video and gives instant corrective feedback. Vision Transformers + MediaPipe + OpenCV.

![demo](docs/demo.gif)

## Why
Most yoga apps are video libraries with no feedback loop. AsanaBot watches you and tells you when your alignment drifts.

## How it works
Input frame → MediaPipe pose landmarks → ViT classifier (5 asanas) → alignment scoring vs reference → visual overlay.

## Where it fails
- Poor lighting drops landmark confidence; ViT then over-classifies as "downward dog" (largest training class).
- Lateral camera angles confuse hip-knee landmarks.
- Body-shape variation degrades accuracy on advanced poses.

## Stack
Python 3.11, PyTorch, Vision Transformers (`timm`), MediaPipe, OpenCV.

## Run locally
```bash
git clone ...
uv sync
uv run python app.py
```
```

Record a 10-second GIF (use ShareX or LICEcap; alternative: 5 screenshots stitched). Commit. Push.

### End of Saturday

Commit everything in the roadmap repo:
```powershell
cd "C:\Users\Manveen\Desktop\new_things_to_mess_araound\new 10x engineer"
git add katas/ site/
git commit -m "week-1 sat: uv+ruff+pytest installed, portfolio site live, AsanaBot README refreshed"
git push
```

---

## Sunday — Big block (3.5 hrs)

Block 9 AM – 1 PM (or whenever's right). Four goals.

### 1. PresentAI README refresh (45 min)

Open PresentAI repo. Replace the top:

```markdown
# PresentAI — AI Presentation Generator

A Next.js SaaS that turns project briefs into editable slide decks using Google Gemini. Auth, persistence, drag-and-drop editing, autosave.

![demo](docs/demo.gif)
[Live demo →](https://presentai.example.com)

## Why
Existing "AI slide generators" output static images or require manual layout work. PresentAI generates structured slide data with recursive layouts you can actually edit.

## Architecture
Brief → Gemini structured generation → recursive slide-component renderer → drag-and-drop editor → autosave to Postgres.

## Stack
Next.js 14, Tailwind, Prisma + PostgreSQL, Clerk auth, Zustand state, React DnD, Google Generative AI.

## What I'd change next
- Replace one-shot generation with iterative refinement (user picks 3 of 5 slide variants → regenerate rest).
- Add eval harness for slide quality (LLM-as-judge on structure + relevance vs brief).
- Per-deck cost dashboard.
```

Commit screenshots/gifs.

### 2. Cursor + Claude Code setup (30 min)

**Cursor:**
- Settings → Features → Tab → **off** (re-enable per-session when you want it).
- Keep chat (Cmd-K, Cmd-L) on — chat is fine; silent inline writing is the problem.
- Add to User Rules:
  > "When I ask for code, explain the approach in 3 sentences first, then propose the diff. Don't suggest 5 alternative implementations; pick one. If I say I'm doing a kata, only answer questions — don't write code."

**Claude Code:**
- Install if not already: `npm install -g @anthropic-ai/claude-code`.
- Use it for multi-file edits and refactors; Cursor for fast inline edits.

### 3. Hamel `evals-faq` re-read with your traces open (90 min)

You already read this once ([notes/week-1-saturday-notes.md](../notes/week-1-saturday-notes.md)) and wrote good notes — three named failure modes. This time, re-read with the **deferred questions** from those notes in mind:

- "How do I surface problematic traces for review beyond user feedback?"
- "How often should I re-run error analysis on production?"
- "Should I build automated evaluators for every failure mode I find?"
- "Can I use the same model for both the main task and evaluation?"
- The **Three Gulfs framework** (specification / generalization / comprehension) — read in *A Field Guide to Rapidly Improving AI Products* if not in `evals-faq`.

Open [projects/business-classification-pipeline/data/traces-week-1.jsonl](../projects/business-classification-pipeline/data/traces-week-1.jsonl) side-by-side. For each principle you re-read, write *one* sentence in `notes/week-1-saturday-notes-v2.md` (don't overwrite v1) about how it would change something concrete in leadlens.

### 4. First Public Push tweet + PROGRESS update (30 min)

**Tweet (15 min):**
> "Restarted my AI engineer roadmap with no-AI Python katas + eval-first design on 50 real classifier traces. Week 1 — here's the setup." + screenshot of green pytest output.

Post on X and LinkedIn. This is your first Public Push. Small. Do it anyway.

**PROGRESS update (15 min):**
1. Fill out the Week 1 section of [PROGRESS.md](../PROGRESS.md). Honest hours, what shipped, what slipped, Stuck Box entries.
2. Update [START_HERE.md](../START_HERE.md) — change "Today is in: Month 1, Week 1" to "Month 1, Week 2." Update the link.
3. Open [week-2.md](./week-2.md). Copy the 2–3 main goals to your sticky note.
4. Confidence check: rate yourself 1–5 on the seven dimensions in PROGRESS.md.

---

## Behind if (must-haves to enter Week 2 cleanly)

- Fewer than 4 of 5 no-AI katas done.
- Portfolio site not live at a public URL.
- AsanaBot OR PresentAI README still has the old version (no "where it fails," no screenshot).
- No tweet/X post sent.
- PROGRESS.md Week 1 not updated.

If any of the above, **don't start Week 2 yet** — recover the gap on Mon/Tue of Week 2, then continue.

## Want to go faster?

If you finish everything by Friday with time to spare:
- Read [Anthropic's Prompt Engineering course](https://github.com/anthropics/courses) Lesson 1 + 2 (notebook).
- Sketch leadlens DESIGN.md early — copy the section list from [README.md](./README.md) above and draft 2–3 sections.

Do NOT start trace open-coding early — Week 2 is paced around it.

# Kata learnings — revision cheat sheet

Crisp recall notes. Updated per kata. Bullets, tables, snippets. No narrative.

---

## Kata 01 — Pydantic + parse_company (Mon 2026-05-25)

### Concepts
- `BaseModel` subclass → class attributes with type hints = validated fields
- `Field(ge=0, le=1)` = numeric constraint, raises `ValidationError` if violated
- `Model.model_validate(d)` = canonical dict→instance method (Pydantic v2)
- `ValidationError` lives in `pydantic` (top-level import)

### Required vs optional
| Pattern | Meaning |
|---|---|
| `x: str` | required string |
| `x: str \| None` | required, must be string or explicit None |
| `x: str \| None = None` | optional (missing key OK, becomes None) |
| `x: str \| None = Field(default=None)` | same as above |

**Rule**: `\| None` alone ≠ optional. Need a default to be truly optional.

### Nested validation cascade
```python
class Company(BaseModel):
    signals: list[Signal]   # each Signal validated in turn
```
Bad signal at any index → ValidationError bubbles up from Company.

### Try/except idiom
```python
try:
    return Company.model_validate(data)
except ValidationError as e:
    return Company(name="?", status="uncertain", signals=[])
```
Fallback Company must supply all REQUIRED fields manually.

### File layout (project-style)
- `katas/kata_NN_thing.py` = the code
- `katas/tests/test_kata_NN.py` = pytest tests
- `pyproject.toml` `[tool.pytest.ini_options] pythonpath = ["."]` so test imports work

---

## Kata 02 — async + httpx + asyncio.gather (Sat 2026-05-30)

### Async fetch pattern
```python
async def fetch_one(client, url):
    r = await client.get(url)
    return {"url": url, "status": r.status_code, "size": len(r.content)}

async def fetch_many(urls):
    async with httpx.AsyncClient(timeout=30.0) as client:
        coros = [fetch_one(client, url) for url in urls]
        return await asyncio.gather(*coros)
```

### Concepts
- `async def` makes a **coroutine function** — calling it returns a coroutine object (NOT result)
- `await` runs a coroutine and waits for result
- `asyncio.run(coroutine)` = entry point from sync code, runs event loop
- `async with` = async context manager (httpx.AsyncClient supports it)

### asyncio.gather mechanics
- Input: `*coroutine_objects` (unstarted)
- Behavior: schedules all on event loop, runs concurrently
- Output: `list` of results in input order (even though they finish in random order)
- Raises first exception by default. Use `return_exceptions=True` to collect.

### Sequential vs parallel
Sequential (slow): `for url in urls: r = await fetch_one(client, url)` → N seconds for N URLs
Parallel (fast): `await asyncio.gather(*[fetch_one(client, url) for url in urls])` → ~1 slowest URL

### Other parallel APIs
| Want | API |
|---|---|
| Timeout entire gather | `asyncio.wait_for(asyncio.gather(...), timeout=10)` |
| Collect exceptions | `asyncio.gather(..., return_exceptions=True)` |
| Return as soon as 1 done | `asyncio.wait(coros, return_when=asyncio.FIRST_COMPLETED)` |
| Stream results as they finish | `for c in asyncio.as_completed(coros): r = await c` |

### Gotchas
- `httpx.AsyncClient` default timeout = 5 sec. Slow APIs → ReadTimeout. Set `timeout=30.0`.
- Use lowercase `list[str]`, not `List[str]` (Python 3.9+, no `from typing import List` needed).
- `r.content` = raw bytes. `r.status_code` = int. `r.text` = decoded str.

---

## Kata 03 — context managers + yield + generators (Sat 2026-05-30)

### Two ways to build a context manager

**Decorator-based (short):**
```python
from contextlib import contextmanager
import time

@contextmanager
def timed():
    start = time.perf_counter()
    yield                              # block runs here
    print(f"elapsed: {time.perf_counter()-start:.4f}s")
```

**Class-based (lets you expose state):**
```python
class Timed:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                     # → `as t` binds to this
    def __exit__(self, exc_type, exc_val, tb):
        self.elapsed = time.perf_counter() - self.start
```

### `with` mechanics
- `with X:` calls `X.__enter__()` at start, `X.__exit__()` at end
- `with X as t:` → `t = X.__enter__()` (binds returned value)
- `__exit__` runs even if block raises (built-in try/finally)

### Object lifecycle (3 separate moments)
```python
t = Timed()        # __init__ runs
with t:            # __enter__ runs
    do_stuff()
                    # __exit__ runs
```
`__init__` ≠ `__enter__`. Don't conflate.

### `yield` keyword — generator mechanics
- A function with `yield` becomes a **generator function**
- Calling it returns a **generator object**, no body code runs yet
- `next(g)` runs body up to next `yield`, returns yielded value, pauses
- Next `next(g)` resumes after yield until next yield or end
- `for x in g:` iterates by calling `next` until `StopIteration`

### `@contextmanager` exploits yield as enter/exit boundary
- Code BEFORE `yield` = setup (runs on `__enter__`)
- Code AFTER `yield` = teardown (runs on `__exit__`)
- The yielded value = what `as t` binds to (or None if bare `yield`)

### `yield` ≠ `await`
- `yield` = synchronous generator pause/resume
- `await` = async coroutine pause/resume (event loop driven)
- Different machinery (PEP 492 vs older generators) but conceptually similar suspend/resume

### `return` in a generator
- Does NOT return value to caller
- Raises `StopIteration(value)` — usually invisible
- Use `print` or assign-to-self.attribute instead

### When use which
- Quick debug timing → `@contextmanager` function (terse)
- Need to access elapsed/state after block → class with `__enter__`/`__exit__`
- Multiple resources → both can wrap each other

### Use in leadlens later
Wrap each pipeline stage:
```python
with timed():
    response = anthropic_call(...)
with timed():
    parsed = pydantic_validate(...)
```
Instant per-stage latency. Same pattern feeds Langfuse traces in Month 2.

---

---

## Kata 04 — pytest fixture + parametrize (Sat 2026-05-30)

### Fixture mechanic — name matching

```python
@pytest.fixture
def sample_company():
    return Company(name="Acme", ...)

def test_summarize(sample_company):       # parameter name == fixture name
    result = summarize(sample_company)     # pytest injects the fixture return
```
- pytest sees `sample_company` parameter → calls matching fixture → injects return value
- One source of truth for setup, reused across tests
- No global state, no setup duplication

### Parametrize mechanic — tuple-of-values per run

```python
@pytest.mark.parametrize("name,domain,status,expected", [
    ("Acme", "acme.com", "operating", "operating"),    # run 1
    ("Closed Co", "closed.com", "closed", "closed"),    # run 2
])
def test_summarize_param(name, domain, status, expected):
    ...
```
- First decorator arg = comma-separated **string** of param names
- Second arg = list of tuples, each tuple = one test run
- Values bind to param names by position
- pytest runs test once per tuple → 2 tests shown separately in `-v` output

### Fixture vs parametrize

| Tool | Purpose |
|---|---|
| `@pytest.fixture` | One shared object across multiple tests (DB conn, sample obj) |
| `@pytest.mark.parametrize` | Same test, many inputs (test classifier across 10 JDs) |

Can combine: parametrize values fed into a fixture-built object.

### Fixtures are pytest-only

- Outside tests, equivalent = plain functions / factories / DI
- Production code wires explicitly; tests use fixtures for boilerplate-free setup

### Use in leadlens later

```python
@pytest.mark.parametrize("jd_id", ["jd_001", ..., "jd_010"])
def test_seniority_valid(jd_id):
    out = run_leadlens(load_jd(jd_id))
    assert out.seniority in {"junior", "mid", "senior"}
```
Add 50 more JDs → only add tuples, no test code changes.

---

## Kata 05 — TypeVar + Callable + async retry with backoff (Sat 2026-05-30)

### Type hints for generic async callbacks

```python
from collections.abc import Callable, Awaitable
from typing import TypeVar

T = TypeVar("T")

async def with_retry(fn: Callable[[], Awaitable[T]], ...) -> T:
    ...
```
- `Callable[[], Awaitable[T]]` reads as: callable with no args, returns awaitable that resolves to T
- `TypeVar("T")` = generic placeholder — preserves return type for caller
- If caller passes `Callable[[], Awaitable[str]]`, return type is `str`

### Retry-with-exponential-backoff pattern

```python
for i in range(attempts):
    try:
        return await fn()
    except Exception as e:
        if i == attempts - 1:
            raise           # last attempt → re-raise, surface to caller
        await asyncio.sleep(backoff)
        backoff *= 2        # exponential: 0.5 → 1.0 → 2.0 → 4.0
```

### `raise` keyword 3 forms

| Form | Meaning |
|---|---|
| `raise ExceptionType("msg")` | Create + raise new exception |
| `raise` (bare, in except block) | Re-raise current exception, preserves traceback |
| `raise X from Y` | Wrap one exception in another, both visible |

### Key gotchas

- `range(attempts)` = 0..attempts-1 → last attempt check is `i == attempts - 1`, NOT `i == attempts`
- Forgetting `return await fn()` → function returns `None` on success silently
- Bare `raise` only valid inside `except` block — outside, raises `RuntimeError: No active exception to re-raise`

### Use in leadlens later

Anthropic API, Tavily, GitHub API — all flaky. Wrap each call:
```python
result = await with_retry(lambda: anthropic.messages.create(...), attempts=3, backoff=1.0)
```
3 attempts, 1s → 2s → 4s backoff. Failed all → exception bubbles up cleanly.

---

## How to revise

Say "revise katas" → I re-read this file with you, quiz pattern recognition on key snippets. ~10 min refresher.

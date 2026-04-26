# Day 0 — Learning System

## Goal for today

Start learning like an engineer, not like someone randomly watching tutorials.

The goal is to understand how to think about a program as a small system with clear input, processing, output, failure handling, evidence, logs, and tests.

## Core idea

A useful automation system should have:

1. Input
2. Processing
3. Output
4. Failure handling
5. Evidence or logs
6. Test cases

This is the foundation for the kind of AI automation systems I want to build.

## Why this matters

A weak script only gives an answer.

A better system explains:

- what input it received
- what checks it ran
- what evidence it used
- what failed
- why it returned the final status

For example, a company classifier should not just say `Active` or `Inactive`.
It should return structured evidence and handle unknown cases safely.

## First mental model

```text
CSV row / company input
   ↓
Python service
   ↓
Search API + scraping + LLM
   ↓
Evidence + classification
   ↓
Clean JSON output
```

## First tiny Python exercise

```python
def classify_company(company_name: str, domain: str) -> dict:
    if not company_name:
        return {
            "status": "error",
            "reason": "company_name is required",
            "evidence": []
        }

    if not domain:
        return {
            "status": "unknown",
            "reason": "domain is missing",
            "evidence": []
        }

    return {
        "status": "needs_research",
        "reason": "company has basic input but no checks have been run yet",
        "evidence": [
            {
                "source": "input",
                "value": {
                    "company_name": company_name,
                    "domain": domain
                }
            }
        ]
    }


result = classify_company("Test Winery", "testwinery.com")
print(result)
```

## Test cases to try

### Good input

```python
classify_company("Test Winery", "testwinery.com")
```

Expected status:

```text
needs_research
```

### Missing domain

```python
classify_company("Test Winery", "")
```

Expected status:

```text
unknown
```

### Missing company name

```python
classify_company("", "testwinery.com")
```

Expected status:

```text
error
```

## What I learned

Before using AI, APIs, scraping, or databases, define the shape of the input and output.

If input and output are messy, the whole system becomes messy.

## Questions I still have

- What exactly is a Python function?
- What is a dictionary?
- What does `str` mean in `company_name: str`?
- Why do we return structured JSON-like data instead of plain text?

## Next lesson

Day 1 — Python functions, types, dictionaries, and structured outputs.

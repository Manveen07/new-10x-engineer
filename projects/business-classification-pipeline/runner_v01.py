"""leadlens v0.1 runner — classify 1 JD via Gemini + Instructor.

Usage:
    uv run python runner_v01.py 0           # classify JD at idx 0
    uv run python runner_v01.py 0 --all     # classify all JDs in both files
"""

import argparse
import json
import os
import time
from pathlib import Path

import instructor
from dotenv import load_dotenv
from google import genai

from leadlens_v01 import JobPosting

load_dotenv()

JDS_PATHS = [Path("data/golden-jds.jsonl")]
OUTPUTS_PATH = Path("data/jd-outputs.jsonl")
METRICS_PATH = Path("data/jd-metrics.jsonl")
MODEL = "gemini-2.5-flash"

# Gemini 2.5 Flash pricing (USD per 1M tokens, 2026)
PRICE_INPUT_PER_M = 0.30
PRICE_OUTPUT_PER_M = 2.50


SYSTEM_PROMPT = """You are a job-description classifier helping a junior AI engineer evaluate
fit for remote roles. Read the JD carefully. Quote specific evidence from the description
before assigning any category. If a field is unclear from the description, use the 'unclear'
literal — do NOT guess.

Output a JobPosting object with all fields populated. Confidence_reasoning must quote
specific phrases from the description as evidence for your category choices."""


def build_user_prompt(jd: dict) -> str:
    return f"""Classify this job posting:

ID: {jd['id']}
Title: {jd['title']}
Company: {jd['company']}
URL: {jd['url']}
Location field: {jd.get('location', 'not specified')}

Description:
{jd['description']}
"""


def load_jds() -> list[dict]:
    jds = []
    for p in JDS_PATHS:
        if p.exists():
            jds.extend(
                json.loads(line)
                for line in p.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
    return jds


def make_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing — check .env file")
    return instructor.from_genai(genai.Client(api_key=api_key))


def classify(client, jd: dict) -> tuple[JobPosting, dict]:
    user_prompt = build_user_prompt(jd)
    t0 = time.perf_counter()
    result, raw = client.chat.completions.create_with_completion(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_model=JobPosting,
    )
    latency_ms = (time.perf_counter() - t0) * 1000
    result.id = jd["id"]
    result.title = jd["title"]
    result.company = jd["company"]
    result.url = jd["url"]

    usage = getattr(raw, "usage_metadata", None) or getattr(raw, "usage", None)
    in_tok = (
        getattr(usage, "prompt_token_count", None)
        or getattr(usage, "input_tokens", 0)
        or 0
    )
    out_tok = (
        getattr(usage, "candidates_token_count", None)
        or getattr(usage, "output_tokens", 0)
        or 0
    )
    cost_usd = (in_tok / 1e6) * PRICE_INPUT_PER_M + (out_tok / 1e6) * PRICE_OUTPUT_PER_M

    metrics = {
        "id": jd["id"],
        "latency_ms": round(latency_ms, 1),
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cost_usd": round(cost_usd, 6),
    }
    return result, metrics


def save_output(posting: JobPosting) -> None:
    OUTPUTS_PATH.parent.mkdir(exist_ok=True)
    existing = {}
    if OUTPUTS_PATH.exists():
        existing = {
            json.loads(line)["id"]: json.loads(line)
            for line in OUTPUTS_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    existing[posting.id] = posting.model_dump()
    OUTPUTS_PATH.write_text(
        "\n".join(
            json.dumps(v) for v in sorted(existing.values(), key=lambda x: x["id"])
        ),
        encoding="utf-8",
    )


def save_metrics(metrics: dict) -> None:
    existing = {}
    if METRICS_PATH.exists():
        existing = {
            json.loads(line)["id"]: json.loads(line)
            for line in METRICS_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    existing[metrics["id"]] = metrics
    METRICS_PATH.write_text(
        "\n".join(
            json.dumps(v) for v in sorted(existing.values(), key=lambda x: x["id"])
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "idx", type=int, nargs="?", default=0, help="Index of JD to classify"
    )
    parser.add_argument(
        "--all", action="store_true", help="Classify all JDs in both files"
    )
    args = parser.parse_args()

    client = make_client()
    jds = load_jds()
    targets = jds if args.all else [jds[args.idx]]

    totals = {
        "latency_ms": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0,
        "n": 0,
    }

    for jd in targets:
        print(f"\n--- {jd['id']} {jd['company']} — {jd['title']} ---")
        try:
            result, metrics = classify(client, jd)
            print(json.dumps(result.model_dump(), indent=2))
            print(
                f"[metrics] latency={metrics['latency_ms']}ms  in={metrics['input_tokens']}tok  out={metrics['output_tokens']}tok  cost=${metrics['cost_usd']}"
            )
            save_output(result)
            save_metrics(metrics)
            for k in ("latency_ms", "input_tokens", "output_tokens", "cost_usd"):
                totals[k] += metrics[k]
            totals["n"] += 1
        except Exception as e:
            print(f"FAILED: {type(e).__name__}: {e}")

    if totals["n"]:
        n = totals["n"]
        print(f"\n=== Aggregate over {n} JDs ===")
        print(f"  avg latency: {totals['latency_ms']/n:.0f}ms")
        print(f"  total cost:  ${totals['cost_usd']:.4f}")
        print(f"  avg cost/JD: ${totals['cost_usd']/n:.5f}")
        print(
            f"  total tokens in/out: {totals['input_tokens']}/{totals['output_tokens']}"
        )


if __name__ == "__main__":
    main()

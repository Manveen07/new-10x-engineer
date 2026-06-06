"""leadlens v0.1 runner — classify 1 JD via Gemini + Instructor.

Usage:
    uv run python runner_v01.py 0           # classify jd_001 (idx 0)
    uv run python runner_v01.py 0 --all     # classify all 10
"""

import argparse
import json
import os
from pathlib import Path

import instructor
from dotenv import load_dotenv
from google import genai

from leadlens_v01 import JobPosting

load_dotenv()

JDS_PATH = Path("data/jds-v0.jsonl")
OUTPUTS_PATH = Path("data/jd-outputs.jsonl")
MODEL = "gemini-2.5-flash"


# ---------- PROMPT (Manveen writes this — it's the eval spec by another name) ----------

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


# ---------- plumbing ----------


def load_jds() -> list[dict]:
    return [
        json.loads(line)
        for line in JDS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def make_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing — check .env file")
    return instructor.from_genai(genai.Client(api_key=api_key))


def classify(client, jd: dict) -> JobPosting:
    user_prompt = build_user_prompt(jd)
    result = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_model=JobPosting,
    )
    # echo input fields so output has full context
    result.id = jd["id"]
    result.title = jd["title"]
    result.company = jd["company"]
    result.url = jd["url"]
    return result


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "idx", type=int, nargs="?", default=0, help="Index of JD to classify (0-9)"
    )
    parser.add_argument("--all", action="store_true", help="Classify all 10 JDs")
    args = parser.parse_args()

    client = make_client()
    jds = load_jds()

    targets = jds if args.all else [jds[args.idx]]

    for jd in targets:
        print(f"\n--- {jd['id']} {jd['company']} — {jd['title']} ---")
        try:
            result = classify(client, jd)
            print(json.dumps(result.model_dump(), indent=2))
            save_output(result)
        except Exception as e:
            print(f"FAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()

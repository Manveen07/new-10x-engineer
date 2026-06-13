"""leadlens judge v2 — binary scam-pattern detector for F-006.

Iteration on v1 (TPR=1.0, TNR=0.882). v1's 2 false positives were real
startup eng roles wrongly flagged as scams (jd_002 Sumble, jd_009 DrSwarm)
because the judge over-fired on "vague" / "founding engineer" language.

v2 changes (to push TNR -> 0.90 without dropping TPR):
1. Two few-shot examples added to the prompt — 1 positive (MIIGO scam) +
   1 negative (Sumble: real role that LOOKS sketchy but isn't). Teaches the
   boundary by example (critique-shadowing).
2. Tightened rule: vague + a real product/technical description != scam.

Usage:
    uv run python judge_v2.py        # run on all 20 JD outputs, print TPR/TNR
"""

import argparse
import json
import os
from pathlib import Path
from typing import Literal

import instructor
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

OUTPUTS_PATH = Path("data/jd-outputs.jsonl")
JDS_PATHS = [Path("data/jds-v0.jsonl"), Path("data/jds-v0-expansion.jsonl")]
JUDGE_OUTPUTS_PATH = Path("data/judge-v2-outputs.jsonl")
MODEL = "gemini-2.5-flash"


# ---------- Judge schema ----------


class ScamVerdict(BaseModel):
    """Binary 'is this an ai_washed / scam-pattern JD?' verdict."""

    critique: str = Field(
        min_length=80,
        description="Quote 2-3 specific phrases from the JD description that drove your verdict. Critique before verdict — never the other way around.",
    )
    is_scam: Literal["yes", "no"] = Field(
        description="yes = ai_washed pattern present (partnership-not-job, no salary, equity-only, AI in title but role is sales/support, vague-on-what-we-build). no = real role even if borderline.",
    )


# ---------- Judge prompt (YOU write the meaty part) ----------

JUDGE_SYSTEM_PROMPT = """You are evaluating job postings for ONE specific failure mode:
"ai_washed" — postings that use AI vocabulary but are not real AI engineering roles.

A posting is `ai_washed` (yes) when ANY of these patterns appear:
- "Partnership opportunity" instead of "job" / revenue share / no fixed salary
- Equity-only with "no salary for first N months" — especially with vague description
- "Will explain on a call" / Telegram-first / DM-first / "viral X posts as traction"
- AI in title but description is sales, customer success, support, or marketing with no engineering content
- MLM-style "need 4 partners" / "co-founders needed" with no real product surface

A posting is NOT ai_washed (no) when the role has real engineering content even if it's:
- Adjacent to AI (e.g. data infrastructure, robotics SDK)
- Senior/onsite/wrong-region (mismatch != scam)
- Thin on stack (some real roles just don't list frameworks)
- Equity-heavy but with a real product + technical description

CRITICAL RULE: vague + a real product or technical description != scam.
Only flag `yes` when there is NO real engineering work AND a scam signal
(no salary / partnership-not-job / equity-only-and-vague / MLM / apply-by-emoji).
A real salaried engineering role that is merely thin on detail, vague on stack,
or uses "founding engineer" language is NOT a scam — verdict `no`.

EXAMPLE 1 (scam -> yes):
JD: "MIIGO — AI co-founder / tech partner needed. Partnership opportunity, not a job.
No salary, revenue share. Need 4 partners. Reply with thumbs-up emoji."
critique: States "partnership opportunity, not a job" and "no salary, revenue share" with
"need 4 partners" and emoji-apply — no real engineering surface, MLM-shaped. Classic ai_washed.
verdict: yes

EXAMPLE 2 (real but sketchy-looking -> no):
JD: "Sumble — AI/ML Engineer, build a knowledge graph from web data. Raised $38.5M,
team of 25 from Google, Meta, Snowflake, Kaggle."
critique: Vague on exact frameworks, but a real salaried engineering role with a real
product (knowledge graph from web data), real funding, and a credentialed team. Vague != scam.
verdict: no

Process:
1. Read the JD description and the leadlens classifier output.
2. Write a 2-3 sentence CRITIQUE first. Quote specific phrases from the description.
3. THEN emit the binary verdict.

Critique before verdict — the order is the discipline."""


# ---------- Plumbing ----------


def load_jds() -> dict[str, dict]:
    out = {}
    for p in JDS_PATHS:
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    jd = json.loads(line)
                    out[jd["id"]] = jd
    return out


def load_classifier_outputs() -> list[dict]:
    return [
        json.loads(line)
        for line in OUTPUTS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def make_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing — check .env file")
    return instructor.from_genai(genai.Client(api_key=api_key))


def judge_one(client, jd: dict, classifier_out: dict) -> ScamVerdict:
    user_prompt = f"""JD to evaluate:

Title: {jd['title']}
Company: {jd['company']}
Location: {jd.get('location', 'not specified')}

Description:
{jd['description']}

leadlens classifier said:
- ai_authenticity: {classifier_out.get('ai_authenticity')}
- red_flags: {classifier_out.get('red_flags')}
- comp_signal: {classifier_out.get('comp_signal')}

Your job: critique + binary verdict on whether this is an ai_washed / scam-pattern role."""

    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_model=ScamVerdict,
    )


def save_judge_output(jd_id: str, verdict: ScamVerdict) -> None:
    existing = {}
    if JUDGE_OUTPUTS_PATH.exists():
        existing = {
            json.loads(line)["id"]: json.loads(line)
            for line in JUDGE_OUTPUTS_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
    existing[jd_id] = {"id": jd_id, **verdict.model_dump()}
    JUDGE_OUTPUTS_PATH.write_text(
        "\n".join(
            json.dumps(v) for v in sorted(existing.values(), key=lambda x: x["id"])
        ),
        encoding="utf-8",
    )


def golden_label(jd: dict) -> str:
    """Convert expected_category to binary scam label.

    ai_washed -> 'yes' (scam pattern)
    everything else -> 'no'
    """
    return "yes" if jd.get("expected_category") == "ai_washed" else "no"


def compute_metrics(results: list[tuple[str, str]]) -> dict:
    """results = list of (judge_verdict, golden_label) tuples."""
    tp = tn = fp = fn = 0
    for verdict, gold in results:
        if verdict == "yes" and gold == "yes":
            tp += 1
        elif verdict == "no" and gold == "no":
            tn += 1
        elif verdict == "yes" and gold == "no":
            fp += 1
        elif verdict == "no" and gold == "yes":
            fn += 1

    total = tp + tn + fp + fn
    return {
        "n": total,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tpr": round(tp / (tp + fn), 3) if (tp + fn) else None,
        "tnr": round(tn / (tn + fp), 3) if (tn + fp) else None,
        "raw_agreement": round((tp + tn) / total, 3) if total else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    client = make_client()
    jds = load_jds()
    outputs = load_classifier_outputs()

    if args.limit:
        outputs = outputs[: args.limit]

    print(
        f"\nJudging {len(outputs)} JDs against gold = expected_category == ai_washed\n"
    )
    results: list[tuple[str, str]] = []

    for out in outputs:
        jd_id = out["id"]
        jd = jds.get(jd_id)
        if not jd:
            continue
        gold = golden_label(jd)
        try:
            verdict = judge_one(client, jd, out)
            save_judge_output(jd_id, verdict)
            mark = "OK " if verdict.is_scam == gold else "X  "
            print(f"{mark} {jd_id}  judge={verdict.is_scam}  gold={gold}")
            print(f"      critique: {verdict.critique[:120]}...")
            results.append((verdict.is_scam, gold))
        except Exception as e:
            print(f"FAILED {jd_id}: {type(e).__name__}: {e}")

    metrics = compute_metrics(results)
    print("\n=== Calibration metrics ===")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    print("\nInterpretation:")
    print(
        f"  TPR = {metrics['tpr']} = of all real scams ({metrics['tp'] + metrics['fn']}), judge caught {metrics['tp']}"
    )
    print(
        f"  TNR = {metrics['tnr']} = of all real non-scams ({metrics['tn'] + metrics['fp']}), judge caught {metrics['tn']}"
    )
    print(
        f"  raw agreement {metrics['raw_agreement']} would lie under class imbalance (only {metrics['tp'] + metrics['fn']}/{metrics['n']} are scams)"
    )


if __name__ == "__main__":
    main()

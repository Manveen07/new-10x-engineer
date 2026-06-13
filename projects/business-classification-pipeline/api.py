"""leadlens API — HTTP door onto the classifier + scam judge.

Same logic as runner_v01 / judge_v2 (the script versions). The only new
thing is the *interface*: anyone can POST a JD and get the structured
verdict back, instead of editing a file and running a script.

Production note: the Gemini client is built ONCE at startup (module load),
not per request. Re-creating it on every call would add latency + waste
connections — load-once is the deploy-shaped pattern.

Run locally:
    uv run uvicorn api:app --reload
Then open http://127.0.0.1:8000/docs  (FastAPI's auto Swagger UI)
"""

from pydantic import BaseModel
from fastapi import FastAPI

from leadlens_v01 import JobPosting
from judge_v2 import ScamVerdict, judge_one
from runner_v01 import classify, make_client

app = FastAPI(title="leadlens", description="AI job-posting classifier + scam judge")

# Build the model client ONCE at startup, reused across requests.
_client = make_client()


# ---------- request bodies ----------


class ClassifyRequest(BaseModel):
    title: str
    company: str
    description: str
    url: str = ""
    location: str = "not specified"


class JudgeRequest(ClassifyRequest):
    # the classifier output to judge (the fields the judge actually reads)
    ai_authenticity: str
    red_flags: list[str] = []
    comp_signal: str | None = None


# ---------- endpoints ----------


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "leadlens"}


@app.post("/classify", response_model=JobPosting)
def classify_endpoint(req: ClassifyRequest) -> JobPosting:
    jd = {
        "id": "api",
        "title": req.title,
        "company": req.company,
        "url": req.url,
        "location": req.location,
        "description": req.description,
    }
    posting, _metrics = classify(_client, jd)
    return posting


@app.post("/judge", response_model=ScamVerdict)
def judge_endpoint(req: JudgeRequest) -> ScamVerdict:
    jd = {
        "title": req.title,
        "company": req.company,
        "location": req.location,
        "description": req.description,
    }
    classifier_out = {
        "ai_authenticity": req.ai_authenticity,
        "red_flags": req.red_flags,
        "comp_signal": req.comp_signal,
    }
    return judge_one(_client, jd, classifier_out)

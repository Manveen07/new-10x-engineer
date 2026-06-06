from pydantic import Field
import os
from pydantic import BaseModel
from typing import Literal
import instructor
from google import genai
from dotenv import load_dotenv

load_dotenv()


class Signal(BaseModel):
    name: str
    evidence: str
    confidence: float


class Company(BaseModel):
    name: str
    domain: str | None = Field(
        default=None, description="null if the company has no website"
    )
    status: Literal["operating", "closed", "uncertain"]
    signals: list[Signal]


client = instructor.from_genai(genai.Client(api_key=os.environ["GEMINI_API_KEY"]))

text = """
Acme Wines is a small local winery. They don't have a website.
"""

result = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_model=Company,
    messages=[{"role": "user", "content": f"Extract a Company record from:\n{text}"}],
)
print(result.model_dump_json(indent=2))

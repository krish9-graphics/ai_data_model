# server.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

class ProblemRequest(BaseModel):
    title: str
    statement: str
    constraints: str = ""
    examples: list = []

def make_prompt(problem):
    return f"""
Problem: {problem['title']}
Statement: {problem['statement']}
Constraints: {problem.get('constraints','')}
Examples: {problem.get('examples',[])}

Task: 1) Restate the problem in one sentence.
2) Suggest the right data structure(s) and time/space complexity.
3) Provide step-by-step plan (numbered).
4) Provide pseudocode.
5) Provide Python solution.
Return as JSON with keys: restatement, structures, steps, pseudocode, code
"""

@app.post("/solve")
async def solve(req: ProblemRequest):
    prompt = make_prompt(req.dict())
    # Example for OpenAI HTTP API (adjust for your provider)
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_KEY}"},
        json={
            "model":"gpt-4o-mini", "messages":[{"role":"user","content":prompt}],
            "max_tokens":1000
        }
    )
    return resp.json()

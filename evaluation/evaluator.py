from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from pathlib import Path

_here = Path(__file__).resolve().parent
load_dotenv(_here.parent / ".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are an evaluation system.

Evaluate the quality of a generated answer.

Rules:
- Only evaluate based on provided facts
- Do NOT add new knowledge

Return JSON:
{
  "correctness": score (0-10),
  "completeness": score (0-10),
  "structure": score (0-10),
  "faithfulness": score (0-10),
  "issues": [...]
}
"""


def evaluate_output(facts, draft):
    prompt = f"""
FACTS:
{facts}

DRAFT:
{draft}

Evaluate the draft.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    return json.loads(content)

def evaluate_with_metrics(state, eval_result):
    return {
        **eval_result,
        "llm_calls": state.get("llm_calls", 0),
        "iterations": state.get("iteration", 0)
    }
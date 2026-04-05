from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a strict reviewer.

Your job is to evaluate a draft based ONLY on provided facts.

Rules:
- DO NOT introduce new facts
- DO NOT rewrite the answer
- Only critique
- Be strict and precise

Check for:
1. Missing facts
2. Incorrect statements
3. Lack of clarity
4. Poor structure

Return ONLY valid JSON:

{
  "issues": [...],
  "missing_points": [...],
  "is_approved": true/false
}
"""


def critique(draft, facts):
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

    try:
        return json.loads(content)
    except:
        raise ValueError(f"Invalid JSON from Editor: {content}")


class EditorAgent:
    def __init__(self):
        pass

    def run(self, writer_output):
        draft = writer_output["draft"]
        facts = writer_output["facts_used"]

        result = critique(draft, facts)

        return result
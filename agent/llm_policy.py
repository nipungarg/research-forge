import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a decision-making agent.

Your job is to decide the NEXT BEST ACTION.

You must ONLY return valid JSON.

Available actions:
1. search_documents(query: str)
2. summarize_notes(facts: list)
3. stop()

Rules:
- If no facts → search
- If enough facts → summarize
- If summary exists → stop
- NEVER hallucinate tools
- ALWAYS return JSON

Output format:
{
  "action": "<tool_name or stop>",
  "input": { ... }
}
"""


def llm_decision(memory, query):
    prompt = f"""
User Query:
{query}

Current Memory:
{json.dumps(memory.to_dict(), indent=2)}

Decide the next action.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # fast + cheap (can upgrade later)
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        decision = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON from LLM: {content}")

    return decision
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a professional technical writer.

Your job is to generate or improve a structured response using facts AND feedback.

STRICT RULES:
- Use ONLY the provided facts
- DO NOT add new information
- Address ALL feedback issues
- Include missing points explicitly
- Improve clarity and structure

Structure:
1. Overview
2. Key Points
3. Risks / Limitations
4. Conclusion
"""


def generate_draft(facts, feedback=None):
    feedback_text = ""

    if feedback:
        feedback_text = f"""
FEEDBACK TO ADDRESS:
Issues:
{feedback.get("issues", [])}

Missing Points:
{feedback.get("missing_points", [])}
"""

    prompt = f"""
FACTS:
{facts}

{feedback_text}

Generate an improved structured response.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def validate_output(draft, facts):
    missing = [f for f in facts if f not in draft]
    if missing:
        print("⚠️ Warning: Some facts not used in draft:")
        for f in missing:
            print(f"  - {f[:120]}{'…' if len(f) > 120 else ''}")

    return draft


class WriterAgent:
    def __init__(self):
        pass

    def run(self, researcher_output, feedback=None):
        facts = researcher_output["facts"]

        if not facts:
            return {
                "draft": "Insufficient information to generate a response.",
                "facts_used": []
            }

        draft = generate_draft(facts, feedback)
        draft = validate_output(draft, facts)

        return {
            "draft": draft,
            "facts_used": facts
        }
from typing import List


def summarize_notes(facts: List[str]) -> str:
    """
    Combine collected facts into a structured summary.
    """
    if not facts:
        return "No sufficient information collected."

    summary = "Summary of Findings:\n"
    for i, fact in enumerate(facts, 1):
        summary += f"{i}. {fact}\n"

    return summary
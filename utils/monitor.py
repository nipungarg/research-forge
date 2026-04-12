def detect_issues(state):
    issues = []

    if state.get("iteration", 0) > 3:
        issues.append("Too many iterations")

    if not state.get("facts"):
        issues.append("No facts retrieved")

    if state.get("llm_calls", 0) > 10:
        issues.append("High LLM cost")

    if issues:
        print("\n⚠️ SYSTEM ALERTS:")
        for issue in issues:
            print(f"- {issue}")

    return issues
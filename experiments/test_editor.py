from multi_agent.editor import EditorAgent


def test_editor():
    editor = EditorAgent()

    writer_output = {
        "draft": """
        AI improves healthcare significantly.
        It reduces costs and increases efficiency.
        """,
        "facts_used": [
            "AI improves diagnostic accuracy",
            "AI reduces costs in hospitals",
            "AI systems may introduce bias"
        ]
    }

    result = editor.run(writer_output)

    print("\n=== EDITOR OUTPUT ===\n")
    print(result)


if __name__ == "__main__":
    test_editor()
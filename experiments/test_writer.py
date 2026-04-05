from multi_agent.writer import WriterAgent


def test_writer():
    writer = WriterAgent()

    researcher_output = {
        "facts": [
            "AI improves diagnostic accuracy",
            "AI reduces costs in hospitals",
            "AI systems may introduce bias"
        ],
        "sources": []
    }

    result = writer.run(researcher_output)

    print("\n=== DRAFT ===\n")
    print(result["draft"])


if __name__ == "__main__":
    test_writer()
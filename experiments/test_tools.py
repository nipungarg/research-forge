from tools.registry import ToolRegistry


def test_tools():
    registry = ToolRegistry()

    print("Available tools:", registry.list_tools())

    # Test search
    results = registry.execute(
        "search_documents",
        query="AI"
    )
    print("\nSearch Results:")
    for r in results:
        print(r)

    # Test summarize
    summary = registry.execute(
        "summarize_notes",
        facts=["AI improves accuracy", "AI reduces costs"]
    )
    print("\nSummary:")
    print(summary)


if __name__ == "__main__":
    test_tools()
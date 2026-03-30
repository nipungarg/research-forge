from agent.agent import ResearchAgent


TEST_CASES = [
    {
        "name": "Simple Question",
        "query": "Impact of AI in healthcare"
    },
    {
        "name": "Ambiguous Question",
        "query": "Is AI good?"
    },
    {
        "name": "Insufficient Data",
        "query": "Quantum effects of AI consciousness"
    }
]


def run_tests():
    for test in TEST_CASES:
        print("\n==============================")
        print(f"TEST: {test['name']}")
        print("==============================")

        agent = ResearchAgent(max_steps=5)
        result = agent.run(test["query"])

        print("\nFinal Summary:")
        print(result.metadata.get("summary"))

        print("\nFacts Collected:", len(result.facts))
        print("Actions Taken:", result.actions_taken)


if __name__ == "__main__":
    run_tests()
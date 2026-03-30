from agent.agent import ResearchAgent


def test_agent():
    agent = ResearchAgent(max_steps=5)

    result = agent.run("Impact of AI in healthcare")

    print("\nFinal Summary:")
    print(result.metadata.get("summary"))


if __name__ == "__main__":
    test_agent()
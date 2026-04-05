from multi_agent.researcher import ResearcherAgent


def test_researcher():
    agent = ResearcherAgent(max_steps=5)

    result = agent.run("Impact of AI in healthcare")

    print("\nFinal Output:")
    print(result)


if __name__ == "__main__":
    test_researcher()
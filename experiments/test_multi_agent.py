from multi_agent.researcher import ResearcherAgent
from multi_agent.orchestrator import Orchestrator


def test_system():
    researcher = ResearcherAgent()
    orchestrator = Orchestrator()

    research_output = researcher.run("Impact of AI in healthcare")

    final_output = orchestrator.run(research_output)

    print("\n=== FINAL ANSWER ===\n")
    print(final_output["draft"])


if __name__ == "__main__":
    test_system()
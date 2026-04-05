from agent.agent import ResearchAgent as SingleAgent
from multi_agent.researcher import ResearcherAgent
from multi_agent.orchestrator import Orchestrator


def compare():
    query = "Impact of AI in healthcare"

    print("\n=== SINGLE AGENT ===")
    single = SingleAgent(max_steps=5)
    single_result = single.run(query)

    print("\n=== MULTI AGENT ===")
    researcher = ResearcherAgent()
    orchestrator = Orchestrator()

    research_output = researcher.run(query)
    multi_result = orchestrator.run(research_output)

    print("\n=== COMPARISON ===")
    print("Single Summary:\n", single_result.metadata.get("summary"))
    print("\nMulti-Agent Output:\n", multi_result["draft"])


if __name__ == "__main__":
    compare()
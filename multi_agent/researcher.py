from tools.registry import ToolRegistry
from multi_agent.researcher_memory import ResearcherMemory


class ResearcherAgent:
    def __init__(self, max_steps=5):
        self.memory = ResearcherMemory()
        self.tools = ToolRegistry()
        self.max_steps = max_steps

    def decide(self, query):
        """
        Simple controlled policy (LLM optional later)
        """

        # Stop conditions
        if self.memory.is_sufficient():
            return {"action": "stop"}

        if self.memory.is_stuck():
            return {"action": "stop"}

        return {
            "action": "search_documents",
            "input": {"query": query}
        }

    def act(self, decision, query):
        action = decision["action"]

        if action == "stop":
            return "STOP"

        if action == "search_documents":
            result = self.tools.execute(
                "search_documents",
                query=query
            )
            return result

    def update_memory(self, query, results):
        self.memory.add_query(query)

        for doc in results:
            self.memory.add_fact(doc["content"])
            self.memory.add_source({
                "id": doc["id"],
                "title": doc["title"]
            })

        self.memory.increment_step()

    def run(self, query):
        print(f"\n=== Researcher started for: {query} ===")

        for step in range(self.max_steps):
            print(f"\n--- Step {step + 1} ---")

            decision = self.decide(query)
            print("Decision:", decision)

            result = self.act(decision, query)

            if result == "STOP":
                print("Researcher stopping.")
                break

            print("Results:", result)

            self.update_memory(query, result)

            print("Facts:", self.memory.facts)
            print("Queries:", self.memory.search_queries)

        print("\n=== Research Complete ===")
        print(self.memory.to_dict())

        return self.memory.to_dict()
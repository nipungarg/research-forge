from memory.memory import AgentMemory
from tools.registry import ToolRegistry
from agent.llm_policy import llm_decision


class ResearchAgent:
    def __init__(self, max_steps=5):
        self.memory = AgentMemory()
        self.tools = ToolRegistry()
        self.max_steps = max_steps

    # -------------------------
    # OBSERVE
    # -------------------------
    def observe(self, query):
        return {
            "query": query,
            "memory": self.memory.to_dict()
        }

    # -------------------------
    # THINK (LLM)
    # -------------------------
    def think(self, observation):
        decision = llm_decision(self.memory, observation["query"])

        # 🔒 Guardrail: Validate decision
        if "action" not in decision:
            raise ValueError("LLM did not return action")

        if decision["action"] != "stop" and "input" not in decision:
            raise ValueError("LLM did not return input")

        return decision

    # -------------------------
    # ACT
    # -------------------------
    def act(self, decision):
        action = decision["action"]

        if action == "stop":
            self.memory.mark_complete()
            return "STOP"

        if action not in self.tools.list_tools():
            raise ValueError(f"Invalid tool requested: {action}")

        result = self.tools.execute(action, **decision["input"])

        return action, result

    # -------------------------
    # MEMORY UPDATE
    # -------------------------
    def update_memory(self, action, result):
        if action == "search_documents":
            for doc in result:
                self.memory.add_fact(doc["content"])
                self.memory.add_source({
                    "id": doc["id"],
                    "title": doc["title"]
                })

        elif action == "summarize_notes":
            self.memory.metadata["summary"] = result
            self.memory.metadata["summary_generated"] = True

        self.memory.add_action(action)

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self, query):
        print(f"\n=== Starting Agent for Query: {query} ===\n")

        for step in range(self.max_steps):
            print(f"\n--- Step {step + 1} ---")

            observation = self.observe(query)
            print("Observation:", observation["memory"]["metadata"])

            decision = self.think(observation)
            print("Decision:", decision)

            result = self.act(decision)

            if result == "STOP":
                print("Agent decided to STOP.")
                break

            action, output = result

            print(f"Action: {action}")
            print(f"Output: {output}")

            self.update_memory(action, output)

            print("Memory Facts:", self.memory.facts)
            print("Actions Taken:", self.memory.actions_taken)

        print("\n=== FINAL MEMORY ===")
        self.memory.pretty_print()

        return self.memory
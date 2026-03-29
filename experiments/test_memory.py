from memory.memory import AgentMemory


def test_memory():
    memory = AgentMemory()

    # Add data
    memory.add_fact("AI improves diagnostic accuracy")
    memory.add_source({"title": "Nature Study", "year": 2022})
    memory.add_action("search: AI healthcare")
    memory.add_open_question("What are risks?")

    # Save
    memory.save("memory_test.json")

    # Load
    loaded_memory = AgentMemory.load("memory_test.json")

    # Print
    loaded_memory.pretty_print()


if __name__ == "__main__":
    test_memory()
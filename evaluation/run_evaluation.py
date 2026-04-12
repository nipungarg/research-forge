from evaluation.evaluator import evaluate_output, evaluate_with_metrics
from multi_agent.researcher import ResearcherAgent
from agent.agent import ResearchAgent as SingleAgent

from langgraph_app.main import build_graph


def run():
    query = "Impact of AI in healthcare"

    # ------------------------
    # SINGLE AGENT (Baseline)
    # ------------------------
    single = SingleAgent(max_steps=5)
    single_result = single.run(query)

    single_draft = single_result.metadata.get("summary")
    facts = single_result.facts

    single_eval = evaluate_output(facts, single_draft)

    single_eval = evaluate_with_metrics(
        getattr(single_result, "metadata", {}),
        single_eval
    )

    # ------------------------
    # LANGGRAPH SYSTEM
    # ------------------------
    app = build_graph()

    result = app.invoke({
        "query": query,
        "facts": [],
        "sources": [],
        "draft": "",
        "feedback": {},
        "iteration": 0,
        "llm_calls": 0
    })

    multi_result = {
        "draft": result["draft"],
        "state": result
    }

    multi_draft = multi_result["draft"]
    facts = result["facts"]

    multi_eval = evaluate_output(facts, multi_draft)

    multi_eval = evaluate_with_metrics(
        multi_result["state"],
        multi_eval
    )

    # ------------------------
    # RESULTS
    # ------------------------
    print("\n=== SINGLE AGENT EVAL ===")
    print(single_eval)

    print("\n=== LANGGRAPH MULTI-AGENT EVAL ===")
    print(multi_eval)


if __name__ == "__main__":
    run()
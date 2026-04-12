from pathlib import Path

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from openai import OpenAI
from typing import TypedDict, List, Dict, Any
import os
from multi_agent.researcher import ResearcherAgent
from multi_agent.writer import WriterAgent
from multi_agent.editor import EditorAgent
from utils.logger import log_event, log_state
from utils.monitor import detect_issues

_here = Path(__file__).resolve().parent
load_dotenv(_here.parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------
# STATE DEFINITION
# -------------------------
class AgentState(TypedDict):
    query: str
    facts: list
    sources: list
    draft: str
    feedback: dict
    iteration: int
    llm_calls: int


# -------------------------
# NODES
# -------------------------

researcher = ResearcherAgent()
def researcher_node(state: AgentState):
    result = researcher.run(state["query"])

    return {
        **state,
        "facts": result["facts"],
        "sources": result["sources"]
    }

writer = WriterAgent()
def writer_node(state: AgentState):
    writer_output = writer.run(
        {
            "facts": state["facts"],
            "sources": state["sources"]
        },
        feedback=state.get("feedback")
    )

    state["llm_calls"] += 1

    new_state = {
        **state,
        "draft": writer_output["draft"],
        "llm_calls": state["llm_calls"]
    }

    return new_state

editor = EditorAgent()
def editor_node(state: AgentState):
    review = editor.run({
        "draft": state["draft"],
        "facts_used": state["facts"]
    })
    state["llm_calls"] += 1

    new_state = {
        **state,
        "feedback": review,
        "iteration": state["iteration"] + 1,
        "llm_calls": state["llm_calls"]
    }

    return new_state


# -------------------------
# ROUTING LOGIC
# -------------------------

def should_continue(state: AgentState):
    feedback = state["feedback"]

    # ✅ Approved
    if feedback.get("is_approved"):
        return END

    # ⚠️ No improvement possible
    if not feedback.get("issues") and not feedback.get("missing_points"):
        return END

    # ⚠️ Max iterations
    if state["iteration"] >= 3:
        return END

    return "writer"


# -------------------------
# GRAPH
# -------------------------

def wrap_node(node_fn, node_name):
    def wrapped(state):
        log_event("NODE_START", {"node": node_name})

        new_state = node_fn(state)

        log_state(node_name, new_state)

        detect_issues(new_state)

        return new_state

    return wrapped

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("researcher", wrap_node(researcher_node, "researcher"))
    graph.add_node("writer", wrap_node(writer_node, "writer"))
    graph.add_node("editor", wrap_node(editor_node, "editor"))

    graph.set_entry_point("researcher")

    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "editor")

    graph.add_conditional_edges(
        "editor",
        should_continue,
        {
            "writer": "writer",
            END: END
        }
    )

    return graph.compile()


# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app = build_graph()

    result = app.invoke({
        "query": "Impact of AI in healthcare",
        "facts": [],
        "sources": [],
        "draft": "",
        "feedback": {},
        "iteration": 0,
        "llm_calls": 0,
    })

    final_output = {
        "draft": result["draft"],
        "state": result
    }

    print("\n=== FINAL OUTPUT ===\n")
    print(final_output["draft"])
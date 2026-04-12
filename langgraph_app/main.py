from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# ---- Your existing modules ----
from multi_agent.researcher import ResearcherAgent
from multi_agent.writer import WriterAgent
from multi_agent.editor import EditorAgent
from memory.store import MemoryStore
from utils.logger import log_event, log_state
from utils.monitor import detect_issues

# ---- Init ----
_here = Path(__file__).resolve().parent
load_dotenv(_here.parent / ".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

researcher = ResearcherAgent()
writer = WriterAgent()
editor = EditorAgent()
memory_store = MemoryStore()

# -------------------------
# STATE DEFINITION
# -------------------------
class AgentState(TypedDict):
    query: str
    facts: List[str]
    sources: List[Dict[str, Any]]
    draft: str
    feedback: Dict
    iteration: int
    llm_calls: int
    memory: List[Dict[str, Any]]


# -------------------------
# WRAPPER (Logging + Monitoring)
# -------------------------
def wrap_node(node_fn, node_name):
    def wrapped(state: AgentState):
        log_event("NODE_START", {"node": node_name})

        new_state = node_fn(state)

        log_state(node_name, new_state)

        detect_issues(new_state)

        return new_state
    return wrapped


# -------------------------
# NODES
# -------------------------

# 🧠 Memory Node
def memory_node(state: AgentState):
    past = memory_store.search(state["query"])

    return {
        **state,
        "memory": past
    }


# 🔬 Researcher Node
def researcher_node(state: AgentState):
    result = researcher.run(state["query"])

    return {
        **state,
        "facts": result.get("facts", []),
        "sources": result.get("sources", [])
    }


# ✍️ Writer Node
def writer_node(state: AgentState):
    writer_output = writer.run(
        {
            "facts": state["facts"],
            "sources": state["sources"],
            "memory": state.get("memory", [])
        },
        feedback=state.get("feedback")
    )

    return {
        **state,
        "draft": writer_output["draft"],
        "llm_calls": state["llm_calls"] + 1
    }


# 🧑‍⚖️ Editor Node
def editor_node(state: AgentState):
    review = editor.run({
        "draft": state["draft"],
        "facts_used": state["facts"]
    })

    return {
        **state,
        "feedback": review,
        "iteration": state["iteration"] + 1,
        "llm_calls": state["llm_calls"] + 1
    }


# -------------------------
# ROUTING LOGIC
# -------------------------
def should_continue(state: AgentState):
    feedback = state["feedback"]

    # ✅ Approved
    if feedback.get("is_approved"):
        return END

    # ⚠️ Nothing to improve
    if not feedback.get("issues") and not feedback.get("missing_points"):
        return END

    # ⚠️ Max iterations
    if state["iteration"] >= 3:
        return END

    return "writer"


# -------------------------
# GRAPH BUILDER
# -------------------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("memory", wrap_node(memory_node, "memory"))
    graph.add_node("researcher", wrap_node(researcher_node, "researcher"))
    graph.add_node("writer", wrap_node(writer_node, "writer"))
    graph.add_node("editor", wrap_node(editor_node, "editor"))

    # Entry point
    graph.set_entry_point("memory")

    # Flow
    graph.add_edge("memory", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "editor")

    # Loop
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

    initial_state = {
        "query": "Impact of AI in healthcare",
        "facts": [],
        "sources": [],
        "draft": "",
        "feedback": {},
        "iteration": 0,
        "llm_calls": 0,
        "memory": []
    }

    result = app.invoke(initial_state)

    # 💾 Save to memory
    memory_store.save({
        "query": result["query"],
        "facts": result["facts"],
        "final_output": result["draft"]
    })

    # 🔥 FINAL OUTPUT (IMPORTANT FOR EVALUATION)
    final_output = {
        "draft": result["draft"],
        "state": result
    }

    print("\n=== FINAL OUTPUT ===\n")
    print(final_output["draft"])

    print("\n=== METRICS ===\n")
    print({
        "iterations": result["iteration"],
        "llm_calls": result["llm_calls"]
    })
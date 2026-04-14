# Research Forge — Autonomous Research Assistant

## Overview

Research Forge is a controlled research system that gathers evidence, updates memory, and produces structured answers. It combines:

- A **single-agent** loop (LLM policy + tools) for experimentation and baselines.
- A **LangGraph** workflow (memory → researcher → writer ↔ editor) used by the **HTTP API** and **Streamlit UI** for async jobs.
- A standalone **multi-agent orchestrator** (researcher → writer ↔ editor) runnable from experiments, parallel to the graph-based path.

## Why Not a Pipeline?

Traditional pipelines fail because research is not linear:

- Information may be incomplete.
- Additional search may be required.
- Quality must be evaluated dynamically.

The single-agent design uses a runtime **Observe → Think → Act** loop. The LangGraph design chains **retrieval**, **research**, **drafting**, and **review** with explicit state and conditional rewriting.

## Repository Layout

| Area | Role |
|------|------|
| **`agent/`** | Single-agent `ResearchAgent`: loop, `llm_policy`, `ToolRegistry`. |
| **`api/`** | FastAPI app: async research jobs, SQLite persistence, invokes LangGraph in background. |
| **`client/`** | Streamlit front end: start jobs, poll status, show answer and metrics. |
| **`langgraph_app/`** | `build_graph()`: **memory** → **researcher** → **writer** ↔ **editor** (`StateGraph`, conditional edges). |
| **`memory/`** | `AgentMemory` (agent loop), `MemoryStore` (JSON file for cross-run recall in the graph). |
| **`multi_agent/`** | `ResearcherAgent`, `WriterAgent`, `EditorAgent`, `Orchestrator` (writer–editor loop used by experiments). |
| **`storage/`** | SQLite `jobs` table (`jobs.db`) for API job state and logs. |
| **`tools/`** | `search_documents`, `summarize_notes`; `ToolRegistry`, `ToolLogger`. |
| **`utils/`** | Logging and monitoring hooks used by LangGraph nodes. |
| **`evaluation/`** | Scripts to compare single-agent vs LangGraph outputs. |
| **`experiments/`** | Runnable modules for each subsystem (see below). |

Design notes: **`agent/loop.md`**, **`memory/schema.md`**, **`multi_agent/architecture.md`**, **`api/design.md`**.

## Prerequisites

- Python 3.11+ (project uses a local `.venv`; adjust if needed).
- **OpenAI API key** for LLM-backed paths (researcher tools policy, writer, editor, single-agent policy).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a **`.env`** in the project root:

```env
OPENAI_API_KEY=sk-...
```

Run Python from the **repository root** so imports resolve (`python -m experiments...`, `uvicorn api.app:app`, etc.).

## Running the Web Stack

The Streamlit client expects the API at **`http://127.0.0.1:8000`**. Start the API first, then the UI.

**Terminal 1 — API (FastAPI + Uvicorn):**

```bash
uvicorn api.app:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 — Streamlit client:**

```bash
streamlit run client/app.py
```

- **`GET /`** — health check (`{"status": "ok"}`).
- **`POST /research/start`** — body `{"query": "..."}` → `job_id`, `status: "running"`.
- **`GET /research/{job_id}`** — job status and result (`answer` = final draft, plus `iterations`, `llm_calls`).
- **`GET /research/{job_id}/logs`** — log lines for the job.

Jobs run in a **background task**; state is stored in **`jobs.db`** (SQLite, created next to the process working directory—typically the repo root).

The LangGraph run also reads/writes **`memory_db.json`** via `MemoryStore` (past queries for the memory node).

## LangGraph Flow (API / `langgraph_app`)

1. **`memory`** — Loads recent matching entries from `MemoryStore` for the query.
2. **`researcher`** — `ResearcherAgent.run` → facts and sources (same tool stack as elsewhere).
3. **`writer`** — Draft from facts, sources, and memory context; optional feedback from the editor.
4. **`editor`** — Structured review; increments `iteration` and `llm_calls`.
5. **Routing** — If approved, no issues, or iteration cap (~3), **END**; else loop back to **writer**.

Try the graph standalone:

```bash
python -m langgraph_app.main
```

## Single-Agent Flow

1. **`ResearchAgent.run(query)`** (`agent/agent.py`) loops up to `max_steps`.
2. **Observe:** Query + `AgentMemory.to_dict()`.
3. **Think:** **`llm_decision`** (`agent/llm_policy.py`) → JSON action + input (`search_documents`, `summarize_notes`, or `stop`).
4. **Act:** **`ToolRegistry.execute`** → **`update_memory`**.

**Try it:** `python -m experiments.test_memory` · `python -m experiments.test_tools` · `python -m experiments.test_agent_llm` · `python -m experiments.evaluate_agent`

## Multi-Agent Experiments

- **`python -m experiments.test_researcher`** — Researcher only.
- **`python -m experiments.test_writer`** / **`test_editor`** — Components in isolation.
- **`python -m experiments.test_multi_agent`** — `ResearcherAgent` + **`Orchestrator`** (writer–editor), *not* the LangGraph compiler path.
- **`python -m experiments.compare_systems`** — Compare approaches.

**LangGraph vs orchestrator:** The **API** uses **`langgraph_app.build_graph()`**. The **orchestrator** in `multi_agent/orchestrator.py` is exercised by experiments for the same roles without LangGraph wiring.

## Evaluation

`evaluation/run_evaluation.py` compares the **single-agent** run with a **`build_graph().invoke(...)`** run on a fixed sample query (extend the script as needed):

```bash
python -m evaluation.run_evaluation
```

## Local Artifacts

| File | Purpose |
|------|---------|
| `jobs.db` | SQLite job rows for the API (created on first use). |
| `memory_db.json` | Append-only store for `MemoryStore` (LangGraph memory node). |

Add these to `.gitignore` if you do not want them committed (project-specific).

## Dependencies (high level)

Pinned in **`requirements.txt`**: OpenAI SDK, python-dotenv, LangGraph (and LangChain stack as required by LangGraph), FastAPI, Uvicorn, Streamlit, Requests.

## Goal

Given a research question, the system aims to produce:

- A structured answer (draft from writer / LangGraph or single-agent summary).
- Supporting evidence (facts) and source attribution where applicable.

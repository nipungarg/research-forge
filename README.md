# Research Forge — Autonomous Research Assistant

## Overview

Research Forge is a controlled research system that gathers evidence, updates explicit memory, and produces structured answers. It includes a **single-agent** loop (LLM policy + tools) and a **multi-agent** path (researcher → writer ↔ editor) for comparison and separation of roles.

## Why Not a Pipeline?

Traditional pipelines fail because research is not linear:

* Information may be incomplete
* Additional search may be required
* Quality must be evaluated dynamically

The single-agent design uses a runtime **Observe → Think → Act** loop. The multi-agent design splits **gathering**, **drafting**, and **review** so each step has a narrow contract.

## Repository Layout

| Area | Role |
|------|------|
| **`agent/`** | Single-agent `ResearchAgent`: loop, calls `llm_policy` for decisions, uses `ToolRegistry`. |
| **`memory/`** | `AgentMemory`: facts, sources, actions, open questions, metadata; JSON via `to_dict()` / `save()` / `load()`. |
| **`tools/`** | `search_documents`, `summarize_notes`; `ToolRegistry` dispatches and `ToolLogger` records calls. |
| **`multi_agent/`** | `ResearcherAgent` (rule-based search loop), `WriterAgent`, `EditorAgent`, `Orchestrator` (writer–editor iterations). |
| **`experiments/`** | Runnable scripts to exercise each subsystem (see below). |

Design notes live in **`agent/loop.md`**, **`memory/schema.md`**, and **`multi_agent/architecture.md`**.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a **`.env`** in the project root with `OPENAI_API_KEY=...` for any path that calls the OpenAI API (single-agent LLM policy, writer, editor).

Run experiments from the **repository root** so imports resolve:

```bash
python -m experiments.<module_name>
```

## Single-Agent Flow

1. **`ResearchAgent.run(query)`** (`agent/agent.py`) loops up to `max_steps`.
2. **Observe:** Builds an observation from the user query and `AgentMemory.to_dict()`.
3. **Think:** **`llm_decision`** (`agent/llm_policy.py`) returns JSON: `action` + `input` (`search_documents`, `summarize_notes`, or `stop`).
4. **Act:** **`ToolRegistry.execute`** runs the tool; results feed **`update_memory`** (facts/sources/summary in metadata).

Tools: lexical search over a small in-memory corpus (`tools/search.py`), deterministic summarize (`tools/summarize.py`).

**Try it:** `python -m experiments.test_memory` · `python -m experiments.test_tools` · `python -m experiments.test_agent_llm` · batch scenarios: `python -m experiments.evaluate_agent`

## Multi-Agent Flow

1. **`ResearcherAgent`** (`multi_agent/researcher.py`) runs a fixed loop: rule-based **decide** (search until enough facts or stuck), **act** via the same **`ToolRegistry`**, **`ResearcherMemory`** (`multi_agent/researcher_memory.py`) for facts/sources/queries.
2. **`Orchestrator`** (`multi_agent/orchestrator.py`) takes researcher output and runs **Writer** → **Editor** for up to `max_iterations`. The editor returns JSON feedback; the writer revises using that feedback until approval, no improvement, or max iterations.
3. **`WriterAgent`** / **`EditorAgent`** (`multi_agent/writer.py`, `multi_agent/editor.py`) use the OpenAI client for draft generation and structured review.

**Try it:** `python -m experiments.test_researcher` · `python -m experiments.test_writer` · `python -m experiments.test_editor` · end-to-end: `python -m experiments.test_multi_agent`

**Compare single vs multi:** `python -m experiments.compare_systems`

## Goal

Given a research question, the system aims to produce:

* Structured summary (single-agent metadata summary or multi-agent draft)
* Supporting evidence (facts)
* Source attribution (where applicable)

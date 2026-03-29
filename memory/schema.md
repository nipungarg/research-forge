# Agent Memory Schema

## 1. facts

Structured information extracted from tools or reasoning.

Example:

* "AI reduces diagnostic errors in radiology"
* "Study from Nature (2022)"

---

## 2. sources

List of references corresponding to facts.

Example:

* {"title": "...", "url": "..."}
* {"paper": "Nature 2022", "authors": "..."}

---

## 3. actions_taken

Chronological list of actions executed by the agent.

Example:

* "search: AI in healthcare"
* "summarize: document_1"

Purpose:
Prevents repeated or redundant actions.

---

## 4. open_questions

What the agent still needs to answer.

Example:

* "What are risks of AI in healthcare?"
* "Any conflicting studies?"

---

## 5. metadata (optional but recommended)

* step_count
* last_action
* status (running / complete)

---

## Design Principles

* Memory must be structured, not free text
* Each field must have a purpose
* Memory size must remain bounded

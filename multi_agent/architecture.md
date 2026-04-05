# Multi-Agent Architecture

## Agents

### 1. Researcher

Input: Query
Output: Facts + Sources

---

### 2. Writer

Input: Facts
Output: Structured Answer

---

### 3. Editor

Input: Answer + Facts
Output: Feedback (issues, gaps)

---

## Flow

1. Researcher gathers facts
2. Writer creates draft
3. Editor reviews draft

IF issues:
→ Writer revises
ELSE:
→ Final output

---

## Constraints

* Agents cannot perform others' roles
* All communication is explicit
* No hidden state sharing

---

## Termination

* Editor approves output
  OR
* Max iterations reached

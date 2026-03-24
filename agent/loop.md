# Agent Loop Design

## Observation

The agent observes:

* User query
* Current memory (facts, sources, actions taken)
* Remaining open questions

## Decision (Think)

The agent decides:

* Do I need more information?
* Should I call a search tool?
* Should I summarize?
* Is the task complete?

## Action

The agent performs one of:

* Search for documents
* Extract facts
* Generate summary
* Stop execution

## Stopping Conditions

The agent stops when:

* Enough facts are collected
* A complete summary can be generated
* Max steps reached

## Loop Constraint

Each iteration must:

* Perform only ONE action
* Log the decision
* Update memory explicitly

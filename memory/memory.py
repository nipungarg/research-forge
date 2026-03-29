import json
from typing import List, Dict, Any
from datetime import datetime


class AgentMemory:
    def __init__(self):
        self.facts: List[str] = []
        self.sources: List[Dict[str, Any]] = []
        self.actions_taken: List[str] = []
        self.open_questions: List[str] = []

        self.metadata: Dict[str, Any] = {
            "step_count": 0,
            "status": "running",
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }

    # -------------------------
    # ADD METHODS
    # -------------------------

    def add_fact(self, fact: str):
        if fact not in self.facts:
            self.facts.append(fact)
            self._update_timestamp()

    def add_source(self, source: Dict[str, Any]):
        if source not in self.sources:
            self.sources.append(source)
            self._update_timestamp()

    def add_action(self, action: str):
        self.actions_taken.append(action)
        self.metadata["step_count"] += 1
        self.metadata["last_action"] = action
        self._update_timestamp()

    def add_open_question(self, question: str):
        if question not in self.open_questions:
            self.open_questions.append(question)
            self._update_timestamp()

    def resolve_question(self, question: str):
        if question in self.open_questions:
            self.open_questions.remove(question)
            self._update_timestamp()

    def mark_complete(self):
        self.metadata["status"] = "complete"
        self._update_timestamp()

    # -------------------------
    # SERIALIZATION
    # -------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "facts": self.facts,
            "sources": self.sources,
            "actions_taken": self.actions_taken,
            "open_questions": self.open_questions,
            "metadata": self.metadata
        }

    def save(self, filepath: str):
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)

        memory = cls()
        memory.facts = data.get("facts", [])
        memory.sources = data.get("sources", [])
        memory.actions_taken = data.get("actions_taken", [])
        memory.open_questions = data.get("open_questions", [])
        memory.metadata = data.get("metadata", {})

        return memory

    # -------------------------
    # INTERNAL
    # -------------------------

    def _update_timestamp(self):
        self.metadata["last_updated"] = datetime.utcnow().isoformat()

    # -------------------------
    # DEBUGGING / INSPECTION
    # -------------------------

    def pretty_print(self):
        print(json.dumps(self.to_dict(), indent=2))
from typing import List, Dict, Any


class ResearcherMemory:
    def __init__(self):
        self.facts: List[str] = []
        self.sources: List[Dict[str, Any]] = []
        self.search_queries: List[str] = []
        self.step_count: int = 0

    def add_fact(self, fact: str):
        if fact not in self.facts:
            self.facts.append(fact)

    def add_source(self, source: Dict[str, Any]):
        if source not in self.sources:
            self.sources.append(source)

    def add_query(self, query: str):
        self.search_queries.append(query)

    def increment_step(self):
        self.step_count += 1

    def is_sufficient(self):
        return len(self.facts) >= 3  # simple threshold

    def is_stuck(self):
        if len(self.search_queries) >= 3:
            return len(set(self.search_queries[-3:])) == 1
        return False

    def to_dict(self):
        return {
            "facts": self.facts,
            "sources": self.sources,
            "search_queries": self.search_queries,
            "step_count": self.step_count
        }
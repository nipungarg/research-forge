import json
import os

MEMORY_FILE = "memory_db.json"


class MemoryStore:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)

    def save(self, entry):
        data = self.load()
        data.append(entry)

        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    def search(self, query):
        data = self.load()

        # Simple keyword match (can upgrade later)
        results = [
            item for item in data
            if query.lower() in item["query"].lower()
        ]

        return results[-3:]  # last 3 matches
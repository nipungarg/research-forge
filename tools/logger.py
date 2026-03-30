import json
from datetime import datetime


class ToolLogger:
    def __init__(self, filepath="tool_logs.json"):
        self.filepath = filepath

    def log(self, tool_name: str, inputs: dict, outputs: dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool_name,
            "inputs": inputs,
            "outputs": outputs
        }

        try:
            with open(self.filepath, "r") as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []

        logs.append(entry)

        with open(self.filepath, "w") as f:
            json.dump(logs, f, indent=2)
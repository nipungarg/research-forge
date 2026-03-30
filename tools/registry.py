from typing import Callable, Dict
from tools.search import search_documents
from tools.summarize import summarize_notes
from tools.logger import ToolLogger


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.logger = ToolLogger()

        self._register_tools()

    def _register_tools(self):
        self.tools["search_documents"] = search_documents
        self.tools["summarize_notes"] = summarize_notes

    def list_tools(self):
        return list(self.tools.keys())

    def execute(self, tool_name: str, **kwargs):
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")

        tool_fn = self.tools[tool_name]

        # Execute tool
        result = tool_fn(**kwargs)

        # Log execution
        self.logger.log(
            tool_name=tool_name,
            inputs=kwargs,
            outputs={"result": result}
        )

        return result
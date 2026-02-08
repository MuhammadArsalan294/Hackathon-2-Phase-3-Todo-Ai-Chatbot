"""
MCP Server for the Todo AI Chatbot
Implements the Model Context Protocol for AI agent interaction
"""
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class MCPServer:
    """
    MCP Server that hosts tools for the AI agent
    """
    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, func, description: str, parameters: Dict[str, Any]):
        """
        Register a tool with the MCP server
        """
        self.tools[name] = {
            "function": func,
            "description": description,
            "parameters": parameters
        }

    def get_tool_spec(self, name: str) -> Dict[str, Any]:
        """
        Get the specification for a registered tool
        """
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")

        tool = self.tools[name]
        return {
            "name": name,
            "description": tool["description"],
            "parameters": {
                "type": "object",
                "properties": tool["parameters"],
                "required": list(tool["parameters"].keys())  # Assuming all params are required
            }
        }

    def get_all_tool_specs(self) -> List[Dict[str, Any]]:
        """
        Get specifications for all registered tools
        """
        return [self.get_tool_spec(name) for name in self.tools.keys()]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a registered tool with the given arguments
        """
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")

        tool = self.tools[name]
        return tool["function"](**arguments)


# Global MCP server instance
mcp_server = MCPServer()


def get_mcp_tools():
    """
    Return all available MCP tools
    """
    return mcp_server.get_all_tool_specs()
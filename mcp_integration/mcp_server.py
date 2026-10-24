

import sys
from pathlib import Path

from fastmcp import FastMCP

# Add the project root to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.notes import save_note, get_notes
from tools.tasks import add_task, list_tasks
from tools.safe_calculator import safe_calculator



mcp = FastMCP(
    name="LangChain AI Assistant MCP Server",
    instructions=(
        "MCP server exposing calculator, notes, and task tools "
        "for the LangChain AI Assistant project."
    ),
)


@mcp.tool()
def calculate(expression: str) -> str:
    """Safely calculate a basic arithmetic expression."""
    return safe_calculator.invoke({"expression": expression})


@mcp.tool()
def save_user_note(content: str) -> str:
    """Save a note to the assistant's existing notes storage."""
    return save_note.invoke({"content": content})


@mcp.tool()
def read_notes() -> str:
    """Read all notes from the assistant's existing notes storage."""
    return get_notes.invoke({})


@mcp.tool()
def create_task(task: str) -> str:
    """Create a task in the assistant's existing task storage."""
    return add_task.invoke({"task": task})


@mcp.tool()
def read_tasks() -> str:
    """List tasks and their completion status."""
    return list_tasks.invoke({})


@mcp.tool()
def get_server_status() -> str:
    """Return the current status of the MCP server."""
    return "MCP Server is running."


if __name__ == "__main__":
    mcp.run(transport="stdio")

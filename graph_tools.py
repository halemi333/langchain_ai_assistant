
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from tools.safe_calculator import safe_calculator
from tools.notes import save_note, get_notes
from tools.tasks import add_task, list_tasks


class ToolState(TypedDict):
    tool_name: str
    tool_input: str
    result: str


def execute_tool(state: ToolState) -> dict:
    """Execute the selected tool."""

    tool_name = state["tool_name"]
    tool_input = state["tool_input"]

    if tool_name == "calculator":
        result = safe_calculator.invoke({
            "expression": tool_input
        })

    elif tool_name == "save_note":
        result = save_note.invoke({
            "content": tool_input
        })

    elif tool_name == "get_notes":
        result = get_notes.invoke({})

    elif tool_name == "add_task":
        result = add_task.invoke({
            "task": tool_input
        })

    elif tool_name == "list_tasks":
        result = list_tasks.invoke({})

    else:
        result = f"Unknown tool: {tool_name}"

    return {"result": result}


builder = StateGraph(ToolState)

builder.add_node("execute_tool", execute_tool)

builder.add_edge(START, "execute_tool")
builder.add_edge("execute_tool", END)

graph = builder.compile()


if __name__ == "__main__":
    print("LangGraph Tool Runner")
    print("Available tools:")
    print("calculator, save_note, get_notes, add_task, list_tasks")
    print("Type 'exit' to quit.")

    while True:
        tool_name = input("\nTool name: ").strip()

        if tool_name.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        tool_input = ""

        if tool_name in {"calculator", "save_note", "add_task"}:
            tool_input = input("Input: ")

        result = graph.invoke({
            "tool_name": tool_name,
            "tool_input": tool_input,
            "result": "",
        })

        print("Result:", result["result"])

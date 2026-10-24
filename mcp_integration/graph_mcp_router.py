

import asyncio
import re
import sys
from pathlib import Path
from typing import TypedDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain.mcp import MCPAdapter
from langgraph.graph import END, START, StateGraph

from tool_router import select_tool


SERVER_PATH = Path(__file__).with_name("mcp_server.py")



class ToolRouterState(TypedDict):
    message: str
    tool_name: str
    result: str


def route_message(state: ToolRouterState) -> dict:
    """Select a tool using the existing project router."""
    return {"tool_name": select_tool(state["message"])}


def choose_route(state: ToolRouterState) -> str:
    """Choose the next graph node."""
    return state["tool_name"]


def extract_expression(message: str) -> str:
    """Extract a basic arithmetic expression from the message."""
    digit_translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )
    message = message.translate(digit_translation)

    tokens = re.findall(r"\d+|//|\*\*|[()+\-*/%]", message)
    return " ".join(tokens)


def format_tool_result(result):
    """Convert MCP text content blocks into readable text."""
    if isinstance(result, list):
        texts = []

        for item in result:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))

        if texts:
            return "\n".join(texts)

    return str(result)


async def run_assistant():
    async with MCPAdapter(SERVER_PATH) as adapter:
        tools = {tool.name: tool for tool in await adapter.list_tools()}

        async def run_calculator(state: ToolRouterState) -> dict:
            expression = extract_expression(state["message"])

            if not expression:
                return {"result": "No mathematical expression found."}

            result = await tools["calculate"].ainvoke(
                {"expression": expression}
            )
            return {"result": format_tool_result(result)}

        async def run_notes(state: ToolRouterState) -> dict:
            result = await tools["read_notes"].ainvoke({})
            return {"result": format_tool_result(result)}

        async def run_save_note(state: ToolRouterState) -> dict:
            # Remove a common English command prefix.
            content = re.sub(
                r"^(save note|remember this|take a note)\s*[:\-]?\s*",
                "",
                state["message"],
                flags=re.IGNORECASE,
            ).strip()

            if not content:
                return {"result": "Error: Note content cannot be empty."}

            result = await tools["save_user_note"].ainvoke(
                {"content": content}
            )
            return {"result": format_tool_result(result)}

        async def run_tasks(state: ToolRouterState) -> dict:
            result = await tools["read_tasks"].ainvoke({})
            return {"result": format_tool_result(result)}
        
        async def run_add_task(state: ToolRouterState) -> dict:
            task_text = re.sub(
                r"^(add task|create task|new task)\s*[:\-]?\s*",
                "",
                state["message"],
                flags=re.IGNORECASE,
            ).strip()

            if not task_text:
                return {"result": "Error: Task description cannot be empty."}

            result = await tools["create_task"].ainvoke(
                {"task": task_text}
            )
            return {"result": format_tool_result(result)}

        async def run_unknown(state: ToolRouterState) -> dict:
            return {"result": "I could not identify a supported tool."}

        builder = StateGraph(ToolRouterState)

        builder.add_node("route_message", route_message)
        builder.add_node("calculator", run_calculator)
        builder.add_node("get_notes", run_notes)
        builder.add_node("save_note", run_save_note)
        builder.add_node("list_tasks", run_tasks)
        builder.add_node("add_task", run_add_task)
        builder.add_node("unknown", run_unknown)

        builder.add_edge(START, "route_message")
        builder.add_conditional_edges(
            "route_message",
            choose_route,
            {
                "calculator": "calculator",
                "get_notes": "get_notes",
                "save_note": "save_note",
                "list_tasks": "list_tasks",
                "add_task": "add_task",
                "unknown": "unknown",
            },
        )

        for node in (
            "calculator",
            "get_notes",
            "save_note",
            "list_tasks",
            "add_task",
            "unknown",
        ):
            builder.add_edge(node, END)

        graph = builder.compile()

        print("MCP LangGraph Assistant Started...")
        print("Type 'exit' or 'quit' to stop.")

        while True:
            message = input("\nUser: ").strip()

            if message.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not message:
                continue

            result = await graph.ainvoke(
                {
                    "message": message,
                    "tool_name": "",
                    "result": "",
                }
            )

            print(f"\nSelected tool: {result['tool_name']}")
            print(f"Assistant: {result['result']}")



async def main():
    await run_assistant()


if __name__ == "__main__":
    asyncio.run(main())

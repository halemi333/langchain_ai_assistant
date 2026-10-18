
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from tool_router import select_tool

from tools.safe_calculator import safe_calculator

from tools.tasks import list_tasks

from tools.tasks import add_task

from tools.notes import get_notes

import re


class ToolRouterState(TypedDict):
    message: str
    tool_name: str
    result: str



def route_message(state: ToolRouterState) -> dict:
    """Select a tool based on the user's message."""

    tool_name = select_tool(state["message"])

    return {
        "tool_name": tool_name,
    }


def choose_route(state: ToolRouterState) -> str:
    """Choose the next graph node based on the selected tool."""

    return state["tool_name"]


def run_calculator(state: ToolRouterState) -> dict:
    """Extract and calculate a math expression from the message."""

    message = state["message"]

    # Convert Persian and Arabic digits to English digits.
    digit_translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )
    message = message.translate(digit_translation)

    # Extract numbers and supported arithmetic operators.
    tokens = re.findall(
    r"\d+|//|\*\*|[()+\-*/%]",
    message,
    )

    expression = " ".join(tokens)

    if not expression:
        return {"result": "No mathematical expression found."}

    result = safe_calculator.invoke({
        "expression": expression
    })

    return {"result": result}


def run_tasks(state: ToolRouterState) -> dict:
    """Run the task-listing tool."""

    result = list_tasks.invoke({})

    return {
        "result": result
    }


def run_add_task(state: ToolRouterState) -> dict:
    """Create a task from the user's message."""
    task_text = re.sub(
    r"^(وظیفه جدید|ثبت وظیفه|اضافه کن|add task|create task)\s*[:：-]?\s*",
    "",
    state["message"],
    flags=re.IGNORECASE,
).strip()
    if not task_text:
        return {"result": "Error: Task description cannot be empty."}
    result = add_task.invoke({"task": task_text})
    return {"result": result}


def run_notes(state: ToolRouterState) -> dict:
    """Run the notes-reading tool."""

    result = get_notes.invoke({})

    return {
        "result": result
    }


builder = StateGraph(ToolRouterState)


builder.add_node("route_message", route_message)

builder.add_node("calculator", run_calculator)
builder.add_node("notes", run_notes)
builder.add_node("tasks", run_tasks)
builder.add_node("add_task", run_add_task)
builder.add_node("unknown", lambda state: {})

builder.add_edge(START, "route_message")

builder.add_conditional_edges(
    "route_message",
    choose_route,
    {
        "calculator": "calculator",
        "save_note": "notes",
        "get_notes": "notes",
        "add_task": "add_task",
        "list_tasks": "tasks",
        "unknown": "unknown",
    },
)

builder.add_edge("calculator", END)
builder.add_edge("notes", END)
builder.add_edge("tasks", END)
builder.add_edge("add_task", END)
builder.add_edge("unknown", END)


graph = builder.compile()




if __name__ == "__main__":
    test_messages = [
        "حاصل ۲ + ۳ چیست؟",
        "وظایفم را نشان بده",
        "یادداشت‌هایم را نمایش بده",
        "add task",
        "وظیفه جدید: خرید نان",
        "hello",
    ]

    for message in test_messages:
        result = graph.invoke({
            "message": message,
            "tool_name": "",
            "result": "",
        })

        print(
            f"Message: {message} "
            f"-> Selected tool: {result['tool_name']}"
        )

        # Print the calculation result only for calculator requests.
        if result["tool_name"] == "calculator":
            print("Calculation result:", result["result"])
            
        if result["tool_name"] == "list_tasks":
            print("Tasks:", result["result"])
            
        if result["tool_name"] == "add_task":
            print("Added task:", result["result"])
             
        if result["tool_name"] == "get_notes":
            print("Notes:", result["result"])


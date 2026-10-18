
from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END


class AssistantState(TypedDict):
    message: str
    route: str
    response: str


def router(state: AssistantState) -> dict:
    """Choose a route using simple rules."""

    message = state["message"].lower()

    complex_keywords = [
        "analyze",
        "compare",
        "explain in detail",
        "plan",
        "analysis",
        "تحلیل",
        "مقایسه",
        "برنامه‌ریزی",
    ]

    if any(keyword in message for keyword in complex_keywords):
        selected_route = "analysis"
    else:
        selected_route = "normal"

    print(f"[Router] Selected route: {selected_route}")

    return {"route": selected_route}


def choose_route(
    state: AssistantState,
) -> Literal["normal", "analysis"]:
    return state["route"]


def normal_node(state: AssistantState) -> dict:
    return {
        "response": (
            "[NORMAL MOCK] Simple request: "
            f"{state['message']}"
        )
    }


def analysis_node(state: AssistantState) -> dict:
    return {
        "response": (
            "[ANALYSIS MOCK] Complex request: "
            f"{state['message']}"
        )
    }


builder = StateGraph(AssistantState)

builder.add_node("router", router)
builder.add_node("normal", normal_node)
builder.add_node("analysis", analysis_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "normal": "normal",
        "analysis": "analysis",
    },
)

builder.add_edge("normal", END)
builder.add_edge("analysis", END)

graph = builder.compile()


if __name__ == "__main__":
    print("LangGraph Conditional Router")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not user_input:
            print("Please enter a message.")
            continue

        result = graph.invoke({
            "message": user_input,
            "route": "",
            "response": "",
        })

        print("Assistant:", result["response"])

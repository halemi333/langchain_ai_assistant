
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from core.mock_llm import MockLLM

llm = MockLLM()


class AssistantState(TypedDict):
    message: str
    response: str


def respond(state: AssistantState) -> dict:
    """Generate a response using the language model."""

    result = llm.invoke(state["message"])

    return {
        "response": result.content
    }


builder = StateGraph(AssistantState)

builder.add_node("respond", respond)

builder.add_edge(START, "respond")
builder.add_edge("respond", END)

graph = builder.compile()



if __name__ == "__main__":
    print("LangGraph Mock Assistant")
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
            "response": ""
        })

        print("Assistant:", result["response"])

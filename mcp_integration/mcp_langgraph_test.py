
import asyncio
from pathlib import Path
from typing import TypedDict

from langchain.mcp import MCPAdapter
from langgraph.graph import END, StateGraph


SERVER_PATH = Path(__file__).with_name("mcp_server.py")


class CalculatorState(TypedDict):
    expression: str
    result: str


async def main():
    async with MCPAdapter(SERVER_PATH) as adapter:
        tools = await adapter.list_tools()
        tools_by_name = {tool.name: tool for tool in tools}

        async def calculate_node(state: CalculatorState):
            result = await tools_by_name["calculate"].ainvoke(
                {"expression": state["expression"]}
            )

            return {"result": str(result)}

        builder = StateGraph(CalculatorState)
        builder.add_node("calculate", calculate_node)
        builder.set_entry_point("calculate")
        builder.add_edge("calculate", END)

        graph = builder.compile()

        result = await graph.ainvoke(
            {"expression": "(10 + 5) * 2"}
        )

        print("Expression:", result["expression"])
        print("Result:", result["result"])


if __name__ == "__main__":
    asyncio.run(main())

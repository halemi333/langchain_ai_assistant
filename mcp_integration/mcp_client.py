
import asyncio
from pathlib import Path

from langchain.mcp import MCPAdapter


SERVER_PATH = Path(__file__).with_name("mcp_server.py")


async def main():
    async with MCPAdapter(SERVER_PATH) as adapter:
        tools = await adapter.list_tools()

        print("Discovered MCP tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        tools_by_name = {tool.name: tool for tool in tools}

        print("\n--- Calculator test ---")
        result = await tools_by_name["calculate"].ainvoke(
            {"expression": "(10 + 5) * 2"}
        )
        print("Calculation result:", result)

        print("\n--- Read notes test ---")
        notes = await tools_by_name["read_notes"].ainvoke({})
        print("Notes:", notes)

        print("\n--- Read tasks test ---")
        tasks = await tools_by_name["read_tasks"].ainvoke({})
        print("Tasks:", tasks)


if __name__ == "__main__":
    asyncio.run(main())
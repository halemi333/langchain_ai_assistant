
import asyncio

from mcp_integration.graph_mcp_router import run_assistant


def main():
    asyncio.run(run_assistant())


if __name__ == "__main__":
    main()

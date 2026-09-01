"""Exercise the mcp-intro server over stdio without any external tooling.

Run:
    ./.venv/bin/python client_demo.py

It spawns server.py as a subprocess, speaks MCP over stdio, and calls every
primitive the server exposes.
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="./.venv/bin/python", args=["server.py"])


async def main() -> None:
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("tools:", [t.name for t in tools.tools])

            add_result = await session.call_tool("add", {"a": 2, "b": 3})
            print("add(2, 3) ->", add_result.content[0].text)

            greet_result = await session.call_tool("greet", {"name": "Ada"})
            print("greet('Ada') ->", greet_result.content[0].text)

            resources = await session.list_resources()
            print("resources:", [str(r.uri) for r in resources.resources])

            version = await session.read_resource("config://version")
            print("config://version ->", version.contents[0].text)

            prompts = await session.list_prompts()
            print("prompts:", [p.name for p in prompts.prompts])

            summary = await session.get_prompt("summarize", {"text": "MCP is a protocol."})
            print("summarize(...) ->", summary.messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())

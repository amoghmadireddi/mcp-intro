"""A minimal MCP server built with MCPServer from the official SDK (mcp 2.x).

Run directly (stdio transport):
    ./.venv/bin/python server.py

Or explore interactively:
    ./.venv/bin/mcp dev server.py
"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("mcp-intro")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


@mcp.resource("config://version")
def version() -> str:
    """Expose the server version as a readable resource."""
    return "1.0.0"


@mcp.prompt()
def summarize(text: str) -> str:
    """A reusable prompt template the client can invoke."""
    return f"Summarize the following text in one sentence:\n\n{text}"


if __name__ == "__main__":
    mcp.run()

# mcp-intro

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server built
with the official Python SDK (`mcp` 2.x). It exposes two tools, one resource, and
one prompt so you can see each MCP primitive working end to end.

## Contents

| Path               | Description                                                                                     |
| ------------------ | --------------------------------------------------------------------------------------------- |
| `server.py`        | The MCP server. Defines the `add` and `greet` tools, a `config://version` resource, and a `summarize` prompt, then runs over stdio. |
| `client_demo.py`   | A pure-Python client that spawns `server.py` over stdio and calls every primitive. Useful for a quick smoke test with no Node required. |
| `requirements.txt` | Python dependencies — just `mcp[cli]`, which pulls in the SDK and the `mcp` command-line tool. |
| `.gitignore`       | Ignores the virtualenv and Python bytecode.                                                   |
| `.venv/`           | Local virtual environment (not committed).                                                    |

## What the server provides

- **Tools**
  - `add(a: int, b: int) -> int` — returns `a + b`.
  - `greet(name: str) -> str` — returns `"Hello, {name}!"`.
- **Resource**
  - `config://version` — returns the server version string (`"1.0.0"`).
- **Prompt**
  - `summarize(text: str)` — a reusable prompt template that asks the model to
    summarize `text` in one sentence.

## Setup

Requires Python 3.13+ (the checked-in `.venv` uses 3.13).

```bash
cd /Users/amoghmadireddi/pl/mcp-intro

# Create the virtualenv if it does not already exist
python3 -m venv .venv

# Install dependencies
./.venv/bin/python -m pip install -r requirements.txt
```

## Running the server

The server speaks the **stdio** transport, so it is normally launched by an MCP
client rather than run by hand. To start it directly:

```bash
./.venv/bin/python server.py
```

It will sit waiting for MCP protocol messages on stdin/stdout — this is expected.
Press `Ctrl+C` to stop.

## Quick smoke test (pure Python)

```bash
./.venv/bin/python client_demo.py
```

Expected output:

```
tools: ['add', 'greet']
add(2, 3) -> 5
greet('Ada') -> Hello, Ada!
resources: ['config://version']
config://version -> 1.0.0
prompts: ['summarize']
summarize(...) -> Summarize the following text in one sentence:

MCP is a protocol.
```

## Using it interactively (MCP Inspector)

The `mcp` CLI (installed via `mcp[cli]`) can launch the server with a web-based
inspector for poking at tools, resources, and prompts:

```bash
./.venv/bin/mcp dev server.py
```

**Requires Node.js** — `mcp dev` shells out to `npx` to run the MCP Inspector.
On macOS: `brew install node`.

Then open the URL it prints (it includes an auth token and usually opens your
browser automatically). Click **Connect**, then from the inspector you can:

- call `add` with e.g. `a = 2`, `b = 3` and see `5`
- call `greet` with `name = "Ada"` and see `Hello, Ada!`
- read the `config://version` resource
- render the `summarize` prompt with some text

## Using it from an MCP client

Register the server with any MCP-capable client (Claude Desktop, Claude Code,
etc.) by pointing it at the virtualenv's Python and `server.py`.

Example client config entry:

```json
{
  "mcpServers": {
    "mcp-intro": {
      "command": "/Users/amoghmadireddi/pl/mcp-intro/.venv/bin/python",
      "args": ["/Users/amoghmadireddi/pl/mcp-intro/server.py"]
    }
  }
}
```

For Claude Code specifically:

```bash
claude mcp add mcp-intro -- /Users/amoghmadireddi/pl/mcp-intro/.venv/bin/python /Users/amoghmadireddi/pl/mcp-intro/server.py
```

Once connected, the client can list and call the `add` / `greet` tools, read the
`config://version` resource, and use the `summarize` prompt.

## Extending it

Add a new tool by writing a function and decorating it:

```python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

The type hints define the input schema and the docstring becomes the tool
description shown to clients.

"""Tiny MCP server over stdio (mcp 2.3.0)."""
import sys

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("demo-server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    print(f"add called with a={a}, b={b}", file=sys.stderr)  # logs go to stderr, never stdout
    return a + b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ToolError("b must not be zero")  # becomes an isError: true tool result
    return a / b


if __name__ == "__main__":
    mcp.run()  # default transport is stdio

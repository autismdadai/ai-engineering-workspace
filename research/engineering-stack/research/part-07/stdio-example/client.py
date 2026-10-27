"""Launch server.py as a stdio subprocess, list tools, call tools (mcp 2.3.0)."""
import asyncio
import sys

from mcp import Client, StdioServerParameters


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(params) as client:  # default mode='auto': probes server/discover
        print("protocol version:", client.protocol_version)
        print("server info:", client.server_info)
        tools = await client.list_tools()
        for t in tools.tools:
            print("tool:", t.name, "|", t.description, "|", t.input_schema)
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print("add structured_content:", result.structured_content)
        print("add content:", result.content)
        print("add is_error:", result.is_error)
        bad = await client.call_tool("divide", {"a": 1, "b": 0})
        print("divide is_error:", bad.is_error, "|", bad.content[0].text)


asyncio.run(main())

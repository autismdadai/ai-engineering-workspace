"""In-memory test: no subprocess, no wire (mcp 2.3.0)."""
import asyncio

from mcp import Client
from server import mcp as server


async def main() -> None:
    async with Client(server) as client:
        r = await client.call_tool("add", {"a": 40, "b": 2})
        assert r.structured_content == {"result": 42}, r
        print("in-memory OK:", r.structured_content)


asyncio.run(main())

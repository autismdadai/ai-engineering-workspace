"""Optional cross-check against the official Python SDK (pip install mcp==2.3.0).

Interoperability in both directions:
  A. the SDK's client talks to this lab's standard-library server
  B. this lab's client talks to a server built with the SDK's MCPServer
Prints PASS, FAIL or SKIP lines; exits 1 if any check fails or all are skipped.
"""
import asyncio
import os
import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
results = []


def report(label, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} {label}{': ' + str(detail) if detail != '' else ''}")


try:
    import mcp
    from mcp import Client, StdioServerParameters
    from importlib.metadata import version
    SDK = version("mcp")
except ImportError:
    print("SKIP the mcp package is not installed (pip install -r requirements-crosscheck.txt)")
    sys.exit(1)

print(f"INFO mcp {SDK} on Python {sys.version.split()[0]}")
if SDK != "2.3.0":
    print("INFO this cross-check was written for mcp 2.3.0; other versions may differ")


async def sdk_client_to_lab_server():
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "notes_server.py")])
    async with Client(params) as client:
        report("A1 the SDK client agrees on protocol 2026-07-28 with the lab server",
               client.protocol_version == "2026-07-28", client.protocol_version)
        tools = await client.list_tools()
        names = [t.name for t in tools.tools]
        report("A2 the SDK client lists the lab server's three tools", names ==
               ["search_notes", "add_note", "delete_note"], names)
        found = await client.call_tool("search_notes", {"query": "ledger"})
        report("A3 the SDK client calls a lab tool and reads structured content",
               found.is_error is False and found.structured_content["hits"][0]["id"] == "n2",
               found.structured_content["hits"][0]["id"])

    asked = []

    async def confirm(context, params):
        asked.append(params.message)
        return mcp.types.ElicitResult(action="accept", content={"confirm": True})

    async with Client(params, elicitation_callback=confirm) as client:
        done = await client.call_tool("delete_note", {"note_id": "n3"})
        report("A4 the SDK client answers the lab server's input_required round and retries",
               len(asked) == 1 and done.structured_content == {"deleted": "n3", "text":
               "Rotate the staging API key every 90 days."}, asked[0] if asked else "no prompt")


SDK_SERVER = '''
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

server = MCPServer("sdk-notes")

@server.tool()
def word_count(text: str) -> int:
    """Count the words in a text."""
    return len(text.split())

@server.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ToolError("b must not be zero")
    return a / b

if __name__ == "__main__":
    server.run()
'''


def lab_client_to_sdk_server():
    from mcp_client import RpcError, StdioClient
    folder = pathlib.Path(tempfile.mkdtemp())
    (folder / "sdk_server.py").write_text(SDK_SERVER, encoding="utf-8")
    with StdioClient([sys.executable, str(folder / "sdk_server.py")]) as c:
        found = c.discover()
        report("B1 the lab client's server/discover works against the SDK server",
               "2026-07-28" in found["supportedVersions"] and found["resultType"] == "complete",
               found["supportedVersions"])
        tools = {t["name"]: t for t in c.list_tools()}
        report("B2 the SDK turned type hints into input schemas",
               tools["word_count"]["inputSchema"]["properties"]["text"]["type"] == "string"
               and tools["divide"]["inputSchema"]["required"] == ["a", "b"], sorted(tools))
        counted = c.call_tool("word_count", {"text": "model context protocol"})
        report("B3 the lab client calls an SDK tool", counted["structuredContent"] == {"result": 3}
               and counted["isError"] is False, counted["structuredContent"])
        bad = c.call_tool("divide", {"a": 1, "b": 0})
        report("B4 a ToolError comes back as isError: true with its message",
               bad["isError"] is True and "b must not be zero" in bad["content"][0]["text"],
               bad["content"][0]["text"])
        try:
            unknown = c.call_tool("nope", {})
            how = "isError result" if unknown.get("isError") else "unexpected success"
        except RpcError as error:
            how = f"JSON-RPC error {error.code}"
        print(f"INFO an unknown tool on the SDK server comes back as: {how} "
              "(the spec's example uses a JSON-RPC error; the lab server follows the spec)")


asyncio.run(sdk_client_to_lab_server())
lab_client_to_sdk_server()
print(f"\n{sum(results)} of {len(results)} cross-checks passed")
sys.exit(0 if results and all(results) else 1)

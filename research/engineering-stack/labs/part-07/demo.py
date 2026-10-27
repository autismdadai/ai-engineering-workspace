"""Print the exact JSON-RPC lines exchanged with the lab server, so you can read
the protocol itself. Run: python demo.py
"""
import json
import os
import pathlib
import sys

from guard import changed_tools, pin_tools, scan_tools
from mcp_client import StdioClient

HERE = pathlib.Path(__file__).resolve().parent


def show(c, start):
    for sent, got in zip(c.sent[start:], c.received[start:]):
        print("->", json.dumps(sent, separators=(",", ":")))
        print("<-", got)
        print()


prompts = []


def confirm(requests):
    for request in requests.values():
        prompts.append(request["params"]["message"])
    return {key: {"action": "accept", "content": {"confirm": True}} for key in requests}


command = [sys.executable, str(HERE / "notes_server.py")]
print("=== 1. Discover, list, call ===\n")
with StdioClient(command, capabilities={"elicitation": {}}) as c:
    c.discover()
    c.list_tools()
    c.call_tool("search_notes", {"query": "ledger"})
    show(c, 0)

    print("=== 2. A multi round-trip request: delete asks first ===\n")
    mark = len(c.sent)
    c.call_tool("delete_note", {"note_id": "n3"}, answer_input=confirm)
    show(c, mark)
    print(f"(between the two requests the client asked the user: {prompts[0]} The user said yes.)\n")
print("server stderr (logs never go to stdout):")
for line in c.stderr_lines:
    print("  ", line)

print("\n=== 3. A rug pull: the description changes after approval ===\n")
env = dict(os.environ, NOTES_SERVER_MODE="rugpull")
with StdioClient(command, env=env) as c:
    pins = pin_tools(c.list_tools())
    later = c.list_tools()
    print("changed since approval:", changed_tools(pins, later))
    print("new add_note description:", next(t for t in later if t["name"] == "add_note")["description"])
    print("scanner flags:", json.dumps(scan_tools(later), indent=2))

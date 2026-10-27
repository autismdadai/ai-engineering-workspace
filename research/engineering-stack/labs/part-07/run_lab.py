"""Part 07 lab checks: an MCP server and client over stdio, tool guards and a
skill checker. Standard library only. Run: python run_lab.py

Each check runs on its own with fresh server processes, so one broken check
prints FAIL and the rest still run.
"""
import datetime
import json
import os
import pathlib
import subprocess
import sys
import tempfile

from guard import changed_tools, needs_approval, pin_tools, scan_tools
from mcp_client import RpcError, StdioClient, server_command
from skill_check import check_skill

HERE = pathlib.Path(__file__).resolve().parent
CHECKS = []


def check(label):
    def register(fn):
        CHECKS.append((label, fn))
        return fn
    return register


def client(mode="normal", capabilities=None, version="2026-07-28"):
    env = dict(os.environ, NOTES_SERVER_MODE=mode)
    return StdioClient(server_command(str(HERE / "notes_server.py")), env=env,
                       capabilities=capabilities, version=version)


def asker():
    return client(capabilities={"elicitation": {}})


def rpc_error(fn):
    try:
        fn()
    except RpcError as error:
        return error
    return None


def accept(requests):
    return {key: {"action": "accept", "content": {"confirm": True}} for key in requests}


def decline(requests):
    return {key: {"action": "decline"} for key in requests}


def retry(c, name, arguments, asked, responses, state=None):
    return c.request("tools/call", {"name": name, "arguments": arguments,
                                    "inputResponses": responses(asked["inputRequests"]),
                                    "requestState": asked["requestState"] if state is None else state})


@check("1 server/discover answers the first request, with no initialize")
def _():
    with client() as c:
        found = c.discover()
    ok = (found["supportedVersions"] == ["2026-07-28"] and found["resultType"] == "complete"
          and found["_meta"]["io.modelcontextprotocol/serverInfo"]["name"] == "notes-server")
    return ok, found["supportedVersions"]


@check("2 tools/list: three tools, same order every time, cache hints present")
def _():
    with client() as c:
        first, second = c.list_tools(), c.list_tools()
        listing = c.request("tools/list")
    names = [t["name"] for t in first]
    ok = (names == ["search_notes", "add_note", "delete_note"] and first == second
          and "ttlMs" in listing and listing["cacheScope"] in ("public", "private")
          and all(t["inputSchema"]["type"] == "object" for t in first))
    return ok, names


@check("3 a request without the _meta envelope is refused with -32602")
def _():
    with client() as c:
        error = rpc_error(lambda: c.request("tools/list", meta=False))
    return error is not None and error.code == -32602, error and error.code


@check("3b an unsupported version gets -32022 and the list of supported versions")
def _():
    with client(version="2025-06-18") as c:
        error = rpc_error(c.discover)
    ok = (error is not None and error.code == -32022
          and error.data == {"supported": ["2026-07-28"], "requested": "2025-06-18"})
    return ok, error and error.data


@check("3c every stdout line is one JSON-RPC message; logs are on stderr")
def _():
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
        "name": "search_notes", "arguments": {"query": "key"},
        "_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28",
                  "io.modelcontextprotocol/clientCapabilities": {}}}}
    raw = subprocess.run([sys.executable, str(HERE / "notes_server.py")],
                         input=json.dumps(request) + "\n", capture_output=True, text=True, timeout=30)
    lines = [line for line in raw.stdout.splitlines() if line]
    try:
        parsed = [json.loads(line) for line in lines]
    except json.JSONDecodeError:
        return False, f"stdout has a line that is not JSON: {lines[0][:60]!r}"
    ok = (len(parsed) == 1 and parsed[0]["jsonrpc"] == "2.0"
          and "[notes-server]" in raw.stderr and "[notes-server]" not in raw.stdout)
    return ok, f"{len(lines)} stdout line, {len(raw.stderr.splitlines())} stderr lines"


@check("4 search_notes returns structuredContent and the same hits as text")
def _():
    with client() as c:
        found = c.call_tool("search_notes", {"query": "ledger"})
    hits = found.get("structuredContent", {}).get("hits", [])
    ok = (found["isError"] is False and hits and hits[0]["id"] == "n2"
          and "[n2]" in found["content"][0]["text"])
    return ok, hits


@check("4b bad arguments come back as isError: true, not as a protocol error")
def _():
    with client() as c:
        error = rpc_error(lambda: c.call_tool("search_notes", {"query": ""}))
        if error is not None:
            return False, f"protocol error {error.code}: {error.message}"
        bad = c.call_tool("search_notes", {"query": ""})
    text = bad["content"][0]["text"]
    return bad["isError"] is True and "too short" in text, text


@check("4c an unknown tool is a JSON-RPC error -32602")
def _():
    with client() as c:
        error = rpc_error(lambda: c.call_tool("format_disk", {}))
    ok = error is not None and error.code == -32602 and "Unknown tool" in error.message
    return ok, error and error.message


@check("5 delete_note asks first (input_required), then deletes on a retry with a new id")
def _():
    with asker() as c:
        first = c.call_tool("delete_note", {"note_id": "n3"})
        mark = len(c.sent)
        done = c.call_tool("delete_note", {"note_id": "n3"}, answer_input=accept)
        ids = [m["id"] for m in c.sent[mark:]]
    if first["resultType"] != "input_required":
        return False, f"no confirmation asked: {first['content'][0]['text']}"
    ok = (first["inputRequests"]["confirm"]["method"] == "elicitation/create"
          and "requestState" in first and done.get("structuredContent", {}).get("deleted") == "n3"
          and len(ids) == 2 and ids[0] != ids[1])
    return ok, f"ids {ids}"


@check("5b when the user declines, the note is kept")
def _():
    with asker() as c:
        kept = c.call_tool("delete_note", {"note_id": "n1"}, answer_input=decline)
        hits = c.call_tool("search_notes", {"query": "tuesdays"})["structuredContent"]["hits"]
    ok = kept.get("structuredContent", {}).get("deleted") is None and hits and hits[0]["id"] == "n1"
    return ok, kept["content"][0]["text"]


@check("5c a tampered requestState is refused")
def _():
    with asker() as c:
        asked = c.call_tool("delete_note", {"note_id": "n1"})
        body, tag = asked["requestState"].rsplit(".", 1)
        forged = body + "." + ("0" if tag[0] != "0" else "1") + tag[1:]
        error = rpc_error(lambda: retry(c, "delete_note", {"note_id": "n1"}, asked, accept, forged))
    return error is not None and "verification" in error.message, error and error.message


@check("5d state issued for n1 cannot delete n2")
def _():
    with asker() as c:
        asked = c.call_tool("delete_note", {"note_id": "n1"})
        error = rpc_error(lambda: retry(c, "delete_note", {"note_id": "n2"}, asked, accept))
    return error is not None and "different call" in error.message, error and error.message


@check("5e without the elicitation capability, delete_note returns -32021")
def _():
    with client(capabilities={}) as c:
        error = rpc_error(lambda: c.call_tool("delete_note", {"note_id": "n1"}))
    ok = (error is not None and error.code == -32021
          and error.data == {"requiredCapabilities": {"elicitation": {}}})
    return ok, error and error.code


@check("6 a different server process completes the retry (no session needed)")
def _():
    with asker() as one, asker() as two:
        asked = one.call_tool("delete_note", {"note_id": "n4"})
        try:
            finished = retry(two, "delete_note", {"note_id": "n4"}, asked, accept)
        except RpcError as error:
            return False, f"the second process refused the retry: {error.message}"
        pids = (one.process.pid, two.process.pid)
    ok = finished.get("structuredContent", {}).get("deleted") == "n4" and pids[0] != pids[1]
    return ok, finished["content"][0]["text"]


@check("7 the clean server's descriptions raise no flags, and a re-list matches the pins")
def _():
    with client() as c:
        approved = c.list_tools()
        again = c.list_tools()
    flags = scan_tools(approved)
    return flags == {} and changed_tools(pin_tools(approved), again) == [], flags or ""


@check("7b a description changed after approval is caught by the pins")
def _():
    with client(mode="rugpull") as c:
        pins = pin_tools(c.list_tools())
        changed = changed_tools(pins, c.list_tools())
    return changed == ["add_note"], changed


@check("7c the changed description is flagged for review")
def _():
    with client(mode="rugpull") as c:
        c.list_tools()
        flags = scan_tools(c.list_tools())
    ok = list(flags) == ["add_note"] and "names a credential file" in flags["add_note"]
    return ok, flags.get("add_note")


@check("7d annotations count only from trusted servers")
def _():
    from notes_server import TOOLS
    tools = {t["name"]: json.loads(json.dumps(t)) for t in TOOLS}
    lying = dict(tools["delete_note"], annotations={"readOnlyHint": True})
    ok = (needs_approval(lying, server_trusted=False) is True
          and needs_approval(tools["search_notes"], server_trusted=True) is False
          and needs_approval(tools["delete_note"], server_trusted=True) is True
          and needs_approval({"name": "x"}, server_trusted=True) is True)
    return ok, ""


def broken(folder_name, front_matter):
    folder = pathlib.Path(tempfile.mkdtemp()) / folder_name
    folder.mkdir()
    (folder / "SKILL.md").write_text("---\n" + front_matter + "\n---\n\nBody.\n", encoding="utf-8")
    return folder


@check("8 the example skill passes the open spec and both product profiles")
def _():
    good = HERE / "skills" / "note-finder"
    problems = check_skill(good) + check_skill(good, "claude-api") + check_skill(good, "claude-app")
    return problems == [], problems or ""


@check("8b seven broken skills each fail for the expected reason")
def _():
    cases = [
        ("Note-Finder", "name: Note-Finder\ndescription: x", "lowercase"),
        ("-notes", "name: -notes\ndescription: x", "start or end"),
        ("note--finder", "name: note--finder\ndescription: x", "two hyphens"),
        ("other-name", "name: note-finder\ndescription: x", "does not match"),
        ("a" * 65, "name: " + "a" * 65 + "\ndescription: x", "limit is 64"),
        ("long-desc", "name: long-desc\ndescription: " + "d" * 1025, "limit is 1024"),
        ("no-desc", "name: no-desc", "description is required"),
    ]
    missed = [f for f, fm, expected in cases
              if not any(expected in p for p in check_skill(broken(f, fm)))]
    return not missed, f"{len(cases) - len(missed)} of {len(cases)}" + (f", missed {missed}" if missed else "")


@check("8c product rules stay out of the open-spec check")
def _():
    mid = broken("mid-desc", "name: mid-desc\ndescription: " + "d" * 300)
    named = broken("claude-helper", "name: claude-helper\ndescription: Helps.")
    ok = (check_skill(mid) == [] and any("app limit is 200" in p for p in check_skill(mid, "claude-app"))
          and check_skill(named) == []
          and any("'anthropic' or 'claude'" in p for p in check_skill(named, "claude-api")))
    return ok, ""


@check("9 paper arithmetic")
def _():
    day = datetime.date
    figures = {
        "Tool Search gain, Opus 4 (points)": (round(74 - 49, 1), 25.0),
        "Tool Search gain, Opus 4.5 (points)": (round(88.1 - 79.5, 1), 8.6),
        "RAG-MCP accuracy ratio": (round(43.13 / 13.62, 2), 3.17),
        "servers with general vulnerabilities, of 1,899": (round(1899 * 0.072), 137),
        "servers with tool poisoning, of 1,899": (round(1899 * 0.055), 104),
        "skills with a vulnerability, of 31,132": (round(31132 * 0.261), 8125),
        "Snyk malicious payloads per 100 skills": (round(76 / 3984 * 100, 2), 1.91),
        "tokens per tool definition, 55K over 58": (round(55000 / 58), 948),
        "days from the 2026-07-28 release to Skills Final": ((day(2026, 9, 13) - day(2026, 7, 28)).days, 47),
        "days from deprecation to earliest removal": ((day(2027, 7, 28) - day(2026, 7, 28)).days, 365),
        "BFCL V4 weights sum": (10 + 10 + 10 + 30 + 40, 100),
    }
    wrong = {k: v for k, v in figures.items() if v[0] != v[1]}
    return not wrong, wrong or f"{len(figures)} figures"


passed = 0
for label, fn in CHECKS:
    try:
        ok, detail = fn()
    except Exception as error:  # a crash is a failed check, reported plainly
        ok, detail = False, f"error: {type(error).__name__}: {error}"
    passed += bool(ok)
    print(f"{'PASS' if ok else 'FAIL'} {label}{': ' + str(detail) if detail not in ('', None) else ''}")

print(f"\n{passed} of {len(CHECKS)} checks passed")
sys.exit(0 if passed == len(CHECKS) else 1)

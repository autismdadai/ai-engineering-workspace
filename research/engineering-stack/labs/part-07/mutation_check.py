"""Prove the checks can fail: break the lab on purpose, one change at a time,
in a temporary copy, and confirm run_lab.py notices each break.
Run: python mutation_check.py
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
FILES = ["notes_server.py", "mcp_client.py", "guard.py", "skill_check.py", "run_lab.py"]

# (description, file, original text, broken text)
MUTATIONS = [
    ("discover forgets supportedVersions", "notes_server.py",
     '"supportedVersions": [PROTOCOL_VERSION],', '"versions": [PROTOCOL_VERSION],'),
    ("tool order changes between calls", "notes_server.py",
     "        self.list_calls += 1\n        return tools",
     "        self.list_calls += 1\n        return tools[::-1] if self.list_calls % 2 == 0 else tools"),
    ("server accepts requests without _meta", "notes_server.py",
     '        meta = params.get("_meta")\n        if not isinstance(meta, dict) or \\',
     '        meta = params.get("_meta") or {"io.modelcontextprotocol/protocolVersion": PROTOCOL_VERSION,'
     ' "io.modelcontextprotocol/clientCapabilities": {}}\n        if not isinstance(meta, dict) or \\'),
    ("server ignores the protocol version", "notes_server.py",
     "        if version != PROTOCOL_VERSION:", "        if False:"),
    ("server logs to stdout", "notes_server.py",
     'print(f"[notes-server] {message}", file=sys.stderr, flush=True)',
     'print(f"[notes-server] {message}", flush=True)'),
    ("bad arguments become a protocol error", "notes_server.py",
     '            return self.tool_result(f"Invalid arguments: {problem}", is_error=True)',
     '            raise ProtocolError(INVALID_PARAMS, f"Invalid arguments: {problem}")'),
    ("unknown tool becomes an isError result", "notes_server.py",
     '            raise ProtocolError(INVALID_PARAMS, f"Unknown tool: {name}")',
     '            return self.tool_result(f"Unknown tool: {name}", is_error=True)'),
    ("delete happens without asking", "notes_server.py",
     "        if responses is None and state is None:", "        if False:"),
    ("client retries with the same id", "mcp_client.py",
     "        self.next_id += 1\n", ""),
    ("a declined delete still deletes", "notes_server.py",
     'if answer["action"] == "accept" and (answer.get("content") or {}).get("confirm") is True:',
     "if True:"),
    ("state signature not checked", "notes_server.py",
     "    if not hmac.compare_digest(tag, expected):", "    if False:"),
    ("state not bound to the call", "notes_server.py",
     '    if payload["tool"] != tool or payload["args"] != digest:', '    if payload["tool"] != tool:'),
    ("server asks a client that cannot answer", "notes_server.py",
     '            if "elicitation" not in capabilities:', "            if False:"),
    ("each process signs state with its own random key", "notes_server.py",
     'return os.environ.get("NOTES_STATE_KEY", "lab-only-secret").encode()',
     'return str(os.getpid()).encode()'),
    ("fingerprint covers only the name", "guard.py",
     '    canonical = json.dumps(tool, sort_keys=True, separators=(",", ":"), ensure_ascii=False)',
     '    canonical = tool["name"]'),
    ("annotations trusted from any server", "guard.py",
     "    if not server_trusted:\n        return True\n", ""),
    ("scanner misses credential files", "guard.py",
     '    (r"(~|\\$home|/home/\\w+)/\\.(ssh|aws|config)\\b|id_rsa|\\.env\\b", "names a credential file"),\n', ""),
    ("skill name need not match its folder", "skill_check.py",
     "        if name != folder.name:", "        if False:"),
    ("open spec uses the app's 200-character limit", "skill_check.py",
     "    elif len(description) > DESCRIPTION_MAX:", "    elif len(description) > APP_DESCRIPTION_MAX:"),
    ("double hyphens allowed in names", "skill_check.py",
     '        if "--" in name:', "        if False:"),
]


def run(folder):
    return subprocess.run([sys.executable, "run_lab.py"], cwd=folder, capture_output=True,
                          text=True, timeout=180)


def copy_lab():
    folder = pathlib.Path(tempfile.mkdtemp())
    for name in FILES + ["demo.py"]:
        shutil.copy(HERE / name, folder / name)
    shutil.copytree(HERE / "skills", folder / "skills")
    return folder


control = run(copy_lab())
if control.returncode != 0:
    print("FAIL the unbroken copy does not pass; fix the lab first")
    print(control.stdout[-2000:])
    sys.exit(1)
print("OK   the unbroken copy passes")

caught = 0
for description, filename, original, broken in MUTATIONS:
    folder = copy_lab()
    path = folder / filename
    text = path.read_text(encoding="utf-8")
    if text.count(original) != 1:
        print(f"ERROR {description}: the text to change was found {text.count(original)} times")
        continue
    path.write_text(text.replace(original, broken), encoding="utf-8")
    result = run(folder)
    failed = [line for line in result.stdout.splitlines() if line.startswith("FAIL")]
    crashed = result.returncode != 0 and not failed
    if result.returncode != 0:
        caught += 1
        first = failed[0] if failed else "crashed: " + (result.stderr.strip().splitlines() or ["?"])[-1]
        print(f"CAUGHT {description}: {first[:110]}")
    else:
        print(f"MISSED {description}")
    shutil.rmtree(folder, ignore_errors=True)

print(f"\n{caught} of {len(MUTATIONS)} mutations caught")
sys.exit(0 if caught == len(MUTATIONS) else 1)

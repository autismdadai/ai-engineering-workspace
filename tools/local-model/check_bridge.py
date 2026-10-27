"""Checks the local-model bridge, then times real jobs on the local model.

Part 1 (offline) starts the bridge against a stand-in Ollama on this computer
and checks the handshakes, the tool list and the refusals. No model needed.
Part 2 (live) checks that Ollama is up, then runs three sample jobs on the
real model and prints each answer with Ollama's own timings and a score.

    python check_bridge.py              # both parts
    python check_bridge.py --offline    # part 1 only
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER = HERE / "local_model_server.py"
WORKSPACE = HERE.parents[1]
LIVE_HOST = "http://127.0.0.1:11434"
LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))
NEW_META = {"_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28",
                      "io.modelcontextprotocol/clientCapabilities": {}}}


class Bridge:
    """Starts the bridge as a child process and talks to it one JSON line at a time."""

    def __init__(self, **settings):
        env = dict(os.environ)
        env.update(settings)
        self.errors = tempfile.TemporaryFile()
        self.process = subprocess.Popen([sys.executable, str(SERVER)], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=self.errors, env=env)
        self.last_id = 0
        self.last_line = b""

    def write(self, message):
        self.process.stdin.write(json.dumps(message).encode() + b"\n")
        self.process.stdin.flush()

    def request(self, method, params=None):
        self.last_id += 1
        message = {"jsonrpc": "2.0", "id": self.last_id, "method": method}
        if params is not None:
            message["params"] = params
        self.write(message)
        self.last_line = self.process.stdout.readline()
        if not self.last_line:
            raise RuntimeError("the bridge closed. Its log:\n" + self.close())
        reply = json.loads(self.last_line)
        if reply.get("id") != self.last_id:
            raise RuntimeError(f"reply id {reply.get('id')} doesn't match request {self.last_id}")
        return reply

    def call(self, arguments, name="ask_local_model"):
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def close(self):
        self.process.stdin.close()
        self.process.wait(timeout=10)
        self.errors.seek(0)
        return self.errors.read().decode("utf-8", errors="replace")


class StandIn(BaseHTTPRequestHandler):
    """A fake Ollama with a fixed answer, for the offline checks."""
    received = []

    def do_GET(self):
        self._send({"version": "stand-in"})

    def do_POST(self):
        StandIn.received.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        self._send({"message": {"role": "assistant", "content": "<think>hidden</think>Stand-in answer."},
                    "done_reason": "stop",
                    "prompt_eval_count": 120, "prompt_eval_duration": 1_000_000_000,
                    "eval_count": 16, "eval_duration": 2_000_000_000,
                    "load_duration": 500_000_000, "total_duration": 3_600_000_000})

    def _send(self, body):
        data = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def text_of(result):
    return result["content"][0]["text"]


def offline_checks():
    stand_in = HTTPServer(("127.0.0.1", 0), StandIn)
    threading.Thread(target=stand_in.serve_forever, daemon=True).start()
    host = f"http://127.0.0.1:{stand_in.server_port}"
    results = []

    def check(label, ok):
        results.append(bool(ok))
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")

    client = {"capabilities": {}, "clientInfo": {"name": "check_bridge", "version": "0"}}
    bridge = Bridge(LOCAL_MODEL_HOST=host)
    try:
        r = bridge.request("initialize", {"protocolVersion": "2025-06-18", **client})["result"]
        check("classic handshake: echoes 2025-06-18 and offers tools",
              r["protocolVersion"] == "2025-06-18" and "tools" in r["capabilities"]
              and r["serverInfo"]["name"] == "local-model")
        check("replies end with a bare newline, not \\r\\n",
              bridge.last_line.endswith(b"\n") and not bridge.last_line.endswith(b"\r\n"))
        r = bridge.request("initialize", {"protocolVersion": "2099-01-01", **client})["result"]
        check("an unknown revision gets one the bridge supports", r["protocolVersion"] == "2025-11-25")
        bridge.write({"jsonrpc": "2.0", "method": "notifications/initialized"})
        check("a notification gets no reply (the next line answers the ping)",
              bridge.request("ping").get("result") == {})
        r = bridge.request("server/discover", NEW_META)["result"]
        check("2026-07-28 discover: lists the revision and marks the result complete",
              "2026-07-28" in r["supportedVersions"] and r["resultType"] == "complete")
        tools = bridge.request("tools/list")["result"]["tools"]
        check("tools/list: exactly one read-only tool, ask_local_model",
              [t["name"] for t in tools] == ["ask_local_model"]
              and tools[0]["annotations"]["readOnlyHint"] is True)

        r = bridge.call({"prompt": "Say hello."})["result"]
        check("a job returns the answer, <think> removed, with an 'unchecked draft' footer",
              not r["isError"] and text_of(r).startswith("Stand-in answer.")
              and "hidden" not in text_of(r) and "unchecked draft" in text_of(r))
        sent = StandIn.received[-1]
        check("the request turns thinking off and sets the window and the answer limit",
              sent.get("think") is False and sent.get("options") == {"num_predict": 300, "num_ctx": 8192}
              and sent["messages"][0]["role"] == "system")
        check("Ollama's timings come back in the result's _meta",
              r.get("_meta", {}).get("local-model/stats", {}).get("answer_tokens") == 16)
        r = bridge.request("tools/call", {"name": "ask_local_model", "arguments": {"prompt": "Hi"}, **NEW_META})
        check("a 2026-07-28 tool call is marked complete",
              r["result"]["resultType"] == "complete" and not r["result"]["isError"])
        r = bridge.call({"prompt": "Summarize.", "file_path": "README.md"})["result"]
        user = StandIn.received[-1]["messages"][1]["content"]
        readme = (WORKSPACE / "README.md").read_bytes().decode("utf-8")
        check("the bridge reads a workspace file itself and wraps it in <file> tags",
              not r["isError"] and '<file name="README.md">' in user and readme in user)

        reached = len(StandIn.received)
        r = bridge.call({"prompt": "Read it.", "file_path": "../outside.txt"})["result"]
        check("a relative path leading outside the workspace is refused",
              r["isError"] and "outside the workspace" in text_of(r))
        r = bridge.call({"prompt": "Read it.", "file_path": str(WORKSPACE.parent / "outside.txt")})["result"]
        check("an absolute path outside the workspace is refused",
              r["isError"] and "outside the workspace" in text_of(r))
        r = bridge.call({"prompt": "Read it.", "file_path": "no/such/file.txt"})["result"]
        check("a missing file is reported", r["isError"] and "No file" in text_of(r))
        r = bridge.call({"prompt": "Hi", "max_tokens": 5000})["result"]
        check("max_tokens above 800 is refused", r["isError"] and "max_tokens" in text_of(r))
        r = bridge.call({"prompt": "Hi", "model": "other"})["result"]
        check("an unexpected argument is refused", r["isError"] and "unexpected argument" in text_of(r))
        r = bridge.call({"prompt": "Hi"}, name="delete_everything")
        check("an unknown tool is a protocol error", r.get("error", {}).get("code") == -32602)
        check("refused jobs never reached Ollama", len(StandIn.received) == reached)
    finally:
        bridge.close()

    small = Bridge(LOCAL_MODEL_HOST=host, LOCAL_MODEL_CTX="1024")
    try:
        r = small.call({"prompt": "Summarize.", "file_path": "README.md"})["result"]
        check("a file too big for the window is refused, not cut",
              r["isError"] and "window" in text_of(r) and len(StandIn.received) == reached)
    finally:
        small.close()

    remote = Bridge(LOCAL_MODEL_HOST="http://example.com:11434")
    try:
        r = remote.call({"prompt": "Hi"})["result"]
        check("a host off this computer is refused", r["isError"] and "not on this computer" in text_of(r))
    finally:
        remote.close()

    down = Bridge(LOCAL_MODEL_HOST="http://127.0.0.1:9")
    try:
        r = down.call({"prompt": "Hi"})["result"]
        check("Ollama not running gives a clear message", r["isError"] and "Can't reach Ollama" in text_of(r))
    finally:
        down.close()

    stand_in.shutdown()
    stand_in.server_close()
    print(f"{sum(results)} of {len(results)} offline checks passed")
    return all(results)


# ----- live jobs -----

# Invented notes about this workspace [I]; each has one right tag.
NOTES = [
    ("Ollama 0.40.6 runs qwen3:1.7b at about 8 tokens per second.", "local-models"),
    ("Keep core.autocrlf false so the shell scripts keep LF line endings.", "git"),
    ("Venus found two papers on persona prompting.", "council"),
    ("Skill descriptions on claude.ai must be 200 characters or fewer.", "limits"),
    ("The GitHub copy needs a push after each commit.", "git"),
    ("Planet X checks claims against primary sources.", "council"),
    ("The weekly usage limit resets on October 26.", "limits"),
    ("llama.cpp ran Qwen3-4B at 3.93 tokens per second on the processor.", "local-models"),
]
DATE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)"
                  r" \d{1,2}(?:, \d{4})?")
VERSION = re.compile(r"\bv\d+(?:\.\d+)*\b|\b\d+\.\d+\.\d+\b")
BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")


def score_tags(answer):
    got = dict(re.findall(r"(\d+)\s*[:.)-]\s*([a-z-]+)", answer.lower()))
    right = sum(got.get(str(n)) == tag for n, (_, tag) in enumerate(NOTES, 1))
    return f"{right} of {len(NOTES)} tags right"


def score_bullets(answer):
    bullets = [line for line in answer.splitlines() if BULLET.match(line)]
    return f"{len(bullets)} bullet lines (asked for 3); content graded by hand"


def score_extraction(answer):
    source = (WORKSPACE / "README.md").read_bytes().decode("utf-8")
    dates, versions = sorted(set(DATE.findall(source))), sorted(set(VERSION.findall(source)))
    lines = [BULLET.sub("", line).strip(" `*\"'") for line in answer.splitlines() if line.strip()]
    found_dates = [d for d in dates if d in answer]
    found_versions = [v for v in versions if re.search(rf"(?<![\w.]){re.escape(v)}(?![\w.])", answer)]
    not_in_file = [line for line in lines if line not in source]
    return (f"dates {len(found_dates)} of {len(dates)} {dates}; versions {len(found_versions)} of "
            f"{len(versions)} {versions}; lines not found in the file: {len(not_in_file)} {not_in_file}")


JOBS = [
    {"label": "Tag 8 notes",
     "arguments": {"prompt": "Tag each note with exactly one of these tags: local-models, git, council, limits. "
                             "Answer with one line per note in the form 'number: tag' and nothing else.\n\n"
                             + "\n".join(f"{n}. {note}" for n, (note, _) in enumerate(NOTES, 1)),
                   "max_tokens": 120},
     "score": score_tags},
    {"label": "Summarize Part 07's README in 3 bullets",
     "arguments": {"prompt": "Summarize this file in exactly 3 short bullet points.",
                   "file_path": "research/engineering-stack/labs/part-07/README.md", "max_tokens": 200},
     "score": score_bullets},
    {"label": "List the dates and versions in README.md",
     "arguments": {"prompt": "List every date and every version number in this file, one per line, copied "
                             "exactly as written. A version number looks like v2 or 4.0.1. List nothing else.",
                   "file_path": "README.md", "max_tokens": 200},
     "score": score_extraction},
]


def get_json(path):
    with LOCAL.open(LIVE_HOST + path, timeout=10) as response:
        return json.load(response)


def rate(tokens, seconds):
    return tokens / seconds if seconds > 0 else 0.0


def live_jobs():
    model = os.environ.get("LOCAL_MODEL", "qwen3:1.7b")
    try:
        version = get_json("/api/version")["version"]
        models = [m["name"] for m in get_json("/api/tags")["models"]]
    except OSError as error:
        print(f"Can't reach Ollama at {LIVE_HOST}: is the Ollama app running? ({getattr(error, 'reason', error)})")
        return False
    print(f"Ollama {version}; models: {', '.join(models)}")
    if model not in models:
        print(f"{model} isn't in Ollama's list.")
        return False

    rows = []
    bridge = Bridge(LOCAL_MODEL_HOST=LIVE_HOST)
    try:
        for number, job in enumerate(JOBS, 1):
            print(f"\nJob {number}: {job['label']}")
            r = bridge.call(job["arguments"])["result"]
            if r["isError"]:
                print("  error: " + text_of(r))
                return False
            answer, _, foot = text_of(r).partition("\n\n---\n")
            for line in answer.splitlines():
                print("  | " + line)
            print("  " + foot)
            score = job["score"](answer)
            print("  score: " + score)
            rows.append((job["label"], r["_meta"]["local-model/stats"], score))
    finally:
        log = bridge.close()

    print("\n| Job | Read: tokens, s, per s | Wrote: tokens, s, per s | Load s | Total s | Stop |")
    print("|---|---|---|---|---|---|")
    for label, s, _ in rows:
        print(f"| {label} | {s['read_tokens']}, {s['read_seconds']:.1f}, {rate(s['read_tokens'], s['read_seconds']):.0f} "
              f"| {s['answer_tokens']}, {s['answer_seconds']:.1f}, {rate(s['answer_tokens'], s['answer_seconds']):.1f} "
              f"| {s['load_seconds']:.1f} | {s['wall_seconds']:.1f} | {s['done_reason']} |")
    print("\nBridge log:\n" + log)
    return True


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--offline", action="store_true", help="run part 1 only")
    args = parser.parse_args()
    print("Part 1: offline checks against a stand-in Ollama")
    ok = offline_checks()
    if args.offline or not ok:
        return 0 if ok else 1
    print("\nPart 2: live jobs on the local model")
    return 0 if live_jobs() else 1


if __name__ == "__main__":
    sys.exit(main())

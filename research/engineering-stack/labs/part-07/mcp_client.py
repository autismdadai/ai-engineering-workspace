"""A small MCP client over stdio, standard library only (revision 2026-07-28).

It starts a server as a subprocess, writes one JSON-RPC message per line to its
stdin and reads one per line from its stdout. Every request carries the _meta
envelope, because the 2026-07-28 revision has no initialize handshake.
"""
import json
import subprocess
import sys
import threading

PROTOCOL_VERSION = "2026-07-28"
CLIENT_INFO = {"name": "lab-client", "version": "0.7.0"}


class RpcError(Exception):
    def __init__(self, error):
        super().__init__(f"{error['code']}: {error['message']}")
        self.code = error["code"]
        self.message = error["message"]
        self.data = error.get("data")


class StdioClient:
    def __init__(self, command, env=None, capabilities=None, version=PROTOCOL_VERSION):
        self.process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", env=env, bufsize=1)
        self.capabilities = {} if capabilities is None else capabilities
        self.version = version
        self.next_id = 1
        self.sent = []       # every message written, for the transcript
        self.received = []   # every line read, exactly as the server wrote it
        self.stderr_lines = []
        self._reader = threading.Thread(target=self._drain_stderr, daemon=True)
        self._reader.start()

    def _drain_stderr(self):
        for line in self.process.stderr:
            self.stderr_lines.append(line.rstrip("\n"))

    def meta(self):
        return {
            "io.modelcontextprotocol/protocolVersion": self.version,
            "io.modelcontextprotocol/clientCapabilities": self.capabilities,
            "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
        }

    def send_raw(self, message):
        """Write one message and return the parsed reply (no envelope added)."""
        line = json.dumps(message, separators=(",", ":"))
        assert "\n" not in line  # stdio messages must not contain newlines
        self.sent.append(message)
        self.process.stdin.write(line + "\n")
        self.process.stdin.flush()
        reply_line = self.process.stdout.readline()
        if not reply_line:
            raise ConnectionError("server closed stdout")
        self.received.append(reply_line.rstrip("\n"))
        return json.loads(reply_line)

    def request(self, method, params=None, meta=True):
        params = dict(params or {})
        if meta:
            params["_meta"] = self.meta()
        rid = self.next_id
        self.next_id += 1
        reply = self.send_raw({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        if reply.get("id") != rid:
            raise ValueError(f"reply id {reply.get('id')} does not match request id {rid}")
        if "error" in reply:
            raise RpcError(reply["error"])
        result = reply["result"]
        result.setdefault("resultType", "complete")  # older servers omit it
        return result

    def discover(self):
        return self.request("server/discover")

    def list_tools(self):
        return self.request("tools/list")["tools"]

    def call_tool(self, name, arguments, answer_input=None, max_rounds=3):
        """Call a tool, answering input_required rounds with answer_input.

        answer_input(input_requests) returns the inputResponses map. Each retry
        is a new request with a new id, and echoes requestState unchanged.
        """
        params = {"name": name, "arguments": arguments}
        for _ in range(max_rounds):
            result = self.request("tools/call", params)
            if result["resultType"] != "input_required":
                return result
            if answer_input is None:
                return result  # the caller handles it
            retry = {"name": name, "arguments": arguments}
            if "inputRequests" in result:
                retry["inputResponses"] = answer_input(result["inputRequests"])
            if "requestState" in result:
                retry["requestState"] = result["requestState"]
            params = retry
        raise RuntimeError(f"still input_required after {max_rounds} rounds")

    def close(self):
        """Close stdin, then wait; terminate only if the server hangs (spec, stdio shutdown)."""
        if self.process.stdin:
            self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)
        self._reader.join(timeout=2)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def server_command(path="notes_server.py"):
    return [sys.executable, path]

"""stream_server: a stand-in model streamed over Server-Sent Events
(Engineering Stack, Part 13).

Standard library only. The "model" is invented [I]: it waits a little to
"read" the prompt, then sends the words of a fixed answer one at a time,
whatever the prompt says. What is real is everything around it: the SSE wire
format, the headers, keep-alive comments, an error after the HTTP 200, usage
and a final `done` event, stopping when the client goes away, a size limit,
checked fields, socket timeouts, a cap on clients, an optional API key, and
counts and timings kept without the prompt.

This is a teaching server for 127.0.0.1. It is not a production server:
Part 13, Section 3.1 lists what a public endpoint needs on top.

Run:  python stream_server.py            (listens on 127.0.0.1:8013)
Then: python sse_client.py "Tell me about streaming"
"""
from __future__ import annotations

import hmac
import json
import os
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import ssewire
from shipmath import chat_span
from tinytrace import Tracer

ANSWER = ("Streaming sends the answer in pieces as the model writes it, so the "
          "first words reach the reader long before the last ones exist.")
MAX_BODY = 64 * 1024           # refuse bigger requests before reading them
MAX_TOKENS = 512               # the server's cap; a client can ask for less, not more
MAX_CLIENTS = 32               # requests handled at once; the rest get 503
MAX_SECONDS = 120              # longest a stream may run
SOCKET_TIMEOUT = 30            # seconds a client may stall while sending or reading
REFUSE_SECONDS = 0.5           # how long a refused client gets to finish sending


class StandInModel:
    """Invented timings [I]: prefill grows with the prompt, then one word per step."""

    def __init__(self, prefill_per_char=0.0005, per_token=0.02, base=0.05):
        self.prefill_per_char, self.per_token, self.base = prefill_per_char, per_token, base

    def prefill_seconds(self, prompt: str) -> float:
        return self.base + self.prefill_per_char * len(prompt)

    def tokens(self, max_tokens: int):
        for i, word in enumerate(ANSWER.split(" ")):
            if i >= max_tokens:
                return
            time.sleep(self.per_token)
            yield word if i == 0 else " " + word


def whole_number(value, low: int, high: int) -> int:
    """A JSON whole number in [low, high]; rejects floats, strings and true/false."""
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"must be a whole number from {low} to {high}")
    return value


class Handler(BaseHTTPRequestHandler):
    server_version = "LabStream/1.0"
    timeout = SOCKET_TIMEOUT       # BaseHTTPRequestHandler applies it to the socket
    model = StandInModel()
    tracer = Tracer("stream-server")
    ping_seconds = 1.0
    api_key = os.environ.get("LAB_API_KEY")   # None: no key needed (local lab)
    stats = {"requests": 0, "stopped_early": 0, "tokens_sent": 0, "errors": 0}
    stats_lock = threading.Lock()

    def log_message(self, fmt, *args):         # the default logs every request to stderr
        pass

    def _reply(self, status, body: dict):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send(self, chunk: bytes):
        self.wfile.write(chunk)
        self.wfile.flush()

    def _authorized(self) -> bool:
        if self.api_key is None:
            return True
        scheme, _, given = self.headers.get("Authorization", "").partition(" ")
        return scheme.lower() == "bearer" and hmac.compare_digest(given.encode(),
                                                                  self.api_key.encode())

    def do_POST(self):
        if self.path != "/v1/stream":
            return self._reply(404, {"error": "not found"})
        if not self._authorized():
            return self._reply(401, {"error": "missing or wrong API key"})
        length = self.headers.get("Content-Length", "")
        if not length.isdigit() or not 0 < int(length) <= MAX_BODY:
            return self._reply(413, {"error": f"send a Content-Length of 1 to {MAX_BODY} bytes"})
        try:
            req = json.loads(self.rfile.read(int(length)))
            prompt = req["prompt"]
            if not isinstance(prompt, str):
                raise ValueError("prompt must be text")
            max_tokens = whole_number(req.get("max_tokens", MAX_TOKENS), 1, MAX_TOKENS)
            fail_after = req.get("fail_after")
            if fail_after is not None:
                fail_after = whole_number(fail_after, 0, MAX_TOKENS)
        except (ValueError, KeyError, TypeError, OverflowError, AttributeError):
            # Checked before the 200, so the client gets a clear status, not a broken stream.
            return self._reply(400, {"error": "send JSON with a text 'prompt'; max_tokens and "
                                              f"fail_after are whole numbers up to {MAX_TOKENS}"})

        with self.stats_lock:
            self.stats["requests"] += 1
        with self.tracer.span("POST /v1/stream", kind="SERVER",
                              traceparent=self.headers.get("traceparent")):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("X-Accel-Buffering", "no")   # ask nginx-style proxies not to buffer
            self.end_headers()
            sent, finish = 0, "stop"
            name, attrs = chat_span("standin", "standin-1", {}, [])
            with self.tracer.span(name, attrs, kind="CLIENT") as span:
                stop_at = time.monotonic() + MAX_SECONDS
                try:
                    # Keep-alive comments while the stand-in "reads" the prompt.
                    deadline = time.monotonic() + self.model.prefill_seconds(prompt)
                    while (left := deadline - time.monotonic()) > 0:
                        time.sleep(min(left, self.ping_seconds))
                        if deadline - time.monotonic() > 0:
                            self._send(ssewire.comment("ping"))
                    for i, piece in enumerate(self.model.tokens(max_tokens)):
                        if fail_after is not None and i >= fail_after:
                            # The status line said 200 long ago; the error goes in the stream.
                            finish = "error"
                            self._send(ssewire.encode(json.dumps(
                                {"type": "overloaded_error", "message": "stand-in overload"}),
                                event="error"))
                            break
                        if time.monotonic() > stop_at:
                            finish = "length"
                            break
                        self._send(ssewire.encode(json.dumps({"text": piece}),
                                                  event="token", id=str(i)))
                        sent += 1
                    else:
                        finish = "length" if sent >= max_tokens else "stop"
                    if finish != "error":
                        usage = {"input_tokens": len(prompt.split()), "output_tokens": sent}
                        self._send(ssewire.encode(json.dumps(usage), event="usage"))
                        self._send(ssewire.encode("[DONE]", event="done"))
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
                    finish = "client_gone"   # stop generating: nobody is reading
                    with self.stats_lock:
                        self.stats["stopped_early"] += 1
                except Exception as error:   # anything else: a short error event, no details
                    finish = "error"
                    with self.stats_lock:
                        self.stats["errors"] += 1
                    span["attributes"]["error.type"] = type(error).__name__
                    try:
                        self._send(ssewire.encode(json.dumps(
                            {"type": "server_error", "message": "the stream failed"}), event="error"))
                    except OSError:
                        pass
                span["attributes"].update({"gen_ai.usage.input_tokens": len(prompt.split()),
                                           "gen_ai.usage.output_tokens": sent,
                                           "gen_ai.response.finish_reasons": [finish]})
            with self.stats_lock:
                self.stats["tokens_sent"] += sent


class LabServer(ThreadingHTTPServer):
    """At most MAX_CLIENTS requests at once; the next ones get a quick 503."""
    daemon_threads = True
    request_queue_size = 64

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slots = threading.BoundedSemaphore(MAX_CLIENTS)

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            self.refuse(request)
            return
        super().process_request(request, client_address)

    def refuse(self, request):
        """Send 503, then read what the client sent before closing. Closing at once,
        with its request unread, lost the 503 on Windows in 13 of 20 tries."""
        try:
            request.sendall(b"HTTP/1.0 503 Service Unavailable\r\nContent-Length: 0\r\n\r\n")
            request.shutdown(socket.SHUT_WR)
            stop, got = time.monotonic() + REFUSE_SECONDS, 0
            while got <= MAX_BODY and (left := stop - time.monotonic()) > 0:
                request.settimeout(left)
                chunk = request.recv(4096)
                if not chunk:
                    break
                got += len(chunk)
        except OSError:
            pass
        self.shutdown_request(request)

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def handle_error(self, request, client_address):
        # The default prints the whole traceback, which can hold client text.
        print(f"request failed: {sys.exc_info()[0].__name__}", file=sys.stderr)


def serve(port: int = 8013, host: str = "127.0.0.1") -> LabServer:
    """Start in a background thread and return the server (port 0 picks a free one)."""
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("the lab server only listens on this computer")
    if Handler.api_key == "":
        raise ValueError("LAB_API_KEY is set but empty: set a key or unset it")
    httpd = LabServer((host, port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8013
    httpd = serve(port)
    print(f"Stand-in model streaming on http://127.0.0.1:{httpd.server_address[1]}/v1/stream"
          " (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        httpd.shutdown()

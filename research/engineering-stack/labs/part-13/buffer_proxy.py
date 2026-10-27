"""buffer_proxy: a reverse proxy that buffers responses, the way nginx does
by default (Engineering Stack, Part 13).

Standard library only. A simplified model [I], not nginx: it holds the
upstream's bytes until a 4,096-byte block fills or the response ends, unless
the upstream sent `X-Accel-Buffering: no` (nginx documents that header as a
per-response switch). With honour_header=False it buffers even then, like a
proxy that ignores the header. It shows why a stream can arrive all at once. Lab use on 127.0.0.1 only.
"""
from __future__ import annotations

import http.client
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BLOCK = 4096
MAX_BODY = 64 * 1024
SOCKET_TIMEOUT = 30


def make_handler(upstream_port: int, honour_header: bool):
    class Proxy(BaseHTTPRequestHandler):
        timeout = SOCKET_TIMEOUT

        def log_message(self, fmt, *args):
            pass

        def _refuse(self, status: int, message: str):
            data = message.encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            length = self.headers.get("Content-Length")
            if length is None:
                return self._refuse(411, "send a Content-Length")
            if not re.fullmatch(r"\d{1,9}", length.strip()):
                return self._refuse(400, "bad Content-Length")
            if int(length) > MAX_BODY:
                return self._refuse(413, "request too big")
            if not self.path.startswith("/"):
                return self._refuse(400, "bad path")
            body = self.rfile.read(int(length)) if int(length) else b""
            headers = {k: v for k, v in self.headers.items()
                       if k.lower() in ("content-type", "authorization", "traceparent")}
            headers["Host"] = "127.0.0.1"
            conn = http.client.HTTPConnection("127.0.0.1", upstream_port, timeout=60)
            try:
                conn.request("POST", self.path, body=body, headers=headers)
                resp = conn.getresponse()
            except OSError:
                conn.close()
                return self._refuse(502, "the upstream server did not answer")
            self.send_response(resp.status)
            for k, v in resp.getheaders():
                if k.lower() not in ("connection", "transfer-encoding", "content-length"):
                    self.send_header(k, v)
            self.end_headers()
            passthrough = honour_header and resp.getheader("X-Accel-Buffering", "").lower() == "no"
            held = b""
            try:
                while True:
                    chunk = resp.read1(BLOCK)
                    if not chunk:
                        break
                    if passthrough:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    else:
                        held += chunk
                        while len(held) >= BLOCK:
                            self.wfile.write(held[:BLOCK])
                            self.wfile.flush()
                            held = held[BLOCK:]
                if held:
                    self.wfile.write(held)
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, TimeoutError):
                pass
            finally:
                conn.close()
    return Proxy


def serve(upstream_port: int, honour_header: bool = True, port: int = 0) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), make_handler(upstream_port, honour_header))
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

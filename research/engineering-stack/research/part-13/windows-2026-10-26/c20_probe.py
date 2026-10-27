"""Probe Part 13's c20 failure on Windows, on a scratch copy of the lab.

Repeats c20's over-the-cap step: two silent clients fill MAX_CLIENTS = 2, a third
sends a request and reads the reply. Reports, per trial, whether the 503 arrived
and which error (if any) recv raised. Variant A is the lab folder given (the
October 20 lab lost the 503 in 13 of 20 tries; the fixed lab in 0 of 20); variant B
patches the server to close gently (send 503, shut the write side, read what the
client sent until it closes, then close), which avoids a TCP reset.
Usage: python -B c20_probe.py <scratch lab folder> [trials]
"""
import socket
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
LAB = sys.argv[1]
TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
sys.path.insert(0, LAB)
import stream_server as srv  # noqa: E402

REQUEST = b"POST /v1/stream HTTP/1.1\r\nHost: x\r\n\r\n"


def raw(port, data, wait=3.0):
    out, err = b"", None
    with socket.create_connection(("127.0.0.1", port), timeout=wait) as s:
        s.sendall(data)
        try:
            while chunk := s.recv(4096):
                out += chunk
        except OSError as e:
            err = f"{type(e).__name__} {getattr(e, 'winerror', None) or e.errno}"
    return out, err


def gentle_process_request(self, request, client_address):
    if not self.slots.acquire(blocking=False):
        try:
            request.sendall(b"HTTP/1.0 503 Service Unavailable\r\nContent-Length: 0\r\n\r\n")
            request.shutdown(socket.SHUT_WR)
            request.settimeout(0.5)
            while request.recv(4096):
                pass
        except OSError:
            pass
        self.shutdown_request(request)
        return
    super(srv.LabServer, self).process_request(request, client_address)


def run(label):
    h = srv.Handler
    old_timeout, old_cap = h.timeout, srv.MAX_CLIENTS
    h.timeout, srv.MAX_CLIENTS = 0.5, 2
    small = srv.serve(0)
    got, errors = 0, {}
    try:
        port = small.server_address[1]
        for _ in range(TRIALS):
            idle = [socket.create_connection(("127.0.0.1", port)) for _ in range(2)]
            time.sleep(0.1)
            out, err = raw(port, REQUEST)
            got += out.startswith(b"HTTP/1.0 503")
            errors[err] = errors.get(err, 0) + 1
            for s in idle:
                s.close()
            time.sleep(0.3)
    finally:
        small.shutdown()
        small.server_close()
        h.timeout, srv.MAX_CLIENTS = old_timeout, old_cap
    print(f"{label}: 503 received in {got} of {TRIALS}; recv errors {errors}")


print(f"Python {sys.version.split()[0]} on {sys.platform}")
run("A the lab as given")
srv.LabServer.process_request = gentle_process_request
run("B gentle close")

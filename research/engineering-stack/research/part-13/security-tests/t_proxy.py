import sys, os, socket, time, threading, json, io, contextlib
sys.path.insert(0, "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13")
import stream_server, buffer_proxy
connects = []
_c = socket.socket.connect
def rec(self, addr):
    connects.append(addr); return _c(self, addr)
socket.socket.connect = rec
up = stream_server.serve(0); UP = up.server_address[1]
px = buffer_proxy.serve(UP); PX = px.server_address[1]

def raw(req, port=None, wait=4.0, close_write=True):
    s = socket.create_connection(("127.0.0.1", port or PX), timeout=wait)
    s.sendall(req)
    if close_write: s.shutdown(socket.SHUT_WR)
    out = b""
    try:
        while (d := s.recv(65536)): out += d
    except socket.timeout: out += b"<<timeout>>"
    except ConnectionResetError: out += b"<<reset>>"
    s.close(); return out
body = json.dumps({"prompt": "x", "max_tokens": 1}).encode()
t = sys.argv[1]
err = io.StringIO()
with contextlib.redirect_stderr(err):
    if t == "cl":
        for label, cl in [("not a number", b"abc"), ("negative, body then EOF", b"-1")]:
            r = raw(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: " + cl + b"\r\n\r\n" + body)
            print(f"{label:24} -> {r.split(b'\r\n')[0][:60]!r}")
        # negative length, client keeps socket open: proxy reads to EOF and never answers
        before = threading.active_count()
        s = socket.create_connection(("127.0.0.1", PX)); s.sendall(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: -1\r\n\r\n" + body)
        time.sleep(4); print(f"Content-Length -1, socket open 4 s: threads {before} -> {threading.active_count()}, upstream connects so far {sum(1 for a in connects if a[1]==UP)}")
        s.close()
    elif t == "bigbody":
        import tracemalloc; tracemalloc.start()
        big = b"x" * (8 * 1024 * 1024)
        r = raw(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: %d\r\n\r\n" % len(big) + big, wait=10)
        print("8 MiB body through proxy ->", r.split(b"\r\n")[0][:60], "| proxy peak traced memory %.1f MiB" % (tracemalloc.get_traced_memory()[1]/2**20))
    elif t == "updown":
        up.shutdown(); up.server_close(); time.sleep(0.2)
        r = raw(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: %d\r\n\r\n" % len(body) + body)
        print("upstream down ->", r[:60] or b"(empty: no 502, connection closed)")
    elif t == "headers":
        up_seen = {}
        orig = stream_server.Handler.do_POST
        def spy(self):
            up_seen["path"] = self.path; up_seen["headers"] = dict(self.headers.items()); return orig(self)
        stream_server.Handler.do_POST = spy
        req = (b"POST http://attacker.example/v1/stream HTTP/1.1\r\nHost: attacker.example\r\n"
               b"Authorization: Bearer k\r\nCookie: session=abc\r\nX-Forwarded-For: 1.2.3.4\r\n"
               b"traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01\r\n"
               b"Content-Length: %d\r\n\r\n" % len(body) + body)
        r = raw(req)
        print("client status:", r.split(b"\r\n")[0])
        print("upstream saw path:", up_seen.get("path"))
        print("upstream saw headers:", up_seen.get("headers"))
        print("all outbound connects:", sorted(set(connects)))
        r = raw(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: %d\r\n\r\n" % len(body) + body)
        print("response headers to client:", [l for l in r.split(b"\r\n\r\n")[0].split(b"\r\n")[1:]])
    elif t == "slow":
        before = threading.active_count(); socks = []
        for i in range(30):
            s = socket.create_connection(("127.0.0.1", PX)); s.sendall(b"POST /v1/stream HTTP/1.1\r\n"); socks.append(s)
        time.sleep(6); print(f"30 unfinished requests to the proxy: threads {before} -> {threading.active_count()} after 6 s")
        [s.close() for s in socks]
lines = [l for l in err.getvalue().splitlines() if "Error" in l or "Exception" in l]
print("proxy stderr errors:", sorted(set(lines))[:4])

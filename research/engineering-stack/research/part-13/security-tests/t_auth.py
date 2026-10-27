import sys, os, socket, json
sys.path.insert(0, "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13")
import stream_server
httpd = stream_server.serve(0); PORT = httpd.server_address[1]
print("LAB_API_KEY =", repr(os.environ.get("LAB_API_KEY")), "| Handler.api_key =", repr(stream_server.Handler.api_key))
body = json.dumps({"prompt": "x", "max_tokens": 1}).encode()
def go(auth):
    s = socket.create_connection(("127.0.0.1", PORT), timeout=5)
    h = b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Length: %d\r\n" % len(body)
    if auth is not None: h += b"Authorization: " + auth + b"\r\n"
    s.sendall(h + b"\r\n" + body); s.shutdown(socket.SHUT_WR)
    out = b""
    while (d := s.recv(65536)): out += d
    return out.split(b"\r\n")[0].decode()
for a in [None, b"", b"Bearer", b"Bearer ", b"Bearer wrong", b"Bearer s3cret", b"bearer s3cret", b"Bearer s3cret ", b"Bearer \xff"]:
    print(f"Authorization {a!r:22} -> {go(a)}")
httpd.shutdown()

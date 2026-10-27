import sys, os, socket, time, threading, json, io, contextlib
LAB = "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13"
sys.path.insert(0, LAB)
import stream_server

if os.environ.get("QSIZE"): stream_server.ThreadingHTTPServer.request_queue_size = int(os.environ["QSIZE"])
httpd = stream_server.serve(0)
PORT = httpd.server_address[1]

def raw(req: bytes, wait=3.0, close_write=False):
    s = socket.create_connection(("127.0.0.1", PORT), timeout=wait)
    s.sendall(req)
    if close_write: s.shutdown(socket.SHUT_WR)
    out = b""
    try:
        while True:
            d = s.recv(65536)
            if not d: break
            out += d
    except socket.timeout:
        out += b"<<timeout, connection still open>>"
    s.close()
    return out

def post(body: bytes, extra=b"", cl=None):
    cl = str(len(body)).encode() if cl is None else cl
    h = b"POST /v1/stream HTTP/1.1\r\nHost: x\r\nContent-Type: application/json\r\n"
    if cl != b"NONE": h += b"Content-Length: " + cl + b"\r\n"
    return h + extra + b"\r\n" + body

test = sys.argv[1]
if test == "cl":
    good = json.dumps({"prompt": "hi", "max_tokens": 1}).encode()
    for label, cl in [("missing", b"NONE"), ("negative", b"-5"), ("zero", b"0"), ("huge", b"99999999999999999999999"),
                      ("not a number", b"abc"), ("underscore 1_7", b"1_7"), ("over 64 KB", b"65537")]:
        r = raw(post(good, cl=cl), close_write=True)
        print(f"{label:16} -> {r.split(b'\r\n')[0].decode()}  {r.split(b'\r\n\r\n',1)[-1][:60]!r}")
elif test == "short_body":
    # Content-Length says 100, body has 10 bytes, client keeps the socket open
    before = threading.active_count()
    socks = []
    for i in range(5):
        s = socket.create_connection(("127.0.0.1", PORT))
        s.sendall(post(b'{"prompt":', cl=b"100"))
        socks.append(s)
    time.sleep(5)
    print("threads before", before, "after 5 s with 5 short-body clients", threading.active_count())
    for s in socks: s.close()
    time.sleep(1)
    print("threads after the clients closed", threading.active_count())
elif test == "slowloris":
    before = threading.active_count()
    socks = []
    for i in range(40):
        s = socket.create_connection(("127.0.0.1", PORT))
        s.sendall(b"POST /v1/stream HTTP/1.1\r\nHost: x\r\n")   # headers never finished
        socks.append(s)
    for t in (2, 10):
        time.sleep(t if t == 2 else 8)
        print(f"after {t} s: threads {threading.active_count()} (before {before}); "
              f"server still answers: {b'200 OK' in raw(post(json.dumps({'prompt':'x','max_tokens':1}).encode()), close_write=True)}")
    for s in socks: s.close()
    time.sleep(1)
    print("after the 40 clients closed: threads", threading.active_count())
elif test == "overflow":
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        r = raw(post(b'{"prompt": "hi", "max_tokens": 1e400}'), close_write=True)
        time.sleep(0.3)
    print("client got:", r[:80] or b"(nothing; connection closed with no status line)")
    print("server stderr:", [l for l in err.getvalue().splitlines() if "Error" in l][-1:])
elif test == "fail_after":
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        r = raw(post(b'{"prompt": "hi", "max_tokens": 5, "fail_after": "x"}'), close_write=True)
        time.sleep(0.3)
    print("client got:", r.decode(errors="replace"))
    print("has error event:", b"event: error" in r, "| has usage:", b"event: usage" in r)
    print("server stderr:", [l for l in err.getvalue().splitlines() if "Error" in l][-1:])
    sp = [s for s in stream_server.Handler.tracer.spans][-2:]
    print("spans:", [(s["name"], s["status"], s["attributes"].get("error.type")) for s in sp])
elif test == "leak":
    import tracemalloc
    tracemalloc.start()
    body = json.dumps({"prompt": "SECRET-PROMPT-MARKER please", "max_tokens": 1}).encode()
    def one():
        raw(post(body), close_write=True)
    n0 = len(stream_server.Handler.tracer.spans); m0 = tracemalloc.get_traced_memory()[0]
    for batch in range(10):
        ts = [threading.Thread(target=one) for _ in range(30)]
        [t.start() for t in ts]; [t.join() for t in ts]
    time.sleep(0.3)
    n1 = len(stream_server.Handler.tracer.spans); m1 = tracemalloc.get_traced_memory()[0]
    print(f"300 requests: tracer.spans {n0} -> {n1}; traced memory +{(m1-m0)/1024:.0f} KiB "
          f"(about {(m1-m0)/(n1-n0):.0f} bytes per span, never freed)")
    dump = json.dumps(stream_server.Handler.tracer.spans)
    print("prompt text in spans:", "SECRET-PROMPT-MARKER" in dump)
    print("files in cwd:", sorted(os.listdir(".")))
elif test == "prefill":
    big = json.dumps({"prompt": "a" * 60000, "max_tokens": 1}).encode()
    t0 = time.time()
    r = raw(post(big), wait=60, close_write=True)
    print(f"one {len(big)}-byte request held a server thread for {time.time()-t0:.1f} s; pings sent: {r.count(b': ping')}")
elif test == "concurrency":
    body = json.dumps({"prompt": "hello", "max_tokens": 24}).encode()
    res = []
    def one(): res.append(raw(post(body), wait=20, close_write=True))
    ts = [threading.Thread(target=one) for _ in range(45)]
    t0 = time.time(); [t.start() for t in ts]; peak = threading.active_count(); [t.join() for t in ts]
    time.sleep(0.5)
    print(f"45 concurrent: {sum(b'event: done' in r for r in res)} completed in {time.time()-t0:.1f} s; "
          f"threads peak ~{peak}, after {threading.active_count()}")
elif test == "noread":
    before = threading.active_count()
    socks = []
    for i in range(10):
        s = socket.create_connection(("127.0.0.1", PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
        s.sendall(post(json.dumps({"prompt": "hello", "max_tokens": 512}).encode()))
        socks.append(s)
    time.sleep(3)
    print(f"10 clients that never read: threads {before} -> {threading.active_count()} after 3 s "
          f"(the 24-word answer fits in the socket buffer)")
    for s in socks: s.close()
elif test == "traceparent":
    tp = b"00-deadbeefdeadbeefdeadbeefdeadbeef-1111111111111111-01"
    raw(post(json.dumps({"prompt": "x", "max_tokens": 1}).encode(), extra=b"traceparent: " + tp + b"\r\n"), close_write=True)
    time.sleep(0.2)
    s = stream_server.Handler.tracer.spans[-1]
    print("server span trace_id chosen by the client:", s["trace_id"], "parent", s["parent_id"])
httpd.shutdown()

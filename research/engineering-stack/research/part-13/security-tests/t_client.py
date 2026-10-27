import sys, time, threading
sys.path.insert(0, "/home/claude/part13/phase4/security/lab/engineering-stack-lab-part-13")
import sse_client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
MODE = sys.argv[1]
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        if MODE == "badutf8":
            self.wfile.write(b'event: token\ndata: {"text": "ok"}\n\nevent: token\ndata: {"text": "\xff"}\n\n')
        elif MODE == "notjson":
            self.wfile.write(b'event: token\ndata: not json\n\n')
        elif MODE == "pings":
            for _ in range(16):
                self.wfile.write(b": ping\n\n"); self.wfile.flush(); time.sleep(0.5)
httpd = ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=httpd.serve_forever, daemon=True).start()
t0 = time.perf_counter()
try:
    r = sse_client.stream("hi", httpd.server_address[1])
    print(f"returned after {time.perf_counter()-t0:.1f} s: events {r['events']}, text {r['text']!r}, done {r['done']}")
except Exception as e:
    print(f"sse_client.stream raised {type(e).__name__}: {str(e)[:80]}")
httpd.shutdown()

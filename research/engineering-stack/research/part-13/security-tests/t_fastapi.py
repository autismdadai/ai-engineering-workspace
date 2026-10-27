import asyncio, socket, threading, time, http.client, json
import fastapi, uvicorn, pydantic
from fastapi.sse import EventSourceResponse, ServerSentEvent
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
exp = InMemorySpanExporter(); prov = TracerProvider(); prov.add_span_processor(SimpleSpanProcessor(exp))
app = fastapi.FastAPI(telemetry={"tracer_provider": prov})
class Req(pydantic.BaseModel):
    prompt: str
    max_tokens: int
@app.post("/v1/stream", response_class=EventSourceResponse)
async def stream(req: Req, api_key: str | None = None):
    yield ServerSentEvent(data="ok")
sock = socket.socket(); sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
srv = uvicorn.Server(uvicorn.Config(app, log_level="warning", lifespan="off"))
threading.Thread(target=lambda: asyncio.run(srv.serve(sockets=[sock])), daemon=True).start()
while not srv.started: time.sleep(0.05)
c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
c.request("POST", "/v1/stream?api_key=SECRET-KEY-123", body=json.dumps({"prompt": "SECRET-PROMPT-456", "max_tokens": "lots"}),
          headers={"Content-Type": "application/json", "Authorization": "Bearer SECRET-BEARER-789"})
r = c.getresponse(); body = r.read().decode(); c.close()
print("status", r.status, "| response body echoes the prompt:", "SECRET-PROMPT-456" in body)
time.sleep(0.3)
dump = json.dumps([{"name": s.name, "attrs": dict(s.attributes), "events": [(e.name, dict(e.attributes)) for e in s.events]} for s in exp.get_finished_spans()], default=str)
for marker in ("SECRET-KEY-123", "SECRET-PROMPT-456", "SECRET-BEARER-789"):
    print(f"{marker:18} in FastAPI's spans: {marker in dump}")
for s in exp.get_finished_spans():
    print(" span", s.name, {k: v for k, v in s.attributes.items() if "url" in k or "query" in k or "target" in k})
srv.should_exit = True; time.sleep(0.3)

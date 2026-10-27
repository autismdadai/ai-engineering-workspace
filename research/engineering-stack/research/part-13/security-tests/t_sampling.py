from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.propagators.textmap import DefaultGetter
prov = TracerProvider(sampler=ParentBased(TraceIdRatioBased(0.01)))   # "keep 1 in 100"
tr = prov.get_tracer("t"); prop = TraceContextTextMapPropagator()
import secrets
def run(header):
    kept = 0
    for _ in range(1000):
        ctx = prop.extract({"traceparent": f"00-{secrets.token_hex(16)}-{secrets.token_hex(8)}-{header}"}, getter=DefaultGetter()) if header else None
        with tr.start_as_current_span("POST /v1/stream", context=ctx) as s:
            kept += s.is_recording()
    return kept
print("ParentBased(TraceIdRatioBased(0.01)), 1,000 requests each:")
print("  no traceparent            kept", run(None))
print("  client sends flags 01     kept", run("01"))
print("  client sends flags 00     kept", run("00"))

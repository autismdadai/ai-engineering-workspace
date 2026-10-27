"""tinytrace: a few-dozen-line tracer that shows what a span is
(Engineering Stack, Part 13).

Standard library only, for the lab. Real code should use the OpenTelemetry
SDK (crosscheck.py compares the two). Spans are kept in memory and, if you
ask, written as JSON lines to a file you name. Nothing is sent anywhere.
"""
from __future__ import annotations

import json
import secrets
import threading
import time
from collections import deque
from contextlib import contextmanager

from shipmath import parse_traceparent


class Tracer:
    def __init__(self, service: str, path: str | None = None, keep: int = 10_000):
        self.service = service
        self.path = path
        self.spans: deque[dict] = deque(maxlen=keep)   # the newest `keep` spans; old ones drop off
        self._lock = threading.Lock()
        self._local = threading.local()

    @contextmanager
    def span(self, name: str, attributes: dict | None = None,
             traceparent: str | None = None, kind: str = "INTERNAL"):
        parent = getattr(self._local, "current", None)
        incoming = parse_traceparent(traceparent) if traceparent else None
        if parent is not None:
            trace_id, parent_id = parent["trace_id"], parent["span_id"]
        elif incoming is not None:
            trace_id, parent_id = incoming["trace_id"], incoming["parent_id"]
        else:
            trace_id, parent_id = secrets.token_hex(16), None
        record = {"service": self.service, "name": name, "kind": kind,
                  "trace_id": trace_id, "span_id": secrets.token_hex(8),
                  "parent_id": parent_id, "attributes": dict(attributes or {}),
                  "start": time.time_ns(), "end": None, "status": "UNSET"}
        self._local.current = record
        try:
            yield record
        except BaseException as error:
            record["status"] = "ERROR"
            record["attributes"]["error.type"] = type(error).__name__
            raise
        finally:
            record["end"] = time.time_ns()
            self._local.current = parent
            with self._lock:
                self.spans.append(record)
                if self.path:
                    with open(self.path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(record) + "\n")

    @staticmethod
    def traceparent(record: dict) -> str:
        """The header to send to the next service so its spans join this trace."""
        return f"00-{record['trace_id']}-{record['span_id']}-01"

"""mutation_check: break the lab on purpose and make sure run_lab.py notices.

Each mutation changes one thing in a temporary copy of the lab; run_lab.py
must then fail. The unbroken copy must pass first. Temporary folders are
deleted afterwards. Standard library only.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["README.md", "shipmath.py", "ssewire.py", "tinytrace.py", "stream_server.py", "buffer_proxy.py",
         "sse_client.py", "demo.py", "run_lab.py", "mutation_check.py"]

MUTATIONS = [  # (description, file, old text, new text)
    ('multi-line data sent as one line', 'ssewire.py',
     'for line in data.replace("\\r\\n", "\\n").replace("\\r", "\\n").split("\\n"):',
     'for line in [data]:'),
    ('comment lines read as data', 'ssewire.py',
     'if line.startswith(":"):\n            return None',
     'if line.startswith(":"):\n            self.data += line + "\\n"\n            return None'),
    ('space after the colon kept', 'ssewire.py',
     'if value.startswith(" "):\n                value = value[1:]',
     'if False:\n                value = value[1:]'),
    ('trailing newline of data kept', 'ssewire.py',
     'data = self.data[:-1] if self.data.endswith("\\n") else self.data',
     'data = self.data'),
    ('event type not reset after dispatch', 'ssewire.py',
     'event = Event(self.event_type or "message", data, self.last_event_id)\n        self.event_type = ""',
     'event = Event(self.event_type or "message", data, self.last_event_id)'),
    ('event with no data dispatched', 'ssewire.py',
     'if self.data == "":\n            self.event_type = ""\n            return None',
     'if False:\n            return None'),
    ('NUL in id accepted', 'ssewire.py',
     'if "\\0" not in value:\n                self._id_buffer = value',
     'self._id_buffer = value'),
    ('any retry value accepted', 'ssewire.py',
     'if value and all("0" <= c <= "9" for c in value):',
     'if value.strip().isalnum():'),
    ('CRLF split across chunks counted twice', 'ssewire.py',
     'text = text[1:]          # the LF of a CRLF',
     'text = text          # the LF of a CRLF'),
    ('split UTF-8 character not held back', 'ssewire.py',
     'text = self._decoder.decode(chunk)',
     'text = chunk.decode("utf-8", "replace")'),
    ('BOM not skipped', 'ssewire.py',
     'if text.startswith("\\ufeff"):',
     'if False:'),
    ('buffering header not sent', 'stream_server.py',
     'self.send_header("X-Accel-Buffering", "no")',
     'pass'),
    ('generation goes on after the client leaves', 'stream_server.py',
     'finish = "client_gone"   # stop generating',
     'continue  # keep going'),
    ('error sent as a token', 'stream_server.py',
     '"stand-in overload"}),\n                                event="error"))',
     '"stand-in overload"}),\n                                event="token"))'),
    ('no size limit', 'stream_server.py',
     'if not length.isdigit() or not 0 < int(length) <= MAX_BODY:',
     'if not length.isdigit():'),
    ('API key not checked', 'stream_server.py',
     'return scheme.lower() == "bearer" and hmac',
     'return True or hmac'),
    ('proxy ignores the header even when told to honour it', 'buffer_proxy.py',
     'passthrough = honour_header and',
     'passthrough = False and'),
    ('cached tokens left out of input_tokens', 'shipmath.py',
     '"gen_ai.usage.input_tokens": prompt_tokens(usage),',
     '"gen_ai.usage.input_tokens": usage.get("input", 0),'),
    ('content captured by default', 'shipmath.py',
     'capture_content: bool = False',
     'capture_content: bool = True'),
    ('span named after the provider', 'shipmath.py',
     'return f"chat {model}", attrs',
     'return f"chat {provider}", attrs'),
    ('drop_content keeps the prompt', 'shipmath.py',
     'if k not in CONTENT_ATTRIBUTES}',
     'if k != "gen_ai.output.messages"}'),
    ('all-zero trace ID accepted', 'shipmath.py',
     'set(trace_id) == {"0"} or ',
     ''),
    ('long-context price only on the extra tokens', 'shipmath.py',
     'if rule and prompt_tokens(usage) > rule["over"]:',
     'if rule and usage.get("input", 0) > 10**12:'),
    ('cache tokens not counted toward the threshold', 'shipmath.py',
     'return usage.get("input", 0) + usage.get("cache_read", 0) + usage.get("cache_write", 0)',
     'return usage.get("input", 0)'),
    ('batch discount ignored', 'shipmath.py',
     'total *= BATCH',
     'total *= 1'),
    ('Anthropic spend-cap 429 retried', 'shipmath.py',
     'and "retry-after-ms" not in h:\n        return None',
     'and "retry-after-ms" not in h:\n        pass'),
    ('400 retried', 'shipmath.py',
     'if not (status in (408, 409, 429) or status >= 500):',
     'if status < 0:'),
    ('retry-after ignored', 'shipmath.py',
     'wait = float(value) / scale',
     'wait = min(cap, base * 2 ** attempt)'),
    ('percentile rounds down', 'shipmath.py',
     'rank = math.ceil(q / 100 * len(ordered))',
     'rank = max(1, int(q / 100 * len(ordered)))'),
    ("Little's law divides", 'shipmath.py',
     'return arrivals_per_second * seconds_in_system',
     'return arrivals_per_second / max(seconds_in_system, 1)'),
    ('tracer ignores the incoming traceparent', 'tinytrace.py',
     'elif incoming is not None:',
     'elif False:'),
    ('server listens on every address', 'stream_server.py',
     'if host not in ("127.0.0.1", "localhost"):',
     'if False:'),
    ('max_tokens not checked', 'stream_server.py',
     'max_tokens = whole_number(req.get("max_tokens", MAX_TOKENS), 1, MAX_TOKENS)',
     'max_tokens = req.get("max_tokens", MAX_TOKENS)'),
    ('true accepted as a number', 'stream_server.py',
     'if isinstance(value, bool) or not isinstance',
     'if not isinstance'),
    ('bad UTF-8 raises', 'ssewire.py',
     'errors="replace"',
     'errors="strict"'),
    ('an empty read forgets a pending CR', 'ssewire.py',
     'if not text:\n            return []',
     'if not text:\n            self._pending_cr = False\n            return []'),
    ('no line length limit', 'ssewire.py',
     'if length > MAX_LINE or len(self.data) > MAX_DATA:',
     'if False:'),
    ('no socket timeout', 'stream_server.py',
     'timeout = SOCKET_TIMEOUT       #',
     'timeout = None       #'),
    ('no cap on clients', 'stream_server.py',
     'if not self.slots.acquire(blocking=False):',
     'if not self.slots.acquire(blocking=False) and False:'),
    ('empty key served', 'stream_server.py',
     'if Handler.api_key == "":',
     'if False:'),
    ('Bearer matched case-sensitively', 'stream_server.py',
     'scheme.lower() == "bearer"',
     'scheme == "Bearer"'),
    ('a day-long retry-after obeyed', 'shipmath.py',
     'return wait if wait <= MAX_WAIT else None',
     'return wait'),
    ('proxy trusts any Content-Length', 'buffer_proxy.py',
     'if not re.fullmatch(r"\\d{1,9}", length.strip()):',
     'if False:'),
    ('proxy has no size limit', 'buffer_proxy.py',
     'if int(length) > MAX_BODY:',
     'if False:'),
    ('proxy hangs up instead of 502', 'buffer_proxy.py',
     'except OSError:\n                conn.close()',
     'except ZeroDivisionError:\n                conn.close()'),
    ('tracer keeps every span', 'tinytrace.py',
     'deque(maxlen=keep)',
     'deque()'),
    ('error event shows internal details', 'stream_server.py',
     '"message": "the stream failed"}',
     '"message": str(error)}'),
    ('client deadline ignored', 'sse_client.py',
     'if time.perf_counter() - t0 > deadline:',
     'if False:'),
]


def run(folder: str) -> int:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONIOENCODING", None)
    return subprocess.run([sys.executable, "-B", "run_lab.py"], cwd=folder, env=env,
                          capture_output=True, text=True, timeout=300).returncode


def copy() -> str:
    tmp = tempfile.mkdtemp(prefix="lab13-")
    for f in FILES:
        shutil.copy(os.path.join(HERE, f), tmp)
    return tmp


def main() -> int:
    tmp = copy()
    try:
        if run(tmp) != 0:
            print("The unbroken copy fails: fix run_lab.py first")
            return 1
        print("ok      the unbroken copy passes")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    caught = 0
    for i, (desc, name, old, new) in enumerate(MUTATIONS, 1):
        tmp = copy()
        try:
            path = os.path.join(tmp, name)
            text = open(path, encoding="utf-8").read()
            if text.count(old) != 1:
                print(f"SETUP  {i:2d} {desc}: text found {text.count(old)} times")
                continue
            open(path, "w", encoding="utf-8").write(text.replace(old, new))
            code = run(tmp)
            if code != 0:
                caught += 1
                print(f"caught {i:2d} {desc}")
            else:
                print(f"MISSED {i:2d} {desc}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(f"{caught} of {len(MUTATIONS)} mutations caught")
    return 0 if caught == len(MUTATIONS) else 1


if __name__ == "__main__":
    sys.exit(main())

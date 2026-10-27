"""ssewire: Server-Sent Events on the wire (Engineering Stack, Part 13).

Standard library only. The encoder and the parser follow the WHATWG HTML
Living Standard, section 9.2 "Server-sent events" (read October 20, 2026):
UTF-8 only, lines ending in CRLF, LF or CR, fields `event`, `data`, `id` and
`retry`, comment lines starting with a colon, and a blank line that ends
(dispatches) an event. Part 13, Section 3.2 explains each rule.
"""
from __future__ import annotations

import codecs
import re
from dataclasses import dataclass

MAX_LINE = 1 << 20        # 1 MiB: refuse a line or an event longer than this
MAX_DATA = 1 << 20
_BREAK = re.compile(r"\r\n|\r|\n")


@dataclass
class Event:
    type: str          # "message" unless an `event:` field set it
    data: str
    last_event_id: str


def encode(data: str, event: str | None = None, id: str | None = None,
           retry: int | None = None) -> bytes:
    """One event as bytes. Multi-line data becomes several `data:` lines."""
    out = []
    for name, value in (("event", event), ("id", id)):
        if value is not None:
            if any(c in value for c in "\r\n"):
                raise ValueError(f"{name} must be one line")
            if name == "id" and "\0" in value:
                raise ValueError("id must not contain NUL")
            out.append(f"{name}: {value}")
    if retry is not None:
        if retry < 0:
            raise ValueError("retry is a whole number of milliseconds")
        out.append(f"retry: {int(retry)}")
    for line in data.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        out.append(f"data: {line}")
    return ("\n".join(out) + "\n\n").encode("utf-8")


def comment(text: str = "ping") -> bytes:
    """A comment line: clients ignore it, but it keeps idle connections open."""
    return f": {text}\n\n".encode("utf-8")


class Parser:
    """Feed bytes in any chunk sizes; get complete events back.

    Follows the spec's "interpreting an event stream" steps: one leading BOM
    is skipped, a field without a colon has an empty value, one space after
    the colon is dropped, `id` values containing NUL are ignored, `retry` is
    used only if it is all ASCII digits, and an event with no data is not
    dispatched. Data still pending when the stream ends is discarded.
    """

    def __init__(self) -> None:
        # Bad bytes become U+FFFD, as the spec's "UTF-8 decode" step says;
        # a character split across reads waits for its other half.
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        self._partial: list[str] = []      # an unfinished line, kept as pieces
        self._partial_len = 0
        self._started = False
        self._pending_cr = False
        self.event_type = ""
        self.data = ""
        self.last_event_id = ""
        self._id_buffer = ""
        self.retry: int | None = None

    def feed(self, chunk: bytes) -> list[Event]:
        text = self._decoder.decode(chunk)
        if not text:
            return []
        if not self._started:
            self._started = True
            if text.startswith("\ufeff"):
                text = text[1:]
        return self._lines(text)

    def _lines(self, text: str) -> list[Event]:
        events: list[Event] = []
        if self._pending_cr:
            self._pending_cr = False
            if text.startswith("\n"):
                text = text[1:]          # the LF of a CRLF split across reads
        start = 0
        for match in _BREAK.finditer(text):
            piece = text[start:match.start()]
            if self._partial:
                piece = "".join(self._partial) + piece
                self._partial, self._partial_len = [], 0
            self._check(len(piece))
            if match.group() == "\r" and match.end() == len(text):
                self._pending_cr = True
            start = match.end()
            event = self._line(piece)
            if event is not None:
                events.append(event)
        rest = text[start:]
        if rest:
            self._partial.append(rest)
            self._partial_len += len(rest)
            self._check(self._partial_len)
        return events

    def _check(self, length: int) -> None:
        if length > MAX_LINE or len(self.data) > MAX_DATA:
            raise ValueError("SSE line or event too long for this parser")

    def _line(self, line: str) -> Event | None:
        if line == "":
            return self._dispatch()
        if line.startswith(":"):
            return None
        if ":" in line:
            field, value = line.split(":", 1)
            if value.startswith(" "):
                value = value[1:]
        else:
            field, value = line, ""
        if field == "event":
            self.event_type = value
        elif field == "data":
            self.data += value + "\n"
        elif field == "id":
            if "\0" not in value:
                self._id_buffer = value
        elif field == "retry":
            if value and all("0" <= c <= "9" for c in value):
                self.retry = int(value)
        return None

    def _dispatch(self) -> Event | None:
        self.last_event_id = self._id_buffer
        if self.data == "":
            self.event_type = ""
            return None
        data = self.data[:-1] if self.data.endswith("\n") else self.data
        event = Event(self.event_type or "message", data, self.last_event_id)
        self.event_type = ""
        self.data = ""
        return event


def parse_all(stream: bytes, chunk_size: int = 0) -> list[Event]:
    """Parse a whole byte string, optionally fed in fixed-size chunks."""
    p = Parser()
    if chunk_size <= 0:
        return p.feed(stream)
    events = []
    for i in range(0, len(stream), chunk_size):
        events += p.feed(stream[i:i + chunk_size])
    return events

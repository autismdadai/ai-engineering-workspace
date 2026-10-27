"""Defences written in code for an LLM app, for learning (Engineering Stack, Part 10).

Standard library only. None of these depends on the model behaving well:
a tool-call gate with the Rule of Two (1), output cleaning (2), invisible
text and labels (3), pattern redaction (4), classifier arithmetic (5) and
licence buckets (6). They reduce risk; none makes injection impossible.
The part's Section 3 explains each one.
"""
import hashlib
import hmac
import ipaddress
import json
import logging
import re
import secrets
from urllib.parse import urlsplit

# ---------------------------------------------------------------- 1. the gate

UNTRUSTED = "untrusted_input"   # [A] text from outside: web pages, emails, files
PRIVATE = "private_data"        # [B] reading sensitive or personal data
OUTWARD = "outward_action"      # [C] sending, paying, deleting, posting
ALL_THREE = frozenset({UNTRUSTED, PRIVATE, OUTWARD})


def action_id(call, nonce):
    """A short fingerprint of one exact call (tool plus every argument) and a
    random nonce, so each request for approval gets its own id."""
    body = json.dumps(call, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((nonce + body).encode()).hexdigest()[:16]


class Tool:
    """A tool the app offers. `params` maps each argument to a checker that
    returns None when the value is fine or a reason when it is not. `legs`
    says which of the three risky properties using the tool adds."""

    def __init__(self, name, params, legs=()):
        unknown = set(legs) - ALL_THREE
        if unknown:
            raise ValueError(f"unknown legs {sorted(unknown)}")
        self.name = name
        self.params = dict(params)
        self.legs = frozenset(legs)


class Decision:
    def __init__(self, verdict, reason, call=None):
        self.verdict = verdict          # "allow", "deny" or "ask"
        self.reason = reason
        self.nonce = secrets.token_hex(8)
        self.action_id = action_id(call, self.nonce) if call is not None else None
        self.used = False

    def __repr__(self):
        return f"Decision({self.verdict!r}, {self.reason!r})"


class Gate:
    """Checks tool calls in code. Anything not explicitly allowed is denied.

    `allowed` is per task, not per app; `max_calls` is a per-session budget.
    The session's legs never reset: text read earlier stays in the context.
    """

    def __init__(self, tools, allowed, max_calls=20):
        self.tools = {tool.name: tool for tool in tools}
        self.allowed = frozenset(allowed)
        self.max_calls = max_calls
        self.calls = 0
        self.legs = set()

    def check(self, call):
        if not isinstance(call, dict) or set(call) != {"tool", "args"}:
            return Decision("deny", "a call must have exactly 'tool' and 'args'")
        name, args = call["tool"], call["args"]
        tool = self.tools.get(name) if isinstance(name, str) else None
        if tool is None:
            return Decision("deny", f"unknown tool {name!r}")
        if name not in self.allowed:
            return Decision("deny", f"tool {name!r} is not allowed for this task")
        if self.calls >= self.max_calls:
            return Decision("deny", f"call budget of {self.max_calls} used up")
        if not isinstance(args, dict):
            return Decision("deny", "args must be an object")
        extra = set(args) - set(tool.params)
        if extra:
            return Decision("deny", f"unexpected arguments {sorted(extra)}")
        missing = set(tool.params) - set(args)
        if missing:
            return Decision("deny", f"missing arguments {sorted(missing)}")
        for key, checker in tool.params.items():
            problem = checker(args[key])
            if problem:
                return Decision("deny", f"{key}: {problem}")
        if ALL_THREE <= self.legs | tool.legs:
            return Decision("ask", "untrusted input, private data and an outward "
                                   "action together need a person's approval", call)
        return Decision("allow", "ok", call)

    def approve(self, decision, call, answer):
        """True once, for an explicit approval of this exact call."""
        ok = (decision.verdict == "ask"
              and not decision.used
              and decision.action_id == action_id(call, decision.nonce)
              and isinstance(answer, dict)
              and answer.get("decision") == "approve"
              and answer.get("action_id") == decision.action_id)
        if ok:
            decision.used = True  # an approval can't be replayed
        return ok

    def record(self, call):
        """Call after a tool really ran: count it and remember its legs."""
        self.calls += 1
        self.legs |= self.tools[call["tool"]].legs


# Checkers for Tool params. Each returns None if fine, else a reason.

def one_of(*values):
    return lambda v: None if v in values else f"must be one of {list(values)}"


def number(low, high):
    def check(v):
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return "must be a number"
        return None if low <= v <= high else f"must be between {low} and {high}"
    return check


def text(max_len):
    def check(v):
        if not isinstance(v, str):
            return "must be text"
        return None if len(v) <= max_len else f"longer than {max_len} characters"
    return check


def email_at(*domains):
    pattern = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+)")

    def check(v):
        m = pattern.fullmatch(v) if isinstance(v, str) else None
        if not m:
            return "must be one email address"
        return None if m.group(1).lower() in domains else "domain not allowed"
    return check


def url_on(*hosts):
    return lambda v: None if host_allowed(v, hosts) else "host not allowed"


# ------------------------------------------------------ 2. cleaning the output

def url_problem(url, hosts):
    """None for an https URL whose host is exactly one of `hosts`; otherwise
    the first reason it is refused.

    Refuses any URL with a backslash or a user-info part (name@host), because
    parsers disagree on them: Python's urlsplit reads the host of
    https://evil.example\\@ok.example/ as ok.example, while browsers treat the
    backslash as a slash and go to evil.example. Protocol-relative, data: and
    javascript: URLs have no https scheme and fail.
    """
    if not isinstance(url, str):
        return "not text"
    if "\\" in url:
        return "backslash"
    try:
        parts = urlsplit(url.strip())
        host = parts.hostname
    except ValueError:
        return "unparseable"
    if "@" in parts.netloc:
        return "user info"
    if parts.scheme != "https":
        return "not https"
    if host is None or host not in hosts:
        return "host not allowed"
    return None


def host_allowed(url, hosts):
    return url_problem(url, hosts) is None


_IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^\s)>]*)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
_LINK = re.compile(r"\[([^\]]*)\]\(\s*<?([^\s)>]*)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
_REFDEF = re.compile(r"^[ \t]{0,3}\[([^\]]+)\]:[ \t]*<?(\S+?)>?(?:[ \t]+.*)?$", re.M)
_BARE = re.compile(r"(?i)\b(?:https?|ftp|file|data|javascript):[^\s<>\"')\]]+")
_WWW = re.compile(r"(?i)(?<![\w./@-])www\.[^\s<>\"')\]]+")  # GitHub-style autolinks


def clean_output(markdown, hosts):
    """Return (clean_text, removed_urls).

    Raw HTML is escaped so no tag renders; images and links to hosts not in
    `hosts` are removed (a link keeps its visible text); reference-style link
    definitions and bare URLs to other hosts are removed too.
    """
    removed = []
    kept = []

    def hold(s):
        kept.append(s)
        return f"\x00{len(kept) - 1}\x00"

    out = markdown.replace("\x00", "").replace("<", "&lt;")

    def image(m):
        if host_allowed(m.group(2), hosts):
            return hold(m.group(0))
        removed.append(m.group(2))
        return "[image removed]"

    def link(m):
        if host_allowed(m.group(2), hosts):
            return hold(m.group(0))
        removed.append(m.group(2))
        return f"{m.group(1)} [link removed]"

    def refdef(m):
        if host_allowed(m.group(2), hosts):
            return hold(m.group(0))
        removed.append(m.group(2))
        return f"[{m.group(1)}]: [link removed]"

    def bare(m):
        if host_allowed(m.group(0), hosts):
            return hold(m.group(0))
        removed.append(m.group(0))
        return "[url removed]"

    out = _IMAGE.sub(image, out)
    out = _LINK.sub(link, out)
    out = _REFDEF.sub(refdef, out)
    out = _BARE.sub(bare, out)
    out = _WWW.sub(lambda m: hold(m.group(0)) if host_allowed("https://" + m.group(0), hosts)
                   else (removed.append(m.group(0)) or "[url removed]"), out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], out)
    return out, removed


# --------------------------------------------- 3. invisible text and labelling

INVISIBLE = {
    "tag": range(0xE0000, 0xE0080),          # can spell hidden ASCII text
    "zero_width": [0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF],
    "bidi": list(range(0x202A, 0x202F)) + list(range(0x2066, 0x206A)) + [0x200E, 0x200F, 0x061C],
    "variation": list(range(0xFE00, 0xFE10)) + list(range(0xE0100, 0xE01F0)),  # can carry data
    "other": [0x00AD, 0x180E, 0x2061, 0x2062, 0x2063, 0x2064, 0x034F,
              0x115F, 0x1160, 0x3164, 0xFFA0],  # the last four render as blank space
}
_KIND = {cp: kind for kind, cps in INVISIBLE.items() for cp in cps}


def strip_invisible(text):
    """Remove characters a person can't see. Returns (text, counts by kind).

    Removing the zero-width joiner (U+200D) and variation selectors also
    changes some emoji; that is the price of a simple rule.
    """
    counts = {}
    kept = []
    for ch in text:
        kind = _KIND.get(ord(ch))
        if kind:
            counts[kind] = counts.get(kind, 0) + 1
        else:
            kept.append(ch)
    return "".join(kept), counts


def untrusted_block(content, source):
    """Label outside text as data, JSON-encoded so it can't close the label.
    It shows where text came from; it does not stop injection (Section 3.4)."""
    body = json.dumps(content, ensure_ascii=True)
    body = body.replace("<", "\\u003c").replace(">", "\\u003e")
    label = json.dumps(str(source), ensure_ascii=True)
    label = label.replace("<", "\\u003c").replace(">", "\\u003e")
    return f"<untrusted source={label}>{body}</untrusted>"


# ------------------------------------------------------------- 4. redaction

def luhn_ok(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def _card(m):
    digits = re.sub(r"[ -]", "", m.group(0))
    return 13 <= len(digits) <= 19 and luhn_ok(digits)


def _ssn(m):
    area, group, serial = m.group(1), m.group(2), m.group(3)
    return (area not in ("000", "666") and not area.startswith("9")
            and group != "00" and serial != "0000")


def _ip(m):
    try:
        ipaddress.IPv4Address(m.group(0))
        return True
    except ValueError:
        return False


# (type, pattern, extra check or None). Order is the tie-break for equal spans.
PATTERNS = [
    ("CREDIT_CARD", re.compile(r"(?<![\d-])\d(?:[ -]?\d){12,18}(?![\d-])"), _card),
    ("US_SSN", re.compile(r"(?<![\d-])(\d{3})-(\d{2})-(\d{4})(?![\d-])"), _ssn),
    ("EMAIL", re.compile(r"(?<![\w.+%-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+"
                         r"(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])"), None),
    ("IP_ADDRESS", re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"), _ip),
    ("PHONE_US", re.compile(r"(?<![\w+])(?:\+?1[ .-]?)?(?:\([2-9]\d{2}\)|[2-9]\d{2})"
                            r"[ .-]?[2-9]\d{2}[ .-]?\d{4}(?![\d-])"), None),
]


class Redaction:
    def __init__(self, text, findings, mapping):
        self.text = text            # the redacted text
        self.findings = findings    # [(type, start, end, value)] in the input
        self.mapping = mapping      # placeholder -> original value; keep secret


class Redactor:
    """Finds a few kinds of personal data by pattern and replaces them.

    "label" mode numbers values per call (<EMAIL_1>); "hash" mode uses an
    HMAC under a secret (<EMAIL_3f2a9c1b>), stable across calls: pseudonymous,
    not anonymous, since the secret's holder can test a guess. Finds no names.
    """

    def __init__(self, mode="label", secret=None, types=None):
        if mode not in ("label", "hash"):
            raise ValueError("mode must be 'label' or 'hash'")
        if mode == "hash" and not secret:
            raise ValueError("hash mode needs a secret")
        self.mode = mode
        self.secret = secret.encode() if isinstance(secret, str) else secret
        self.types = set(types) if types else {p[0] for p in PATTERNS}

    def find(self, text):
        candidates = []
        for priority, (kind, pattern, ok) in enumerate(PATTERNS):
            if kind not in self.types:
                continue
            for m in pattern.finditer(text):
                if ok is None or ok(m):
                    candidates.append((m.start(), m.end(), priority, kind))
        candidates.sort(key=lambda c: (c[0] - c[1], c[2], c[0]))
        chosen = []
        for start, end, _, kind in candidates:
            if all(end <= s or start >= e for s, e, _ in chosen):
                chosen.append((start, end, kind))
        chosen.sort()
        return [(kind, s, e, text[s:e]) for s, e, kind in chosen]

    def _placeholder(self, kind, value, numbers):
        if self.mode == "hash":
            digest = hmac.new(self.secret, f"{kind}:{value}".encode(), hashlib.sha256)
            return f"<{kind}_{digest.hexdigest()[:8]}>"
        key = (kind, value)
        if key not in numbers:
            numbers[key] = sum(1 for k in numbers if k[0] == kind) + 1
        return f"<{kind}_{numbers[key]}>"

    def redact(self, text):
        findings = self.find(text)
        numbers, mapping, pieces, last = {}, {}, [], 0
        for kind, start, end, value in findings:
            placeholder = self._placeholder(kind, value, numbers)
            mapping[placeholder] = value
            pieces.append(text[last:start])
            pieces.append(placeholder)
            last = end
        pieces.append(text[last:])
        return Redaction("".join(pieces), findings, mapping)


def restore(text, mapping):
    """Put the original values back (only for someone allowed to see them)."""
    for placeholder, value in mapping.items():
        text = text.replace(placeholder, value)
    return text


class RedactingFilter(logging.Filter):
    """A logging filter that redacts each message before any handler writes it."""

    def __init__(self, redactor):
        super().__init__()
        self.redactor = redactor

    def filter(self, record):
        record.msg = self.redactor.redact(record.getMessage()).text
        record.args = None
        return True


def score(found, gold):
    """Per-type precision and recall for exact (type, start, end) matches."""
    found_set = {(k, s, e) for k, s, e, *_ in found}
    gold_set = {(k, s, e) for k, s, e, *_ in gold}
    result = {}
    for kind in sorted({k for k, _, _ in found_set | gold_set}):
        f = {x for x in found_set if x[0] == kind}
        g = {x for x in gold_set if x[0] == kind}
        tp = len(f & g)
        result[kind] = {"precision": tp / len(f) if f else None,
                        "recall": tp / len(g) if g else None,
                        "found": len(f), "gold": len(g), "true_positives": tp}
    return result


# -------------------------------------------- 5. what classifier numbers mean

def screen(n, base_rate, recall, fpr):
    """Expected outcomes when a classifier screens n items, a fraction
    base_rate of which are truly bad."""
    for name, value in (("base_rate", base_rate), ("recall", recall), ("fpr", fpr)):
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    bad = n * base_rate
    good = n - bad
    caught = bad * recall
    false_alarms = good * fpr
    flagged = caught + false_alarms
    return {"bad": bad, "caught": caught, "missed": bad - caught,
            "false_alarms": false_alarms,
            "precision": caught / flagged if flagged else None}


def stack(layers):
    """Recall and false-positive rate of several layers where any one can
    block, IF their mistakes were independent. They rarely are, so treat the
    result as a best case."""
    miss, pass_good = 1.0, 1.0
    for recall, fpr in layers:
        miss *= 1 - recall
        pass_good *= 1 - fpr
    return {"recall": 1 - miss, "fpr": 1 - pass_good}


# --------------------------------------------------------------- 6. licences

# A small table, read from SPDX License List 3.29.0 (Part 10, Section 3.10).
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
              "Zlib", "BSL-1.0", "0BSD", "Unlicense", "PostgreSQL"}
COPYLEFT = {"GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later",
            "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later",
            "AGPL-3.0-only", "AGPL-3.0-or-later", "MPL-2.0", "EPL-2.0"}
SOURCE_AVAILABLE = {"Elastic-2.0", "SSPL-1.0", "BUSL-1.1"}
DATA_OPEN = {"CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0"}
NON_COMMERCIAL = {"CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "CC-BY-NC-ND-4.0"}

# Lower is easier to use; OR takes the easier side, AND the harder one.
RANK = {"permissive": 0, "open-data": 0, "copyleft": 1, "read-terms": 2,
        "non-commercial": 3, "source-available": 3, "unknown": 4}

_TOKEN = re.compile(r"\s*(\(|\)|[A-Za-z0-9.+:-]+)")


def _bucket(identifier):
    if identifier in PERMISSIVE:
        return "permissive"
    if identifier in COPYLEFT:
        return "copyleft"
    if identifier in SOURCE_AVAILABLE:
        return "source-available"
    if identifier in DATA_OPEN:
        return "open-data"
    if identifier in NON_COMMERCIAL:
        return "non-commercial"
    if identifier.startswith("LicenseRef-"):
        return "read-terms"
    return "unknown"


def classify_licence(expression):
    """Sort an SPDX licence expression into one bucket. Malformed or empty
    expressions are "unknown", never "permissive". Information, not legal
    advice."""
    if not isinstance(expression, str):
        return "unknown"
    tokens, pos = [], 0
    while pos < len(expression):
        m = _TOKEN.match(expression, pos)
        if not m or not m.group(1):
            return "unknown"
        tokens.append(m.group(1))
        pos = m.end()
        while pos < len(expression) and expression[pos].isspace():
            pos += 1
    if not tokens:
        return "unknown"
    index = 0

    def peek():
        return tokens[index] if index < len(tokens) else None

    def take():
        nonlocal index
        index += 1
        return tokens[index - 1]

    def atom():
        tok = peek()
        if tok is None or tok.upper() in ("AND", "OR", "WITH", ")"):
            raise ValueError("expected a licence")
        take()
        if tok == "(":
            value = either()
            if peek() != ")":
                raise ValueError("missing )")
            take()
            return value
        value = _bucket(tok)
        if peek() is not None and peek().upper() == "WITH":
            take()
            exc = peek()
            if exc is None or exc in ("(", ")") or exc.upper() in ("AND", "OR", "WITH"):
                raise ValueError("WITH needs an exception id")
            take()
        return value

    def both():
        value = atom()
        while peek() is not None and peek().upper() == "AND":
            take()
            other = atom()
            value = max(value, other, key=RANK.get)
        return value

    def either():
        value = both()
        while peek() is not None and peek().upper() == "OR":
            take()
            other = both()
            value = min(value, other, key=RANK.get)
        return value

    try:
        result = either()
    except ValueError:
        return "unknown"
    return result if index == len(tokens) else "unknown"

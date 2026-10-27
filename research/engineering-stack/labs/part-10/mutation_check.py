"""Prove the checks can fail (Engineering Stack, Part 10).

Each mutation breaks the lab in one small way, in a temporary copy of this
folder, and runs run_lab.py there. A mutation is "caught" when run_lab.py
fails. The temporary copies are deleted when the run ends.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ("guard.py", "examples.py", "run_lab.py")

# (file, text to replace, replacement, what it breaks)
MUTATIONS = [
    ("guard.py", "        if extra:", "        if False:", "smuggled arguments allowed"),
    ("guard.py", "        if missing:", "        if False:", "missing arguments allowed"),
    ("guard.py", "        if name not in self.allowed:", "        if False:", "any known tool allowed"),
    ("guard.py", "if self.calls >= self.max_calls:", "if self.calls > self.max_calls:",
     "budget off by one"),
    ("guard.py", 'return Decision("ask"', 'return Decision("allow"', "Rule of Two never asks"),
    ("guard.py", "if ALL_THREE <= self.legs | tool.legs:", "if ALL_THREE <= self.legs:",
     "the call's own leg ignored"),
    ("guard.py", "self.legs |= self.tools[call[\"tool\"]].legs",
     "self.legs = set(self.tools[call[\"tool\"]].legs)", "legs reset after each call"),
    ("guard.py", "\n              and answer.get(\"action_id\") == decision.action_id)", ")",
     "approval not tied to an action id"),
    ("guard.py", "\n              and decision.action_id == action_id(call, decision.nonce)", "",
     "approval not tied to the exact call"),
    ("guard.py", "\n              and not decision.used", "", "an approval can be replayed"),
    ("guard.py", "return hashlib.sha256((nonce + body).encode())",
     "return hashlib.sha256(body.encode())", "no nonce, so an old approval fits a new call"),
    ("guard.py", "    out = _WWW.sub(", "    out = out if True else _WWW.sub(", "www. links kept"),
    ("guard.py", '"variation": list(range(0xFE00, 0xFE10)) + list(range(0xE0100, 0xE01F0)),',
     '"variation": [],', "variation selectors kept"),
    ("guard.py", 'answer.get("decision") == "approve"',
     'str(answer.get("decision")).lower() == "approve"', "approval accepts 'Approve'"),
    ("guard.py", 'decision.verdict == "ask"\n', 'decision.verdict in ("ask", "allow")\n',
     "approve() works on any decision"),
    ("guard.py", "if isinstance(v, bool) or not isinstance(v, (int, float)):",
     "if not isinstance(v, (int, float)):", "True accepted as a number"),
    ("guard.py", "m = pattern.fullmatch(v)", "m = pattern.match(v)", "email checks a prefix only"),
    ("guard.py", '    if parts.scheme != "https":\n        return "not https"\n', "", "plain http allowed"),
    ("guard.py", '    if "@" in parts.netloc:\n        return "user info"\n', "", "user-info allowed"),
    ("guard.py", '    if "\\\\" in url:\n        return "backslash"\n', "", "backslash allowed"),
    ("guard.py", "if host is None or host not in hosts:",
     "if host is None or not any(h in host for h in hosts):", "host matched by substring"),
    ("guard.py", '.replace("\\x00", "").replace("<", "&lt;")', '.replace("\\x00", "")',
     "raw HTML not escaped"),
    ("guard.py", "    out = _BARE.sub(bare, out)", "    out = out", "bare URLs kept"),
    ("guard.py", "    out = _REFDEF.sub(refdef, out)", "    out = out", "reference links not checked"),
    ("guard.py", '        return f"{m.group(1)} [link removed]"', "        return m.group(0)",
     "off-list link kept"),
    ("guard.py", "    def image(m):\n        if host_allowed(m.group(2), hosts):",
     "    def image(m):\n        if True:", "every image kept"),
    ("guard.py", "range(0xE0000, 0xE0080)", "range(0xE0000, 0xE0020)", "most tag characters kept"),
    ("guard.py", "list(range(0x202A, 0x202F)) + ", "", "bidi overrides kept"),
    ("guard.py", 'body = body.replace("<", "\\\\u003c").replace(">", "\\\\u003e")',
     'body = body.replace(">", "\\\\u003e")', "content can close its label"),
    ("guard.py", "body = json.dumps(content, ensure_ascii=True)",
     "body = json.dumps(content, ensure_ascii=False)", "invisible characters not shown"),
    ("guard.py", "    return total % 10 == 0", "    return True", "no Luhn check"),
    ("guard.py", "        if i % 2 == 1:", "        if i % 2 == 0:", "Luhn doubles the wrong digits"),
    ("guard.py", 'area not in ("000", "666")', 'area not in ("000",)', "SSN area 666 allowed"),
    ("guard.py", ' and not area.startswith("9")', "", "SSN area 9xx allowed"),
    ("guard.py", '(?![\\d.])"), _ip),', '(?![\\d.])"), None),', "IP octets not checked"),
    ("guard.py", "if all(end <= s or start >= e for s, e, _ in chosen):", "if True:",
     "overlapping findings kept"),
    ("guard.py", "        if key not in numbers:", "        if True:",
     "same value, new placeholder"),
    ("guard.py", "numbers[key] = sum(1 for k in numbers if k[0] == kind) + 1",
     "numbers[key] = len(numbers) + 1", "numbering shared across types"),
    ("guard.py", "digest = hmac.new(self.secret,", "digest = hmac.new(b\"fixed\",",
     "hash ignores the secret"),
    ("guard.py", '        if mode == "hash" and not secret:', "        if False:",
     "hash mode without a secret"),
    ("guard.py", "record.msg = self.redactor.redact(record.getMessage()).text",
     "record.msg = self.redactor.redact(record.msg).text", "log arguments not redacted"),
    ("guard.py", '"precision": caught / flagged if flagged else None',
     '"precision": caught / bad if bad else None', "precision is really recall"),
    ("guard.py", "        pass_good *= 1 - fpr", "        pass_good *= fpr", "stacked FPR wrong"),
    ("guard.py", 'for name, value in (("base_rate", base_rate), ("recall", recall), ("fpr", fpr)):',
     "for name, value in ():", "rates not range-checked"),
    ("guard.py", "            value = max(value, other, key=RANK.get)",
     "            value = min(value, other, key=RANK.get)", "AND takes the easier side"),
    ("guard.py", "            value = min(value, other, key=RANK.get)\n        return value\n\n    try:",
     "            value = max(value, other, key=RANK.get)\n        return value\n\n    try:",
     "OR takes the harder side"),
    ("guard.py", 'return result if index == len(tokens) else "unknown"', "return result",
     "trailing tokens ignored"),
    ("guard.py", '        return "read-terms"', '        return "permissive"',
     "custom licences treated as permissive"),
    ("guard.py", "    if identifier in SOURCE_AVAILABLE:", "    if False:",
     "source-available not recognized"),
    ("examples.py", "if gate.approve(decision, call, approve(decision, call)):",
     "if approve(decision, call):", "any answer approves in the app"),
]


def run_checks(tmp):
    # Python reuses compiled .pyc files when a source file's size and
    # modification second are unchanged, which a same-length mutation written
    # within the same second can hit. So: no cache, and run with -B.
    shutil.rmtree(os.path.join(tmp, "__pycache__"), ignore_errors=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, "-B", "run_lab.py"], cwd=tmp, env=env,
                          capture_output=True, text=True, timeout=120)


def run_mutation(tmp, file, old, new):
    path = os.path.join(tmp, file)
    with open(path, encoding="utf-8") as handle:
        source = handle.read()
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{file}: expected the text once, found it {count} times: {old!r}")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(source.replace(old, new))
    result = run_checks(tmp)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(source)
    return result.returncode != 0


def main():
    caught = 0
    with tempfile.TemporaryDirectory(prefix="lab10-") as tmp:
        for name in FILES:
            shutil.copy(os.path.join(HERE, name), tmp)
        baseline = run_checks(tmp)
        if baseline.returncode != 0:
            print("The unbroken lab fails; fix that first:\n" + baseline.stdout[-800:])
            return 1
        for number, (file, old, new, what) in enumerate(MUTATIONS, 1):
            try:
                hit = run_mutation(tmp, file, old, new)
            except RuntimeError as error:
                print(f"ERROR  {number:2} {what}: {error}")
                continue
            caught += hit
            print(f"{'caught' if hit else 'MISSED'}  {number:2} {what}")
    print(f"{caught} of {len(MUTATIONS)} mutations caught")
    return 0 if caught == len(MUTATIONS) else 1


if __name__ == "__main__":
    sys.exit(main())

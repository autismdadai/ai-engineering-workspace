"""Harmless edge cases for the Part 10 lab's defences (reserved names only)."""
import sys
sys.path.insert(0, "/home/claude/part10/lab/engineering-stack-lab-part-10")
import guard as g, examples as ex
H = ("docs.example.com",)
print("== clean_output: does anything reach a host other than docs.example.com?")
cases = {
 "autolink": "<https://other.example.invalid/a>",
 "image in link": "[![i](https://docs.example.com/i.png)](https://other.example.invalid/)",
 "entity colon": "![i](https&#58;//other.example.invalid/p.png)",
 "percent host": "![i](https://other%2Eexample.invalid/p.png)",
 "trailing dot allowed host": "![i](https://docs.example.com./p.png)",
 "ref with angle": "[a][1]\n\n[1]: <https://other.example.invalid/x> \"t\"",
 "paren title": "![i](https://other.example.invalid/p.png (t))",
 "www autolink (GFM)": "see www.other.example.invalid/p?d=1",
 "fullwidth dot": "![i](https://other．example.invalid/p.png)",
}
for name, md in cases.items():
    out, removed = g.clean_output(md, H)
    leaked = "other" in out.replace("&lt;", "<")
    print(f"  {name:28} leaked={leaked}  out={out!r}")
print("== strip_invisible: invisible or blank-looking characters it keeps")
for cp, name in [(0xFE0F, "variation selector 16"), (0xE0100, "variation selector 17"),
                 (0x034F, "combining grapheme joiner"), (0x3164, "Hangul filler"),
                 (0x115F, "Hangul choseong filler"), (0x061C, "Arabic letter mark"), (0xFFA0, "halfwidth Hangul filler")]:
    out, counts = g.strip_invisible("a" + chr(cp) + "b")
    print(f"  U+{cp:04X} {name:26} kept={len(out) == 3}")
print("== Gate.approve: can one approval be used twice?")
gate = g.Gate(ex.TOOLS, allowed={"read_inbox", "fetch_page", "send_email"})
read = {"tool": "read_inbox", "args": {"folder": "inbox"}}
fetch = {"tool": "fetch_page", "args": {"url": "https://docs.example.com/n"}}
send = {"tool": "send_email", "args": {"to": "me@example.com", "subject": "s", "body": "b"}}
gate.record(read); gate.record(fetch)
d1 = gate.check(send); ans = {"decision": "approve", "action_id": d1.action_id}
print("  first approval:", gate.approve(d1, send, ans))
d2 = gate.check(send)
print("  same answer on a later identical call:", gate.approve(d2, send, ans), "| same decision again:", gate.approve(d1, send, ans))
print("== Redactor: forms it misses")
for t in ["SSN 123 45 6789", "SSN 123456789", "card 4111.1111.1111.1111", "ip 2001:db8::1", "phone +44 20 7946 0000"]:
    print(f"  {t!r:32} -> {g.Redactor().redact(t).text!r}")
print("== classify_licence: surprises")
for e in ["MIT WITH Unknown-exception", "Apache-2.0+", "DocumentRef-x:LicenseRef-y", "MIT OR LicenseRef-Proprietary"]:
    print(f"  {e!r:34} -> {g.classify_licence(e)}")

"""Optional: compare the lab's redaction with Microsoft Presidio's pattern
recognizers and its Luhn check with python-stdnum (Engineering Stack, Part 10).

Install first:  python -m pip install -r requirements-crosscheck.txt
Needs no model download, account or key. Network connections are blocked for
this script's own run, and every attempt is recorded and printed, so you can
see what a library tries to reach.
"""
import atexit
import logging
import os
import random
import shutil
import socket
import sys
import tempfile

ATTEMPTS = []
# tldextract (used by Presidio's email check) caches the Public Suffix List in
# your home folder. A throwaway cache makes every run behave like a first run
# and leaves nothing behind.
TLD_CACHE = tempfile.mkdtemp(prefix="lab10-tld-")
atexit.register(shutil.rmtree, TLD_CACHE, True)  # removed even if an import fails
os.environ["TLDEXTRACT_CACHE"] = TLD_CACHE
os.environ["NO_PROXY"] = "*"          # connect directly, so attempts name the host
os.environ["no_proxy"] = "*"
for var in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(var, None)


def _blocked_lookup(host, *args, **kwargs):
    ATTEMPTS.append(str(host))
    raise OSError(f"network blocked by crosscheck.py: {host}")


def _blocked_connect(address, *args, **kwargs):
    ATTEMPTS.append(str(address[0]) if isinstance(address, tuple) else str(address))
    raise OSError("network blocked by crosscheck.py")


socket.getaddrinfo = _blocked_lookup
socket.create_connection = _blocked_connect
socket.socket.connect = lambda self, address: _blocked_connect(address)
logging.getLogger("tldextract").setLevel(logging.CRITICAL)
logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)

from presidio_analyzer.predefined_recognizers import (  # noqa: E402
    CreditCardRecognizer, EmailRecognizer, IpRecognizer, PhoneRecognizer, UsSsnRecognizer)
from stdnum import luhn  # noqa: E402

import examples as ex  # noqa: E402
import guard as g  # noqa: E402

PRESIDIO = {
    "CREDIT_CARD": ("CREDIT_CARD", CreditCardRecognizer()),
    "EMAIL": ("EMAIL_ADDRESS", EmailRecognizer()),
    "IP_ADDRESS": ("IP_ADDRESS", IpRecognizer()),
    "US_SSN": ("US_SSN", UsSsnRecognizer()),
    "PHONE_US": ("PHONE_NUMBER", PhoneRecognizer(supported_regions=("US",))),
}


def spans(kind):
    """(lab set, Presidio set) of (record number, matched text)."""
    entity, recognizer = PRESIDIO[kind]
    lab, theirs = set(), set()
    for i, (text, _) in enumerate(ex.RECORDS):
        lab |= {(i, v) for k, _, _, v in g.Redactor(types={kind}).find(text)}
        theirs |= {(i, text[r.start:r.end]) for r in recognizer.analyze(text, [entity], None)}
    return lab, theirs


CHECKS = []


def check(cid, title):
    def wrap(fn):
        CHECKS.append((cid, title, fn))
        return fn
    return wrap


@check("X1", "the lab's Luhn check agrees with python-stdnum on 5,000 numbers")
def _():
    rng = random.Random(10)
    numbers = ["4111111111111111", "5555555555554444", "378282246310005", "4111111111111112"]
    numbers += ["".join(rng.choice("0123456789") for _ in range(rng.randint(13, 19)))
                for _ in range(4996)]
    disagree = [n for n in numbers if g.luhn_ok(n) != luhn.is_valid(n)]
    valid = sum(luhn.is_valid(n) for n in numbers)
    assert not disagree, disagree[:5]
    return f"{len(numbers)} numbers, {valid} valid, 0 disagreements"


@check("X2", "card numbers: the same matches as Presidio")
def _():
    lab, theirs = spans("CREDIT_CARD")
    assert lab == theirs, (lab, theirs)
    return f"{len(lab)} found by both"


@check("X3", "email addresses: the same matches as Presidio")
def _():
    lab, theirs = spans("EMAIL")
    assert lab == theirs, (lab, theirs)
    return f"{len(lab)} found by both"


@check("X4", "IPv4 addresses: the same matches, including the version-number false positive")
def _():
    lab, theirs = spans("IP_ADDRESS")
    assert lab == theirs and (3, "1.2.3.4") in lab, (lab, theirs)
    return f"{len(lab)} found by both, 1.2.3.4 among them"


@check("X5", "SSNs differ exactly where the two rule sets differ")
def _():
    lab, theirs = spans("US_SSN")
    assert lab - theirs == {(2, "123-45-6789")}, lab - theirs
    assert theirs - lab == {(2, "900-12-3456")}, theirs - lab
    return ("lab only: 123-45-6789 (Presidio drops published sample numbers); "
            "Presidio only: 900-12-3456 (the lab drops 9xx areas)")


@check("X6", "US phone numbers: the same matches as Presidio")
def _():
    lab, theirs = spans("PHONE_US")
    assert lab == theirs, (lab, theirs)
    return f"{len(lab)} found by both"


@check("X7", "the only network attempts are the suffix-list download, and matching works without it")
def _():
    ex_text = "write to dana.w@example.com"
    found = EmailRecognizer().analyze(ex_text, ["EMAIL_ADDRESS"], None)
    assert [ex_text[r.start:r.end] for r in found] == ["dana.w@example.com"], found
    hosts = set(ATTEMPTS)
    assert hosts <= {"publicsuffix.org", "raw.githubusercontent.com"}, hosts
    return f"attempted: {', '.join(sorted(hosts)) or 'none'} (tldextract's fixed suffix-list URLs)"


def main():
    passed = 0
    for cid, title, fn in CHECKS:
        try:
            note = fn()
        except Exception as error:  # any failure is a FAIL line, never a crash
            print(f"FAIL  {cid} {title}\n      {type(error).__name__}: {error}")
        else:
            passed += 1
            print(f"PASS  {cid} {title}\n      {note}")
    hosts = sorted(set(ATTEMPTS))
    print(f"Network attempts blocked: {len(ATTEMPTS)}" + (f" ({', '.join(hosts)})" if hosts else ""))
    print(f"{passed} of {len(CHECKS)} cross-checks passed")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())

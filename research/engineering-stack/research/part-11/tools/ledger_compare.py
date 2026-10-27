"""Compare every column of the freshness ledger's Section 2 with pypi_fresh.py output.

Usage: python ledger_compare.py LEDGER.md PYPI_OUTPUT.txt
Read-only: prints the differences and which Python versions every package accepts.
"""
import re
import sys

from packaging.specifiers import SpecifierSet

sys.stdout.reconfigure(encoding="utf-8", newline="\n")
COLUMNS = ["version", "released", "licence", "python"]


def ledger_rows(path):
    text = open(path, encoding="utf-8").read()
    section = text.split("## 2. Python packages (PyPI)")[1].split("\n## ")[0]
    rows = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and cells[0] not in ("Package", "") and not cells[0].startswith("---"):
            rows[cells[0]] = dict(zip(COLUMNS + ["used", "note"], cells[1:]))
    return rows


def pypi_rows(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) == 5:
            rows[cells[0]] = dict(zip(COLUMNS, cells[1:]))
    return rows


def norm_licence(value):
    value = value.replace("(repository)", "").strip()
    if " AND " in value or value.startswith("compound"):
        return "compound"
    key = re.sub(r"[^a-z0-9]", "", value.lower())
    key = re.sub(r"license|software|version", "", key)
    if key in ("apache", "apache20", "apache2"):
        return "Apache-2.0"
    if key == "mit":
        return "MIT"
    return value


def norm_python(value):
    if value in ("", "not stated"):
        return ""
    clauses = []
    for clause in value.split(","):
        clause = clause.strip()
        while re.search(r"\d+\.\d+\.0$", clause):  # >=3.10.0 is >=3.10
            clause = clause[:-2]
        clauses.append(clause)
    return ",".join(sorted(clauses))


def same(column, old, new):
    if column == "licence":  # the ledger notes "(repository)" when PyPI gives none
        return norm_licence(old) == norm_licence(new) or ("(repository)" in old and new == "?")
    if column == "python":
        return norm_python(old) == norm_python(new)
    return old == new


def excluded_by(rows, minor):
    return [name for name, row in rows.items()
            if norm_python(row["python"]) and f"3.{minor}" not in SpecifierSet(norm_python(row["python"]))]


ledger = ledger_rows(sys.argv[1])
pypi = pypi_rows(sys.argv[2])
print(f"Ledger Section 2 rows: {len(ledger)}; PyPI rows: {len(pypi)}")
print(f"In the ledger only: {sorted(set(ledger) - set(pypi)) or 'none'}")
print(f"In the PyPI output only: {sorted(set(pypi) - set(ledger)) or 'none'}")
print()

changed = {}
for name in ledger:
    if name not in pypi:
        continue
    diffs = [(c, ledger[name][c], pypi[name][c]) for c in COLUMNS
             if not same(c, ledger[name][c], pypi[name][c])]
    if diffs:
        changed[name] = diffs
for column in COLUMNS:
    names = [n for n, d in changed.items() if any(c == column for c, _, _ in d)]
    print(f"{column}: {len(names)} differ")
print(f"packages with any difference: {len(changed)} of {len(ledger)}")
print()
for name, diffs in changed.items():
    print(name)
    for column, old, new in diffs:
        print(f"    {column}: {old!r} -> {new!r}")
print()

for label, rows in (("ledger", ledger), ("PyPI Oct 26", pypi)):
    print(f"Python versions accepted by all packages ({label}):")
    for minor in range(10, 16):
        names = excluded_by(rows, minor)
        print(f"    3.{minor}: " + ("all accept" if not names else "excluded by " + ", ".join(names)))

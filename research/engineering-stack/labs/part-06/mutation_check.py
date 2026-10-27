"""Break the lab on purpose, one mistake at a time, and confirm run_lab.py
catches each one. Works on a temporary copy; your files are never changed."""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
FILES = ("graph.py", "memory.py", "run_lab.py")

MUTATIONS = [  # (what goes wrong, file, original text, broken text)
    ("extractor drops the source note", "graph.py", "triples.append((subj, rel, obj, doc_id))",
     "triples.append((subj, rel, obj, 'n1'))"),
    ("resolution ignores the alias table", "graph.py", "return ALIASES.get(key, key)", "return key"),
    ("normalizing keeps upper case", "graph.py", "key = re.sub(r\"\\s+\", \" \", name.lower()).strip()",
     "key = re.sub(r\"\\s+\", \" \", name).strip()"),
    ("backwards edges walk forwards", "graph.py", "edges = self.inn[node] if backwards else self.out[node]",
     "edges = self.out[node]"),
    ("path search follows edge direction only", "graph.py",
     "for _, other, _ in self.out[node] + self.inn[node]:", "for _, other, _ in self.out[node]:"),
    ("modularity forgets the expected term", "graph.py", "q += inside[i] / m - (d / (2 * m)) ** 2",
     "q += inside[i] / m"),
    ("modularity squares with m, not 2m", "graph.py", "(d / (2 * m)) ** 2", "(d / m) ** 2"),
    ("local moving never moves a node", "graph.py", "if best_c != comm[n]:", "if False:"),
    ("merging phase switched off", "graph.py", "if gain > 1e-12 and", "if False and"),
    ("overwrite keeps the old value", "memory.py", "self.facts = [f for f in self.facts if f not in same]", "pass"),
    ("temporal mode never closes old facts", "memory.py", "f.invalid_at = fact.valid_at", "pass"),
    ("temporal mode closes newer facts too", "memory.py", "and f.valid_at < fact.valid_at", ""),
    ("as_of ignores the end date", "memory.py", "and (f.invalid_at is None or day < f.invalid_at)", ""),
    ("quarantine switched off", "memory.py", "if fact.source not in self.TRUSTED and not approved:", "if False:"),
    ("path check skips normalizing", "memory.py", "norm = posixpath.normpath(path)", "norm = path"),
    ("path check accepts look-alike folders", "memory.py",
     "if norm != root and not norm.startswith(root + \"/\"):", "if not norm.startswith(root):"),
]


def run_copy(edit=None):
    with tempfile.TemporaryDirectory() as tmp:
        for f in FILES:
            shutil.copy(HERE / f, tmp)
        if edit:
            target = pathlib.Path(tmp) / edit[1]
            text = target.read_text(encoding="utf-8")
            if edit[2] not in text:
                return "missing", ""
            target.write_text(text.replace(edit[2], edit[3], 1), encoding="utf-8")
        run = subprocess.run([sys.executable, "run_lab.py"], cwd=tmp, capture_output=True, text=True)
        first = next((l for l in run.stdout.splitlines() if l.startswith("FAIL")), "crashed")
        return ("pass" if run.returncode == 0 else "fail"), first


if run_copy()[0] != "pass":
    print("STOP the unbroken lab fails run_lab.py; fix that first")
    sys.exit(1)
print("OK   the unbroken copy passes")

caught = 0
for edit in MUTATIONS:
    outcome, first = run_copy(edit)
    if outcome == "missing":
        print(f"ERROR mutation text not found: {edit[0]}")
        continue
    caught += outcome == "fail"
    print(f"{'CAUGHT' if outcome == 'fail' else 'MISSED'} {edit[0]}: {first if outcome == 'fail' else ''}")

print(f"\n{caught} of {len(MUTATIONS)} mutations caught")
sys.exit(0 if caught == len(MUTATIONS) else 1)

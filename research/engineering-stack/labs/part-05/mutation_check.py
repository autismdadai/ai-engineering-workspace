"""Break the lab on purpose, one mistake at a time, and confirm run_lab.py
catches each one. Works on a temporary copy; your files are never changed."""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent

MUTATIONS = [  # (what goes wrong, file, original text, broken text)
    ("IDF loses Lucene's +1", "retrieval.py", "math.log(1 + (self.n - c + 0.5)", "math.log((self.n - c + 0.5)"),
    ("drop the (k1 + 1) factor", "retrieval.py", "f * (self.k1 + 1) / denom", "f / denom"),
    ("ignore document length (b)", "retrieval.py", "self.b * dl / self.avgdl", "self.b * 1"),
    ("tokenizer drops digits", "retrieval.py", r'r"[a-z0-9]+"', r'r"[a-z]+"'),
    ("dense vectors not unit length", "retrieval.py", "v / norm for k, v", "v for k, v"),
    ("RRF ranks start at 0", "retrieval.py", "enumerate(ranking, start=1)", "enumerate(ranking, start=0)"),
    ("RRF default k = 1", "retrieval.py", "def rrf(rankings, k=60", "def rrf(rankings, k=1"),
    ("RRF adds scores, not ranks", "retrieval.py", "fused[doc_id] += 1.0 / (k + rank)", "fused[doc_id] += _score"),
    ("min-max upside down", "retrieval.py", "(s - lo) / (hi - lo)", "(hi - s) / (hi - lo)"),
    ("convex weights swapped", "retrieval.py", "alpha * dn.get(d, 0.0) + (1 - alpha) * sn.get(d, 0.0)",
     "alpha * sn.get(d, 0.0) + (1 - alpha) * dn.get(d, 0.0)"),
    ("recall divides by k", "retrieval.py", "/ len(relevant) if relevant", "/ k if relevant"),
    ("precision divides by what came back", "retrieval.py", "rels.get(d, 0) > 0) / k",
     "rels.get(d, 0) > 0) / max(1, len(ranked_ids[:k]))"),
    ("MRR off by one rank", "retrieval.py", "for rank, d in enumerate(ranked_ids, start=1):\n        if rels",
     "for rank, d in enumerate(ranked_ids, start=2):\n        if rels"),
    ("nDCG ideal list not sorted", "retrieval.py", "sorted(rels.values(), reverse=True)[:k]", "list(rels.values())[:k]"),
    ("chunks lose their overlap", "retrieval.py", "piece = tail + piece", "piece = piece"),
    ("query mapped to the wrong concept", "corpus.py", '"squeaky": "noise"', '"squeaky": "water"'),
]

def control_passes():
    """The unbroken copy must pass, or a 'caught' count would mean nothing."""
    with tempfile.TemporaryDirectory() as tmp:
        for f in ("corpus.py", "retrieval.py", "run_lab.py"):
            shutil.copy(HERE / f, tmp)
        return subprocess.run([sys.executable, "run_lab.py"], cwd=tmp,
                              capture_output=True, text=True).returncode == 0


if not control_passes():
    print("STOP the unbroken lab fails run_lab.py; fix that first")
    sys.exit(1)
print("OK   the unbroken copy passes")

caught = 0
for name, filename, old, new in MUTATIONS:
    with tempfile.TemporaryDirectory() as tmp:
        for f in ("corpus.py", "retrieval.py", "run_lab.py"):
            shutil.copy(HERE / f, tmp)
        target = pathlib.Path(tmp) / filename
        text = target.read_text(encoding="utf-8")
        if old not in text:
            print(f"ERROR mutation text not found: {name}")
            continue
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        run = subprocess.run([sys.executable, "run_lab.py"], cwd=tmp, capture_output=True, text=True)
        failed = run.returncode != 0
        caught += failed
        first = next((l for l in run.stdout.splitlines() if l.startswith("FAIL")), "crashed")
        print(f"{'CAUGHT' if failed else 'MISSED'} {name}: {first if failed else ''}")

print(f"\n{caught} of {len(MUTATIONS)} mutations caught")
sys.exit(0 if caught == len(MUTATIONS) else 1)

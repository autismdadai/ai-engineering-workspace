"""Prove each check can fail: break the code on purpose, expect run_lab to fail.

Each mutation copies the lab to a temporary folder, makes one small edit,
runs run_lab.py there and expects a non-zero exit. The unbroken copy must
pass. Ends with "Every mutation behaved as expected." when all do.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

MUTATIONS = [  # (file, text to find, replacement, what it breaks)
    ("token_budget.py", "if p.must_keep]", "if False]", "must-keep parts not reserved"),
    ("token_budget.py", "key=lambda p: (-p.priority, p.order))", "key=lambda p: p.order)",
     "priority ignored"),
    ("token_budget.py", "/ growth)", ")", "growth ignored"),
    ("token_budget.py", "keep_always.add(len(messages) - 1)", "pass", "Ollama rule drops the last message"),
    ("token_budget.py", 'return {"status": 400, "kept": None, "dropped": None}',
     'return {"status": 200, "kept": [], "dropped": []}', "overflow silently accepted"),
    ("cache_cost.py", "return int(threshold) + 1", "return int(threshold)", "break-even off by one"),
    ("cache_cost.py", "write * writes + read * reads", "write + read * reads", "expired writes not charged"),
    ("cache_sim.py", 'h.update(f"{b.level}\\x00{b.text}\\x00".encode())',
     'h.update(f"{b.level}\\x00{b.tokens}\\x00".encode())', "fingerprint ignores text"),
    ("cache_sim.py", "if entry and entry[0] > now", "if entry", "expired entries still hit"),
    ("cache_sim.py", "self.entries[key] = (now + ttl, ttl)   # a hit refreshes",
     "pass  # a hit refreshes", "hits don't refresh the lifetime"),
    ("cache_sim.py", "if cum[bp] < self.minimum:", "if False:", "minimum length ignored"),
    ("cache_sim.py", "if ranks != sorted(ranks):", "if False:", "block order not checked"),
    ("placement_test.py", "and lo[e] > hi[worst]", "", "verdict ignores the intervals"),
    ("placement_test.py", "(2 * x - 1) ** 2", "0.5", "U stand-in loses its bias"),
    ("paper_numbers.py", "9: 53.8", "9: 57.8", "copied figure wrong"),
]


def run_copy(edit=None):
    with tempfile.TemporaryDirectory() as tmp:
        for path in HERE.glob("*.py"):
            shutil.copy(path, tmp)
        if edit:
            target = Path(tmp) / edit[0]
            text = target.read_text(encoding="utf-8")
            if edit[1] not in text:
                return "missing"
            target.write_text(text.replace(edit[1], edit[2], 1), encoding="utf-8")
        result = subprocess.run([sys.executable, "run_lab.py"], cwd=tmp,
                                capture_output=True, text=True, timeout=300)
        return "pass" if result.returncode == 0 else "fail"


def main():
    good = True
    control = run_copy()
    print(f"[{'OK' if control == 'pass' else 'BAD'}] unbroken copy: {control}")
    good &= control == "pass"
    for edit in MUTATIONS:
        outcome = run_copy(edit)
        ok = outcome == "fail"
        good &= ok
        print(f"[{'OK' if ok else 'BAD'}] {edit[3]} ({edit[0]}): run_lab {outcome}")
    print("Every mutation behaved as expected." if good else "Some mutations did not.")
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()

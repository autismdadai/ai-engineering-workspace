"""Prove that run_lab.py's checks can fail.

    python mutation_check.py             # all 11 mutations (M7 and M8 need PyPI)
    python mutation_check.py --offline   # skips M7 and M8

It copies this lab folder to a temporary place, damages one file on purpose
(a "mutation"), runs run_lab.py on the damaged copy, and confirms that exactly the
checks aimed at that damage fail. One harmless change must still pass every check.
A check that can't fail proves nothing. M7 and M8 rely on check 8, which downloads
pytest from PyPI; if PyPI can't be reached they are reported as BAD, not as passing.
Exit code 0 means every mutation that ran behaved as expected.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["evalkit.py", "router.py", "run_eval.py", "semantic_entropy.py", "judge_check.py",
         "check_overlap.py", "test_evals.py", "requirements.txt", "run_lab.py"]
NO_PYPI = "If this computer can't reach PyPI"  # printed by run_lab.py's check 8

# (name, file, text to find, replacement, checks expected to fail, offline?)
MUTATIONS = [
    ("M1 the Wilson interval uses 90% instead of 95%", "evalkit.py",
     "Z95 = 1.959963984540054", "Z95 = 1.6448536269514722", ["1.", "4."], True),
    ("M2 the mid-p forgets to subtract half the point probability", "evalkit.py",
     "2 * (one_sided - 0.5 * _point(k, n))", "2 * one_sided", ["1.", "3."], True),
    ("M3 kappa leaves out the correction for chance", "evalkit.py",
     "    return (p_o - p_e) / (1 - p_e)", "    return p_o", ["1.", "7."], True),
    ("M4 entropy reports bits where nats are expected", "evalkit.py",
     "def entropy(counts, base=math.e):", "def entropy(counts, base=2):", ["1.", "6."], True),
    ("M5 AUROC counts ties as wins", "evalkit.py",
     "1.0 if p > q else 0.5 if p == q else 0.0", "1.0 if p >= q else 0.0", ["1.", "6."], True),
    ("M6 answers are grouped by exact wording, not meaning", "semantic_entropy.py",
     "    return meaning(a) == meaning(b)", "    return a == b", ["6."], True),
    ("M7 the gate ignores a label's lost recall", "run_eval.py",
     "MAX_RECALL_DROP = 0.15", "MAX_RECALL_DROP = 1.0", ["3.", "8."], False),
    ("M8 the judge check forgets that B was shown first", "judge_check.py",
     'ba = underlying(row["judge_ba"], "B")', 'ba = underlying(row["judge_ba"], "A")',
     ["7.", "8."], False),
    ("M9 the overlap check misses near-copies", "evalkit.py",
     "def overlaps(test_texts, other_texts, threshold=0.8):",
     "def overlaps(test_texts, other_texts, threshold=0.95):", ["5."], True),
    ("M10 the accuracy floor is never applied", "run_eval.py",
     "    if low < ACCURACY_FLOOR:", "    if low < 0.5:", ["4."], True),
    ("M11 harmless: a reworded comment", "router.py",
     "free, instant, and the same answer every run.",
     "free, instant, and the same answer on every run.", [], True),
]


def apply(folder, file_name, find, replace):
    path = os.path.join(folder, file_name)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.count(find) != 1:
        raise SystemExit(f"Mutation target not found exactly once in {file_name}: {find!r}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(find, replace))


def failed_checks(output):
    return [line.split()[1] for line in output.splitlines() if line.startswith("FAIL ")]


def main():
    parser = argparse.ArgumentParser(description="Prove that run_lab.py's checks can fail.")
    parser.add_argument("--offline", action="store_true", help="skip M7 and M8 (PyPI)")
    args = parser.parse_args()
    bad, skipped, no_pypi = [], [], []
    for name, file_name, find, replace, expected, offline in MUTATIONS:
        if args.offline and not offline:
            skipped.append(name.split()[0])
            print(f"SKIP {name}: needs PyPI")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "data"))
            for item in FILES:
                shutil.copy(os.path.join(HERE, item), tmp)
            for item in os.listdir(os.path.join(HERE, "data")):
                shutil.copy(os.path.join(HERE, "data", item), os.path.join(tmp, "data"))
            apply(tmp, file_name, find, replace)
            command = [sys.executable, os.path.join(tmp, "run_lab.py")]
            if offline:
                command.append("--offline")
            done = subprocess.run(command, cwd=tmp, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=900)
            failed = failed_checks(done.stdout)
            ok = failed == expected and (done.returncode != 0) == bool(expected)
            note = ""
            if NO_PYPI in done.stdout:  # check 8 failed for lack of PyPI, not the mutation
                ok, note = False, " (check 8 couldn't reach PyPI, so this proves nothing)"
                no_pypi.append(name.split()[0])
            elif not ok:
                bad.append(name.split()[0])
            print(f"{'OK  ' if ok else 'BAD '} {name}: failed checks {failed or 'none'}, "
                  f"expected {expected or 'none'}{note}")
    if bad:
        print("\nSome mutation did not behave as expected: a check may be unable to fail.")
    if no_pypi:
        print(f"\n{' and '.join(no_pypi)} couldn't reach PyPI. Run again online, "
              "or run python mutation_check.py --offline to skip them.")
    if not bad and not no_pypi:
        print(f"\nEvery mutation that ran behaved as expected ({' and '.join(skipped)} skipped)."
              if skipped else "\nEvery mutation behaved as expected.")
    return 0 if not bad and not no_pypi else 1


if __name__ == "__main__":
    sys.exit(main())

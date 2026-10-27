"""Run the Part 02 lab end to end and check every result.

    python run_lab.py            # all 8 checks (check 8 downloads pytest from PyPI)
    python run_lab.py --offline  # skips check 8

Check 1 tests the statistics against reference values; checks 2 to 8 repeat the
lab's steps 1 to 7. It works on a copy of this folder in a temporary place and
deletes it afterwards, so it changes nothing here. Each check prints PASS or FAIL.
The "break it" checks damage something on purpose and pass only when the damage is
noticed, which proves the check can fail. Exit code 0 means every check passed.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["evalkit.py", "router.py", "run_eval.py", "semantic_entropy.py", "judge_check.py",
         "check_overlap.py", "test_evals.py", "requirements.txt"]
results = []


def step(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if detail and not ok:
        print("      " + detail.strip()[-1500:].replace("\n", "\n      "))


def run(command, cwd, extra_env=None):
    """Run a command; return (exit code, everything it printed)."""
    env = dict(os.environ, PYTHONUTF8="1", **(extra_env or {}))
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=900)
    return done.returncode, done.stdout + done.stderr


def script(work, name, *args, extra_env=None):
    return run([sys.executable, os.path.join(work, name), *args], work, extra_env)


def close(a, b):
    return abs(a - b) < 1e-9


def check_statistics(work):
    sys.path.insert(0, work)
    import evalkit
    # Reference values, cross-checked against scikit-learn 1.9.1, statsmodels 0.15.0
    # and SciPy 1.18.1 when this lab was written.
    checks = [
        ("Wilson 48/60", evalkit.wilson_interval(48, 60), (0.6821819419, 0.8817149468)),
        ("Wilson 12/15", evalkit.wilson_interval(12, 15), (0.5481455128, 0.9295245065)),
        ("McNemar 6 vs 4", evalkit.mcnemar(6, 4), (0.75390625, 0.548828125)),
        ("McNemar 6 vs 0", evalkit.mcnemar(6, 0), (0.03125, 0.015625)),
        ("McNemar 3 vs 3", evalkit.mcnemar(3, 3), (1.0, 0.84375)),
        ("kappa", (evalkit.cohen_kappa(list("AABBA"), list("ABBBA")),), (0.6153846154,)),
        ("entropy 6/3/1", (evalkit.entropy([6, 3, 1]), evalkit.entropy([6, 3, 1], 2)),
         (0.8979457249, 1.2954618442)),
        ("AUROC", (evalkit.auroc([0.9, 0.0, 0.0, 0.3], [True, True, False, False]),), (0.625,)),
        ("pass@k", (evalkit.pass_at_k(10, 3, 1), evalkit.pass_at_k(10, 3, 5)),
         (0.3, 0.9166666667)),
    ]
    wrong = [name for name, got, want in checks
             if not all(abs(g - w) < 1e-9 for g, w in zip(got, want))]
    sys.path.remove(work)
    step("1. evalkit's statistics match the reference values", not wrong,
         "Mismatched: " + ", ".join(wrong))


def check_gate(work):
    code, out = script(work, "run_eval.py")
    step("2. The version in use (v1) passes its own gate", code == 0 and "GATE: PASS" in out, out)
    code, out = script(work, "run_eval.py", "--candidate", "v2")
    ok = (code == 1 and "account: recall fell 42.9 points" in out
          and "McNemar mid-p 0.549" in out and "overall:" not in out)
    step("3. Break it: v2 fails the gate on account recall, which overall accuracy "
         "can't show", ok, out)
    code, out = script(work, "run_eval.py", "--limit", "15")
    ok = code == 1 and "54.8%, is below the 60.0% floor (15 tickets)" in out
    step("4. Break it: with 15 tickets, 12 right can't show the 60% floor", ok, out)


def check_overlap_step(work):
    code, out = script(work, "check_overlap.py")
    planted = os.path.join(work, "examples-with-a-test-ticket.jsonl")
    shutil.copy(os.path.join(work, "data", "examples.jsonl"), planted)
    with open(planted, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": "e9", "label": "technical",
                            "text": "The editor crashes every time I paste in a table."}) + "\n")
    code2, out2 = script(work, "check_overlap.py", "--examples", planted)
    ok = code == 0 and code2 == 1 and "t02:" in out2
    step("5. No test ticket is in the prompt's examples, and a planted near-copy is caught",
         ok, out + out2)


def check_semantic_entropy(work):
    code, out = script(work, "semantic_entropy.py")
    lines = out.splitlines()
    ok = (code == 0 and "Flagged (semantic entropy above 0.6 nats): q4, q5, q6" in lines
          and "Wrong but not flagged: q7" in lines and "semantic entropy 0.8125" in out)
    step("6. Semantic entropy flags the three arbitrary answers and misses the "
         "consistently wrong one", ok, out)


def check_judge(work):
    code, out = script(work, "judge_check.py")
    code2, out2 = script(work, "judge_check.py", "--always-first")
    ok = (code == 0 and "Cohen's kappa 0.689" in out and code2 == 1
          and "consistency 0.0% is below 80%" in out2)
    step("7. The recorded judge passes, and a judge that always picks the first "
         "answer fails", ok, out + out2)


def check_pytest(work):
    venv = os.path.join(work, ".venv-lab")
    code, out = run([sys.executable, "-m", "venv", venv], work)
    python = os.path.join(venv, *(("Scripts", "python.exe") if os.name == "nt" else ("bin", "python")))
    code, out = run([python, "-m", "pip", "install", "--no-cache-dir", "--require-hashes",
                     "-r", "requirements.txt"], work)
    if code != 0:
        step("8. pytest runs the gate: it passes for v1 and fails for v2", False,
             out + "\nIf this computer can't reach PyPI, run: python run_lab.py --offline")
        return
    code1, out1 = run([python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_evals.py"],
                      work, {"CANDIDATE": "v1"})
    code2, out2 = run([python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_evals.py"],
                      work, {"CANDIDATE": "v2"})
    ok = (code1 == 0 and "5 passed" in out1 and code2 == 1 and "1 failed, 4 passed" in out2
          and "test_no_label_loses_recall" in out2)
    step("8. pytest runs the gate: it passes for v1 and fails for v2", ok, out1 + out2)


def main():
    parser = argparse.ArgumentParser(description="Run the Part 02 lab and check it.")
    parser.add_argument("--offline", action="store_true", help="skip check 8 (PyPI)")
    args = parser.parse_args()
    print(f"Part 02 lab, run with Python {sys.version.split()[0]}\n")
    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, "lab")
        os.makedirs(os.path.join(work, "data"))
        for name in FILES:
            shutil.copy(os.path.join(HERE, name), work)
        for name in os.listdir(os.path.join(HERE, "data")):
            shutil.copy(os.path.join(HERE, "data", name), os.path.join(work, "data"))
        check_statistics(work)
        check_gate(work)
        check_overlap_step(work)
        check_semantic_entropy(work)
        check_judge(work)
        if args.offline:
            print("SKIP  8. pytest check (--offline)")
        else:
            check_pytest(work)
    print(f"\n{sum(results)} of {len(results)} checks passed.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

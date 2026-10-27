"""Prove that run_lab.py's checks can fail.

    python mutation_check.py

It copies this lab folder to a temporary place, damages one file on purpose
(a "mutation"), runs run_lab.py on the damaged copy, and confirms that the step
aimed at that damage fails. One harmless change must still pass every step.
A check that can't fail proves nothing. Exit code 0 means every mutation behaved
as expected. Mutations M5 and M6 download from PyPI; the rest run offline.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["check_setup.py", "run_lab.py", "read_key.py", "requirements.txt",
         "requirements-one-hash-wrong.txt", "requirements-all-hashes-wrong.txt",
         ".gitignore", ".env.example"]

# (name, file, text to find, replacement, steps expected to fail, offline?)
MUTATIONS = [
    ("M1 .gitignore no longer lists .env", ".gitignore",
     "# Secrets: never commit these\n.env\n", "# Secrets: never commit these\n",
     ["5."], True),
    ("M2 read_key.py prints the key", "read_key.py",
     "({len(value)} characters). Its value is not shown.", ": {value}",
     ["7."], True),
    ("M3 read_key.py accepts the placeholder", "read_key.py",
     "    if value == PLACEHOLDER:", "    if value == 'never-matches':",
     ["7."], True),
    ("M4 check_setup.py never reports a .env problem", "check_setup.py",
     'report("FAIL", "Git would NOT ignore a .env file here; add .env to .gitignore")',
     'report("PASS", "Git ignores .env in this folder")',
     ["6."], True),
    ("M5 requirements.txt pins hashes that match no file", "requirements.txt",
     "cd1c \\", "cd1d \\",
     ["2.", "3.", "4."], False),
    ("M6 the all-wrong file has correct hashes again", "requirements-all-hashes-wrong.txt",
     "cd1d \\", "cd1c \\",
     ["4."], False),
    ("M7 harmless: a reworded comment", "check_setup.py",
     "# oldest version every package in the series accepts",
     "# the oldest version that every package in the series accepts",
     [], True),
]


def apply(folder, file_name, find, replace):
    path = os.path.join(folder, file_name)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.count(find) != 1:
        raise SystemExit(f"Mutation target not found exactly once in {file_name}: {find!r}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(find, replace))


def failed_steps(output):
    return [line.split()[1] for line in output.splitlines() if line.startswith("FAIL ")]


def main():
    all_ok = True
    for name, file_name, find, replace, target, offline in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            for item in FILES:
                shutil.copy(os.path.join(HERE, item), tmp)
            apply(tmp, file_name, find, replace)
            if name.startswith("M5"):
                # Break the second hash too, so no file on PyPI matches.
                apply(tmp, "requirements.txt", "ed79\n", "ed7a\n")
            if name.startswith("M6"):
                # Restore the second hash too, so the "broken" file installs.
                apply(tmp, "requirements-all-hashes-wrong.txt", "ed7a\n", "ed79\n")
            command = [sys.executable, os.path.join(tmp, "run_lab.py")]
            if offline:
                command.append("--offline")
            done = subprocess.run(command, cwd=tmp, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=900)
            failed = failed_steps(done.stdout)
            expected = target
            ok = failed == expected and (done.returncode != 0) == bool(expected)
            all_ok = all_ok and ok
            print(f"{'OK  ' if ok else 'BAD '} {name}: failed steps {failed or 'none'}, "
                  f"expected {expected or 'none'}")
    print("\nEvery mutation behaved as expected." if all_ok
          else "\nSome mutation did not behave as expected: a check may be unable to fail.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

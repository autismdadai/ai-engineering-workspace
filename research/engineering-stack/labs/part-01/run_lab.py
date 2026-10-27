"""Run the Part 01 lab end to end and check every result.

    python run_lab.py            # every step (needs internet access to PyPI)
    python run_lab.py --offline  # skips the three steps that download a package

It works in a temporary folder and deletes it afterwards, so it changes nothing
in this folder or in your Python installation. Each step prints PASS or FAIL.
The "break it" steps damage something on purpose and pass only when the check
notices the damage, which proves the check can fail. Exit code 0 means every
step passed.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS = os.path.join(HERE, "requirements.txt")
PINNED_VERSION = "26.3"  # the version pinned in requirements.txt
results = []


def step(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if detail and not ok:
        print("      " + detail.strip().replace("\n", "\n      "))


def run(command, cwd=None, extra_env=None, drop_env=()):
    """Run a command; return (exit code, stdout, stderr)."""
    env = dict(os.environ, PYTHONUTF8="1")
    for name in drop_env:
        env.pop(name, None)
    env.update(extra_env or {})
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=900)
    return done.returncode, done.stdout, done.stderr


def make_venv(folder):
    """Create a fresh virtual environment and return the path to its Python."""
    code, out, err = run([sys.executable, "-m", "venv", folder])
    if code != 0:
        raise RuntimeError("Could not create a virtual environment:\n" + out + err)
    parts = ("Scripts", "python.exe") if os.name == "nt" else ("bin", "python")
    return os.path.join(folder, *parts)


def pip_install(python, requirements_file):
    return run([python, "-m", "pip", "install", "--no-cache-dir",
                "--require-hashes", "-r", requirements_file])


def break_hashes(text, every=False):
    """Change the last character of the first sha256 hash, or of every one."""
    marker = "--hash=sha256:"
    position = 0
    while True:
        start = text.find(marker, position)
        if start == -1:
            return text
        end = start + len(marker) + 64
        last = text[end - 1]
        swapped = "0" if last == "f" else format(int(last, 16) + 1, "x")
        text = text[:end - 1] + swapped + text[end:]
        if not every:
            return text
        position = end


def lab_setup_check():
    code, out, err = run([sys.executable, os.path.join(HERE, "check_setup.py")], cwd=HERE)
    step("1. The setup check reports no FAIL lines", code == 0, out[-1500:] + err)


def shipped_matches(file_name, expected_text):
    """Is a shipped broken file exactly requirements.txt with the expected change?"""
    with open(os.path.join(HERE, file_name), encoding="utf-8") as f:
        shipped = [line for line in f.read().splitlines() if not line.startswith("#")]
    expected = [line for line in expected_text.splitlines() if not line.startswith("#")]
    return shipped == expected


def lab_hashes(tmp):
    python = make_venv(os.path.join(tmp, "good-venv"))
    code, out, err = pip_install(python, REQUIREMENTS)
    detail = out[-1500:] + err[-1500:]
    ok = code == 0
    if ok:
        code, version, err = run([python, "-c", "import packaging; print(packaging.__version__)"])
        ok = code == 0 and version.strip() == PINNED_VERSION
        detail = f"installed version: {version.strip()} {err}"
    else:
        detail += "\nIf this computer can't reach PyPI, run: python run_lab.py --offline"
    step(f"2. The hash-pinned install succeeds and gives packaging {PINNED_VERSION}", ok, detail)

    with open(REQUIREMENTS, encoding="utf-8") as f:
        original = f.read()

    one_wrong = os.path.join(HERE, "requirements-one-hash-wrong.txt")
    same_change = shipped_matches("requirements-one-hash-wrong.txt", break_hashes(original))
    python = make_venv(os.path.join(tmp, "one-wrong-venv"))
    code, out, err = pip_install(python, one_wrong)
    version = run([python, "-c", "import packaging; print(packaging.__version__)"])[1].strip()
    fell_back = (code == 0 and "packaging-26.3.tar.gz" in out
                 and "packaging-26.3-py3-none-any.whl" not in out.split("Created wheel")[0]
                 and version == PINNED_VERSION)
    step("3. Break it: with only the wheel's hash wrong, pip skips the wheel and "
         "builds from the source archive, whose hash still matches", same_change and fell_back,
         ("" if same_change else "requirements-one-hash-wrong.txt is not requirements.txt "
          "with only the first hash changed.\n") + out[-1500:] + err[-1500:])

    all_wrong = os.path.join(HERE, "requirements-all-hashes-wrong.txt")
    same_change = shipped_matches("requirements-all-hashes-wrong.txt",
                                  break_hashes(original, every=True))
    python = make_venv(os.path.join(tmp, "all-wrong-venv"))
    code, out, err = pip_install(python, all_wrong)
    refused = code != 0 and "DO NOT MATCH THE HASHES" in (out + err).upper()
    not_installed = run([python, "-c", "import packaging"])[0] != 0
    step("4. Break it: with every hash wrong, pip refuses to install anything",
         same_change and refused and not_installed,
         ("" if same_change else "requirements-all-hashes-wrong.txt is not requirements.txt "
          "with every hash changed.\n") + out[-1500:] + err[-1500:])


def lab_secrets(tmp):
    git = shutil.which("git")
    if git is None:
        step("5. Git ignores .env", False, "Git not found; install it first")
        step("6. Break it: un-ignoring .env is caught", False, "Git not found")
        return
    repo = os.path.join(tmp, "repo")
    os.mkdir(repo)
    shutil.copy(os.path.join(HERE, ".gitignore"), repo)
    shutil.copy(os.path.join(HERE, ".env.example"), repo)
    with open(os.path.join(repo, ".env"), "w", encoding="utf-8") as f:
        f.write("EXAMPLE_API_KEY=test-value-not-a-real-key\n")
    run([git, "init", "-q"], cwd=repo)

    def untracked_files():
        code, out, err = run([git, "status", "--porcelain", "--untracked-files=all"], cwd=repo)
        return [line[3:] for line in out.splitlines() if line.startswith("??")]

    ignored = run([git, "check-ignore", "-q", ".env"], cwd=repo)[0] == 0
    example_kept = run([git, "check-ignore", "-q", ".env.example"], cwd=repo)[0] == 1
    listed = untracked_files()
    step("5. Git ignores .env but keeps .env.example",
         ignored and example_kept and ".env" not in listed and ".env.example" in listed,
         f"untracked files Git would offer to commit: {listed}")

    with open(os.path.join(repo, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("# The .env lines were removed on purpose\n__pycache__/\n")
    listed = untracked_files()
    code, out, err = run([sys.executable, os.path.join(HERE, "check_setup.py")], cwd=repo)
    caught = (".env" in listed and code == 1
              and "Git would NOT ignore a .env file here" in out)
    step("6. Break it: with .env removed from .gitignore, Git would commit it, "
         "and check_setup.py reports FAIL", caught,
         f"untracked files: {listed}; check_setup.py exit code {code}")


def lab_key_reader(tmp):
    folder = os.path.join(tmp, "keys")
    os.mkdir(folder)
    script = os.path.join(HERE, "read_key.py")
    no_key = run([sys.executable, script], cwd=folder, drop_env=["EXAMPLE_API_KEY"])[0]
    shutil.copy(os.path.join(HERE, ".env.example"), os.path.join(folder, ".env"))
    placeholder = run([sys.executable, script], cwd=folder, drop_env=["EXAMPLE_API_KEY"])[0]
    fake_key = "test-value-not-a-real-key-7f3a"
    code, out, err = run([sys.executable, script], cwd=folder,
                         extra_env={"EXAMPLE_API_KEY": fake_key})
    ok = no_key == 2 and placeholder == 2 and code == 0 and fake_key not in out + err
    step("7. read_key.py refuses a missing or placeholder key and never prints a real one",
         ok, f"exit codes: missing {no_key}, placeholder {placeholder}, set {code}; output: {out}")


def main():
    parser = argparse.ArgumentParser(description="Run and check the Part 01 lab.")
    parser.add_argument("--offline", action="store_true",
                        help="skip the three steps that download from PyPI")
    args = parser.parse_args()
    print(f"Part 01 lab, run with Python {sys.version.split()[0]}\n")
    lab_setup_check()
    with tempfile.TemporaryDirectory() as tmp:
        if args.offline:
            print("SKIP  2, 3 and 4 (offline)")
        else:
            lab_hashes(tmp)
        lab_secrets(tmp)
        lab_key_reader(tmp)
    print(f"\n{sum(results)} of {len(results)} steps passed.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

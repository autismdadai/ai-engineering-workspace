# Part 01 lab: a safe starter project

From *The AI Engineering Stack*, Part 01 (claude/engineering-stack-part-01-setup.md in the "Prompting" project). The part explains every step; this file is the short version.

- **Goal:** a project folder with its own virtual environment, one package installed from a hash-pinned requirements file, and a `.env` file that Git ignores.
- **Time:** about 20 minutes by hand, or 1 minute for the automated check.
- **Cost:** none. No account, API key or payment.
- **Needs:** Python 3.11 to 3.13 (3.13 recommended), Git, and internet access to PyPI for steps 2 to 4. Node.js is checked but not required yet.
- **Pinned:** `packaging==26.3` with the SHA-256 hashes PyPI published for its two files (read October 9, 2026).
- **Tested:** Linux (Ubuntu 24.04 in a cloud container), Git 2.43.0, October 9, 2026, with Python 3.13.16 (pip 26.2.1) and with Ubuntu's own Python 3.12.3 (pip 24.0): 7 of 7 steps passed, and all 7 mutations behaved as expected. Windows and macOS are not yet tested.

## Run it

Open a terminal in this folder, with your virtual environment active, and run:

```
python check_setup.py
python run_lab.py
python mutation_check.py
```

| Command | What it does | Expected last line |
|---|---|---|
| `python check_setup.py` | Reads your setup and prints PASS, WARN, FAIL and INFO lines. Installs nothing. | `Ready for the labs.` |
| `python run_lab.py` | Runs the lab in a temporary folder, including three steps that break something on purpose. Add `--offline` to skip the three download steps. | `7 of 7 steps passed.` |
| `python mutation_check.py` | Damages copies of these files one at a time and confirms the matching check fails. | `Every mutation behaved as expected.` |

On macOS and Linux, use `python3` instead of `python` if no virtual environment is active.

## Files

Names starting with a dot are hidden by default: `ls -a` (macOS, Linux) or `Get-ChildItem -Force` (PowerShell) shows them. Test hash failures in a fresh virtual environment, because pip skips packages that are already installed.

| File | Purpose |
|---|---|
| `check_setup.py` | The setup check (standard library only) |
| `requirements.txt` | One package, pinned with hashes |
| `requirements-one-hash-wrong.txt` | The same, with the wheel's hash broken on purpose |
| `requirements-all-hashes-wrong.txt` | The same, with every hash broken on purpose |
| `.gitignore` | Keeps `.env` and any `.venv...` folder out of Git; keeps `.env.example` in |
| `.env.example` | A placeholder key line to copy into `.env` |
| `read_key.py` | Reads a key from the environment or `.env` without printing it |
| `run_lab.py` | The automated lab and its checks |
| `mutation_check.py` | Proof that the checks can fail |

## Safety

No lab needs a real API key. `.env.example` holds a placeholder. If you ever put a real key in `.env`, keep it out of chats, screenshots and commits; if one leaks, revoke it first.

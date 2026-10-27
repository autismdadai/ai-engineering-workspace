# Part 08 beginner-tester report

Date: October 14, 2026. Document: engineering-stack-part-08-agents.md. Lab zip md5 9309cf1ff5e2bc0bed550b50819c423c (unchanged; nothing under /home/claude/part08 was modified except this file).
Platform: Linux (Ubuntu-style container), bash. Each run used a fresh scratch "home" with its own ai-stack folder, the Section 7 unzip command (`python3 -m zipfile -e <zip> <ai-stack>`) and a fresh `.venv`. OPENAI_API_KEY was not set.

## Python versions and final lines

| Python | run_lab.py | mutation_check.py | crosscheck.py |
|---|---|---|---|
| 3.12.3 (/usr/bin/python3.12) | `21 of 21 checks passed` | `20 of 20 mutations caught` | `3 of 3 cross-checks passed` |
| 3.11.17 (python3.11) | `21 of 21 checks passed` | `20 of 20 mutations caught` | `3 of 3 cross-checks passed` |
| 3.13.16 (python3) | `21 of 21 checks passed` | `20 of 20 mutations caught` | `3 of 3 cross-checks passed` |

run_lab.py output was byte-identical across the three versions. 7.4 (SDK install) was done on all three; mutation_check took about 17 s, run_lab.py about 1 s.

Network check: crosscheck.py on 3.12 was run under strace (`-f -e trace=connect`) and with a socket.connect/getaddrinfo hook: zero connect calls and zero DNS lookups. No "Tracing request failed" or any other warning appeared on any version.

## Steps that matched the text exactly

- 7.3 unzip and venv, `python run_lab.py` (21 of 21), exit code 0.
- Step 2 `demo.py` part 1: order of calls and results matches; log matches.
- Step 3 break: the quoted line exists once in stand_in.py; after changing True to False, demo printed `result for t3: refunded 250 on order A17` and `('issue_refund', 'ok')` with the unchanged "so I didn't issue it" message; run_lab.py printed `FAIL 3 ... default: ok; approved: ok` and `20 of 21 checks passed` (exit 1). Changing it back restored 21 of 21.
- Step 5 `sandbox_check.py` (--privileged, hardened command joined onto one line in single quotes), step 6 and 7 (demo part 3, not_a_sandbox: True), mutation_check sample output, B1 to B3.
- Exercise 1 prints `(12000, 75000)`. Exercise 2 is check 5 (PASS). Exercise 3 reports `host_network` and `root_user`, exit 1.
- The appendix listing of agent_loop.py is identical to the file in the zip (186 lines).

## Problems

### P1 (medium) Exercises 1 and 3 do not say where to run them
Section 9, Exercise 1: "Check: `python -c "from agent_loop import context_tokens; print(context_tokens(3000, 1000, 10))"` prints `(12000, 75000)`".
Did: ran it from ai-stack (one folder above the lab folder), as a beginner who has closed the lab terminal might.
Saw: `ModuleNotFoundError: No module named 'agent_loop'`.
Fix: add "from inside the lab folder, with the virtual environment active". Same for Exercise 3's `python sandbox_check.py ...` (that gives the "can't open file" error).

### P2 (medium) "Exit code" is used in several places but never explained or shown
Quotes: 7.6 "exit code 0 only if all pass"; Step 5 "exits with code 1"; Exercise 3 "it exits with code 1".
Did: nothing in the text says how to see it. In bash it is `echo $?`; in PowerShell `$LASTEXITCODE`; in cmd `echo %errorlevel%`.
Fix: one sentence in 7.6 or Step 5 with the three commands, and a one-line definition ("a number a program returns; 0 means success").

### P3 (medium) Section 7.7 tracing row does not match what I saw without a key
Quote: "`[non-fatal] Tracing request failed` | You used the SDK in your own script with tracing on and no key: it tried to upload traces to OpenAI".
Did: copied crosscheck.py, removed both tracing-off lines, ran it on 3.12 with no key.
Saw: the SDK printed `OPENAI_API_KEY is not set, skipping trace export`, not "Tracing request failed", and made no upload. (The copy then crashed on `import agent_loop` only because I ran it from another folder; unrelated.)
Fix: say the message you get with no key is "skipping trace export", and that "Tracing request failed" is seen when a key is set but the upload fails, or whatever the source check showed. Say which case was tested, or tag it [R]/[U] if it was not reproduced.

### P4 (medium) Wrong section cross-references inside the lab files
- sandbox_check.py docstring (printed when you run it with no argument or unquoted): "gVisor's documentation (Part 08, Section 3.6)". Containers are Section 3.7; Section 3.6 is "Does it work? Measuring agents".
- screen_agent.py docstring: "(Part 08, Section 3.8)". Computer use is Sections 3.10 and 3.11; 3.8 is gVisor and Firecracker.
Fix: change to 3.7 and 3.10/3.11 and re-zip. A beginner who follows the pointer lands on the wrong topic.

### P5 (medium) 7.7 row "expected a command starting with 'docker run'" does not appear when quotes are missing
Quote: "`error: expected a command starting with 'docker run'` | `sandbox_check.py` was given another command, or the quotes were missing".
Did: `python sandbox_check.py docker run --privileged img` (no quotes).
Saw: the usage/docstring text (starting "Review a `docker run` command for running untrusted agent code.") and exit code 2, no JSON, no "error:" line. The error line only appears for a non-docker command such as `"ls -l"`.
Fix: say that missing quotes show the usage text, or make the script print the error line in that case.

### P6 (medium) Step 5 and 7.5: command joining and a confusing sentence
- Step 5: "Try the hardened command from Section 3.7, joined onto one line and put in single quotes". A beginner must remove the `\` characters and line breaks and keep `"$PWD/task:/work:ro"` intact. It worked for me, but a ready-to-paste one-line version in Step 5 would remove the risk. On Windows PowerShell, single quotes around text with inner double quotes can be passed differently to python (untested, [R]).
- 7.5: "check what the code inside can reach: `python -c "import urllib.request; urllib.request.urlopen('https://example.com')"` as `main.py`". The command is written as a shell command, but "as main.py" means the code is the content of main.py (without `python -c`). Reword: "put `import urllib.request` and the `urlopen(...)` line in task/main.py".

### P7 (low) 7.3 may not work on a fresh Ubuntu
Quote: "The same commands as macOS, with `python3` in place of `python3.13`".
Did: `python3 -m venv .venv` worked here. On a stock Ubuntu 24.04 desktop or server, `python3 -m venv` can fail with "ensurepip is not available ... install python3-venv" unless the package is installed (not reproduced here).
Fix: add "if you see 'ensurepip is not available', run `sudo apt install python3-venv` (needs administrator rights), or see Part 01." Also tell the reader that `python3` must be 3.11 to 3.13 (`python3 -V`); the text says so only in a clause.

### P8 (low) Step 4 note about shortened lines is inaccurate
Quote: "(`...` and `[...]` shorten lines that `run_lab.py` prints in full.)"
Saw: run_lab.py itself cuts several lines mid-word, e.g. `PASS 2 ... No tool named 'delete_everything'. Available: broken_tool, i` and `['Invalid arguments: missing required argu', "Invalid arguments: argument 'path' must "]`. The doc shows `No tool named ...` and `[...]`; also check 8 and 2c are printed in full. Not wrong enough to confuse, but "prints in full" is false.
Fix: "shortened with ... here; run_lab.py cuts long details to about 40 characters itself."

### P9 (low) Placeholder left in the document
Section "Checks run on this part": "To be filled after Phase 4." The header (line 3) says tags are counted "in Sections 1 to 12 and the checks after them". Fill it (or remove) before release.

### P10 (low) Package count differs on 3.11
7.4: "38 packages besides pip in a fresh environment on Python 3.12". On 3.12 and 3.13 I counted 38 (3.13: same as 3.12); on 3.11.17 `pip list` showed one more (39 besides pip). Say "about 38 to 39" or "38 on 3.12".

### P11 (low) sandbox_check exit code and "ok" can disagree
`python sandbox_check.py "docker run img"` prints `"ok": false` (8 missing options) but exits 0, because only dangerous options set exit 1. The text (7.6) does say "exit code 1 if anything dangerous is present", so it is documented, but a beginner who reads `"ok": false` and sees `$?` = 0 may be confused. Consider a one-line note in Step 5.

### P12 (low) mutation_check: step 4 and Section 8 intro do not say what the 60 second limit is for
Section 8 says "a 60-second limit" only in the last paragraph, after the run. mutation_check took 17 s here, so a slow machine could still be fine, but the "Time: under a minute automated" line plus a 60 s per-run limit may look like a contradiction on slow computers. Low.

### P13 (low) Windows and macOS steps (read only, not run)
- 7.1: `py -V:3.13` fails if only 3.12 or 3.11 is installed (error from py launcher); the text covers this for macOS (7.2: "use the 3.11 or 3.12 you installed") but not for Windows.
- 7.1 says "Check 2d waits half a second for a slow tool on purpose." fine, but this is the only place the delay is explained; Linux readers (7.3) never see it.
- 7.2 and 7.1 assume the lab folder is at `~/ai-stack/...`/`$HOME\ai-stack\...`; a reader who extracted to Downloads gets "can't find the path" with no 7.7 row for `cd` failures (only for the Python file error).
- 7.5: "restart Docker" and "`sudo runsc install`" are fine as warned.

## Terms a beginner would not understand (not defined where first used, or only in the glossary)

stand-in (Section 8 explains it only after use), harness, `stop_reason`, `tool_use`, `is_error`, mutation / "mutation check" (Section 7.6 and 8; never defined in plain words), "caught" (what it means for a mutation), exit code, JSON, `exec` and "builtins", loopback device, tmpfs, seccomp, cgroups, namespaces, user space, "virtual machine", "pip cache", "tracing" (OpenAI), "SDK", "pass^k", ASR, "allowlist", "token budget" vs "turn cap" in Section 7.6 (defined in 3.3, far from the lab), `$PWD`, `rm -rf` (7.8, destructive; works as described).

## Other notes

- 7.8 uninstall worked: `deactivate`, `cd ..`, `rm -rf engineering-stack-lab-part-08` (done on the 3.13 copy). I did not run `pip cache purge` because the pip cache here (332 MB) is shared; `pip cache info` works.
- README.md in the zip repeats the quick start correctly (21 / 20 / 3).
- No account, key or network use was needed at any point.

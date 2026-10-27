# Part 09 beginner-tester report

Tester: careful beginner persona who knows a little Python and follows Sections 7, 8 and 9 literally. Date: October 15, 2026.
Machine: the test container (Ubuntu, Python 3.13.16 as `python3`, `/usr/bin/python3.12` 3.12.3, `/usr/bin/python3.11` 3.11.17). Learner home: /home/claude/tester9; series folder /home/claude/tester9/ai-stack.
Virtual environments: `.venv313`, `.venv312`, `.venv311` inside the lab folder (the doc's `.venv` name would collide). Nothing under /home/claude/part09 was edited except this report.

## Summary

Everything the document promises ran and matched on all three Pythons: 30 of 30 checks, 6 of 6 cross-checks, 33 of 33 mutations, every quoted output in Sections 5, 8 and 9, the 41-package count, and the uninstall steps. No high-severity problems. The problems are beginner traps and small wrong details.

| Severity | Count |
|---|---|
| High | 0 |
| Medium | 5 |
| Low | 16 |

## What ran, and what it printed

| Step | 3.13.16 | 3.12.3 | 3.11.17 | Matches the doc? |
|---|---|---|---|---|
| Unzip (Section 7, Linux), from the zip's folder: `python3 -m zipfile -e engineering-stack-lab-part-09.zip /home/claude/tester9/ai-stack` | exit 0; `ai-stack` did not exist and was created; 10 files | | | Yes. Appendix `workflow.py` is byte-identical to the zip's copy |
| 7.3 `python run_lab.py` | 30 of 30, exit 0 | 30 of 30, exit 0 | 30 of 30, exit 0 | Yes; the five abridged lines in Section 8's expected output match character for character |
| 7.4 `pip install -r requirements-crosscheck.txt` | ok, pip 26.2.1, no notice | ok, pip 24.0, `[notice] A new release of pip is available: 24.0 -> 26.2.1` | same as 3.12 | Yes |
| 7.4 `pip freeze \| wc -l` | 41 | 41 | 41 | Yes, "41 packages" |
| 7.4 `python crosscheck.py` | 6 PASS, `6 of 6 cross-checks passed`, exit 0 | same | same | Yes |
| Network audit of crosscheck (Python audit hook on all `socket.*` events) | 1 event: `socket.__new__` AF_INET6, from urllib3's import-time `HAS_IPV6 = _has_ipv6("::1")` probe (binds to localhost, never connects). No `socket.connect`, no `socket.getaddrinfo` | same | same | Nothing tried to reach the network; no errors |
| 8.2 `python demo.py` | every quoted line in Section 5 and 3.9 matches: `status interrupted after 5 steps; model small-model; drafts 2`, the pending dict, the retry log entry, `waited 0.07 s`, `status done; refund rf_1`, `charges at the payment service: 1`, the step counts dict, `charges: 2`, 63,900 / 3,900 / 60,000, 77.4%, 68.7%, 60.1% | same | same | Yes |
| 8.3 first `python -c` | `interrupted {'action': 'refund', 'order': 'A17', 'amount': 250}`; `my-checkpoints/A17.json` created | same | same | Yes |
| 8.3 second `python -c` | `done rf_1` | same | same | Yes |
| 8.4 edit, run, revert | FAIL 2c, FAIL 2d, `28 of 30 checks passed`; after revert 30 of 30 | same | same | Yes |
| 8.6 one-liner | `501 3` | `501 3` | `501 3` | Yes |
| 8.7 `python mutation_check.py` | `33 of 33 mutations caught`, exit 0, 15 s | 16 s | 16 s | Yes (time: see L4) |
| 8.8 `python crosscheck.py` | as 7.4 | | | Yes |
| 9, exercise 1 check | `4.0` | `4.0` | `4.0` | Yes |
| 9, exercise 2 check | `0.8171` | `0.8171` | `0.8171` | Yes, matches the stated answer |
| 9, exercise 3 check | `[1, 2, 4, 8, 16, 32, 64, 100]` | same | same | Yes |
| 7.8 uninstall (on `.venv313`) | `pip cache purge`: `Files removed: 876 (447.7 MB)`, exit 0; a second purge: `WARNING: No matching packages`, `Files removed: 0`, exit 0; `deactivate`, `cd ..`, `rm -rf engineering-stack-lab-part-09` exit 0; folder gone, venvs and LangGraph gone with it | | | Works. (I backed up and restored the shared pip cache so the purge didn't affect other sessions.) |

### Section 7.7 error table, reproduced

| Row | How I caused it | What printed (last line) | Wording matches? |
|---|---|---|---|
| can't open file | `python run_lab.py` from the home folder | `python: can't open file '/home/claude/tester9/run_lab.py': [Errno 2] No such file or directory` | Yes |
| ModuleNotFoundError | `crosscheck.py` in a fresh venv with nothing installed | `ModuleNotFoundError: No module named 'langgraph'` | Yes |
| no thread | `f.run('x', FileCheckpointer('cpx'))` | `ValueError: no thread 'x'; pass state= to start one` | Yes |
| is paused | start `t1`, then `f.run('t1', c)` | `ValueError: thread 't1' is paused; pass resume=` | Yes |
| StepLimitError | a node that routes to itself, default limit | `workflow.StepLimitError: step limit of 25 reached without reaching END` | Yes, but with a `workflow.` prefix (L6) |
| StateTamperedError | start with `secret='a'`, resume with `secret='b'` | `workflow.StateTamperedError: checkpoint for 't2' was changed` | Yes, prefix as above |
| IndexError | `python crash_run.py` | `IndexError: list index out of range` | Yes |
| pip notice | seen on 3.11 and 3.12 installs | `[notice] A new release of pip is available: 24.0 -> 26.2.1` | Yes |

Errors a beginner can hit that the table lacks: `ValueError: thread 'A17' already exists` (M2) and `ValueError: thread_id must be 1 to 64 letters, digits, _ or -` (L7).

## Problems

### Medium

**M1. Section 9, exercise 1: the retry number is counted from 0, and nothing in the exercise says so.**
- What I did: read "the longest possible wait before retry n = 3" as "before the third retry", which gives 0.5 x 2^2 = 2 s.
- What I saw: the answer is 4 s, because the engine numbers retries 0, 1, 2, ... (stated only in `workflow.py`'s `RetryPolicy` docstring, "The wait before retry n (n = 0, 1, ...)"). For n = 5 both readings happen to give 8 s, so only the first half trips. A careful learner gets "the wrong answer" for following plain English.
- Fix: say "counting retries from 0 (the first retry is n = 0), so n = 3 is the fourth retry", or rephrase as "before the fourth retry".

**M2. Section 8, step 3, and Section 7.7: re-running step 3 gives an error the table doesn't cover, and no delete command is given.**
- What I did: ran the first `python -c` again (a natural thing to do when experimenting, or when the "Delete `my-checkpoints`" step was skipped because no command was given).
- What I saw: a traceback ending `ValueError: thread 'A17' already exists`. Not in 7.7. (Running the second command again quietly prints `done rf_1` again, since a finished thread is returned as is, which can also puzzle.)
- Fix: give the delete command (`rm -rf my-checkpoints` on macOS and Linux, `Remove-Item -Recurse -Force my-checkpoints` in PowerShell) and add a 7.7 row: `ValueError: thread 'A17' already exists` | the checkpoint folder already holds that thread | delete the folder (or use a new thread id).

**M3. Section 8, step 4: the replacement line is shown without its indentation.**
- What I did: followed "replace the line with `flow.add_edge("approve", "refund")`" literally, replacing the whole line (which is indented 4 spaces in `build_refund_workflow`) with the unindented text.
- What I saw: `run_lab.py` crashed before any check ran: `File ".../examples.py", line 96` / `flow.add_edge("refund", END)` / `IndentationError: unexpected indent`. The error points at line 96, the line after the edit, which is extra confusing. Keeping the 4 spaces gives exactly the promised `28 of 30 checks passed` with FAIL 2c and 2d.
- Fix: "replace that text (keep the four spaces in front of it) with ...", and suggest copying the original line first so it can be put back.

**M4. Section 7.8: the temporary-folder note undercounts and misses one prefix.**
- What I did: counted folders left in the temp folder by one run of each script (fresh `TMPDIR`).
- What I saw: one `run_lab.py` run leaves 21 folders; one `mutation_check.py` run leaves 711; `demo.py` leaves 1 (`demo09-...`); `crosscheck.py` leaves `lg09-...` folders, a prefix 7.8 doesn't mention. "Small folders" is true, but a learner who runs the lab a few times has thousands, and isn't told where the temporary folder is or how to delete them.
- Fix: "Each run leaves small folders in your temporary folder (hundreds after `mutation_check.py`), named `lab09-`, `demo09-` or `lg09-`. To remove them: `rm -rf /tmp/lab09-* /tmp/demo09-* /tmp/lg09-*` on Linux; on macOS the folder is `$TMPDIR`; in PowerShell `Remove-Item -Recurse -Force $env:TEMP\lab09-*, $env:TEMP\demo09-*, $env:TEMP\lg09-*`." Better still, have `run_lab.py` and `mutation_check.py` clean up after themselves.

**M5. Section 6: "Three paths, as in every part" is followed by four bullets, plus a fifth sentence.**
- What I saw: Learn the ideas; Build a small app; Avoid lock-in; When not to use an agent at all (which also contains "When not to use several agents"). As a beginner I looked for the third "path" and found two items that aren't paths.
- Fix: "Three paths" then the first three bullets, with "When not to use..." as a separate paragraph after the list; or "Three paths, and when to skip them".

### Low

**L1. Section 8, step 6: "a brief carries three words" is not quite what `3` counts.** The brief `'Check A17.'` is two words; the 3 includes the one-word instructions `'Billing.'`. Likewise 501 is ten 50-word messages plus that word. Fix: "prints `501 3`: the handoff carries all ten 50-word messages plus the one-word instruction; the agent-as-tool input is the two-word brief plus the same instruction."

**L2. Section 8, step 3: "Open that file: the whole state is there."** The file holds the checkpoint as a JSON string inside JSON, so a beginner sees a wall of `\"` escapes (`{"checkpoint": "{\"log\": [], \"node\": \"approve\", ...`). Fix: say so, and offer a readable view: `python -c "import json; print(json.dumps(json.loads(json.load(open('my-checkpoints/A17.json'))['checkpoint']), indent=2))"`.

**L3. Section 8, step 2: "`python demo.py`, part 1 and 2".** The script prints all four parts; there is no way to run only parts 1 and 2. Fix: "`python demo.py`; its first two parts print ...".

**L4. Section 7.6 and Section 8, step 7: "about a minute".** Measured 15 to 16 s on all three Pythons here. Fine as an upper bound; "under a minute" would match better.

**L5. Section 8, step 7: "On the first run, two breaks went unnoticed".** Reads as if the learner's own first run might miss two. Fix: "While the lab was being built, two breaks went unnoticed ...".

**L6. Section 7.7: the table shows `StepLimitError: ...` and `StateTamperedError`, but Python prints `workflow.StepLimitError: step limit of 25 reached without reaching END` and `workflow.StateTamperedError: checkpoint for 't2' was changed`.** A learner searching the page for the exact line won't find it. Fix: show the full last line.

**L7. Section 7.7: no row for `ValueError: thread_id must be 1 to 64 letters, digits, _ or -`.** Easy to hit in your own code (I used `'order A17'`, with a space). Fix: add a row.

**L8. Section 8, "What the checks cover": check 1b (routing) is missing.** The list names 29 of the 30 checks. Fix: add "routing (1b)".

**L9. Section 3.6, rule 2: lists "Approve" (a bare string) as refused.** Check 2d actually tests `"approve"` (lowercase bare string) and `{"decision": "Approve"}`. Both are refused, and "Approve" would be too, but the doc's list doesn't match what the check runs. Fix: quote the check's list, or say `{"decision": "Approve"}`.

**L10. Section 7.6, "In your own code": two facts a beginner needs are missing.** The first node added is where a run starts (there is no `START`), and `IdempotencyStore.run(key, params, fn)` calls `fn(**params)`, so `params` must be a dictionary of the function's keyword arguments (a list gives `TypeError: ... argument after ** must be a mapping, not list`). I built a two-step workflow from the paragraph alone and it worked once I guessed these.

**L11. Section 9, exercise 1's check is cryptic and checks only half the answer.** `type('H', (), {'uniform': lambda s, a, b: b})()` is unexplained to a learner who "knows a little Python", and the command checks n = 3 only. Fix: one sentence ("a stand-in random source that always returns the top of the range, so delay() prints the longest wait"), and a second command with `delay(5, ...)` that prints `8.0` (I ran it; it does).

**L12. Section 7.4: "blocks network connections".** `crosscheck.py` replaces `socket.socket.connect` and `socket.create_connection` only; DNS lookups (`getaddrinfo`), `connect_ex` and UDP `sendto` are not blocked. In practice nothing tried (audit hook above), so the claim holds for this run; the wording could be "blocks outgoing connections made through `connect`" or the script could also patch `connect_ex` and `getaddrinfo`.

**L13. Sections 1 to 3: terms used without plain-words definitions.** HMAC-SHA256 (3.3 and 3.6, rule 3: "signs checkpoints with HMAC-SHA256"; plain words: a keyed fingerprint only someone with the secret can make), "upserts" and "read-before-write checks" (3.3), "pending writes" (3.3). "Control layer" and topic codes T16 to T18 point to the series plan, which a learner may not have open. The opening tag line names Temporal, CrewAI and Microsoft Agent Framework before anything defines them (Section 2 says they come in Sections 3 and 6, which helps). Fix: add HMAC, upsert and pending writes to the Section 2 table.

**L14. Section 3.9: "68.7% of the time (the exact figure is 68.3%)".** A beginner will wonder why the lab disagrees with the exact figure. Fix: "(a simulation of 20,000 questions; the exact figure is 68.3%)". I checked 68.3%: 0.6^5 + 5(0.6^4)(0.4) + 10(0.6^3)(0.4^2) = 0.6826.

**L15. Opening line: tag counts depend on an unstated rule.** Counting exact `[T]` from Section 1 through the cheat sheet gives 57 [T], 173 [V], 9 [R], 10 [I], matching the header. Counting the three `[T on ...]` forms as [T] gives 60. Fix: none needed if the rule is "exact tags", but say so, or count the variants.

**L16. Sections 7 and 7.3: small missing feedback for beginners.** 7.3 says "if your Python 3 is 3.11 to 3.13" without the command to check (`python3 --version`); the Linux unzip command prints nothing on success, so suggest `ls ~/ai-stack` to confirm the folder arrived. And 7.8 could reassure that deleting the lab folder also removes the virtual environment, LangGraph and `my-checkpoints`, since they all live inside it.

## Things that worked well (for the editor)

- Every quoted output in Sections 5, 8 and 9 matched exactly on all three Pythons.
- The Linux unzip command works even when `ai-stack` doesn't exist yet.
- The break-and-revert in step 4 is a good lesson and fails exactly as described.
- The cross-check is genuinely offline after the install.

## Files

- Report: /home/claude/part09/phase4/tester-report.md
- Test copy (lab folder deleted by the 7.8 test, as the doc instructs): /home/claude/tester9/ai-stack

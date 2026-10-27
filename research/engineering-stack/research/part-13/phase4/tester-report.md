# Part 13 beginner test report (Sections 6 to 9 and the appendix)

Tester: careful new Linux user, following the text literally. Date: October 20, 2026.
Folder: /home/claude/part13/phase4/tester/ (run313, run312, run311, each with its own fresh unzip into `ai-stack` and its own `.venv`).
Pythons: 3.13.16 (python3.13), 3.12.3 (/usr/bin/python3.12), 3.11.17 (/usr/bin/python3.11).

## Summary

| Severity | Count |
|---|---|
| High (reader can't continue or gets a wrong result) | 0 |
| Medium (confusing or misleading) | 4 |
| Low (polish) | 12 |

Everything the text says should happen on Linux happened, on all three Pythons:

- `python run_lab.py`: `17 of 17 checks passed`, exit 0, about 4.6 s (text: "about five seconds").
- `python crosscheck.py` before the install: `Install the cross-check packages first (Part 13, Section 7.4): No module named 'fastapi'`, exit 2 (matches Section 7.7).
- Install: the same 16 pinned packages on each Python (FastAPI 0.156.1, uvicorn 0.54.0, OpenTelemetry SDK 1.45.1, Starlette 1.9.0 and the rest).
- Cross-check: seven PASS lines, `Network attempts outside this computer: 0 []`, `7 of 7 cross-checks passed`, exit 0.
- Two windows (server in the background): the server line is exactly as printed in 7.5; the client printed `time to first token 0.085 s, total 0.552 s, 24 tokens, usage {'input_tokens': 4, 'output_tokens': 24}` on 3.13 (0.085/0.553 on 3.12, 0.086/0.553 on 3.11). Ctrl+C (SIGINT) stopped the server cleanly with no traceback and freed the port. Port 8014 works as described. The port-in-use error (`OSError: [Errno 98] Address already in use`) and `ConnectionRefusedError` both appear as Section 7.7 says.
- Tour (7.6): `Fraction(9, 1000)`, `Fraction(9, 2000)` with `batch=True`, `40`.
- Section 8 step 2: three events as described. Step 3: `demo.py` prints the seven tables in the stated order; table 1 matches Section 3.9 exactly.
- Step 5, break it: line 58 is the right line; after the change: `FAIL c11_long_context_whole_request: AssertionError 1103/200` and `16 of 17 checks passed` (1103/200 = 5.515). After restoring the file: 17 of 17 again.
- Step 6, mutation check (once, on 3.13): `32 of 32 mutations caught`, 2 min 27 s (text: about 3 minutes). Every mutation named in step 6 is in the list.
- Section 9: exercise 1 prints `0.003375`, exercise 2 `240`, exercise 3 `[('a', 'x\ny'), ('message', 'z')]`. The self-check answers agree with the code (mean 1.48, p95 9; above 272,000 gpt-6-astra rates go 10 to 20, 1 to 2, 12.50 to 25, 50 to 75).
- Appendix: `shipmath.py` in the zip and the appendix listing are byte for byte identical (8,974 bytes, `cmp` reports no difference).
- Network: `strace -e connect` on `run_lab.py`, `demo.py` and `crosscheck.py` showed only 127.0.0.1 (plus the local name-service socket). Only the pip install reached PyPI.
- Leftovers: no `/tmp/lab13-*` folders after any step, including after interrupting `mutation_check.py` with Ctrl+C partway through (its try/finally removed the copy). No lab process was left listening. (One Python process listening on 127.0.0.1:8099 belongs to another reviewer's folder, /home/claude/part13/phase4/security/lab; I left it alone.)

Tester's own side effect, for honesty: the pip install wrote to pip's download cache in the real home folder (`/root/.cache/pip`). That is also the subject of finding 3.

## Findings

### 1. Medium. Section 7.5: activate before going to the folder

Text: "Open two terminal windows, activate the lab's environment in both, and go to the lab folder."

What happened: read literally, the new window starts in the home folder, and `source .venv/bin/activate` fails there (`No such file or directory`), because the path is relative to the lab folder. It works only in the other order: `cd` first, then activate.

Fix: "In both windows, go to the lab folder and activate its environment (the first and third commands of Section 7.1 or 7.2/7.3)." Or print the two lines for each system.

### 2. Medium. Section 7, "Before you start": no macOS unzip step

Text: "(on Windows: right-click, Extract All, ...) ...; on Linux, from the folder holding the zip, `python3 -m zipfile -e engineering-stack-lab-part-13.zip ~/ai-stack`"

What happened: macOS gets no instruction. Double-clicking in Finder unpacks into Downloads, not into `~/ai-stack`, so `cd ~/ai-stack/engineering-stack-lab-part-13` in 7.2 fails.

Fix: "on macOS and Linux, in Terminal, from the folder holding the zip: `python3 -m zipfile -e engineering-stack-lab-part-13.zip ~/ai-stack`." (The command works as given on Linux: I used it for all three unzips.)

### 3. Medium. Section 7.8: pip's cache stays behind

Text: "The cross-check's packages go with the virtual environment. The lab writes no files outside its folder"

What happened: pip keeps a download cache in the home folder. `python -m pip cache dir` printed `/root/.cache/pip`, and the second and third installs said `Using cached ...whl`. On macOS that is `~/Library/Caches/pip`; on Windows `%LOCALAPPDATA%\pip\Cache`. The lab itself does write only inside its folder (plus `__pycache__` there); the claim is about pip.

Fix: add "pip keeps a download cache outside the folder; `python -m pip cache purge`, run before `deactivate`, empties it." Or install with `python -m pip install --no-cache-dir -r requirements-crosscheck.txt` in 7.4.

### 4. Medium (judged by reading; Windows not run). Section 7.7: the Windows port-in-use error may not appear

Text: "`OSError: [Errno 98] Address already in use` (Windows: `[WinError 10048]`) from `stream_server.py`"

What happened: `stream_server.py` uses `http.server.ThreadingHTTPServer`, which sets `allow_reuse_address = 1` (seen in /usr/lib/python3.13/http/server.py line 136), so the socket gets `SO_REUSEADDR`. On Linux that still refuses a second listener (I got Errno 98). On Windows, `SO_REUSEADDR` lets a second socket bind a port already in use, so a second `stream_server.py` may start without any error, and requests may go to either server. The row is marked [R on Windows], so this needs a Windows run.

Fix: run it on Windows. If it starts silently, change the row to say so ("a second server may start without an error; stop the first one") or set `allow_reuse_address = False` in the lab's server on Windows.

### 5. Low. Section 7.5: the answer doesn't depend on the prompt

Text: "In the second: `python sse_client.py "Tell me about streaming"`. It prints the answer"

What happened: the stand-in gives the same sentence for any prompt ("Streaming sends the answer in pieces as the model writes it, ..."). With `"hi"` only `input_tokens` changed (1 instead of 4). A beginner who tries their own prompt may think something is broken.

Fix: "It prints the stand-in's fixed answer (the same for any prompt) and a line like ..."

### 6. Low. Section 7.6: "In your own code" only works from the lab folder

Text: "In your own code, after `import shipmath as sm`: ..."

What happened: the import works from the lab folder (checked). From a script in another folder Python can't find it and raises `ModuleNotFoundError: No module named 'shipmath'` (standard import behaviour; my rerun from outside the folder was blocked by a tool timeout, so this one line is by reading).

Fix: "In your own code, run from the lab folder or with `shipmath.py` copied next to it, ..."

### 7. Low. Section 7.4: package count and pip notices

Text: "16 packages in all [T]"

What happened: 16 is right for what gets installed. But on 3.11 `pip list` shows 17 lines besides pip, because that venv starts with `setuptools 79.0.1`; and every install ends with `[notice] A new release of pip is available` (26.2.1 to 26.2.2 on 3.13; 24.0 to 26.2.2 on 3.11). A beginner who counts may worry.

Fix: "16 packages are installed (`pip list` may also show pip and setuptools). A notice that a newer pip exists is harmless."

### 8. Low. Section 7.4: show the cross-check's output shape

Text: "Expect seven PASS lines, `Network attempts outside this computer: 0 []` and `7 of 7 cross-checks passed`"

What happened: correct, but the output also starts with a version line (`fastapi 0.156.1, uvicorn 0.54.0, Python 3.13.16`) and every PASS line has an indented detail line under it, one of which says "note the JSON quotes around a plain string".

Fix: an abridged output block like the one in Section 8.

### 9. Low. Section 8, step 2: the printed form differs from the description

Text: "prints three events: `first event` with ID `1`; `second event` with an empty ID, ...; and ` third event` with its second space kept"

What happened (all three Pythons):
```
Event(type='message', data='first event', last_event_id='1')
Event(type='message', data='second event', last_event_id='')
Event(type='message', data=' third event', last_event_id='')
```
The words agree, but a beginner looks for "ID" and sees `last_event_id`.

Fix: print this block in the text, or say "the ID is shown as `last_event_id`".

### 10. Low. Section 8: timings vary

Text: "PASS c06_proxy_buffering: header honoured: first token 0.08 of 0.54 s; ..." and "Outputs are from the test machine"

What happened: one 3.13 run printed `first token 0.07 of 0.54 s`; c05 printed `first at 0.09 s` once and `0.08 s` otherwise.

Fix: add "timings vary by a few hundredths" next to the block.

### 11. Low. Section 9: exercises don't say "environment active"

Text: "Run the checks from the lab folder."

What happened: they work in the venv. Outside it, on many Linux systems, `python` doesn't exist (only `python3`).

Fix: "Run the checks from the lab folder, with its environment active (Section 7)."

### 12. Low. Appendix and shipmath.py: wrong section number

Text (appendix and the zip, line 45): `BATCH = F(1, 2)            # all three vendors: half price (Section 3.7)`

What happened: Section 3.7 is "The GenAI conventions: names for model calls". Batch prices are in Section 3.9 ("What it costs", "Discounts and surcharges").

Fix: change to `(Section 3.9)` in both the zip and the appendix, so they stay byte-identical. Section 8 step 5's "line 58" is unaffected.

### 13. Low. Section 7.2/7.3: the fallback command isn't given

Text: "If `py -V:3.13` or `python3.13` isn't found, use the 3.11 or 3.12 from Part 01."

What happened: on Linux `/usr/bin/python3.12 -m venv .venv` and `/usr/bin/python3.11 -m venv .venv` worked, and everything after them gave the same results. A beginner has to guess the spelling.

Fix: "(for example `py -V:3.12 -m venv .venv` or `python3.12 -m venv .venv`)".

### 14. Low. demo.py table 1: rounding of the Haiku batch price

Text (Section 3.9 table, printed by `demo.py`): `claude-haiku-5-5  $0.00045  batch  $0.00022`

What happened: the exact value is $0.000225. The display rounds it down to $0.00022 (float formatting), while the other rows are exact. A reader who halves $0.00045 by hand gets $0.000225.

Fix: show one more digit for that column, or `$0.000225`.

### 15. Low (judged by reading). Section 7, Windows unzip destination

Text: "right-click, Extract All, destination `ai-stack`"

What happened: Extract All asks for a full path and suggests `...\Downloads\engineering-stack-lab-part-13`. Typing just `ai-stack` would extract relative to the dialog's default, not the home folder.

Fix: "destination `C:\Users\<your name>\ai-stack` (Browse to it)".

### 16. Low. Section 8, step 1: no line numbers

Text: "Open `ssewire.py`: `Parser._line` is the spec's list of field rules, and `_dispatch` is what happens at a blank line."

What happened: both exist (`_line` at line 108, `_dispatch` at line 131), but the file also has `_lines` at line 84, which a beginner searching for "_line" finds first.

Fix: "(line 108) ... (line 131)", as step 5 does for `shipmath.py`.

## Things checked that need no change

- Section 6 versions agree with `requirements-crosscheck.txt` and with what pip installed.
- Section 7.4's "[T on Python 3.13.16, 3.12.3, 3.11.17]" matches the three versions tested here.
- Section 7.7: the wrong-folder message reads `python: can't open file '/.../run_lab.py': [Errno 2] No such file or directory`, as in the table.
- Section 7.1 Windows commands (`py -V:3.13`, `.venv\Scripts\Activate.ps1`) and the PowerShell environment-variable syntax in Section 6 look right by reading. The `python -c "..."` commands in Sections 8 and 9 use double quotes outside and single quotes inside, which PowerShell passes through unchanged.
- Ctrl+C during `mutation_check.py` leaves no `/tmp/lab13-*` folder and no process (a KeyboardInterrupt traceback prints, which is normal).
- `run_lab.py`, `demo.py` and the cross-check pick their own ports (port 0), so they work while `stream_server.py` holds 8013.

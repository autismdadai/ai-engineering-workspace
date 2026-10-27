# Beginner-tester report: Part 07, Tools and Protocols

Date: October 14, 2026. Document: engineering-stack-part-07-tools-and-protocols.md. Lab: engineering-stack-lab-part-07.zip.
Tester role: careful beginner (a little Python, Part 01 done). Linux path (7.3), plus 7.4, 7.6, Section 8 (all steps, break-it steps undone as written) and Section 9 (three exercises). Windows (7.1), macOS (7.2) and host (7.5) read only.

Method: for each Python I made a separate fake home folder, created ai-stack, unzipped with `python3 -m zipfile -e engineering-stack-lab-part-07.zip ~/ai-stack` (run from the folder holding the zip), made a fresh `.venv` inside the lab folder, activated it, and typed the commands from the text. Nothing under /home/claude/part07 was changed. No accounts, no API keys. A system-wide `mcp` 2.2.0 exists outside venvs on python3 (3.13); I stayed inside the venv except for one deliberate test.

## Results by Python version

| Python | run_lab.py | mutation_check.py | crosscheck.py (after pip install -r requirements-crosscheck.txt) |
|---|---|---|---|
| 3.12.3 (/usr/bin/python3.12) | `22 of 22 checks passed` (exit 0) | `20 of 20 mutations caught` (16 s) | `INFO mcp 2.3.0 on Python 3.12.3` ... `8 of 8 cross-checks passed`, 1 INFO line about unknown tool |
| 3.11.17 (python3.11) | `22 of 22 checks passed` (exit 0) | `20 of 20 mutations caught` (15 s) | `INFO mcp 2.3.0 on Python 3.11.17` ... `8 of 8 cross-checks passed`, 1 INFO line |
| 3.13.16 (python3) | `22 of 22 checks passed` (exit 0) | `20 of 20 mutations caught` (17 s) | `INFO mcp 2.3.0 on Python 3.13.16` ... `8 of 8 cross-checks passed`, 1 INFO line |

The SDK install (7.4) was done on all three. pip rc 0 each time. The last INFO line on all three: `INFO an unknown tool on the SDK server comes back as: isError result (the spec's example uses a JSON-RPC error; the lab server follows the spec)`.

Also run on all three and matching the text: demo.py (Part 1, 2, 3 as described; ttlMs 0 and cacheScope public on tools/list; serverInfo in `_meta`), Section 8 steps 3 (break stdout: `5 of 22 checks passed`, FAIL 1 ... JSONDecodeError; restored byte-identical; back to 22 of 22), 4 (`{'id': 'n5'}`, hits n2 and n5), 5 (the 22 lines match the text except the two `[...]` shortenings), 6 (scanner prints `[]`), 7 (ok true; Note-Finder copy lists the expected problem; copy deleted), 8, the mutation_check output shape, Section 9 exercise 1 (isError True, "Invalid arguments: query is too short"), 7.8 uninstall (`Files removed: 168`), the appendix listing (identical to the zip's notes_server.py, 321 lines), the 7.6 "in your own code" API (all names and signatures exist and work), and the 7.7 rows I could trigger (run_lab from the wrong folder, `SKIP the mcp package is not installed`, `INFO mcp 2.2.0 on Python 3.13.16` outside the venv, the FastMCP ModuleNotFoundError text, `ConnectionError: server closed stdout`, -32602 message).

Not run: 7.1, 7.2, 7.5 (read only), Windows Ctrl+Z, the Windows and macOS file handling noted below (reasoned, not tested).

## Problems

Severity: high = stops a beginner; medium = confusing or output differs; low = polish. No high problems on Linux.

### 1. (medium) Step 2: removing `"_meta":{...}` literally gives a parse error, not -32602
Quote (Section 8, step 2): "Now paste the same request without `"_meta":{...}`: the reply is an `error` with code `-32602`".
Did: took the request line and deleted `"_meta":{...}` as written. The comma before it stays, so the line ends `"arguments":{"query":"ledger"},}}`.
Saw: `{"jsonrpc":"2.0","id":null,"error":{"code":-32700,"message":"Parse error"}}`. The correct request (comma also removed) gives `{"jsonrpc":"2.0","id":1,"error":{"code":-32602,"message":"params._meta must carry protocolVersion and clientCapabilities"}}`.
Fix: print the second request in full as its own code block (`...,"arguments":{"query":"ledger"}}}`), or say "remove the comma and the whole `"_meta"` part".

### 2. (medium) Exercise 2 has no command that reaches the answer
Quote (Section 9, exercise 2): "What code, and what does `data` hold? Answer: `RpcError: -32022: Unsupported protocol version`; catching the error and printing `error.data` gives ..."
Did: ran the given one-liner.
Saw: a full traceback ending `mcp_client.RpcError: -32022: Unsupported protocol version` (note the `mcp_client.` prefix; the text shows `RpcError:` only). There is no command for "catching the error and printing error.data", and a beginner would not know the exception class is importable from mcp_client or that it has `.data`. A one-line `python -c` cannot hold try/except.
Works (I tried): 
```
python -c "
from mcp_client import *; import sys
c = StdioClient([sys.executable, 'notes_server.py'], version='2025-11-25')
try:
    c.discover()
except RpcError as error:
    print(error.code, error.data)
c.close()
"
```
printing `-32022 {'supported': ['2026-07-28'], 'requested': '2025-11-25'}`.
Fix: give this block (and a PowerShell-safe alternative, or tell Windows readers to save it as a .py file), and say a traceback is expected from the one-liner.

### 3. (medium) Exercise 3 gives no SKILL.md and no command
Quote: "A folder `pdf-tools` has `name: pdf_tools`. ... Check by making the folder: `skill_check.py` reports ..."
Did: had to guess: copied skills/note-finder to skills/pdf-tools, changed the `name:` line, ran `python skill_check.py skills/pdf-tools`.
Saw: the two expected problems, rc 1. A beginner starting from an empty folder does not know the file needs `---` front matter with a `description`, and does not know where to make the folder or what command to run.
Fix: "copy skills/note-finder to skills/pdf-tools, change the name line to `name: pdf_tools`, run `python skill_check.py skills/pdf-tools`", then "delete skills/pdf-tools afterwards" (the text does not say to delete it, and a leftover folder is harmless but untidy).

### 4. (medium, reasoned not run) Step 7 on Windows and macOS: the copy has the same name as the original
Quote (step 7): "Copy the folder to `skills/Note-Finder`, change the `name:` line to match, and run it on the copy ... Delete the copy afterwards."
Windows and default macOS file systems ignore letter case, so `skills/Note-Finder` is the same folder as `skills/note-finder`. The copy command either fails or merges into the original; "change the name line" then edits the real skill, and "delete the copy" deletes the real skill, after which run_lab.py check 8 would fail. On Linux (tested) it works.
Fix: use a name that differs by more than case, for example copy to `skills/note_finder` and set `name: note_finder` (it fails the same rule). Also say how to copy on each system (`cp -r` is Linux/macOS only; PowerShell uses `Copy-Item -Recurse`).

### 5. (medium, reasoned not run) Windows: Extract All probably nests the folder
Quote (Section 7, Before you start): "On Windows, right-click the zip and choose Extract All" then 7.1 `cd $HOME\ai-stack\engineering-stack-lab-part-07`.
Windows proposes extracting into a folder named after the zip next to it. The zip already has the top folder `engineering-stack-lab-part-07/`, so the result is `...\engineering-stack-lab-part-07\engineering-stack-lab-part-07\`, and the 7.1 `cd` lands in the outer folder with no run_lab.py (the 7.7 first row error). The text does not say to put the zip into ai-stack first or to change the destination.
Fix: "Move the zip into ai-stack, right-click, Extract All, and in the destination box delete the suggested last folder name so the destination is ai-stack."

### 6. (low) 7.7: JSONDecodeError position differs
Quote: "`JSONDecodeError: Expecting value: line 1 column 1 (char 0)` from a client".
Saw with the lab's own stdout break (step 3): `Expecting value: line 1 column 2 (char 1)`, because the log line starts with `[`, which is valid JSON start. Fix: say "Expecting value: line 1 column ..." (any position), or show the lab's actual text.

### 7. (low) Step 2: the terminal shows more than "the reply is one line"
Tested in a real terminal (pty). After pasting I saw my pasted line echoed, then `[notes-server] tools/call search_notes {"query": "ledger"}` (stderr), then the JSON reply. Then Ctrl+D printed `[notes-server] stdin closed, exiting`. The text says "The reply is one line" and does not mention the log line or the echo. Fix: one sentence: "You will also see a log line starting [notes-server]; that is standard error."

### 8. (low) Step 3: the result of the break is not stated beyond "every check ... fails"
Saw 17 FAIL lines and `5 of 22 checks passed` (the five that do not use the server still pass: 7d, 8, 8b, 8c, 9). A beginner may think "every" means 22 and be unsure the break worked. Fix: say "17 FAIL lines and `5 of 22 checks passed`". Also no mention of which editor to use; fine for Part 01 readers but worth "open the file in any text editor".

### 9. (low) Undefined terms
HMAC (in the diagram, 3.6 and Section 5, never explained; "a signature that proves the message was not changed" would do), SDK (never expanded), CVE and CVSS (3.8, 3.11, 5), NVD, ZDR (3.8 table; "zero data retention"), DNS rebinding (3.5), SHA-256 (3.11), JWS and gRPC (3.9), SEP (3.5, 3.10), BCP 14 (How to read), SSE is defined only in 3.5 (and is used in Section 1-2 context via transports). "stdout" and "stderr" are assumed known in 3.5 and Step 2; one clause would help ("the two output channels `print` can use").

### 10. (low) 7.4: package count and pip notice vary by Python
Quote: "28 packages besides pip in a fresh environment". True on 3.12 and 3.13. On 3.11 a fresh venv also contains `setuptools`, so I counted 29 besides pip, and the `[notice] A new release of pip is available: 24.0 -> 26.2.1` lines appear on 3.11 only (3.12 and 3.13 venvs had pip 26.2.1). Fix: "about 28" and mention the notice (it is in 7.7 already).

### 11. (low) 7.8: `pip cache purge` is global
It deleted 168 files from the pip cache that all projects share (in the fake home). Not harmful but the text implies it only cleans this lab. Fix: "this empties pip's shared download cache; other projects will just download again".

### 12. (low) Step 5: `[...]` note points to the wrong place
Quote: "(`[...]` stands for the hit list and the five scanner reasons, shown in full by `demo.py`.)" run_lab.py itself prints both in full (checks 4 and 7c). A beginner comparing will see more text than the book and wonder. Fix: "run_lab.py prints these in full; the book shortens them".

### 13. (low) 7.6 `answer_input=fn` is underspecified
"where `fn` answers `input_required` rounds". It does not say fn receives the `inputRequests` map and must return the `inputResponses` map. (It is in the code's docstring; I got it working with `lambda reqs: {'confirm': {'action':'accept','content':{'confirm':True}}}` after reading the source.) Fix: add the one sentence and this example.

### 14. (low) Section 7 file list is ambiguous about notes_server.py
Section 8 "Files": "`notes_server.py`, the protocol itself, is listed in the appendix; `mcp_client.py`, ... are in the zip". This reads as if notes_server.py is not in the zip. It is (and the appendix is identical). Fix: "all files are in the zip; notes_server.py is also printed in the appendix".

### 15. (low) Step 7: "change the `name:` line to match" is ambiguous
Match what? (The new folder name.) Fix: "set it to `Note-Finder`, the new folder name".

### 16. (low, read only) 7.1 to 7.3 gaps
7.1: `py -V:3.13` fails if only Python 3.12 or 3.11 is installed (Section 6 says 3.11 to 3.13 are fine). 7.2: `python3.13` fails on a Mac with only 3.12 and has no "Expect 22 of 22" line (7.1 and 7.3 do). 7.3: says "the same commands as macOS" but the first command is a `cd` that assumes the unzip landed in ~/ai-stack; fine, but a one-line recap would help. 7.5: "using the Python from your virtual environment" does not show how to get its full path (`which python` on Linux and macOS, `where python` on Windows after activating).

### 17. (low) Reader-facing text that is really author notes
- "Checks run on this part: To be filled after Phase 4." is still in the document (just before the Cheat sheet).
- "Run on your computer" table: "Send back the output; each [R] above then becomes [T] with the date." is addressed to the author, not to the reader.
- Step 8 closing paragraph: "On the first run, five breaks were caught only because `run_lab.py` crashed; the checks were then rewritten ..." is build history that confuses a beginner.
- The opening italic paragraph is packed with [V], [T], [R], [U], [I] tags and counts before "How to read this part" explains them. A beginner stops reading there. Consider moving the tag counts below the "What this part gives you" paragraph.

### 18. (info) Behaviour worth one sentence in 7.7
Outside the venv, python3 (3.13) imports the system-wide `mcp` 2.2.0: `crosscheck.py` then prints `INFO mcp 2.2.0 on Python 3.13.16` and `INFO this cross-check was written for mcp 2.3.0; other versions may differ` and runs anyway. The 7.7 row covers this correctly. python3.11 and python3.12 outside the venv print `SKIP the mcp package is not installed`, also as the text says. Also, mutation_check.py with an un-restored step 3 break correctly stops with `FAIL the unbroken copy does not pass; fix the lab first` (nice, but the text could mention it in 7.7).

## Things that worked exactly as written
All 22 run_lab lines (except the two shortened `[...]`), the mutation_check head and tail lines, the crosscheck count and INFO line, the demo transcript properties, the step 4 and 6 one-liners, the exercise 1 output, the exercise 3 messages, the 7.7 rows listed above, and the uninstall steps. No Python-version differences in any output apart from item 10.

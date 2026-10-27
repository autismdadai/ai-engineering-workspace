# Engineering Stack: Windows Reader-Test Run, October 26, 2026 (Part 13)

*Part 13's reader tests R1, R2 and R4 on the owner's Windows 11 computer (P-04 on the owner's decisions page, which stays private). This time the owner typed every step, as a reader would, in the Claude desktop app's Terminal panel, and Claude read the output from that panel. Every result below is copied from it. R3 waits until November 3, 2026 or later, when its two newest pins have been on PyPI for 14 days (owner approved, Oct 26, Claude chat). Nothing was downloaded or installed, and no account, key or payment was used. Steps: `part-13-reader-test-steps.md`. Evidence class: project test record.*

## The computer and the lab

- Windows 11 Pro 10.0.26300; Windows PowerShell in the app's Terminal panel. Python 3.13.16 from python.org, through `py -V:3.13` [T]. No Python 3.11 or 3.12 is installed, so this is a one-Python test.
- Lab zip: `archive\zips\engineering-stack-lab-part-13.zip`, 31,744 bytes, SHA-256 `ad2261325494a2f817616c65d3960b875dd5423981057890d33c724e1cafb50c` [T]. Unzipped, its 12 files match `research/engineering-stack/labs/part-13/` byte for byte [T: SHA-256 of each file].

## Results

| Step | Part 13 says | What happened |
|---|---|---|
| Unzip (Section 7) | Extract All, then Browse to `C:\Users\<your name>\ai-stack` | Not done: the owner couldn't find `C:\Users` in the Browse dialog, and nothing was extracted. `Expand-Archive .\archive\zips\engineering-stack-lab-part-13.zip $HOME\ai-stack` worked and gave `%USERPROFILE%\ai-stack\engineering-stack-lab-part-13` with no extra folder level [T] |
| 7.1 `cd ...` and `py -V:3.13 -m venv .venv` | (no output) | Worked, no output [T] |
| 7.1 `.venv\Scripts\Activate.ps1` | May be refused; Part 01's fix | Refused: `cannot be loaded because running scripts is disabled on this system` (`PSSecurityException`) [T]. The owner chose not to change the execution policy, so every later step used `.venv\Scripts\python.exe` instead of `python`. The 7.7 fix stays [R] |
| R1 `run_lab.py` | `21 of 21 checks passed` | `20 of 21 checks passed`. `FAIL c20_server_limits: ConnectionAbortedError [WinError 10053] An established connection was aborted by the software in your host machine`. The same on a second run with `-v`, which showed it comes from `run_lab.py` line 412 (the client over the cap) inside `_raw`, line 311 (`s.recv`) [T]. The other 20 passed; c06 showed `header honoured: first token 0.10 of 0.58 s` [T]. No firewall prompt was mentioned (not asked directly), so 7.1's [U] stays |
| R2 `mutation_check.py` | `48 of 48 mutations caught` | `The unbroken copy fails: fix run_lab.py first`, then it stopped [T]. It can't run on Windows until c20 passes |
| R3 cross-check | `7 of 7 cross-checks passed` | Not run: waits until November 3 or later (14-day rule: fastapi 0.156.1 was uploaded October 20, starlette 1.9.0 on October 18) [V: PyPI] |
| R4 (7.5), server tab | `Stand-in model streaming on http://127.0.0.1:8013/v1/stream (Ctrl+C to stop)` | The same; Ctrl+C stopped it with no error output [T] |
| R4 (7.5), client tab | The answer, then a timing line | `Streaming sends the answer in pieces as the model writes it, so the first words reach the reader long before the last ones exist.` then `time to first token 0.112 s, total 0.590 s, 24 tokens, usage {'input_tokens': 4, 'output_tokens': 24}` [T] |

## The c20 failure, tested on a scratch copy

`research/engineering-stack/research/part-13/windows-2026-10-26/c20_probe.py` repeats c20's over-the-cap step 20 times: two silent clients fill `MAX_CLIENTS = 2`, then a third sends a request and reads the reply. It ran on a copy of the lab in Claude's scratch folder, with the lab's own Python 3.13.16 (owner approved, Oct 26, Claude chat). The copy was deleted afterwards. Output [T]:

```
Python 3.13.16 on win32
A as shipped: 503 received in 7 of 20; recv errors {None: 7, 'ConnectionAbortedError 10053': 13}
B gentle close: 503 received in 20 of 20; recv errors {None: 20}
```

- **What it shows [T]:** on Windows, a client over the cap got the server's 503 in only 7 of 20 tries. The other 13 ended with `WinError 10053` and no reply. Variant B changes only the server's busy path: send the 503, shut the write side, read what the client sent until it closes (0.5 s limit), then close. With that change, all 20 got the 503.
- **Why, as far as it's known:** `LabServer.process_request` (`stream_server.py`, lines 189 to 196) sends the 503 and closes without reading the client's request. Closing a socket with unread data makes TCP send a reset, which can wipe out the reply before the client reads it [U: standard TCP behaviour; no source opened this session; variant B is consistent with it]. The Linux runs passed 21 of 21 on three Pythons (Part 13, "Checks run on this part") [T, October 20]. The lab's `_raw` helper also catches only `TimeoutError` and `ConnectionResetError`, not `ConnectionAbortedError`.
- **So:** the lab's claim "a client over the cap gets 503" doesn't hold reliably on Windows. That's a bug in the stand-in server, not only in the test.

## The fix, October 26 (owner approved, Oct 26, Claude chat)

- **`stream_server.py`:** the busy path moved into `LabServer.refuse`. It sends the 503, shuts the write side, then reads what the client sent until the client closes, up to `REFUSE_SECONDS = 0.5` in total and at most `MAX_BODY` bytes, so one slow client can't hold the accept loop longer than that. Then it closes. It also adds `import socket`.
- **`run_lab.py`:** `_raw` now treats any `ConnectionError` as the end of the reply, not only `ConnectionResetError`. A lost 503 now shows as c20's assertion (`reply[:40]`) instead of a crash.
- **Tested on a scratch copy, then copied into `research/engineering-stack/labs/part-13/` [T]:** `run_lab.py` five times, 21 of 21 each time. `c20_probe.py` on the fixed copy: 503 received in 20 of 20 (its variant A is now the fixed server). `mutation_check.py`: `ok the unbroken copy passes`, then `48 of 48 mutations caught` in 375 s, with no SETUP lines, so every mutation's text still matches. Python 3.13.16, Windows, `-B` with `PYTHONDONTWRITEBYTECODE=1`. The scratch copy was deleted.
- **Zip:** rebuilt from the lab folder in the old layout (one top folder, deflated): `archive\zips\engineering-stack-lab-part-13.zip`, 31,990 bytes, SHA-256 `7cc3dcb84d408e3fb331ee3ccfbb6905c40bd0094c6c650cd7c7274248a3bf06`. All 12 files match the folder byte for byte [T]. The October 20 zip was kept as `engineering-stack-lab-part-13-2026-10-20.zip` (SHA-256 `ad2261…cafb50c`, as above). `archive/` stays local.
- **Not re-run:** the Linux runs, which can't be done on this computer, so the October 20 [T] on three Pythons is for the old code. The owner's unzipped copy in `%USERPROFILE%\ai-stack` still holds the old code. Unzipping the new zip and re-running R1 and R2 as typed fits the R3 sitting on or after November 3.

## Part 13 updated, October 26 (owner approved, Oct 26, Claude chat)

- **Edited, on a scratch copy, then diffed:** the unzip sentence now gives the PowerShell `Expand-Archive` line [T]; 7.1's tag says what was typed on Windows; 7.1 and 7.7 add `.venv\Scripts\python.exe` as the no-setting-change way round `Activate.ps1` [T]; 7.5 and Section 8, step 4, go from [R] to [T], with the Windows timings; "Run on your computer" gets a dated Windows paragraph; and "Checks run on this part" gets a Windows row.
- **Tag count in the header:** recounted the way the header counts (tags opening `[X]`, `[X:` or `[X on`, from Section 1 to the end of the checks). That method reproduces the October 20 header (183, 79, 10, 16, 20) at commit `b24f88c`. Before these edits the file already had 185 [V] and 83 [T], because the October 26 package re-check added tags without updating the header. Now: 185 [V], 92 [T], 7 [R], 16 [U], 20 [I] [T].
- **Size:** 841 lines before, 844 after; 146 table rows before, 147 after (one new row). `git diff`: 11 lines in, 8 out, each as intended.
- Not covered: Extract All itself, `Activate.ps1` and its fix, R3, Python 3.11 and 3.12, `demo.py`, and Section 8's hand steps 1 to 3 and 5.

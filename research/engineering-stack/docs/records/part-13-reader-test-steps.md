# Part 13 reader tests on Windows: steps for the sitting

*Prepared October 26, 2026 by Claude for P-04 (on the owner's decisions page, which stays private). Source: Part 13, Section 7 and "Run on your computer" (R1 to R4). Run the same day, all but R3. Results are in `engineering-stack-windows-run-2026-10-26.md`.*

## Why this sitting

Part 13's lab passed 21 of 21 checks on Linux with Python 3.13.16, 3.12.3 and 3.11.17 [T]. Its Windows steps are still marked [R], meaning never run on Windows: the Extract All unzip, `py -V:3.13`, `Activate.ps1` and the two-window stream. The October 20 Windows run called each lab's `python.exe` from scripts, so it never tested those typed steps. This time you type the steps, the way a reader would. Each step that works then turns its [R] into [T] with the date.

## Already checked (file lookups only, nothing run)

| Item | Found |
|---|---|
| Python 3.13 | `AppData\Local\Programs\Python\Python313\python.exe` is there; the October 20 record says 3.13.16. No 3.11 or 3.12 is installed, so this is a one-Python test |
| `py` launcher | `AppData\Local\Programs\Python\Launcher\py.exe` is there |
| Lab zip | `archive\zips\engineering-stack-lab-part-13.zip`. No SHA-256 has been recorded for it, so step 0 records one |
| `%USERPROFILE%\ai-stack` | Doesn't exist (the earlier labs are in `Downloads\ai-stack`). The part says to use the home folder, so this test does |
| Where to type | Two tabs in the desktop app's Terminal panel. Claude reads the output from there, so you don't copy and paste |

## Steps

Type each command on its own line. Admin rights aren't needed for any step. Only R3 needs the internet.

| # | You type or do | What it does | Needs | Time | Claude records |
|---|---|---|---|---|---|
| 0 | `Get-FileHash $HOME\Documents\ai-workspace\archive\zips\engineering-stack-lab-part-13.zip` | Fingerprints the zip | Nothing | Seconds | SHA-256 |
| 1 | In File Explorer: right-click the zip, Extract All, Browse to `%USERPROFILE%\ai-stack` | Unzips the lab as Section 7 says | Nothing | 1 minute | Whether the folder ended up nested (`...\engineering-stack-lab-part-13\engineering-stack-lab-part-13`) |
| 2 | `cd $HOME\ai-stack\engineering-stack-lab-part-13`, then `py -V:3.13 -m venv .venv`, then `.venv\Scripts\Activate.ps1` | Makes the lab's own Python environment and switches to it | Nothing installed | Under 1 minute | Any error; whether the prompt starts with `(.venv)`; `python --version` |
| R1 | `python run_lab.py` | Runs the 21 checks | Nothing. Windows Firewall may ask about Python: choose Cancel (the lab only uses 127.0.0.1) | About 10 seconds | The whole output, and whether the firewall prompt appeared (Part 13 marks that [U]) |
| R2 | `python mutation_check.py` | Breaks the lab 48 ways in temporary copies (`%TEMP%\lab13-*`, deleted afterwards) and expects each one to fail | Nothing | About 5 minutes | The last line and any FAIL lines |
| R3 | The install (see below), then `python crosscheck.py` | Checks the lab's rules against FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1 | Internet (PyPI); 16 packages; its own yes | A few minutes [U] | pip's install list and the whole cross-check output, including the network-attempt line |
| R4 | Tab 1: `python stream_server.py`. Tab 2 (after the `cd` and activation from step 2): `python sse_client.py "Tell me about streaming"`. Then Ctrl+C in tab 1 | Streams the stand-in model between two windows | Port 8013 free | 1 minute | Both tabs' output, especially the `time to first token ... total ...` line |
| After | Leave the lab folder until the record is written | Keeps the evidence | | | |

**If PowerShell refuses `Activate.ps1`:** it's your call, because the fix changes a security setting, so you type it, not Claude.
- (a) Part 01's one-time fix: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, then activate again. This also tests Part 13's 7.7 row.
- (b) Change no setting: type `.venv\Scripts\python.exe` wherever a step says `python`. The activation step then stays [R].

**R3, the install.** The part's command, `python -m pip install -r requirements-crosscheck.txt`, pins exact versions but not file hashes (Section 7.4 says so). The workspace rules ask for checksums where they're published, and PyPI publishes them.
- **With hashes (recommended; this is the October 20 method and the `LESSONS.md` rule):** before the sitting, Claude reads each of the 16 files' SHA-256 and upload date from PyPI and writes a hashed copy of the list. You then run `python -m pip download --require-hashes --only-binary :all: -r <hashed list> -d <new empty folder>`, then `python -m pip install --no-index --find-links <that folder> -r requirements-crosscheck.txt`. The last command still uses the part's own list.
- **As written:** the part's one command. It's faster, but nothing checks the files.
- **14-day rule:** the pins were the newest versions on October 20. Any of them uploaded after October 12 is less than 14 days old today, and Claude flags it before you install.
- **Decided October 26:** with hashes, using `part-13-crosscheck-hashes-2026-10-26.txt` (in this folder). Two pins are too new: fastapi 0.156.1 was uploaded October 20 and starlette 1.9.0 on October 18 [V: PyPI]. So R3 runs on or after November 3, and R1, R2 and R4 run on October 26.

## Tags in Part 13 that results would change

| Where | Tag now | Becomes, if the step works |
|---|---|---|
| Section 7, the Extract All sentence | [R] | [T: Windows, date] |
| 7.1, the typed steps | [R: typed steps not run on Windows ...] | [T: Windows, date] |
| 7.1, the firewall prompt | [U] | Whatever happened, [T] |
| 7.5 and Section 8, step 4 (R4) | [R] | [T: Windows, date], with your timings |
| 7.7, the `Activate.ps1` row | [R] | [T] only if fix (a) is used |
| 7.8, `Remove-Item` | [R] | [T] only if you uninstall at the end |
| "Run on your computer" | R1 to R4 | Each one run gets its date |

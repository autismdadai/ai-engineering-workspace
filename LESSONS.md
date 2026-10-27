# Lessons

Technical traps hit while building this workspace, and the rule each one led to. Any model working here follows them. Add a row when a failure happens, or happens again, and keep personal details out.

Sources: the corrections logs of the October 20, 22 and 26 handoffs and the model pages (all in the owner's private workspace), the October 26 council run, and the October 26 Windows run (`research/engineering-stack/docs/records/engineering-stack-windows-run-2026-10-26.md`).

## Windows, Python and the shell

| What went wrong | Rule | When |
|---|---|---|
| The Windows console (cp1252) can't print Greek letters such as φ or ψ; scripts crashed. Claude hit it, then Codex hit it again | In scripts, call `sys.stdout.reconfigure(encoding="utf-8")`, or run with `python -X utf8`. `python -I` ignores `PYTHONIOENCODING` | Oct 21, Oct 22 |
| Python failed on a long temporary path | Work inside the short workspace path | Oct 21 |
| `core.autocrlf true` rewrote line endings and broke the labs' shell scripts | Keep `core.autocrlf false`; `.gitattributes` keeps LF | Oct 21 |
| A bash heredoc holding a single quote broke the command parser | Write the script with the file-writing tool, then run it | Oct 21 to 22 |
| PowerShell 5.1 `Start-Process -Wait` waited for every child process and hung for hours at the Ollama installer | Use `-PassThru`, `$null = $p.Handle` and `$p.WaitForExit(ms)` on the one process | Oct 19 to 20 |
| A large download broke partway (curl error 56) and the checksum refused it | Resume with `curl -C -` (up to 6 tries), then re-check SHA-256 | Oct 19 to 20 |
| The newest pypdf on PyPI was only 5 days old; bad releases are usually caught within days | Install the newest release at least 14 days old, pinned with its PyPI SHA-256 (`pip download --require-hashes` into a new empty folder, then `pip install --no-index` from it) | Oct 26 |
| A version-sorting script crashed on a very old SymPy release labelled `0.5.13-hg` | Skip version labels that don't parse | Oct 26 |
| Two of Part 13's pinned lab versions (fastapi 0.156.1, starlette 1.9.0) were under 14 days old; the rule had only been applied to newest releases | Check each pinned file's upload date on PyPI too, before installing a pinned list | Oct 26 |
| A lab server sent its 503 and closed without reading the request. On Windows the reply was lost in 13 of 20 tries (`WinError 10053`); Linux passed | Before closing on a refused or early reply, shut the write side and read what the client sent, with a time limit. Client helpers catch `ConnectionError`, not only `ConnectionResetError`. Run network labs on Windows as well as Linux | Oct 26 |

## Checks and tests

| What went wrong | Rule | When |
|---|---|---|
| A check's expected value was written without running it, and was wrong | Run the code first and copy the real output | Oct 2026, Part 12 |
| Mutation "catches" were really crashes | Checks are registered functions; any exception prints a FAIL line | Part 07 |
| Stale bytecode let mutants pass | Mutation runs use `python -B` and `PYTHONDONTWRITEBYTECODE=1`, and clear `__pycache__` | Part 10 |
| Checks left temporary folders behind | Scripts delete their temporary folders | Part 09 |
| A lab step had readers edit shipped data, which broke a check | Copy to a scratch file, and say to delete the copy afterwards | Part 12 |
| Table edits risked lost or duplicated rows | Compare header and row counts before and after; search for duplicates | Glossary |
| Long files edited from memory risked losing text | Patch an exact copy with exact-string edits, then diff before saving | Oct 2026 |
| The first October 26 freshness record compared version numbers only, and missed anthropic's licence change and three Python ranges | Compare every column with `ledger_compare.py` before editing the ledger | Oct 26 |
| Part 13 and the ledger said FastAPI "needs Starlette 1.9.0"; FastAPI declares `starlette>=0.46.0` | Check a dependency claim against the project's own `pyproject.toml`, or PyPI's `requires_dist`. When that is empty (click 8.5.0), read `pyproject.toml` at the release tag | Oct 26 |
| A basic-grep alternation (a backslash, then a pipe) matched every line; a browser JavaScript filter matched the `15: ` line-number prefix and pushed the real hit out of view | Filter on the line text before adding line numbers; sanity-check a search's hit count | Oct 26 |
| Part 13's header tag count went stale: the package re-check added 2 [V] and 4 [T] without updating it | After an edit that adds or removes tags, recount with the header's own method, first confirming it reproduces an older header, and update the count | Oct 26 |

## Git, GitHub and other models

| What went wrong | Rule | When |
|---|---|---|
| A push was rejected because Codex had pushed from elsewhere | `git fetch`, read the remote commits, then rebase or fast-forward, then push. Never force-push | Oct 22 |
| GitHub had a Codex commit while the local copy had other uncommitted Codex notes in the same file | Back up the local file, fast-forward, re-add the local notes, and check both sides byte for byte | Oct 22 |
| A status line on one model's page went stale against another's | Current decisions live on one decisions page; the model pages keep dated logs | Oct 26 |

## Plugin and claude.ai

| What went wrong | Rule | When |
|---|---|---|
| claude.ai loaded the plugin but dropped all 13 skills, because their descriptions ran over 200 characters | Each skill carries `metadata.claude-app-description` (200 characters or fewer); `tools/package_for_claude_ai.py` swaps it in | Oct 21 |
| A test session saw the plugin registered but not yet installed | Test plugins in a new session, and allow for install lag | Oct 21 |
| The desktop app runs its own copy of the plugin (`AppData\Roaming\Claude\rpm\...`), not the workspace folder | Compare that copy with the workspace before relying on a plugin change; rebuild and re-upload the claude.ai zip after plugin edits | Oct 26 |

## Local model (qwen3:1.7b through `ask_local_model`)

| What went wrong | Rule | When |
|---|---|---|
| With the instruction placed before the file, the model copied the file instead of doing the job | Put the instruction after the file, and give no sample answers (the model copies them) | Oct 21 |
| Asked for exact dates and versions, it found 0 of 4 dates and added lines not in the file | Exact lists go to Grep or a script; the local model only tags and roughly summarises | Oct 21 |
| Summaries of files of 2,900 to 5,700 tokens: 0 of 5 fully accurate, 2 of 6 attempts copied the file, writing slowed to 2.6 to 4.4 tokens per second | Send it only short files (up to about 5,500 characters); read longer files yourself | Oct 26 |

## Usage and research

| What went wrong | Rule | When |
|---|---|---|
| 19 agents launched at once on Opus hit the 5-hour limit in about 10 minutes, and no reports were saved | Check usage first; use Sonnet or Haiku; launch in waves of three; save each report as it returns; check usage between waves | Oct 21 |
| A council-sized run (10 Sonnet agents) used 41 points of the 5-hour window but only 5 weekly points | For big runs, pace by the 5-hour window, not the weekly one | Oct 26 |
| Estimates missed both ways: a browser copy took 410,928 tokens, more than estimated; the council run took about half its estimate | Measure usage before and after, and record the real figure next to the estimate | Oct 22, Oct 26 |
| WebFetch couldn't read arXiv PDFs, and Read can't render PDFs here | Read papers from ar5iv HTML (`https://ar5iv.labs.arxiv.org/html/<id>`) | Oct 22 |
| DBLP returned empty answers and Semantic Scholar rate-limited | Check citations with the arXiv API and Crossref | Oct 22 |
| `fetch()` run inside a page failed ("Failed to fetch"): on raw.githubusercontent.com, and from pypi.org to files.pythonhosted.org. Navigating to files.pythonhosted.org was refused | Open each file with `navigate` plus a short script inside one `browser_batch`; read PyPI facts from `https://pypi.org/pypi/<name>/<version>/json` | Oct 26 |

## Reader tests at the keyboard

| What went wrong | Rule | When |
|---|---|---|
| A block of five steps left the owner unsure where to type | Give one step at a time, name the panel to type in, and read the output from the Terminal panel instead of asking for copies | Oct 26 |
| `Get-FileHash` in a narrow panel cut the hash short (`AD2261325494A2F817616C65D...`) | Print the whole value: `(Get-FileHash <file>).Hash.ToLower()` | Oct 26 |
| Extract All's Browse dialog didn't lead to `C:\Users\<name>`, and nothing was extracted | Give a one-line `Expand-Archive <zip> $HOME\<folder>`, then check where the files landed | Oct 26 |
| `Activate.ps1` was refused (scripts disabled on this system) | Offer `.venv\Scripts\python.exe` in place of `python`. Changing the execution policy is the owner's call, typed by the owner, never by a model | Oct 26 |

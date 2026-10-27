# Beginner test report: Part 11, Sections 6 to 9

Tester: a self-taught beginner following `tester-sections.md` literally, as a fresh Linux user (`HOME=/home/claude/part11/phase4/tester/home`). The lab zip was copied to `~/Downloads` and unzipped into `~/ai-stack` with the Linux command from "Before you start". Three complete runs, each with a fresh lab folder and a fresh virtual environment: `python3.13`, `/usr/bin/python3.12`, `/usr/bin/python3.11`. The first attempt was interrupted by a usage limit and a container restart and nothing from it was kept; everything here is from the restarted test, 19 October 2026.

**Bottom line.** On Linux the lab itself behaves exactly as the text says on all three Pythons: every command ran, every number the text prints matched, the mutation check caught 31 of 31, the break-it step gave `10 of 14` and the restore gave `14 of 14`. The problems are in the text around the lab: a command that fails as printed, a few claims about the lab that are not true, quoted output that is not exactly what appears, and many gaps in 7.5 for a Windows reader. The Windows, macOS, Ollama and llama.cpp steps could not be run here, so those rows are from reading only and are marked "not run".

Counts: 1 high, 10 medium, 14 low (25 problems). 17 of them were reproduced on this machine; 8 (rows 1, 6, 7, 8, 9, 10, 21, 23) are read-through findings that I could not run.

## (a) Problems found

| # | Severity | Section and step | Quote from the text | What happened | Suggested fix |
|---|---|---|---|---|---|
| 1 | high | 7.1 (Windows), line 3 | `.venv\Scripts\Activate.ps1` | Not run (no Windows here). On a fresh Windows PC, PowerShell's default script policy normally refuses `.ps1` files with a red "running scripts is disabled on this system" error, which stops every later step. Part 11 does not mention it; the text says only "typed steps not run on Windows". | Add one line: if PowerShell refuses, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or point to where Part 01 says this. Run the Windows steps on a clean machine before release. |
| 2 | medium | 7.4, "In your own code" | `rm.gguf_bytes(rm.llama_tensors(cfg), rm.k_quant_m("Q4_K", "Q6_K"), n_layers)` | Typed as printed on all three Pythons: `NameError: name 'cfg' is not defined`. The text never says what `cfg` and `n_layers` are. With `cfg = rm.LLAMA3_8B` and `n_layers = 32` it prints `4912898048`. | Show the two assignments, e.g. `cfg = rm.LLAMA3_8B; n_layers = cfg["n_layers"]`, and say the call prints 4912898048 bytes. |
| 3 | medium | 8, step 1 | "each function is a few lines, and its docstring names the source" | Counted with Python's `ast` module (same on all three Pythons): 24 functions, 6 have no docstring at all (`count`, `bits_per_weight`, `uniform`, `_check`, `best_gamma`, the inner `choose`), and only 6 docstrings name a source (`ffn_width`, `gpt_oss_bytes`, `use_more_bits`, `expected_tokens`, `speedup`, `stream_metrics`). Most sources are in `#` comments above the data tables. Five functions run 10 to 13 lines. | Say "most functions are short; the sources are named in comments above the tables and in some docstrings", or add the missing docstrings. |
| 4 | medium | 8, step 2 | the four-line block starting `1. Llama 3 8B file sizes ...` ending `Q4_K_M   4.8944 bits/weight ...` | Each of the four quoted lines matches a real line character for character on all three Pythons, but the real output has three more rows between them (`Q8_0`, `Q6_K`, `Q5_K_M`) and then seven more tables (8 in all). The block is not marked as abridged, so a beginner sees extra rows and a longer output than shown. | Add `...` between the F16 and Q4_K_M lines, or say "abridged: the F16 and Q4_K_M rows". |
| 5 | medium | 7.4, last tour row; 8 step 8 | `python reader_local.py --self-test` / "Runs the reader test against a stand-in for Ollama" | Runs, exit 0, prints `Model stand-in:1.7b, file 1.40 GB`, `Measured: 12.5 tokens/s ...`, `Ceiling:  29.7 tokens/s ...`, `Measured is 42% of the ceiling.` The text gives no expected output, and the output never says "passed" or that the numbers are canned. A beginner cannot tell success from failure except by the exit code, and may think a real model was timed. | Quote the four lines and say "these numbers are fixed by the stand-in; success is exit code 0 and `12.5`". Better, print `Self-test OK` at the end. |
| 6 | medium | 7.5 step 4 and 7.6 "Above the ceiling" | "using your own processor's memory bandwidth (Intel lists it on each processor's specification page)"; "A wrong bandwidth figure" | Not run. Three gaps for the reader: (a) no way to find the processor model; (b) only Intel is covered, nothing for AMD, Apple or Snapdragon readers (no "transfer rate x 8 bytes x channels" rule); (c) on a PC with a supported GPU or on a Mac, Ollama normally runs on the GPU or unified memory, so the speed can legitimately beat a CPU-memory ceiling and the script then blames the bandwidth or the model name. I could not check this without Ollama; it follows from how the script computes the ceiling. | Say how to find the CPU model; give the DDR formula and an Apple/AMD example; add "if you have a GPU, use its memory bandwidth, or run Ollama CPU-only"; add this cause to the 7.6 row. |
| 7 | medium | 7.5, llama.cpp route | "download Qwen's own GGUF of Qwen3 4B at Q4_K_M (2.5 GB) from Hugging Face, then `llama-bench -m` with that file" | Not run. No link, no repository or file name, no way to download (browser? command?), and no full command: `llama-bench -m <path>` needs the real path. After `winget install` a Windows reader also needs a new PowerShell window before `llama-bench` is found. The sum `41.6 / 2.5` uses the example chip's bandwidth although step 4 said to use your own. | Give the exact download page and file name, the full `llama-bench -m C:\path\file.gguf` line, a "open a new PowerShell window" note, and "replace 41.6 with your own figure". |
| 8 | medium | 7.5 steps 1 to 4 (Windows) | "quit Ollama from the taskbar, open *Edit environment variables for your account*, add `OLLAMA_NO_CLOUD` ..."; "In the lab folder: `python reader_local.py ...`" | Not run. Gaps: the Ollama icon is in the hidden-icons tray, not the taskbar; how to open the environment-variables window (search the Start menu) and that you click New, then OK, is not said; where Ollama's settings are is not said; PowerShell windows opened before the install do not find `ollama`, so step 3 needs a new window; step 4 says "in the lab folder" but a new window has no `.venv` active, so `python` may be missing or be a different Python. | Add "open a new PowerShell window", repeat the `cd ...` and `.venv\Scripts\Activate.ps1` lines in step 4, and describe the tray icon and environment-variable dialog in one sentence each. |
| 9 | medium | 7.5 Expected; 8 "If it fails" | "Send back what it prints."; "A check that fails only on your machine is worth reporting: send the whole output." | Neither says where or how to send it (an email? a form?), and these sentences read like instructions to test readers. The tags `[T]`, `[R]`, `[V: ...]`, `[I]` and the name "Reader test R3" are used throughout these sections and none is explained here. | Name the destination, or delete the sentences; add a one-line key to the tags or a pointer to where they are defined. |
| 10 | medium | 6 (Picks) and 7.5, last lines | "With Ollama, set `OLLAMA_NO_CLOUD=1` unless you want its cloud models"; "On macOS, Ollama installs as an app [R]; on Linux, read its install script first (Section 3.8) [R]." | Not run. Section 6 tells every reader to set the variable, but 7.5 shows how only for Windows. A macOS or Linux reader has no steps for installing, pulling the model, or setting the variable, although 7.4 and the command in step 4 are the same on all systems. | Add three lines each for macOS and Linux: install, `OLLAMA_NO_CLOUD=1 ollama serve` (or the system's equivalent), `ollama pull qwen3:1.7b`. |
| 11 | medium | 7.5 Expected | "which for a 1.4 GB file at 41.6 GB/s is 29.7 tokens per second" | Checked with my own stand-in server, not real Ollama: the script prints `Ceiling:  29.7 tokens/s` only when the file is exactly 1,400,000,000 bytes. With an illustrative size of 1,359,293,444 bytes it printed `file 1.36 GB` and `Ceiling:  30.6`. I do not know the real byte size of `qwen3:1.7b`, but the beginner's first printed line will probably not say 1.40 GB and the ceiling will probably not be 29.7. | Say "about 30 tokens per second; the exact figure follows the exact file size the script prints". |
| 12 | low | 8, step 5 | "the file sizes, the fit check and the speed ceiling all move" | `10 of 14 checks passed` matches on all three Pythons, but four checks fail, not three: c03 (bits per weight), c05 (file sizes), c08 (fit) and c09 (ceiling). c03 is not mentioned. | List the four, or say "four checks fail, including c03". |
| 13 | low | 8, "If it fails" | "A FAIL line names the check and the failing value" | True for c03, c05 and c09. With the step 5 break c08 prints `FAIL c08_what_fits: AssertionError ` with nothing after it (the asserts in c08, `run_lab.py` lines 103 to 108, have no message). | Give the c08 assert a message (`assert ..., value`), or soften the sentence. |
| 14 | low | 7.6, row 2 | `qwen3:1.7b isn't pulled yet. Run: ollama pull qwen3:1.7b` | Using my stand-in server with an empty model list, all three Pythons: stderr shows `qwen3:1.7b isn't pulled yet. Run:  ollama pull qwen3:1.7b`, with TWO spaces after `Run:` (exit 1). The text has one. Cosmetic, but it fails a character-for-character match or a copy-and-search. | Make the message and the table agree (one space in `reader_local.py` line 39). |
| 15 | low | 7.6, rows 1 and 3 | `Can't reach Ollama at http://127.0.0.1:11434: is it running?`; fix: "Start it from the Start menu" | Real line on Linux: `... is it running? ([Errno 111] Connection refused)` (Windows will show a `WinError 10061` sentence). Row 1's real text is `python: can't open file '/full/path/run_lab.py': [Errno 2] No such file or directory`. Both quotes are fair excerpts but not marked as such. "Start menu" only exists on Windows. | Add "... and then a reason in brackets"; name the macOS and Linux way to start Ollama. |
| 16 | low | 8, step 3 | "Llama 3 8B's cache for one 32,768-token conversation is as large as its 4-bit weights" | `4.0` matches on all three Pythons. But the demo prints 4.58 GiB for the Q4_K_M weights, so the cache is 87% of them, not "as large as". | "nearly as large as (4.0 against 4.58 GiB)". |
| 17 | low | 8, step 7 | "one check (c08) failed on its own first run because its expected value had been typed in rather than computed, and was corrected to the computed 80,482 tokens" | The value is right (`rm.max_tokens(...)` computes 80482 on all three Pythons), but this is the author's development history in a beginner's step, and `run_lab.py` line 107 still has `80_482` typed in as a literal. | Delete the sentence (keep it in a changelog). |
| 18 | low | 8, "Expected output" | `PASS c14_reader_test_logic` then `...` then `14 of 14 checks passed` | The five quoted PASS lines match, in order, on all three Pythons, and the last line matches. But `...` stands after c14, which is the last check, so nothing lies between it and the summary; the nine elided lines are between the quoted ones. | Move `...` between the PASS lines, and say "abridged: 9 more PASS lines". |
| 19 | low | 9, exercise 2 | `rm.decode_ceiling(307e9, 4.912898048e9)` | Prints `62.48857537863566` on all three Pythons. The number 4.912898048e9 is not derived anywhere (the demo shows only `4.91 GB`). It equals the `gguf_bytes` result from problem 2's call. | Say where it comes from, or write the call with `rm.gguf_bytes(...)` inside. |
| 20 | low | "Before you start" (Linux) | "`python3 -m zipfile -e engineering-stack-lab-part-11.zip ~/ai-stack`" | Works (exit 0) but prints nothing, so a beginner has no sign it worked. It also needs `~/ai-stack` from Part 01; I created it myself. | Add "then `ls ~/ai-stack/engineering-stack-lab-part-11` should list six files". |
| 21 | low | 7.1 to 7.3 heading and intro; "Before you start" (Windows, macOS) | "7.1 to 7.3 Windows, macOS and Linux ... The same steps as Part 10, Sections 7.1 to 7.3"; "right-click, Extract All, destination `ai-stack`" | Read-through. One heading covers three systems with no 7.1, 7.2, 7.3 labels, and points to Part 10 although the steps are printed. For Windows the Extract All dialog needs a full path typed or browsed, and the "inner folder" remark is hard to follow. | Label each block (7.1 Windows, 7.2 macOS, 7.3 Linux) and drop the Part 10 reference. |
| 22 | low | 8, step 5 | "In `runmath.py`, change `"Q6_K": (256, 210)` to `"Q6_K": (256, 208)`" | The text occurs exactly once (line 83, in a line with four entries) and the edit works. But no editor is named and no line number or search hint is given. | Add "line 83" and "open the file in Notepad, TextEdit or nano". |
| 23 | low | 9, exercise 3 and the tutor prompt intro | "α beats c, the best γ is 1"; "modelled on claude/github-tutor-prompt.md" | Read-through. α, γ and c are not defined in Sections 6 to 9 (the code uses `alpha`, `gamma`, `c`); the tutor prompt cites a file path the reader does not have. | Define the symbols once in exercise 3; cut the file path. |
| 24 | low | 7.4 table, row `python demo.py` | "Prints Sections 3 and 5's tables" | Sections 3 and 5 were not given to me so I could not compare. The demo prints 8 tables numbered 1 to 8, which do not match section numbers. | Say "prints eight worked tables (file sizes, KV cache, ceilings, ...)". |
| 25 | low | 7.7 | "`deactivate`, move up one folder with `cd ..`, and delete `engineering-stack-lab-part-11`" | Worked on all three Pythons. After `deactivate` the shell's `python` resolved to `/usr/bin/python` here, which many Linux systems lack. A beginner who runs the lab commands after deactivating may see `python: command not found`. | Add "(use `python3` again after `deactivate`)". |

## (b) Every quoted output compared

OK = matched exactly. "Part" = the quoted text matched but the real output has extra text. "No" = does not match. Every row was run on all three Pythons unless its note says otherwise. Python columns are 3.13 / 3.12 / 3.11.

| # | Quoted in the text | Where | 3.13 | 3.12 | 3.11 | Note |
|---|---|---|---|---|---|---|
| 1 | `14 of 14 checks passed` | 7.1 to 7.3, 8 | OK | OK | OK | exit code 0 |
| 2 | "14 checks; exit code 0 only if all pass" | 7.4 | OK | OK | OK | exit 0 when passing, 1 when the Q6_K line is broken |
| 3 | `python mutation_check.py` "31 ways" ... "about 15 seconds" | 7.4, 8 step 7 | OK | OK | OK | 14.3 s, 15.5 s, 12.1 s |
| 4 | `31 of 31 mutations caught` | 8 step 7 | OK | OK | OK | 31 "caught" lines each |
| 5 | The seven example mutations in step 7 | 8 step 7 | OK | OK | OK | all appear; "keys without values" is printed as "keys stored without values" |
| 6 | Expected output block (c01, c05, c06, c11, c14 PASS lines, last line) | 8 | OK | OK | OK | order correct; `...` misplaced (problem 18) |
| 7 | demo block, four lines | 8 step 2 | OK | OK | OK | each line exact; not consecutive (problem 4) |
| 8 | `python demo.py` "Prints Sections 3 and 5's tables" | 7.4 | not checkable | not checkable | not checkable | runs, 8 tables, output byte-identical on all three |
| 9 | `python reader_local.py --self-test` | 7.4 | runs, exit 0 | runs, exit 0 | runs, exit 0 | no expected output given (problem 5) |
| 10 | `rm.gguf_bytes(rm.llama_tensors(cfg), ..., n_layers)` | 7.4 | No | No | No | NameError (problem 2) |
| 11 | `python run_lab.py` `10 of 14 checks passed` after the Q6_K edit | 8 step 5 | OK | OK | OK | four FAIL lines, not three (problem 12) |
| 12 | "Put it back and confirm 14 of 14" | 8 step 5 | OK | OK | OK | file identical to the original (`cmp`) |
| 13 | `4.0` | 8 step 3 | OK | OK | OK | |
| 14 | `29.714285714285715` | 8 step 4 | OK | OK | OK | |
| 15 | `8 3.0920795428571433` | 8 step 6 | OK | OK | OK | |
| 16 | `rm.speedup(0.2, 4, 0.25)` "under 1" | 8 step 6 | OK | OK | OK | prints `0.6248` |
| 17 | "corrected to the computed 80,482 tokens" | 8 step 7 | OK | OK | OK | `rm.max_tokens(...)` gives 80482 |
| 18 | `0.7529296875` | 9 exercise 1 | OK | OK | OK | |
| 19 | `62.48857537863566` | 9 exercise 2 | OK | OK | OK | |
| 20 | `1 1.0714285714285714` | 9 exercise 3 | OK | OK | OK | |
| 21 | `can't open file '.../run_lab.py'` | 7.6 row 1 | Part | Part | Part | real line starts `python: ` and ends `: [Errno 2] No such file or directory` |
| 22 | `Can't reach Ollama at http://127.0.0.1:11434: is it running?` | 7.6 row 3 | Part | Part | Part | real line adds ` ([Errno 111] Connection refused)` |
| 23 | `qwen3:1.7b isn't pulled yet. Run: ollama pull qwen3:1.7b` | 7.6 row 2 | No | No | No | two spaces after `Run:` (stand-in server) |
| 24 | `Above the ceiling: check --bandwidth and the model name.` | 7.6 row 4 | OK | OK | OK | stand-in server, 40 tokens/s; exit 1 |
| 25 | "29.7 tokens per second" for 1.4 GB at 41.6 GB/s | 7.5 | OK | OK | OK | only for exactly 1.4e9 bytes (problem 11); stand-in server |
| 26 | "exits with an error if the measurement beats the ceiling" | 7.5 | OK | OK | OK | exit 1 |
| 27 | `rm -rf engineering-stack-lab-part-11` removes the lab; "The mutation check deletes its own temporary folders" | 7.7 | OK | OK | OK | no `lab11*` left in /tmp; Ctrl+C test done on 3.11 only (also clean) |
| 28 | Section 9 numbers: 4.89 bits, 30.6% of 16-bit; gpt-oss-20b reads 3.71 GB per token; Llama 3 8B 131,072 bytes per token; best gamma 1 and 1.07 times | 9 | OK | OK | OK | arithmetic recomputed on 3.13 only; `c07` (131,072) passes on all three |
| 29 | Section 6: "Python 3.11 to 3.13, standard library" | 6 | OK | OK | OK | lab ran on all three; the import scan and `pip list` (only pip and setuptools) were done in the 3.11 venv |
| 30 | Not checked | 6 versions and licences; 7.5 real Ollama, llama.cpp, Hugging Face, `winget`; Windows and macOS steps; Sections 3 and 5 | | | | no access or not supplied |

## (c) Timings, versions, environment

| Item | 3.13 | 3.12 | 3.11 |
|---|---|---|---|
| Python | 3.13.16 | 3.12.3 | 3.11.17 |
| pip in the new virtual environment | 26.2.1 | 24.0 | 24.0 |
| Create venv (`-m venv .venv`) | 3.7 s | 6.8 s | 5.9 s |
| `python mutation_check.py`, real time | 14.3 s | 15.5 s | 12.1 s |
| `python mutation_check.py`, CPU (user) | 4.5 s | 5.1 s | 3.4 s |

`run_lab.py`, `demo.py` and the one-line commands were not timed separately. Machine: 2 CPU cores, Linux 6.18, idle. The text says Section 8's outputs came from Python 3.13.16, the same version as the 3.13 run here. The system temp folder is `/tmp` (`tempfile.gettempdir()`); it had no `lab11*` entries before the test, none after each mutation check, and none after cleanup. Cleanup done: everything under `tester/` deleted (the folder itself is left empty); no stand-in server still running; `/tmp` listed, no `lab11*` folders.

---

## Appendix: step log (written as I went, kept as recorded)


### Before the runs: reading the lab files (static findings)

I read all six lab files before running them. Findings that I confirm or drop below once I have run things:

- S1. Section 8 step 1 says each function's "docstring names the source". In `runmath.py` most docstrings do not name a source (sources are in comments above the data tables), and several functions have no docstring.
- S2. `reader_local.py` prints `isn't pulled yet. Run:  ollama pull ...` with two spaces after "Run:"; Section 7.6 quotes one space.
- S3. `reader_local.py` appends the system's reason to the "Can't reach Ollama" line; Section 7.6 quotes the line without it.
- S4. Section 8 step 2 shows two of the five table rows of `demo.py` without saying rows are left out.

### Run 1, python3.13 (3.13.16, pip 26.2.1), steps done so far

- "Before you start" Linux unzip (`python3 -m zipfile -e ... ~/ai-stack`): worked, exit 0, but prints nothing at all (no confirmation; a beginner has to `ls` to know it worked). Created `~/ai-stack/engineering-stack-lab-part-11/` with the six files (README.md, demo.py, mutation_check.py, reader_local.py, run_lab.py, runmath.py). I had to create `~/ai-stack` myself first (the text relies on Part 01 for that).
- 7.1 to 7.3 Linux: `python3.13 -m venv .venv` took 3.7 s, no output; `source .venv/bin/activate`; `python run_lab.py` -> 14 PASS lines and `14 of 14 checks passed`, exit code 0. MATCH.
- 7.4 `python mutation_check.py`: 31 "caught" lines, `31 of 31 mutations caught`, 14.3 s real (text: "about 15 seconds"). MATCH. No `lab11*` folders left in /tmp afterwards.
- 7.4 `python demo.py`: exit 0, 8 numbered tables printed. Section 8 step 2's four quoted lines each match a real line character for character, but they are NOT consecutive: the real output has three more rows (Q8_0, Q6_K, Q5_K_M) between the F16 and Q4_K_M rows and the text does not say it left them out.
- 7.4 `python reader_local.py --self-test`: exit 0; printed `Model stand-in:1.7b, file 1.40 GB` / `Measured: 12.5 tokens/s (median of the timed runs)` / `Ceiling:  29.7 tokens/s (bandwidth / file size)` / `Measured is 42% of the ceiling.` Nothing says the test passed or that the numbers are canned; the text gives no expected output for it.
- 7.4 "In your own code" line: `rm.gguf_bytes(rm.llama_tensors(cfg), rm.k_quant_m("Q4_K", "Q6_K"), n_layers)` typed as printed fails with `NameError: name 'cfg' is not defined`. The text never says what `cfg` and `n_layers` are. It works if you guess `cfg = rm.LLAMA3_8B` and `n_layers = 32` (prints 4912898048). `rm.kv_bytes(32, 8, 128, 1)` prints 131072 as expected.
- 8 step 1 ("each function is a few lines, and its docstring names the source"): counted with Python's `ast` module: 24 functions, 6 have no docstring at all (`count`, `bits_per_weight`, `uniform`, `_check`, `best_gamma`, inner `choose`), and only 6 docstrings name a source (`ffn_width`, `gpt_oss_bytes`, `use_more_bits`, `expected_tokens`, `speedup`, `stream_metrics`), counting generously. The sources for the data tables are in `#` comments above them. Longest functions are 10 to 13 lines (`gpt_oss_params`, `gpt_oss_bytes`, `k_quant_m`, `llama_tensors`, `stream_metrics`), more than "a few".
- 8 step 3 `rm.kv_bytes(32, 8, 128, 32768) / rm.GIB` prints `4.0`: MATCH. But the claim "as large as its 4-bit weights" compares 4.0 GiB with the 4.58 GiB the demo prints for Q4_K_M: the cache is 87% of the weights, not equal.
- 8 step 4 prints `29.714285714285715`: MATCH.
- 8 step 6 prints `8 3.0920795428571433`: MATCH. `rm.speedup(0.2, 4, 0.25)` prints `0.6248` (under 1, as the text says).
- 9 exercise 1 prints `0.7529296875`: MATCH. Exercise 2 prints `62.48857537863566`: MATCH. Exercise 3 prints `1 1.0714285714285714`: MATCH. (Exercise 2's number `4.912898048e9` is not derived anywhere in the text; the demo shows only `4.91 GB`. It equals the `gguf_bytes` result above.)
- 9 other numbers: 4.8944/16.0005 = 30.59% (text 30.6%) OK; gpt-oss-20b one token reads 3.708 GB (demo prints 3.71) OK; Llama 3 8B KV per token 131072 bytes OK; for alpha 0.5 and c 0.4, gamma 1 gives 1.0714 and gamma 2 gives 0.9722, so best gamma is 1, OK.
- 8 step 5 (break it): the text to change, `"Q6_K": (256, 210)`, occurs exactly once (line 83). After the change `python run_lab.py` ended `10 of 14 checks passed`: MATCH. Four checks fail, not three: c03 (bits per weight), c05 (file sizes), c08 (what fits) and c09 (decode ceiling). The text names "the file sizes, the fit check and the speed ceiling" and does not mention c03. The FAIL lines: `FAIL c03_bits_per_weight_from_block_layouts: AssertionError ('Q6_K', 6.5)`, `FAIL c05_...: AssertionError ('Q6_K', 6.500845441983807)`, `FAIL c08_what_fits: AssertionError ` (no value at all), `FAIL c09_decode_ceiling: AssertionError 8.488185699146522`. So "A FAIL line names the check and the failing value" is true for three of four; c08 shows none. After restoring the line (file byte-identical to the original, checked with `cmp`), `14 of 14 checks passed`, exit 0. (I waited 2 s between edits; the edit keeps the file size the same, so an edit-run-edit-run inside one second could reuse a stale compiled file, but a human cannot type that fast.)
- 7.6 error 1, run from `~/ai-stack` instead of the lab folder: real text is `python: can't open file '/home/.../ai-stack/run_lab.py': [Errno 2] No such file or directory`, exit 2. The text's `can't open file '.../run_lab.py'` is a fair excerpt. MATCH (partial quote).
- 7.6 error 3, Ollama not running (nothing on port 11434): `Can't reach Ollama at http://127.0.0.1:11434: is it running? ([Errno 111] Connection refused)`, exit 2. The quoted text is the first part only; the real line has an extra `([Errno 111] Connection refused)` (on Windows it will be a `[WinError 10061]` sentence). The fix column says "Start it from the Start menu", which only exists on Windows.
- 7.6 errors 2 and 4 and 7.5 expected output, using my own stand-in server on 127.0.0.1:11434 (tools/fake_ollama.py, not the real Ollama):
  - empty model list: stderr `qwen3:1.7b isn't pulled yet. Run:  ollama pull qwen3:1.7b`, exit 1. Real text has TWO spaces after `Run:`; the text quotes one. NOT an exact match (cosmetic).
  - model of exactly 1,400,000,000 bytes, 12.5 tokens/s: `Model qwen3:1.7b, file 1.40 GB` / `Measured: 12.5 tokens/s ...` / `Ceiling:  29.7 tokens/s (bandwidth / file size)` / `Measured is 42% of the ceiling.`, exit 0. The 29.7 in 7.5 matches only for a file of exactly 1.4e9 bytes: with an illustrative size of 1,359,293,444 bytes the script printed `file 1.36 GB` and `Ceiling:  30.6`. (I do not know the real byte size of qwen3:1.7b; the point is the printed ceiling follows the exact size, so a beginner's figure will probably not be 29.7.)
  - 40 tokens/s against a 29.7 ceiling: `Measured is 135% of the ceiling.` then `Above the ceiling: check --bandwidth and the model name.`, exit 1. MATCH.
- 7.7 uninstall on run 1: `deactivate`, `cd ..`, `rm -rf engineering-stack-lab-part-11` worked; `~/ai-stack` was empty afterwards. After `deactivate`, `python` resolved to `/usr/bin/python` on this machine (on a typical Ubuntu there is no plain `python`, which only matters if the beginner types it after deactivating). No `lab11*` in /tmp. Run 1 complete.

### Run 2, /usr/bin/python3.12 (3.12.3, pip 24.0), stage A

- venv created (6.8 s), `python run_lab.py`: 14 PASS, `14 of 14 checks passed`, exit 0. MATCH.
- `python mutation_check.py`: `31 of 31 mutations caught`, 15.5 s real. MATCH ("about 15 seconds"). No lab11 folders left in /tmp.
- `python demo.py`: output byte-identical to run 1. `python reader_local.py --self-test`: identical to run 1, exit 0.
- Section 8 quoted blocks (compare.py): same results as run 1 (four demo lines each match a real line, not consecutive; expected-output PASS lines in order and last line `14 of 14 checks passed`).

### Run 2, stage B

- Section 8 steps 3, 4, 6 and Section 9 exercises 1 to 3: all output byte-identical to run 1 (`4.0`, `29.714285714285715`, `8 3.0920795428571433`, `0.6248`, `0.7529296875`, `62.48857537863566`, `1 1.0714285714285714`). MATCH.
- Step 5: after the edit `10 of 14 checks passed` (same four FAIL lines as run 1; c08 again shows no value); restored byte for byte; `14 of 14 checks passed` again. MATCH.
- 7.6 wrong-folder and Ollama-not-running messages: identical to run 1. 7.7 uninstall worked. Run 2 complete.

### Run 3, /usr/bin/python3.11 (3.11.17), stage A

- venv created (5.9 s, pip 24.0); `python run_lab.py`: `14 of 14 checks passed`, exit 0. MATCH.
- `python mutation_check.py`: `31 of 31 mutations caught`, 12.1 s real. MATCH. No lab11 folders left in /tmp.
- demo.py and `--self-test` output byte-identical to run 1. compare.py: 10 quoted lines match, same as runs 1 and 2.

### Run 3, stage B and extras

- Steps 3, 4, 6, exercises 1 to 3: byte-identical to run 1. Step 5: `10 of 14 checks passed` with the same four FAIL lines, restored byte for byte, then `14 of 14 checks passed`. MATCH.
- Extra: Section 6 says the lab is "Python 3.11 to 3.13, standard library". Static import scan of all six files: argparse, http, json, os, shutil, statistics, subprocess, sys, tempfile, threading, urllib; nothing outside the standard library. `pip list` in the fresh venv shows only pip 24.0 and setuptools 79.0.1. OK.
- Extra: sent Ctrl+C (SIGINT to the process group) to `mutation_check.py` 4 s in: it stopped with a KeyboardInterrupt traceback and left no `lab11*` folder in /tmp (the folder existed while it ran). So "The mutation check deletes its own temporary folders" also holds after an interrupt.

- 7.6 wrong-folder and Ollama-not-running messages, and the 7.7 uninstall: identical to runs 1 and 2. Run 3 complete.

### Extra pass on all three Pythons (fresh extraction, Pythons called directly, same files)

Run to fill the per-Python table for checks I had run only once. Results identical on 3.13, 3.12 and 3.11: the 7.4 own-code line gives `NameError: name 'cfg' is not defined`; `rm.max_tokens(16 * rm.GIB, ...)` gives 80482; 24 functions of which 6 have no docstring; with my stand-in server: empty model list prints `qwen3:1.7b isn't pulled yet. Run:  ollama pull qwen3:1.7b` (two spaces, exit 1); a 1.4e9-byte model at 12.5 tokens/s prints ceiling 29.7 and exit 0; at 40 tokens/s prints `Measured is 135% of the ceiling.` and `Above the ceiling: check --bandwidth and the model name.` and exit 1.

### Not tested here

Windows, macOS, `py -V:3.13`, PowerShell activation, Extract All, `Remove-Item`; installing Ollama or llama.cpp, `ollama pull`, `winget`, Hugging Face downloads; Section 6's versions, licences and platform claims; Sections 3 and 5 (not supplied). My stand-in server (`fake_ollama.py`) only imitates the two Ollama calls the script makes, so it shows the script's messages but not real Ollama behaviour.

---

## Short list of problems, worst first

1. **7.1 (Windows)**, `.venv\Scripts\Activate.ps1`: not run, but on a default Windows PowerShell this usually fails with "running scripts is disabled on this system" and the text does not mention it. Blocks every later step for those readers.
2. **7.4**, "`rm.gguf_bytes(rm.llama_tensors(cfg), rm.k_quant_m("Q4_K", "Q6_K"), n_layers)`": typed as printed it gives `NameError: name 'cfg' is not defined` on all three Pythons. `cfg` and `n_layers` are never defined (`rm.LLAMA3_8B` and `32` work and print 4912898048).
3. **8 step 1**, "its docstring names the source": 6 of 24 functions have no docstring and only 6 docstrings name a source; the sources are mostly in comments above the data tables.
4. **8 step 2**, the four-line `demo.py` block: the lines are exact, but three more rows (Q8_0, Q6_K, Q5_K_M) sit between the F16 and Q4_K_M lines and the block is not marked as abridged.
5. **7.4**, "`python reader_local.py --self-test` ... Runs the reader test against a stand-in for Ollama": it prints four lines of fixed numbers (`Measured: 12.5 tokens/s`, `Ceiling:  29.7 tokens/s`, ...) with no "passed" and no expected output in the text.
6. **7.5 step 4 and 7.6**, "using your own processor's memory bandwidth (Intel lists it ...)": not run; no way to find the processor, nothing for AMD or Apple readers, and a GPU or Mac can legitimately exceed a CPU ceiling, so the script's "check --bandwidth and the model name" would mislead.
7. **7.5 llama.cpp route**, "download Qwen's own GGUF of Qwen3 4B at Q4_K_M (2.5 GB) from Hugging Face, then `llama-bench -m` with that file": not run; no link, no file name, no full command.
8. **7.5 steps 1 to 4**: not run; the tray icon, the environment-variable dialog, a new PowerShell window after the install (so `ollama` and the `.venv` are found) are all missing.
9. **7.5 and 8**, "Send back what it prints." and "send the whole output": no destination given; the tags `[T]`, `[R]`, `[V: ...]`, `[I]` are never explained in these sections.
10. **6 and 7.5**, "With Ollama, set `OLLAMA_NO_CLOUD=1`": 7.5 gives the steps for Windows only; macOS and Linux readers get one line each.
11. **7.5 Expected**, "for a 1.4 GB file at 41.6 GB/s is 29.7 tokens per second": the script prints 29.7 only for exactly 1,400,000,000 bytes (stand-in server); a different exact size prints a different ceiling (30.6 for my illustrative 1,359,293,444).
12. **8 step 5 and "If it fails"**, "the file sizes, the fit check and the speed ceiling all move" and "A FAIL line names the check and the failing value": four checks fail (c03 as well) and c08 prints `FAIL c08_what_fits: AssertionError ` with no value.
13. **7.6**, "`qwen3:1.7b isn't pulled yet. Run: ollama pull qwen3:1.7b`": the script prints two spaces after `Run:`.
14. Lower polish items are rows 15 to 25 in table (a).

Everything else in Sections 7 to 9 that can run on Linux matched the text exactly, on all three Pythons.

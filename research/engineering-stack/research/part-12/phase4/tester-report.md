# Part 12, Sections 6 to 9: beginner tester report

Tester: smart, self-taught, new to machine learning, Linux. Inputs: `tester-sections.md` (Sections 6 to 9) and `engineering-stack-lab-part-12.zip`. Date of test: October 19, 2026.

Path substitution: I set `HOME=/home/claude/part12/phase4/tester/home` for every command, so `~/ai-stack` expanded to `/home/claude/part12/phase4/tester/home/ai-stack`. No other substitution was needed. Commands were typed as written in the text.

Not done, as instructed: no `pip install` of torch, transformers or peft; no full `reader_lora.py` run. Not run, only reasoned: Windows and macOS. Each problem below is tagged `[run]` (I ran it and saw it), `[reasoning]` (I could not run it; argued from the files or from PyPI metadata), or `[PyPI]` (read from PyPI's JSON for the pinned versions, no install).

Everything the text predicts for the core lab matched, character by character, on Python 3.13.16, 3.12.3 and 3.11.17. The problems are around the edges: one trap in Section 8 step 4, platform claims for the optional R3 install, undefined labels, and missing "how" details.

## Counts by severity

- High: 2
- Medium: 7
- Low: 21

## High and medium problems

### High

**1. High. Section 8, step 4 then steps 5 and 6: the "bot" edit has no safe recipe, and the natural way of doing it breaks the next two steps.** `[run]`
Text: "Then make your own copy of one training line with the role `"bot"` and run it again: the checker names the line [T]."
What happened: the text does not say where the copy goes, how to make it (no editor named, unlike step 5), or what to expect. I tried three ways.
- Copy `train.jsonl` to a new file, append line 1 with `user` changed to `bot`, run `datacheck.py` on it: prints `train line 13: message 1: role must be one of ['assistant', 'system', 'tool', 'user']`, then also `train: example 13 repeats example 1` (the duplicate check ignores roles), and ends `4 problem(s) found`, not 2. Nothing in the text prepares the reader for 4.
- Replace `assistant` with `bot` on the last message: 5 problems (adds "last message isn't the assistant's, so there is no answer to learn").
- Append the line to `data/train.jsonl` itself (the most literal reading of "copy of one training line", and the easiest for a beginner): then `run_lab.py` shows `FAIL c14_sample_data` and `16 of 17`. If the reader goes on to step 5 without noticing, the break gives `15 of 17` (c07 and c14), not the `16 of 17` the text promises. Step 6 then stops at once with `FAIL the unbroken copy doesn't pass; fix the lab first` and no mutation list. `reader_lora.py` would also train on the bad line.
Suggested fix: give exact commands per system, using a separate file and never touching `data/train.jsonl`. For example: copy `data/train.jsonl` to `data/mytrain.jsonl`, append a changed line 1, run `python datacheck.py data/mytrain.jsonl data/test.jsonl`. Print the expected lines (`train line 13: message 1: role must be one of ...` and `4 problem(s) found`), explain the extra "repeats example 1" line, and end with "delete `data/mytrain.jsonl`; do not edit `train.jsonl`, because `run_lab.py` and `reader_lora.py` use it."

**2. High (optional R3 path only). Section 6 "Runs on: Windows, macOS, Linux" for PyTorch and Section 7.5 "It runs on any computer" are too broad; the pinned `torch==2.14.1` has no wheel for several common machines.** `[PyPI]`
What I found in the PyPI file list for torch 2.14.1: macOS wheels exist only as `macosx_14_0_arm64` (Apple silicon, macOS 14 or later); Windows only `win_amd64`; Linux only `manylinux_2_28` for x86_64 and aarch64. There is no source package. So on an Intel Mac, a Mac on macOS 13 or older, Windows on ARM, or an old Linux (glibc older than 2.28), `pip install torch==2.14.1 ...` stops with "No matching distribution found" and the text gives no fix or fallback.
Suggested fix: in the Section 6 PyTorch row and in 7.5, state the real limits (Apple silicon with macOS 14 or later, 64-bit Intel or AMD Windows, 64-bit Linux), say what to do otherwise (skip R3; `--plan` still works), and drop "It runs on any computer". Core lab is unaffected.

### Medium

**3. Medium. Section 7.5 download size is given for Windows only; on Linux it is many times larger.** `[PyPI]`
Text: "about 170 MB in about 40 packages on Windows, most of it PyTorch's 124 MB wheel". The Windows wheel is 124.1 MB, which matches. But the Linux x86_64 wheel is 554.6 MB, and `torch 2.14.1` requires on Linux `cuda-toolkit[...]==13.0.3`, `nvidia-cudnn-cu13` (553 MB), `nvidia-nccl-cu13` (216 MB), `nvidia-cusparselt-cu13` (170 MB), `nvidia-nvshmem-cu13` (60 MB) and `triton` (248 MB), plus the cuBLAS, cuFFT, cuSOLVER and other toolkit wheels. The five I could size alone add 1.25 GB beyond the wheel itself, so a plain Linux install is at least about 2 GB and probably more, even on a machine with no NVIDIA GPU. A Linux reader on a small disk or slow link is surprised and may get stuck mid-install. The text tells the "ordinary PC with no GPU" reader (Section 6 picks) to train on the processor.
Suggested fix: give Linux and macOS figures next to the Windows one; tell the reader to check free disk space first; and, if verified, show PyTorch's CPU-only install route for no-GPU machines. I could not reach PyTorch's CPU index from here (proxy returned 403), so I cannot confirm that `2.14.1` exists there.

**4. Medium. Undefined labels and "reader tests" throughout Sections 6 to 9.** `[run: read as a beginner]`
Places: first line of Section 6 "[V: PYPI]"; the table and picks use `[V: PFT, TRL, UNS, AXO, LLF, MLX, TFM, PYPI]`, `[T]`, `[R]`, `[U]`, `[I]`; 7.1 explains one `[R: ...]` in passing but nothing else; Section 6 says "as in reader test R3" before R3 exists (first defined in 7.5); 8 and 7.5 say "keep the whole output for reader test R1 (Section 12)" and "Note what it prints for reader test R3 (Section 12): ... the number no source read here gives [U]". A beginner cannot tell what these brackets mean, whether they must do anything, or who to send "the whole output" to. The R3 sentence reads like a note from the author to reviewers, not a lesson.
Suggested fix: one-line key at the top of Section 6 (what [V], [T], [R], [U], [I] mean and that the codes are in Section 12's source list), define "reader test" once, and say what the reader should do with the output (or drop the sentence from the beginner path).

**5. Medium. Sections 8 and 9 use plain `python` but never say the virtual environment (or the lab folder) must be active in the terminal you are using.** `[run]` for the module error, `[reasoning]` for `python` missing.
Text: Section 8 steps 2 to 4 and all Section 9 exercises use `python ...`; Section 9 says only "Run the checks from the lab folder."
What happened: from another folder, `python -c "import adaptmath as am"` gives `ModuleNotFoundError: No module named 'adaptmath'`; this error is not in the 7.6 table (the table only covers the `run_lab.py` form, `[Errno 2]`, which I reproduced and which matches). On a stock Ubuntu or macOS machine, in a new terminal where the venv is not active, plain `python` is not defined at all ("command not found"; I could not reproduce because this sandbox has `/usr/bin/python`). The core lab needs no venv, so a beginner who skips activation after a restart gets stuck on a non-error.
Suggested fix: at the top of Sections 8 and 9: "Open a terminal, `cd ~/ai-stack/engineering-stack-lab-part-12`, run `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`)." Add a 7.6 row for `ModuleNotFoundError: No module named 'adaptmath'` (same cause as `[Errno 2]`) and one for `python: command not found`.

**6. Medium. Section 7.4: "To add a model, copy its numbers from its `config.json` into a dict like `QWEN3_06B`" cannot be followed as written.** `[run: read adaptmath.py]; HF key names are from general knowledge [reasoning]`
The dict keys (`hidden`, `layers`, `heads`, `kv_heads`, `head_dim`, `ffn`, `vocab`, `tied`, `qkv_bias`, `qk_norm`) are not the names in a Hugging Face `config.json` (which uses names like `hidden_size`, `num_hidden_layers`, `num_attention_heads`, `num_key_value_heads`, `intermediate_size`, `vocab_size`, `tie_word_embeddings`). `head_dim` is absent from many configs, and `qkv_bias` and `qk_norm` are not config fields at all (the comment in `adaptmath.py` says they depend on the model family). The counting function also assumes one block layout (three-matrix MLP, two norms); a different architecture gets a wrong number with no warning.
Suggested fix: add a small mapping table (config name to dict key, and how to get `head_dim`, `qkv_bias`, `qk_norm`), one worked example, and a sentence saying which architectures the arithmetic covers, and that the answer should be checked against the model card's parameter count.

**7. Medium. Section 7.6 lacks the errors a Linux or macOS beginner is most likely to hit.** `[reasoning]` except where noted
Missing rows: (a) on Debian or Ubuntu, `python3.13 -m venv .venv` can fail with "ensurepip is not available ... install python3-venv" until a `python3.x-venv` package is installed; (b) `python3.13: command not found` (Ubuntu 24.04 ships 3.12): the sentence "use the 3.11 or 3.12 from Part 01" does not say to type `python3.12 -m venv .venv`; (c) `python: command not found` and `ModuleNotFoundError` (see problem 5, the latter `[run]`); (d) for R3, `pip` failing with "No matching distribution" (problem 2) and `from_pretrained` failing when Hugging Face cannot be reached (it is blocked in this test environment, so a reader behind a proxy or school network will see this); (e) running out of disk (problem 3).
Suggested fix: add these rows, and make the 7.3 command easier to adapt, for example "`python3.13` (or `python3.12` / `python3.11`, whichever you have)".

**8. Medium. Section 7.5 and 7.4: the expected `--plan` output is never shown, and the two parameter totals differ without explanation.** `[run]`
Text promises `460,800 trainable of 134,975,808 parameters` for the full run. `python reader_lora.py --plan` (and the "Missing package" case) prints `HuggingFaceTB/SmolLM2-135M-Instruct: 134,515,008 weights; LoRA r=8 on q and v trains 460,800` and `Model states for LoRA in 32-bit: 0.55 GB, plus activations`. 134,515,008 and 134,975,808 look like a mismatch to a beginner; the second is the first plus 460,800 (PEFT counts the adapter in "all params"). Also the "Missing package" message appears after those two lines, and the exit code is 2; the text mentions neither. The `--plan` row in 7.4 is tagged [T] but shows no output to compare.
Suggested fix: print the exact two `--plan` lines in 7.4, and add "134,975,808 = 134,515,008 + 460,800, because PEFT counts the adapter too."

**9. Medium. Section 9, misconception 2: "retrieval beat fine-tuning by 19 to 31 points on new facts [V: OVA, GEK]".** `[run: read as a beginner]`
"Points" of what is not said (accuracy? on which model and test?), the unit should be "percentage points" if that is what they are, and one range is cited to two different papers (Ovadia et al. and Gekhman et al.), so a reader cannot tell which paper gives which end. A number without its scope is likely to be repeated wrongly. (I did not check the papers.)
Suggested fix: name the measure, the models and the benchmark, and say "percentage points", or cite one paper per number.

## Low problems

**10. Low. Section 7.4: `python mutation_check.py` "(about 20 seconds)".** `[run]` Measured: 2.28 s on 3.13.16, 1.90 s on 3.12.3, 1.79 s on 3.11.17 (first run included). Output `33 of 33 mutations caught` matched. The line carries no tag. Fix: say "a few seconds" or give the machine.

**11. Low. Section 8 step 5: the FAIL line gives no reason.** `[run]` Output is `FAIL c07_full_finetuning_memory: AssertionError ` (empty message). The text explains the cause (ZeRO's 24 GB for 1.5 billion weights), but the reader only learns it by opening `run_lab.py` line 76. Fix: tell the reader where to look ("open `run_lab.py`, find `c07_full_finetuning_memory`") or make the assertions print the number.

**12. Low. Section 7.5: adapter size "about 1.8 MB".** `[reasoning]` (full run not allowed). The weights alone are 460,800 x 4 bytes = 1.84 MB, but `reader_lora.py` prints the sum of every file in `lora-out`. Simulating the safetensors header for the 120 tensors (about 15.6 KB) plus the config and model-card files, the script should print `1.9 MB`. Fix: write "about 1.9 MB" or "1.8 to 1.9 MB" and mention that the number is rounded from a folder total.

**13. Low. Section 6, PyTorch licence cell.** `[PyPI]` PyPI's expression for torch 2.14.1 is `Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT`; the cell lists five and leaves out the LLVM-exception one. The note above the table also says licences come "from each project's licence file", but this cell is from PyPI. Fix: include the sixth term or say "five of the six, see PyPI", and word the note to match.

**14. Low. Section 7 "Before you start": unzip details.** `[run]` for the first point, `[reasoning]` for the others. (a) `python3 -m zipfile -e engineering-stack-lab-part-12.zip ~/ai-stack` only works in the folder holding the zip; from anywhere else it ends in `FileNotFoundError: ... 'engineering-stack-lab-part-12.zip'` (a beginner's zip is usually in Downloads). Say "first `cd ~/Downloads`" or give the full path. (b) macOS is not named in the unzip sentence (Windows and Linux are), though the same command should work there and Finder's double-click unzips next to the zip, not into `ai-stack`. (c) Windows "Extract All, destination `ai-stack`": the dialog wants a full path (`C:\Users\<you>\ai-stack`), so typing `ai-stack` is ambiguous; say "Browse and choose your `ai-stack` folder". The command did create a missing target folder, and re-extracting over an existing copy worked.

**15. Low. `reader_lora.py --help` description is cut off.** `[run]` It prints "Reader test R3 (Engineering Stack, Part 12): train a small LoRA adapter on / your" because only the first docstring line is used. Fix: shorten the first docstring line or build the description from the first paragraph.

**16. Low. Section 7.4 code snippets use names the reader has not defined.** `[run: read as a beginner]` `am.training_bytes(n, "qlora", adapter)` and `am.shortlist(memory_gb, {...})` cannot be pasted: `n`, `adapter` and `memory_gb` do not exist, and nothing says to run from the lab folder. Only the `lora_params` example (returns `10092544`, which matched) is runnable. Fix: show one full `python -c` line for each, like Section 9 does.

**17. Low. "Exit code" is used about eight times and never explained or shown.** `[run]` Sections 7.4, 7.6, 8 and the README say a command "exits with code 1 on purpose" or "exit code 0 only if all pass". Observed: `run_lab.py` 0 on success and 1 on failure, `datacheck.py` 1, `--plan` 0, missing-package run 2 (all as the text implies, except 2 is undocumented). A beginner sees no difference on screen. Fix: one line: "see it with `echo $?` (macOS, Linux) or `echo $LASTEXITCODE` (PowerShell)".

**18. Low. Section 6 picks: how to set the environment variables.** `[reasoning]` "set `HF_HUB_DISABLE_TELEMETRY=1` before TRL runs" and "with `UNSLOTH_DISABLE_STATISTICS` set" give no command per system (`export ...` vs `$env:...`) and no value for the Unsloth one. A reader who cannot do it skips a privacy step. Fix: add the two commands, and the value.

**19. Low. Section 6 picks lack numbers, and the lab points back to Section 6 for advice it does not contain.** `[run]` "Best default for a solo builder with a GPU" gives no memory threshold; the reader is not pointed to the lab's own calculator (demo table 3, Exercise 3). In `adaptmath.py`, the rule for `have_hardware=False` says "rent a GPU ... (Section 6)", but Section 6 never mentions renting. Fix: add "use `training_bytes` and `fits` to check" to the picks, and either add a sentence on renting or change the cross-reference.

**20. Low. `demo.py` table 3 is hard to read for a beginner.** `[run]` The header says "7.79 GB (the test PC's RAM)", which means nothing on the reader's machine; the method names `lora_fp32` and `lora_bf16` are not explained anywhere in Sections 7 or 8; the reserve rule ("with a fifth kept free") is stated in the header but not in the text of Section 8. Fix: say "7.79 GB is the tester's RAM; try your own number", and gloss the method names.

**21. Low. Cross-references that do not agree or cannot be followed from Sections 6 to 9.** `[run: read as a beginner]` 7.4 says `demo.py` prints the tables "behind Sections 3 and 5", Section 8 step 3 says "Sections 3.4 to 3.7 quote them"; step 4 says the report is in "Section 3.8"; "Section 12" is needed for R1 and R3. I could not check these (only 6 to 9 were given). Fix: make the first two agree and check the numbers.

**22. Low. Section 7.5 and 7.7: the model download and its cache.** `[reasoning]` 7.5 gives the PyTorch size but not the model's download size (SmolLM2-135M is on the order of a few hundred MB; I could not check because Hugging Face is blocked). 7.7 says the model "stays in Hugging Face's cache, `.cache\huggingface` in your home folder", written with a Windows backslash in a section that also covers macOS and Linux (`~/.cache/huggingface`), and never says how to remove it. Fix: state the size, show both paths, and add the delete command.

**23. Low. Windows and Python-version details.** `[reasoning]` (a) `py -V:3.13` needs a recent Python launcher; older launchers only accept `py -3.13`, so the text should name the form that works with Part 01's install. (b) The heading "7.1 to 7.3" followed by bold run-in labels makes "Section 7.3" hard to find. (c) The ceiling "Python 3.11 to 3.13" is not explained; PyPI shows torch 2.14.1 and transformers 5.20.2 support 3.14, and the lab is standard library only, so a reader whose default is 3.14 is told to install an older one for no stated reason (I had no 3.14 to test).

**24. Low. Section 9 self-check wording.** `[run: read as a beginner]` (a) Question 1 asks how a score can "overstate" skill; saturation (a test most models ace) makes scores less useful for ranking rather than overstating anyone's skill. Reword to "mislead". (b) The answers sit directly under the questions, so the reader cannot try first; add "cover the answers" or move them to the end.

**25. Low. Section 9 prerequisites.** `[run: read as a beginner]` Section 7 requires Part 01's setup, but the prerequisite list names Parts 02, 05, 10 and 11 only. "Reading a little Python" understates what the exercises ask (running `python -c` one-liners from a terminal). Fix: add Part 01 and "using a terminal".

**26. Low. Section 9 Exercise 2 ("on a laptop").** `[run]` The answer (9.54 GB, yes at 16 GB, no at 8 GB) matches. But "16 GB" is not said to be RAM or GPU memory, `fits()` silently keeps a fifth free (12.8 GB and 6.4 GB are the real limits), and GB means 1e9 bytes, not 2^30. The yes and no do not change, but a careful reader who recomputes with GiB or without the reserve will wonder. Fix: add one sentence naming the unit and the fifth-free rule.

**27. Low. "Best next resources" and the tutor prompt.** `[run: read as a beginner]` The resources are listed only by code (`[V: LOR]`, `[V: QLR]`, `[V: OVA, GEK]`, `[V: PFT]`, `[V: TRL]`, `[V: MCR]`) with no titles, years or links in the text given, so a beginner cannot open them (this may be an artifact of the excerpt). The tutor prompt is introduced as "modelled on claude/github-tutor-prompt.md", a path the reader does not have; and the prompt never mentions the lab or `adaptmath.py`, so the tutor cannot ask the reader to run the exercises.

**28. Low. Jargon that Section 6 uses before any gloss in Sections 6 to 9.** `[run: read as a beginner]` wheel ("Windows wheel 124 MB"), gated models, telemetry, Trainer, SFT/DPO/GRPO, YAML, WSL2, Ascend, QLoRA, adapter, "all linear layers", `r`, "processor" (meaning CPU), "Pinned", "masks each prompt". LoRA is explained only in Section 9 (misconception 3), after Sections 6 and 8 use it. Earlier Parts or Section 3 may define these; I only saw 6 to 9. Fix: gloss on first use or add "(defined in Section X)".

**29. Low. Platform claim for MLX-LM and the lab's licence line.** `[PyPI]` / `[run]` The MLX-LM row says "macOS on Apple silicon"; its PyPI metadata also offers `cuda12`, `cuda13` and `cpu` extras, so it can run elsewhere (the pick is still right for Macs). The lab row says licence "This series", but the zip has no LICENSE file, so a reader cannot tell if they may reuse or share the scripts.

**30. Low. Mutation labels are paraphrased.** `[run]` Section 8 step 6 lists "Qwen's biases left out", "only A counted and not B", "the prompt left unmasked"; the script prints "q, k and v biases left out", "only A counted, not B", "prompt not masked: the model learns to write the question". All nine items exist; the wording differs, which a literal-minded beginner may notice. Fix: use the script's words.

## Commands run, Python version, and match

Python versions: 3.13.16 (`python3.13`), 3.12.3 and 3.11.17 (`/usr/bin/python3.12`, `/usr/bin/python3.11`). On 3.12 and 3.11 each command's full output was byte-for-byte identical to 3.13's (checked with `cmp`).

| Command (as written, from the lab folder unless noted) | Python | Text says | Result |
|---|---|---|---|
| `python3 -m zipfile -e engineering-stack-lab-part-12.zip ~/ai-stack` (run from the folder holding the zip) | 3.13.16 | unzips into `ai-stack` | Matched. Fails with FileNotFoundError from any other folder (problem 14) |
| `python3.13 -m venv .venv`, `source .venv/bin/activate`, `python run_lab.py` | 3.13.16 | `17 of 17 checks passed` | Matched, 17 PASS lines, exit 0 |
| same, with `/usr/bin/python3.12` and `/usr/bin/python3.11` (venvs `.venv312`, `.venv311`) | 3.12.3, 3.11.17 | same | Matched, identical output |
| `python mutation_check.py` | 3.13 / 3.12 / 3.11 | `33 of 33 mutations caught`, "about 20 seconds" | Count matched. Time did not: 2.28 s / 1.90 s / 1.79 s (problem 10) |
| `python demo.py` | 3.13 / 3.12 / 3.11 | six tables | Matched in count and titles; the excerpt shows no table values to compare |
| `python datacheck.py data/train.jsonl data/test.jsonl` | 3.13 / 3.12 / 3.11 | finds duplicate and leak, `2 problem(s) found`, exit 1 | Matched: "example 12 repeats example 3", "test: example 2 shares 13 words in a row", exit 1 |
| `python reader_lora.py --plan` | 3.13 / 3.12 / 3.11 | predictions, no download | Ran, exit 0; no expected text to compare (problem 8) |
| `python reader_lora.py` and `--steps 24` (no torch) | 3.13 / 3.12 / 3.11 | `Missing package (torch). Install torch, transformers and peft first (Part 12, Section 7.5), or run with --plan.` | Message matched exactly; printed after two prediction lines; exit 2 (problem 8) |
| `python -c "import adaptmath as am; ... lora_params(am.QWEN3_06B, am.ALL_LINEAR, 16)"` (7.4) | 3.13 / 3.12 / 3.11 | `10092544` | Matched |
| Section 8 step 2 one-liner (`QWEN25_3B`, `['qwen2']`, r 16) | 3.13 | `3686400 3085938688`, sum 3,089,625,088 | Matched; sum checked by hand |
| Section 8 step 4 with a `bot` line (three variants) | 3.13 | "the checker names the line" | Names the line (`train line 13`); problem count 4 or 5, not stated (problem 1) |
| Section 8 step 5: edit line 67 to `2 + 2 + 8`, run, restore | 3.13 | `16 of 17 checks passed`, `c07_full_finetuning_memory` fails, restore gives 17 | Matched. Line 67 is correct. Exit code 1 on failure |
| Step 4 edited in place, then step 5, then `mutation_check.py` (scratch copy) | 3.13 | `16 of 17` | Did not match: `15 of 17`, then `FAIL the unbroken copy doesn't pass` (problem 1) |
| Exercise 1 | 3.13 / 3.12 / 3.11 | `167772160 2.09` | Matched; hand-checked (81,920 per layer at r=1, x64 x32 layers) |
| Exercise 2 | 3.13 / 3.12 / 3.11 | `9.53679872 True False` | Matched |
| Exercise 3 | 3.13 / 3.12 / 3.11 | `4.81 True` | Matched |
| 7.6 row 2 (run `run_lab.py` from `~`) | 3.13 | `can't open file '.../run_lab.py': [Errno 2] No such file or directory` | Matched (output begins `python: can't open file`) |
| 7.6 row 4 (`2 problem(s) found`) | 3.13 | as above | Matched |
| 7.6 row 5 (stub tokenizer whose prompt is not a prefix) | 3.13 | `The chat template's prompt isn't a prefix of the full example.` | Message matched; exit code 1 (the same code as a count mismatch) |
| 7.6 row 1 (PowerShell policy), 7.1 Windows steps, macOS steps | not run | | Reasoning only (problems 14, 23) |
| Extra: `python reader_lora.py --help`; `python datacheck.py` with no or one file | 3.13 | | Help text cut off (problem 15); usage line printed; one-file run works |
| Extra: PyPI JSON for the eight tools in Section 6 (no install) | n/a | versions and Python limits in the table | All eight versions exist; Python limits (torch 3.10+, TRL 3.11+, Axolotl 3.12+, LLaMA-Factory 3.11+) and the Windows 124 MB wheel match; problems 2, 3, 13, 29 |
| `pip install torch==2.14.1 transformers==5.20.2 peft==0.21.2`; full `reader_lora.py --steps 24` | not run | | Not run, as instructed |

Other checks that passed: the five model dictionaries listed in Section 8 "Data" exist; all files named in "Files" are in the zip; the lab uses only ASCII; there are no em or en dashes in the lab files or in Sections 6 to 9; the mutation check leaves no temporary folders behind (7.7 claim); the Section 9 answer to self-check question 4 (2 + 2 + 12 bytes) agrees with `ADAM_MIXED_BYTES`, and question 5 agrees with the `llama3.1` rule in `SHARING`.

Not verifiable from here: demo table values against Sections 3 and 5, every [V: ...] source claim, model and product names dated after my own knowledge (for example the shortlist entries), the "170 MB, about 40 packages" Windows estimate, the Windows and macOS steps, and the full R3 run (loss values, speed, adapter size).

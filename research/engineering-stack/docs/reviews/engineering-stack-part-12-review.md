# Engineering Stack Part 12: Phase 4 Review

*October 19, 2026. The Phase 4 record for claude/engineering-stack-part-12-adapting-models.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding below was reproduced by the lead session before it was fixed: source files were fetched again at the pinned commits (mistralai/platform-docs-public e7de7a7, LLaMA-Factory v0.9.5, llama.cpp b11739), web pages were read again (Biderman et al., arXiv 2405.09673v2), PyPI's listings were re-read for torch 2.14.1 and its Linux dependencies, and lab outputs were rerun. Raw checker notes are in engineering-stack-research-part-12.zip, sent to the owner.*

## Who checked what

| Check | By | Result |
|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet; only claims and sources (Sections 1 to 3.6) | 61 claims: 52 supported, 8 partly, 0 contradicted, 1 not checkable; 41 lookups |
| Blind source check B | Same rules (Section 3.7 onward) | 110 claims: 97 supported, 10 partly, 0 contradicted, 3 not checkable; 39 lookups |
| Beginner test | Fresh agent on Claude Sonnet, Sections 6 to 9 literally, as a new Linux user, fresh environments on Python 3.13.16, 3.12.3, 3.11.17, without PyTorch | 2 high, 7 medium, 21 low; every printed number matched, byte for byte across the three Pythons |

## Findings

### F-01 · High · The data step broke the lab's own checks
- **The draft said:** Section 8, step 4: "make your own copy of one training line with the role `"bot"` and run it again".
- **What goes wrong:** the natural reading edits `data/train.jsonl`, which check c14 reads, so step 5 gives 15 of 17 instead of the promised 16, and step 6 stops with "the unbroken copy doesn't pass".
- **Why:** tester 1; reproduced by editing a copy and running `datacheck.py` and `run_lab.py`.
- **Fix:** step 4 now copies the file to `data/mytrain.jsonl`, says exactly what to change, warns not to touch the original, shows the three-problem output, and says to delete the copy.

### F-02 · High · "It runs on any computer"
- **The draft said:** Section 6, PyTorch "Windows, macOS, Linux"; Section 7.5 "It runs on any computer" and "about 170 MB".
- **What goes wrong:** Intel Macs and Windows on Arm get "No matching distribution"; Linux readers download several GB, not 170 MB.
- **Why:** PyPI's file list for torch 2.14.1 has wheels only for macOS 14 on Apple silicon, 64-bit Windows and manylinux_2_28 (x86-64 and Arm); the Linux wheel is 554.6 MB and requires NVIDIA's cuDNN, NCCL, cuSPARSELt, NVSHMEM and Triton on Linux, each hundreds of MB (tester 2 and 3; reproduced from PyPI's JSON).
- **Fix:** Section 6's row lists the platforms and both sizes; Section 7.5 gives the Windows and Linux sizes, the platforms without a wheel, and marks PyTorch's processor-only builds as unchecked; Section 7.6 has a "No matching distribution" row.

### F-03 · Medium · "Retrieval beat fine-tuning by 19 to 31 points"
- **The draft said:** Sections 1 and 9.
- **What goes wrong:** the range is against fine-tuning on paraphrases only; against plain fine-tuning the gaps are 36.5 to 37.1 points, and Section 9 cited a second paper for the number.
- **Why:** Ovadia et al., Table 2 (checker B, B096; recomputed: 0.875 - 0.504, 0.585 - 0.219, 0.876 - 0.511).
- **Fix:** "19 to 37 percentage points" in Sections 1 and 9, with the number tagged to Ovadia alone; Section 3.6 gives both ranges.

### F-04 · Medium · Hosted fine-tuning overstated as closed
- **The draft said:** Section 1, "the big hosted services have mostly stopped selling it"; Section 3.10, "Mistral marks its fine-tuning deprecated".
- **What goes wrong:** OpenAI's existing active customers can still start jobs until January 6, 2027, and Mistral's docs disagree with themselves.
- **Why:** mistralai/platform-docs-public at e7de7a7: `resources/deprecated/finetuning/page.mdx` says deprecated, while `_guides/finetuning_sections/_01_intro_basics/page.mdx` line 5 says "Mistral provides a fine-tuning API in Studio" (checker A, A006; reproduced).
- **Fix:** Section 1 says the services are closing to newcomers; Section 3.10 reports both Mistral pages and marks the guide's publication [U]; Section 6's skip list says Mistral's docs mark it deprecated.

### F-05 · Medium · The Muse revenue condition lost its scope
- **The draft said:** "above a revenue threshold a separate agreement with Meta is needed".
- **What goes wrong:** the condition applies to offering the model as a hosted service, not to every use.
- **Why:** Muse Spark Open card, licence summary (checker A, A040; matches researcher row C042).
- **Fix:** Sections 3.4 and 3.12 say "offering it as a hosted model service above 20 million US dollars of revenue"; the lab's note says the same.

### F-06 · Medium · Biderman's rank finding narrowed
- **The draft said:** LoRA "nearly matched full fine-tuning for instruction tuning only at rank 256".
- **What goes wrong:** true for code; for maths "r=64 suffices to approach full finetuning".
- **Why:** arXiv 2405.09673v2, Section 4.1 (checker B, B016; re-read).
- **Fix:** "256 for code, while 64 came close for maths".

### F-07 · Medium · Undefined steps and outputs for a beginner (tester 4, 5, 6, 7, 8)
- **What goes wrong:** "reader test R3" used before it is defined; "(Section 12)" for a table that comes after it; no note that commands run from the lab folder with the environment active; no way to map `config.json` names to the lab's dict; missing common errors; the `--plan` output not shown and its total (134,515,008) not reconciled with PEFT's expected 134,975,808; exit codes unexplained.
- **Why:** each reproduced by running or reading the command.
- **Fix:** a forward reference to Section 7.5; "Run on your computer" named; a sentence at the top of Section 8's steps; the field mapping, with what isn't in config files and the block layout it assumes; three new rows in Section 7.6; the `--plan` lines shown, the 460,800 difference explained, and exit codes 0, 1 and 2 stated.

### F-08 · Low · Smaller source mismatches (checkers)
- A032: Hugging Face retired its leaderboard as "slowly becoming obsolete", not because tasks "no longer separated models". Fixed.
- A003, A050, A061, A004: "a few dozen" tasks, "change one thing at a time", two reasons to fine-tune and the format sentence weren't in the cited pages. Now Mistral's "100 test cases can be enough", Anthropic's "Upgrade only if necessary", the rest marked [I], and the format sentence tagged to Hugging Face's course.
- B011: the non-embedding count was 440,466,432, the block layers alone; 596,049,920 less the embedding is 440,467,456. Fixed.
- B057: the Llama 3 clause now keeps "(excluding Meta Llama 3 or derivative works thereof)". B052: "seems to work", not "seem". B076: PyTorch's licence list adds "Apache-2.0 WITH LLVM-exception". B080: MLX-LM's PyPI page also lists Linux. B083: LLaMA-Factory documents AMD ROCm. B088: Unsloth's README lists CPUs for running models, while its training code stops without a GPU; both now said. B094: Llama 3 8B's configuration is Part 11's. B106: Ovadia also used five MMLU subjects. B108: "numbers neither side published in full" replaced by "not recomputed here". A042: "flagship" replaced by "largest". A045: 4.89 bits is Part 11's figure, now said. A007: the naming row says only that old links lead to arena.ai.

### F-09 · Low · Polish (tester)
- The mutation check takes about 2 seconds, not 20 (tester 10). The break-it FAIL line was empty; check c07 now prints the value it got, `18000000000.0` (11). The adapter is about 1.9 MB with its config file (12). The Linux unzip command works from the zip's folder (14). `--help` cut its description mid-sentence (15). Undefined names in a code snippet (16). How to set an environment variable in each shell (18). The demo's "test PC's RAM" label (20). A cross-reference to Sections 3.4 to 3.7 that should run to 3.10 (21). Part 01 missing from the prerequisites (25). "16 GB" without "of memory" (26). "Wheel" glossed (28). Each fixed.

## Not acted on, with reasons

- **Process and self-reference claims** (A039, B050, B075, B084): reading dates, the lab's own files and an internal cross-reference can't be checked against an outside source; they stand as written.
- **Venue hedges** (A021): the arXiv comment and the authors' README both say TMLR for Biderman et al.; the series names a venue as confirmed only when seen on the publisher's page, so the hedge stays.
- **GPT-3's Appendix C** (A033) wasn't read; Section 4 states the 13-word rule, which is what the lab uses.
- **Tester items left as the series' convention:** tag definitions sit in "How to read this part" (4, in part); sources listed by key (27); `py -V:3.13` from Part 01 (23); self-check wording (24); the demo table's layout (20, in part); the model's download size, not checked (22); paraphrased mutation labels (30); the advice for picks without numbers (19).

## After the fixes

`run_lab.py` 17 of 17 and `mutation_check.py` 33 of 33 on Python 3.13.16, 3.12.3 and 3.11.17, also from a fresh unzip of the rebuilt zip; `demo.py` output identical on all three; the break-it step gives `16 of 17` with the value on the FAIL line; the edited-copy data step prints the output Section 8 shows; no `lab12` folders left in the temporary folder [T]. The part is about 87 KB, under the 100 KB cap, with no em or en dashes.

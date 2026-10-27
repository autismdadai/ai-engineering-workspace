# Engineering Stack Part 11: Phase 4 Review

*October 19, 2026. The Phase 4 record for claude/engineering-stack-part-11-running-models.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding below was reproduced by the lead session before it was fixed: source files were fetched again at the pinned tags (vLLM v0.31.0, SGLang v0.5.22, llama.cpp f336359, Ollama v0.40.5, Megatron-LM 3888b34, LMDeploy v0.18.0, lmstudio-ai/docs 4f8082f, mlcommons inference_results_v6.1 and policies), web pages were read again, and lab outputs were rerun. Raw checker notes are in engineering-stack-research-part-11.zip, sent to the owner.*

## Who checked what

| Check | By | Result |
|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet; only claims and sources (Sections 1 to 3.8) | 108 claims: 90 supported, 17 partly, 0 contradicted, 1 not checkable; 45 lookups |
| Blind source check B | Same rules (Section 3.9 onward) | 99 claims: 82 supported, 14 partly, 0 contradicted, 3 not checkable; 43 lookups |
| Beginner test | Fresh agent, Sections 6 to 9 literally, as a new Linux user, fresh environments, Python 3.13.16, 3.12.3, 3.11.17, with its own stand-in for Ollama | 1 high, 10 medium, 14 low; every printed number matched; mutation check 14.3 s, 15.5 s and 12.1 s |

All three agents were stopped by usage limits and a container restart on October 16. Check A finished that day; check B finished when resumed that evening; the beginner test was lost and rerun from the start on October 19. No finding depends on the lost run.

## Findings

### F-01 · High · "Llama 4 is Meta's current line" is out of date
- **The draft said:** Section 4, ledger P10-09b: "Outdated (settled in Part 10): Llama 4 is Meta's current line".
- **What goes wrong:** a reader picking an open-weight Meta model would miss Meta's newer releases.
- **Why:** Hugging Face's verified "meta-models (Meta Inc.)" organization lists Muse-Glimmer-30B (card: "License: apache-2.0", "Model Release Date: August 2026") and Muse-Spark-Open-816B-A42B. Found by checker B (B048), which saw Muse names in llm-compressor, llama.cpp and MLX-LM files; reproduced by the lead on October 19 from the organization page and the model card.
- **Fix:** Section 4's row names Muse Glimmer and Muse Spark Open; Section 3.8 notes Muse Glimmer needs about 18 GB at Q4_K_M [T]; new source MUS; Section 10 flags Part 10 and claim ledger P10-09b for Phase 5.

### F-02 · Medium · `OLLAMA_NO_CLOUD` doesn't stop the update check
- **The draft said:** "Ollama calls ollama.com unless told not to" (Section 9); "To keep it local, ... add `OLLAMA_NO_CLOUD`" (Section 7.5).
- **What goes wrong:** a reader sets the variable and believes nothing leaves the computer.
- **Why:** Ollama v0.40.5 `server/model_recommendations.go` returns early when `envconfig.NoCloud()` is true; `app/updater/updater.go` checks `https://ollama.com/api/update` every `60 * 60 * time.Second` under the comment "Always check for updates", with no such test (checker B, B084, with B051, B076, B077; reproduced). The same code stores a `Survey` setting, `DEFAULT TRUE` in `app/store/database.go`, described in `app/store/store.go` as whether "the user allows anonymous inference information to be shared with Ollama"; a search of the v0.40.5 code found no other use (checker A's note on A088 and A095; reproduced).
- **Fix:** Sections 3.8, 4, 7.5, 9, 10 and the cheat sheet say what the variable stops and what it doesn't; Section 3.8 reports the stored `Survey` setting.

### F-03 · Medium · Megatron-LM's figures made to refute a claim they can't refute
- **The draft said:** P4-05 "Unsupported: NVIDIA reports 41% to 48% of peak compute used on up to 6,144 H100s".
- **What goes wrong:** model FLOP utilization of 41% to 48% neither proves nor disproves "rarely compute-bound", and the range is across model sizes, not one 6,144-GPU job.
- **Why:** Megatron-LM README lines 96 to 123: "MFU increases from 41% to 47" to "48% with model size" (the README prints a dash between 47 and 48), "6,144 H100 GPUs: Successfully benchmarked 462B parameter model training", strong scaling "from 47% to 42%" (checker B, B033 and B023; reproduced).
- **Fix:** Sections 3.10 and 4 define MFU, scope the range, and say no source read measures the claim [U].

### F-04 · Medium · vLLM's metrics example misquoted
- **The draft said:** "in chunks of 1, 2 and 2 tokens".
- **Why:** vLLM v0.31.0 `docs/benchmarking/cli.md` line 158: "The three tokens in the second streamed output do not create additional ITL samples"; its figure labels Output 2 "bundled" T2 T3 T4 (checker A, A077; reproduced).
- **Fix:** Section 3.6 says 1, 3 and 1; the lab's check c13 and `demo.py` now use vLLM's chunks (TTFT 100 ms, TPOT 20 ms, ITL 40 ms, unchanged).

### F-05 · Medium · LM Studio called "free"
- **The draft said:** "free for personal and internal business use" (Sections 3.8 and 6).
- **Why:** the terms (Version: August 23, 2026) grant use "solely for Your personal and / or internal business purposes" and say "Certain features of the Software may be offered for a fee"; no sentence says the software is free (checkers A and B, A101 and B064; reproduced). The docs list Windows on Arm and Linux too.
- **Fix:** Sections 3.8 and 6 quote the licence scope, mention paid features and list all three systems; "Best free option" now excludes LM Studio.

### F-06 · Medium · Quality claims missing their scope
- **The draft said:** "speed rises" (Section 1); "+2.79%" without its row; "small models and low-resource languages lose most" (Sections 3.3 and 4).
- **Why:** llama.cpp `tools/quantize/README.md` (Llama 3.1 8B table): generation 71.93 against 29.17 t/s, but prompt processing 821.81 against 923.49 t/s; `tools/perplexity/README.md`: +2.79% is the row without an importance matrix, +2.40% with one; MAR's abstract says 4-bit "often preserves translation quality for high-resource languages and large models" and that GGUF variants were the most consistent (checkers A and B, A002, A056, B054, B083, B095; reproduced).
- **Fix:** Section 1 says generation speeds up; Section 3.3 adds the importance-matrix figures (+2.40%, +8.04%, +38.74% [T]) and words the MAR finding as its abstract does; Section 4's B4-05 row scoped.

### F-07 · Medium · MLPerf called "the independent benchmark"
- **Why:** MLPerf's policies make submitters the reviewers ("Representatives of each submitter"); the word "independent" isn't in them (checker B, B091; reproduced with a search of mlcommons/policies at 45b8b62).
- **Fix:** Sections 1, 3.6 and 10 call it shared and peer-reviewed by submitters.

### F-08 · Medium · Beginner steps that fail or mislead
- `rm.gguf_bytes(rm.llama_tensors(cfg), ..., n_layers)` gave `NameError: name 'cfg' is not defined` (tester 2): Section 7.4 now defines `cfg`, and the call returns 4912898048 [T].
- Windows: no pointer to the PowerShell script-policy fix, no new window after installing, no re-activation, no way to find the bandwidth (testers 1, 6, 8): Section 7.5 follows Ollama's FAQ steps, points to Part 01, Section 7.1, step 5, gives the transfer-rate formula, and says to use a GPU's or a Mac's bandwidth when the model runs there; the script's "Above the ceiling" message says the same.
- No steps for macOS or Linux (tester 10): added from Ollama's FAQ (`launchctl setenv`; `systemctl edit`).
- The llama.cpp route had no file name or full command (tester 7): now the Qwen3-4B-GGUF page, `Qwen3-4B-Q4_K_M.gguf` and the full `llama-bench` line.
- "29.7 tokens per second" holds only for exactly 1.4e9 bytes (tester 11): now "about 30".

### F-09 · Low · Smaller source mismatches (grouped)
- SGLang retracts "the same way" (A065): its victim is the request with the fewest generated tokens or lowest priority, and beam-search groups are aborted (`schedule_batch.py`). Reworded.
- "Norms stay 32-bit" (A049): `src/llama-quant.cpp` says only "do not quantize norm tensors". Reworded; the lab's 32-bit count noted.
- 4.8944 is published for Llama 3.1 8B (A015); the community's "4.92 GB" and "metadata" (A051); Ollama loads GGUF needed OLS (A013); Llama 3.2 licence needed LLM (A104); "each new token needs every weight read once" needed Pope et al., "once per forward pass" (A004); the α-below-c clause is the lab's inference from Theorem 3.8 (A070); SGLang's paging analogy (A001); "do this" (A003). Each fixed.
- Dense H100 figures come from the rule NVIDIA prints for Blackwell, "Dense is ½ sparse spec shown", not an H100 page; "pruned" isn't in NVIDIA's text (B001, B002, B036). Reworded with the preliminary table's 2,000 and 1,000.
- MI355X "matches Blackwell Ultra's memory" (B009): no NVIDIA page read gives 288 GB per GPU. Now the bandwidth match only.
- EAGLE-3's batch table was run by the SGLang team (B090); LMDeploy's README dates one claim to 2024 (B090). Fixed.
- Ollama's library pages: granite4's does name its licence (A108). Fixed.
- "Official routes" for llama.cpp left out conda-forge, Nix and Docker (A099); "no background service" and "no update checks" weren't in the sources (B063). Fixed or dropped.
- "a few weeks later" (B008), Slurm's GPL version 2 or later (B026), the Ollama uninstaller's ticked "Remove models" box (B080), vLLM's fourth protected prefix `/cohere` on its security page (A068), NVIDIA's 2.86 times from an earlier post and build (A072), EAGLE-3's model and benchmark (A074), LMDeploy's Ascend builds (A085), vLLM's 199 packages as this session's own download [T] (A081). Fixed.

### F-10 · Low · Beginner-test polish
- Docstrings: 6 of 24 functions have none (tester 3). Section 8 now says sources are in comments and docstrings.
- Abridged blocks not marked; the `...` after the last check (testers 4, 18). Marked and moved.
- `--self-test` never said it passed (tester 5): `reader_local.py` now ends `Self-test passed: these numbers come from the stand-in, not a model.`
- Four checks fail in the break-it step, not three; c08 printed no value (testers 12, 13): text corrected; c08's asserts now print their values (`FAIL c08_what_fits: AssertionError 80573`).
- `Run:  ollama pull` had two spaces (tester 14): one now.
- Partial error quotes, "Start menu" only (tester 15); "as large as" (16, the cache is 87% of the weights); the development note in step 7 (17); exercise 2's unexplained byte count (19); the silent Linux unzip (20); unlabelled 7.1 to 7.3 (21); no line number or editor in step 5 (22); α, γ and c undefined in exercise 3 (23); "Sections 3 and 5's tables" (24); `python` after `deactivate` (25). Each fixed.

## Not acted on, with reasons

- **Claim-extraction artifacts** (A047, B058, B061, B070): a tag line, an italic heading, the lab's own table row and a "Sources" line became empty or untestable claims in the checkers' lists. The paper's text is fine; the extraction script should skip such lines next time.
- **A081 to A089 share one source list per table** (Section 3.7): each row names one engine, whose source key is its own; left as is.
- **Granite 4 micro's 2.1 GB** (A106): Ollama's page pairs "3b (micro)" with `granite4:3b`, which is 2.1 GB (re-read October 19).
- **Newer releases since October 16** (B060, B062: Ollama v0.40.6, llama.cpp b11706): the tools table is dated; the freshness ledger records them.
- **Scope notes already in the text or minor** (A063's wider body ranges, A066's 1,024-sequence condition, A073's dataset, B018, B020, B027): no change.
- **Tags and file paths outside Sections 6 to 9** (tester 9 in part, tester 23's tutor-prompt path): the tags are defined in "How to read this part"; the path follows the series' convention.
- **Two findings rested on sources Section 12 didn't locate precisely:** "published September 16, 2026" (A079) is the embargo date in the title of MLPerf's supplemental PDF ("UNDER EMBARGO UNTIL 9/16/26 8:00 AM PT"), and "NeurIPS 2024" for Dutta et al. (A056, B083) is on the proceedings page; both kept, with Section 12 now pointing to them.

## After the fixes

`run_lab.py` 14 of 14 and `mutation_check.py` 31 of 31 on Python 3.13.16, 3.12.3 and 3.11.17; `demo.py` output identical on all three (only table 8's chunk sizes changed); `reader_local.py --self-test`, an empty model list and a closed port print the messages Section 7.6 quotes; the break-it step gives `10 of 14` with a value on every FAIL line; the rebuilt zip passes from a fresh unzip; no `lab11` folders left in the temporary folder [T]. The part is 92,339 bytes, under the 100 KB cap, with no em or en dashes.

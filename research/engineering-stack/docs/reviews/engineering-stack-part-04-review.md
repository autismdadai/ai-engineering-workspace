# Engineering Stack Part 04: Phase 4 Review

*October 13, 2026. The Phase 4 record for claude/engineering-stack-part-04-context.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed: source findings by re-reading the source, lab findings by re-running the step. Evidence class: project audit.*

## Who checked

| Check | Who | Input | Result |
|---|---|---|---|
| Blind source check A | Claude Sonnet agent, about 45 web lookups | 85 claims (context windows, tokens, overflow, compaction, position effects) and their source links only | 72 supported, 12 partly, 0 contradicted, 1 could not check |
| Blind source check B | Claude Sonnet agent, about 22 web lookups plus GitHub source files | 69 claims (prompt caching, prices, engines, privacy) and their source links only | 56 supported, 11 partly, 0 contradicted, 2 could not check |
| Beginner test | Claude Opus 5.5 agent (the session's model), fresh folder and fresh environments | The lab zip and Sections 3 and 7 to 9 only | Lab passed on Python 3.13.16, 3.12.3, 3.11.17; every shown output matched; 15 problems in the instructions |

The two researchers (Claude Opus 5.5 agents; 71 and 78 claim rows, saved in the research zip) are not counted as checks: their tables fed the draft. The beginner test ran on the same model family as the author, so it is independent in context, not in model.

## Source findings

| # | Severity | Quote (draft) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| S1 | Medium | "every one of 18 models did better ... given a focused prompt" (and three similar lines) | Overstates the scope | Chroma's appendix: "Not all 18 models are included in each experiement"; the LongMemEval section says "Across all models, we see significantly higher performance on focused prompts" (re-read by the author) | "across all the models it ran", quoted, with the appendix caveat |
| S2 | Medium | "accuracy sank toward zero even at the edges" | Stronger than the paper | NoLiMa §4.4.2: larger contexts "shift the entire trendline downward toward zero", "with performance declining even at the edges" (re-read) | Quoted exactly |
| S3 | Medium | OpenAI lookback: "Automatic routing" | Wrong kind of answer | OpenAI's caching page: implicit mode checks "up to 20 earlier eligible message endings" (re-read) | Cell replaced; Gemini's cell now "Not stated [U]" |
| S4 | Medium | Gemini's savings "aren't guaranteed" | Paraphrase in quotation marks | Google's caching page: "no cost saving guarantee" (re-read) | Exact words used, in two places |
| S5 | Medium | "It doesn't make generation faster, only the processing of the prompt [V: VPC]" | The cited design page doesn't say it | vLLM's feature page: APC "does not reduce the time of generating new tokens (the decoding phase)"; the same page says "Set `enable_prefix_caching=True`" (re-read) | Feature page added to the source entry; sentence quotes it |
| S6 | Low | "[V: LUM, Table 1]" | Wrong table | Lumer et al. v2: the comparison is Table 2, "Full comparison of cache modes across all models" (re-read) | Table 2; figures unchanged (27.8 to 81.4% cost) |
| S7 | Low | "every major API caches identical prefixes" | Too broad for three cited vendors | APC, OPC, GCC cover three vendors | "Anthropic, OpenAI and Google all cache identical prefixes, automatically or when you mark them" |
| S8 | Low | "That last warning holds everywhere: implicit caches are best effort" | Generalizes from two sources | Bedrock "best effort", DeepSeek "best-effort", Google "no cost saving guarantee" | Each vendor's own words |
| S9 | Low | OpenAI GPT-5.6 and later "have the same 1.25x and 0.1x" | GPT-6.1 Sol reads at 0.05x | OPC; break-even unchanged | Exception named |
| S10 | Low | Song preprint: hit rates "levelling off near 0.83 over 30-call sessions" | Missing "below that threshold" | Abstract: "below which the hit rate plateaus at rho~0.83" (re-read; sole author Yan Song) | Quoted |
| S11 | Low | "OpenAI routes by load and prefix hash" | "load" not seen by the checker | OPC lists "Current machine load and available capacity" (re-read) | Kept, quoted |
| S12 | Low | HELMET: needle tests "do not reliably predict downstream performance" | Drops the qualifier | Abstract: "synthetic tasks like NIAH do not reliably predict" | Full phrase quoted, in two places |
| S13 | Low | "Chroma sells a retrieval database" | Not on the page | Chroma calls itself "the open-source search infrastructure for AI" and lists ChromaDB | "Chroma makes ChromaDB, an open-source search database" |
| S14 | Low | OpenAI `truncation` `auto`: "nothing tells you in the reply what was dropped" | Not in the source | The reference describes the behaviour only | Now an open question [U] |
| S15 | Low | Google `countTokens` "counts system instructions, tools and media" | The page shows those through usage fields | GTK | "Counts a request's input, media included" |
| S16 | Low | "Shared caches leaked ... in 2024" | The paper is from 2025 | Gu et al. ran the audit in autumn 2024 and posted it in February 2025 | "In tests run in 2024 (published 2025) ... at seven providers" |
| S17 | Low | The SGLang default "suggests the cache is on" | Checker B located the declaration | v0.5.21 `arg_groups/fields/memory.py`: `disable_radix_cache` with help "Disable RadixAttention for prefix caching." defaults to `False` (read by the author from the release tag) | Settled [T] |
| S18 | Note | Esmi et al. models; GPT-4.1 guide date | Incomplete scope | The abstract also names GPT-4; the guide is undated (model ID `gpt-4.1-2025-04-14`) | Both added |
| S19 | None | "Versions from PyPI"; the worked example's 91,500; "critical" (P2-11) | "Could not check" | A placeholder URL pattern; the worked example and the Gemini paper weren't given to the checker, on purpose | No change |

## Lab and instruction findings

| # | Severity | Quote (draft) | What goes wrong | Why (reproduced) | Fix |
|---|---|---|---|---|---|
| L1 | High | "a 30% margin for a newer tokenizer" (`margin=0.3`) | Wrong size: 30% more tokens needs a budget divided by 1.3, a margin of 1 - 1/1.3, about 23%; the worked example's "handbook goes too" came from over-correcting | Recomputed: contract plus handbook at 1.3x is 855,660 tokens, which fits in 872,000 | Planner takes `growth` (divides the budget); worked example, check 2, the mutation and the text changed; with growth 1.3 the plan still fits, with 12,569 to spare |
| L2 | High | "Add the rest in order of priority, until the next piece wouldn't fit" | The code skips a piece that doesn't fit and keeps adding smaller ones | After lab step 1's edit, the growth line drops the priority-5 contract and keeps the priority-3 handbook (re-run) | Step 3 rewritten; step 1 explains the line and says to change the priority back |
| L3 | Medium | `run_lab.py --with-tiktoken`: "three lines of counts" | `run_lab.py` shows only the optional script's last line | Re-run: one `[PASS]`/`[FAIL]` line | Text says to run `optional_tiktoken_check.py` for the counts |
| L4 | Medium | 7.6: wrong folder gives `No module named 'cache_sim'` | From the wrong folder, Python can't open `run_lab.py` at all (exit code 2) | Re-run | New row with the real message; `No module named` row now for the `-c` one-liners; exit code 2 explained in 7.5 |
| L5 | Medium | tiktoken not installed: `[FAIL] ... SKIP  tiktoken is not installed` | FAIL and SKIP on one line | Re-run | The optional script now prints FAIL with a clear reason and exits 1; 7.6 row added |
| L6 | Medium | Linux: `unzip ... -d ~/ai-stack` | `unzip` may be missing, and the folder to run it in isn't said; Part 01 uses `python3 -m zipfile -e` | Part 01, Section 7 | `python3 -m zipfile -e ... ~/ai-stack`, run in the folder that holds the zip |
| L7 | Medium | "one 8,000-token document" while every line shows 10,000 cached | The prefix includes tools and the system prompt; `input_tokens` unexplained | 400 + 1,600 + 8,000 = 10,000 | Explained before the output |
| L8 | Medium | `paper_numbers.py` shown nowhere; prints `[9, 14]` where the text says 10th and 15th | Zero-based indexes and an unexplained 12.5 | Re-run | Positions now counted from 1 (`[10, 15]`); the output line and the 12.5-point oracle gap explained in 7.5 |
| L9 | Medium | `--ollama MODEL` in the tour | Default of 200 trials is 1,000 model calls; without Ollama, a 65-line traceback | Re-run against no server and a stand-in server | `--ollama` defaults to 10 trials and prints the call count; one clear line and exit code 1 when Ollama isn't reachable |
| L10 | Low | "needle", `prompt_eval_count` | Undefined | | Defined where first used |
| L11 | Low | 3.3 says compare `prompt_eval_count` with what you sent; the script compares it with `num_ctx` on `/api/generate` | Text and script describe different checks | `placement_test.py` | Both explained |
| L12 | Low | "(Part 01, Section 6)" for installing Python 3.13 | Wrong section | Part 01, Section 7 | Fixed |
| L13 | Low | Partial output blocks unmarked | A reader expects the whole output | | "The first part of the output" |
| L14 | Low | 7.7: tiktoken's cache folder [U] | Settleable | tiktoken 0.14.0 `load.py`: `TIKTOKEN_CACHE_DIR`, then `DATA_GYM_CACHE_DIR`, then `<tempdir>/data-gym-cache` (read by the author from the installed package) | Settled [T] |
| L15 | Low | `... don't change these counts: 2 2`; pip's notice; "a third"; macOS `python3` | Unlabelled numbers; an unexplained notice; 30% isn't a third; `python3` may be 3.14 on macOS | Re-run | Labelled output; 7.6 row for the notice; "nearly a third"; macOS uses `python3.13` |

Not reproduced, so not changed: the beginner's guess that Windows Extract All nests the folder twice (no Windows test here; Part 01's and Part 02's Windows run used folders copied by script).

## Checks after the fixes

`run_lab.py` 13 of 13 and `mutation_check.py` 15 of 15 on Python 3.13.16, 3.12.3 and 3.11.17; every output block in Sections 3 to 8 re-run and matched; `--ollama` run against a stand-in server for both the normal and the "prompt filled the context" paths; October 13, 2026 [T].

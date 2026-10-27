# Engineering Stack Part 03: Phase 4 Review

*October 12, 2026. The Phase 4 record for claude/engineering-stack-part-03-prompts-as-interfaces.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed; one that didn't reproduce is marked so. Evidence class: project audit.*

## Who checked

| Check | Who | Input | Result |
|---|---|---|---|
| Blind source check A | Claude Sonnet agent, 23 web lookups plus shallow clones | 84 claims (structured outputs, tools, local runtimes, format studies) and their source list only | 79 supported, 3 partly, 0 contradicted, 2 could not check |
| Blind source check B | Claude Sonnet agent, 25 web lookups plus clones and the DSPy 3.4.0 wheel | 64 claims (reasoning models, DSPy, MIPRO, GEPA) and their source list only | 58 supported, 5 partly, 0 contradicted, 1 could not check |
| Beginner test | Claude Sonnet agent, fresh folder and fresh environments | The lab zip and Sections 7 to 9 only | Lab passed on Python 3.13.16, 3.12.3, 3.11.17; 16 problems in the instructions |

The two researchers (Claude Opus 5.5 agents; 72 and 56 claim rows) are not counted as checks: their tables fed the draft.

## Source findings

| # | Severity | Quote (draft) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| S1 | Medium, not reproduced | "a clear goal, strong constraints, and an explicit output contract" | Checker B couldn't find the quote on OpenAI's reasoning pages | The author found it on the Markdown view of https://developers.openai.com/api/docs/guides/reasoning.md: "Reasoning-capable GPT-5 models usually work best when you give them a clear goal, strong constraints, and an explicit output contract". The HTML view is cut off | Kept; quoted with its scope ("Reasoning-capable GPT-5 models") and the "tuning knob" sentence quoted exactly |
| S2 | Medium-low | "Constrained decoding scored higher with every engine" | Too strong | JSONSchemaBench Table 8: on Shuffle Objects, Llamacpp 52.6% equals LM only 52.6% (re-read by the author) | "On GSM8K every engine scored higher ... On Shuffle Objects one engine tied" |
| S3 | Low | "`logit_bias` (Chat Completions only)" | Contradicts Section 3.2 | OpenAI's OpenAPI spec has `logit_bias` in legacy Completions and Chat Completions; not in the Responses request | "Chat Completions and legacy Completions, not the Responses API" |
| S4 | Low | "Anthropic's and OpenAI's current pages list exceptions (refusal, `max_tokens`)" | Only Anthropic lists both | OpenAI's Structured Outputs page documents refusals; incomplete output appears only in code comments | "Anthropic's current page lists two exceptions ... and OpenAI's lists refusals" |
| S5 | Low | "MIPROv2 or GEPA only with a few hundred examples" | The threshold is documented for MIPROv2 only | DSPy optimizers.md: MIPROv2 with "200 examples or more to prevent overfitting"; nothing for GEPA | Attributed to MIPROv2; the budget cap and held-out test set labelled as this series' advice |
| S6 | Low | "Three optimizers, in order of cost" | The ordering is the author's | DSPy's docs give no cost ordering | "simplest first" |
| S7 | Low | "surpasses" free text | Misattributes the comparison | Tam et al. §4.1: "surpasses the other three methodologies" | "the other formats tested" |
| S8 | Low | "ran 10,000 real-world schemas" | The abstract says "10K"; Table 1 counts 9,558 (checker's reading) | JSONSchemaBench abstract and Table 1 | "thousands of real-world schemas ("10K" in its abstract)" |
| S9 | Low (checker note) | "can spend hundreds of dollars" | DSPy's own pages disagree | optimizers.md: "on the order of $2 USD", "up to tens of dollars" (author grepped the clone) | Both statements quoted; "Cap the budget before you start" |
| S10 | Low (checker note) | MIPROv2 "implemented with Optuna's tree-structured Parzen estimator" | Missing the install step | Optuna is an optional extra; MIPROv2 raises an ImportError suggesting `pip install dspy[optuna]` | Added |
| S11 | Low (checker note) | effort "`low`, `medium`, `high`, `xhigh` and `max`" | Not every model has `xhigh` | Anthropic's effort page (re-read by the author): "Not every model that supports `max` supports `xhigh`"; Opus 4.6 and Sonnet 4.6 lack it | Added, quoted |
| S12 | None | "The diagram renders with mermaid-cli 12.0.0"; "Sources: [V: ATD, OFC]." | "Could not check" | The first is a [T] result, not a source claim; the second was a table-source line split off by the extraction script | No change |

## Beginner-test findings

| # | Severity | Quote or step | What went wrong | Why it matters | Fix |
|---|---|---|---|---|---|
| L1 | Medium | Step 1, `python ticket_contract.py > ticket_schema.json` | PowerShell 5.1's `>` writes UTF-16; the linter crashed with `UnicodeDecodeError` (reproduced with a UTF-16 file) | The first lab step would fail on the owner's Windows computer | `schema_lint.py` reads UTF-8 and UTF-16; check 3 tests it; mutation "lint can't read UTF-16" |
| L2 | Medium | Step 2, "open it, and delete the line ... together with the comma" | No editor named; a leftover comma gave a raw `JSONDecodeError` traceback (reproduced) | A beginner can't tell a typo from a broken tool | Before-and-after lines shown, editor named; the linter prints `{"error": "not valid JSON: ..."}` with exit code 2; mutation "lint crashes on broken JSON" |
| L3 | Low-medium | Exercise 1 | A schema without `"type": "object"` got `"ok": true` (reproduced) | A false all-clear | The linter flags properties without an object type; full exercise JSON given; mutation "lint misses a missing object type"; the text says the linter checks only the `required` half |
| L4 | Low-medium | Section 7.6, the hash error's wording | pip prints "missing from some requirements" (reproduced with pip 26.2.1) | Exact-text search misses it, and pip's advice to add hashes is the wrong fix | Real wording; "Ignore pip's advice to add hashes" |
| L5 | Medium | "exit code 0", "exit code 1" | No command to see an exit code | Unverifiable for a beginner | `echo $?` and `echo $LASTEXITCODE` in Section 7.5 |
| L6 | Medium | Steps 3 and 5, "the output in Section 5", "Section 3.7" | The tester had only Sections 7 to 9 | Readers jump between sections | Outputs shown in place; a line on the tags |
| L7 | Medium | Section 7.3, "same commands as macOS" | No unzip command or folder creation; `python3-venv` may be missing on stock Ubuntu | First-run failure | Unzip commands for each system; the `python3-venv` note marked [R] |
| L8 | Low | Step 4, `blocks=5`, `blocks=10` | Unexplained | Confusing next to "five calls" | Explained: each call and each result is a block |
| L9 | Low | Exercise 2, "in a copy" | Where and how unclear; "45" lacks its baseline | | `cp toy_optimizer.py toy3.py`, the exact edit, "45 candidates, up from 33" (re-run by the author) |
| L10 | Low | Step 6 output | The version line differs per Python; `$ ` could be typed | | "The first line shows your own Python version"; `$ ` explained in Section 7 |
| L11 | Low | "about 70 packages" | 61 were added in a fresh 3.13 environment | | "about 60 packages (61 ...)" |
| L12 | Low | Section 7.4 | The DSPy file also asks for Pydantic | Unclear whether the hash check is bypassed | Install order stated; the author confirmed pip keeps the hash-checked 2.14.1 ("Requirement already satisfied") |
| L13 | Low | pip 24.0's `[notice]` line | Looks like an error | | Said to ignore it |
| L14 | Low | Undefined words | enum, refusal, `max_tokens`, 400 error, stand-in, mutation | | Rows added to Section 2 |
| L15 | Low | `schema_lint.py` with no file | Exit code 2 undocumented | | Exit codes 0, 1, 2 in the tour |
| L16 | Low | Section 7.7 | No delete command | | Commands for each system |

Reported but not changed: learning objectives 2 and 4 have no hands-on step, because live structured output and reasoning settings need a model and a key (the owner's decision: no keys). They are taught from the vendors' documentation and practiced with the tutor prompt.

## After the fixes

`run_lab.py`: 7 of 7, and 9 of 9 with `--with-pydantic --with-dspy`; `mutation_check.py`: 17 of 17 mutations caught. Python 3.13.16, 3.12.3 and 3.11.17, Ubuntu 24.04, October 12, 2026. Both exercises and the step 2 edit were re-run from a fresh unzip.

## Where Part 03 disagrees with existing project docs (flagged, not applied)

1. claude/prompt-construction-guide-2e.md §18 and claude/taxonomy-of-prompt-engineering-3e.md §10.5: constrained output "cannot" violate the schema. Anthropic documents refusal and `max_tokens` exceptions; OpenAI documents refusals. Erratum text is in the part, Section 10.
2. skills/sophisticated-prompt-generator/references/seven-axis-checklist.md (low temperature for single-answer tasks) and claude/new-skills-appendix.md §1 (the expander emits "low-temperature settings for structured output"): Claude's 5.x-era models reject any non-default temperature. Suggested erratum: "where the model accepts it".

Held until the series is finished, per the owner's decision of October 9, 2026.

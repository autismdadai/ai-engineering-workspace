# Session B review: Part 03

Part reviewed: `research/engineering-stack/docs/parts/engineering-stack-part-03-prompts-as-interfaces.md` (all 1,498 lines read). KEY rows checked: Appendix B rows 11 and 12, the only rows whose "Where" column names Part 03. I traced the toy optimizer (both validation sets, the 3-demo exercise), the tool loop, the retry loop, the linter report and the mutation list by hand against the listed code. Their printed outputs agree with the code. No web search, no commands run.

Severity key: error, overclaim, missing scope, inconsistency, unusable example, process trace.

## Rubric 1: every number carries model, task and year

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 1.1 | Section 1, "The problem it solves"; Section 3.2 table, row 1 | An invented failure rate and an unsupported frequency claim, with no model, task, source or [I] tag | "Asking nicely for JSON works most of the time. A program that breaks one time in fifty is still broken." and "Nothing. The model usually complies" | missing scope |
| 1.2 | Section 3.4, JSONSchemaBench paragraph | The sentence attaches "Llama-3.2-1B-Instruct" to every engine's figure, including OpenAI's API, which cannot have run on that model. The model behind 0.09 and 1.00 is never named; the next sentence only says the engines "ran on different models" | "On its "GitHub Hard" set with Llama-3.2-1B-Instruct, ... OpenAI's API handled 0.09, but every schema it accepted, it followed (compliance 1.00)" | missing scope |
| 1.3 | Section 3.5 table, dottxt row; Section 12, DTX | The figures have no year (the citation says "undated") and no metric name; "0.77 ... 0.78" could be accuracy or exact match | "reports GSM8K 0.77 unstructured against 0.78 structured [V: DTX]"; DTX: "dottxt blog (undated)" | missing scope |
| 1.4 | Section 3.7, "What they reported"; Section 4, GEPA row | The GRPO comparison names no model, gives no unit for "38.00 against 32.00", and doesn't say which score is which. The six benchmarks are not named. The previous sentence names Qwen3 8B and GPT-4.1 Mini, so a reader may assume one of them | "GEPA used 1,839 to 7,051 rollouts per benchmark where GRPO used 24,000 (3.4x to 13.1x fewer), and GRPO still scored higher on AIME-2025 (38.00 against 32.00)" | missing scope |
| 1.5 | Section 3.7, "What they cost"; Section 10, "Costs" | Dollar figures carry no model or task. Section 3.7 says DSPy's own pages disagree ("a few cents" up to "tens of dollars" against "hundreds of dollars"). Section 10 then states only the highest figure, as a general fact | Section 10: "a single optimizer run can cost hundreds of dollars [V: DSD]" | missing scope |
| 1.6 | Section 9, tutor prompt, FACTS (this box is pasted into a chat alone, so its scope doesn't travel) | The two paper figures drop the scope given in Section 3.7: no "aggregate over six benchmarks" for GEPA, and no "test set, exact match" or year for MIPRO | "MIPRO on ScoNe with Llama-3-8B: 69.1 to 79.4 (+10.3 points). GEPA beat MIPROv2 by 7.01 points (Qwen3 8B) and 6.55 (GPT-4.1 Mini)." | missing scope |

## Rubric 2: accuracy changes in percentage points

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 2.1 | Section 4, MIPROv2 "by 15%" row, and GEPA row | Two abstract quotes use "%" for accuracy gains without saying points or relative. The row also sets a 14.9% relative gain beside "as much as 13%", so the reader sees a number above the abstract's stated maximum, with no explanation (different comparator? points against relative?) | "+10.3 points, 14.9% relative; the abstract says 'as much as 13% accuracy'" and "'by 6% on average'". Needs source check | missing scope |

All other changes are given in points ("+10.3 points", "7.01 and 6.55 points", "a gain of 1.5 to 3.7 percentage points"). The relative figure 14.9% is labelled relative.

## Rubric 3: citations complete enough to find

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 3.1 | Section 9, "Best next resources"; Section 12, PYD | The DSPy link goes to the repository root, not the optimizer page (the path is only in Section 12). PYD is read from "main branch" with no version or commit, so the text read can't be pinned | "DSPy, "Optimizers" (in the repository's docs): https://github.com/stanfordnlp/dspy"; PYD: "github.com/pydantic/pydantic, main branch" | missing scope |

No citation looks wrong. The arXiv IDs, DOI and ACL Anthology addresses given are well formed.

## Rubric 4: same number everywhere; cross-references resolve

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 4.1 | Section 3.2 and Section 9 against Section 4 and Section 10 | The number of documented exceptions is three in some places and two in others. Section 9 also cites OSO for `max_tokens`, but the Checks section says "only Anthropic's page lists `max_tokens` as an exception" | Section 3.2: "handles each of these three cases on purpose"; Section 9: "name its three documented exceptions"; Section 4: "documented exceptions (refusal, `max_tokens`)"; Section 10: "Anthropic's current page lists two exceptions, a refusal and a `max_tokens` cut-off" | inconsistency |
| 4.2 | Appendix, `requirements-dspy.txt` against Section 7.4 and Checks | The listing, shown "exactly as tested", still says about 70 packages. The text says 60 and records "the package count (about 60, not 70)" as fixed | Listing: "DSPy pulls in about 70 packages"; Section 7.4: "about 60 packages (61 in a fresh Python 3.13 environment)" | inconsistency |
| 4.3 | Opening box ("What this part gives you") against Section 6 | A blanket "no key" claim, but Section 6 and Section 3.2 need keys and paid usage for the vendor SDKs and for DSPy optimizer runs | "Everything here is free and needs no model, account or API key." against "An API key" / "Free; API usage is paid" / "optimizer runs pay for model calls" | inconsistency |
| 4.4 | "How to read this part" | The claim fails on the part's own structure: Section 3.6 is reasoning models only, Section 3.7 is optimization only, and Sections 5, 6, 11 and 12 don't treat all three topics | "Each of the twelve sections below covers all three, so related ideas sit together." | inconsistency |

The in-part references to Sections 3.2, 3.3, 3.5, 3.6, 3.7, 7.4, 7.5, 7.6, 8 and 12 all resolve. Every [V: KEY] used in the text has a row in Section 12. The header's tag counts could not be checked without counting by script.

## Rubric 5: example prompts and code blocks

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 5.1 | Cheat sheet, "Settings" block | Python keyword-argument lines use the JSON literal `true`, which raises `NameError` in Python. `{...}` placeholders are left in. The OpenAI Responses line has `type`, `strict` and `schema` but no schema name; whether the API requires one is a needs-source-check item | `OpenAI     text={"format": {"type": "json_schema", "strict": true, "schema": {...}}}` | unusable example |
| 5.2 | Section 3.2 (end of the table notes), Section 7.5 | The text says the linter checks both columns' documented rules. The code checks only `additionalProperties`, `required` (OpenAI), the Anthropic unsupported keywords, `minItems` above 1, and two `$ref` cases. It does not check the Anthropic size limits in the table, and it flags nothing for OpenAI's `minLength` / `maxLength` ("Not in its supported list") | "`schema_lint.py` checks a schema against both columns' documented rules before you send it [T]" | inconsistency |

Traced and consistent with the printed output: `toy_optimizer.py` (1.0 and 0.417 on the 5-ticket pick, 0.733 and 0.75 on the 15-ticket pick, 33 candidates, 165 and 495 calls, plain prompt 0.167, the "order" explanation), Exercise 2 (45 candidates, 225 and 675 calls, 0.8 and 0.833), `tool_loop.py` (`blocks=5` and `blocks=10`, `tool_errors=1`), `validate_retry.py` (attempts 2, the "Second prompt sent" line, Exercise 3 with `max_attempts=1`), the 8 linter checks, the 17 mutations, and `paper_numbers.py` (10.3, 14.9, 7.01, 6.55, 3.4 to 13.1). Exercise 1's lint results and fix are correct.

## Rubric 6: evidence-class label for each technique

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 6.1 | Section 3.5, "What to do" | The "two habits" advice has no tag. The one citation, ASO, supports only the refusal warning, not that the habits "make the debate matter less". It should carry [U] or [I] | "Two habits make the debate matter less. First, let the model reason in free text and put only the final answer in a structured field, or ask for reasoning in a separate call" | missing scope |
| 6.2 | Section 6, "For prompt optimization" | The "about 50" threshold has no source or tag. It also reads against the line before it, which recommends BootstrapFewShot at "about 10 examples" | "With fewer than about 50 labelled examples, this series' advice is to improve the prompt by hand" | missing scope |
| 6.3 | Section 5, "Reading it" | An effectiveness claim for retry-with-error-text with no tag of its own; the cited [T] run uses a recorded stand-in [I], so it shows the loop's mechanics, not that a model repairs itself from the message | "the error text goes back to the model, so the model knows what to fix (guide Example 17.2)" | missing scope |

## Rubric 7: KEY rows for Part 03

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 7.1 | KEY row 11 against Section 9 | The numbers match (100% = 1.0, 41.7% = 0.417). The scope doesn't: row 11 says "5 validation tickets", "invented tickets" and [T][I]. Section 9's two sentences carry [T] only and name neither the 5 tickets nor the invented data. The full scope is in Section 3.7 | Section 9: "The toy's 100% became 41.7% on new tickets [T]." and "the toy's winner fell to 41.7% on new tickets [T]" | missing scope |
| 7.2 | KEY row 12 against Section 9 | Row 12's scope is "5.x-era models; checked October 12, 2026". The Section 9 answer has "5.x-era models" but no date; the date is in the Section 3.6 intro and the tutor prompt header, not in this sentence | "(5) A 400 error: the 5.x-era models reject any non-default temperature [V: ATK]" | missing scope |

## Rubric 8: wording that overreaches

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 8.1 | Section 10, "Guarantees have edges" | Two generalizations the part's own text doesn't support. "Silently" is documented only for llama.cpp [V: LCG]. "Local engines enforce less" cuts against Section 3.4, where a local engine (Guidance, 0.41) covers more than OpenAI's API (0.09). "Strongest ... on offer" is a superlative with no comparison source | "Strict structured output is the strongest format guarantee on offer ... Local engines enforce less, and silently [V: LCG, JSB]." | overclaim |
| 8.2 | Section 3.3, "The model never runs anything"; Section 9, self-check Q3 | An absolute with a citation only to client-defined function tools. If either vendor offers tools that run on its servers, "never" is false as written. Needs source check | "**The model never runs anything.** It asks." and "Your program, which is where every check and permission belongs [V: OFC]." | overclaim |
| 8.3 | Section 1, definition and analogy | Stated as a flat guarantee before the three exceptions in Section 3.2, which a skim-reader of the plain-words level will miss | "the vendor's software makes the model's output follow it" and "The form guarantees every box is filled in the right format." | overclaim |

## Rubric 9: traces of how the document was made

| # | Location | Problem | Evidence | Severity |
|---|---|---|---|---|
| 9.1 | Section 12, opening paragraph (and "Checks run on this part") | References to a lead session and researcher agents, and to the author's reproduction steps. "Checks run on this part" may count as the series' method; the Section 12 sentence about who opened which source is the clearest trace | "All opened October 12, 2026, by the lead session or one of two researcher agents." and "(forced tool use, the thinking retirement and JSONSchemaBench's tables by the lead session)" | process trace |
| 9.2 | Section 10, "Where this part disagrees with project docs" | Project-management history (an owner decision about when to edit other documents) inside a reader-facing part | "(flagged, not changed, per the owner's decision to leave the taxonomy and guide alone until the series is finished)" | process trace |
| 9.3 | "Run on your computer" | Written for the author or owner collecting results, not for a reader; there is no one for a reader to "send back" to | "Run them from the lab folder with its environment active, and send back the output; each [R] above then becomes [T] with the date." | process trace |

Findings by severity: error 0, overclaim 3, missing scope 13, inconsistency 5, unusable example 1, process trace 3 (25 in total).

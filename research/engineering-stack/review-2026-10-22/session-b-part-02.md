# Session B review: Part 02

Reviewed: `research/engineering-stack/docs/parts/engineering-stack-part-02-evals.md`, against the Session B brief and Appendix B (KEY) of the overview. Findings only.

Method note: I read the whole part, including the lab listings and data files in the appendix. I did not run anything. I checked the lab's printed outputs by hand against the listed code and data (all 60 tickets under both routers, the 8 semantic-entropy questions, the 20 judge pairs, the Wilson, McNemar, kappa, entropy, AUROC and pass@k arithmetic). Everything matched except the items below.

## Rubric 1: every number carries its model and task (and year) in the same sentence

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| 3.6 table, row "Position bias"; Section 4, row P9-13 | The 65.0% and 77.5% figures do not name the benchmark or task in their own row or sentence. KEY row 16 gives the scope as "Zheng et al. 2023, MT-bench", and only the first row of the table says MT-bench. | "GPT-4's verdict stayed the same after the two answers swapped places in 65.0% of cases, and favoured the first answer in 30.0%; with few-shot examples, 77.5% stayed the same"; Section 4: "Few-shot judging raised GPT-4's position consistency from 65.0% to 77.5% [V: ZHE]" | missing scope |
| 3.2 "Keep test items out of what the model sees"; Section 5, item 3 | GSM1k figure is given for "leading models" with no model named. KEY row 27 (the same figure, hosted in Part 12) scopes it "for some models", which is narrower. Needs source check on whether the drops were limited to some model families. | 3.2: "they found 'accuracy drops of up to 8%' for leading models"; Section 5: "leading models showed 'accuracy drops of up to 8%'" | missing scope |
| 3.5 "Related questions"; Section 4 row P9-02 and Section 9 tutor prompt FACTS; Section 5 item 6 | Restatements drop scope that the main text gives. (a) The clustered-error ratios name tasks but no model. (b) The AUROC pair 0.790 / 0.691 is stated without "averaged across 30 combinations of tasks and models" (Section 4) or with only "average" (tutor FACTS). (c) Section 5 item 6 says "one model" and "one prompt" where 3.8 names Qwen3-235B-A22B-Instruct-2507 and the Feynman prompt. | 3.5: "1.10 times the naive value on RACE-H, 1.88 on MGSM and 3.05 on DROP [V: MIL]"; Section 4: "Naive entropy averaged an AUROC of 0.691 against semantic entropy's 0.790"; FACTS: "average AUROC 0.790 against 0.691 for naive entropy"; Section 5: "A thousand temperature-0 completions of one prompt from one model gave 80 different texts on a standard serving stack" | missing scope |

## Rubric 2: accuracy changes in percentage points

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| 3.2 and Section 5 item 3 | The GSM1k accuracy change is written as "8%" with no "points". The part's own convention elsewhere is points ("38.1 points wide", "fell 42.9 points", "3.3 percentage points"), so a reader cannot tell whether 8% is absolute or relative. Same wording as KEY row 27. | "accuracy drops of up to 8%" (both places) | missing scope |

Other accuracy and recall changes in the part are in points and the subtraction is right ("differ by 3.3 percentage points", "technical recall rose 25 points").

## Rubric 3: citations complete enough to find

None found. Every key used in the text resolves to a Section 12 row with a URL, DOI, arXiv ID or full title. I did not try to verify any of them. (The `NPM` row gives a command, `npm view promptfoo`, not a URL; I judged that findable and did not flag it.)

## Rubric 4: same number everywhere; cross-references resolve

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| 3.2 "How many"; Section 5 "Reading it" and output; Section 9 self-check answer (1) | Three figures do not equal the difference of the endpoints printed for them elsewhere in the part (they come from unrounded values, but a reader will subtract the printed ones). 15 cases: width 38.1, endpoints 54.8% and 93.0% (difference 38.2). 960 cases: width 5.1, endpoints 77.4% and 82.4% (difference 5.0). Account recall: "fell 42.9 points" while the printed ends are 85.7% and 42.9% (difference 42.8). | 3.2: "38.1 points wide with 15 cases, ... and 5.1 with 960"; Section 9: "80% spans 54.8% to 93.0% on 15 cases and 77.4% to 82.4% on 960"; Section 5: "account: recall fell 42.9 points (85.7% to 42.9%)" | inconsistency |
| Opening italic note | It says "live model judges and local models are [R] too", but no passage in Sections 1 to 12 carries an [R] tag for a live judge or a local model. The judge section uses recorded verdicts, and the Ollama mentions in Section 6 are tagged [V: PFE]. | "No AI model runs on the test machine, so live model judges and local models are [R] too." | inconsistency |

Checked and consistent: 80.0%, 48/60, 68.2% to 88.2%; 76.7%, 46/60, 64.6% to 85.6%; mid-p 0.549 and exact 0.754; 0.016; 0.062; kappa 0.689; 65.0% and 77.5% (also 65% in the self-check); 0.790, 0.691, 0.687 to 0.698; the dates for the Evals shutdown (October 31 and November 30, 2026), gpt-4 (October 23, 2026), the promptfoo acquisition (March 9, 2026) and promptfoo 0.124.1. Every internal "Section n" and "step n" cross-reference resolves. The [U] count in the opening note (7) matches the body. I did not recount [V] and [T]; the [R] and [I] counts depend on how nested tags such as "[T on [I] data]" and "[T on Linux; R on Windows and macOS]" are counted.

## Rubric 5: example prompts and code blocks internally correct

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| Section 5, "Reading it" | Says all six regressed account tickets mention an app, a page or a screen. Only five do. Ticket t34 ("Password reset is not working for my work email.") contains none of those words; v2 caught it through "not working". The other five are t26, t46, t42 (app), t30 (page) and t38 (screen). | "The confusion matrix (Section 3.4) shows why: six account tickets mention an app, a page or a screen, and v2 now reaches its technical words first." | error |
| 3.4, paragraph after the confusion matrix | Wrong cause. Six account tickets landing in technical cannot raise technical's recall (the share of technical tickets labelled technical). Technical recall rose from 75.0% to 100.0% because v2's extra words caught four more technical tickets (t09, t53, t56, t58). The six account tickets lower technical's precision and account's recall. | "Six account tickets landed in technical. That raised technical's recall to 100% but cut its precision to 72.7%, and cut account's recall to 42.9% [T]." | error |

Hand-checked with no problem found: the 60-ticket outputs for v1 and v2 (48 and 46 right; 6 only-v1 and 4 only-v2; the confusion matrix, precision, recall, F1 and the 25-point technical rise); `--limit 15` (12 of 15; 54.8%); Exercise 2 (v3 at 52/60, 75.8% to 93.1%, mid-p 0.062); Exercises 1, 3 and 4; the 20 judge pairs (17/2/1, 16 agree, kappa 0.689, longer 11 of 15 and 10 of 17, and the `--always-first` result of 0.0% and 0.000); all eight semantic-entropy rows, both AUROC values (0.8125, 0.6562), the flagged set and q7; the mutation lists; the `run_lab.py` check numbering against steps 1 to 7; the planted near-copy (9 of 10 distinct words); the promptfoo counts (94, 26, 48/46, 12/14) and the "25 shown, 35 more" rows.

## Rubric 6: each technique carries an evidence-class label or tag

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| 3.1 step 7; 3.2 "Writing more cases" and "Keep test items out of what the model sees"; 3.5 last paragraph | Several techniques and design choices are stated as advice with no tag ([V], [T], [U] or [I]) and no class. They are the part's own reasoning, so each should say so or name what would settle it. The held-out set is repeated as decision rule 5 in the cheat sheet, also untagged. | 3.1: "Adding real failures to the test set is this series' advice: it keeps the test set close to what users actually send."; 3.2: "Have a person check generated cases before they count: a wrong label in the test set is a wrong grade on every run." and "Keep a held-out part of the test set that you never tune against, so a final check is still honest."; 3.5: "a false alarm costs a second look, while a missed regression reaches users." | missing scope |

All sourced techniques (Wilson, McNemar and mid-p, kappa, the swap rule, semantic entropy, probes, pass@k, paired inference, clustered errors) carry [V: KEY] and a class in Section 12.

## Rubric 7: KEY rows for this part

Only row 16 names Part 02. It is present with the same numbers (65.0% and 77.5%) in 3.6, Section 4, the Section 9 self-check and the tutor prompt FACTS. Its scope ("Zheng et al. 2023, MT-bench") is complete in the self-check and the FACTS but missing in two places, listed under rubric 1. Row 27 (GSM1k) names Part 12, but the same figure appears here with a wider scope ("leading models" against "for some models"); see rubric 1.

## Rubric 8: claims stronger than the source could support

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| 7.5 command table; Section 8 "Goal" and "Proof that the checks can fail" | "Proves each lab check can fail" is contradicted by the part's own mutation list. Check 2 ("The version in use (v1) passes its own gate") appears in no mutation's expected failures, so the listing never shows check 2 failing. More generally, 11 hand-picked mutations show those faults are caught, which is weaker than proving that each check can fail. | 7.5, the `python mutation_check.py` row: "Proves each lab check can fail"; Section 8: "**Proof that the checks can fail.**"; expected lists in the output: ['1.', '4.'], ['1.', '3.'], ['1.', '7.'], ['1.', '6.'], ['1.', '6.'], ['6.'], ['3.', '8.'], ['7.', '8.'], ['5.'], ['4.'], none | overclaim |
| Section 5, item 3 | The headline and the second clause are stronger than the paper's own hedge, which 3.2 quotes: "suggesting that some models may have partially memorized GSM8k". The part's correlation is r² = 0.36, which is moderate. | "A fresh test set exposing memorization. On GSM1k, leading models showed ... and the drops tracked how readily a model reproduced GSM8k examples [V: GSM]" | overclaim |
| Section 9, "A tutor prompt to practice with" | Flat statement that a measure does not exist anywhere in a long paper, with no tag. An absence claim like this needs a stated check (what was searched) or a [U]. Needs source check. | "No such measure exists in that paper; a usable tutor says it can't find it." | overclaim |

## Rubric 9: traces of how the document was made

| Location | Problem | Evidence | Severity |
|---|---|---|---|
| "Checks run on this part", bullets "Blind source check" and "Beginner test"; also "Run on your computer" | Reads as a change log of earlier drafts, with "now" statements about what was fixed, plus "the author" and "a fresh agent" as actors. This may be the series' lab-record method, which the brief exempts; I flag the wording that describes revisions (what the text or script used to say) rather than the result. The sentence "send back the output" is addressed to someone outside the document. | "now paraphrased"; "they are now \"checks\" throughout"; "it now reports them as failures"; "A fresh agent on the same model followed Sections 7 to 9 literally"; "the author reproduced each before fixing it"; "send back the output; each [R] above then becomes [T] with the date" | process trace |

No TODO, "as discussed", chat-session reference or leftover drafting note was found elsewhere in the part.

## Count

13 findings: 2 error, 3 overclaim, 5 missing scope, 2 inconsistency, 0 unusable example, 1 process trace.


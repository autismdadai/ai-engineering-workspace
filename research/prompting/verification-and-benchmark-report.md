# Verification and Benchmark Report

## *The Taxonomy of Prompt Engineering* (Third Edition) and *The Prompt Construction Guide* (Second Edition)

**October 2026** · Prepared under *The Edition Protocol*, version 3

## 1. Summary

Both documents were checked against the protocol's six acceptance tests. Independent checkers, in separate sessions and on models different from the one that drafted the documents, verified the sources, reviewed the text, and checked the worked examples.

- **Sources.** 46 citation claims and all 26 checkable figures in the manual's Canonical Figures table were verified against primary sources. No number was wrong. Twelve figures lacked part of their scope, and one "common misreading" entry labeled the paper's own wording as an error. All thirteen are fixed.
- **Reviews.** 172 review findings were reported (53 on the manual and 119 on the guide), including 20 errors and 35 example prompts that could not run as written. All were adjudicated and resolved.
- **Fidelity.** Two fresh summaries of the corrected manual, on two different models, restated 24 canonical figures with no distortions.
- **What remains open.** One date in one citation could not be confirmed. Some carried-over figures were not re-read. The Chapter 28 list and Section 7 of this report name them.

## 2. How the checks were run

| Step | What it does | Who ran it | Independence |
|---|---|---|---|
| Drafting (Session A) | Wrote both editions from the second editions, an answer key, and outside reviews | An Opus-class model | Author |
| Citation audit | Checked 46 claims about venues, quotes, and figures (items A1–A23 and B1–B23) | Sonnet-class models | Separate sessions; primary sources only |
| Canonical Figures audit | Checked every figure in Appendix A for value, scope, and misreading | A Sonnet-class model | Separate session; primary sources only |
| Independent review (Session B) | Read each document against the protocol's nine-point rubric | Three Sonnet-class reviewers: one for the manual, two for the halves of the guide | Separate sessions; no access to drafting history |
| Adjudication and fixes | Accepted or rejected each finding against the source, then fixed the text with exact-string patches | The author session, plus two fixer sessions given the adjudication rules | Fixers were not the reviewers |
| Fidelity test (Session C) | Summarized the final manual in about 500 words; scored against Appendix A | Haiku-class and Sonnet-class models | Fresh sessions with only the document attached |

All checking models are from one model family. The protocol prefers a different model for review and summaries, and these were different models from the drafting model, but a model from another developer could catch blind spots this family shares.

## 3. Source verification

### 3.1 Citation audit (46 items)

| Part | Items | Verified | Corrected | Not confirmed |
|---|---|---|---|---|
| A (new citations: venues, quotes, figures) | 23 | 23 | 0 | 0 |
| B (venues and quoted figures) | 23 | 22 | 0 | 1 |
| **Total** | **46** | **45** | **0** | **1** |

The one item not confirmed is B20, the publication date of Sheila Teo's CO-STAR article in *Towards Data Science* (29 December 2023). The quoted credit to GovTech Singapore's Data Science & AI team was confirmed word for word, but the date could not be read from the page. The manual does not depend on the exact day.

### 3.2 Canonical Figures audit (Appendix A)

Of 27 rows, 26 were checkable; the reliability mnemonic is the manual's own heuristic.

| Result | Rows | What changed |
|---|---|---|
| Verified as written | 13 | Nothing |
| Scope added | 12 | Chain-of-Symbol: the 60.8-point gain is over zero-shot CoT in one setting, and over few-shot CoT the gain is 17.5 points. Self-Consistency: the gains are GPT-3 code-davinci-002's. GEPA: the GRPO comparison is on Qwen3 8B only. Tree-of-Thoughts: "5–100×" is the paper's general range, and a compute-matched baseline scored 49%. Also: models and benchmarks for Least-to-Most, OPRO, CoT on reasoning models, CoT faithfulness, alignment faking, Contextual Retrieval, the Vectara dataset change, and the GSM1k paper version |
| Corrected | 1 | OPRO cost: the paper calls its word-based counts "tokens", so the misreading is now "treating them as exact tokenizer counts or as dollars" |

### 3.3 Further checks made during adjudication

Eleven claims flagged by the reviewers were checked against their primary sources:

- CaMeL's 77% versus 84% on AgentDojo;
- Nasr et al.'s 12 defenses bypassed at above 90% for most;
- Perez et al.'s finding that toxicity is a stronger attractor than length;
- LongLLMLingua's 21.4% on NaturalQuestions with GPT-3.5-Turbo;
- Turpin et al.'s "as much as 36%" with GPT-3.5 and Claude 1.0;
- Self-Refine's roughly 20-point average gain across seven tasks with GPT-3.5, ChatGPT, and GPT-4;
- EvoPrompt's 31 datasets with GPT-3.5 and Alpaca;
- Directional Stimulus Prompting's 41.4% with ChatGPT on 80 MultiWOZ dialogues;
- Graph-of-Thoughts' 62% sorting result with GPT-3.5;
- Snell et al.'s use of PaLM 2-S* on MATH;
- GEPA's Pareto frontier.

All were confirmed except the last. GEPA keeps every candidate that is best on at least one training instance. It does not trade score against instruction length, as an example in both documents had said; both examples are corrected.

## 4. Independent review

| Severity | Manual | Guide, Parts 1–4 | Guide, Parts 5–8 | Total |
|---|---|---|---|---|
| Error | 3 | 7 | 10 | 20 |
| Unusable example | 7 | 17 | 11 | 35 |
| Inconsistency | 13 | 13 | 18 | 44 |
| Overclaim | 14 | 14 | 11 | 39 |
| Missing scope | 10 | 4 | 8 | 22 |
| Process trace | 4 | 0 | 0 | 4 |
| Typo or formatting | 2 | 4 | 2 | 8 |
| **Total** | **53** | **59** | **60** | **172** |

**Disposition.** Every finding was resolved:

- Four guide findings concerned the separate Task-Type Index and were fixed there.
- One concerned a date example that the guide had right and the manual had wrong, so the manual was fixed.
- Blank-line formatting was fixed by script.
- All other findings were fixed in place.

**Examples of what was fixed:**

- **The quarantine example.** The manual's prompt-injection example claimed a security property its own schema broke. Free-text fields would have carried attacker text to the call that has tools; the schema now passes only validated dates, enums, and booleans.
- **The 45-day notice example.** It answered March 6 in the manual and March 5 in the guide. Both now say the start date is day 1 and answer March 5.
- **Voting rules.** One voting rule was silent on splits such as 3-1-1, and an extraction vote covered only some of its possible outcomes. Both now cover every split.
- **Evaluator loops.** These loops required both a per-rule table and a reply of exactly "ACCEPT". They now end with a "VERDICT:" line that code matches.
- **Persona lines.** A copy-editing example that began "Act as a copy editor", against its own build step, now states the behavior instead.

## 5. Worked examples

All 150 guide examples were read by a reviewer; 107 had at least one problem, and all were fixed. The most common problem was a missing input slot, such as a call told to rewrite "the email" with no {draft} placeholder. In the manual, 15 example prompts were corrected.

These answers were recomputed by script after the fixes:

| Example | Answer |
|---|---|
| Chain-of-Draft arithmetic | 24 × 18 × 3 = 1,296; 7 tickets at $12 less 15% = $71.40 |
| Chain-of-Draft dates | 2026-03-14 minus 21 days = 2026-02-21; a 45-day period starting 2026-01-20 as day 1 ends 2026-03-05 |
| Audit-and-close schedule | Audit 2026-04-06 to 04-10; close ends 2026-04-15 |
| Loan | $250,000 at 6.25%, monthly, 30 years: payment $1,539.29; total interest $304,145.48 (from the unrounded payment) |
| Business days | 18 business days from 2026-04-06, skipping weekends and the 2026-04-20 holiday, end 2026-04-30 |
| Grid route (guide 8.2) | Exactly one shortest path, 6 moves |
| Vote splits | Five votes can split 7 ways; the rules in guide Examples 10.1 and 24.3 now handle all of them |

## 6. Fidelity tests

The protocol scores any summary against the canonical figures:

- **CORRECT:** restated with its scope intact.
- **DISTORTED:** restated wrongly.
- **ABSENT:** not restated, and not counted.

| Summary | Edition summarized | Canonical items restated | Correct | Distorted | Notes |
|---|---|---|---|---|---|
| Gemini | Second | 5 | 0 | 5 | Scored earlier against the answer key |
| Google AI Overview | Second | 12 | 3 | 9 | Also invented a "98/100" quality score |
| ChatGPT | Second | 0 | 0 | 0 | Stayed at the level of evaluation |
| Grok | Second | 3 | 3 | 0 | |
| Sonnet-class, fresh session | Third, after review fixes | 14 | 14 | 0 | |
| Haiku-class, fresh session | Third, after review fixes | 9 | 7 | 2 | See below |
| Haiku-class, fresh session (re-run) | Third, final | 10 | 10 | 0 | Omitted the zero-shot baseline for Chain-of-Symbol, but stated nothing wrong |

**The first Haiku summary** distorted two items:

- **The GSM1k figure.** It quoted the paper's superseded first-version figure, 13%, which the manual mentioned in passing. The manual now gives only the current figure, and the old one appears only as a named misreading.
- **Few-shot CoT on strong models.** It extended this finding from Qwen2.5 to DeepSeek-R1. The manual's wording was already scoped, so this is a summarizer error.

The same summary also stated things the manual does not say, such as calling the manual "peer-reviewed". These are recorded, not counted against the document. Three small wording changes followed, and a fresh summary of the final text had no distortions.

**Acceptance test 2** requires two independent summaries with zero distortions. It is met by the Sonnet-class summary and the Haiku-class re-run. The Sonnet-class summary was made before the last three wording changes, none of which touched an item it restated.

## 7. Acceptance tests

| # | Test | Result |
|---|---|---|
| 1 | Every canonical statement is present in the document | Met: Appendix A holds all 27, with scope |
| 2 | Two independent summaries contain zero distorted items | Met (Section 6) |
| 3 | Every new citation resolves and supports its sentence, and a stated sample of carried-over citations does too | Met, with one exception: 45 of 46 audit items fully verified, and the B20 date not confirmed. The carried-over sample is the 26 Appendix A rows plus 11 further checks |
| 4 | Every example prompt runs as written and is internally correct | Met for the issues found: all 150 guide examples were reviewed and the problems fixed, and stated answers were recomputed. The examples are still not benchmarked against alternatives |
| 5 | Every number is identical wherever it appears | Met for the figures checked by script across both documents: Chain-of-Draft tokens and latency, Self-Consistency, Tree-of-Thoughts, OPRO, GEPA, and the faithfulness rates |
| 6 | The Still Unverified list is complete | Met for the items the review found: three items were added (Chain-of-Symbol transfer, the salience hypothesis, company and practitioner sources), and the list of carried-over figures not re-read was extended |

## 8. Limits of this verification

- **One model family.** Every checker is from one model family. No model from another developer reviewed the third edition. The outside-model scores above are for the second edition.
- **Fetch summaries.** Web pages were read through a tool that summarizes them. Checkers asked for verbatim quotes and cross-checked table cells by arithmetic, but a misread cell remains possible.
- **Guide usage data.** The usage shares in the guide's Part 7 were made internally consistent with the sources the guide names: units, products, and dates. They were not re-read against those reports.
- **Carried-over figures.** Figures carried over from earlier editions and not in Appendix A were not all re-read; manual Section 28.9 lists them.
- **Vendor documentation.** Vendor documentation was read in September 2026 and will change.
- **Unbenchmarked examples.** The example prompts illustrate technique shape. None has been benchmarked, so run your own evaluation before relying on one.

## 9. Files in the final set

| File | Content |
|---|---|
| `The_Taxonomy_of_Prompt_Engineering_Third_Edition` (.md, .pdf) | The seven-axis reference manual |
| `The_Prompt_Construction_Guide_Second_Edition` (.md, .pdf) | Build steps and 150 worked examples |
| `Task_Type_Index_Prompt_Engineering` (.md, .pdf) | Job-to-technique lookup aligned to the seven axes |
| `Edition_Protocol_v3` (.md, .pdf) | The verification-first revision protocol, with a section on running it within a budget |
| `Agent_Skills_and_Advanced_Prompt_Engineering_Reference` (.md, .pdf) | Version 1.2 of the skills reference |
| `New_Skills_Appendix` (.md, .pdf) | Changes to skills and skill files, with status |
| `Verification_and_Benchmark_Report` (.md, .pdf) | This report |
| `Prompt_Engineering_Combined_Volume.pdf` | All of the above in one volume |
| `skills/sophisticated-prompt-generator/` | Corrected SKILL.md, version 1.2.1, with its two reference files |

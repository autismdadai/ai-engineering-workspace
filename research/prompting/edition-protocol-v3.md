# The Edition Protocol

## A verification-first prompt set for revising AI-assisted technical references

**Version 3** · Replaces *Master Prompt — Rebuilding "The Taxonomy of Prompt Engineering."* This protocol produced the Third Edition of *The Taxonomy of Prompt Engineering*.

## 1. What changed from version 2, and why

Version 2 was a sound six-pass prompt with three defects. Each is fixed here.

| Defect in v2 | Why it matters | Fix in v3 |
|---|---|---|
| The review pass was self-review: the same model, in the same conversation, was told to "switch roles" and become a hostile reviewer. | Self-correction without external feedback is unreliable (Huang et al., ICLR 2024). Evaluators recognize and favor their own generations (Panickssery et al., NeurIPS 2024). A persona does not add accuracy (Zheng et al., Findings of EMNLP 2024). | Review runs in a separate session, with no memory of drafting, preferably on a different model. It gets a rubric and an answer key instead of a persona. |
| The known-error list was asserted as "confirmed against primary sources." | The receiving model cannot tell a verified correction from an unverified one. Trust moves to a place nobody checks. | Every correction carries its source. The author session re-verifies each one before applying it. The list is treated as leads. |
| The process ended when the passes ended. | A pass is a cost, not evidence. There was no way to tell whether a pass helped. | The process ends when acceptance tests pass (§6). |

## 2. Design rules and the evidence behind each

| Rule | Reason | Evidence class and source |
|---|---|---|
| Use no persona anywhere, including the reviewer. State the standard of work instead. | Across 162 personas and 2,410 multiple-choice MMLU questions in four open-source model families, adding a persona did not improve accuracy. | Peer-reviewed: Zheng et al., Findings of EMNLP 2024 (arXiv 2311.10054) |
| State rules positively and attach the reason. | Both major vendors advise saying what to do rather than only what not to do. | Vendor documentation: Anthropic and OpenAI prompting guides |
| Verify against primary sources. Never verify against the previous draft or against other AI reviews. | Text passed repeatedly through language models drifts toward attractors. | Peer-reviewed: Perez et al., arXiv 2407.04503 (ICLR 2025) |
| Review in a separate session, ideally with a different model. | Unaided self-correction can degrade answers, and model judges favor their own outputs. | Peer-reviewed: Huang et al., arXiv 2310.01798; Panickssery et al., arXiv 2404.13076 |
| Cross-check models in parallel, not in series. | In a relay, later models inherit earlier wording, so agreement is manufactured rather than independent. Assistants also drift toward the user's stated view. | Peer-reviewed: Sharma et al., arXiv 2310.13548; relay effect per Perez et al. |
| Preserve verified text. Every edit states its reason. | New text is new claim surface. | Design rule |
| Stop on tests, not on the number of passes. | Only a test shows whether a pass helped. | Design rule |

## 3. What to attach

1. **BASE:** the current edition. Markdown is preferred over PDF, because PDF extraction scrambles tables and code blocks.
2. **KEY:** the answer key. Each entry gives a canonical statement, its known distortions, and its primary source.
3. **LEADS:** outside reviews and fact-checks. They are leads, not authorities, and some will be wrong.

## 4. Session A: the author

Paste the following into a fresh conversation with BASE, KEY, and LEADS attached.

```
Produce the next edition of the attached reference manual (BASE). Keep its
structure, voice, and core arguments unless a change is justified below.
Readers: a builder who will copy a technique today, and a reviewer who will
check every citation. Write so the builder can act and the reviewer finds
nothing to object to.

Work in three passes. Show only what each pass asks for. If your output stops
mid-pass, resume in the next reply at the exact sentence where it stopped. Do
not repeat earlier passes or sections.

PASS 1 - CLAIM INVENTORY
List every quantitative or attributional claim in BASE, one line each:
claim | source cited | section.

PASS 2 - VERIFICATION
For each claim, and for every item in KEY, mark it verified, corrected (give
the fix), or unverifiable. Give the primary source: paper plus table or
section, or official documentation URL plus date read. KEY items are leads
with sources attached. Re-check each one before applying it. Where a LEAD is
itself wrong, say so and give the source.

PASS 3 - REVISION
Write the full revised manual. Rules, each with its reason:
1. Put the scope next to the number: the model and the benchmark or task in
   the same sentence, and the year in that sentence or its citation. A number
   separated from its scope reads as a universal law.
2. Write accuracy changes in percentage points. 31.8% to 92.6% is +60.8
   percentage points; mixing points and percent misstates effect size.
3. Cite primary sources only: the paper, official documentation, or the
   standards body. If only secondary support exists, write "reported by X;
   primary source not located," or drop the claim.
4. Label each technique's evidence class: peer-reviewed, preprint, vendor
   documentation, technical report, or practitioner mnemonic.
5. If a claim cannot be verified, write "unverified as of [date]" and list it
   in the Still Unverified chapter.
6. Readers see only the finished work. Leave out any mention of drafts,
   prompts, search budgets, or source-name tags.
7. Describe mechanisms at the confidence the interpretability papers state.
   Never claim a prompt targets specific neurons or attention heads.
8. Call heuristics heuristics. Design mnemonics are not measured equations.
9. Keep verified text. Change it only to fix a verified problem, and record
   each change and its source in the changelog.
10. Keep a Canonical Figures appendix. For each of the most-quoted results,
   give the exact scoped statement and the common misreading it replaces.
Every example prompt must be runnable as written, with {placeholders} only
for the user's own data. Do the arithmetic and check each expected answer.
Each example must follow its technique's own evidence (for example,
Chain-of-Draft examples include few-shot drafts).
Output: the manual, a changelog, and a Still Unverified list.
```

## 5. Session B: independent review

Open a new session, preferably on a different model. Attach only the revised draft, KEY, and the rubric below. Do not attach Session A's transcript.

```
Review the attached document against the rubric below. For each finding give:
location | problem | evidence (primary source) | severity (error, overclaim,
missing scope, inconsistency, unusable example, process trace). Report
findings only; do not rewrite the document. If a rubric line produces no
findings, write "none found" for it.

Rubric:
1. Every number carries its model and task in the same sentence, and its
   year in that sentence or its citation.
2. Accuracy changes are in percentage points.
3. Each citation exists and supports the sentence that cites it.
4. The same number is identical everywhere it appears; cross-references
   resolve.
5. Each example prompt is runnable and internally correct.
6. Each technique carries an evidence-class label.
7. Every KEY statement is preserved; no KEY distortion appears.
8. No claim is stronger than its source supports.
9. No trace of how the document was made remains.
```

**Adjudication (back in Session A).** For each finding, accept it and fix the draft, citing the source, or reject it and cite the source showing the draft is right. A finding is never accepted or rejected on the reviewer's authority alone. Finish with a consistency sweep: identical numbers everywhere, cross-references resolved, and every cited work in Works Cited.

## 6. Session C: fidelity test and acceptance

Open a new session with a fresh model. Attach only the final document.

```
Summarize this document's main findings for a technical reader in about 500
words, including the key numbers.
```

Score the summary against KEY. Mark each item CORRECT (restated with its scope intact), DISTORTED (restated wrongly), or ABSENT (not restated). A DISTORTED item means the document's wording let a number travel without its scope. Fix the sentence at the source, add it to Canonical Figures if it is not already there, and re-run the test in a new session. Run at least two independent summaries, and three or more models if they are available.

**The edition is final when all six tests pass:**

1. Every KEY statement is present in the document.
2. Two independent summaries contain zero DISTORTED items.
3. Every new citation resolves and supports its sentence. A stated sample of carried-over citations does too.
4. Every example prompt runs as written and is internally correct.
5. Every number is identical wherever it appears.
6. The Still Unverified list is complete.

## 7. Scoring any model's review against the KEY

The same KEY scores any outside model's summary or review of the document. Count CORRECT, DISTORTED, and ABSENT items, and note any fabricated meta-claim, such as an overall "accuracy score" the document never gives. The distortion count measures how much a model degrades a correct document while restating it. Because the KEY's corrections are all traceable to primary sources, the measure is objective.

## 8. Companion prompt: the construction guide

Use after the manual is final, in Session A.

```
Write (or revise) the companion construction guide. For each core technique
and each orchestration pattern (prompt chaining, routing, parallelization,
orchestrator-workers, evaluator-optimizer, multi-agent debate, automated
optimization loops, independent parallel review), give: a one-paragraph
"what it does and when to reach for it"; numbered build steps; what it
combines with and what it conflicts with; and five worked examples, each with
a scenario, the complete prompt or call flow, the build steps it
demonstrates, and a line saying what to check in the output. An example
adapted from the manual may extend it but must not contradict it: the same
numbers, the same expected answers, and the same check. Add an index by task
type. Base the technique-to-task table on published usage studies and give
each share with its scope. Apply the same rules as the manual.
```

## 9. Running the protocol on a budget

*Added October 2026, after the Third Edition's final checks.* One earlier attempt to run these checks stopped partway when many parallel checkers used up a usage cap. These practices kept the final run within bounds:

1. **Cap every checker.** Give each checking agent a limit on web lookups (30 to 50 was enough for 11 to 27 items). If a page can't be reached after two tries, the item is marked unverifiable and the checker moves on; it never repeats a failing call.
2. **Split long documents.** Give each reviewer one part of a long document, about 15,000 words or less, plus the shared reference it must match.
3. **Save every report as it arrives.** A report that exists only inside a stopped agent is lost. Ask an interrupted agent to report what it has, without further checking, before anything else.
4. **Review with a different model.** A different, cheaper model satisfies the different-model rule and costs less. Keep reviewing and fixing separate: reviewers report, and the author session adjudicates each finding.
5. **Fix with exact-string patches.** Apply many edits per script. Each edit applies only if its target text occurs exactly once, and failures are listed for a second pass. Every change stays traceable, and nothing is edited by accident.
6. **Re-test after fixing.** When a summary shows a distortion that the document's wording made possible, fix the wording and run a fresh summary of the corrected text. Count only distortions the document's wording made possible. Facts a summarizer invented are recorded, but they are not counted against the document.

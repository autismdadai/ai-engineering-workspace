# Session B brief: independent review of one part

This review follows the Edition Protocol v3, Section 5 (`research/prompting/edition-protocol-v3.md`). You did not write the part, and you see none of the author's notes, so you can judge it the way a reader would.

## What to read

1. The part named in your task, in full.
2. The overview's Appendix B, `research/engineering-stack/docs/engineering-stack-overview.md`, lines 122 to 158. It is the KEY: the series' key figures with their scope. Check only the rows whose "Where" column names your part.

Read nothing else and do not search the web. A separate script checks that each citation exists, so your job is what the text itself says.

## Rubric

1. Every number carries its model and task in the same sentence, and its year in that sentence or its citation.
2. Accuracy changes are in percentage points.
3. Each citation is complete enough to find (an arXiv ID, DOI, URL or full title). Flag citations that look wrong or incomplete; don't try to verify them.
4. The same number is identical everywhere it appears in the part; cross-references inside the part resolve.
5. Each example prompt and code block is internally correct (no contradiction between its text and its expected output).
6. Each technique carries an evidence-class label or tag.
7. Each KEY row for this part is present in the part with the same number and scope.
8. No claim is stronger than its cited source could support. You can't open sources, so flag only wording that overreaches on its face: "always", "proves", "guarantees", a vendor's claim stated as fact, a single study stated as a general law.
9. No trace of how the document was made remains. The tags [V], [T], [R], [U], [I], dated "read on" notes and the lab records are part of the series' method, not traces. Flag leftover drafting notes, TODOs, references to chat sessions or agents' turns, "as discussed", and similar.

## How to report

Report findings only; do not rewrite the part. Each finding is one table row: location (section and a short quote) | problem | evidence (quote the part's own text, or say "needs source check") | severity: error, overclaim, missing scope, inconsistency, unusable example, or process trace. If a rubric line produces nothing, write "none found" for it. Prefer fewer, solid findings to many weak ones.

Save as you go, because an interrupted review is lost otherwise: write the file's heading first, then append each rubric line's findings as soon as you have them. End the file with a line counting findings by severity.

# Appendix L review: status, October 22, 2026

The separate-session review of the Engineering Stack (overview, Appendix L), run under the Edition Protocol v3, Sections 5, 6 and 9. Reviewers report; this session adjudicated each finding against the part's own text or the lab's code, never on a reviewer's word alone.

## What ran

| Step | Result |
|---|---|
| Session C, fidelity test | Three fresh summaries of the overview, scored against Appendix B's 30 rows. Sonnet: 18 correct, 1 distorted, 11 absent. Haiku: 11 correct, 1 distorted, 18 absent. Sonnet re-test after the fix: 23 correct, 0 distorted, 7 absent [T] |
| Cross-part consistency (`consistency_check.py`) | Every Appendix B number appears in the part it cites. All 113 arXiv IDs cited across the series resolve; the 9 surname mismatches flagged were the script reading title words, plus one ("Liu" before NoLiMa) where two citations share a line. Tools with two versions were each explained by context, except Ollama (fixed) [T] |
| Session B, part reviews | Parts 01, 02 and 03 reviewed (Sonnet, no web lookups; citations were checked by the script instead). Parts 04 to 13 not yet reviewed |

**Acceptance test 2 now passes:** two independent summaries (Haiku, and the Sonnet re-test) with zero distortions the document's wording made possible. The Haiku summary's one distortion ("loses 2.79% perplexity" for "+2.79% perplexity") was the summarizer's own wording, so it is recorded but not counted (protocol Section 9, rule 6).

## Fixes applied

| Where | Fix | Settled by |
|---|---|---|
| Overview, Appendix B row 24 | The decode ceiling (8.5, worked out) and the qwen3:1.7b measurement (8.4 and 8.0) now read as two separate figures; the old wording let a summary say the measurement "matched" the ceiling | Session C (Sonnet) |
| Part 11 | Says the code reading is of Ollama v0.40.5 while the test PC ran v0.40.6, as Part 04 says | Consistency check |
| Part 01 | 6 findings: two out-of-date "[R: no Windows test machine]" reasons; the refusal message's file name; the hash-and-backslash description; "everything free" given Docker's paid tier; "strongest" uv; Ubuntu generalized to Debian | Session B |
| Part 02 | 2 errors: the six regressed account tickets (five mention an app, page or screen; t34 doesn't), and the cause of technical recall reaching 100% (v2 caught t09, t53, t56 and t58), both confirmed by running the lab's router [T]. Also MT-bench named in two restatements; GSM1k scoped to "some models" with the paper's own hedge; "proves each check can fail" narrowed to "catch planted faults" | Session B |
| Part 03 | 8 findings: three documented exceptions everywhere (not two); the DSPy package count (about 60, in the text, the listing and `labs/part-03/requirements-dspy.txt`; lab re-run 7 of 7); "no key" limited to the labs; the twelve-sections claim; Python `True` in the cheat sheet; what `schema_lint.py` actually checks; the stale "owner's decision" note; "local engines enforce less, and silently" | Session B |

## Rejected

Process-trace findings about the "Checks run on this part" sections, source provenance notes and "send back the output": these record the series' method (who checked what, and how a reader test becomes [T]), which the brief exempts.

## Deferred (accepted in principle, not yet fixed)

Part 01: 11 (missing scope on tags, the expected `Python 3.13.16` output, the freshness-ledger citation, the PyPI template URL, [T] given to macOS cells, the tutor prompt's Linux venv step, Windows Extract All's folder, two vendor-claim overclaims). Part 02: 5 (restated scopes, rounding of interval widths, the opening [R] note, untagged advice, the tutor-prompt absence claim). Part 03: 15 (13 missing-scope items and two overclaims needing a source check: "the model never runs anything" and Section 1's flat guarantee). Each is in its part's review file with location and quote.

## Still to run

1. Session B for Parts 04 to 13, with the same brief (`session-b-brief.md`), after the weekly usage reset on October 26, 2026. Measured cost on October 22: about 200,000 to 235,000 tokens per reviewer, roughly 1 point of the Pro weekly limit each [T, from the usage meter before and after].
2. Adjudicate their findings, then the deferred items above.
3. The open reader tests in Appendix H.

# The AI Engineering Stack: what's here

Gathered October 20, 2026 from the owner's Downloads folder, and completed October 21 from `engineering-stack-bundle-2026-10-21.zip`. All 33 bundle files matched the SHA-256 values in its MANIFEST. The originals stay in Downloads, with copies in the workspace's local-only `archive/zips/` (not uploaded to GitHub).

## Where the series stands

Phases 0 to 5 are done (progress file, "In progress: Nothing"). Still open:

1. **The separate-session review** (overview, Appendix L), started October 22, 2026; status in `review-2026-10-22/REVIEW_STATUS.md`:
   - Session B: Parts 01 to 03 reviewed and adjudicated; Parts 04 to 13 still to run, after the October 26 usage reset.
   - Session C: done. Two fresh summaries with zero distortions, so acceptance test 2 passes.
   - The cross-part consistency pass: done (`review-2026-10-22/consistency_check.py`).
2. ~~A held change for the owner~~ Done October 21, 2026: the prompt generator's Procedure step 3 now says "low temperature for single-answer tasks, where the model accepts it" (both copies).
3. **The freshness ledger needs a full re-check** (`pypi_fresh.py`).
4. **Open reader tests:**
   - Part 13's R1 to R4;
   - Part 04 R4 at full size (now possible with `--timeout`);
   - Part 01 R4 and Part 02 R4 (Node.js);
   - Part 07 R4 (Claude Code);
   - Part 08 R4 (Docker);
   - the typed PowerShell steps and every macOS step.
5. ~~From the October 15 source research~~ Done October 21 and 22, 2026: all of its Sections 3.2 to 3.4 (nine corrections, four scope fixes, five web sources) are applied to the taxonomy and logged in its Section 27.7.

## Folder layout

| Folder | Contents |
|---|---|
| `docs/parts/` | the final texts of all 13 parts (October 20 versions; Parts 01 and 02 from October 12, unchanged since) |
| `docs/reviews/` | the Phase 4 review records of all 13 parts |
| `docs/` | overview, progress, claim ledger, freshness ledger, glossary (current), plan, series prompt, file map. The three handoffs stay in the owner's private workspace |
| `docs/records/` | the Windows-run records of October 12, 19 and 20. In this public copy the user folder is written as `%USERPROFILE%` |
| `docs/sources/` | the Gemini report the claim ledger audits |
| `archive/superseded/engineering-stack/` (workspace root, local only) | older local copies replaced by the bundle: Part 03 of October 13, the Part 05 and 06 drafts, and the October 15 glossary and freshness ledger |
| `labs/part-01` … `labs/part-13` | every lab, unpacked; Part 04 has the October 20 `placement_test.py` |
| `research/part-01` … `research/part-13`, `research/part-11-start` | every research zip, unpacked |
| `windows-runs/` | the PowerShell reader-test scripts and logs from October 19 and 20. In this public copy the user folder is written as `%USERPROFILE%`, and package maintainers' emails as `[email removed]` |
| `../prompting/` | (moved) the October 20 taxonomy 3e, guide 2e and New Skills Appendix; the checklist is in `skills/sophisticated-prompt-generator/references/` |
| `archive/zips/` (workspace root, local only) | the zips as downloaded, and `bundle-2026-10-21/` unpacked with its MANIFEST |

Not copied: `Downloads/Qwen3-4B-Q4_K_M.gguf` (2.5 GB, the Part 11 reader-test model).

## Left out of this public copy

These files are in the owner's private workspace but not here:

- **The three handoffs in `docs/`:** working notes for new chats, with personal context.
- **`research/part-11/research/serving/reports_vllm.json`:** the pip install report (pip 24.0, `install --report`, October 16, 2026) behind claim S078 in `claims.md`. It held 189 distinct email-like strings, most of them package maintainers' addresses. Running pip's `install --report` for `vllm==0.31.0` rebuilds it.
- **`loose/part-12-phase4/`:** Part 12's raw Phase 4 files.
- **`labs/part-04/placement_test.py.before-2026-10-20`:** the file `placement_test.py` replaced.
- **`research/part-12/windows/part11-reader-tests.log`:** a byte-for-byte copy of `windows-runs/part11-reader-tests.log`.
- **`review-2026-10-22/codex-request-part-04.md`:** a review request written for Codex, tied to the private pages.

## Old `claude/` paths in the texts

The series was written in a claude.ai Project, and its texts cite files by their names there, as `claude/<name>`: 311 mentions of 38 names. The texts are kept as they were checked, so the names are mapped here instead. Every named file is in this folder (`research/engineering-stack/`):

| Name in the texts | Where the file is now |
|---|---|
| `claude/engineering-stack-part-NN-<topic>.md` (the 13 parts) | `docs/parts/` |
| `claude/engineering-stack-part-NN-review.md` (the 13 reviews) | `docs/reviews/` |
| `claude/engineering-stack-windows-run-2026-10-12.md`, `-10-19.md` and `-10-20.md` | `docs/records/` |
| `claude/engineering-stack-` followed by `claim-ledger`, `freshness-ledger`, `glossary`, `overview`, `plan`, `progress` or `prompt`, then `.md` | `docs/` |

`claude/engineering-stack-part-NN-` and `part-NN-topic.md` are naming patterns in the texts, not files.

The texts here and in `research/prompting/` also cite 25 other `claude/` names (188 mentions):

| Name in the texts | Where the file is now |
|---|---|
| The prompting papers and methods: `claude/` followed by `taxonomy-of-prompt-engineering-3e`, `prompt-construction-guide-2e`, `new-skills-appendix`, `agent-skills-reference-v1-2`, `edition-protocol-v3`, `skills-booklet`, `trigger-tests-2026-10-08`, `research-verification-toolkit`, `multi-lens-review-method`, `verification-and-benchmark-report`, `portable-research-prompt`, `task-type-index`, `prompt-suite-method` or `plugin-review-2026-10-12`, then `.md` | `research/prompting/` (from the repository root) |
| `claude/project-file-map.md` | `docs/` in this folder |
| `claude/fabel-prompt-audit.md`, `claude/github-tutor-prompt.md`, `claude/skill-install-guide.md`, `claude/visual-prompts-seven-axis.md` and the handoffs (`claude/handoff-…`) | Not in this repository: they stay in the claude.ai Project or the owner's private workspace |

The other four names (`claude/`, `claude/...md`, `claude/handoff-*.md` and `claude/portable-research-prompt.md.*`) are patterns, not files.

## Per part

| Part | Text | Words | Review | Lab | Research |
|---|---|---|---|---|---|
| 01 setup | yes | 13,381 | yes | yes | yes |
| 02 evals | yes | 20,301 | yes | yes | yes |
| 03 prompts as interfaces | yes | 14,578 | yes | yes | yes |
| 04 context | yes | 20,311 | yes | yes | yes |
| 05 retrieval | yes | 19,264 | yes | yes | yes |
| 06 graphs and memory | yes | 14,708 | yes | yes | yes |
| 07 tools and protocols | yes | 16,448 | yes | yes | yes |
| 08 agents | yes | 16,980 | yes | yes | yes |
| 09 workflows and multi-agent | yes | 14,316 | yes | yes | yes |
| 10 security | yes | 19,024 | yes | yes | yes |
| 11 running models | yes | 15,770 | yes | yes | yes |
| 12 adapting models | yes | 14,624 | yes | yes | yes |
| 13 shipping | yes | 14,822 | yes | yes | yes |

Nothing is missing for the separate-session review. Total part text: about 215,000 words.

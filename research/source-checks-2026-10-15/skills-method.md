# Skills-method check: validators and build method vs official sources

Run date: 2026-10-15. Lookups used: 20 of 20 (cap reached). Nothing in the sources folder was run or edited. No packages installed. All "inference" labels below mean "reasoned from sourced facts, not executed".

## Short answer

1. Neither of the kit's validators matches the official ones. validate_skill.sh passes skills it never really read (it sees ">" as the description). skill_audit.py fails valid skills (its line parser rejects YAML block scalars). Both skip rules that the official validators enforce: unknown top-level fields, the 500-character compatibility limit, and (for Anthropic's validator) angle brackets in the description.
2. example-skill's unindented second description line is NOT valid YAML. The YAML 1.2.2 spec requires continuation lines of a block-mapping value to be indented at least one space. Both official validators parse real YAML, so they would reject it. It also fails the official folder-name rule.
3. Most of the kit's build method is supported by official sources (evals first, baseline, near-miss trigger tests, 60/40 split, one-level references, script rules). The weak spots: inconsistent trigger-test counts across the three kit documents, "double-blind matrices" (official: optional blind comparison), the `disable-model-invocation` lock (Claude Code only; the official portable validators reject it), and nothing about testing on Haiku, Sonnet and Opus.
4. A fact the kit does not know: claude.ai custom-skill upload caps the description at 200 characters (Anthropic help center). The kit's own three real skills have descriptions of 610, 411 and 253 characters.

## Part 1. Validators

### 1.1 Which "official validator"? There are two, and they disagree

| | skills-ref (agentskills repo) | quick_validate.py (anthropics/skills, skill-creator) |
|---|---|---|
| YAML parser | strictyaml (`strictyaml.load`), errors become ParseError "Invalid YAML in frontmatter" | PyYAML `yaml.safe_load`, frontmatter cut with regex `^---\n(.*?)\n---` |
| Unknown top-level keys | rejected: "Unexpected fields in frontmatter" | rejected: "Unexpected key(s) in SKILL.md frontmatter" |
| Allowed keys | name, description, license, allowed-tools, metadata, compatibility | same six |
| Folder name must equal name | yes (NFKC-normalised both sides) | no, never checked |
| Name characters | lowercase and `isalnum()` or hyphen (Unicode letters allowed) | ASCII `^[a-z0-9-]+$` |
| Angle brackets in description | not checked | rejected |
| compatibility | string, max 500 | string, max 500 |

Status of skills-ref, from its own README: "This library is intended for demonstration purposes only. It is not meant to be used in production." The spec page still tells authors to run `skills-ref validate`.

Source URLs:
- https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/src/skills_ref/validator.py
- https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/src/skills_ref/parser.py
- https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/README.md
- https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/scripts/quick_validate.py
- https://agentskills.io/specification

Line numbers for validator.py come from the fetch tool's own count and were not re-counted by me, so treat them as approximate: constants L10-12 (64 / 1024 / 500), ALLOWED_FIELDS L15, `_validate_name` L25, NFKC L37, name length L39, lowercase L45, leading/trailing hyphen L48, "--" L51, isalnum L54, directory match L62, `_validate_description` L70, description length L78, `_validate_compatibility` L87, `_validate_metadata_fields` L104, `validate_metadata` L118, `validate` L150. For parser.py the fetch tool would not quote the file, so only function behaviour is known (`parse_frontmatter`, `read_properties`, `find_skill_md`), no line numbers.

### 1.2 Rules the kit's scripts miss, get wrong, or add

"Miss" = official validators enforce it, the kit's script does not.

| # | Rule | Official | validate_skill.sh | skill_audit.py | Verdict |
|---|---|---|---|---|---|
| V1 | Read the frontmatter as YAML (folded `>`, literal `|`, quotes) | real YAML parsers | reads one line only (awk L46-52); description `>` becomes length 1 (L84) | line parser (L34-41); a continuation line without a colon returns an error (L37-38), then fields are reset to {} (L58-59), so "name is missing" and "description is missing" are false follow-on errors | WRONG in both, in opposite directions: false PASS and false FAIL |
| V2 | Unknown top-level fields rejected | both official validators | not checked | not checked; nested `metadata:` keys are flattened to top level (L39-40), so it could not detect them anyway | MISSED |
| V3 | compatibility is a string, max 500 | both | not checked | not checked | MISSED |
| V4 | Description must not contain angle brackets / XML tags | quick_validate checks `<` `>`; Anthropic best-practices and skills-guide: "no XML tags" in name and description | not checked | not checked | MISSED (kit's own Omnibus step 6 says "without XML tokens" but nothing enforces it) |
| V5 | Name must not contain reserved words "anthropic" or "claude" | documented in Anthropic best-practices and skills-guide; neither official script was seen to check it | not checked | not checked | MISSED (documentation-only rule) |
| V6 | Folder name equals name | skills-ref and spec: yes; quick_validate: no | checked (L55), raw compare | checked (L73), raw compare | OK. Missing only the NFKC normalisation. |
| V7 | Name charset | skills-ref allows Unicode letters; quick_validate ASCII only | ASCII regex (L57) | ASCII regex (L20) | OK, stricter than skills-ref, matches Anthropic's script |
| V8 | Description non-empty and at most 1024 | spec: 1-1024 | checked, but on the wrong text (see V1) | checked, but broken by V1 | WRONG in effect |
| V9 | Description at most 200 characters for claude.ai upload | Anthropic help center: "200 characters maximum" | not checked | not checked | MISSED (host rule, not in the spec) |
| V10 | Delimiter handling | skills-ref: `startswith("---")` then `split("---", 2)`, so any `---` text cuts the frontmatter short (reading of the fetch result) | whole-line `---` only | whole-line `---` only | Kit is more careful here. But a skill can pass the kit and still fail skills-ref. |
| V11 | File name | skills-ref accepts SKILL.md, then skill.md; quick_validate requires SKILL.md | SKILL.md only | SKILL.md only | OK (note: the Anthropic help article itself spells the file "skill.md") |
| V12 | 500-line body | recommendation only ("Keep your main SKILL.md under 500 lines"); neither official script enforces it. Spec also recommends under 5,000 tokens for the body. | warning only (L75-78) | warning only (L81-83) | Kit treats it correctly. 5,000-token advice not checked by either. |
| V13 | Absolute-path / backslash warnings (kit addition) | not in any official validator | regex needs whitespace or start before the drive letter (L80), few false hits | `[A-Za-z]:[\\/]+` (L87) matches the "s:/" inside any "https://" URL; any backslash at all warns (L85) | Added by the kit. skill_audit.py version gives false warnings (reading the regex; not run). |
| V14 | CRLF files (this machine is Windows) | PyYAML/strictyaml handle them | `$0=="---"` and `head -n 1` compare against "---" without removing \r (L35, L40), so a CRLF file would likely fail | uses `splitlines()` and `strip()`, fine | INFERENCE, not run |

Local measurements (a small read-only script I wrote in the scratchpad; it reads each SKILL.md as data and does not run anything from the sources folder; 2026-10-15):

| Skill | Description length (folded lines joined) | Angle brackets | SKILL.md lines |
|---|---|---|---|
| sophisticated-prompt-generator | 610 | none | 129 |
| cross-model-accuracy-verifier | 411 | none | 48 |
| server-log-triager | 253 | none | 23 |
| example-skill | 72 on its first line, plus 1 unindented continuation line | none | 38 |

All are inside the spec's 1024 limit. The first three exceed the claude.ai upload limit of 200.

What the official validators would say (inference, not run):
- sophisticated-prompt-generator and cross-model-accuracy-verifier: valid for quick_validate (PyYAML reads `>` folded scalars). For skills-ref (strictyaml): NOT CONFIRMED. The strictyaml docs page I read did not cover the folded `>` indicator. The agentskills.io page itself uses `description: >` in its "Optimizing descriptions" example, which points to it being acceptable, but that is not proof about the validator. Run `skills-ref validate` once on these two to settle it.
- server-log-triager: valid. Unquoted `version: 1.0.0` is fine since skills-ref converts metadata values to strings.
- example-skill: invalid in both (see 1.3), and invalid in skills-ref for the folder name too ("Directory name must match skill name": folder `example-skill`, name `invoice-reconciliation`).

### 1.3 example-skill: is the unindented second description line valid YAML?

Answer: no.

- The frontmatter is a block mapping at indentation 0. `description:` has a plain scalar on line 3 of the file, and the next line ("Use when comparing invoices, ...") starts at column 0.
- YAML 1.2.2 section 8.2.3 (Block Nodes): "Flow nodes must be indented by at least one more space than the parent block collection." A plain scalar is a flow node.
- The grammar says the same: production [197] `s-l+flow-in-block(n)` = `s-separate(n+1, FLOW-OUT) ns-flow-node(n+1, FLOW-OUT)`; continuation lines come from [134] `s-ns-plain-next-line(n,c)` = `s-flow-folded(n) ns-plain-char(c) nb-ns-plain-in-line(c)`; [74] `s-flow-folded(n)` ends in [69] `s-flow-line-prefix(n)` = `s-indent(n) s-separate-in-line?`. With the mapping at n = 0, continuation lines need an indent of at least 1 space. Column 0 is not allowed. (The step from "mapping at n = 0" to "continuation needs n+1" is my reading of the productions.)
- Result in a real parser: the column-0 line is read as a new mapping key, finds no colon, and errors. skills-ref would raise ParseError "Invalid YAML in frontmatter"; quick_validate.py would print "Invalid YAML in frontmatter: ...". Not run.
- Fix: indent line 3 by two spaces, or use `description: >` with indented lines. Then rename the folder to `invoice-reconciliation` (or the name to `example-skill`).
- Note: skill_audit.py's FAIL on this file is the right verdict, reached by luck (its parser rejects every line without a colon, including valid indented continuations).

Source: https://yaml.org/spec/1.2.2/ (sections 8.2.3, 6.3, 6.7, 7.3.3; productions [69], [74], [134], [197]).

### 1.4 Other official facts that affect the validators

- Claude Code: "All fields are optional"; only `description` is recommended. "Claude Code ignores a field it doesn't recognize without reporting an error." So a typo like `disable-model-invokation` is silently ignored there but rejected by both official validators. Description plus `when_to_use` is truncated at 1,536 characters in the skill listing. `allowed-tools` accepts a space/comma string or a YAML list; the spec says a space-separated string. https://code.claude.com/docs/en/skills
- Claude API: up to 20 skills per request; total upload under 30 MB uncompressed; name max 64, lowercase letters/numbers/hyphens, no XML tags, no reserved words; description max 1024, non-empty, no XML tags. https://platform.claude.com/docs/en/build-with-claude/skills-guide
- claude.ai custom skill: name 64 characters maximum; description "200 characters maximum"; "Ensure the folder name matches your skill's name"; the ZIP should contain the skill folder as its root. The article calls the file "skill.md". https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

### 1.5 Recommendations for the validators (describe only; no files edited)

1. Parse the frontmatter with a real YAML parser. In skill_audit.py use PyYAML `safe_load` (document the dependency) or strictyaml to mirror skills-ref. If "standard library only" is a hard rule, write a small parser that supports plain, quoted, folded `>`/`>-` and literal `|` scalars plus one nested mapping for `metadata`, and fails loudly on anything else. In validate_skill.sh, either call the Python script or at least join indented continuation lines, strip quotes, strip `\r`, and stop reporting a length when the value is `>` or `|`.
2. Add the missing rules: reject unknown top-level keys (the six-field set); compatibility must be a string of at most 500; metadata must be a map; description must be a non-empty string; no `<` or `>` in the description; warn on "anthropic" or "claude" in the name; NFKC-normalise name and folder before comparing.
3. Add host profiles through a flag: `spec` (skills-ref rules), `claude-ai` (description at most 200, folder equals name), `claude-code` (allow its extra fields, warn on near-miss field names because unknown fields are silently ignored), `api` (at most 20 skills, under 30 MB). Print the description length against each limit. Today the three real skills would show "OK for spec, EXCEEDS claude.ai (610 / 411 / 253)".
4. Make both scripts give the same verdict from one implementation (one wraps the other). Ship a fixture set and an expected-verdict table: valid folded, valid quoted, CRLF, unindented continuation, unknown field, name mismatch, description over 1024, over 200, `---` inside the description, `https://` URL in the body. The kit's own rule applies: "A test only counts if a wrong answer would fail it." The ">" = length 1 false PASS would have been caught on the first fixture.
5. Where skills-ref is installed, run it side by side and report any disagreement. Say in the docs that skills-ref is demonstration-only and that Anthropic's quick_validate.py differs from it.
6. Cut false warnings: require a non-letter before a drive letter in the path regex so "https://" does not match; flag backslashes only outside fenced code or inside path-like tokens.
7. Repair example-skill (see 1.3) so the teaching example passes its own validators and skills-ref.
8. Update Reference sections 3 and 9: they still say the validator scripts are "not in this project", and the scripts now exist with the defects above.
9. If any skill will be uploaded to claude.ai, either keep a 200-character description for that upload or test the real upload first. Keep the long descriptions for Claude Code and the API (spec limit 1024; Claude Code listing cap 1,536).

## Part 2. Build method vs Anthropic's authoring page and skill-creator

Sources used: Anthropic "Skill authoring best practices" (platform.claude.com), anthropics/skills skill-creator SKILL.md, agentskills.io specification, "Using scripts in skills" and "Optimizing skill descriptions" pages, Claude Code skills docs, the SkillsBench abstract. Grades: SUPPORTED / PARTIALLY_SUPPORTED / CONTRADICTED / UNVERIFIED. "UNVERIFIED" here means no statement was found in the pages read; it does not mean wrong.

### 2.1 Graded steps

| ID | Where | Step or claim | Grade | Evidence |
|---|---|---|---|---|
| M01 | master prompt, Evidence rule 1 | Do not invent frontmatter fields or limits | SUPPORTED | Spec lists six fields; both official validators reject others. Caveat: Claude Code adds fields, so "do not invent" must be host-aware. |
| M02 | master prompt, Evidence rule 2 | Label facts [SOURCE] / [INFERENCE] / [UNVERIFIED] / [PROPOSED] | UNVERIFIED | Project convention; no official page prescribes labels. Not contradicted. |
| M03 | master prompt, Phase 0 | Ask for 3-5 triggering and 3-5 near-miss requests | PARTIALLY_SUPPORTED | Near-misses are strongly supported ("the most valuable negative test cases are near-misses"). But the official eval set is about 20 queries (8-10 and 8-10). The kit itself says 3-5 (master prompt), 10 and 10 (Reference 4.2), 20 at 60/40 (Omnibus). |
| M04 | master prompt, Phase 1 | Decide whether a skill is the right mechanism (vs memory, tools, hooks, subagent) | UNVERIFIED | No such gate in the best-practices page, skill-creator or the spec. Reasonable design. |
| M05 | master prompt, Phase 2 | At least 3 realistic tasks, run without the skill first, record the gap, add no instruction that closes no gap | SUPPORTED | Best-practices "Build evaluations first": identify gaps without a Skill, build three scenarios, establish baseline, "Write minimal instructions". Checklist: "At least three evaluations created". skill-creator: 2-3 test prompts, with-skill and baseline runs started in the same turn. |
| M06 | master prompt, Phase 2 | Trigger set of should-trigger and near-miss, separate validation set, test triggering apart from output quality | SUPPORTED | agentskills.io: train about 60%, validation about 40%, keep validation results out of revisions; output quality is a separate guide. |
| M07 | master prompt, Phase 3 | One default approach with a short escape hatch, no menu of equal options | SUPPORTED | Best-practices "Avoid offering too many options": provide a default with an escape hatch. |
| M08 | master prompt, Phase 3; Reference 1 | Scope to one coherent job | PARTIALLY_SUPPORTED | SkillsBench v1 abstract: focused Skills with 2-3 modules beat comprehensive documentation. That is about module count, not "one job per skill". |
| M09 | master prompt, Phase 4 | Portable frontmatter fields only; host-specific metadata in host-specific files | PARTIALLY_SUPPORTED | Spec has six fields, not two (license, compatibility, metadata, allowed-tools are optional). Claude Code keeps its extensions in the same SKILL.md frontmatter and ignores unknown fields without an error; "host-specific files" is the kit's own design. |
| M10 | master prompt, Phases 5-6 | Lean SKILL.md, explicit steps, relative forward-slash paths, references one level deep, say when each reference is read | SUPPORTED | Best-practices: "Concise is key", "Always use forward slashes", "Keep references one level deep". Spec: same one-level rule. |
| M11 | master prompt, Phase 7 | Script rules: non-interactive, --help, explicit inputs, useful errors, distinct exit codes, safe rerun, --dry-run, bounded output, documented dependencies | SUPPORTED | agentskills.io "Using scripts": interactive prompts are "a hard requirement" to avoid; --help; helpful errors; idempotency; dry-run; meaningful exit codes; predictable output size; state prerequisites. "No hidden network calls" is not stated there. |
| M12 | master prompt, Phase 8 | Do not present experimental host controls as universal security boundaries | SUPPORTED | Spec: `allowed-tools` is "Experimental. Support ... may vary between agent implementations". Claude Code: it pre-approves tools. "Audit bundled files" is not in the pages read (UNVERIFIED). |
| M13 | master prompt, Phase 9 | Check each host's documentation; limits do not transfer between hosts | SUPPORTED | Real differences found: description 1024 (spec/API) vs 200 (claude.ai upload) vs 1,536 listing cap (Claude Code); API 20 skills and 30 MB, no network at runtime; claude.ai can install packages. |
| M14 | master prompt, Phase 10 | Test battery: structural, with/without, trigger, adversarial/security, regression | PARTIALLY_SUPPORTED | Structural, baseline and trigger tests are official. Adversarial and regression tests are not in the pages read. Official advice the battery omits: test on Haiku, Sonnet and Opus; run repeated trials; human review. |
| M15 | master prompt, Phase 11 | Fix underlying causes, not keywords from failed examples; move repeated helper logic into scripts | SUPPORTED | agentskills.io: "Avoid adding specific keywords from failed queries - that's overfitting". skill-creator: "Generalize from the feedback"; "Look for repeated work across test cases ... put it in scripts/". "Add corrections to Gotchas" is UNVERIFIED. |
| M16 | master prompt, Phase 12 | Final delivery bundle (tree, full files, install steps, results, audit, changelog) | UNVERIFIED | Project convention. |
| M17 | Reference 4.2, step 1 | Collect 10 triggering and 10 non-triggering requests | PARTIALLY_SUPPORTED | Fits "about 20 queries: 8-10 and 8-10". But in the official flow the assistant drafts the 20 queries and the user reviews them (skill-creator Step 1); the kit asks the user to supply them. |
| M18 | Reference 4.2 step 6, section 8.8 | Break the skill on purpose and confirm each test fails | PARTIALLY_SUPPORTED | Not an official step. Closest official checks: skill-creator's analyzer flags "assertions that always pass regardless of skill (non-discriminating)" and "high-variance evals (possibly flaky)". Same aim, different method. |
| M19 | Reference section 3 | Description up to 200 characters for skills uploaded to the Claude app | SUPPORTED | Help center: "(200 characters maximum)". |
| M20 | Reference section 1 | SkillsBench (arXiv 2602.12670 v1): focused skills with 2-3 modules beat comprehensive documentation; self-generated skills gave no average benefit | SUPPORTED | v1 abstract (13 Feb 2026): 86 tasks, 11 domains, 7 agent-model configurations, 7,308 trajectories; curated Skills +16.2 percentage points; "Self-generated Skills provide no benefit on average"; "Focused Skills with 2--3 modules outperform comprehensive documentation". The current abstract page differs (see N10). |
| M21 | Omnibus 3, step 5 | Freedom calibration: prose for creative loops, scripts for precision | PARTIALLY_SUPPORTED | Official guidance has three levels (high, medium, low freedom); the medium level (pseudocode or scripts with parameters) is missing. |
| M22 | Omnibus 3, step 10 | Lock sensitive operations behind `disable-model-invocation: true` | PARTIALLY_SUPPORTED | Real, documented Claude Code field ("Set to true to prevent Claude from automatically loading this skill"). Not part of the portable spec: both official validators reject unknown keys (inference: not run), and other hosts would ignore it silently, so there is no lock there. It also conflicts with the kit's own step 11 (validate with skills-ref). |
| M23 | Omnibus 3, step 12 | Trigger evals: 20 queries split 60/40 | SUPPORTED | agentskills.io and skill-creator both say 20 queries, 8-10 each way, 60/40 train/validation. The kit leaves out: 3 runs per query, 0.5 trigger-rate threshold, up to 5 iterations, pick the best iteration by validation pass rate. "Similarity loops" is not an official term. |
| M24 | Omnibus 3, step 13 | "Double-blind test matrices" comparing with-skill against baseline | PARTIALLY_SUPPORTED | With-skill vs baseline is official. Blind comparison is "optional, requires subagents, and most users won't need it", and it means one independent judge not told which output is which (single-blind). "Double-blind matrices" is not official wording. |
| M25 | Omnibus 2, spec limits | name 64, description <1,024, body <500 lines | PARTIALLY_SUPPORTED | Spec: description "Max 1024" (1024 is allowed). Body "under 500 lines" and "< 5000 tokens" are recommendations, not limits. Metadata about 100 tokens is correct. |
| M26 | Omnibus 2, Claude API | 20 skills per request, 30 MB uncompressed, no network or runtime installs | SUPPORTED | Skills guide: "up to 20 Skills for each request"; "under 30 MB (uncompressed)". Best-practices: the API "has no network access and no runtime package installation". |
| M27 | Omnibus 3, step 6 | Frontmatter without XML tokens | SUPPORTED | Anthropic: no XML tags in name or description; quick_validate rejects `<` and `>` in the description. |
| M28 | Omnibus 3, step 11 | Validate with `skills-ref validate` | SUPPORTED | Spec "Validation" section. Caveat: README says demonstration only. |

Count: 28 graded. SUPPORTED 15, PARTIALLY_SUPPORTED 10, UNVERIFIED 3, CONTRADICTED 0.

### 2.2 Official advice the kit lacks

1. Test on every model you plan to use: Haiku, Sonnet, Opus (best-practices; checklist item "Tested with Haiku, Sonnet, and Opus").
2. Reference files longer than 100 lines should start with a table of contents.
3. Trigger testing details: 3 runs per query, trigger-rate threshold 0.5, up to 5 iterations, choose the iteration with the best validation pass rate (it may not be the last). Also: simple one-step tasks may not trigger a skill even with a perfect description.
4. Description style: agentskills.io says use imperative phrasing ("Use this skill when...") and "Err on the side of being pushy"; skill-creator says make descriptions "a little bit pushy" and put all "when to use" information in the description; Anthropic best-practices says write in third person. The official sources differ here; the kit's pattern (third-person "what it does" then "Use when ...") fits both.
5. Claude A / Claude B loop: build with one instance, test on real tasks with a fresh instance, bring observations back. Anthropic also says you do not need "a 'writing skills' skill" to get Claude to help create skills. The kit's master prompt is useful for its gates (baseline first, evidence labels), not for teaching the format.
6. Wording advice from skill-creator: "Explain the why"; ALL-CAPS ALWAYS or NEVER is "a yellow flag".
7. Reporting from skill-creator: pass rate, time and tokens per configuration as mean plus or minus standard deviation; human review through a viewer; check programmable assertions with a script, judge subjective skills by hand.
8. Anthropic content rules: no time-sensitive information (use an "old patterns" section); one term per concept; MCP tool names fully qualified as `ServerName:tool_name`; gerund naming (`processing-pdfs`) as the preferred style; no reserved words in names; avoid vague names (`helper`, `utils`).
9. Script advice: "Solve, don't defer" (handle errors in the script), no unexplained constants ("voodoo constants"), plan-validate-execute for batch or destructive work, verbose validator messages, pin versions in one-off commands, PEP 723 inline dependencies, stdout for data and stderr for diagnostics, checklists and feedback loops for multistep work.
10. The `compatibility` field (max 500) for environment needs; `when_to_use` and the 1,536-character listing cap in Claude Code.

### 2.3 Recommendations for the method

1. Pick one trigger-eval protocol and use it in all three kit documents: about 20 queries (8-10 / 8-10), fixed 60/40 split with both sets mixed, 3 runs each, 0.5 threshold, at most 5 iterations, best iteration by validation score. Keep "3-5 examples" only as Phase 0 seeding.
2. Replace "double-blind test matrices" with the official wording: with-skill vs baseline runs started together; optional blind comparison by an independent judge; mean plus or minus standard deviation over repeated runs; human review for subjective output.
3. Add a model matrix (Haiku, Sonnet, Opus) to the test phase and to the final checklist.
4. Keep "break the skill on purpose" as an extra check [PROPOSED], and add the official ones next to it: look for assertions that pass without the skill, and re-run evals to find flaky ones.
5. Fix Omnibus section 2 and 3 wording: description "at most 1,024"; body "recommended under 500 lines and about 5,000 tokens"; step 1 "prompt injection overhead" should read "repeated re-prompting" (prompt injection means an attack).
6. Move `disable-model-invocation` out of the portable steps. Say it is a Claude Code field, that portable validators reject it, and that on other hosts it does nothing. That removes the conflict between Omnibus steps 10 and 11.
7. Add the description rules in one place: third person, what plus when, no angle brackets, no reserved words in the name, at most 200 characters for claude.ai upload (with a short variant), 1,536 total with `when_to_use` in Claude Code.
8. Add the Claude A / Claude B loop with real tasks to the iteration phase, plus tables of contents for long reference files.
9. State which validator profile the kit targets and that skills-ref is demonstration-only (see 1.5).

## Part 3. What is new for daily use

- Two official validators exist and disagree; neither is a production gate by itself (skills-ref says so). Use the host's own check as the final test.
- claude.ai upload: 200-character description limit. Plan a short description if you upload there.
- Claude Code: all fields optional, unknown fields ignored silently, so spell-check your frontmatter by running a validator.
- SkillsBench has been revised since the Reference cited version 1 (see N10).

## Not verified or not reached (cap reached)

- Whether strictyaml accepts the folded `>` form: the page I read did not cover it (UNVERIFIED). Test with `skills-ref validate` yourself.
- validator.py line numbers are from the fetch tool's count, not mine. parser.py line numbers not obtained.
- No official validator was run, so every "would fail" statement about them is inference from source and spec.
- CRLF behaviour of validate_skill.sh (V14) is inference.
- Claude Code docs: last 9,478 characters not read. Skills guide: last 50,107 characters not read.
- Omnibus section 2 claims about Claude Code "1% of context", OpenAI Codex, OpenAI API and Cursor limits, and section 4's Snyk 36.8% were not checked in this run.
- agentskills.io "Evaluating skill output quality" page and Anthropic's Skills overview page were not read.

## New findings (N-ids)

- N01 Anthropic ships its own validator (quick_validate.py) that differs from skills-ref: PyYAML, angle-bracket ban, no folder-name check.
- N02 skills-ref README: demonstration only, not for production; it parses with strictyaml.
- N03 Claude Code: every frontmatter field optional; unknown fields ignored silently; description plus when_to_use capped at 1,536 characters in the listing.
- N04 claude.ai upload: description max 200 characters, name 64, folder must match name, ZIP root is the skill folder.
- N05 Official trigger-test protocol: 20 queries, 60/40, 3 runs, 0.5 threshold, up to 5 iterations.
- N06 Anthropic's authoring page: test on Haiku, Sonnet, Opus; table of contents for reference files over 100 lines; no time-sensitive facts.
- N07 skill-creator: analyzer flags non-discriminating and flaky assertions; benchmark reports mean plus or minus standard deviation; blind comparison is optional.
- N08 agentskills.io script guidance: avoiding interactive prompts is a hard requirement; separate stdout data from stderr diagnostics; pin versions.
- N09 Official sources differ on description voice (imperative and "pushy" vs third person).
- N10 SkillsBench current abstract page differs from v1: 87 tasks, 8 domains, 18 model-harness configurations, pass rate 33.9% to 50.5% (+16.6 percentage points), "Focused Skills with at most three modules outperform larger or exhaustive bundles". The Reference cites v1 (86 tasks, 11 domains, 7 configurations, +16.2 pp), which matches v1 exactly.
- N11 Anthropic: no special "writing skills" skill is needed to have Claude help create skills.
- N12 The kit's own three real skills have descriptions of 610, 411 and 253 characters, all over the claude.ai 200 limit.

## Source list (all primary)

- https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/src/skills_ref/validator.py
- https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/src/skills_ref/parser.py
- https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/README.md
- https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/scripts/quick_validate.py
- https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
- https://agentskills.io/specification
- https://agentskills.io/skill-creation/using-scripts
- https://agentskills.io/skill-creation/optimizing-descriptions
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://platform.claude.com/docs/en/build-with-claude/skills-guide
- https://code.claude.com/docs/en/skills
- https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- https://yaml.org/spec/1.2.2/
- https://arxiv.org/abs/2602.12670v1
- https://arxiv.org/abs/2602.12670
- https://hitchdev.com/strictyaml/using/alpha/scalar/string/ (did not cover `>`)

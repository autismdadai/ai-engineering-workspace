# Engineering Stack Part 09: Phase 4 Review

*October 15, 2026. The Phase 4 record for claude/engineering-stack-part-09-workflows-and-multi-agent.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed, or is marked otherwise. The plan gives Part 09 no security reviewer. Raw reports went to the owner in engineering-stack-research-part-09.zip.*

## Who checked what

| Check | By | Scope | Result |
|---|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet, given only claims and source links | 83 claims: Sections 1 to 3.6 (workflows, checkpoints, Temporal, retries, approval) | 77 supported, 3 supported in the part outside its scope, 3 partly, 0 contradicted; 16 web lookups plus clones and wheels |
| Blind source check B | Fresh agent on Claude Sonnet, same rules | 87 claims: Sections 3.7 to 11 (several agents, frameworks, picks, teaching, limits) | 79 supported, 4 outside scope, 4 partly, 0 contradicted; 28 web lookups |
| Beginner test | Fresh agent following Sections 7 to 9 literally, fresh virtual environments | Python 3.13.16, 3.12.3, 3.11.17; core lab and the LangGraph cross-check on all three | 21 problems: 0 high, 5 medium, 16 low; every quoted output matched character for character; no network connections (socket audit) |
| Mutation check | The lab's own `mutation_check.py` | 33 deliberate breaks | 31 of 33 on the first run (two real gaps, below); 33 of 33 after |
| LangGraph cross-check | `crosscheck.py` with `langgraph` 1.2.15 and `langgraph-checkpoint-sqlite` 3.1.2 | Resume rules, interrupt order, step limit, retry defaults, thread ids, SQLite resume | 6 of 6 on all three Pythons |
| Lead re-checks | The author | LangGraph's step-limit default and retry defaults in source; Temporal's retry defaults (SDK) and history limits (server); the Anthropic SDK's retry constants and jitter; Anthropic's multi-agent post; Kim et al.'s abstract | All confirmed; see findings 3 and 4 |

## Findings

| # | Severity | Quote (draft or lab) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| 1 | Medium | `run_lab.py`, `mutation_check.py`, `demo.py`, `crosscheck.py`: `tempfile.mkdtemp(...)` with no cleanup | Each `run_lab.py` run left 21 folders and each mutation run about 700; the test machine held 5,291 `lab09-` folders | Beginner test M4; reproduced with `ls /tmp \| grep -c lab09-` | The scripts now delete what they create; a full run leaves 0 [T]. Section 7.8 says so |
| 2 | Medium | Mutation "an existing thread restarted from scratch" and "ties counted as right" | Neither made `run_lab.py` fail | First mutation run, 31 of 33 | Check 2f now restarts a finished thread under its old id; check 12 adds a two-voter case where a tie is the deciding outcome; 33 of 33 |
| 3 | Medium | Draft, Section 3.9: "grows from 87 to 375 words" | The numbers were written before running; the lab prints 75 to 363 | Author's own re-run before Phase 4 | Corrected to 75 and 363 [T] |
| 4 | Info | Research: LangGraph's default recursion limit | The widely quoted 25 and the docs' 1,000 are both wrong for 1.2.15 | Re-read `_internal/_config.py` (10007); ran it (check L3) | Section 3.3 cites the code and says the docs differ; Section 5 uses it as a real example |
| 5 | Medium | "Calling another agent like a tool, with only a brief" | The source says the tool agent "receives generated input", not "a brief" | Check A025; reproduced: `agents/agent.py` docstring, line 633 | Reworded: "only the input the manager writes for it" |
| 6 | Low | "'Full Jitter' uses 'less work, but slightly more time'" | The comparison is with decorrelated jitter, which the sentence didn't say | Check A064; AWB | Named the comparison |
| 7 | Medium | Stripe's key rules (stored 500s, 255 characters, 24 hours) | Stated generally; the source scopes them to API v1 | Check A065; STR | Added "described for its API v1; v2 behaves differently" |
| 8 | Medium | "wide, separable research helped; sequential planning got worse [V: SCAL]" | SCAL's positive case is decomposable financial reasoning; the research case is Anthropic's | Check B008 | Cited both, each for its own case |
| 9 | Medium | "Copies of one model ... share mistakes, which is a reason debate ... gains shrink [V: ZHNG, SMIT]" | The explanation isn't in either source | Check B031 | Marked as this part's reading [I]; the sources cited only for what they found |
| 10 | Medium | "marking inter-agent text as data combined with a tagging step blocked it"; "about 4.7 turns" | The paper's Marking is a special symbol separating user and agent prompts; 4.7 is the turn of full infection in one 10-agent society | Check B032; PINF | Rewritten with the paper's definitions, and Marking alone's 76% added |
| 11 | Low | "Du et al. matched the number of calls, not tokens" | "Not tokens" is inference; the paper matched agents and doesn't report tokens | Check B081; DU | Quoted the paper's wording; "they don't report token counts" |
| 12 | Medium | Section 9, exercise 1: "before retry n = 3" | n counts from 0, which the exercise didn't say; a literal reader gets 2 s, not 4 s | Beginner test M1; reproduced | Said so; explained the stand-in random source; added the n = 5 check |
| 13 | Medium | Section 8, step 3: "Delete `my-checkpoints` when done." | No command; rerunning step 3 gives `ValueError: thread 'A17' already exists`, not in 7.7 | Beginner test M2; reproduced | Commands for both systems; a 7.7 row |
| 14 | Medium | Section 8, step 4: "replace the line with `flow.add_edge(...)`" | Pasting without the four-space indent gives `IndentationError` | Beginner test M3; reproduced | "keeping the four spaces at the start of the line" |
| 15 | Low | Section 6: "Three paths, as in every part" | Followed by four bullets | Beginner test M5 | "Paths, and when to skip them" |
| 16 | Low | 7.7 rows `StepLimitError: ...`, `StateTamperedError` | Python prints them with a `workflow.` prefix | Beginner test L6; reproduced | Full last lines shown |
| 17 | Low | Several wordings: "a brief carries three words", "part 1 and 2", "On the first run, two breaks", "about a minute", rule 2's "Approve", 68.7% against 68.3% | Each slightly off from what runs | Beginner test L1, L3 to L5, L9, L14 | Each reworded to match the output |
| 18 | Low | Terms without plain words: HMAC-SHA256, upsert; missing "first step is the entry"; `params` must be keyword arguments; no `thread_id` error row | Beginner trips | Beginner test L7, L10, L13 | Plain-words glosses, 7.6 sentences and a 7.7 row added |
| 19 | Low | "blocks network connections" | The script blocks `connect` and `create_connection`, not every route | Beginner test L12 | Narrowed the wording; the separate socket audit saw no connections |
| 20 | Low | Header tag counts | `[T on ...]` tags were not counted as [T] | Beginner test L15 | `assemble.py` counts them now (66 [T]) |

**Not changed.** Three set-A and four set-B claims were marked "supported, outside scope": negative statements ("no source compares", "no adoption data found") and ledger verdicts, which no source can confirm; their sourced parts checked out. Beginner L2 (a readable view of the checkpoint file) and L16's unzip confirmation were judged minor; L2 is answered by noting the file is one escaped string.

## Flags for the owner (not applied)

1. Claim ledger P8-01 and B1-03 are marked "confirmed"; the evidence supports "overstated" (Part 09, Section 10).
2. The prompt guide's §25 rule 7, capping total calls in code, matters more now that Claude Code subagents nest three layers by default. No change needed.

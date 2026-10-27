# Engineering Stack Part 07: Phase 4 Review

*October 14, 2026. The Phase 4 record for claude/engineering-stack-part-07-tools-and-protocols.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed, or is marked otherwise. Raw reports went to the owner in engineering-stack-research-part-07.zip.*

## Who checked what

| Check | By | Scope | Result |
|---|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet, given only claims and source links | 110 claims: Sections 1 to 3.8 (MCP) | 103 supported, 7 partly, 0 contradicted; 17 web lookups plus git clones |
| Blind source check B | Fresh agent on Claude Sonnet, same rules | 99 claims: Sections 3.9 to 11 (other protocols, skills, security, picks, teaching, limits) | 91 supported, 5 partly, 3 not checkable (headings or advice), 0 contradicted; 28 web lookups |
| Beginner test | Fresh agent following Sections 7 to 9 literally, fresh virtual environments | Python 3.13.16, 3.12.3, 3.11.17; core lab and the SDK cross-check on all three | 18 problems: 0 high, 5 medium, 13 low or information; everything passed on all three |
| Mutation check | The lab's own `mutation_check.py` | 20 deliberate breaks | 20 of 20; on the first run 5 were caught only by crashes, so the checks were restructured to report every crash as a FAIL line |
| SDK cross-check | `crosscheck.py` with `mcp` 2.3.0 | The SDK's client against the lab server (including the input_required round), the lab client against an SDK server | 8 of 8 on all three Pythons |
| Lead re-checks | The author | The 2026-07-28 changelog, MRTR, discover and schema pages (from the spec repo at tag 2026-07-28); the TypeScript package split (`npm view`); `mcp-remote` release dates; the Python SDK's "what's new" page at v2.3.0; AP2's FAQ; the A2A docs on ACP | See findings |

## Findings

| # | Severity | Quote (draft) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| 1 | Medium | "the same stdio server answers a 2025-era client's `initialize` and a 2026-era client's requests" | Spliced, not verbatim | Reproduced: `docs/whats-new.md` at v2.3.0 reads "the same `streamable_http_app()` (and the same stdio server) answers ..." | Exact quote; the researcher's own test stated separately as [T] |
| 2 | Medium | "The model still never talks to an MCP server directly" [V: MSP] | An inference, not a sentence in the spec | Checkers A and B; reproduced: `architecture/index.mdx:58` says the host "Coordinates AI/LLM integration and sampling" | Reworded as a conclusion from the quoted architecture, cited to MAR; same in the misconception in Section 9 |
| 3 | Medium | AP2: "Google project" | Incomplete: AP2's docs say spec work moves to FIDO | Reproduced: AP2 `docs/faq.md:149`, "The core specification work will continue in FIDO" | "Created by Google; 'core specification work will continue in FIDO'"; the extension quote now names UCP too |
| 4 | Medium | "both specs call them complementary" | MCP's spec doesn't mention A2A | Checker B; reproduced by searching the MCP spec repo | "the A2A spec calls them complementary (MCP's spec doesn't mention A2A)" |
| 5 | Medium | Section 8, step 2: "paste the same request without `"_meta":{...}`" | Deleting it by hand leaves a trailing comma: the server replies `-32700 Parse error`, not `-32602` | Reproduced | The second request printed in full; a note explains `-32700` |
| 6 | Medium | Exercise 2's check command | Ends in a traceback; nothing prints `error.data` | Reproduced | A one-line command that catches the error and prints the code and data; run and matched |
| 7 | Medium | Exercise 3: "Check by making the folder" | No content, location or command | Reproduced by reading | Copy, edit and run commands given; run and matched |
| 8 | Medium | Step 7: copy to `skills/Note-Finder` | On Windows and macOS, which ignore letter case, that is the same folder as `note-finder`; the copy and delete would hit the real skill | Reasoned (no Windows or macOS machine), accepted | Copy to `note_finder` with `shutil`, cross-platform; warning added |
| 9 | Medium | Section 7: "right-click the zip and choose Extract All" | Windows may nest the folder, so 7.1's `cd` fails | Reasoned, accepted [R] | Set the destination to `ai-stack`; move the inner folder up if nested |
| 10 | Low | "Input validation moved ... in 2025-11-25" [V: MTO] | The date is in the 2025-11-25 changelog, not the tools page | Checker A; reproduced: 2025-11-25 `changelog.mdx:28`, minor change 5 (SEP-1303) | New key M25 |
| 11 | Low | "each message is an HTTP POST to a single MCP endpoint" [V: MSH] | Quote is from the transports overview | Checker A; reproduced: `basic/transports/index.mdx:21` | Cited to MTR |
| 12 | Low | Definitions: "Spec revision 2026-07-28 is current" [V: MSP] | The overview doesn't say "current" | Checker A | "Revision 2026-07-28 is the newest" [V: MGT] |
| 13 | Low | Definitions: confused deputy [V: MAU] | The general definition isn't in MAU; MAU covers the MCP proxy case | Checker A; reproduced: `security-considerations.mdx:107-109` | Note narrowed to the MCP proxy case |
| 14 | Low | "Fewer tools also helped small models on edge devices" | The abstract says edge devices, not small models | Checker B | "models running on edge devices" |
| 15 | Low | 7.5: the lab server "refuses older handshakes, so a host ... will fail" [V: CCM] | The lab's behaviour isn't in CCM | Checker B | Tagged [T] for the lab's behaviour, [R] for hosts |
| 16 | Low | ACP source: A2A `docs/index.md` "IBM ACP: Incorporated into the A2A Protocol" | Not on A2A's main branch | Checker B's note; reproduced: no "ACP" in A2A `docs/` or README at commit 7c861a5 | Removed from the source entry; the ACP README and the LF AI & Data post remain |
| 17 | Low | Claude API connector header `mcp-client-2025-11-20` | A newer header exists | Checker A's note | Newer `mcp-client-2026-09-15` (tool-list pinning) mentioned |
| 18 | Low | 7.7: `column 1 (char 0)` | The lab's own break gives `column 2 (char 1)` | Reproduced | Both forms listed |
| 19 | Low | Step 3 result unstated | A beginner can't tell if 17 failures are expected | Reproduced: 17 FAIL lines, `5 of 22 checks passed` | Stated |
| 20 | Low | Step 2 output | The echoed paste and log line aren't mentioned | Reproduced | Described |
| 21 | Low | HMAC, SDK, CVE, CVSS, NVD, ZDR, stdout and stderr | Used without explanation | Reproduced by reading | Five definition rows added; other terms (gRPC, JWS, SEP) are glossed where used or are names |
| 22 | Low | 7.4: "28 packages besides pip" | Python 3.11 environments also have setuptools | Tester | "plus setuptools on Python 3.11" |
| 23 | Low | 7.8: `pip cache purge` | The cache is shared by all projects | Tester | Said so, as optional |
| 24 | Low | Step 5: "shown in full by `demo.py`" | `run_lab.py` prints them in full | Reproduced | Corrected |
| 25 | Low | 7.6: `answer_input=fn` | What `fn` receives and returns isn't said | Reproduced by reading | Stated |
| 26 | Low | Section 8 "Files" | Read as if the server isn't in the zip | Reproduced by reading | "all are in the zip" |
| 27 | Low | 7.2 had no expected result; 7.5 no way to find the environment's Python | Tester | Reproduced by reading | Added both |
| 28 | Low | Lead, before Phase 4: "Each client ... exactly one server" [V: MSP]; "Model-controlled" quotes | Quote is on the Architecture page; the control labels are on `server/index.mdx` | Lead's own extraction | Cited to MAR; MSP entry names `server/index.mdx` |
| 29 | n/a | Three claims (B007, B014, B069) | Headings or advice | Not defects | No change |

## Not changed, with reasons

- Checker A noted that "co-founded by Anthropic, Block and OpenAI" is the MCP blog's wording while the Linux Foundation release says "founding contributions from"; the AAF entry already includes the MCP blog post of the same date.
- Checker A noted a git tag `2024-10-07` in the spec repo with no revision folder; the part lists revisions, not tags.
- Checker B could not see the tail of the CVE-2025-49596 description in its fetch summary; the researcher's NVD read had it, and the score, scorer and fixed version were confirmed. Kept, with the source entry's grade at 8.
- The tester asked to remove the series' reader-test line ("Send back the output ...") and the mutation history; both are series conventions that record what was and wasn't run.
- The part is 108.8 KB, above the roughly 100 KB target agreed for Parts 06 onward, after removing duplicate passages and moving two lab files from the appendix to the zip.

# Engineering Stack Part 10: Phase 4 Review

*October 15, 2026. The Phase 4 record for claude/engineering-stack-part-10-security.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding below was reproduced by the lead session before it was fixed. Raw checker notes are in engineering-stack-research-part-10.zip, sent to the owner.*

## Who checked what

| Check | By | Result |
|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet; only claims and sources (179 claims split by topic) | 102 claims: 85 supported, 15 partly, 0 contradicted, 2 not checkable; 34 lookups |
| Blind source check B | Same rules | 77 claims: 51 supported, 18 partly, 0 contradicted, 8 not checkable; 44 lookups |
| Beginner test | Fresh agent, Sections 6 to 9 literally, fresh environments, Python 3.13.16, 3.12.3, 3.11.17 | 0 high, 0 medium, 3 low; every quoted output matched; cross-check installs took 100 s, 452 s and 200 s |
| Security review | Fresh agent, then the lead | The agent read the lab and most of the draft, then stopped when a safety classifier blocked its bypass testing; it chose not to work around the stop and reported no findings. The lead did the text pass and ran harmless edge cases with reserved names only (example.com, example.invalid) against each defence |

The first run of all four agents was cut off by a usage limit after about seven minutes; each was resumed with its own context once the limit reset.

## Findings

### F-01 · High · Per-defence adaptive results overstated
- **The draft said:** spotlighting and sandwiching "Above 95%"; classifiers "Above 90% for each"; target models "mostly not stated".
- **What goes wrong:** the figures hold on most target models, not all; a reader would think every tested setup failed at those rates.
- **Why:** Nasr et al., arXiv 2510.09023v1, Table 7 (Appendix G), search attack on AgentDojo across four targets: spotlighting 99/47/99/99%, sandwiching 95/69/100/99%, PromptGuard 94/75/99/95%, Protect AI 90/81/94/94%, Model Armor 90/56/82/82%, PIGuard 71/49/61/64%; no defence 100/75/100/96%. Found by checker A (A050 to A056, A063, A068, A087, A088) and checker B (B073); reproduced by the lead from the PDF through a summarizing fetch.
- **Fix:** Section 3.4's table gives the per-model numbers and the undefended baseline; Sections 4, 5, 9 and 10 reworded to match.

### F-02 · Medium · NeMo's model-free rails listed too narrowly
- **The draft said:** "regex, Presidio and YARA rails don't" call a model.
- **Why:** nemoguardrails 0.24.1, `library/jailbreak_detection/heuristics/checks.py` loads `gpt2-large` (checker A, A073; reproduced in the wheel).
- **Fix:** Sections 3.6 and 4 say jailbreak detection runs a local model.

### F-03 · Medium · Anthropic's HIPAA feature misnamed
- **The draft said:** "HIPAA mode"; "it needs a separate organization".
- **Why:** Anthropic's "API and data retention" page names the setting "HIPAA readiness", says it can't be disabled by an administrator, and says to use separate organizations only when both HIPAA-ready and general access are needed (checker B, B033; reproduced).
- **Fix:** Section 3.9's vendor table and the ABA source row.

### F-04 · Medium · The PwC caveat attributed to the authors
- **The draft said:** the prompt-level labels are something "the authors note penalizes any judge that reads the response"; a "150-million-parameter encoder" "ran about 187 times faster".
- **Why:** the paper states the labels are prompt-level (Section 2.3) but the penalty reasoning is this part's; another section calls the holdout human-adjudicated. The 187x is completions per second at batch size 8 on eight V100s (checker B, B015, B016; reproduced).
- **Fix:** Section 3.7 names Ettin-150M, scopes the throughput, marks the reasoning [I] and notes the paper's inconsistency.

### F-05 · Medium · Smaller source mismatches (grouped)
- Llama Guard 4 "April 2025" isn't on its card; the licence is dated April 5, 2025 (A066). Fixed.
- Meta's category-customization cookbook was written for Llama Guard 3, warns prompt-only additions work best near trained topics, and shows evaluation (A076). Fixed.
- Mistral's README names MNPL and MRL licences and doesn't say which models are Apache-2.0 (B047). Fixed.
- OpenAI's "since March 1, 2023" wasn't in the text the checker saw (B034). Date dropped.
- NCSC's wording is "may never be totally mitigated" (B071). Section 1 now uses it.
- ShieldGemma's F1 range spans three sizes, not one card (B008). Scoped.
- `LicenseRef-` is defined in the SPDX specification, not opened (A024): marked [U]. "Source-available" is this part's label (A025): said so.
- Section 1 cited the health-apps page for the covered-entity list (A006) and the AI Act's dates page for its reach (A007): citations corrected; the reach marked [U].
- Qwen README date January 8, not 9 (B046): now "January 2026".

### F-06 · Medium · `clean_output` let GitHub-style `www.` links through
- **The code:** `_BARE` matched only scheme-prefixed URLs.
- **What goes wrong:** a renderer that turns `www.host/path?d=data` into a link, or unfurls a preview, would contact a host not on the allowlist.
- **Why:** lead edge case: `see www.other.example.invalid/p?d=1` came out unchanged.
- **Fix:** a `_WWW` pass checked as `https://`; check 4d; mutation "www. links kept".

### F-07 · Medium · `strip_invisible` kept characters that hide data or render blank
- **Why:** lead edge cases kept U+FE0F, U+E0100 (variation selectors, which can carry data), U+034F, U+115F, U+3164, U+FFA0 and U+061C.
- **Fix:** a "variation" kind and a longer "other" list, with the emoji trade-off stated; check 5; mutation "variation selectors kept".

### F-08 · Medium · One approval could be reused
- **The code:** `action_id` hashed only the call, and `approve` had no used flag.
- **What goes wrong:** the same answer approved the same decision twice and a later identical call.
- **Why:** lead edge case: `same answer on a later identical call: True | same decision again: True`.
- **Fix:** a random nonce in each decision's id and single use; check 2c reordered (bad answers before the good one, since a used approval would make them pass trivially) plus replay cases; two mutations. Without the reorder, the mutation "approval accepts 'Approve'" was missed on the first run after the change, which is how the ordering problem was found.

### F-09 · Low · Redactor limits not stated
- **Why:** lead edge cases: SSNs without dashes or with spaces, cards with dots, IPv6, non-US phones pass unchanged.
- **Fix:** stated in Section 3.8 rather than widening the patterns, which would add false positives.

### F-10 · Low · Two absolute phrases
- "a recipient allowlist ... is always right" (Section 6) and "The doors ... always close" (Section 1): rules in code can be built wrong, as the part's own URL-parser case shows. Reworded.

### F-11 · Low · Beginner-test polish
- Step 7 prints a five-key dictionary with an unrounded precision: the text now says so.
- An empty `~/.cache/pip` folder remains after `pip cache purge`: harmless, not changed.
- Two self-check answers rely on Section 3, which the tester wasn't given: by design.

## Not acted on, with reasons

- Checker notes that are interpretations by design and already tagged [I] (B028, B070, A069).
- Items the checkers couldn't open but the lead or a researcher read in this session: reginfo.gov's agenda entry (B030, B076; re-read by the lead), the FTC page (B032; read by a researcher), the GDPR recitals (B036; read by the lead, grade 5).
- "Only housekeeping commits" for LlamaFirewall (B003) comes from a full `git log` in the researcher's clone; the checker's shallow clone couldn't show it.

## After the fixes

`run_lab.py` 28 of 28 and `mutation_check.py` 50 of 50 on Python 3.13.16, 3.12.3 and 3.11.17; `crosscheck.py` 7 of 7 re-run on 3.11.17; `demo.py` output unchanged; no `lab10` folders left in the temporary folder [T].

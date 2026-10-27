# Blind source check, list B (claims B001 to B077)

Checked October 15, 2026. Table: Claim | Verdict | Where in the source | Note. Local checks (wheels, git clones) marked [local]. Web lookups used so far: 0 (updated at end).

| Claim | Verdict | Where in the source | Note |
|---|---|---|---|
| B001 | supported | [local] nemoguardrails 0.24.1 wheel: METADATA (Apache-2.0, five rail types list lines ~218-226, Colang 1.0 default, "may or may not be suitable" line 325); telemetry.py lines 41, 98-113, 351-385; rails/llm/config.py `embeddings_only` | Telemetry on by default with startup + heartbeat (default 600 s) to events.telemetry.data.nvidia.com; opt-outs exactly as claimed. Source also honours `CI` and pytest as opt-outs (not mentioned, harmless). Not separately verified: which rails call a model (library/ dirs: content_safety, topic_safety, llama_guard, hallucination use the LLM; regex, sensitive_data_detection, injection_detection do not; consistent). |
| B002 | supported | [local] guardrails-ai 0.11.0 wheel: cli/configure.py lines 18-19 (DEFAULT_ENABLE_METRICS = True, DEFAULT_USE_REMOTE_INFERENCING = True), flags `--disable-metrics`, `--disable-remote-inferencing`; hub/install.py line 111 | Apache-2.0 in METADATA. Not traced: that validated text goes to "the vendor's hub API" (remote inference is used when a module has an endpoint). |
| B003 | partly | [local] llamafirewall 1.0.3 wheel and PurpleLlama at d934ea2: LICENSE (MIT), custom_check_scanner.py lines 37-39 (Llama-4-Maverick on api.together.xyz, TOGETHER_API_KEY), promptguard_utils.py line 111 (`truncation=True, max_length=512`), README line 172; PyPI JSON: 1.0.3 uploaded 2025-05-29 | Release date, licence, default model and truncation supported. Paper figures (17.63% to 1.75%, 47.73% to 42.68%) not yet checked (LFP). "only housekeeping commits since" not checkable from a depth-1 clone. |
| B004 | supported | [local] protectai/llm-guard: commit 168c103 "Archiving Project (#355)" dated 2026-07-08; README lines 1-4 | README says project and Hugging Face models "no longer under active development or maintained" (claim paraphrases as "no longer maintained"; fine). MIT badge in README. |
| B005 | supported | [local] Llama-Guard4/12B/MODEL_CARD.md lines 5, 50, ~160-190 table, LICENSE | 12B, pruned from Llama 4 Scout, S1 to S14 (S14 code interpreter abuse), English R 69% FPR 11% F1 61%, multilingual R 43% FPR 3% (F1 51%), output filtering, Llama 4 Community License. Card does not say "in-house" for the set explicitly in the table caption (card says "internal tests" elsewhere); text and images yes. |
| B006 | supported | [local] Llama-Guard3/8B and 1B MODEL_CARD.md, LICENSE | 8B: F1 0.939, FPR 0.040 (Table 1, internal English test set, response classification); 1B row 0.899/0.090 present (line 173 of 1B card); 14 categories (8B) and 13 (1B); Llama 3.2 Community License header in both. The 1B card does not label its table as a "response set" explicitly. |
| B007 | supported | [local] Llama-Prompt-Guard-2/86M MODEL_CARD.md lines 18, 22, 24, 69-75 | 86M 97.5%, 22M 88.7% recall at 1% FPR (English), "private benchmark", benign/malicious, explicit override attempts, Llama 4 Community License (LICENSE header). |
| B009 | supported | [local] ibm-granite/granite-guardian README (commit 9698a42, 2026-08-26) lines 5, 56-64; LICENSE Apache 2.0 | April 2026, 8B, yes/no score, custom criterion (BYOC). |
| B011 | supported | [local] nemoguardrails library/llama_guard/flows.co, flows.v1.co ("define bot refuse to respond" with fixed text "I'm sorry, I can't respond to that."); LG4 card (labels safe/unsafe + S codes) | The rail turns the Llama Guard verdict into a fixed refusal. |
| B013 | supported | [local] Prompt Guard 2 card line 24 | "support a 512-token context window. For longer inputs, split prompts into segments and scan them in parallel". |
| B014 | supported | [local] llamafirewall/scanners/promptguard_utils.py line 111 | `truncation=True, max_length=512`: text beyond 512 tokens is cut. |
| B020 | partly | [local] presidio repo head 2523c7b (2026-10-08): presidio-analyzer/presidio_analyzer/conf/default.yaml (model_name en_core_web_lg); LICENSE MIT; wheel presidio_analyzer 2.2.364 downloaded | Default spaCy model and MIT supported. Release date "July 22, 2026" for 2.2.364 not yet checked (PyPI). |
| B022 | supported | [local] presidio default_recognizers.yaml: 70 entries `enabled: false`, including UsMbi, UsNpi, UsHealthInsuranceMemberId, UsPriorAuthorizationNumber, UsClaimNumber, UsPrescriptionNumber, UsReferralNumber, UsProviderTaxId | |
| B023 | supported | [local] presidio README.MD line 55 (also docs/index.md line 43) | Exact quote present. |
| B024 | supported | [local] presidio-anonymizer/operators/: replace, redact, mask, hash (hash.py has a salt parameter), encrypt (aes_cipher.py, decrypt.py) | Pseudonymous-vs-anonymous statement is interpretation, not from source. |
| B045 | supported | [local] openai/gpt-oss README line 40 (Apache 2.0), line 45 (20b "run within 16GB of memory"), USAGE_POLICY | |
| B046 | supported | [local] QwenLM/Qwen3 README lines 395-398: "All our open-weight models are licensed under Apache 2.0." | Last README commit is 2026-01-08, claim says "(January 9, 2026)": one-day difference, possibly timezone. |
| B047 | partly | [local] mistral-inference README lines 71-72, 419-421 | MNPL ("Mistral AI Non-Production") and MRL named; library itself Apache-2.0. README does not state that listed models are Apache-2.0; it only flags two models as non-commercial. Claim "Varies: Apache-2.0, MNPL, MRL" is a fair inference, not stated. |
| B042 | supported | [local] llama-models @0e0b8c5 models/llama3/LICENSE lines 3, 22, 26, 28 | Release date April 18, 2024; "Built with Meta Llama 3"; no use of outputs to improve any other LLM; 700 million MAU. |
| B043 | partly | [local] llama3_1/LICENSE lines 24, 32; llama4/LICENSE lines 35, 46; llama3_2/USE_POLICY.md line 43; llama4/USE_POLICY.md line 71; llama3_3/LICENSE | Everything supported (no outputs ban in 3.1/4, "Built with Llama", "Llama" at beginning of name, 700M clause, EU multimodal restriction with end-user exception). Caveat: the 3.3 licence was not in the cited file list and the outputs-ban absence was not read in 3.2/3.3 text; checked only 3.1 and 4. |
| B044 | partly | [local] LG4 and PG2 LICENSE headers: Llama 4 Community License | Licence supported. Hugging Face gating (name, date of birth, organisation) not yet checked (HFG). |
| B051 | supported | [local] spdx/license-list-data @31ba1a5 json/licenses.json: version 3.29.0, release 2026-09-16; Elastic-2.0, SSPL-1.0, BUSL-1.1 all isOsiApproved False; no Llama or Gemma identifier | `LicenseRef-` advice is general SPDX practice, not in licenses.json. |
| B052 | supported | [local] same file: CC-BY-4.0 and CC-BY-NC-4.0 present, isOsiApproved False | The "doesn't belong in a commercial training set" is interpretation. |
| B053 | supported | [local] NeMo telemetry.py (see B001) | |
| B054 | partly | [local] guardrails-ai configure.py (supported); garak 0.17.0 wheel: grep for telemetry/analytics/requests.post found only generator modules (watsonx, huggingface, langchain_serve) | "garak, none found" is consistent with the wheel (only a search result, not a full audit). |
| B055 | supported | [local] presidio-analyzer email_recognizer.py line 3, 52 (`tldextract`), pyproject.toml line 32 | tldextract fetches the public suffix list by default; the fetch itself is in tldextract, not read here. |
| B056 | supported | [local] garak 0.17.0 wheel: METADATA (Apache-2.0, Requires-Python >=3.11), evaluators/base.py lines 389, 465 ("attack success rate", `ci_text`) | Confidence intervals present as `ci_text` in output. |
| B057 | supported | [local] garak detectors/agent_breaker.py lines 41-43: `detector_model_type: "nim"`, `detector_model_name: "openai/gpt-oss-120b"` | Needs-a-key-only-for-hosted-targets not fully traced. |
| B058 | partly | [local] garak METADATA: 45 Requires-Dist lines not marked `extra ==` (count 45); includes torch>=2.13.0 | 45 direct dependencies: matches exactly. "Pulls NVIDIA CUDA libraries on Linux" is a property of PyTorch's wheels, not shown in garak (and cites Part 05, not checkable). |
| B061 | supported | [local] microsoft/BIPIA: last commit a004b69, 2024-04-15 | |
| B064 | not checkable | | Recommendation, no source fact. |

## Updates to rows above after the web checks

| Claim | Verdict | Where in the source | Note |
|---|---|---|---|
| B003 | partly (final) | LFP arXiv 2505.03574v1 Section 4.3.2 and its table: baseline ASR 0.1763, utility 0.4773; combined 0.0175, 0.4268; PyPI release 2025-05-29 | Paper numbers and the 15.88 and 5.05 point differences are right (text rounds to 17.6%, 47.7%, 1.75%, 42.7%). Only "housekeeping commits since" could not be checked (shallow clone). |
| B020 | supported (final) | PyPI JSON: presidio-analyzer and presidio-anonymizer 2.2.364 uploaded 2026-07-22, MIT | |
| B044 | supported (final) | HFG page: login and accept needed; form asks full legal name, date of birth, full organization name; licence Llama 4 Community License | |
| B060 | supported | [local] agentdojo LICENSE (MIT); README BibTeX line 72 (NeurIPS 2024 Datasets and Benchmarks) | |
| B063 | not checkable | | "Checked October 15, 2026" is a date statement; PyPI JSON reads in this session did return current data, nothing to compare. |

## Remaining claims

| Claim | Verdict | Where in the source | Note |
|---|---|---|---|
| B008 | partly | SHG overview page: 2B, 9B, 27B and ShieldGemma 2 4B for images confirmed. Hugging Face card for shieldgemma-2b: "four harm categories", 2B optimal F1 0.812 (OpenAI Mod), 0.704 (ToxicChat), 0.825 internal prompt, 0.743 internal response; gemma terms | The overview page itself does not give the four harm types, the F1 range or the licence (it says CC BY 4.0 for the page content, Apache 2.0 for code). "0.69 to 0.83 across four sets" could not be reproduced: the 2B card shows 0.704 to 0.825 over the sets it lists (SimpleSafetyTests not reported there); the other sizes were not read. |
| B010 | supported | OMD page: "13" categories table, text and image inputs, "free to use", no accuracy figures | "Needs a key" is not stated on the page but is implied by any API endpoint. |
| B012 | not checkable | LGP (dev.meta.ai prompt-format page, llama-cookbook) not opened | The Llama Guard 4 card says its table values are averaged over S1 to S13, which is consistent with "own trained categories", but the ledger claim itself was not tested. |
| B015 | partly | PWC arXiv 2606.25782v1 Section 6.1 ("FNR of 0.658" for LlamaGuard-4; Ettin-150M "FNR of 0.422"), Section 6.3 ("187x throughput improvement" at batch size 8: 244.8 vs 1.31 CPS), Section 2.3 | 42,899 holdout, 65.8%, 42.2%, 187x confirmed. Differences: the 187x is throughput at batch size 8 on one cloud instance with 100 conversations (latency 717.6 ms to 3.6 ms), not a general speedup; the paper does not state "150 million parameters" (only the model name "Ettin-150M"); "out-of-distribution" and "PwC" were not shown on the pages read (arXiv page lists authors with no affiliation). |
| B016 | partly | PWC Section 2.3: "ground-truth labels are inherited directly from JailbreakBench and AILuminate and correspond to prompt-level labels rather than response-level adjudications" | Prompt-level labels confirmed. The claim that the authors "note [this] penalizes any judge that reads the response" was not found in the text returned. Also Section 5 of the paper calls the holdout "human-adjudicated annotations", which conflicts with Section 2.3; worth a caveat. |
| B017 | supported | YNG arXiv 2511.22047v1 abstract | Ten guard models, 1,445 prompts, 21 attack categories, Qwen3Guard-8B best at 91.0% public vs 33.8% novel, one author (Richard J. Young). |
| B018 | supported | JBB arXiv 2404.01318v5 Table 1: Llama Guard 72.0%, Llama Guard 2 87.7% agreement (300 prompt-response pairs, majority of three experts) | Section number 3.5 not confirmed from the page text. |
| B019 | supported | NAS arXiv 2510.09023v1 abstract and Table 7 | Adaptive attacks bypassed 12 defenses, most with ASR above 90%; the paper includes classifier defenses (PromptGuard 94%, Protect AI 90%, Model Armor 90%, PIGuard 71%). |
| B021 | supported | SPC release page en_core_web_lg-3.8.0: model size 382 MB, licence MIT | |
| B025 | supported | HHD (HHS de-identification page): "Although the risk is very small, it is not zero" | |
| B026 | supported | HHS Security Rule summary | Covered entities (plans, clearinghouses, providers sending standard electronic transactions) and business associates. |
| B027 | supported | HHS Security Rule summary: "Content last reviewed August 7, 2026"; "ePHI they create, receive, maintain, or transmit"; administrative, physical, technical safeguards; "accurate and thorough assessment" | |
| B028 | partly | Same page | The page lists the safeguard families; the specific inference (local processing does not make a system compliant; access controls, audit controls, device security) is the author's reading, and "ledger B4-08" was not seen. |
| B029 | partly | HHC cloud guidance: BAA required ("Yes, provided ... enters into a HIPAA-compliant business associate contract"); "Lacking an encryption key does not exempt a CSP from business associate status"; last reviewed December 23, 2022 | BAA and key points confirmed. "Plus its own risk analysis" was not confirmed in the text returned. |
| B030 | not checkable | RIN: reginfo.gov agenda pages for 0945-AA22 returned only a list of agenda links and an empty XML stub | "Long-Term Actions", "July 2027" and "90 FR 898" not confirmed or contradicted. |
| B031 | supported | HHA page, last reviewed May 30, 2025: information received by an app at the individual's direction is "no longer subject to the protections of the HIPAA Rules" | |
| B032 | not checkable | FTC page failed to load twice (client error) | The HHA page does not mention the Health Breach Notification Rule. 60 days, 500 or more, health apps, "unauthorized disclosure" all unverified. |
| B033 | partly | ACT: "Effective June 17, 2025", "Anthropic may not train models on Customer Content from Services". ABA docs page: "Conversation content ... is not retained by default; the exception is Covered Models ... 30-day retention"; "once enabled through the Console it cannot be disabled by an administrator". APR: updated July 1, 2026, "automatically delete inputs and outputs on our backend within 30 days". Privacy Center HIPAA article 8956058 | Training clause, date, the two conflicting retention descriptions and no-turn-off all confirmed. Not found: the name "HIPAA mode" (docs say "HIPAA-enabled organization" and "HIPAA readiness"), and "needs a separate organization". The docs say eligible features only (non-eligible features return a 400). Note the docs now name "Covered Models" with 30-day retention, which the claim does not mention. |
| B034 | partly | OYD page | Not used for training by default, 30-day abuse-monitoring retention, ZDR "subject to prior approval" confirmed. "Since March 1, 2023" not in the text returned. The page's HIPAA wording is "Business Associate and Healthcare Addendum" for the Decisions API, with per-endpoint conditions; the claim says "Business Associate Addendum for eligible endpoints". |
| B035 | supported | GMT: effective March 23, 2026; unpaid services used to improve products, human reviewers; paid services not used, logged "for a limited period of time, solely for detecting and preventing violations" plus legal disclosures; "You may use only Paid Services when making API Clients available to users in the European Economic Area" (and Switzerland, UK per page summary) | |
| B036 | not checkable | GDP: both EUR-Lex URLs returned only navigation and metadata, no recital text | Recitals 75 and 85 not read in this session. |
| B037 | partly | OMN EUR-Lex metadata: adopted 8 July 2026, `first_date_entry_in_force` 2026-07-27; EUA Article 113 text | Title, adoption and entry-into-force dates confirmed. The claim as given is cut off before the list of AI Act dates, so those were not checkable against OMN itself; the Article 113 page (consolidated 27 July 2026) shows 2 August 2026 general application, 2 December 2026 for Article 5(1)(ba),(bb), 2 December 2027 (Annex III) and 2 August 2028 (Annex I). |
| B038 | supported | EUA Article 113 page | Page links OJ:L_202601744 and states only a consolidation date (27 July 2026); no OJ publication date. Article 113 says entry into force is "on the twentieth day following that of its publication". |
| B039 | partly | CPP page: "Effective Date: January 1, 2026" for the ADMT, risk assessment and cybersecurity audit regulations (adopted July 24, 2025, OAL approval filed September 22, 2025) | Effective date confirmed. The page returned no later compliance deadlines, so "took effect" for all three topics is right only as an effective date. |
| B040 | supported | COL McDermott post (May 27, 2026; metadata modified July 29, 2026) | SB 26-189 signed May 14, 2026, effective January 1, 2027; a federal order of April 27, 2026 blocked enforcement of SB 205; SB 205 "now-defunct". "Never took effect as written" fits. Claim already flags it as a law-firm report. |
| B041 | supported | NIS: AI RMF abstract "intended for voluntary use"; AI 600-1 PDF Section 2.9 "prompt injection involves modifying what input is provided to a GAI system so that it behaves in unintended ways"; MS-2.7-007 lists "GAI attacks (e.g., prompt injection)" | |
| B048 | supported | GTU: "Last modified: April 1, 2026"; Section 3.1 requires distributors to bind recipients to the restrictions, 3.2 refers to the Prohibited Use Policy | |
| B049 | supported | gpt-oss README (Apache 2.0), Qwen README (Apache 2.0), Llama 3 licence (outputs ban, naming, 700M) | "Two generations old" and "strictest" are the author's judgement. |
| B050 | supported | OSD page | Four freedoms, data information "sufficiently detailed ... skilled person", complete code to train and run, parameters; October 28, 2024. |
| B059 | supported | GAP is an arXiv preprint (2406.11036); garak 0.17.0 README describes scanning models | Not opened: GAP full text. |
| B062 | supported | LKG dataset card: 1,000 rows (777/111/112), MIT, "prompt injections from Gandalf by Lakera" | |
| B065 | not checkable | | Recommendation list; sources ADJ, GAR, HHC support the individual items (AgentDojo, garak, BAA/cloud). |
| B066 | supported | NEM telemetry on by default (B001) and GAI metrics default True (B002) | |
| B067 | supported | OMD: free endpoint; text is sent to the endpoint | |
| B068 | supported | LLG archived 2026-07-08; OW6 LLM01 "no reliable prevention mechanism exists today" | |
| B069 | supported | CAM abstract: "solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo"; LFP numbers (B003); PRG arXiv 2606.26479v1 | PRG tests only Progent, one open-weight Qwen2.5-7B agent, 8 user tasks per suite, and says "one small-scale data point on a weak model with a single black-box attack template". NAS excludes CaMeL from its adaptive tests (it says plan-then-execute defences are out of scope), which supports "the one independent adaptive test ... was small". |
| B070 | partly | SHG, LG4, PG2, PWC, YNG | "Optimal F1" wording is on the ShieldGemma card; the gloss "best threshold chosen after the fact" is a definition, not a quote. Vendor-versus-independent disagreement and the two caveats are supported by PWC (prompt-level labels) and YNG (single author). |
| B071 | supported | NAS (adaptive attacks above 90% ASR on most defenses); NCS blog 8 December 2025; OW6 LLM01 line 65 | NCSC wording is "prompt injection attacks may never be totally mitigated" and "cannot be fully mitigated with a product or appliance", not literally "cannot be reliably prevented". |
| B072 | partly | OW6 repo @9253e38: 2026/README.md "Status: Published, Release date: August 4, 2026", CITATION.cff date-released 2026-08-04; LLM01 line 65 ("no reliable prevention mechanism exists today"); LLM08_HiddenContextExposure.md title "LLM08:2026 Hidden Context Exposure" | August 2026, the new LLM08 name and the LLM01 wording are confirmed. Not confirmed: "announced September 1"; the explicit statement that it renames System Prompt Leakage (the LLM08 file only mentions "system prompt leakage" in passing; the Preface refers generally to "renamed/re-scoped" entries); "hardens" relative to the 2025 text. |
| B073 | partly | NAS Table 7 | Spotlighting under the search-based adaptive attack: 99% for Gemini-2.5 Pro, Llama-3.3 70B and MetaSecAlign 70B, but 47% for GPT-5 Mini. "Above 95%" holds for three of four base models, not all. Taxonomy 3e itself was not seen. |
| B074 | supported | OW6 LLM01 prevention item 6: provenance labelling "reduces attack success in non-adaptive tests only: an attacker who knows the marking scheme can mimic..."; NAS | Matches "aid, not a defence". Skills appendix idea 3 not seen. |
| B075 | supported | [local] Llama-Guard3/8B/LICENSE and 1B/LICENSE headers: "LLAMA 3.2 COMMUNITY LICENSE AGREEMENT" | LGP, NCS, OW6 cited for this claim are irrelevant to it. |
| B076 | not checkable | RIN pages did not show the agenda status | See B030. |
| B077 | partly | OW6 (published August 2026 confirmed); PG2 card in PurpleLlama at d934ea2 is still Prompt Guard 2 | "Published August 2026" confirmed. "No newer Prompt Guard found" is a negative search result; the repo at the commit read shows only Prompt-Guard (v1) and Prompt Guard 2. |

## Not-instructions note
No page or file read contained text addressed to AI assistants. One file (the llm-guard README) carries an archive warning aimed at humans.

## Lookups used
44 of 45 (WebFetch plus one WebSearch; a failed FTC fetch counted). Clones and PyPI/wheel reads were free.

## Counts
Final verdicts over all 77 claims:
- supported: 51
- partly: 18 (B003, B008, B015, B016, B028, B029, B033, B034, B037, B039, B043, B047, B054, B058, B070, B072, B073, B077)
- contradicted: 0
- not checkable: 8 (B012, B030, B032, B036, B063, B064, B065, B076)

## Findings that matter most
1. B015: the "187 times faster" is throughput at batch size 8 on one cloud instance (100 conversations), not a general speedup. "150 million parameters" and "out-of-distribution" and "PwC" are not stated in the paper text read.
2. B016: the PwC paper contradicts itself on labels (Section 2.3 prompt-level labels; Section 5 "human-adjudicated annotations"). The claim that the authors note the penalty on response-reading judges was not found.
3. B073: spotlighting under adaptive attack is above 95% for three of four base models but 47% for GPT-5 Mini (NAS Table 7). "Above 95% on AgentDojo" overstates.
4. B033: "HIPAA mode" and "needs a separate organization" are not in the cited Anthropic pages (docs say "HIPAA-enabled organization"; cannot be disabled is confirmed). The docs now also name "Covered Models" with 30-day retention.
5. B034: OpenAI's page names a "Business Associate and Healthcare Addendum" (Decisions API example), per-endpoint conditions; "since March 1, 2023" not shown.
6. B008: the 0.69 to 0.83 F1 range was not reproduced; the 2B card shows 0.704 to 0.825.
7. B030, B076, B032, B036: RIN, FTC and GDPR pages would not load usable text; HIPAA proposal timing, the 60-day/500 breach rule and the GDPR recitals are unverified.
8. B072: "announced September 1" and the explicit "renames System Prompt Leakage" statement are not in the repo; August 4, 2026 release date and LLM08:2026 Hidden Context Exposure are confirmed.
9. B046: Qwen README last changed January 8, 2026 (claim says January 9).
10. B003: "only housekeeping commits since" not checkable from a shallow clone.

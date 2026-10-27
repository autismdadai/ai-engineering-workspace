# Checker A results (blind source check of claims-A.md)

Batch 1: OWASP 2026/2025 (git), ATLAS (git), ASI mapping file. Claims that cite other sources too are marked "OW6 part only" until the other source is checked.

| Claim | Verdict | Where in the source | Note |
|---|---|---|---|
| A001 | supported | OW6 LLM01 Prevention and Mitigation, first paragraph | Quote exact: "LLMs make no architectural distinction between instructions and data ... no reliable prevention mechanism exists today". |
| A004 | supported | OW6 LLM03:2026 Description; OW5 file LLM06_ExcessiveAgency.md heading "LLM06:2025" | Was LLM06 in 2025 (sixth), LLM03 in 2026. Root causes: excessive functionality, permissions, autonomy. |
| A009 | supported | OW6 LLM01 | |
| A012 | supported | OW6 LLM01, Direct Injection section | "Jailbreaking is the subset of prompt injection..." |
| A013 | supported | OW6 LLM03:2026 | |
| A014 | supported | ATLAS v2026.09, AML.T0077 "LLM Response Rendering" | ID and mechanism right. Plain-language label is the document's own. |
| A015 | supported | ATLAS v2026.09, AML.T0110 "AI Agent Tool Poisoning" (sub-technique T0110.000 covers descriptions) | |
| A028 | supported | OW6 repo, `2026/final/` exists at commit 9253e38 | |
| A030 | supported | OW5 `2_0_vulns/LLM01_PromptInjection.md` line 34 | Quote exact. |
| A031 | supported | OW6 LLM01 Prevention, first paragraph | "the model's instruction boundary will eventually be bypassed". |
| A032 | supported | OW6 LLM08:2026 Description | Covers system prompt, developer instructions, retrieved policy text, tool schemas; "should not be considered a secret"; not a security boundary. |
| A033 | partly | `final/mappings/asi-2026.json` | Titles match except wording: file has "Tool Misuse & Exploitation", "Unexpected Code Execution (RCE)", "Memory & Context Poisoning". File says "announced 2025-12-09", not "published". The announcement post itself (source ASI) was not opened. |
| A034 | partly | asi-2026.json "version": "2026 (announced 2025-12-09)" | Mapping file side confirmed. Announcement post not read (web). |
| A036 | supported | OW6 LLM01 Indirect Prompt Injection section | web page, document, email, tool response, RAG passage, image, MCP output all listed. |
| A037 | supported | ATLAS v2026.09, AML.T0051 and AML.T0051.002 "Triggered" | Description matches: via user action or event, often targets AI agents. |
| A039 | supported | ATLAS AML.T0110 | |
| A040 | supported | OW6 LLM01 mitigation 5 (strip tag-block, variation-selector, zero-width characters) | |
| A041 | supported | ATLAS AML.T0080.000 "Memory"; OW6 LLM01 mitigation 9 | "Treat agent memory writes as privileged operations". |
| A042 | supported | OW6 LLM03 Description | |
| A043 | supported | OW6 LLM03 mitigations 1-7 are tool/permission/approval measures | |
| A044 | supported | OW6 LLM03 Note | "Sanitization of model inputs and outputs is not a root control for Excessive Agency". |
| A045 | supported | OW6 LLM01 Scenario #2 (markdown image exfiltration); ATLAS AML.T0077 | |
| A048 | supported | OW6 LLM01 mitigation 8 "Rule of Two as a floor" | Trifecta is restated in the same entry. |
| A093 | supported | OW6 LLM01 | |
| A098 | partly | OW6 repo exists; ASI mapping exists | "Checked to exist": repo confirmed. Agentic list page not opened. |

Batch 2: git/pip sources (PurpleLlama at d934ea2, nemoguardrails 0.24.1, garak 0.17.0, llama-models 0e0b8c5, gpt-oss, Qwen3, SPDX 3.29.0, llm-guard, AgentDojo, Presidio). Only the part of each claim these sources cover is rated; "X part only" means other cited sources are still pending.

| Claim | Verdict | Where in the source | Note |
|---|---|---|---|
| A008 | supported | LLM: llama3 LICENSE (700M MAU cap, "Built with Llama" naming, ban on using outputs to improve other LLMs); GOS: gpt-oss LICENSE Apache License 2.0; SPX | Apache-2.0 "keep the notice" is general licence knowledge, not in these files. |
| A019 | supported | NEM METADATA Summary: "adding programmable guardrails to LLM-based conversational systems" | |
| A020 | supported | LG4 model card: "safety classifier ... content safety classification" | |
| A023 | supported | SPX licenses.json v3.29.0 (2026-09-16): licenseId field | |
| A024 | not checkable | SPX licenses.json has no LicenseRef entries (as expected) | `LicenseRef-` is defined in the SPDX spec, which I did not open. |
| A025 | partly | SPX: Elastic-2.0, SSPL-1.0, BUSL-1.1 are all listed, none OSI-approved | "Source-available" is not an SPDX category; the label is the author's. IDs correct. |
| A053 (LG/PG part) | not checked here | | See NAS batch. |
| A057 | supported | ADJ: ethz-spylab/agentdojo LICENSE "MIT License" | |
| A066 | partly | LG3 8B card: "14 categories ... based on MLCommons taxonomy of 13 hazards"; LG4 card: S1-S14, 14 categories | "13 or 14" is right. "April 2025" release date and "12B" (12B yes) : date not in the cards. "Can be edited in the prompt ... no published accuracy" needs LGP (pending). LG3 "diverse risk taxonomies" quote not seen in the card. |
| A067 | partly | LG4 card, "Classifier performance" table: English R 69%, FPR 11% | LG4 half confirmed, with scope: output filtering, in-house test set, English. PWC "65.8%" pending. |
| A069 | partly | GAR METADATA: Summary "LLM vulnerability scanner"; subtitle "Generative AI Red-teaming & Assessment Kit"; OW6 README: release date August 4, 2026 | Both garak self-descriptions confirmed. "Tests a model, not live traffic" is the author's reading (README says it probes "an LLM or dialog system"). OWP "list page still 2025" pending. |
| A070 | supported | NEM library/llama_guard/actions.py parses a label; flows.co defines "bot refuse to respond"; LG4 card: model outputs safe/unsafe | |
| A071 | partly | PG2 card: "512-token context window ... split prompts into segments"; LFW promptguard_utils.py line 113 `truncation=True, max_length=512` | Truncation and 512 tokens confirmed. The quoted phrases from the other document are not in these sources. |
| A073 | partly | NEM library: self_check, content_safety, topic_safety, llama_guard actions call an LLM; regex, injection_detection (YARA), sensitive_data_detection (Presidio) do not | "Only regex, Presidio and YARA don't" is too narrow: library/jailbreak_detection/heuristics uses GPT-2 perplexity (a model call but not the app LLM) and there are many third-party rails. Version 0.24.1 confirmed. |
| A074 | supported | NEM METADATA: "Two versions of Colang, 1.0 and 2.0, are supported and Colang 1.0 is the default"; config.py UserMessagesConfig.embeddings_only default False | |
| A075 | supported | NEM (rule-based rails: regex, YARA, Presidio) | |
| A076 | pending | LGP not opened | |
| A077 (PG2 part) | supported | PG2 86M card: "Recall @ 1% FPR (English) 97.5%", private benchmark | Applies to the 86M model; the 22M is 88.7%. NAS part pending. |
| A082 | supported | LLM: llama3 LICENSE clause v ("will not use ... output or results ... to improve any other large language model"); llama3_1 and llama4 LICENSE have no such clause; GOS Apache License; QWN README "All our open-weight models are licensed under Apache 2.0" | "Llama 3.1 to 3.3" directories exist; 3.3 licence text not read. |
| A084 | supported | LLG git log: 168c103 "Archiving Project (#355)", 2026-07-08 | |
| A086 | partly | PG2 22M card: 512-token window | "22M" model exists; HFG page pending (the "start with 22M" advice is the author's). |
| A091 | supported | PRS README.MD line 55: "no guarantee that Presidio will find all sensitive information" | "Patterns miss names and addresses" is the author's test result (not checked). |

Batch 3: web sources (arXiv abs/pdf via WebFetch, Meta, Willison, NCSC, HHS, FTC, EU AI Act service desk, Anthropic/OpenAI docs, Google, WHATWG, OWASP pages, NIST, HF) and MCP spec (git). 34 web lookups used of 45. WebFetch results are summaries by a small model, so exact numbers were taken from its extraction of the paper tables; no page contained text aimed at AI assistants.

## Final table (all verdicts; refer to batches above for locations)

| Claim | Verdict | Where in the source (section, line, table) | Note |
|---|---|---|---|
| A001 | supported | OW6 LLM01 Prevention para 1 | |
| A002 | supported | NCS blog, 8 Dec 2025: "inherently confusable deputy"; "no distinction made between 'data' or 'instructions'" | |
| A003 | supported | GRE abstract (data likely to be retrieved, remote); OW6 LLM01 Indirect section ("The user did not supply or see those instructions") | |
| A004 | supported | OW6 LLM03; OW5 LLM06:2025 | |
| A005 | supported | LG4 card table (69% R / 11% FPR); PG2 card (97.5% at 1% FPR); both "in-house"/"private" sets | |
| A006 | partly | FTC page (mod. July 14, 2026): HBNR covers PHR vendors, related entities, third-party service providers; excludes HIPAA covered entities; HHA (reviewed May 30, 2025): defines business associate, says apps outside HIPAA are not covered | The list of covered entities (plans, clearinghouses, providers sending electronic standard transactions) is not on the HHA page I opened; HHA page does not mention the FTC rule. FTC half is fine. |
| A007 | partly | EUA Art 113: applies from 2 Aug 2026, with staggered dates | Article 113 gives dates only; it says nothing on EU reach (that is Art 2, not cited) or the GDPR (author already flags it unread). |
| A008 | supported | LLM, GOS, SPX (see batch 2) | |
| A009 | supported | OW6 LLM01 | |
| A010 | supported | NIS 2.9: "In direct prompt injections, attackers might craft malicious prompts and input them directly"; OW6 Direct Injection | |
| A011 | supported | GRE; OW6 Indirect section | |
| A012 | supported | OW6 LLM01: jailbreaking "is the subset of prompt injection" | |
| A013 | supported | OW6 LLM03 | |
| A014 | supported | ATL T0077 | |
| A015 | supported | ATL T0110 | |
| A016 | supported | LTF: private data, untrusted content, external communication | |
| A017 | supported | RO2: "no more than two" of A untrustworthy inputs, B sensitive systems or private data, C change state or communicate externally | "Without a person" is not in the property wording (the blog adds human supervision when all three are present). Minor. |
| A018 | supported | NAS abstract: attackers tailor methods to each defense | |
| A019 | supported | NEM | |
| A020 | supported | LG4 | |
| A021 | supported | HHS Security Rule summary (ePHI) | |
| A022 | supported | HHC: HIPAA-compliant business associate contract with the CSP | |
| A023 | supported | SPX | |
| A024 | not checkable | SPX licenses.json lists no LicenseRef entries | Defined in SPDX spec, not opened. |
| A025 | partly | SPX | IDs listed, none OSI-approved; "source-available" label is the author's. |
| A026 | supported | OWP resource page: "August 3, 2026"; announcement URL dated /2026/09/01/ | Note: OW6 README and CITATION.cff say August 4, 2026 (release date). Three dates in play: Aug 3 (page), Aug 4 (repo), Sept 1 (post). |
| A027 | supported | OWP list page fetched Oct 15, 2026: heading "2025 Top 10", entries LLM01:2025 to LLM10:2025; only 2026 mention is an InfoSec World banner | |
| A028 | supported | OW6 repo `2026/final` | |
| A029 | not checkable | Claim text is empty in claims-A.md (only source keys OW5, OW6) | |
| A030 | supported | OW5 LLM01 line 34 | |
| A031 | supported | OW6 LLM01 | |
| A032 | supported | OW6 LLM08 | |
| A033 | supported | ASI resource page: Dec 9, 2025, "for 2026"; asi-2026.json titles | Title wording: file has "&" and "(RCE)"; page does not list the ten. |
| A034 | supported | asi-2026.json "announced 2025-12-09"; resource page Dec 9, 2025 | |
| A035 | supported | GRE abstract (arXiv v, Feb 23 2023, rev May 5 2023) | AISec 2023 venue and pp. 79-90 not confirmable from the arXiv page. |
| A036 | supported | OW6 LLM01 | |
| A037 | supported | ATL v2026.09, T0051 / T0051.002 | |
| A038 | supported | MCP 2026-07-28 index.mdx lines 110-112; tools.mdx line 306 ("MUST" for annotations) | |
| A039 | supported | ATL | |
| A040 | supported | OW6 LLM01 mitigation 5 | |
| A041 | supported | ATL T0080.000; OW6 mitigation 9 | |
| A042 | supported | OW6 LLM03 | |
| A043 | supported | OW6 LLM03 | |
| A044 | supported | OW6 LLM03 Note | |
| A045 | supported | OW6 Scenario #2; ATL T0077 | |
| A046 | supported | LTF: "in web application security 95% is very much a failing grade" | Source frames it as vendor claims of catching 95%. |
| A047 | supported | RO2: "a supplement ... not a substitute"; "should not be viewed as a finish line" | |
| A048 | supported | OW6 mitigation 8 | |
| A049 | supported | NAS abstract: "bypass 12 recent defenses ... above 90% for most; ... the majority of defenses originally reported near-zero" | |
| A050 | partly | NAS Table 7 (Spotlighting: 99% Gemini 2.5 Pro, 47% GPT-5 Mini, 99% Llama-3.3 70B, 99% MetaSecAlign); SPT abstract ("greater than 50% to below 2%", GPT-family) | SPT figures confirmed. "Above 95%" holds on three of four targets; on GPT-5 Mini it is 47%. |
| A051 | partly | NAS Table 7 (Sandwiching: 95%, 69%, 100%, 99%) | "Above 95%" is exactly 95% on Gemini and 69% on GPT-5 Mini. |
| A052 | supported | NAS Table 7: MetaSecAlign 70B with no external defense 96% | |
| A053 | partly | NAS Table 7 (Gemini 2.5 Pro column): PromptGuard 94%, Protect AI 90%, Model Armor 90%, PIGuard 71% | "Above 90% for each" is wrong: Protect AI and Model Armor are exactly 90% on Gemini and lower on other targets (Model Armor 56% GPT-5 Mini; PIGuard 49-71%). PIGuard 71% matches the Gemini column. |
| A054 | supported | IHR abstract: "drastically increases robustness", GPT-3.5, no figures | "Not among the 12" matches the NAS list as far as I saw. |
| A055 | supported | CAM abstract (v2, 2025-06-24): 77% with provable security vs 84% undefended | |
| A056 | partly | NAS Table 7 lists four target models (Gemini 2.5 Pro, GPT-5 Mini, Llama-3.3 70B, MetaSecAlign 70B); Model Armor row uses Gemini 2.5 Pro base | Classifier rows are reported for several targets, not only Gemini 2.5 Pro. Text for other defenses (RPO, Circuit Breakers, StruQ) names no target. |
| A057 | supported | ADJ LICENSE (MIT) | |
| A058 | supported | PRG: Progent, Qwen2.5-7B, ASR 25.8% to 4.2%, adaptive 2.6%; "one small-scale data point ... a preliminary data point, not a proof" | Also "Not peer-reviewed". |
| A059 | supported | AJB indirect-injection section | Page also says "While Claude is inherently resilient to such attacks" and "a successful injection can do minimal damage" (implied, not a plain admission). |
| A060 | supported | OAG: "greatly reduce, but don't fully remove, this risk" | |
| A061 | supported | GWS (updated 2026-10-13 UTC): "consistently mitigated indirect prompt injection attempts"; stripping risky markdown, user approval | URL is knowledge.workspace.google.com/admin/security/... "No one outside Google has measured" cannot be checked from the page. |
| A062 | supported | WHW: invalid-reverse-solidus, no failure; last updated 7 Oct 2026 | "Browser uses it as a slash" is shown by the spec example, not stated in the error row. |
| A063 | partly | NAS Table 7 | Spotlighting "above 95%" not true on GPT-5 Mini (47%). The lab-check part is not in any source. |
| A064 | supported | OW6 (jailbreak = subset of injection); NIS section 2 lists "Dangerous, Violent, or Hateful Content" as its own risk | |
| A065 | supported | OW6 LLM01 para 1; NCS; NAS | |
| A066 | partly | LG3 (14 categories on a 13-hazard taxonomy), LG4 (S1-S14); LGP cookbook | "Llama Guard 4 12B" yes; "April 2025" not in cards; LG3 quote "diverse risk taxonomies" not found in the card; cookbook shows customization plus an evaluation example (see A076). |
| A067 | supported | LG4 card table, English: R 69%, FPR 11% (output filtering, in-house set); PWC Section 6.1: "LlamaGuard-4 ... harmful rate of 3.5% and FNR of 0.658" | |
| A068 | partly | OW6 11 controls (input filtering is #3, "evadable by rephrasing or encoding"); NAS | OWASP count of 11 and filter evasion confirmed. "Over 90%" fails for PIGuard (71%) and varies by target. |
| A069 | partly | GAR METADATA; OW6 README (Aug 4, 2026); OWP | Garak's two self-descriptions confirmed; "tests a model, not live traffic" is interpretation (README says "an LLM or dialog system"). Publish date: see A026. |
| A070 | supported | NEM llama_guard actions and flows; LG4 | |
| A071 | supported | PG2: 512-token window, "split prompts into segments"; LFW promptguard_utils.py:113 truncation=True, max_length=512 | Quoted phrases from the other document are not in these sources. |
| A072 | supported | OW6 mitigation 1 ("partial control only"); WEI abstract ("vulnerabilities persist despite the extensive red-teaming and safety-training") | |
| A073 | partly | NEM 0.24.1 library | See batch 2: "only regex, Presidio and YARA" is too narrow (jailbreak_detection heuristics use GPT-2 perplexity). |
| A074 | supported | NEM | |
| A075 | supported | NEM | |
| A076 | partly | LGP cookbook README ("categories ... can be tuned"; notebook title "Taxonomy Customization, Zero/Few-shot prompting, Evaluation and Fine Tuning") | Customization in the prompt confirmed. Cookbook says prompt-only category addition "will only work for topics closely related to existing categories" and gives an evaluation example, so "publishes accuracy only for its own categories" may be too strong. LG3 notebook, not LG4. |
| A077 | supported | PG2 86M card: 97.5% recall at 1% FPR, private benchmark; NAS | 22M is 88.7%. |
| A078 | supported | NEM topic_safety actions call an LLM | |
| A079 | supported | LES abstract: soft prompts learned by backpropagation, frozen model | |
| A080 | supported | HHC (BAA + risk analysis); ABA (BAA for Claude API with HIPAA config); OYD (OpenAI BAA/"Healthcare Addendum") | Defence and finance not checked, as the claim says. |
| A081 | supported | HHS Security Rule summary: "create, receive, maintain, or transmit" | |
| A082 | supported | LLM, GOS, QWN | |
| A083 | supported | NAS abstract | Rates differ by defense (PIGuard 71% on Gemini). |
| A084 | supported | LLG | |
| A085 | supported | OW6 README vs OWP list page | |
| A086 | supported | PG2, HFG: 22M exists, 512-token window | Advice to start with 22M is the author's. |
| A087 | partly | OW6 mitigation 1 (partial control) fine; NAS Table 7 | "Above 95%" is not true for both defenses on every target (Spotlighting 47% and Sandwiching 69% on GPT-5 Mini). |
| A088 | partly | NAS Table 7 | "Above 90%" does not hold for PIGuard (71%, 49%, 61%, 64%) or Model Armor on several targets. "Most flags are false alarms at realistic rates" is the author's calculation, not from NAS. |
| A089 | supported | OW6 LLM01 Scenario #2 | |
| A090 | supported | HHS | |
| A091 | supported | PRS README line 55 | |
| A092 | supported | OW6, RO2 | |
| A093 | supported | OW6 | |
| A094 | supported | RO2 | |
| A095 | supported | WHW | |
| A096 | supported | LG4 table (in-house, output filtering, English); PWC; NAS | |
| A097 | supported | HHS | "Starting with a risk analysis" is the author's ordering; the page requires risk analysis. |
| A098 | supported | OW6 repo and ASI resource page exist | |
| A099 | supported | CAM, NAS arXiv pages open | |
| A100 | supported | RO2 page open | |
| A101 | supported | PRS repo at 2026-10-08 head | |
| A102 | supported | HHS summary, HHC page open | |

## Counts

- supported: 85
- partly: 15 (A006, A007, A025, A050, A051, A053, A056, A063, A066, A068, A069, A073, A076, A087, A088)
- contradicted: 0
- not checkable: 2 (A024, A029)


## Findings that matter most

1. NAS numbers are overstated as blanket figures. Table 7 shows target-dependent results; "above 95%" for spotlighting and sandwiching (A050, A051, A063, A087) and "above 90% for each" classifier (A053, A068, A088) fail on at least one target (GPT-5 Mini 47% and 69%; PIGuard 49-71%; Protect AI and Model Armor exactly 90% on Gemini). The abstract only says "above 90% for most".
2. A056 says classifier rows name Gemini 2.5 Pro; the table has four targets.
3. A073 "only regex, Presidio and YARA don't call a model" is too narrow (jailbreak_detection heuristics use GPT-2).
4. A076/A066: Meta's cookbook shows an evaluation example and a limit on prompt-only category addition.
5. A006: the covered-entity list is not on the cited HHA page.
6. Dates: OWASP resource page says August 3, repo says August 4; the author lists only Aug 3 and Sept 1.
7. A029 has no claim text.

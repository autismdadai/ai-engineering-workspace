# Claims to check, list B

B001. | NeMo Guardrails 0.24.1 (NVIDIA, Apache-2.0) | Five rail types: input, dialog, retrieval, execution (tool input and output), output | Self-check input and output, fact-checking, hallucination, content-safety, topic-safety and Llama Guard rails call a model; regex, Presidio and YARA rails don't. Dialog rails use the LLM to match the user's intent unless `embeddings_only` is set | Colang 1.0 is the default, 2.0 supported. **Usage telemetry to NVIDIA is on by default**: a startup event and a heartbeat every 600 seconds to `events.telemetry.data.nvidia.com`, off with `NEMO_GUARDRAILS_NO_USAGE_STATS=1`, `DO_NOT_TRACK=1` or the file `~/.config/nemoguardrails/do_not_track` (read in the 0.24.1 wheel) . Its README says the built-in rails "may or may not be suitable" for a given production use |
    Sources: NEM

B002. | Guardrails AI 0.11.0 (Apache-2.0) | Input and output "Guards" built from validators | Depends on the validator | `guardrails configure` turns on vendor metrics and remote inference by default, which sends validated text to the vendor's hub API; turn both off with `guardrails configure --disable-metrics --disable-remote-inferencing` |
    Sources: GAI

B003. | LlamaFirewall 1.0.3 (Meta, MIT) | Prompt Guard 2, AlignmentCheck (audits an agent's reasoning for goal hijacking), CodeShield (static analysis of generated code) | AlignmentCheck calls Llama 4 Maverick on Together AI by default, which needs a key and sends text there | No release since May 29, 2025; only housekeeping commits since. Its Prompt Guard scanner truncates text at 512 tokens instead of splitting it, so long tool outputs are only partly scanned . Its paper reports attack success on AgentDojo falling from 17.63% to 1.75%, with task success from 47.73% to 42.68%, on a fixed attack set: 15.88 and 5.05 percentage points (vendor-run preprint) |
    Sources: LFP, LFW

B004. | LLM Guard (Protect AI, MIT) | Local scanners for injection, toxicity, secrets and personal data | Its own small models | **Archived on July 8, 2026**: the README says the project and its Hugging Face models are no longer maintained |
    Sources: LLG

B005. | Llama Guard 4 (Meta, April 2025) | 12B, pruned from Llama 4 Scout; text and images | Prompts or responses: "safe" or "unsafe" plus codes S1 to S14 (13 MLCommons hazards plus code-interpreter abuse) | English, output filtering, in-house set: recall 69%, FPR 11%, F1 61%; seven other languages: recall 43%, FPR 3% | Llama 4 Community License |
    Sources: LG4

B006. | Llama Guard 3 (Meta, 2024) | 8B; a 1B version | Same idea; 14 categories (13 for the 1B) | 8B: F1 0.939, FPR 0.040; 1B: F1 0.899, FPR 0.090 (internal English response set) | Llama 3.2 Community License |
    Sources: LG3

B007. | Llama Prompt Guard 2 (Meta, 2025) | 86M and 22M | "Benign" or "malicious": explicit attempts to override instructions, not harm | 86M: recall 97.5% at 1% FPR; 22M: 88.7% (Meta's private English jailbreak set) | Llama 4 Community License |
    Sources: PG2

B008. | ShieldGemma (Google) | 2B, 9B, 27B; ShieldGemma 2 for images (4B) | Four harm types | Optimal F1 0.69 to 0.83 across four sets, two of them Google's own | Gemma Terms of Use |
    Sources: SHG

B009. | Granite Guardian 4.1 (IBM, April 2026) | 8B | Yes or no for a named risk or your own criterion | IBM's claims not re-checked | Apache-2.0 |
    Sources: GGU

B010. | OpenAI `omni-moderation-latest` | Hosted | 13 categories, text and images | None published on the guide page | Free, but text goes to OpenAI and needs a key |
    Sources: OMD

B011. **The model writes a label, your app writes the refusal.** Llama Guard's output is text such as `unsafe` and `S1`; what the user sees comes from your code, as in NeMo's Llama Guard rail, which turns the label into a fixed refusal message .
    Sources: LG4, NEM

B012. Meta publishes accuracy only for its own trained categories (ledger B2-05) .
    Sources: LGP

B013. **Windows are short.** Prompt Guard 2 reads 512 tokens at a time, and its card says to split longer input and scan the pieces .
    Sources: PG2

B014. Code that truncates instead, as LlamaFirewall's scanner does, never sees the rest .
    Sources: LFW

B015. **Independent measurements are worse.** A 2026 preprint from PwC compared judges on a 42,899-example out-of-distribution holdout and found Llama Guard 4 missed 65.8% of harmful cases, against 42.2% for a 150-million-parameter encoder, which also ran about 187 times faster .
    Sources: PWC

B016. Its gold labels were taken from the benchmarks' prompt-level labels, not from judging each response, which the authors note penalizes any judge that reads the response; read 0.658 as disagreement with those labels, not a pure miss rate .
    Sources: PWC

B017. A 2025 single-author preprint tested 10 guard models on 1,445 prompts: the best, Qwen3Guard-8B, scored 91.0% on prompts from public benchmarks and 33.8% on new attacks .
    Sources: YNG

B018. Older guard versions were judged by JailbreakBench in 2024, where Llama Guard (version 1) agreed with expert labels 72.0% of the time and Llama Guard 2 87.7% .
    Sources: JBB

B019. And none of these rates holds against an attacker who tunes against the classifier (Section 3.4) .
    Sources: NAS

B020. **Presidio.** Microsoft's Presidio (presidio-analyzer and presidio-anonymizer 2.2.364, July 22, 2026, MIT) combines pattern recognizers like these with a named-entity model, spaCy's `en_core_web_lg` by default .
    Sources: PRS

B021. That model is 382 MB (version 3.8.0, MIT) .
    Sources: SPC

B022. Many recognizers ship turned off, including several US health-care identifiers, so a health app has to enable them deliberately .
    Sources: PRS

B023. Presidio's own README warns that because detection is automated, "there is no guarantee that Presidio will find all sensitive information" .
    Sources: PRS

B024. Its anonymizer can replace, redact, mask, hash (salted) or encrypt; encryption and keyed hashing can be reversed or tested by whoever holds the key, so they give pseudonymous data, not anonymous data .
    Sources: PRS

B025. HHS notes that the remaining risk is "very small", not zero .
    Sources: HHD

B026. **HIPAA.** It applies to covered entities (health plans, health-care clearinghouses, and providers that send health information electronically in standard transactions) and their business associates .
    Sources: HHS

B027. The Security Rule covers electronic protected health information they create, receive, **maintain** or transmit, and requires administrative, physical and technical safeguards, starting with an accurate and thorough risk analysis (HHS summary, last reviewed August 7, 2026) .
    Sources: HHS

B028. So processing on your own computer doesn't by itself make a system compliant: the data stored there still needs access controls, audit controls, device security and the rest (ledger B4-08) .
    Sources: HHS

B029. Cloud processing is allowed: a covered entity or business associate may use a cloud provider under a business associate agreement plus its own risk analysis, and a provider that stores encrypted ePHI without the key is still a business associate (ledger B4-01) .
    Sources: HHC

B030. The proposed update to the Security Rule (published January 6, 2025, 90 FR 898) is still a proposal: the latest Unified Agenda lists it under "Long-Term Actions" with final action estimated for July 2027 .
    Sources: RIN

B031. **Health apps outside HIPAA.** An app that is neither a covered entity nor a business associate, and receives health data at the user's direction, is outside HIPAA .
    Sources: HHA

B032. The FTC's Health Breach Notification Rule can then apply: it covers health apps, counts an unauthorized disclosure as a breach, and requires notice within 60 days of discovery, to the FTC as well when 500 or more people are affected .
    Sources: FTC

B033. | Anthropic | Commercial Terms (effective June 17, 2025): Anthropic may not train on customer content | Two Anthropic pages describe the default differently: the Privacy Center says API data is deleted within 30 days; the API docs say content isn't kept by default except for some models and features. Check both before relying on either | A business associate agreement through "HIPAA mode" in the Console; once on it can't be turned off, it needs a separate organization, and only eligible features work |
    Sources: ABA, ACT, APR

B034. | OpenAI | Not used for training by default since March 1, 2023 | Abuse-monitoring logs up to 30 days; zero data retention needs approval | A Business Associate Addendum for eligible endpoints |
    Sources: OYD

B035. | Google (Gemini API) | Free tier: content may be used to improve products and read by human reviewers; paid tier: not | Paid tier: logged for a limited period for abuse and legal needs | Apps offered to users in the EEA, Switzerland or the UK must use the paid tier (terms effective March 23, 2026) |
    Sources: GMT

B036. **The EU.** The GDPR treats health data as a special category and expects a controller to report a personal-data breach to the supervisory authority within 72 hours of becoming aware of it where feasible; both points were read in its recitals (75 and 85) .
    Sources: GDP

B037. The EU AI Act's dates, as amended by the Digital Omnibus on AI (Regulation (EU) 2026/1744, adopted July 8, 2026, in force July 27, 2026) :
    Sources: OMN

B038. The Official Journal publication date of the omnibus wasn't shown on the page read .
    Sources: EUA

B039. **US states and voluntary frameworks.** California's rules on automated decision-making, risk assessments and cybersecurity audits took effect on January 1, 2026 .
    Sources: CPP

B040. Colorado's 2024 AI Act never took effect as written; law-firm reports say a replacement, SB 26-189, was signed on May 14, 2026, to take effect on January 1, 2027 (not checked against the legislature's pages) .
    Sources: COL

B041. NIST's Generative AI Profile (AI 600-1, July 2024) is voluntary and lists prompt injection under information security .
    Sources: NIS

B042. | Llama 3 (April 18, 2024) | Meta Llama 3 Community License | Outputs may not be used to improve other large language models; show "Built with Meta Llama 3"; a separate licence above 700 million monthly active users |
    Sources: LLM

B043. | Llama 3.1 to 3.3 and Llama 4 | Their own community licences | The outputs ban is gone; show "Built with Llama"; a model trained on Llama output and distributed must have a name starting with "Llama"; the 700 million clause stays. The 3.2 and 4 use policies withhold rights to the multimodal models from people and companies based in the EU; their end users are not affected |
    Sources: LLM

B044. | Llama Guard 4, Prompt Guard 2 | Llama 4 Community License | Downloading Prompt Guard 2 from Hugging Face needs an account and accepting the licence, giving your name, date of birth and organization |
    Sources: HFG, LG4, PG2

B045. | gpt-oss-20b and 120b (OpenAI) | Apache-2.0, plus a short usage policy | The 20b runs within 16 GB of memory |
    Sources: GOS

B046. | Qwen (Alibaba) | Apache-2.0 for its open-weight models, per its README | Check each model card |
    Sources: QWN

B047. | Mistral | Varies: Apache-2.0, a non-production licence (MNPL) or a research licence (MRL) | Check each model |
    Sources: MIS

B048. | Gemma (Google) | Gemma Terms of Use (April 1, 2026) | Use restrictions that must be passed on to anyone you give the model to |
    Sources: GTU

B049. So (ledger P10-09b) Llama 3 8B is two generations old with the strictest of these terms; gpt-oss-20b or a small Qwen model, both Apache-2.0, have fewer conditions .
    Sources: GOS, LLM, QWN

B050. **What "open source" means for AI.** The Open Source Initiative's Open Source AI Definition 1.0 (October 28, 2024) asks for the freedom to use, study, modify and share, plus enough information about the training data for a skilled person to build a substantially equivalent system, the full training and running code, and the parameters .
    Sources: OSD

B051. **Tools.** The SPDX License List (version 3.29.0, September 16, 2026) gives standard short names; it marks Elastic-2.0 (Arize Phoenix, Part 02), SSPL-1.0 and BUSL-1.1 as not OSI-approved, and has no identifier for the Llama or Gemma terms, so a software bill of materials uses a custom `LicenseRef-` name for them .
    Sources: SPX

B052. CC-BY-4.0 and CC-BY-NC-4.0 both have SPDX identifiers and neither is an OSI software licence ; the NC means non-commercial, so such data doesn't belong in a commercial product's training set without separate permission .
    Sources: SPX

B053. **Telemetry, in one place,** as read in the code: NeMo Guardrails sends usage events to NVIDIA ;
    Sources: NEM

B054. Guardrails AI, metrics and remote inference once configured ; garak, none found ;
    Sources: GAI, GAR

B055. Presidio, none in its own code, but the suffix-list download .
    Sources: PRS

B056. **garak** (NVIDIA, 0.17.0, Apache-2.0, Python 3.11 or later) scans a model you point it at: probes send inputs, detectors judge the outputs, and the report gives an attack success rate per probe and detector, with confidence intervals .
    Sources: GAR

B057. It needs a key only for hosted targets, though one detector defaults to a hosted judge on NVIDIA's service .
    Sources: GAR

B058. It has about 45 direct dependencies, PyTorch among them, which on Linux pulls NVIDIA's CUDA libraries (Part 05, Section 7.5) .
    Sources: PYPI

B059. It tests a model, not your app's tool permissions ; its paper is a preprint .
    Sources: GAP

B060. **For agents,** AgentDojo (MIT) runs tasks and injection cases against an agent setup .
    Sources: ADJ

B061. Microsoft's BIPIA has had no commits since April 2024 .
    Sources: BIP

B062. Lakera publishes 1,000 injection attempts from its Gandalf game (MIT); it holds real attack text, so load it into a harness rather than pasting it anywhere .
    Sources: LKG

B063. Checked October 15, 2026 .
    Sources: PYPI

B064. Add Presidio when you need names and addresses found, and plan for its misses .
    Sources: PRS

B065. - **For production:** the same, plus a maintained guardrail framework or your model provider's classifiers as one more signal, adaptive tests of your own agent (AgentDojo-style tasks against your real tools), garak against the model you deploy, and a business associate agreement before any protected health information reaches a vendor .
    Sources: ADJ, GAR, HHC

B066. Turn off telemetry you didn't choose .
    Sources: GAI, NEM

B067. OpenAI's free moderation endpoint sends the text to OpenAI .
    Sources: OMD

B068. - **Avoid:** LLM Guard for new work (archived) ; any defence whose only safeguard is the model deciding correctly .
    Sources: LLG, OW6

B069. CaMeL's 77% against 84% and LlamaFirewall's AgentDojo figures are their authors' own measurements; the one independent adaptive test of a system-level defence found was small and says so .
    Sources: CAM, LFP, NAS, PRG

B070. Google's ShieldGemma figures are "optimal F1", the best threshold chosen after the fact; the independent preprints disagree with the vendors and have caveats of their own (PwC's prompt-level labels; a single-author study) .
    Sources: LG4, PG2, PWC, SHG, YNG

B071. - **An open question.** OWASP's 2026 text, the NCSC and Nasr et al. agree that injection can't be reliably prevented today; whether a future model architecture changes that is unknown, and this part doesn't predict it .
    Sources: NAS, NCS, OW6

B072. The 2026 edition (published August 2026; announced September 1, the date ledger §9 flag 2 gives) hardens LLM01 to no reliable prevention today and renames System Prompt Leakage as Hidden Context Exposure (LLM08:2026) .
    Sources: OW6

B073. *Taxonomy 3e, §17.3* reports spotlighting's result without Nasr et al.'s adaptive result against it (above 95% on AgentDojo) ; a freshness note, since its point about adaptive attacks stands.
    Sources: NAS, SPT

B074. *New skills appendix, idea 3, "injection-hardening"* builds on spotlighting; given the adaptive results, it should treat labelling as an aid, not a defence (Section 11) .
    Sources: NAS, OW6

B075. P12-03's note should say Llama Guard 3's licence files name the Llama 3.2 licence .
    Sources: LG3, LGP, NCS, OW6

B076. *Freshness ledger, Section 1:* the HIPAA question is settled (still a proposal, final action estimated July 2027) ;
    Sources: RIN

B077. OWASP's date becomes "published August 2026"; no newer Prompt Guard was found .
    Sources: OW6, PG2


# Sources

- ABA: Anthropic, "API and data retention" (https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) and Privacy Center, "I need to be HIPAA compliant, can I use Claude?" (https://privacy.claude.com/en/articles/8956058) [class OD]
- ACT: Anthropic Commercial Terms of Service, effective June 17, 2025. https://www.anthropic.com/legal/commercial-terms [class OD]
- ADJ: Debenedetti et al., "AgentDojo", arXiv 2406.13352v3; ethz-spylab/agentdojo README (NeurIPS 2024 Datasets and Benchmarks, per its BibTeX); PyPI [class PR]
- APR: Anthropic Privacy Center, "How long do you store my organization's data?", updated July 1, 2026. https://privacy.claude.com/en/articles/7996866 [class OD]
- BIP: microsoft/BIPIA repository (last commit April 15, 2024) [class OD]
- CAM: Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL), arXiv 2503.18813v2 [class PP]
- COL: McDermott Will & Schulz, "Colorado AI law in flux", May 27, 2026 (law-firm post) [class VB]
- CPP: California Privacy Protection Agency, CCPA updates rulemaking page. https://cppa.ca.gov/regulations/ccpa_updates.html [class SB]
- EUA: Regulation (EU) 2024/1689, Articles 50, 111 and 113, consolidated as of July 27, 2026, read via the European Commission's AI Act Service Desk. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113 [class SB]
- FTC: FTC, "Complying with FTC's Health Breach Notification Rule" (July 2024; page modified July 14, 2026) [class SB]
- GAI: guardrails-ai 0.11.0 wheel: `cli/configure.py`, `hub/validator_package_service.py`, `utils/hub_telemetry_utils.py` [class OD]
- GAP: Derczynski et al., "garak: A Framework for Security Probing Large Language Models", arXiv 2406.11036 [class PP]
- GAR: garak 0.17.0 wheel: README (METADATA), `evaluators/base.py`, `generators/`, `detectors/agent_breaker.py`; licence file [class OD]
- GDP: Regulation (EU) 2016/679 (GDPR), EUR-Lex CELEX 32016R0679, recitals 75 and 85 (the articles weren't reached) [class SB]
- GGU: ibm-granite/granite-guardian README and LICENSE (August 26, 2026) [class OD]
- GMT: Gemini API Additional Terms of Service, effective March 23, 2026. https://ai.google.dev/gemini-api/terms [class OD]
- GOS: openai/gpt-oss repository: LICENSE, USAGE_POLICY, README [class OD]
- GTU: Google, Gemma Terms of Use, last modified April 1, 2026. https://ai.google.dev/gemma/terms [class OD]
- HFG: Hugging Face model page, meta-llama/Llama-Prompt-Guard-2-86M [class OD]
- HHA: HHS, "The access right, health apps, and APIs", last reviewed May 30, 2025 [class SB]
- HHC: HHS, "Guidance on HIPAA & Cloud Computing", last reviewed December 23, 2022 [class SB]
- HHD: HHS, "Guidance Regarding Methods for De-identification of Protected Health Information" [class SB]
- HHS: HHS, "Summary of the HIPAA Security Rule", last reviewed August 7, 2026. https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html [class SB]
- JBB: Chao et al., "JailbreakBench", arXiv 2404.01318v5, Section 3.5, Table 1 [class PP]
- LFP: Chennabasappa et al., "LlamaFirewall", arXiv 2505.03574v1, Section 4.3.2 [class PP]
- LFW: meta-llama/PurpleLlama, `LlamaFirewall/` at commit d934ea2: README, `scanners/`, `promptguard_utils.py`, LICENSE; PyPI [class OD]
- LG3: Llama Guard 3 8B and 1B model cards and LICENSE files, PurpleLlama at d934ea2 [class OD]
- LG4: Llama Guard 4 12B model card and LICENSE, PurpleLlama at d934ea2 [class OD]
- LGP: Meta, Llama Guard 4 prompt-format page (dev.meta.ai); llama-cookbook `llama_guard` README and notebook [class OD]
- LKG: Hugging Face dataset card, Lakera/gandalf_ignore_instructions [class VB]
- LLG: protectai/llm-guard, commit 168c103 "Archiving Project", July 8, 2026; PyPI [class OD]
- LLM: meta-llama/llama-models at commit 0e0b8c5: `models/llama3/LICENSE`, `llama3_1/LICENSE`, `llama3_2/USE_POLICY.md`, `llama4/LICENSE`, `llama4/USE_POLICY.md` [class OD]
- MIS: mistralai/mistral-inference README (June 16, 2026) [class OD]
- NAS: Nasr et al., "The Attacker Moves Second", arXiv 2510.09023v1 (October 10, 2025): abstract, Section 5, Table 1 [class PP]
- NCS: UK NCSC, "Prompt injection is not SQL injection (it may be worse)", December 8, 2025 [class SB]
- NEM: nemoguardrails 0.24.1 wheel: README (METADATA), `telemetry.py`, `rails/llm/config.py`, `library/*/actions.py`, `library/llama_guard/` [class OD]
- NIS: NIST AI 600-1, Generative AI Profile, July 2024, Section 2.9 and MS-2.7-007. doi:10.6028/NIST.AI.600-1 [class SB]
- OMD: OpenAI docs, Moderation guide. https://developers.openai.com/api/docs/guides/moderation [class OD]
- OMN: Regulation (EU) 2026/1744 (Digital Omnibus on AI), EUR-Lex record OJ:L_202601744 [class SB]
- OSD: Open Source Initiative, Open Source AI Definition 1.0, October 28, 2024 [class SB]
- OW6: OWASP Top 10 for LLM Applications 2026, GenAI-Security-Project/GenAI-LLM-Top10 at commit 9253e38: CITATION.cff, `2026/README.md`, `2026/final/LLM01`, `LLM03`, `LLM08` [class SB]
- OYD: OpenAI docs, "Data controls in the OpenAI platform". https://developers.openai.com/api/docs/guides/your-data [class OD]
- PG2: Llama Prompt Guard 2 86M and 22M model cards and LICENSE, PurpleLlama at d934ea2 [class OD]
- PRG: Narisetty et al., "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents", arXiv 2606.26479v1 [class PP]
- PRS: microsoft/presidio at its October 8, 2026 head: README, `conf/default.yaml`, `default_recognizers.yaml`, `presidio_anonymizer/operators/`; presidio-analyzer 2.2.364 as installed and run [class OD]
- PWC: Jeon et al. (PwC), "Do Encoders Suffice?", arXiv 2606.25782v1: Sections 2.3, 6.1, 6.3, Appendices A and B [class PP]
- PYPI: PyPI JSON API, read October 15, 2026 [class OD]
- QWN: QwenLM/Qwen3 README, "License Agreement" (January 9, 2026) [class OD]
- RIN: reginfo.gov, Unified Agenda, RIN 0945-AA22, publication 2026 [class SB]
- SHG: Google, ShieldGemma overview and model card. https://ai.google.dev/gemma/docs/shieldgemma [class OD]
- SPC: explosion/spacy-models, release en_core_web_lg-3.8.0 [class OD]
- SPT: Hines et al., "Defending Against Indirect Prompt Injection Attacks With Spotlighting", arXiv 2403.14720 [class PP]
- SPX: spdx/license-list-data at commit 31ba1a5, `json/licenses.json`, version 3.29.0 (September 16, 2026) [class SB]
- YNG: Young, "Evaluating the Robustness of Large Language Model Safety Guardrails Against Adversarial Attacks", arXiv 2511.22047v1 [class PP]

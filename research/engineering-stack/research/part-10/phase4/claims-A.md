# Claims to check, list A

A001. OWASP's 2026 Top 10 for LLM Applications puts it as its first risk, LLM01, and says "LLMs make no architectural distinction between instructions and data", so "no reliable prevention mechanism exists today" .
    Sources: OW6

A002. The UK's National Cyber Security Centre says the same and calls the model "an inherently confusable deputy" .
    Sources: NCS

A003. **indirect** injection arrives in content the user never wrote or saw, such as a web page, an email or a tool's result .
    Sources: GRE, OW6

A004. OWASP lists it as LLM03:2026, up from sixth place in 2025, with three root causes: excessive functionality, excessive permissions and excessive autonomy .
    Sources: OW6

A005. They catch most of what they were trained on, miss some, and flag some harmless text, at rates their makers publish for their own test sets .
    Sources: LG4, PG2

A006. HIPAA covers health plans, health-care clearinghouses, health-care providers that send health information electronically in standard transactions, and their business associates, not every app that touches health data; an app outside HIPAA may fall under the FTC's Health Breach Notification Rule instead .
    Sources: FTC, HHA

A007. Serving people in the EU can bring in the GDPR (its territorial-scope article wasn't read in this session ) and the EU AI Act .
    Sources: EUA

A008. **T22, licences and data governance.** Model weights, code and datasets each come with a licence. "Open" ranges from Apache-2.0 (use it for anything, keep the notice) to licences with use policies, user caps, naming rules or a ban on commercial use .
    Sources: GOS, LLM, SPX

A009. | Instructions smuggled into a model's input | Prompt injection | OWASP LLM01:2026 |
    Sources: OW6

A010. | Injection typed by the user | Direct prompt injection | |
    Sources: NIS, OW6

A011. | Injection hidden in content the model reads | Indirect prompt injection | |
    Sources: GRE, OW6

A012. | Injection aimed at getting around safety rules | Jailbreak | OWASP treats it as a kind of injection |
    Sources: OW6

A013. | An agent that can do more than its job needs | Excessive agency | LLM03:2026 |
    Sources: OW6

A014. | Data sent out through a link or image the model writes | Exfiltration through rendered output | ATLAS AML.T0077 |
    Sources: ATL

A015. | Hidden instructions in a tool's description | Tool poisoning | ATLAS AML.T0110 |
    Sources: ATL

A016. | Private data, untrusted content and a way to send data out, together | Lethal trifecta | |
    Sources: LTF

A017. | At most two of untrusted input, sensitive access and outward action without a person | Agents Rule of Two | |
    Sources: RO2

A018. | Attacks tuned against the specific defence | Adaptive attack | |
    Sources: NAS

A019. | Checks around a model, by rules or by models | Guardrails | NeMo's term: "programmable guardrails" |
    Sources: NEM

A020. | A small model that labels text safe or unsafe | Safety classifier; guard model | |
    Sources: LG4

A021. | Health information HIPAA protects, in electronic form | ePHI | |
    Sources: HHS

A022. | A contract that lets a vendor handle a covered entity's PHI | Business associate agreement (BAA) | |
    Sources: HHC

A023. | A standard short name for a licence | SPDX identifier | |
    Sources: SPX

A024. | A licence name SPDX doesn't list | `LicenseRef-` identifier | |
    Sources: SPX

A025. | Code you can read but not use freely | Source-available licence | e.g. Elastic-2.0, SSPL-1.0, BUSL-1.1 |
    Sources: SPX

A026. OWASP's resource page shows August 3; the announcement post is dated September 1 .
    Sources: OW6, OWP

A027. One trap: on October 15, 2026, the list page at genai.owasp.org/llm-top-10/ still showed the 2025 edition, and nothing on it pointed to 2026 .
    Sources: OWP

A028. Use the 2026 files in OWASP's GitHub repository (GenAI-Security-Project/GenAI-LLM-Top10, folder `2026/final`) .
    Sources: OW6

A029. 
    Sources: OW5, OW6

A030. **The wording hardened.** In 2025, LLM01 said "it is unclear if there are fool-proof methods of prevention for prompt injection" .
    Sources: OW5

A031. Design on the assumption that the model's instruction boundary "will eventually be bypassed", and limit what the model may do and what its output may reach .
    Sources: OW6

A032. **Hidden Context Exposure** (LLM08:2026) widens the old system-prompt risk to developer instructions, retrieved policy text and tool schemas: design as if anything in the context can be extracted, and never put a secret there or rely on it as a boundary .
    Sources: OW6

A033. **Agents got their own list.** OWASP's Top 10 for Agentic Applications was published on December 9, 2025, labelled the 2026 edition: ASI01 Agent Goal Hijack, ASI02 Tool Misuse and Exploitation, ASI03 Identity and Privilege Abuse, ASI04 Agentic Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution, ASI06 Memory and Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue Agents .
    Sources: ASI

A034. OWASP's announcement and the 2026 list's mapping file agree on it (the PDF wasn't opened) .
    Sources: ASI, OW6

A035. Greshake et al. showed in 2023 that an attacker can plant instructions in data an LLM-integrated application is likely to retrieve, and so attack it remotely with no access to the chat (AISec 2023) .
    Sources: GRE

A036. OWASP's 2026 text lists the routes: web pages, emails, tool responses, retrieved passages, images and MCP output .
    Sources: OW6

A037. MITRE ATLAS, a catalogue of attacks on AI systems, splits LLM prompt injection (AML.T0051) into direct, indirect and **triggered** injection, the last fired by a later user action or event, often against agents (data release v2026.09) .
    Sources: ATL

A038. The MCP specification (revision 2026-07-28) says descriptions of tool behaviour such as annotations should be treated as untrusted unless they come from a trusted server, and that hosts must get the user's consent before invoking a tool .
    Sources: MCP

A039. ATLAS calls a planted description **tool poisoning** (AML.T0110) .
    Sources: ATL

A040. OWASP's 2026 mitigations include stripping invisible Unicode before text reaches the model .
    Sources: OW6

A041. ATLAS lists memory poisoning (AML.T0080.000), and OWASP says to treat memory writes as privileged actions .
    Sources: ATL, OW6

A042. **Excessive agency.** OWASP defines it as damage done because an LLM's output was unexpected, ambiguous or manipulated, whatever the cause, and traces it to excessive functionality, permissions or autonomy .
    Sources: OW6

A043. Its mitigations are mostly about the tools, not the model :
    Sources: OW6

A044. OWASP adds that cleaning inputs and outputs is not a root control for this risk .
    Sources: OW6

A045. OWASP's 2026 LLM01 uses exactly this as its second example scenario, and ATLAS lists it as AML.T0077, LLM response rendering .
    Sources: ATL, OW6

A046. He adds that a filter catching 95% of attacks is a failing grade in security .
    Sources: LTF

A047. Meta calls it a supplement to least privilege, not a finish line .
    Sources: RO2

A048. OWASP's 2026 text adopts both and calls the Rule of Two "a floor" .
    Sources: OW6

A049. They got past all 12, with attack success above 90% for most, though most had originally reported near-zero success .
    Sources: NAS

A050. | Spotlighting (Microsoft, 2024) | Mark untrusted text so the model can tell where it came from | Attack success from above 50% to below 2% on GPT-family models | Above 95% |
    Sources: NAS, SPT

A051. | Prompt sandwiching | Repeat the user's request after the untrusted text | n/a | Above 95% |
    Sources: NAS

A052. | MetaSecAlign | Train the model to ignore instructions in the data part | n/a | 96% |
    Sources: NAS

A053. | Injection classifiers (PromptGuard as packaged in LlamaFirewall; Protect AI's detector; Google's Model Armor) | A small model flags injection attempts | Prompt Guard 2: Section 3.7 | Above 90% for each; PIGuard 71% |
    Sources: NAS

A054. | Instruction hierarchy (OpenAI, 2024) | Train the model to rank system over user over third-party text | Robustness "drastically" up on GPT-3.5; the abstract gives no figures | Not among the 12; no independent adaptive test found |
    Sources: IHR

A055. | CaMeL (Google DeepMind and others, 2025) | Code derives the plan from the user's request only; untrusted data can't change it; policies check every tool call | 77% of AgentDojo tasks with provable security, against 84% undefended | Not among the 12; no independent replication found |
    Sources: CAM

A056. Target models for the adaptive results are mostly not stated in the paper's text; the classifier rows name Gemini 2.5 Pro .
    Sources: NAS

A057. MIT licence) .
    Sources: ADJ

A058. One small independent 2026 preprint tested a system-level defence (Progent) adaptively on a 7-billion-parameter model and found it held, while saying itself that one small test settles little .
    Sources: PRG

A059. **What vendors advise.** Anthropic: put untrusted content only in tool results, label its source, give tools least privilege, screen tool outputs with a classifier, red-team before launch; no guarantee claimed, and no plain statement that injections still get through .
    Sources: AJB

A060. OpenAI: keep untrusted input out of developer messages, pass structured outputs between steps, keep approvals on for MCP tools; it says these reduce the risk without removing it .
    Sources: OAG

A061. Google describes layered Gemini defences, including Markdown sanitization and user confirmation, and says they have "consistently mitigated" attempts, which no one outside Google has measured .
    Sources: GWS

A062. The WHATWG URL Standard treats a backslash in an `https` URL as a validation error, not a failure, so a browser goes on and uses it as a slash .
    Sources: WHW

A063. It is not a defence by itself: spotlighting, a published form of labelling, fell to adaptive attacks above 95% (Section 3.4) , and in the lab the stand-in model follows the injected line whether the page is labelled or stripped or neither; only the gate stops it (check 3c) .
    Sources: NAS

A064. | Threats include prompt injection, jailbreaking, data exfiltration and toxic output (P12-01) | Confirmed, with a caveat: OWASP counts jailbreaks as a kind of injection and exfiltration as an outcome, while harmful content is a separate safety concern, as NIST's profile also treats it | 3.1 |
    Sources: NIS, OW6

A065. | Separating data from instructions is "fundamentally challenging at the transformer level" (P12-02) | Partly supported: OWASP 2026 and the NCSC now say the model makes no distinction between instructions and data, and every defence tested adaptively fell; that is an expert position and a body of attacks, not a proof about the architecture | 1, 3.4 |
    Sources: NAS, NCS, OW6

A066. | Llama Guard 3 classifies "across diverse risk taxonomies" (P12-03) | Outdated: Llama Guard 4 (12B, April 2025) is Meta's newest; both use one trained set of 13 or 14 categories, which can be edited in the prompt with no published accuracy for the result | 3.7 |
    Sources: LG3, LG4, LGP

A067. | Routing text through Llama Guard "deterministically blocks" violations (P12-04) | Overstated: Llama Guard 4's own card gives 69% recall and 11% FPR on Meta's set; an independent preprint found it missed 65.8% on its holdout | 3.7 |
    Sources: LG4, PWC

A068. | Defence in depth requires sanitizing inputs, such as Base64 and role-play (P12-05) | Overstated: input filtering is one of OWASP's 11 controls, filters fall to rephrasing and encoding, and adaptive attacks beat the published input classifiers at over 90% | 3.3, 3.4 |
    Sources: NAS, OW6

A069. | Tools: the OWASP Top 10 for LLMs, NeMo Guardrails, garak, "a comprehensive LLM vulnerability scanner" (P12-06) | Overstated: the 2026 edition is current (published August 2026; the list page still shows 2025); garak calls itself both a vulnerability scanner and a red-teaming kit, and it tests a model, not live traffic | 3.1, 3.11 |
    Sources: GAR, OW6, OWP

A070. | Examples: an input classifier, PII masking, Llama Guard refusals (P12-07) | Illustrative ; Llama Guard outputs a label, and the application writes the refusal | 3.7 |
    Sources: LG4, NEM

A071. | An input filter with a risk threshold; output guardrails "enforce rigid" policy on "all" text (P12-08) | Overstated: thresholds trade misses for false alarms; Prompt Guard 2 reads 512 tokens at a time, and code that truncates checks only part of the text | 3.7 |
    Sources: LFW, PG2

A072. | Instruction-only alignment ("do not be toxic") is highly susceptible to jailbreaks (B2-01) | Confirmed indirectly: OWASP calls a constraining system prompt a partial control, and even trained-in safety is bypassed | 3.4 |
    Sources: OW6, WEI

A073. | Programmable guardrails "solve this fundamental flaw" with "deterministic, isolated" filters (B2-02) | Overstated: in NeMo Guardrails 0.24.1, self-check, content-safety, topic and Llama Guard rails call a model; only regex, Presidio and YARA rails don't | 3.6 |
    Sources: NEM

A074. | NeMo uses Colang for deterministic dialog flows (B2-03) | Overstated: Colang 1.0 is the default and 2.0 supported; dialog rails match intent with the LLM unless `embeddings_only` is set | 3.6 |
    Sources: NEM

A075. | Guardrails reroute "without ever invoking" the model (B2-04) | Overstated: true only of rule-based rails | 3.6 |
    Sources: NEM

A076. | Llama Guard scores against customized taxonomies (B2-05) | Partly supported: Meta says categories can be customized in the prompt; it publishes accuracy only for its own categories | 3.7 |
    Sources: LGP

A077. | A "deterministic" guardrail blocks "any" input resembling an override (B2-06) | Overstated: Prompt Guard 2 catches 97.5% at a 1% FPR on Meta's private set, and adaptive attacks beat such classifiers | 3.4, 3.7 |
    Sources: NAS, PG2

A078. | Colang flows "force" a banking assistant to refuse off-topic branches (B2-07) | Illustrative ; topic rails exist and rely on model calls and intent matching | 3.6 |
    Sources: NEM

A079. | The limits of "soft-prompt alignment (RLHF)" (B2-08) | Corrected: soft prompts are learned vectors with the model frozen; RLHF changes weights; a written instruction is neither | 2 |
    Sources: LES

A080. | Cloud APIs are "a non-starter" for medical work (B4-01) | Corrected: HHS allows cloud providers under a business associate agreement plus a risk analysis, and Anthropic and OpenAI both offer one for eligible API use; defence and finance rules not checked | 3.9 |
    Sources: ABA, HHC, OYD

A081. | Local summarization avoids HIPAA violations "by ensuring zero external network transmission" (B4-08) | Corrected: the Security Rule covers ePHI that is maintained, not only transmitted, and requires administrative, physical and technical safeguards | 3.9 |
    Sources: HHS

A082. | Llama 3 8B as the local example (P10-09b) | Outdated: followed by Llama 3.1 to 3.3 and Llama 4; Llama 3's licence alone bars using outputs to improve other models; gpt-oss-20b and Qwen's open models are Apache-2.0 | 3.10 |
    Sources: GOS, LLM, QWN

A083. *All 12 defences fell to adaptive attacks* .
    Sources: NAS

A084. *A guardrail library disappeared under its users* .
    Sources: LLG

A085. *The official page lagged the official release* .
    Sources: OW6, OWP

A086. If you do run it, start with the 22M model on your own harmless text, and remember the 512-token window .
    Sources: HFG, PG2

A087. - *"A good system prompt stops injection."* OWASP calls a constraining system prompt a partial control; adaptive attacks beat prompting defences such as spotlighting and sandwiching above 95% .
    Sources: NAS, OW6

A088. - *"An injection classifier makes it safe."* Published classifiers fell to adaptive attacks above 90%, and at realistic attack rates most of their flags are false alarms .
    Sources: NAS

A089. - *"If the model can't send email, data can't leave."* A rendered image URL is enough (Section 3.3) .
    Sources: OW6

A090. - *"Running locally makes it HIPAA compliant."* The Security Rule covers stored data and requires safeguards whatever the network does .
    Sources: HHS

A091. - *"Redaction removed the personal data."* Patterns miss names and addresses, and even Presidio says it can't guarantee finding everything .
    Sources: PRS

A092. It can still post something embarrassing, which is why the rule is a floor, not a complete defence .
    Sources: OW6, RO2

A093. *Answers.* (1) No reliable prevention mechanism exists today; defence is architectural: assume the instruction boundary will be bypassed and limit what the model can do and reach .
    Sources: OW6

A094. (2) Untrusted input, access to sensitive data, and changing state or communicating externally .
    Sources: RO2

A095. (3) Browsers treat the backslash as a slash and would go to a different host; parsers that disagree defeat allowlists .
    Sources: WHW

A096. (4) It was measured on Meta's own in-house set, on output filtering in English; your attack rate changes its precision; an independent test found it missed far more; and attackers can tune against it .
    Sources: LG4, NAS, PWC

A097. (5) No; the Security Rule covers stored ePHI and requires administrative, physical and technical safeguards, starting with a risk analysis .
    Sources: HHS

A098. **Best next resources** (checked to exist on October 15, 2026): OWASP's 2026 list in its GitHub repository and its agentic list ;
    Sources: ASI, OW6

A099. Nasr et al. and CaMeL ;
    Sources: CAM, NAS

A100. Meta's Rule of Two ;
    Sources: RO2

A101. Presidio's repository ;
    Sources: PRS

A102. HHS's Security Rule summary and cloud guidance .
    Sources: HHC, HHS


# Sources

- ABA: Anthropic, "API and data retention" (https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) and Privacy Center, "I need to be HIPAA compliant, can I use Claude?" (https://privacy.claude.com/en/articles/8956058) [class OD]
- ADJ: Debenedetti et al., "AgentDojo", arXiv 2406.13352v3; ethz-spylab/agentdojo README (NeurIPS 2024 Datasets and Benchmarks, per its BibTeX); PyPI [class PR]
- AJB: Anthropic docs, "Mitigate jailbreaks and prompt injections". https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks [class OD]
- ASI: OWASP, "OWASP Top 10 for Agentic Applications for 2026", December 9, 2025 (announcement post and resource page); the 2026 LLM list's mapping file `2026/final/mappings/asi-2026.json` [class SB]
- ATL: MITRE ATLAS, mitre-atlas/atlas-data, `dist/ATLAS.yaml`, data release v2026.09 [class SB]
- CAM: Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL), arXiv 2503.18813v2 [class PP]
- EUA: Regulation (EU) 2024/1689, Articles 50, 111 and 113, consolidated as of July 27, 2026, read via the European Commission's AI Act Service Desk. https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113 [class SB]
- FTC: FTC, "Complying with FTC's Health Breach Notification Rule" (July 2024; page modified July 14, 2026) [class SB]
- GAR: garak 0.17.0 wheel: README (METADATA), `evaluators/base.py`, `generators/`, `detectors/agent_breaker.py`; licence file [class OD]
- GOS: openai/gpt-oss repository: LICENSE, USAGE_POLICY, README [class OD]
- GRE: Greshake et al., "Not what you've signed up for", AISec 2023, pp. 79 to 90, doi:10.1145/3605764.3623985; arXiv 2302.12173 [class PR]
- GWS: Google Workspace, "Indirect prompt injections and Google's layered defense strategy for Gemini", updated October 13, 2026 [class OD]
- HFG: Hugging Face model page, meta-llama/Llama-Prompt-Guard-2-86M [class OD]
- HHA: HHS, "The access right, health apps, and APIs", last reviewed May 30, 2025 [class SB]
- HHC: HHS, "Guidance on HIPAA & Cloud Computing", last reviewed December 23, 2022 [class SB]
- HHS: HHS, "Summary of the HIPAA Security Rule", last reviewed August 7, 2026. https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html [class SB]
- IHR: Wallace et al., "The Instruction Hierarchy", arXiv 2404.13208 [class PP]
- LES: Lester et al., "The Power of Scale for Parameter-Efficient Prompt Tuning", arXiv 2104.08691 [class PP]
- LFW: meta-llama/PurpleLlama, `LlamaFirewall/` at commit d934ea2: README, `scanners/`, `promptguard_utils.py`, LICENSE; PyPI [class OD]
- LG3: Llama Guard 3 8B and 1B model cards and LICENSE files, PurpleLlama at d934ea2 [class OD]
- LG4: Llama Guard 4 12B model card and LICENSE, PurpleLlama at d934ea2 [class OD]
- LGP: Meta, Llama Guard 4 prompt-format page (dev.meta.ai); llama-cookbook `llama_guard` README and notebook [class OD]
- LLG: protectai/llm-guard, commit 168c103 "Archiving Project", July 8, 2026; PyPI [class OD]
- LLM: meta-llama/llama-models at commit 0e0b8c5: `models/llama3/LICENSE`, `llama3_1/LICENSE`, `llama3_2/USE_POLICY.md`, `llama4/LICENSE`, `llama4/USE_POLICY.md` [class OD]
- LTF: Willison, "The lethal trifecta for AI agents", June 16, 2025. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ [class PB]
- MCP: Model Context Protocol specification 2026-07-28, "Security and Trust & Safety" and tools page (modelcontextprotocol repository) [class OD]
- NAS: Nasr et al., "The Attacker Moves Second", arXiv 2510.09023v1 (October 10, 2025): abstract, Section 5, Table 1 [class PP]
- NCS: UK NCSC, "Prompt injection is not SQL injection (it may be worse)", December 8, 2025 [class SB]
- NEM: nemoguardrails 0.24.1 wheel: README (METADATA), `telemetry.py`, `rails/llm/config.py`, `library/*/actions.py`, `library/llama_guard/` [class OD]
- NIS: NIST AI 600-1, Generative AI Profile, July 2024, Section 2.9 and MS-2.7-007. doi:10.6028/NIST.AI.600-1 [class SB]
- OAG: OpenAI docs, "Safety in building agents". https://developers.openai.com/api/docs/guides/agent-builder-safety [class OD]
- OW5: OWASP Top 10 for LLM Applications 2025, `2_0_vulns/` in OWASP/www-project-top-10-for-large-language-model-applications [class SB]
- OW6: OWASP Top 10 for LLM Applications 2026, GenAI-Security-Project/GenAI-LLM-Top10 at commit 9253e38: CITATION.cff, `2026/README.md`, `2026/final/LLM01`, `LLM03`, `LLM08` [class SB]
- OWP: OWASP GenAI pages: the list page https://genai.owasp.org/llm-top-10/ (still 2025 on October 15, 2026), the 2026 resource page (August 3), the announcement post (September 1, 2026) [class SB]
- OYD: OpenAI docs, "Data controls in the OpenAI platform". https://developers.openai.com/api/docs/guides/your-data [class OD]
- PG2: Llama Prompt Guard 2 86M and 22M model cards and LICENSE, PurpleLlama at d934ea2 [class OD]
- PRG: Narisetty et al., "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents", arXiv 2606.26479v1 [class PP]
- PRS: microsoft/presidio at its October 8, 2026 head: README, `conf/default.yaml`, `default_recognizers.yaml`, `presidio_anonymizer/operators/`; presidio-analyzer 2.2.364 as installed and run [class OD]
- PWC: Jeon et al. (PwC), "Do Encoders Suffice?", arXiv 2606.25782v1: Sections 2.3, 6.1, 6.3, Appendices A and B [class PP]
- QWN: QwenLM/Qwen3 README, "License Agreement" (January 9, 2026) [class OD]
- RO2: Meta AI, "Agents Rule of Two: A Practical Approach to AI Agent Security", October 31, 2025. https://ai.meta.com/blog/practical-ai-agent-security/ [class VB]
- SPT: Hines et al., "Defending Against Indirect Prompt Injection Attacks With Spotlighting", arXiv 2403.14720 [class PP]
- SPX: spdx/license-list-data at commit 31ba1a5, `json/licenses.json`, version 3.29.0 (September 16, 2026) [class SB]
- WEI: Wei et al., "Jailbroken: How Does LLM Safety Training Fail?", arXiv 2307.02483 [class PP]
- WHW: WHATWG URL Standard, validation error "invalid-reverse-solidus" (last updated October 7, 2026). https://url.spec.whatwg.org/ [class SB]

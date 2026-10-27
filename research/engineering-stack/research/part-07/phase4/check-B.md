# Source check, set B (claims B001-B099)
B001 | SUPPORTED | evidence: LF press release dated Dec. 9, 2025: "Donating MCP to the Linux Foundation as part of the AAIF"; MCP 2026-07-28 tag exists in modelcontextprotocol repo | none
B002 | SUPPORTED | evidence: A2A CHANGELOG "1.0.1 ... (2026-05-26)", "1.0.0 ... (2026-03-12)"; LF press release June 23, 2025; docs/blog/posts/a2a-joins-aaif.md dated 2026-08-27 "accepted as a Growth Stage project" | none
B003 | SUPPORTED | evidence: LF AI & Data post Aug 29, 2025: "ACP is officially merging with the A2A under the Linux Foundation"; i-am-bee/acp README: "ACP is now part of A2A under the Linux Foundation!" | The quoted phrase is a substring of the post sentence; fine. The A2A docs/index.md line "IBM ACP: Incorporated into the A2A Protocol" was not found in a2a main (only a link in docs/partners.md), but the claim does not depend on it
B004 | SUPPORTED | evidence: ag-ui DEPRECATIONS.md "shipped in 1.0, released on 2026-09-17"; LICENSE "MIT License"; README MIT badge points at copilotkit/copilotkit | "Started by CopilotKit" is only indirectly shown (docs/introduction.mdx: "AG-UI was born from CopilotKit's initial partnership with LangChain and CrewAI")
B005 | PARTLY | evidence: AP2 docs/index.md: "available as an extension for the open-source Agent2Agent (A2A) protocol and Universal Commerce Protocol"; docs/index.md line 190 and faq.md: "The core specification work will continue in FIDO"; spec title "Agentic Payment Protocol (v0.2)"; CHANGELOG 0.2.0 | "Google project" is incomplete: the repo says standardization of the spec continues in FIDO Alliance working groups (AP2 v0.2 Release and FIDO Alliance Donation). Also the extension quote omits that it is equally an extension for UCP
B006 | SUPPORTED | evidence: ANP README table: "Released v1.2" for ANP-02, 03, 04, 07, 08; "based on W3C DID"; LICENSE Apache-2.0; "Repository copyright notices identify ANP Community" | none
B007 | NOT CHECKABLE | evidence: claim text is only a heading ("A2A in more detail") | not a factual claim
B008 | SUPPORTED | evidence: PyPI a2a-sdk version 1.2.2, license_expression Apache-2.0, author_email "Google LLC" | none
B009 | SUPPORTED | evidence: a2a.proto: "// Represents a distinct capability or function that an agent can perform." message AgentSkill | The quote in the claim is a fragment of that comment; matches
B010 | PARTLY | evidence: A2A docs/specification.md Appendix B: "A2A and MCP are complementary protocols"; MCP 2026-07-28 spec text has no mention of A2A (grep of specification/2026-07-28 found none) | "both specs call them complementary" is only verified for the A2A spec; the MCP spec does not say it. Cited source key A2S covers only A2A
B011 | SUPPORTED | evidence: LF press June 23, 2025 ("created by Google"); GOVERNANCE.md: "The Committee has eight seats, each held by the following companies" (Google, Microsoft, Cisco, AWS, Salesforce, ServiceNow, SAP, IBM) | Governance is a technical steering committee of eight companies; claim says "steering committee", fine
B012 | SUPPORTED | evidence: aaif.io/projects lists Model Context Protocol, goose, AGENTS.md, agentgateway, Agent2Agent (A2A), Agent Router; no AG-UI, AP2 or Agent Skills | none
B013 | SUPPORTED | evidence: agents.md README: "AGENTS.md is a simple, open format for guiding coding agents"; "Think of AGENTS.md as a README for agents"; AboutSection.tsx: "AGENTS.md is now stewarded by the" Agentic AI Foundation | none
B014 | NOT CHECKABLE | evidence: claim text is only a heading ("The format") | not a factual claim
B015 | SUPPORTED | evidence: specification.mdx: "Metadata (~100 tokens)", "Instructions (< 5000 tokens recommended)", "Resources (as needed)", "Keep your main `SKILL.md` under 500 lines" | none
B016 | SUPPORTED | evidence: Claude API Skills overview: name "Cannot contain reserved words: "anthropic", "claude""; name and description "Cannot contain XML tags" | none
B017 | SUPPORTED | evidence: Help Center article 12512198: "(200 characters maximum)" for the description | none
B018 | SUPPORTED | evidence: learn.chatgpt.com build-skills: "Skills build on the open agent skills standard", Codex checks `.agents/skills`; GitHub Docs: "(`.github/skills`, `.claude/skills`, or `.agents/skills`)"; Gemini CLI: "Based on the Agent Skills open standard"; Cursor: "Agent Skills is an open standard for extending AI agents" | none
B019 | SUPPORTED | evidence: agentskills repo docs/snippets/clients.jsx has 46 entries (46 lines matching `^    name:`) at commit 69ef37e | I counted entries by pattern; no duplicates seen
B020 | SUPPORTED | evidence: SEP-2640: "each file in a skill directory is exposed as an MCP resource, conventionally under the `skill://` URI scheme"; format "delegated entirely to the Agent Skills specification"; extensions/skills/overview.mdx names `io.modelcontextprotocol/skills` | none
B021 | SUPPORTED | evidence: skills-over-mcp working-group page: "SEP-2640 is Final, merged on September 13, 2026"; overview.mdx: "SDK and host support is still being implemented"; 2026-07-28 to 2026-09-13 = 47 days | none
B022 | SUPPORTED | evidence: python-sdk v2.3.0 examples/stories/skills/README.md: "Status: not yet implemented (#2896)"; no skills module found in src | none
B023 | SUPPORTED | evidence: Invariant post dated April 1, 2025; both quotes found verbatim | none
B024 | SUPPORTED | evidence: "Clients should pin the version of the MCP server and its tools to prevent unauthorized changes" | none
B025 | SUPPORTED | evidence: arXiv 2508.14925v2: 45 live servers, 353 tools, 1,348 malicious cases, 20 agents, o1-mini 72.8%, "more capable models are often more susceptible" | none
B026 | SUPPORTED | evidence: arXiv 2508.13220v3: 17 distinct attack types, four surfaces, protections "largely ineffective ... average success rate of less than 30%" | none
B027 | SUPPORTED | evidence: arXiv 2506.13538v5: 1,899 servers; 7.2% general vulnerabilities; 5.5% tool poisoning; 7.2% x 1899 = 137, 5.5% x 1899 = 104 | Method is a hybrid of a general static analysis tool plus an MCP-specific scanner; "static analysis" is a fair short form
B028 | SUPPORTED | evidence: arXiv 2601.10338v1: 31,132 skills analyzed, two marketplaces, 26.1%, OR 2.12, precision 86.7% | 26.1% x 31,132 = 8,126 (claim says about 8,125; fine)
B029 | SUPPORTED | evidence: Snyk PDF (Feb 5, 2026): "3,984 AI agent skills ... 76 confirmed malicious payloads"; 76/3984 = 1.91 per 100 | "a vendor that sells a scanner" is a characterization not stated in the PDF
B030 | SUPPORTED | evidence: NVD CVE-2025-6514: "mcp-remote is exposed to OS command injection when connecting to untrusted MCP servers"; JFrog CNA 9.6 CRITICAL CVSS 3.1; NIST N/A; JFrog range 0.0.5 to 0.1.15. mcp-remote git: fix commit 607b226 (2025-06-17), first tag containing it v0.1.16; npm 0.1.16 published 2025-06-17 | none
B031 | SUPPORTED | evidence: NVD CVE-2025-49596: GitHub CNA 9.4 CVSS 4.0; no 3.x score; affected "< 0.14.1"; description "lack of authentication between the Inspector client and proxy" (the tail "allowing unauthenticated requests to launch MCP commands over stdio" was not shown in the fetch summary but matches the CVE text as I know it) | Tail of the quote not independently seen in the fetch output
B032 | SUPPORTED | evidence: OWASP LLM06:2025 Excessive Agency: "excessive functionality", "excessive permissions", "excessive autonomy"; "Limit the extensions that LLM agents are allowed to call to only the minimum necessary" | none
B033 | SUPPORTED | evidence: OWASP resource page: title "OWASP Top 10 for Agentic Applications for 2026", date December 9, 2025, page does not list the ten items | none
B034 | SUPPORTED | evidence: Anthropic post (Nov 24, 2025): "That's 58 tools consuming approximately 55K tokens before the conversation even starts" (GitHub 35, Slack 11, Sentry 5, Grafana 5, Splunk 2); "we've seen tool definitions consume 134K tokens before optimization"; 55,000/58 = 948 | none
B035 | SUPPORTED | evidence: OpenAI: "Aim for fewer than 20 functions available at the start of a turn at any one time, though this is just a soft suggestion." | none
B036 | SUPPORTED | evidence: arXiv 2505.03275v1: "43.13% vs 13.62%", "by over 50%" | 3.17x is the claim writer's own ratio (43.13/13.62); the paper says "more than triples"
B037 | SUPPORTED | evidence: Anthropic post: Opus 4 49% to 74%, Opus 4.5 79.5% to 88.1%, "Internal testing ... MCP evaluations"; differences 25 and 8.6 | none
B038 | SUPPORTED | evidence: arXiv 2506.01056v4: 2,797 tools from 308 servers; "98% reduction in token consumption on APIBank" | none
B039 | PARTLY | evidence: arXiv 2411.15399v1: "selectively reducing the number of tools available to LLMs significantly improves their function-calling performance", on edge hardware | The abstract does not say "small models"; it says LLMs on edge devices
B040 | SUPPORTED | evidence: PMLR 267:48371-48392, ICML 2025: "state-of-the-art LLMs excel at singleturn calls"; "memory, dynamic decision-making, and long-horizon reasoning remain open challenges"; "evaluates serial and parallel function calls" | Source spells "singleturn" without hyphen, same as the claim
B041 | SUPPORTED | evidence: gorilla BFCL CHANGELOG "[Jul 17, 2025] BFCL V4 release"; weighting table row "Agentic | 0 | **40**" | none
B042 | SUPPORTED | evidence: 2026-07-28 changelog items 1-2: removes sessions and `Mcp-Session-Id`, removes `initialize` handshake; every request carries `io.modelcontextprotocol/protocolVersion` and `clientCapabilities` | none
B043 | SUPPORTED | evidence: changelog item 7 and mrtr.mdx: servers return `InputRequiredResult` (`resultType: "input_required"`); clients retry with `inputResponses` | none
B044 | SUPPORTED | evidence: deprecated.mdx: Roots and Sampling deprecated in `2026-07-28`, earliest removal "First revision released on or after 2027-07-28" | none
B045 | SUPPORTED | evidence: deprecated.mdx lists HTTP+SSE transport as Deprecated, "No features have been removed"; streamable-http.mdx: "Content-Type: text/event-stream (an SSE response stream)" | none
B046 | SUPPORTED | evidence: python-sdk docs/migration.md: "`FastMCP` renamed to `MCPServer`", "ModuleNotFoundError: No module named 'mcp.server.fastmcp'" | none
B047 | SUPPORTED | evidence: TS SDK v1.x README: "implements the MCP spec up to 2025-11-25 ... 2026-07-28 ... is in v2"; npm `@modelcontextprotocol/sdk` 1.32.1, `/server` and `/client` 2.3.1 | none
B048 | SUPPORTED | evidence: LF press Dec 9, 2025: "Donating MCP to the Linux Foundation as part of the AAIF" | none
B049 | SUPPORTED | evidence: tools.mdx: "clients MUST consider tool annotations to be untrusted unless they come from trusted servers" | none
B050 | SUPPORTED | evidence: tools.mdx error example for unknown tool: code -32602 "Unknown tool: invalid_tool_name"; python-sdk v2.3.0 exceptions.py: "The SDK raises [ToolError] too, for an unknown tool name"; docs/handlers/context.md: "the result is an error the model can read" | none
B051 | SUPPORTED | evidence: A2A v0.2.6 spec: `/.well-known/agent.json`; v0.3.0 CHANGELOG: "Change Well-Known URI for Agent Card hosting from `agent.json` to `agent-card.json`" | none
B052 | SUPPORTED | evidence: LF press June 23, 2025; A2A blog dated 2026-08-27 "accepted as a Growth Stage project at the Agentic AI Foundation" | none
B053 | SUPPORTED | evidence: LF AI & Data post Aug 29, 2025 "ACP is officially merging with the A2A"; ACP README "ACP is now part of A2A" | none
B054 | SUPPORTED | evidence: spec: description "Max 1024 characters"; Help Center "(200 characters maximum)" | none
B055 | SUPPORTED | evidence: spec name rules list no reserved words; Claude API docs: "Cannot contain reserved words: "anthropic", "claude"" | none
B056 | SUPPORTED | evidence: spec: "pre-approved tools the skill may use. (Experimental)"; "Support for this field may vary between agent implementations" | none
B057 | SUPPORTED | evidence: OpenAI "fewer than 20 ... soft suggestion"; Anthropic tool search gains; RAG-MCP 13.62% to 43.13% | none
B058 | SUPPORTED | evidence: NVD CVE-2025-6514 description and mcp-remote fix commit 607b226 | Heading-style caption, backed by the cited sources
B059 | SUPPORTED | evidence: npm time: 0.1.16 published 2025-06-17; `npm view mcp-remote version` = 0.15.0 | none
B060 | SUPPORTED | evidence: Anthropic post: 55K tokens before the conversation starts | Caption-style claim, consistent with source
B061 | SUPPORTED | evidence: A2A v0.2.6 `agent.json` vs v0.3.0 `agent-card.json` | Caption-style claim, consistent with source
B062 | SUPPORTED | evidence: git ls-remote tags include 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28; npm and PyPI queried today | The tag list also has 2024-10-07, 2024-11-05-final and -RC tags; claim lists only the released revisions
B063 | SUPPORTED | evidence: PyPI mcp 2.3.0, MIT, requires_python >=3.10, upload 2026-10-02T22:06:52 | Python SDK main already requires >=3.11 (pyproject on main); the claim's 3.10 matches the 2.3.0 release
B064 | SUPPORTED | evidence: npm `@modelcontextprotocol/server` and `/client`: 2.3.1, Apache-2.0, node >=20 | none
B065 | SUPPORTED | evidence: npm `@modelcontextprotocol/sdk` 1.32.1, MIT, node >=18; v1.x README "maintenance line", bug fixes and security updates | none
B066 | SUPPORTED | evidence: Inspector LICENSE: "licensing transition from the MIT License to ... Apache-2.0"; README "Requires Node >=22.19.0"; npm 2.11.0 | none
B067 | SUPPORTED | evidence: skills-ref/pyproject.toml `license = "Apache-2.0"`; repo README: code Apache 2.0, docs CC-BY-4.0 | none
B068 | SUPPORTED | evidence: python-sdk v2.3.0 migration.md: "`Client` ... accepts a `Server` or `MCPServer` instance directly" (in-process); README lists stdio transport | Recommendation; the factual parts check out
B069 | NOT CHECKABLE | evidence: advice, not a factual claim | none
B070 | SUPPORTED | evidence: authorization-server-discovery.mdx: servers MUST implement Protected Resource Metadata (RFC9728); authorization index lists Resource Indicators; security best practices has "Token Passthrough" as an anti-pattern; streamable-http: servers MUST validate `Origin`; changelog removes sessions | none
B071 | SUPPORTED | evidence: TS v1.x README says 2026-07-28 support is in v2 | Recommendation consistent with source
B072 | SUPPORTED | evidence: Claude API MCP connector page: "The MCP connector is not covered by ZDR arrangements" | The other "when not to use" items are advice
B073 | SUPPORTED | evidence: OpenAI function-calling guide exists; PyPI `fastmcp` 4.1.0 | "more built in than the official SDK" is opinion, not verified
B074 | SUPPORTED | evidence: Claude Code MCP docs: "claude mcp add [options] <name> -- <command> [args...]", python example with `--` | none
B075 | PARTLY | evidence: Claude Code MCP docs: "v2 runtime (MCP TypeScript SDK 2.0), which adds MCP protocol revision 2026-07-28" | The statement that the lab server refuses older handshakes and that older hosts fail is about the project's own lab server; not in the cited source. Claude Code docs also mention a `MCP_PROTOCOL_NEGOTIATION` legacy mode
B076 | PARTLY | evidence: 2026-07-28 architecture: "client-host-server architecture", host mediates "User- or model-initiated action" | No sentence says "the model never talks to a server"; it is an inference from the architecture
B077 | SUPPORTED | evidence: tools.mdx: annotations "untrusted unless they come from trusted servers" | none
B078 | SUPPORTED | evidence: mcp-remote is a local bridge process; MCP Inspector is "a developer tool for testing and debugging MCP servers" (NVD) | Locality is inferred from what the tools are; sources do not use the phrase
B079 | SUPPORTED | evidence: Invariant: rug pull "change the tool description after the client has already approved it"; advice to pin | none
B080 | SUPPORTED | evidence: A2A spec Appendix B "complementary protocols designed for different aspects" | none
B081 | SUPPORTED | evidence: tools.mdx: "Tool Execution Errors contain actionable feedback that language models can use to self-correct", reported "with `isError: true`" | none
B082 | SUPPORTED | evidence: spec: name "May only contain unicode lowercase alphanumeric characters and hyphens"; "Must match the parent directory name" | Whether the field in the lab was named with underscores is outside the source
B083 | SUPPORTED | evidence: changelog item 2: `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientCapabilities` | none
B084 | SUPPORTED | evidence: changelog Deprecated: Roots, Sampling, Logging, HTTP+SSE, Dynamic Client Registration; Major changes: `initialize` handshake, sessions, `ping` removed | none
B085 | SUPPORTED | evidence: mrtr.mdx diagram: retry is `tools/call (id: 2, ElicitResult, requestState)`; "client MUST echo back the exact value" of `requestState` | none
B086 | SUPPORTED | evidence: A2A spec: `GET /.well-known/agent-card.json` | none
B087 | SUPPORTED | evidence: 2026-07-28 changelog and docs/2026-07-28/tutorials/security/security_best_practices.mdx exist | none
B088 | SUPPORTED | evidence: python-sdk docs/migration.md exists at v2.3.0 | none
B089 | SUPPORTED | evidence: A2A tag v1.0.1 exists (commit 3303592); CHANGELOG 1.0.1 | none
B090 | SUPPORTED | evidence: agentskills.io specification (docs/specification.mdx) | The project file claude/agent-skills-reference-v1-2.md is not a cited source and was not checked
B091 | SUPPORTED | evidence: Invariant post of April 1, 2025 on tool poisoning | none
B092 | SUPPORTED | evidence: index.mdx: extensions "negotiated during initialization"; basic/index.mdx: "Client Features: Elicitation, sampling and root directory lists provided by clients" | none
B093 | SUPPORTED | evidence: TS v1.x README (up to 2025-11-25); python-sdk migration.md "This SDK does not implement the extension yet" (Tasks); extensions/skills/overview.mdx "still being implemented"; python-genai and js-genai READMEs "Model Context Protocol (MCP) support (experimental)"; registry README and docs "currently in preview" | none
B094 | SUPPORTED | evidence: all seven are arXiv preprints / vendor PDF; Snyk is the vendor; detector precision 86.7% noted in SIW | "2025-era models" not independently checked per paper
B095 | SUPPORTED | evidence: sources are OpenAI guide, Anthropic engineering post, arXiv preprint RAG-MCP | The negative ("no peer-reviewed study read here") cannot be proved from sources, but is consistent
B096 | SUPPORTED | evidence: "The MCP connector is not covered by ZDR arrangements. Data exchanged with MCP servers ... is retained according to Anthropic's standard data retention policy." | none
B097 | SUPPORTED | evidence: LF press Dec 9, 2025; changelog removes handshake and sessions | none
B098 | SUPPORTED | evidence: spec table: "pre-approved tools the skill may use. (Experimental)"; "Support for this field may vary between agent implementations" | The quoted "may vary between agent implementations" matches; "pre-approved tools the skill may use" matches the table row
B099 | SUPPORTED | evidence: spec "Max 1024 characters"; Help Center "(200 characters maximum)" | The project-instructions side was not checked here
## Summary
Counts: SUPPORTED 91, PARTLY 5, CONTRADICTED 0, NOT CHECKABLE 3 (total 99).
PARTLY: B005, B010, B039, B075, B076. NOT CHECKABLE: B007, B014, B069.
Five most important problems:
1. B005: AP2 is described as a "Google project", but the repo says core spec work moves to FIDO (donation announced with v0.2). Needs a qualifier.
2. B010: "both specs call them complementary" is true only for A2A; the MCP 2026-07-28 spec never mentions A2A.
3. B075: the lab-server behavior (refuses older handshakes, older hosts fail) is the project's own, not from Claude Code docs; the Claude Code v2 runtime point is correct.
4. B039: Less is More says LLMs on edge devices, not "small models".
5. B076: "The model never talks to a server" is an inference from the client-host-server architecture, not a sentence in the spec.
Minor: B004 "started by CopilotKit" only indirect; B031 quote tail not seen in fetch output; B003 A2A docs/index.md "IBM ACP: Incorporated" line not found on main (claim still holds via the other two sources); B062 tag list also has RC and extra tags; B090 and B099 reference project files not checked.
Lookups used: 28 WebFetch (7 arXiv, 7 vendor/NVD/OWASP pages, 14 other docs), 0 WebSearch. Everything else came from git clones (A2A, agentskills, ag-ui, AP2, ANP, ACP, agents.md, mcp-remote, MCP spec repo, python-sdk v2.3.0, typescript-sdk v1.x, inspector, registry, python-genai, js-genai, gorilla sparse, mcp-scan), PyPI JSON and npm view. Not fully fetched: the A2A v1.0.1 tag was checked via main at 7c861a5 plus tags v0.2.6, v0.3.0 and v1.0.1 existence; spec text read from main. Clones were first created in /home/claude/part07 by mistake (shell cwd) and moved at once into the scratchpad; none remain there.

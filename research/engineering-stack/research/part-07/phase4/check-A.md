# Source check, set A (claims A001-A110)
A001 | SUPPORTED | evidence: MSP index.mdx "uses JSON-RPC 2.0 messages ... Hosts: LLM applications that initiate connections; Clients: Connectors within the host; Servers: Services that provide context and capabilities"; server/index.mdx lists prompts, resources, tools | none
A002 | SUPPORTED | evidence: MCP blog 2025-12-09 "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation"; LF release dated Dec. 9, 2025 lists MCP as a founding contribution; spec dir 2024-11-05 is the oldest revision | Minor: git tag 2024-10-07 also exists (pre-release tag, no spec revision directory). "Directed fund" wording is in the MCP blog, not in the LF release
A003 | SUPPORTED | evidence: docs/specification.md section 3 (line 3600-3603) "A2A and MCP are complementary protocols"; "tools, APIs, data sources, and other external resources"; "communicate and collaborate with each other as peers" | none
A004 | SUPPORTED | evidence: agentskills.io overview "At startup, agents load only the name and description of each available skill"; "When a task matches a skill's description, the agent reads the full SKILL.md" | none
A005 | SUPPORTED | evidence: agentskills.io "originally developed by Anthropic, released as an open standard"; Codex page "Skills build on the open agent skills standard"; Cursor "an open standard"; Gemini CLI "Based on the Agent Skills open standard"; GitHub "open standard", works with Copilot cloud agent, CLI, VS Code agent mode | GitHub page did not mention the SKILL.md filename (fetch summary); not material
A006 | SUPPORTED | evidence: AAT "That's 58 tools consuming approximately 55K tokens before the conversation even starts"; five servers listed (GitHub 35, Slack 11, Sentry 5, Grafana 5, Splunk 2) | none
A007 | SUPPORTED | evidence: INV post describes hidden instructions in tool descriptions; NVD CVE-2025-49596 (MCP Inspector RCE, CVSS 4.0 9.4 Critical) and CVE-2025-6514 (mcp-remote OS command injection, CVSS 9.6) | none
A008 | PARTLY | evidence: MSP index.mdx describes the protocol but never says "current"; tag list shows 2026-07-28 as the newest dated revision | "is current" is not in the cited MSP key (it rests on MGT)
A009 | SUPPORTED | evidence: MAR "Each client is created by the host and communicates with exactly one server" | The claim's quote "Each client ... communicates with exactly one server" uses an ellipsis correctly
A010 | SUPPORTED | evidence: MBP "Requests MUST include a string or integer ID"; "Result responses MUST include a result field"; error responses include error field | none
A011 | SUPPORTED | evidence: MSP server/index.mdx control table: Prompts "User-controlled", Resources "Application-controlled", Tools "Model-controlled" | none
A012 | SUPPORTED | evidence: MCL major change 2 "Every request now carries its protocol version and client capabilities in _meta" | none
A013 | SUPPORTED | evidence: MDI "Servers MUST implement it" | none
A014 | SUPPORTED | evidence: MCL "Every request now carries its protocol version and client capabilities in _meta"; MAR "declare their supported features on each request" | none
A015 | SUPPORTED | evidence: MCL item 7 "Multi Round-Trip Requests (MRTR) pattern introduced which replaces the previous approach of sending server-initiated requests"; resultType "input_required" | none
A016 | SUPPORTED | evidence: MSP index.mdx "Clients may offer the following features to servers: Elicitation: Server-initiated requests for additional information from users" (only one listed) | none
A017 | SUPPORTED | evidence: MDP registry rows Roots and Sampling, "Deprecated in 2026-07-28" | none
A018 | SUPPORTED | evidence: MST "Messages are delimited by newlines, and MUST NOT contain embedded newlines"; "one message per line" | none
A019 | SUPPORTED | evidence: MTR "Streamable HTTP: each message is an HTTP POST to a single MCP endpoint"; MSH "sends every JSON-RPC request or notification as its own HTTP POST" | none
A020 | SUPPORTED | evidence: MTO "clients MUST consider tool annotations to be untrusted unless they come from trusted servers" | none
A021 | SUPPORTED | evidence: MTO Error Handling "Tool Execution Errors ... reported in tool results with isError: true"; protocol errors are the other kind | none
A022 | SUPPORTED | evidence: MSP "Extensions are always opt-in and require explicit support from both client and server"; names Tasks, Skills over MCP, MCP Apps; SEP-2640 extension id io.modelcontextprotocol/skills | none
A023 | SUPPORTED | evidence: MAU "Implementations using an HTTP-based transport SHOULD conform ... STDIO transport SHOULD NOT follow this specification"; "OAuth 2.1 resource server" | none
A024 | SUPPORTED | evidence: A2A repo tag v1.0.1, commit 3303592 (git clone --branch v1.0.1) | none
A025 | SUPPORTED | evidence: specification.md section 8 "https://{server_domain}/.well-known/agent-card.json"; IANA registration "URI suffix: agent-card.json" | none
A026 | SUPPORTED | evidence: agentskills.io "a skill is a folder containing a SKILL.md file ... scripts, reference materials" | none
A027 | SUPPORTED | evidence: agentskills.io specification "Progressive disclosure: Metadata (~100 tokens): name and description loaded at startup ... full SKILL.md loaded when activated" | none
A028 | SUPPORTED | evidence: agents.md "A simple, open format for guiding coding agents"; FAQ "just standard Markdown" | Site says "standard Markdown", not "plain"; trivial
A029 | SUPPORTED | evidence: INV post title and body "Tool Poisoning Attacks": tool description contains hidden instructions | Post gives no formal definition, only examples
A030 | SUPPORTED | evidence: INV "MCP Rug Pull ... a malicious server can change the tool description after the client has already approved it" | none
A031 | PARTLY | evidence: MAU security-considerations "Confused Deputy Problem: Attackers can exploit MCP servers acting as intermediaries to third-party APIs ... obtain access tokens without user consent" | The general definition given is not in MAU; the source only describes the MCP proxy case
A032 | SUPPORTED | evidence: OFC five-step flow: step 3 "Execute code on the application side with input from the tool call"; step 5 "Receive a final response from the model (or more tool calls)" | none
A033 | PARTLY | evidence: MSP and MAR say the host coordinates AI/LLM integration and enforces boundaries ("Full conversation history stays with the host") | The exact statement "the model never talks to an MCP server directly" is an inference, not stated
A034 | SUPPORTED | evidence: MAR Host, Clients, Servers sections; MSP Hosts/Clients/Servers | none
A035 | SUPPORTED | evidence: MAR design principle 3 "Servers should not be able to read the whole conversation, nor "see into" other servers" | none
A036 | SUPPORTED | evidence: MSP server/index.mdx three primitives with Control column | none
A037 | SUPPORTED | evidence: MSP index.mdx lists only Elicitation under client features | none
A038 | SUPPORTED | evidence: MDP Roots and Sampling rows, Deprecated in 2026-07-28 | none
A039 | SUPPORTED | evidence: MBP basic/index.mdx "Client Features: Elicitation, sampling and root directory lists provided by clients" | none
A040 | SUPPORTED | evidence: MBP request has jsonrpc, id, method, params; results/errors carry same ID | none
A041 | SUPPORTED | evidence: MBP "Unlike base JSON-RPC, the ID MUST NOT be null" | none
A042 | SUPPORTED | evidence: MCP blog 2025-12-09 "a directed fund under the Linux Foundation, co-founded by Anthropic, Block and OpenAI"; LF release lists MCP (Anthropic), goose (Block), AGENTS.md (OpenAI, Aug 2025) | The exact quote "co-founded by" is in the MCP blog; the LF press release says "With founding contributions from Anthropic, Block, and OpenAI"
A043 | SUPPORTED | evidence: PyPI mcp 2.3.0 author "Model Context Protocol a Series of LF Projects, LLC."; same name in modelcontextprotocol GOVERNANCE.md | PyPI has trailing period; "legal home" comes from GOVERNANCE.md, not PYPI
A044 | SUPPORTED | evidence: docs/specification contains 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28; git ls-remote tags | ls-remote also shows 2024-10-07, 2024-11-05-final and -RC tags (not spec revisions)
A045 | SUPPORTED | evidence: MCL "Key Changes" page | none
A046 | SUPPORTED | evidence: MCL item 1 "Remove protocol-level sessions and the Mcp-Session-Id header from the Streamable HTTP transport"; "explicit, server-minted handles passed as ordinary tool arguments"; MTO create_basket / basket_id example | none
A047 | SUPPORTED | evidence: MDI "Servers MUST implement it"; MCL "Clients MAY call it before any other request"; result has supportedVersions, capabilities, serverInfo | none
A048 | SUPPORTED | evidence: MRT "Servers return an InputRequiredResult (resultType: "input_required") ... Clients ... retry" | none
A049 | SUPPORTED | evidence: MCL item 8 "Clients MUST treat results from earlier-protocol servers that omit the field as "complete"" | none
A050 | SUPPORTED | evidence: MCL item 5 "Log level is now set per-request via io.modelcontextprotocol/logLevel in _meta" | none
A051 | SUPPORTED | evidence: MDP "First revision released on or after 2027-07-28"; MCL "a minimum twelve-month deprecation window" | none
A052 | SUPPORTED | evidence: MDP migration paths: "Pass directories or files via tool parameters, resource URIs, or server configuration"; "Integrate directly with LLM provider APIs"; "Log to stderr ... use OpenTelemetry" | "resource addresses" is a paraphrase of "resource URIs"
A053 | SUPPORTED | evidence: MCL item 6 "official extension (io.modelcontextprotocol/tasks) ... replaces tasks/result with polling via tasks/get" | none
A054 | SUPPORTED | evidence: MCL minor 5 "Require ttlMs and cacheScope ... cacheScope ("public" or "private")"; schema.ts CacheableResult ttlMs: number; cacheScope | none
A055 | SUPPORTED | evidence: MTO "MUST NOT vary per-connection or as a side effect of other requests"; "SHOULD return tools in a deterministic order"; MCP blog "keep upstream prompt caches stable" | none
A056 | SUPPORTED | evidence: MBP Error Codes: -32021 MissingRequiredClientCapability, -32022 UnsupportedProtocolVersion, "-32020 to -32099 reserved"; "-32002 resource not found ... replaced by -32602" | none
A057 | SUPPORTED | evidence: MCL minor 10 "structuredContent to allow any JSON value"; MTO "This can be any JSON value" | none
A058 | SUPPORTED | evidence: docs/extensions/overview.mdx "Official extensions use the io.modelcontextprotocol vendor prefix" | none
A059 | SUPPORTED | evidence: MSP "Tasks; Skills over MCP; MCP Apps: Interactive UI elements (charts, forms, video players) rendered inline"; MVR example id io.modelcontextprotocol/ui | none
A060 | SUPPORTED | evidence: MSP "negotiated during initialization"; MVR "Extensions are advertised in the extensions field of capabilities" | The "left over" characterization is the author's inference, consistent with the changelog
A061 | SUPPORTED | evidence: MST Backward Compatibility "SHOULD probe with server/discover"; "The fallback MUST NOT be keyed to one specific error code" | none
A062 | PARTLY | evidence: PSD docs/whats-new.md "the same streamable_http_app() (and the same stdio server) answers a 2025-era client's initialize and a 2026-era client's requests" | The quote is spliced and not verbatim ("the same stdio server" sits in a parenthesis). The "researcher confirmed by sending a 2025-06-18 initialize" is not in any cited source
A063 | SUPPORTED | evidence: MTO Tool: name, title, description, icons, inputSchema, outputSchema, annotations | none
A064 | SUPPORTED | evidence: MTO "MUST be a valid JSON Schema object (not null)"; "Defaults to 2020-12"; "{ "type": "object", "additionalProperties": false } - Recommended" | none
A065 | SUPPORTED | evidence: MTO "SHOULD be between 1 and 128 characters"; allowed A-Z a-z 0-9 _ - . | none
A066 | SUPPORTED | evidence: MTO "a tool that returns structured content SHOULD also return the serialized JSON in a TextContent block" | none
A067 | SUPPORTED | evidence: MTO Output Schema "Servers MUST provide structured results that conform to this schema. Clients SHOULD validate" | none
A068 | SUPPORTED | evidence: MTO "unrelated to LLM "structured outputs" (schema-constrained model generation)" | none
A069 | SUPPORTED | evidence: MTO Error Handling "Tools use two error reporting mechanisms" | none
A070 | PARTLY | evidence: MTO lists "Input validation errors" under Tool Execution Errors; the date comes from 2025-11-25 changelog item 5 (SEP-1303) | The cited MTO does not say it moved in 2025-11-25; true per another file
A071 | SUPPORTED | evidence: MTO "clients MUST consider tool annotations to be untrusted unless they come from trusted servers"; schema.ts "Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers" | none
A072 | SUPPORTED | evidence: MTO "there SHOULD always be a human in the loop with the ability to deny tool invocations"; Security Considerations "Servers MUST: Validate all tool inputs, Implement proper access controls, Rate limit tool invocations, Sanitize tool outputs" | none
A073 | SUPPORTED | evidence: MTR lists stdio and Streamable HTTP as the standard bindings | none
A074 | SUPPORTED | evidence: MST rules (framing, stderr, no non-MCP stdout) | Not a factual claim beyond heading
A075 | SUPPORTED | evidence: MBP Auth "implementations using STDIO transport SHOULD NOT follow this specification, and instead retrieve credentials from the environment" | none
A076 | SUPPORTED | evidence: PSD docs/client/transports.md "The child does not inherit your environment. It gets a minimal allow-list (HOME, LOGNAME, ...)"; "env= adds to it" | none
A077 | PARTLY | evidence: quote "each message is an HTTP POST to a single MCP endpoint" is in MTR (transports/index.mdx); MSH says "Resumable SSE streams via Last-Event-ID are not supported"; removals of GET stream and sessions in MSH Info box and MCL | The first quote is from MTR, not from the cited MCL or MSH
A078 | SUPPORTED | evidence: MSH "Mcp-Method ... All requests"; "Mcp-Name ... tools/call, resources/read, prompts/get"; "These headers are REQUIRED for compliance" | none
A079 | SUPPORTED | evidence: MSH "Servers MUST validate the Origin header on all incoming connections to prevent DNS rebinding attacks"; "SHOULD bind only to localhost (127.0.0.1)" | none
A080 | SUPPORTED | evidence: MDP HTTP+SSE row "Deprecated in 2025-03-26 ... Three months after SEP-2596 reaches Final" | none
A081 | SUPPORTED | evidence: MSH "answers each request with either a single JSON object or a Server-Sent Events (SSE) stream" | none
A082 | SUPPORTED | evidence: MRT "without requiring a shared storage layer across server instances or requiring stateful load balancing" | Claim is a fragment; context not visible
A083 | SUPPORTED | evidence: MRT "MUST protect its integrity (e.g. HMAC or AEAD)" | Fragment
A084 | SUPPORTED | evidence: MRT "SHOULD include ... the authenticated principal ... a short expiry (TTL) ... an identifier for the originating request" | none
A085 | SUPPORTED | evidence: MRT "Servers MUST NOT send an inputRequests that the client has not declared support for"; MBP/schema.ts MissingRequiredClientCapability -32021 with data.requiredCapabilities | The -32021 link is in MBP and MSC, not in MRT itself
A086 | SUPPORTED | evidence: MAU "protected MCP server acts as an OAuth 2.1 resource server" | The "Sign in with ..." gloss is the author's, not in the source
A087 | SUPPORTED | evidence: MAU security-considerations "The MCP server MUST NOT pass through the token it received from the MCP client" | none
A088 | SUPPORTED | evidence: MBS Token Passthrough "Token passthrough is explicitly forbidden in the authorization specification" | none
A089 | SUPPORTED | evidence: MAU security-considerations "MCP proxy servers using static client IDs MUST obtain user consent for each dynamically registered client before forwarding" | none
A090 | SUPPORTED | evidence: MCL Deprecated item 4 (DCR in favor of Client ID Metadata Documents); minor 7 RFC 9207 iss validation | none
A091 | SUPPORTED | evidence: MBS "State Handle Hijacking ... MCP servers MUST NOT treat possession of a state handle as authentication"; points to old "Session Hijacking" section | none
A092 | SUPPORTED | evidence: MBS Local MCP Server Compromise "Show the exact command that will be executed, without truncation"; "Require explicit user approval" | none
A093 | SUPPORTED | evidence: PyPI mcp 2.3.0, uploaded 2026-10-02, license MIT, requires_python >=3.10 | none
A094 | SUPPORTED | evidence: PSD migration.md "The FastMCP class has been renamed to MCPServer"; "from mcp.server.mcpserver import MCPServer"; snake_case table inputSchema->input_schema, structuredContent->structured_content, isError->is_error; httpx replaced by httpx2 | none
A095 | SUPPORTED | evidence: PSD whats-new.md "Client takes a URL (Streamable HTTP), a StdioServerParameters (a stdio subprocess) ... or, in tests, the server object itself (in memory)" | none
A096 | SUPPORTED | evidence: PSD whats-new.md "which this SDK does not implement yet" (Tasks) | none
A097 | SUPPORTED | evidence: python-sdk main pyproject.toml requires-python ">=3.11"; v2.3.0 ">=3.10" | none
A098 | SUPPORTED | evidence: PyPI fastmcp 4.1.0 Apache-2.0, repo PrefectHQ/fastmcp; fastmcp-slim requires mcp>=2.0.0,<3.0.0 (client/server extras) | none
A099 | SUPPORTED | evidence: typescript-sdk v1.x README "Support for the 2026-07-28 spec is not planned for v1.x"; npm @modelcontextprotocol/sdk 1.32.1 | none
A100 | SUPPORTED | evidence: npm view @modelcontextprotocol/server and /client 2.3.1, license Apache-2.0, engines node >=20 | none
A101 | SUPPORTED | evidence: npm view @modelcontextprotocol/inspector 2.11.0, engines node >=22.19.0; README Web, CLI, TUI modes | Inspector LICENSE is a MIT-to-Apache transition notice; not claimed
A102 | SUPPORTED | evidence: NVD CVE-2025-49596 "Versions of MCP Inspector below 0.14.1 are vulnerable to remote code execution"; CVSS 4.0 9.4 Critical | none
A103 | SUPPORTED | evidence: MRG about.mdx "Breaking changes or data resets may occur before general availability"; registry README "API freeze (v0.1)" dated 2025-10-24 | none
A104 | SUPPORTED | evidence: MRG about.mdx "The MCP Registry does not support private servers" | none
A105 | SUPPORTED | evidence: CMC "supports both Streamable HTTP and SSE transports. Local STDIO servers cannot be connected directly"; "The MCP connector is not covered by ZDR arrangements"; "only tool calls are currently supported"; beta mcp-client-2025-11-20 | Page now also lists a newer header mcp-client-2026-09-15, so the table may be one step behind
A106 | SUPPORTED | evidence: CCM Options 1-4 HTTP, SSE ("deprecated"), stdio, WebSocket; "The v2 runtime is the same code on MCP TypeScript SDK 2.0, which adds MCP protocol revision 2026-07-28"; "Verify you trust each server before connecting it" | Last 16.7k characters of the page not read
A107 | SUPPORTED | evidence: OMC "By default, OpenAI will request your approval before any data is shared with a connector or remote MCP server"; "A malicious server can exfiltrate sensitive data from anything that enters the model's context"; mcp tool type | Quote is cut mid-sentence without an ellipsis
A108 | SUPPORTED | evidence: OAS "the dependency range mcp>=1.19.0,<3"; hosted, Streamable HTTP, SSE (deprecated), stdio | none
A109 | SUPPORTED | evidence: python-genai README and js-genai README "Built-in MCP support is an experimental feature. You can pass a local MCP server as a tool directly" | Commits I read were newer than the cited ones
A110 | SUPPORTED | evidence: GCL mcp-server.md "Stdio, SSE, or Streamable HTTP" at commit 06d3298 | none
## Summary
Counts: SUPPORTED 103, PARTLY 7, CONTRADICTED 0, NOT CHECKABLE 0 (total 110).
Most important problems:
1. A062: the quoted Python SDK sentence is spliced (not verbatim), and the "researcher confirmed by sending a 2025-06-18 initialize" clause is in no cited source.
2. A077: the quote "each message is an HTTP POST to a single MCP endpoint" is from the Transports overview (MTR), not the cited MCL or MSH.
3. A070: the claim that input validation moved to execution errors in 2025-11-25 is not in the cited MTO; it is in the 2025-11-25 changelog (SEP-1303).
4. A033 and A031: stated as source facts but are inferences or generic definitions (model never talks to the server directly; confused deputy definition).
5. A008: "revision 2026-07-28 is current" is not stated in the cited MSP; only the tag list supports it. Also A105: the Claude API page now lists a newer beta header (mcp-client-2026-09-15), and A002/A044: a 2024-10-07 tag exists before 2024-11-05.
Lookups used: 17 web lookups (WebFetch). All spec, SDK, registry, A2A, npm and PyPI checks were done from git clones, npm view and the PyPI JSON API, which do not count.

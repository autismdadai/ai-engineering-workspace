# Researcher A: MCP (Part 07)

Checked on 2026-10-14. Primary sources were read mostly from git checkouts, which give exact file:line locations and do not count as web lookups:

- Spec repo `github.com/modelcontextprotocol/modelcontextprotocol`: tag `2026-07-28` (commit 5f5440b, dated 2026-07-28) and `main` (commit ff465f0, 2026-10-14). Between the tag and main, the `docs/specification/2026-07-28/` folder changed in 8 files, almost all link fixes (`/docs/draft/...` changed to `/docs/2026-07-28/...`) plus one wording change in subscriptions.mdx. Line numbers below refer to the tag unless a row says "main".
- Python SDK repo `github.com/modelcontextprotocol/python-sdk`, tag `v2.3.0` (2026-10-02).
- TypeScript SDK repo (main and `v1.x` branches), Inspector repo, Registry repo, `googleapis/python-genai`, `googleapis/js-genai` and `google-gemini/gemini-cli` (all shallow clones taken 2026-10-14).

Live URLs are given so the paper can link to them. The spec base URL is https://modelcontextprotocol.io/specification/2026-07-28. Abbreviations: SB = spec, OD = official docs or repo, VB = vendor blog, PR = peer-reviewed, PP = preprint. "Spec repo" means the 2026-07-28 tag of the spec repo.

## (a) Claim table

| ID | Claim | Source | Class | Location | Verdict | Exact numbers and scope | Note |
|---|---|---|---|---|---|---|---|
| A01 | The current revision is 2026-07-28, released on that date | Spec repo tag `2026-07-28`; blog post "The 2026-07-28 Specification" (https://blog.modelcontextprotocol.io, source `blog/content/posts/2026-07-28-spec-ga/index.md`) | SB, VB | tag commit 5f5440b, date 2026-07-28; blog front matter `date: "2026-07-28T09:00:00+00:00"` | confirmed | Earlier revisions: 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25 (git tags) | The blog says "we're officially pushing the release button on the next version of the MCP specification, `2026-07-28`" |
| A02 | The base protocol is "Stateless, self-contained requests" with "Per-request capability negotiation" | https://modelcontextprotocol.io/specification/2026-07-28 | SB | `docs/specification/2026-07-28/index.mdx:50-54` "Base Protocol" | confirmed | Bullets: "JSON-RPC message format / Stateless, self-contained requests / Per-request capability negotiation" | The live page matched the repo when fetched on 2026-10-14 |
| A03 | The `initialize` handshake is removed | Changelog https://modelcontextprotocol.io/specification/2026-07-28/changelog | SB | `changelog.mdx:14`, Major change 2 | confirmed | "Make MCP stateless: remove the `initialize`/`notifications/initialized` handshake. Every request now carries its protocol version and client capabilities in `_meta`" (SEP-2575) | Clients SHOULD send `io.modelcontextprotocol/clientInfo` on each request; servers SHOULD send `io.modelcontextprotocol/serverInfo` in each result's `_meta` |
| A04 | Protocol-level sessions and the `Mcp-Session-Id` header are removed | Changelog | SB | `changelog.mdx:12`, Major change 1 | confirmed | "Remove protocol-level sessions and the `Mcp-Session-Id` header from the Streamable HTTP transport." State that spans calls uses "explicit, server-minted handles passed as ordinary tool arguments" (SEP-2567) | See A33 for the handle pattern |
| A05 | `server/discover` is new; servers MUST implement it; clients MAY call it | Changelog; Discover page | SB | `changelog.mdx:16`; `server/discover.mdx:7-9` | confirmed | "Servers **MUST** implement it." Clients "MAY call it before any other request" | Local test: the `mcp` 2.3.0 server answered `server/discover` with `supportedVersions:["2026-07-28"]` (section b) |
| A06 | Servers must not rely on earlier requests on the same connection | Base Protocol overview https://modelcontextprotocol.io/specification/2026-07-28/basic | SB | `basic/index.mdx:182-209`, "Statelessness" | confirmed | "Servers **MUST NOT** rely on prior requests over the same connection to establish context"; note: "an open connection, such as a STDIO process, is not a conversation or session" | |
| A07 | Every request carries `_meta` keys for protocol version and client capabilities | Changelog; Transports overview | SB | `changelog.mdx:14`; `basic/transports/index.mdx:38-43` | confirmed | Keys: `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientCapabilities` (required); `io.modelcontextprotocol/clientInfo` (SHOULD) | Local test: `mcp` 2.3.0 rejects a request without them with `-32602` "params._meta must be an object carrying the required ... envelope keys" (section b) |
| A08 | Multi Round-Trip Requests (MRTR) replace server-initiated requests | Changelog; Base Protocol | SB | `changelog.mdx:24,26`; `basic/index.mdx:73-85` | confirmed | The server returns `resultType: "input_required"` with `inputRequests`; the client retries with `inputResponses`. Every result MUST carry `resultType`; clients "**MUST** treat an absent `resultType` as `"complete"`" (SEP-2322) | Replaces `roots/list`, `sampling/createMessage` and `elicitation/create` sent from server to client |
| A09 | `ping`, `logging/setLevel` and `notifications/roots/list_changed` are removed | Changelog | SB | `changelog.mdx:20`, Major change 5 | confirmed | Log level is now set per request through `io.modelcontextprotocol/logLevel` in `_meta`; servers "MUST NOT emit `notifications/message` for requests that did not include this field" | |
| A10 | Roots, Sampling and Logging are deprecated, not removed | Deprecated features registry https://modelcontextprotocol.io/specification/2026-07-28/deprecated | SB | `deprecated.mdx:26-28`; `changelog.mdx:73-80` | confirmed | Deprecated in `2026-07-28` (SEP-2577). Earliest removal: "First revision released on or after 2027-07-28". Migration paths: tool parameters or resource URIs instead of Roots; "Integrate directly with LLM provider APIs" instead of Sampling; stderr or OpenTelemetry instead of Logging | A reader who thinks sampling is "gone" is wrong: it "remain[s] fully functional during the deprecation window" |
| A11 | A feature lifecycle policy with a minimum twelve-month deprecation window was adopted | Changelog | SB | `changelog.mdx:107-112` | confirmed | "a minimum twelve-month deprecation window" (SEP-2596) | |
| A12 | Tasks moved out of the core protocol into an official extension | Changelog | SB | `changelog.mdx:22`, Major change 6 | confirmed | Extension ID `io.modelcontextprotocol/tasks`. It "replaces the blocking `tasks/result` method with polling via `tasks/get` and a new `tasks/update`" and "removes `tasks/list`" (SEP-2663) | Tasks first appeared as experimental in 2025-11-25 (SEP-1686, `2025-11-25/changelog.mdx` Major change 9) |
| A13 | The spec overview names three notable extensions: Tasks, Skills over MCP and MCP Apps | Spec overview | SB | `index.mdx:75-87` "Extensions" | confirmed, with an internal inconsistency | Quote: extensions "are always opt-in and require explicit support from both client and server, negotiated during initialization" | "Negotiated during initialization" contradicts A03: initialization no longer exists. Actual mechanism: an `extensions` map in capabilities (`basic/versioning.mdx:80-90`, `changelog.mdx:32`). In the tag, Skills over MCP links to a working-group page, not to an extension spec |
| A14 | Extension IDs use a vendor prefix; official ones use `io.modelcontextprotocol/` | Extensions overview https://modelcontextprotocol.io/extensions/overview | OD | spec repo main `docs/extensions/overview.mdx` | confirmed | Format `{vendor-prefix}/{extension-name}`. MCP Apps = `io.modelcontextprotocol/ui` (`basic/versioning.mdx:90`); official repositories use the `ext-` prefix (ext-auth, ext-apps) | Official auth extensions: OAuth Client Credentials and Enterprise-Managed Authorization |
| A15 | The Skills extension (SEP-2640) is Final, but only after the 2026-07-28 release | Skills Over MCP WG charter; Skills extension overview | OD | spec repo main `docs/community/working-groups/skills-over-mcp.mdx:128`; `docs/extensions/skills/overview.mdx:9,52` | confirmed (scoped) | "SEP-2640 is **Final**, merged on September 13, 2026." ID `io.modelcontextprotocol/skills`. Servers "**MUST** declare both the `resources` capability and the `io.modelcontextprotocol/skills` extension" | Skills are delivered over Resources. Final 47 days after the spec release, so the extension is not part of the 2026-07-28 text. Agent Skills themselves belong to Researcher B |
| A16 | `subscriptions/listen` replaces the HTTP GET stream and `resources/subscribe` | Changelog | SB | `changelog.mdx:18`, Major change 4 | confirmed | Clients opt in to `toolsListChanged`, `promptsListChanged`, `resourcesListChanged`, `resourceSubscriptions`; notifications are tagged `io.modelcontextprotocol/subscriptionId` | Request-scoped notifications (progress, message) stay on the response stream of their own request |
| A17 | SSE resumability (`Last-Event-ID`) is removed | Changelog; Streamable HTTP page | SB | `changelog.mdx:28`; `basic/transports/streamable-http.mdx:157` | confirmed | "Resumable SSE streams via `Last-Event-ID` are not supported." A broken stream loses the request; clients "**MUST** re-issue it as a new request with a new request ID" | Reverses 2025-11-25 minor changes 6-7 (SSE polling and resumption) |
| A18 | List and read results carry cache hints | Changelog | SB | `changelog.mdx:36`, minor change 5 | confirmed | Required `ttlMs` (milliseconds) and `cacheScope` (`"public"` or `"private"`) on `tools/list`, `prompts/list`, `resources/list`, `resources/read`, `resources/templates/list` (SEP-2549) | Local test: the discover result also carried `"cacheScope":"private","ttlMs":0` |
| A19 | Error codes were renumbered into an MCP-reserved range | Base Protocol | SB | `basic/index.mdx:109-151` "Error Codes" | confirmed | `-32020` HeaderMismatch, `-32021` MissingRequiredClientCapability, `-32022` UnsupportedProtocolVersion; `-32020` to `-32099` reserved for the spec; resource not found changed from `-32002` to `-32602` | The SDK constant `UNSUPPORTED_PROTOCOL_VERSION = -32022` (checked in `mcp` 2.3.0) |
| A20 | `tools/list` must not vary per connection, and should have a deterministic order | Tools page https://modelcontextprotocol.io/specification/2026-07-28/server/tools | SB | `server/tools.mdx:62-73` | confirmed | "**MUST NOT** vary per-connection or as a side effect of other requests"; the set "**MAY** vary by the authorization presented on the request". Order: "Servers **SHOULD** return tools in a deterministic order" | The GA blog gives the reason: stable upstream prompt caches |
| A21 | MCP uses JSON-RPC 2.0 between hosts, clients and servers | Spec overview; Base Protocol | SB | `index.mdx:35-40`; `basic/index.mdx:27-49` | confirmed | Hosts: "LLM applications that initiate connections"; Clients: "Connectors within the host application"; Servers: "Services that provide context and capabilities". Request IDs "**MUST NOT** be `null`" | JSON-RPC batching was removed in 2025-06-18 (`2025-06-18/changelog.mdx`, Major change 1) |
| A22 | Each client has a 1:1 relationship with one server; the host keeps the conversation | Architecture https://modelcontextprotocol.io/specification/2026-07-28/architecture | SB | `architecture/index.mdx:61-72, 101-107` | confirmed | "Each client is created by the host and communicates with exactly one server"; "Servers should not be able to read the whole conversation, nor 'see into' other servers" | Clients now "Attach[] protocol version and capabilities to every request" (line 66) |
| A23 | Server features: Tools are model-controlled, Resources application-controlled, Prompts user-controlled | Server features overview | SB | `server/index.mdx:19-21` | confirmed | Prompts: "User-controlled"; Resources: "Application-controlled"; Tools: "Model-controlled" | |
| A24 | Client features: the overview lists only Elicitation | Spec overview; Base Protocol | SB | `index.mdx:64-66`; `basic/index.mdx:14` | confirmed, with an inconsistency | Overview: "Clients may offer the following features to servers: **Elicitation**". But `basic/index.mdx:14` still says "Client Features: Elicitation, sampling and root directory lists" | Sampling and Roots are still in the spec, as deprecated features (A10). Elicitation now travels through MRTR |
| A25 | Fields of a tool definition | Tools page | SB | `server/tools.mdx:283-301`, "Tool" | confirmed | `name`, `title` (optional), `description`, `icons` (optional), `inputSchema` (MUST be a valid JSON Schema object, not `null`; defaults to 2020-12), `outputSchema` (optional), `annotations` (optional) | Recommended schema for a tool with no parameters: `{ "type": "object", "additionalProperties": false }` |
| A26 | Tool names should be 1 to 128 characters from a limited character set | Tools page | SB | `server/tools.mdx:309-316` | confirmed | "between 1 and 128 characters in length (inclusive)"; A-Z, a-z, 0-9, `_`, `-`, `.` | Guidance added in 2025-11-25 (SEP-986) |
| A27 | `structuredContent` may be any JSON value; `outputSchema` binds the server | Tools page; Changelog | SB | `server/tools.mdx:496-515`; `changelog.mdx:49-52` | confirmed | "This can be any JSON value (object, array, string, number, boolean, or null)". A tool returning structured content "SHOULD also return the serialized JSON in a TextContent block". With `outputSchema`, servers "**MUST** provide structured results that conform"; clients "**SHOULD** validate" | Before 2026-07-28 it had to be an object (SEP-2106 loosened it). Structured output was added in 2025-06-18. The spec notes it is "unrelated to LLM 'structured outputs'" |
| A28 | Tool annotations are hints and are untrusted | Tools page; schema.ts | SB | `server/tools.mdx:303-306`; `schema/2026-07-28/schema.ts` ToolAnnotations (around lines 1900-1955) | confirmed | "clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers." Defaults: `readOnlyHint` false, `destructiveHint` true, `idempotentHint` false, `openWorldHint` true | schema.ts: "Clients should never make tool use decisions based on `ToolAnnotations` received from untrusted servers." |
| A29 | Two kinds of tool error: protocol errors and `isError` tool results | Tools page | SB | `server/tools.mdx:738-785`, "Error Handling" | confirmed | Protocol errors (unknown tool, malformed request, server errors) are JSON-RPC errors (example code `-32602`). Tool execution errors (API failures, input validation, business logic) use `isError: true`. "Clients **SHOULD** provide tool execution errors to language models to enable self-correction." | Input validation errors were moved to tool execution errors in 2025-11-25 (SEP-1303). See A54 for how the Python SDK reports an unknown tool |
| A30 | A human should stay in the loop, and servers must validate inputs | Tools page | SB | `server/tools.mdx:33-34, 787-801` | confirmed | "there **SHOULD** always be a human in the loop with the ability to deny tool invocations". Servers MUST "Validate all tool inputs / Implement proper access controls / Rate limit tool invocations / Sanitize tool outputs" | Clients SHOULD show tool inputs before calling, validate results before passing them to the LLM, and set timeouts |
| A31 | Stateful tools should use explicit handles (non-normative guidance) | Tools page | SB | `server/tools.mdx:683-735`, "Stateful Tools" | confirmed | "MCP has no protocol-level session"; servers return "an explicit handle from a creation tool" (example `basket_id`). "a handle is a name, not a capability"; unauthenticated handles need "sufficient entropy (e.g., a UUIDv4)" | Useful design rule for the lab |
| A32 | Two standard transports: stdio and Streamable HTTP | Transports overview https://modelcontextprotocol.io/specification/2026-07-28/basic/transports | SB | `basic/transports/index.mdx:18-22` | confirmed | stdio: "newline-delimited messages over the standard streams of a client-launched subprocess"; Streamable HTTP: "each message is an HTTP POST to a single MCP endpoint" | Servers "do not initiate JSON-RPC requests and clients do not send JSON-RPC responses" (lines 34-36) |
| A33 | stdio rules: stdout carries only MCP messages; logs go to stderr; messages are newline-delimited | stdio page https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio | SB | `basic/transports/stdio.mdx:10-21, 55` | confirmed | "Messages are delimited by newlines, and **MUST NOT** contain embedded newlines"; "The server **MAY** write UTF-8 strings to `stderr` for any logging purposes"; "The server **MUST NOT** write anything to its `stdout` that is not a valid MCP message"; "The server **MUST NOT** write JSON-RPC _requests_ to `stdout`" | Shutdown: the client closes stdin, waits, then sends SIGTERM and SIGKILL (lines 87-107) |
| A34 | stdio backward compatibility: probe with `server/discover`, then fall back to `initialize` | stdio page | SB | `basic/transports/stdio.mdx:121-147` | confirmed | "The fallback **MUST NOT** be keyed to one specific error code"; probing is "**RECOMMENDED**" even for clients that only support the new revision | The Python `Client` does this by default (`mode='auto'`, A50) |
| A35 | Streamable HTTP: one POST endpoint; the GET stream and sessions are removed | Streamable HTTP page https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | SB | `basic/transports/streamable-http.mdx:14-21, 29-50` | confirmed | "Removal of the GET stream endpoint. / Removal of protocol-level sessions." The server answers each POST with "a single JSON object or a Server-Sent Events (SSE) stream scoped to that request" | |
| A36 | Streamable HTTP security: validate Origin; bind to localhost when local | Streamable HTTP page | SB | `basic/transports/streamable-http.mdx:56-67`, "Security & Endpoint" | confirmed | "Servers **MUST** validate the `Origin` header on all incoming connections to prevent DNS rebinding attacks"; invalid Origin gets "HTTP 403 Forbidden"; "When running locally, servers **SHOULD** bind only to localhost (127.0.0.1) rather than all network interfaces (0.0.0.0)" | The 403 rule was clarified in 2025-11-25 (PR #1439) |
| A37 | Streamable HTTP requires the `Mcp-Method` and `Mcp-Name` headers | Streamable HTTP page; Changelog | SB | `streamable-http.mdx:253-291`; `changelog.mdx:35` | confirmed | `Mcp-Method` on all requests; `Mcp-Name` on `tools/call`, `resources/read`, `prompts/get`; also `MCP-Protocol-Version: 2026-07-28` | Tool parameters can be mirrored into headers with `x-mcp-header` (SEP-2243); credentials should not be marked for it (`tools.mdx:399`) |
| A38 | Is SSE gone? The old HTTP+SSE transport is deprecated, not removed; SSE is still used inside Streamable HTTP | Deprecated features registry; Streamable HTTP page | SB | `deprecated.mdx:31`; `changelog.mdx:82-85` | corrected | HTTP+SSE (from 2024-11-05) was "deprecated since protocol version `2025-03-26`" and is reclassified as Deprecated. Earliest removal: "Three months after SEP-2596 reaches Final" | "SSE is gone" is wrong both ways: the legacy transport still exists as Deprecated, and Streamable HTTP still streams responses as `text/event-stream` |
| A39 | Authorization applies to HTTP transports; stdio servers take credentials from the environment | Base Protocol | SB | `basic/index.mdx:221-229`, "Auth" | confirmed | HTTP-based transports "**SHOULD** conform to this specification, whereas implementations using STDIO transport **SHOULD NOT** follow this specification, and instead retrieve credentials from the environment" | Python SDK: a stdio child gets only an allow-listed environment; pass secrets with `env=` (`docs/client/transports.md:119-125`) |
| A40 | Authorization is based on OAuth 2.1 (IETF draft); an MCP server is an OAuth resource server | Authorization https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | SB | `basic/authorization/index.mdx:32-52` | confirmed | Cites "OAuth 2.1 IETF DRAFT (draft-ietf-oauth-v2-1-13)", RFC 8414, RFC 8707, RFC 9728. "A protected _MCP server_ acts as an OAuth 2.1 resource server" | OAuth 2.1 is still a draft, not an RFC |
| A41 | Protected Resource Metadata (RFC 9728) is mandatory | Authorization | SB | `basic/authorization/index.mdx:73-74` | confirmed | "MCP servers **MUST** implement OAuth 2.0 Protected Resource Metadata (RFC9728). MCP clients **MUST** use OAuth 2.0 Protected Resource Metadata for authorization server discovery." | Introduced in 2025-06-18 (Major change 3) |
| A42 | Resource Indicators (RFC 8707) are mandatory for clients | Authorization; Security considerations | SB | `basic/authorization/index.mdx:217-222`; `basic/authorization/security-considerations.mdx:19-20` | confirmed | "MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in RFC 8707"; clients MUST include the `resource` parameter, using the server's canonical URI | Introduced in 2025-06-18 (Major change 4) |
| A43 | Token passthrough is forbidden | Security considerations; Security Best Practices https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | SB, OD | `security-considerations.mdx:124-126`; `docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx:278-347` | confirmed | "The MCP server **MUST NOT** pass through the token it received from the MCP client." Best Practices: "Token passthrough is explicitly forbidden"; "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server." | |
| A44 | Confused deputy: proxy servers must get consent per client | Security considerations; Best Practices | SB, OD | `security-considerations.mdx:107-113`; Best Practices lines 27-276 | confirmed | "MCP proxy servers using static client IDs **MUST** obtain user consent for each dynamically registered client before forwarding to third-party authorization servers (which may require additional consent)." (lines 112-114, link text flattened); Best Practices line 160: proxies "**MUST** implement" per-client consent | |
| A45 | Authorization hardening in 2026-07-28 | Changelog; Deprecated registry | SB | `changelog.mdx:38-48, 93-99`; `deprecated.mdx:29` | confirmed | RFC 9207 `iss` validation (SEP-2468); `application_type` during DCR (SEP-837); credentials keyed by issuer (SEP-2352); Dynamic Client Registration (RFC 7591) deprecated in favor of Client ID Metadata Documents (PR #2858) | CIMD was added as "recommended" in 2025-11-25 (SEP-991) |
| A46 | Session Hijacking is replaced by State Handle Hijacking in the 2026-07-28 Best Practices | Best Practices 2026-07-28 vs 2025-11-25 | OD | 2026-07-28 file lines 516-557; 2025-11-25 and 2025-06-18 files line 479 "### Session Hijacking" | corrected | "MCP servers **MUST NOT** treat possession of a state handle as authentication"; handles SHOULD be bound server-side as `<user_id>:<handle>` | The new page points back to the 2025-11-25 page for session-ID guidance. "Session hijacking" now applies only to older protocol versions |
| A47 | SSRF guidance targets clients that fetch OAuth URLs | Best Practices | OD | lines 349-515 | confirmed | "MCP clients deployed to a server **MUST** consider SSRF risks and implement appropriate mitigations when fetching OAuth-related URLs"; SHOULD require HTTPS, except for loopback addresses during development | Includes a subsection on SSRF against authorization servers (line 484) |
| A48 | Local MCP server compromise: one-click installs need explicit consent | Best Practices | OD | lines 559-652 | confirmed | If a client supports one-click local server setup it "**MUST** implement proper consent mechanisms" and MUST "Show the exact command that will be executed, without truncation" and "Require explicit user approval" | Also covers OAuth URL validation (reject `javascript:` and `file:` schemes, no shell to open URLs), stdio proxy security, mix-up attacks and localhost redirect impersonation |
| A49 | Scope minimization | Best Practices | OD | lines 874-990 | confirmed | "Minimal initial scope set (e.g., `mcp:tools-basic`)"; "Incremental elevation via targeted `WWW-Authenticate` `scope="..."` challenges" | Incremental scope consent came in 2025-11-25 (SEP-835) |
| A50 | The spec's security principles: user consent and control, data privacy, tool safety | Spec overview | SB | `index.mdx:89-124`, "Security and Trust & Safety" | confirmed | "Hosts must obtain explicit user consent before invoking any tool"; "MCP itself cannot enforce these security principles at the protocol level" | In this section "must" is lowercase, so it is not a BCP 14 keyword. Only the "Implementation Guidelines" use **SHOULD** |
| A51 | PyPI `mcp` 2.3.0: released 2026-10-02, needs Python >=3.10, MIT licence | PyPI JSON API https://pypi.org/pypi/mcp/2.3.0/json; repo `pyproject.toml` at v2.3.0 | OD | `upload_time` 2026-10-02T22:06:52Z; `requires-python = ">=3.10"`; `license = { text = "MIT" }` | confirmed | Author on PyPI: "Model Context Protocol a Series of LF Projects, LLC." Dependencies include `mcp-types`, `httpx2`, `pydantic`, `starlette`, `uvicorn`, `opentelemetry-api` | Repo `main` after 2.3.0 already says `requires-python = ">=3.11"`, so a later release may drop 3.10 |
| A52 | The high-level server class in 2.x is `MCPServer`; `FastMCP` was renamed | Python SDK migration guide https://py.sdk.modelcontextprotocol.io/migration/ | OD | `docs/migration.md:643-675` at v2.3.0; `src/mcp/server/fastmcp.py` | confirmed | "The `FastMCP` class has been renamed to `MCPServer`". Import: `from mcp.server.mcpserver import MCPServer` (the README also uses `from mcp.server import MCPServer`). Importing `mcp.server.fastmcp` raises `ModuleNotFoundError` | Decorator `@mcp.tool()` is unchanged. `mcp.run()` defaults to stdio (`run(self, transport: Literal["stdio"] = ...)`) |
| A53 | The client API is `mcp.Client`; one constructor covers stdio, HTTP and in-memory | Python SDK docs: Client transports | OD | `docs/client/transports.md:105-158` at v2.3.0 | confirmed (tested) | "stdio is `Client(StdioServerParameters(...))`"; a URL string means Streamable HTTP; "`Client(mcp)` (the server object) connects in memory" | Methods: `list_tools()`, `call_tool(name, args)`; result fields are snake_case (`structured_content`, `is_error`, `input_schema`) |
| A54 | `mcp` 2.3.0 returns an unknown tool as an `isError` result, not as a JSON-RPC error | Local test (section b, wire.jsonl id 4); `mcp/server/mcpserver/tools/tool_manager.py:72,85` | OD (code) | Observed output: `{"jsonrpc":"2.0","id":4,"result":{"content":[{"text":"Unknown tool: nope","type":"text"}],"isError":true,...}}` | confirmed (observed) | Python 3.13.16, mcp 2.3.0, stdio | Differs from the spec example in A29, which lists "Unknown tool" as a protocol error (`-32602`). Worth a sentence in the paper: SDKs may map errors differently |
| A55 | Breaking changes from 1.x | Migration guide | OD | `docs/migration.md:16-34`, "Changes almost every project hits" | confirmed | `FastMCP` renamed `MCPServer`; camelCase fields become snake_case; `mcp.types` names removed or moved to the `mcp-types` package; `McpError` becomes `MCPError`; resource URIs become `str`; `streamablehttp_client` removed; `httpx` replaced by `httpx2`; `Client` defaults to `mode='auto'`; transport parameters move to `run()`; sync handlers run on a worker thread; low-level decorators replaced by `on_*` parameters; low-level tool exceptions no longer become `isError` | Also: experimental Tasks removed (`migration.md:2009-2015`): "This SDK does not implement the extension yet." |
| A56 | There is an in-memory transport for tests | Migration guide "Testing utilities" | OD | `docs/migration.md:2668-2692` | confirmed (tested) | "`create_connected_server_and_client_session` ... has been removed. Use `mcp.client.Client` instead"; usage `async with Client(server) as client:` | In `mode='auto'` an in-process client "dispatches calls directly through `DirectDispatcher` with no JSON-RPC framing" (`migration.md:1792-1796`) |
| A57 | The v2 server speaks both protocol eras; server-to-client calls fail on 2026-07-28 connections | Python SDK "What's new" | OD | `docs/whats-new.md:151-165` | confirmed (tested) | "the same stdio server answers a 2025-era client's `initialize` and a 2026-era client's requests"; "`ctx.elicit()` and `ctx.session.create_message()` fail there with `NoBackChannelError`" | Local test: `initialize` with protocolVersion 2025-06-18 succeeded against the v2 server (section b) |
| A58 | `fastmcp` 4.1.0 is a separate project (PrefectHQ), Apache-2.0, built on top of `mcp` 2.x | PyPI JSON for `fastmcp` 4.1.0 and `fastmcp-slim` 4.1.0 | OD | `license_expression` "Apache-2.0"; `requires_python` ">=3.10"; uploaded 2026-10-08; repository https://github.com/PrefectHQ/fastmcp | confirmed | `fastmcp` requires `fastmcp-slim[client,server]==4.1.0`, which requires `mcp<3.0.0,>=2.0.0` and `mcp-types` | Not the same as the SDK's `MCPServer` (formerly `FastMCP`). That FastMCP 1.0 was merged into the official SDK in 2024 is background knowledge, not checked. Prefect's CEO announced "FastMCP 4.0" in the GA blog |
| A59 | `@modelcontextprotocol/sdk` 1.32.1 is the v1 maintenance line and does not implement 2026-07-28 | `npm view`; TS SDK `v1.x` branch README and `src/types.ts` | OD | npm: version 1.32.1, license MIT, engines node ">=18". README: "It implements the MCP spec up to 2025-11-25. Support for the 2026-07-28 spec ... is not planned for v1.x"; `LATEST_PROTOCOL_VERSION = '2025-11-25'` | corrected | v2 ships as separate packages `@modelcontextprotocol/server`, `@modelcontextprotocol/client` and `@modelcontextprotocol/core`, each 2.3.1, Apache-2.0, node ">=20". v1.x gets fixes "for at least six months after the v2 release (2026-07-27)" | Anyone citing "TS SDK 1.32.1" as current for 2026-07-28 is wrong |
| A60 | MCP Inspector 2.11.0: a developer tool for testing servers; Node >=22.19.0 | `npm view @modelcontextprotocol/inspector`; Inspector README | OD | npm: version 2.11.0, license "SEE LICENSE IN LICENSE", engines node ">=22.19.0" | confirmed | "A developer tool for inspecting MCP servers"; four modes: Web, CLI, TUI, and `mcpdo` (experimental) | README warns that without a keychain, secrets go to `~/.mcp-inspector/secrets.json` "unencrypted unless you supply a key". Licence file: project "transition from the MIT License to the Apache License, Version 2.0"; new code Apache-2.0, docs CC-BY-4.0. Not run (no npx) |
| A61 | Official MCP Registry: still in preview; API frozen at v0.1 | Registry docs https://modelcontextprotocol.io/registry/about; Registry repo README; preview blog 2025-09-08 | OD, VB | spec repo main `docs/registry/about.mdx` Note; registry README lines 9-11 (commit 11b7b0e, 2026-10-11) | confirmed | "The MCP Registry is currently in preview. Breaking changes or data resets may occur before general availability." Launched in preview 2025-09-08; "API freeze (v0.1)" announced 2025-10-24 | The live landing page states no status (fetched 2026-10-14). It holds metadata only, "does **not** support private servers", and "is not intended to be directly consumed by host applications" |
| A62 | Governance: Anthropic donated MCP to the Agentic AI Foundation (Linux Foundation) | Linux Foundation press release; MCP blog 2025-12-09; GOVERNANCE.md | VB, OD | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation (dated December 9, 2025); `blog/content/posts/2025-12-09-mcp-joins-agentic-ai-foundation.md:17,25`; `GOVERNANCE.md:3` | confirmed | "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation." AAIF was "co-founded by Anthropic, Block and OpenAI". Founding projects: MCP (Anthropic), goose (Block), AGENTS.md (OpenAI) | Legal entity: "Model Context Protocol a Series of LF Projects, LLC". Blog: projects "maintain full autonomy over their technical direction" |
| A63 | Claude API MCP connector: beta header, tools only, remote HTTP only | https://platform.claude.com/docs/en/agents-and-tools/mcp-connector | OD | Basic example; "Limitations"; "Pin an MCP server's tool list (beta)"; "Data retention" | confirmed | Header `mcp-client-2025-11-20`; "The previous version of this feature (`mcp-client-2025-04-04`) is deprecated"; newer `mcp-client-2026-09-15` "records the tool list each server returns and lets you pin it". "only tool calls are currently supported"; "supports both Streamable HTTP and SSE transports"; "Local STDIO servers cannot be connected directly"; "not covered by ZDR arrangements" | Request uses `mcp_servers` (`type: "url"`, `url` must start with https://) plus a `tools` entry `type: "mcp_toolset"`. Platforms: Claude API, Claude Platform on AWS, Microsoft Foundry (all Beta). The page does not say which MCP protocol revision it speaks |
| A64 | Claude Code is an MCP client over stdio, HTTP, SSE (deprecated) and WebSocket; its v2 runtime adds 2026-07-28 | https://code.claude.com/docs/en/mcp | OD | "Option 1-4"; "MCP installation scopes"; "MCP client runtimes" | confirmed | `claude mcp add --transport http <name> <url>`; stdio: `claude mcp add [options] <name> -- <command> [args...]`; "The SSE (Server-Sent Events) transport is deprecated." Scopes: local (default) and user in `~/.claude.json`, project in `.mcp.json`. "The v2 runtime is the same code on MCP TypeScript SDK 2.0, which adds MCP protocol revision 2026-07-28" | v2 is the default from Claude Code v2.1.232 (sessions that fetch feature flags) or v2.1.274 (others). Override with `MCP_SDK_GENERATION=v1|v2` and `MCP_PROTOCOL_NEGOTIATION=auto|legacy`. Warning: "Verify you trust each server before connecting it." |
| A65 | OpenAI Responses API: the remote MCP tool | https://developers.openai.com/api/docs/guides/tools-connectors-mcp (redirected from platform.openai.com) | OD | sections on remote MCP, approvals, risks | confirmed (via fetch summary) | "Use the `mcp` tool type in the Responses API"; works with "either the Streamable HTTP or the HTTP/SSE transport protocols"; "By default, OpenAI will request your approval before any data is shared"; approvals arrive as `mcp_approval_request` items. "A malicious server can exfiltrate sensitive data from anything that enters the model's context." | Fields: `server_label`, `server_url`, `require_approval` (`"never"` or per tool), `allowed_tools`. Local servers through a `tunnel_id` ("Secure MCP Tunnel"). The page names no protocol revision and links the 2025-03-26 spec. No beta header found |
| A66 | OpenAI Agents SDK (Python): MCP server classes | https://openai.github.io/openai-agents-python/mcp/ | OD | transport list; protocol version note | confirmed (via fetch summary) | `HostedMCPTool`, `MCPServerStreamableHttp`, `MCPServerSse`, `MCPServerStdio`; "The MCP project has deprecated the Server-Sent Events transport." | Supports `mcp>=1.19.0,<3`; "The installed `mcp` package version is separate from the MCP protocol version negotiated with a server." |
| A67 | Google Gemini: MCP support in the GenAI SDKs is "experimental" and client-side | `googleapis/python-genai` README (commit 829ec55); `googleapis/js-genai` README (commit 6bfba87) | OD | python-genai `README.md:942-999`; js-genai `README.md:298-335` | confirmed (scoped) | "Built-in MCP support is an experimental feature. You can pass a local MCP server as a tool directly." Python passes an `mcp.ClientSession` in `tools=[session]`; JS uses `mcpToTool(mcpClient)` with `@modelcontextprotocol/sdk` (v1) | Gemini Enterprise Agent Platform: `Tool.mcp_servers`. The ai.google.dev function-calling page had no MCP section on 2026-10-14 (two fetches). Gemini CLI supports "Stdio, SSE, or Streamable HTTP" (`docs/tools/mcp-server.md:37-61`, commit 06d3298). No version header found |

## (b) Working stdio example (files, commands, exact output, Python version)

Environment: Linux; system `python3 --version` gives `Python 3.13.16`. Fresh venv; `pip install mcp==2.3.0` pulled in `mcp-types 2.3.0`, `httpx2 2.13.1` and `pydantic 2.14.1`.

Files are in `/home/claude/part07/research/stdio-example/`: `server.py`, `client.py`, `test_inmemory.py`, `wire.jsonl`.

**Setup**
```bash
python3 -m venv venv
venv/bin/pip install mcp==2.3.0
venv/bin/pip show mcp        # Version: 2.3.0, License: MIT
```

**server.py**
```python
"""Tiny MCP server over stdio (mcp 2.3.0)."""
import sys

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("demo-server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    print(f"add called with a={a}, b={b}", file=sys.stderr)  # logs go to stderr, never stdout
    return a + b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ToolError("b must not be zero")  # becomes an isError: true tool result
    return a / b


if __name__ == "__main__":
    mcp.run()  # default transport is stdio
```

**client.py**
```python
"""Launch server.py as a stdio subprocess, list tools, call tools (mcp 2.3.0)."""
import asyncio
import sys

from mcp import Client, StdioServerParameters


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(params) as client:  # default mode='auto': probes server/discover
        print("protocol version:", client.protocol_version)
        print("server info:", client.server_info)
        tools = await client.list_tools()
        for t in tools.tools:
            print("tool:", t.name, "|", t.description, "|", t.input_schema)
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print("add structured_content:", result.structured_content)
        print("add content:", result.content)
        print("add is_error:", result.is_error)
        bad = await client.call_tool("divide", {"a": 1, "b": 0})
        print("divide is_error:", bad.is_error, "|", bad.content[0].text)


asyncio.run(main())
```

**Run:** `venv/bin/python client.py 2> err.txt` (run from the example folder). Exit code 0.

stdout:
```
protocol version: 2026-07-28
server info: name='demo-server' title=None version='' description=None website_url=None icons=None
tool: add | Add two integers. | {'type': 'object', 'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'addArguments'}
tool: divide | Divide a by b. | {'type': 'object', 'properties': {'a': {'title': 'A', 'type': 'number'}, 'b': {'title': 'B', 'type': 'number'}}, 'required': ['a', 'b'], 'title': 'divideArguments'}
add structured_content: {'result': 5}
add content: [TextContent(type='text', text='5', annotations=None, meta=None)]
add is_error: False
divide is_error: True | Error executing tool divide: b must not be zero
```
stderr (the server's stderr is passed through to the client's):
```
add called with a=2, b=3
Tool 'divide' failed: 'Error executing tool divide: b must not be zero'
```
Notes:
- The type hints became `inputSchema`. The return annotation also produced an `outputSchema` (`addOutput`, seen in the legacy test below), and an `int` return comes back wrapped as `structured_content {'result': 5}` plus a text block.
- With a plain `ValueError` instead of `ToolError`, the result is still `is_error: True`, but the text is only "Error executing tool divide" and a full traceback goes to stderr. For the lab, use `ToolError` so the model can read the reason.

**In-memory test (test_inmemory.py):** no subprocess.
```python
import asyncio
from mcp import Client
from server import mcp as server

async def main() -> None:
    async with Client(server) as client:
        r = await client.call_tool("add", {"a": 40, "b": 2})
        assert r.structured_content == {"result": 42}, r
        print("in-memory OK:", r.structured_content)

asyncio.run(main())
```
Output: `add called with a=40, b=2` then `in-memory OK: {'result': 42}`.

**Raw wire test (no SDK client, no `initialize`).** Command: `(cat wire.jsonl; sleep 2) | venv/bin/python server.py 2>/dev/null`. Keep stdin open for a moment: with plain `< wire.jsonl` the server saw EOF and exited before answering the last request (only 3 of 4 replies). That matches the spec: on stdin EOF the server exits and in-flight requests are lost (stdio.mdx:102-115).

wire.jsonl (four lines):
```
{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{},"io.modelcontextprotocol/clientInfo":{"name":"raw","version":"0"}}}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2}}}
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"nope","arguments":{},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}
```
stdout:
```
{"jsonrpc":"2.0","id":1,"result":{"cacheScope":"private","capabilities":{"prompts":{"listChanged":true},"resources":{"listChanged":true,"subscribe":true},"tools":{"listChanged":true}},"resultType":"complete","supportedVersions":["2026-07-28"],"ttlMs":0,"_meta":{"io.modelcontextprotocol/serverInfo":{"name":"demo-server","version":""}}}}
{"jsonrpc":"2.0","id":2,"result":{"content":[{"text":"3","type":"text"}],"isError":false,"resultType":"complete","structuredContent":{"result":3},"_meta":{"io.modelcontextprotocol/serverInfo":{"name":"demo-server","version":""}}}}
{"jsonrpc":"2.0","id":3,"error":{"code":-32602,"message":"params._meta must be an object carrying the required 'io.modelcontextprotocol/protocolVersion' and 'io.modelcontextprotocol/clientCapabilities' envelope keys"}}
{"jsonrpc":"2.0","id":4,"result":{"content":[{"text":"Unknown tool: nope","type":"text"}],"isError":true,"resultType":"complete","_meta":{"io.modelcontextprotocol/serverInfo":{"name":"demo-server","version":""}}}}
```
This one test shows: no handshake is needed, `_meta` is required on every request, `resultType` and `serverInfo` appear in every result, and `server/discover` works. An unknown tool comes back as `isError` (A54).

**Legacy check:** sending `initialize` (protocolVersion `2025-06-18`), then `notifications/initialized`, then `tools/list` to the same server worked. The reply was `{"jsonrpc":"2.0","id":1,"result":{"capabilities":{...},"protocolVersion":"2025-06-18","serverInfo":{"name":"demo-server","version":""}}}`, and the tool list included `outputSchema`.

SDK constants (mcp 2.3.0): `LATEST_PROTOCOL_VERSION = 2026-07-28`, `DEFAULT_NEGOTIATED_VERSION = 2025-03-26`, `UNSUPPORTED_PROTOCOL_VERSION = -32022`.

## (c) Changes since 2025-06-18 that a reader with older knowledge would get wrong

1. **"Clients start with `initialize` and hold a session."** Wrong for 2026-07-28: no handshake and no `Mcp-Session-Id`. Each request carries version and capabilities in `_meta`; `server/discover` is optional for clients but mandatory for servers (A03 to A07).
2. **"Servers call back to the client for sampling, elicitation and roots."** Server-initiated requests are gone. Servers now return `resultType: "input_required"` and the client retries (MRTR, A08). In the Python SDK, push-style `ctx.elicit()` fails on 2026 connections with `NoBackChannelError` (A57).
3. **"Sampling and roots are core client features."** Both are Deprecated, along with server Logging. Earliest removal: the first revision released on or after 2027-07-28 (A10). `ping` and `logging/setLevel` are removed outright (A09).
4. **"Tasks are an experimental core feature."** Tasks were experimental core only in 2025-11-25. They are now the `io.modelcontextprotocol/tasks` extension with polling via `tasks/get` (A12), and the Python SDK 2.3.0 does not implement it (A55).
5. **"Extensions are informal."** There is now a formal framework: an `extensions` capability map and `io.modelcontextprotocol/*` IDs. MCP Apps = `io.modelcontextprotocol/ui`. Skills over MCP = `io.modelcontextprotocol/skills`, Final only on 2026-09-13 (A13 to A15).
6. **"Streamable HTTP has a GET stream and resumable SSE."** The GET endpoint and `Last-Event-ID` resumption are gone; `subscriptions/listen` is the change-notification channel. New headers `Mcp-Method` and `Mcp-Name` are required (A16, A17, A35, A37).
7. **"SSE is dead"** (or the opposite, "SSE is a normal option"). Both are wrong. The HTTP+SSE transport is formally Deprecated, not removed, and SSE remains the response-stream format inside Streamable HTTP. Some vendors (Claude API connector, OpenAI Responses API) still accept SSE servers (A38, A63, A65).
8. **"`structuredContent` must be an object."** It can be any JSON value since 2026-07-28 (A27). Input validation failures belong in `isError` results, not protocol errors (since 2025-11-25, A29).
9. **"Dynamic Client Registration is the way to register OAuth clients."** DCR is deprecated in favor of Client ID Metadata Documents. RFC 9207 `iss` validation is new (A45).
10. **"Session hijacking" as the headline threat.** In the 2026-07-28 Best Practices it is replaced by "State Handle Hijacking" (A46).
11. **"`from mcp.server.fastmcp import FastMCP`."** Fails on `mcp` 2.x with `ModuleNotFoundError`; use `MCPServer` (A52). Fields are snake_case (`input_schema`, `structured_content`, `is_error`).
12. **"`@modelcontextprotocol/sdk` is the TypeScript SDK."** That package is the v1 maintenance line (2025-11-25 at most). The 2026-07-28 TypeScript SDK is `@modelcontextprotocol/server` and `@modelcontextprotocol/client` 2.x (Apache-2.0, Node >=20) (A59).
13. **"MCP is Anthropic's protocol."** Since 2025-12-09 it is a project of the Agentic AI Foundation under the Linux Foundation (A62).
14. **Error codes.** Resource not found is `-32602` (was `-32002`), and new codes live in `-32020` to `-32022` (A19).

## (d) Open questions and things you couldn't check

- **Spec inconsistencies to flag rather than quote as fact:** `index.mdx:79-80` says extensions are "negotiated during initialization", although initialization was removed; `basic/index.mdx:14` lists sampling and roots as client features, while `index.mdx:64-66` lists only Elicitation. Both are in the 2026-07-28 tag and unchanged on main.
- **Error-handling divergence:** the spec presents "Unknown tool" as a protocol error, but `mcp` 2.3.0 `MCPServer` returns it as `isError: true` (A54). I did not check the TypeScript v2 SDK's behavior.
- **Claude API connector:** the fetch summary said `mcp-client-2026-09-15` "includes everything `mcp-client-2025-11-20` does". A verbatim re-fetch did not show that sentence, so treat it as unverified. The page does not state which MCP protocol revision the connector speaks.
- **OpenAI:** the Responses API and Agents SDK rows (A65, A66) come from WebFetch summaries. Their quotes look verbatim but were not compared character by character. I found no beta header for the OpenAI MCP tool. The protocol revision OpenAI's hosted MCP client speaks is not stated on the page.
- **Google:** no official ai.google.dev page with MCP content was found in 2 fetches and 2 searches. The Gemini evidence is the official SDK READMEs and the Gemini CLI repo docs (OD), not the API docs. The js-genai example uses the v1 TypeScript SDK. Google Cloud's statement in the GA blog is a vendor quote, not documentation.
- **Inspector 2.11.0:** not run (no npx, as instructed). I did not verify whether it speaks 2026-07-28. Its licence string is "SEE LICENSE IN LICENSE" (mixed MIT and Apache-2.0 transition text), not a single SPDX ID.
- **Python SDK `requires-python`:** 2.3.0 says >=3.10, but repo `main` after the release says >=3.11. A future 2.x release may drop 3.10; tell lab readers to pin `mcp==2.3.0`.
- **Python SDK extensions:** 2.3.0 ships an MCP Apps module (`mcp/server/apps.py`) but no Skills module, and it does not implement Tasks. I did not check Skills support in the TypeScript v2 SDK.
- **Registry GA:** the docs and README still say "preview" (latest dated update in the README: 2025-10-24 API freeze). I could not confirm whether a v1 or GA date exists; the live landing page states no status.
- **SEP-2596 status:** the earliest removal of HTTP+SSE is "Three months after SEP-2596 reaches Final". I did not check whether SEP-2596 is Final yet.
- **Background, not verified:** FastMCP 1.0 was merged into the official Python SDK in 2024, and the standalone `fastmcp` package continued separately. The PyPI data (A58) confirms only that it is a separate Apache-2.0 project that depends on `mcp` 2.x.
- **Not opened:** the SEP pull requests themselves (cited only through the changelog); the RFC texts (cited only through the spec).

## (e) Lookup count

Web lookups (WebFetch and WebSearch): **16 of about 35**.
1. modelcontextprotocol.io/specification/2026-07-28 (live check)
2. docs.claude.com MCP connector (redirect only)
3. platform.claude.com MCP connector
4. code.claude.com/docs/en/mcp
5. platform.openai.com MCP guide (redirect only)
6. developers.openai.com MCP guide
7. openai.github.io Agents SDK MCP
8. ai.google.dev function-calling (no MCP section)
9. WebSearch: Gemini API MCP (only non-official results)
10. ai.google.dev function-calling, offset 100000 (no MCP section)
11. WebSearch: Gemini MCP docs (only non-official results)
12. registry.modelcontextprotocol.io (no status on page)
13. WebSearch: Linux Foundation AAIF press release
14. linuxfoundation.org AAIF press release
15. platform.claude.com MCP connector (verbatim re-check)
16. code.claude.com MCP (verbatim "MCP client runtimes")

Not counted under the rules, listed for transparency:
- 6 `curl` calls to the PyPI JSON API (`mcp`, `fastmcp`, `mcp` 2.3.0, `fastmcp` 4.1.0 twice, `fastmcp-slim` 4.1.0)
- 3 `npm view` calls covering 6 packages
- 7 git clones or fetches (spec, python-sdk, typescript-sdk including the v1.x branch, inspector, registry, python-genai, js-genai, gemini-cli)
- 1 `pip install mcp==2.3.0`

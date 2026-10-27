# Source check, set A (claims A001-A083)
A001 | SUPPORTED | evidence: BEA "They are typically just LLMs using tools based on environmental feedback in a loop." | none
A002 | SUPPORTED | evidence: BEA "Workflows are systems where LLMs and tools are orchestrated through predefined code paths"; "Agents ... are systems where LLMs dynamically direct their own processes and tool usage" | none
A003 | SUPPORTED | evidence: FW2 describes the harness as "everything in an AI agent except the model itself" | the list (instruction files, tests, limits) is the author's gloss
A004 | PARTLY | evidence: gVisor security.md "A sandbox is not a substitute for a secure architecture" (word for word) | quote is right; "gVisor and Firecracker are stronger boundaries" than a container is not in the cited GVS
A005 | SUPPORTED | evidence: ACU "roughly 1,000-1,800 input tokens each" (screenshots in long loops); prompt-injection text on screen covered in the security section | none
A006 | SUPPORTED | evidence: ACU "instructions on webpages or contained in images might override your instructions or cause Claude to make mistakes" | none
A007 | PARTLY | evidence: MRS "In our data, agents typically use about 4× more tokens than chat interactions" (June 13, 2025) | quote and date right; the cause ("because the whole history is sent again on every turn") is not given in MRS
A008 | SUPPORTED | evidence: BEA agent definition (LLM using tools in a loop) | none
A009 | SUPPORTED | evidence: STOP quick-reference table lists end_turn, max_tokens, stop_sequence, tool_use, pause_turn, refusal, model_context_window_exceeded = 7 | the page does not state the count; it is a tally of the table
A010 | SUPPORTED | evidence: HTC "`is_error` (optional): Set to `true` if the tool execution resulted in an error." | none
A011 | SUPPORTED | evidence: PAR page is about several tool_use blocks in one response | none
A012 | SUPPORTED | evidence: OAS `DEFAULT_MAX_TURNS = 10`, `max_turns`; SDL max_turns and max_budget_usd | none
A013 | SUPPORTED | evidence: OWL "Utilise human-in-the-loop control to require a human to approve high-impact actions before they are taken" | none
A014 | SUPPORTED | evidence: ACE defines compaction; CED context editing (clear_tool_uses_20250919) | "Shortening an old conversation" fits compaction; context editing clears tool results rather than shortening the conversation, a loose pairing
A015 | PARTLY | evidence: FW2 "everything in an AI agent except the model itself" | "Three senses (Section 3.5)" is the document's own synthesis; FW2 gives one definition
A016 | SUPPORTED | evidence: CMM "Claude treats them as context, not enforced configuration"; AGENTS.md readable in place of CLAUDE.md | none
A017 | SUPPORTED | evidence: CAS types.py hooks; PreToolUse hook (line 244 area) can return permissionDecision; SDL "a PreToolUse hook that rejects a tool call prevents it from executing" | none
A018 | SUPPORTED | evidence: TAU "a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials" | none
A019 | SUPPORTED | evidence: DSE "Kernel namespaces", control groups sections; "namespaces and cgroups" | none
A020 | SUPPORTED | evidence: DSC "the profile is an allowlist that denies access to system calls by default" | none
A021 | SUPPORTED | evidence: MOB daemon/pkg/oci/caps/defaults.go at docker-v29.9.1 lists exactly 14 CAP_ entries | none
A022 | SUPPORTED | evidence: GVI "written in memory-safe Go"; "gVisor Sentry"; runsc runtime | none
A023 | SUPPORTED | evidence: FCR README "lightweight virtual machines, called microVMs" | none
A024 | SUPPORTED | evidence: runc CHANGELOG 1.1.12 "CVE-2024-21626, a container breakout attack" | none
A025 | SUPPORTED | evidence: ACU "screenshot capabilities and mouse/keyboard control"; GCU "generating specific UI actions like mouse clicks and keyboard inputs"; OCU "Computer use lets a model operate browser and desktop interfaces" | none
A026 | SUPPORTED | evidence: PWM README "Uses Playwright's accessibility tree, not pixel-based input" and "structured accessibility snapshots, bypassing the need for screenshots" | none
A027 | SUPPORTED | evidence: OFC five steps, last: "Receive a final response from the model (or more tool calls)" | none
A028 | SUPPORTED | evidence: SDL "Claude continues calling tools and processing results until it produces a response with no tool calls." | none
A029 | SUPPORTED | evidence: STOP table of seven values | count is a tally, not stated
A030 | SUPPORTED | evidence: STOP "Returned when the server-side sampling loop reaches its iteration limit while executing server tools such as web search"; client tools never give pause_turn | none
A031 | SUPPORTED | evidence: HTC "tool_result blocks must come FIRST in the content array"; PAR "all together in the next user message" | label only; content matches
A032 | SUPPORTED | evidence: PAR "The API doesn't prescribe an execution order"; "Tools with side effects, shared state, or ordering requirements might be better run sequentially." | none
A033 | SUPPORTED | evidence: HTC tool_result with "is_error": true | none
A034 | SUPPORTED | evidence: HTC "Claude will retry 2-3 times with corrections before apologizing to the user" | source scopes it to invalid or missing-parameter requests; no rate given, so the "not a measured rate" note is fair
A035 | SUPPORTED | evidence: HTC "include what went wrong and what Claude should try next"; WTA "prompt-engineer your error responses to clearly communicate specific and actionable improvements" (page confirms start of the sentence; the tail "rather than opaque error codes or tracebacks" was not shown in the fetch summary) | tail of WTA quote not independently confirmed
A036 | SUPPORTED | evidence: OAS tool.py `default_tool_error_function`: "Return a fixed error response without exposing the exception to the model"; returns "An error occurred while running the tool. Please try again." | the "lab's cross-check (B2)" part cannot be checked from this source
A037 | SUPPORTED | evidence: BEA "it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control." | none
A038 | SUPPORTED | evidence: OAS run_config.py `DEFAULT_MAX_TURNS = 10`; run.py "defined as one AI invocation (including any tool calls that might occur)"; docs "raise a MaxTurnsExceeded"; error_handlers key "max_turns"; no budget option found | none
A039 | SUPPORTED | evidence: SDL table "Max turns ... No limit", "Max budget ... No limit"; `error_max_turns`, `error_max_budget_usd`; "Spend can therefore pass the cap by up to the cost of that one response" | SDL adds "plus anything that subagents still running ... spend"; claim's quote is a true truncation
A040 | SUPPORTED | evidence: SDL "max_turns ... counts tool-use turns only"; CAS types.py "A turn consists of a user message and assistant response." | none
A041 | SUPPORTED | evidence: OWL LLM06 "excessive functionality; excessive permissions; excessive autonomy"; both advice quotes match lines 74 and 78 | none
A042 | SUPPORTED | evidence: OWL "The following options will not prevent Excessive Agency, but can limit the level of damage caused" (logging and rate limiting listed) | none
A043 | SUPPORTED | evidence: openai-agents docs human_in_the_loop.md "pause agent execution until a person approves or rejects sensitive tool calls"; SDL "a PreToolUse hook that rejects a tool call prevents it from executing" | none
A044 | SUPPORTED | evidence: SDL "Claude receives a rejection message as the tool result and typically attempts a different approach or reports that it couldn't proceed." | none
A045 | SUPPORTED | evidence: SDL "It does not reset between turns within a session." | none
A046 | SUPPORTED | evidence: ACE "One of the safest lightest touch forms of compaction is tool result clearing" | none
A047 | SUPPORTED | evidence: CED `clear_tool_uses_20250919`, trigger default 100,000 input tokens, keep default 3 tool uses | none
A048 | SUPPORTED | evidence: ACE compaction = conversation nearing the limit summarized; SDL "specific instructions from early in the conversation may not be preserved"; "Persistent rules belong in CLAUDE.md" | none
A049 | SUPPORTED | evidence: WTA "For Claude Code, we restrict tool responses to 25,000 tokens by default." | none
A050 | SUPPORTED | evidence: ACE subagent "returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)" | none
A051 | SUPPORTED | evidence: LEH README "a unified framework to test generative language models on a large number of different evaluation tasks"; SWB docs "Docker-based evaluation harness" (docs/reference/harness.md, docs/guides/docker_setup.md) | the phrase is in docs, not the top README; README says "containerized evaluation harness using Docker"
A052 | SUPPORTED | evidence: AHL "a powerful, general-purpose agent harness adept at coding" | none
A053 | SUPPORTED | evidence: FW2 "everything in an AI agent except the model itself"; guides "anticipate the agent's behaviour and aim to steer it before it acts"; sensors "observe after the agent acts and help it self-correct" | none
A054 | SUPPORTED | evidence: FW1 (17 Feb 2026) "I like 'harness' as a word to describe the tooling and practices we can use to keep AI agents in check."; FW2 dated 02 April 2026 and says it supersedes the memo | the guides/sensors half rests on FW2, not FW1
A055 | SUPPORTED | evidence: OHE "designing environments, feedback loops, and control systems"; "roughly 1,500 pull requests ... a small team of just three engineers"; "0 lines of manually-written code"; "Over the past five months"; term not defined in body | post says team later grew to seven; "popularized" is not from OHE
A056 | SUPPORTED | evidence: CMM "To block an action regardless of what Claude decides, use a PreToolUse hook instead." | none
A057 | SUPPORTED | evidence: CMM "target under 200 lines per CLAUDE.md file" | none
A058 | SUPPORTED | evidence: CMM "By default, Claude reads AGENTS.md only when you have no CLAUDE.md in your working directory or above it" (v2.1.277 or later); CDX agents_md.rs "Collect every AGENTS.md found from the project root down to the ..."; config_toml.rs `DEFAULT_PROJECT_DOC_MAX_BYTES: usize = 32 * 1024` | none
A059 | SUPPORTED | evidence: OHE "we treat it as the table of contents" | none
A060 | SUPPORTED | evidence: OHE "These constraints are enforced mechanically via custom linters (Codex-generated, of course!) and structural tests." | none
A061 | SUPPORTED | evidence: AHL "tended to try to do too much at once"; later agent could "declare the job done"; claude-progress.txt, feature requirements file, initial git commit | none
A062 | SUPPORTED | evidence: REA abstract "in an interleaved manner, allowing for greater synergy between the two"; action "search[entity]" | quote is from the abstract, not §3.1 to §3.3
A063 | SUPPORTED | evidence: REA "We set 7 and 5 steps for HotpotQA and FEVER respectively as we find more steps will not improve ReAct performance"; "when ReAct fails to return an answer within given steps, back off to CoT-SC" | none
A064 | SUPPORTED | evidence: RER hotpotqa.ipynb and FEVER.ipynb both use `range(1, 8)` (7 steps) | none
A065 | SUPPORTED | evidence: REA Table 1 rows "ReAct 27.4 60.9" and "CoT-SC 33.4 60.4" | 33.4 - 27.4 = 6.0 EM points, correct
A066 | PARTLY | evidence: REA Table 2 "Reasoning error ... 47%", "Search result error ... 23%" for ReAct | the paper sampled 50 trajectories from ReAct and 50 from CoT with correct and incorrect answers (200 total); "50 failed runs" misstates the sample
A067 | SUPPORTED | evidence: TAR airline table "TC (gpt-4o) 0.420" and "ReAct (gpt-4o) 0.325" Pass^1 | none
A068 | SUPPORTED | evidence: TAU "a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials" | "chance that all k tries succeed" is the standard definition, not in the abstract
A069 | SUPPORTED | evidence: TAR retail "TC (claude-3-5-sonnet-20241022) 0.692 ... 0.462" (Pass^1 to Pass^4) | none
A070 | PARTLY | evidence: SWB README "Aug. 13, 2024: Introducing SWE-bench Verified! ... A subset of 500 problems that real software engineers have confirmed are solvable" with OpenAI Preparedness | "became the standard coding score" is not in SWB
A071 | PARTLY | evidence: SWX (Feb 23, 2026) "SWE-bench Verified is increasingly contaminated"; "59.4% of the 138 problems contained material issues in test design and/or problem description" | claim says "flawed tests" only; source says tests and/or problem description; the 138 were problems o3 did not consistently solve (a subset)
A072 | SUPPORTED | evidence: TBP "a carefully curated hard benchmark composed of 89 tasks in computer terminal environments"; "frontier models and agents score less than 65%"; v1 17 Jan 2026 | none
A073 | SUPPORTED | evidence: MTP "Claude 3.7 Sonnet have a 50% time horizon of around 50 minutes"; "doubling approximately every seven months since 2019"; v1 18 Mar 2025 | none
A074 | SUPPORTED | evidence: DSE sections on namespaces, control groups, capabilities | label only
A075 | SUPPORTED | evidence: DSE "By default Docker drops all capabilities except those needed, an allowlist instead of a denylist approach"; "remove all capabilities except those explicitly required for their processes"; MOB lists 14 | none
A076 | SUPPORTED | evidence: DSC "disables around 44 system calls out of 300+. It is moderately protective while providing wide application compatibility"; io_uring_* "Blocked due to security vulnerabilities that can be exploited to break out of containers"; "It is not recommended to change the default seccomp profile" | none
A077 | SUPPORTED | evidence: DSE "Docker containers are, by default, quite secure; especially if you run your processes as non-privileged users inside the container"; "may provide incomplete isolation, either independently, or when used in combination with kernel vulnerabilities" | none
A078 | SUPPORTED | evidence: DRR "Enables all Linux kernel capabilities", "Disables the default seccomp profile", "Disables the default AppArmor profile"; "A container with `--privileged` is not a securely sandboxed process." | none
A079 | PARTLY | evidence: DPI "The `docker` group grants root-level privileges to the user." | the quote is about docker group membership, not mounting the socket into a container; "anything that can reach the socket can start a privileged container" is not in DPI
A080 | SUPPORTED | evidence: DSE "User Namespaces ... This facility is available but not enabled by default." | root-in-container as default is not stated in DSE but is common knowledge
A081 | SUPPORTED | evidence: C19 NVD CVSS 3.1 8.6 (NIST), description "overwrite the host runc binary" (parenthetical is in the full NVD text but the fetch summary cut it off); RUN CHANGELOG 1.1.12 (2024-01-31) "a file descriptor that was leaked internally within runc"; C24 NVD 8.6 from GitHub CNA; RUN 1.2.8, 1.3.3, 1.4.0-rc.3 all 2025-11-05 "fixes for the following high-severity security issues" (CVE-2025-31133, -52565, -52881) | the C24 quote is in the runc CHANGELOG, not the NVD page
A082 | SUPPORTED | evidence: DNN, DRC, DRR, DSE each contain the options used (network none, cap-drop, no-new-privileges, read-only, pids-limit, memory, user) | none
A083 | PARTLY | evidence: DNN "only the loopback device is created"; DRC "If --memory-swap is set to the same value as --memory ... the container doesn't have access to swap"; DRR no-new-privileges "commands that raise privileges such as `su` or `sudo` no longer work" | DRR names su and sudo, not "setuid files"
## Summary
Counts: SUPPORTED 75, PARTLY 8, CONTRADICTED 0, NOT CHECKABLE 0.
Most important problems:
1. A066: ReAct Table 2 percentages (47%, 23%) are right, but the sample is 50 ReAct and 50 CoT trajectories with correct and incorrect answers, not "50 failed runs".
2. A071: "59.4% (about 82) had flawed tests" narrows the source, which says "material issues in test design and/or problem description", and the 138 were problems o3 did not consistently solve.
3. A079: "anything that can reach the socket can start a privileged container" and the socket-mount framing are not in DPI, which only says docker group membership grants root-level privileges.
4. A083 (and A082 by extension): DRR says no-new-privileges stops su or sudo, not setuid files in general.
5. A007, A004, A015, A070: explanations or comparisons added beyond the source (history resent each turn; gVisor/Firecracker as stronger boundaries; "three senses" of harness; SWE-bench Verified "became the standard").
Other notes: A035 WTA quote tail "rather than opaque error codes or tracebacks" was not shown in the fetch summary. A036's "lab cross-check (B2)" is not checkable from OAS. A051's "Docker-based evaluation harness" is in SWB docs, not the README.
Lookups used: 25 WebFetch calls (Anthropic/OpenAI/Fowler/Claude docs/arXiv/NVD/Gemini/OpenAI computer use). Local reads: openai-agents 0.23.1 and claude-agent-sdk 0.2.167 wheels, openai-agents-python docs, ReAct, tau-bench, SWE-bench, lm-evaluation-harness, codex, moby docker-v29.9.1, docker/docs, gVisor, runc, OWASP LLM repo, playwright-mcp, firecracker.

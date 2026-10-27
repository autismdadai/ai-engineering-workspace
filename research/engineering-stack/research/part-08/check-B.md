# Source check, set B (claims B001-B104)
B001 | SUPPORTED | evidence: intro_to_gvisor.md: "runs in userspace"; "written in memory-safe Go"; runsc named in the same page | none
B002 | SUPPORTED | evidence: intro_to_gvisor.md L41 "the workload is only one system call away from host compromise"; L150 "an attacker would need to simultaneously exploit the gVisor Sentry kernel *and* the host Linux kernel, which do not share any code" | source lists seccomp-bpf, AppArmor, Landlock, namespaces; claim says "only seccomp and namespaces" (minor)
B003 | SUPPORTED | evidence: intro_to_gvisor.md L156 "There are currently two supported platforms: Systrap (the default)... KVM"; architecture_guide/platforms.md "systrap replaced ptrace as the default gVisor platform in mid-2023"; "it is no longer supported" | none
B004 | SUPPORTED | evidence: filesystem.md L7 "communicate with their respective sentry using the LISAFS protocol"; L75 "Directfs is enabled by default in runsc"; g3doc/README.md L152 "via the 9P protocol" | "where the claim comes from" is inference, not in sources
B005 | SUPPORTED | evidence: security.md L85 "A sandbox is not a substitute for a secure architecture"; 2020 blog "We cannot guarantee that a container escape will never happen in gVisor"; security.md L238 "gVisor does not provide protection against hardware side channels" | none
B006 | SUPPORTED | evidence: performance.md L151 "This cost will principally impact applications that are system call bound" | none
B007 | SUPPORTED | evidence: quick_start/docker.md: "sudo runsc install", "sudo systemctl restart docker", "docker run --runtime=runsc"; debugging.md: --strace, log ending ".boot" | none
B008 | SUPPORTED | evidence: quick_start/docker.md L73 "this is easily replicated by an attacker so applications should never use dmesg to verify the runtime" | none
B009 | SUPPORTED | evidence: gvisor README L33-35 "Containers are not a sandbox... using them to run untrusted or potentially malicious code without additional isolation is not a good idea" | none
B010 | SUPPORTED | evidence: docker/docs engine/security/_index.md L270 "Docker containers are, by default, quite secure" | none
B011 | SUPPORTED | evidence: Firecracker README: "a virtual machine monitor (VMM) that uses the Linux Kernel Virtual Machine (KVM) to create and run microVMs"; "developed at Amazon Web Services... AWS Lambda... AWS Fargate" | none
B012 | SUPPORTED | evidence: SPECIFICATION.md: "<= 125 ms" InstanceStart to /sbin/init, serial console disabled, minimal kernel; "<= 5 MiB" with 1 CPU and 128 MiB; M5D.metal and M6G.metal; "enforced by integration tests" | none
B013 | SUPPORTED | evidence: firecracker-microvm.github.io: "Boot in <125ms", "<5 MiB overhead per VM", no hardware/vCPU/kernel conditions beside them | none
B014 | SUPPORTED | evidence: design.md: "Firecracker should be started only via the jailer binary"; "Firecracker does not perform any network traffic filtering... should be filtered at the host-level" | none
B015 | SUPPORTED | evidence: gVisor performance.md system-call cost; Firecracker runs a full guest (microVM with guest Linux kernel, SPECIFICATION.md 1 CPU/128 MiB guest) | "whole guest kernel per sandbox" is an inference from the VM design, not a quoted statement
B016 | SUPPORTED | evidence: e2b-dev/infra README L45 "One Firecracker microVM per sandbox"; e2b.dev/pricing: Hobby FREE with "$100 one-time usage credit", Pro "$150" /month | API-key requirement not in the README; taken from the e2b package/pricing context, not independently confirmed
B017 | PARTLY | evidence: modal.com sandboxes guide: "Sandboxes run on one of two runtimes" gVisor or VM; "Switch runtimes via the runtime parameter, or leave unset to let Modal choose for you." | page does not say gVisor is the default; it says Modal chooses when unset
B018 | SUPPORTED | evidence: code.claude.com sandboxing: "The sandbox is off by default"; macOS "Seatbelt"; Linux/WSL2 "bubblewrap and socat"; allowed domains "start empty", via a proxy on your machine | none
B019 | SUPPORTED | evidence: linux-sandbox/README: bubblewrap + seccomp, "legacy Landlock"; config_types.rs SandboxMode default ReadOnly; AskForApproval default OnRequest; SandboxWorkspaceWrite network_access defaults false; seatbelt.rs present | none
B020 | SUPPORTED | evidence: gemini-cli docs/cli/sandbox.md lists Seatbelt, Docker/Podman, runsc, LXC; configuration.md L3086 "Sandboxing is disabled by default" | none
B021 | SUPPORTED | evidence: sandboxing page: "Claude's file tools, MCP servers, and hooks run outside it" | none
B022 | SUPPORTED | evidence: sandboxing page table: "Most of the machine, including credential files such as ~/.ssh and ~/.aws/credentials" | quote truncated before the second example; acceptable
B023 | SUPPORTED | evidence: sandboxing page: "Claude Code runs commands without sandboxing"; sandbox.failIfUnavailable true makes it exit | none
B024 | SUPPORTED | evidence: sandboxing page: "Sandboxing reduces risk but is not a complete isolation boundary"; "can potentially use domain fronting or similar techniques to reach hosts outside the allowlist" | none
B025 | SUPPORTED | evidence: anthropic.com/engineering/claude-code-sandboxing: "In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%." No method given | none
B026 | SUPPORTED | evidence: codex-rs/utils/cli/src/shared_options.rs L53 "EXTREMELY DANGEROUS. Intended solely for running in environments that are externally sandboxed." | claim is a fragment; the flag it refers to is the dangerous bypass option
B027 | SUPPORTED | evidence: functions.rst "is **not** a security mechanism: the executed code can still access all builtins"; sys.rst audit hooks "not suitable for implementing a \"sandbox\""; runpy.rst "*not* a sandbox module"; ast.rst "That was misleading"; smolagents doc "no local python sandbox can ever be completely secure" and recommends remote execution (E2B, Docker) | none
B028 | SUPPORTED | evidence: computer-use docs: "referred to as the \"agent loop\"" | none
B029 | SUPPORTED | evidence: ACU: toolset {"type": "computer_toolset_20260801"}, "The request needs no beta header"; "17 member tools"; zoom; classifiers "will automatically scan what the tools return, such as screenshots, to flag potential prompt injections"; "Claude 5.5 and later models... return an error for the earlier computer_20251124 and computer_20250124" | source says "5.5 and later"; claim says "5.5 models"
B030 | SUPPORTED | evidence: OCU: "Text in a page, document, or tool result cannot grant permission or override the user's instructions."; actions click, double_click, drag, move, scroll, keypress, type, wait, screenshot; "For GPT-6 Astra, we recommend code execution" (PyAutoGUI or Playwright); links "Migration from computer-use-preview" | OCI page itself does not mention GPT-6 Astra or computer_use_preview; OCU does
B031 | SUPPORTED | evidence: GCU: "build browser, mobile, and desktop control agents"; "computer_use"; "If the safety_decision is require_confirmation, prompt the end user"; "is an opt-in feature. The default is false"; "As a Preview capability, Computer Use may contain errors and security vulnerabilities"; google-genai 2.31.0 types has enable_prompt_injection_detection | none
B032 | SUPPORTED | evidence: ACU cost section: toolset adds about 4,500 input tokens; older versions 466-499 system prompt tokens, ~735 per tool definition | none
B033 | SUPPORTED | evidence: ACU lists exactly four precautions (dedicated VM/container, no sensitive data, domain allowlist, human confirmation) | none
B034 | SUPPORTED | evidence: ACU: protection "won't be ideal for every use case (for example, use cases without a human in the loop)" | none
B035 | SUPPORTED | evidence: playwright-mcp README: "through structured accessibility snapshots, bypassing the need for screenshots or visually-tuned models"; PyPI playwright 1.64.0, Apache-2.0 | none
B036 | SUPPORTED | evidence: ACU: "In some circumstances, Claude will follow commands found in content even when they conflict with your instructions." | none
B037 | SUPPORTED | evidence: arXiv 2411.02391v2 abstract: "attack success rate (the frequency of the agent clicking the pop-ups) of 86% on average"; defenses "are ineffective" | OSWorld/VisualWebArena and "2024 models" not shown in the abstract text I retrieved
B038 | SUPPORTED | evidence: arXiv 2409.11295v5: "EIA achieves up to 70% ASR in stealing specific PII and 16% ASR for full user request"; abstract says "one of the most capable generalist web agent frameworks" | none
B039 | SUPPORTED | evidence: arXiv 2504.18575v3: "while attacks partially succeed in up to 86% of the case"; "often struggle to fully complete the attacker goals"; "security by incompetence" | none
B040 | SUPPORTED | evidence: claude.com article: "123 test cases representing 29 different attack scenarios"; "23.6%" to "11.2%"; all in autonomous mode; 23.6-11.2 = 12.4 points | none
B041 | SUPPORTED | evidence: Anthropic research post: Claude Opus 4.5, browser use, "1% attack success rate", adaptive attacker, "100 attempts per environment", "prompt injection is far from a solved problem" | none
B042 | SUPPORTED | evidence: OCU: "cannot grant permission or override the user's instructions" | none
B043 | SUPPORTED | evidence: OSWorld abstract: "369 computer tasks"; "humans can accomplish over 72.36% of the tasks"; test_nogdrive.json has 361 tasks (369 minus 8) | "of them" is ambiguous: the human figure is over all 369 tasks, not the 361
B044 | SUPPORTED | evidence: Sonnet 4.6 page: "OSWorld-Verified (released July 2025) is an in-place upgrade of the original OSWorld benchmark"; OSWorld README 2025-07-28 "fixed several issues reported by the community" | none
B045 | SUPPORTED | evidence: Opus 4.8 page footnote: "We made changes to how we run the OSWorld-Verified evaluation... and have updated the Opus 4.7 score to 82.3%." | none
B046 | SUPPORTED | evidence: arXiv 2606.29537: "108 long-horizon computer-use workflows"; "median of about 1.6 hours"; "completes only 20.6% of tasks" (submitted 2026-06-28) | none
B047 | SUPPORTED | evidence: Opus 5.5 page table: "OSWorld 2.1" "81.8%partial"; no footnote defines OSWorld 2.1 | none
B048 | PARTLY | evidence: WebArena run.py: --observation_type default "accessibility_tree"; test.raw.json has 812 entries | default is the agent's observation type, not how tasks are scored (scoring uses evaluators); "scored with" is wrong wording
B049 | SUPPORTED | evidence: ReAct Table 1 HotpotQA: CoT-SC 33.4, ReAct 27.4 (6.0 below); tau-bench README airline Pass^1: TC gpt-4o 0.420 vs ReAct gpt-4o 0.325 | none
B050 | SUPPORTED | evidence: ReAct: ReAct->CoT-SC limits 7 (HotpotQA) and 5 (FEVER); ysymyth/ReAct hotpotqa.ipynb and FEVER.ipynb both use "for i in range(1, 8)" (7 steps) | none
B051 | SUPPORTED | evidence: ReAct Table 2: reasoning error 47%; WTA: "rather than opaque error codes or tracebacks"; openai-agents 0.23.1 default_tool_error_function returns fixed "An error occurred while running the tool. Please try again." without exposing exception | none
B052 | SUPPORTED | evidence: OWASP LLM06: "require a human to approve high-impact actions before they are taken"; Agents SDK human_in_the_loop docs and Claude SDK canUseTool/permission modes support approval | none
B053 | SUPPORTED | evidence: BEA: loop with stopping conditions "such as a maximum number of iterations"; STOP lists stop reasons (tool_use, max_tokens, pause_turn, refusal etc.); HTC covers tool results/errors | none
B054 | SUPPORTED | evidence: Böckeler Apr 2 2026 article defines guides ("steer it before it acts") and sensors ("observe after the agent acts"); Feb 17 memo only uses the terms in a later-added paragraph that points to the fuller article, without defining them | nuance: the Feb 17 page does contain the words "guides and sensors" (see B103)
B055 | SUPPORTED | evidence: sandboxing page "off by default"; gemini-cli "Sandboxing is disabled by default"; security.md "A sandbox is not a substitute for a secure architecture" | none
B056 | SUPPORTED | evidence: intro_to_gvisor.md: application kernel, userspace, memory-safe Go, runsc | none
B057 | SUPPORTED | evidence: Docker security page "quite secure"; gVisor "only one system call away from host compromise"; shared kernel described in both | none
B058 | SUPPORTED | evidence: intro_to_gvisor.md: Systrap (seccomp-bpf interception, default) and KVM; platforms.md ptrace default replaced mid-2023, "no longer supported" | none
B059 | SUPPORTED | evidence: filesystem.md LISAFS and directfs on by default; g3doc/README.md still "9P protocol" | none
B060 | SUPPORTED | evidence: SPECIFICATION.md states hosts, 1 CPU/128 MiB, minimal kernel; website lists "<125ms" and "<5 MiB" with no conditions; gVisor performance.md for syscall cost | none
B061 | SUPPORTED | evidence: moby tag docker-v29.9.1 and docs release-notes 29.md "## 29.9.1"; gVisor tag release-20261005.0 (git ls-remote); quick_start/docker.md "sudo runsc install" | none
B062 | SUPPORTED | evidence: 2020 blog "We cannot guarantee that a container escape will never happen in gVisor"; security.md no protection against hardware side channels | none
B063 | SUPPORTED | evidence: gVisor README "without additional isolation is not a good idea"; Docker "quite secure"; debugging.md and docker.md give runsc procedure | none
B064 | SUPPORTED | evidence: OpenAI post (Feb 23 2026): "we have stopped reporting SWE-bench Verified scores, and we recommend that other model developers do so too"; SWE-bench README says Verified was built with OpenAI Preparedness | "retired" is loose: OpenAI stopped reporting; the benchmark itself is still maintained
B065 | SUPPORTED | evidence: NVD CVE-2024-21626: "due to an internal file descriptor leak... container escape"; runc CHANGELOG L1455 "a container breakout attack"; fixed in 1.1.12; CVSS 3.1 8.6 scored by CNA GitHub | none
B066 | SUPPORTED | evidence: ACH 23.6% to 11.2% (Aug 2025); API Opus 4.5 1% (Nov 2025) | none
B067 | SUPPORTED | evidence: git ls-remote tags and PyPI JSON confirmed (gvisor release-20261005.0, firecracker v1.17.0, moby docker-v29.9.1, docker/cli v29.9.1; playwright 1.64.0, e2b 2.56.0, openai-agents 0.23.1, claude-agent-sdk 0.2.167, anthropic 1.14.0) | none
B068 | SUPPORTED | evidence: docker/docs mac-install.md "more than 250 employees or more than $10 million USD in annual revenue... paid subscription"; Engine Apache License 2.0; 29.9.1 | Windows page says "OR"; Mac/get-docker wording ok
B069 | SUPPORTED | evidence: pricing: Hobby FREE "$100 one-time usage credit"; PyPI e2b 2.56.0, license MIT | none
B070 | SUPPORTED | evidence: HTC (tool_result is_error) and Agents SDK failure_error_function; consistent with WTA | none
B071 | SUPPORTED | evidence: sandbox off by default in Claude Code and Gemini CLI (both confirmed above) | none
B072 | SUPPORTED | evidence: E2B Firecracker microVM; Firecracker design.md jailer and host-level egress filtering; gVisor quick start; Modal sandbox runtimes gVisor or VM | none
B073 | SUPPORTED | evidence: runc CHANGELOG records CVE-2024-21626 fix in 1.1.12; advice is a recommendation | none
B074 | SUPPORTED | evidence: OWASP LLM06: "Implement authorization in downstream systems rather than relying on an LLM to decide if an action is allowed or not." | none
B075 | SUPPORTED | evidence: BEA: "we recommend finding the simplest solution possible, and only increasing complexity when needed"; "Agentic systems often trade latency and cost for better task performance" | none
B076 | SUPPORTED | evidence: playwright-mcp README: accessibility snapshots instead of screenshots | "when there's an API" is advice, not in PWM; reasonable opinion
B077 | SUPPORTED | evidence: OCU: "For GPT-6 Astra, we recommend code execution... uses a library such as PyAutoGUI or Playwright" | none
B078 | SUPPORTED | evidence: docker none driver page: "--network none... only the loopback device is created" | none
B079 | SUPPORTED | evidence: quick_start/docker.md: "sudo runsc install", restart Docker; user_guide/install.md exists (gvisor.dev/docs/user_guide/install/) | none
B080 | PARTLY | evidence: Python docs (functions.rst) confirm __builtins__ override is not a security mechanism | the demo's output row and version behaviour are not in any cited source and could not be checked
B081 | SUPPORTED | evidence: openai-cua-sample-app README L90 "A final answer does not prove the task succeeded." | none
B082 | SUPPORTED | evidence: Claude Agent SDK agent-loop docs: max_turns default "No limit"; openai-agents has DEFAULT_MAX_TURNS = 10; BEA mentions stopping conditions | none
B083 | SUPPORTED | evidence: WTA "rather than opaque error codes or tracebacks"; Agents SDK default hides exception | none
B084 | SUPPORTED | evidence: memory docs: "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook"; permissions.deny also listed | none
B085 | SUPPORTED | evidence: Docker security page and gVisor README positions as described | none
B086 | SUPPORTED | evidence: gVisor 2020 blog: "We cannot guarantee that a container escape will never happen in gVisor" | none
B087 | SUPPORTED | evidence: OSWorld abstract 72.36% human on original; Opus 5.5 reports "OSWorld 2.1" | none
B088 | SUPPORTED | evidence: STOP: truncated tool_use block on max_tokens -> "retry the request with a higher max_tokens" | "never run that call" is implied by the docs, not stated
B089 | SUPPORTED | evidence: STOP: pause_turn "while executing server tools such as web search" | none
B090 | SUPPORTED | evidence: openai-agents DEFAULT_MAX_TURNS = 10, MaxTurnsExceeded; Claude Agent SDK docs max turns default "No limit" | none
B091 | PARTLY | evidence: DRR has "--privileged" ("not a securely sandboxed process"), "--security-opt seccomp=unconfined" and a docker.sock mount example; linux-postinstall says docker group access equals Docker socket access | neither cited page flags --network host as a hazard; mounting the socket is only shown as an example
B092 | SUPPORTED | evidence: filesystem.md LISAFS + directfs default; g3doc/README.md "9P" | none
B093 | SUPPORTED | evidence: ACU: protection "won't be ideal for every use case (for example, use cases without a human in the loop)" | "nobody to ask" is a paraphrase
B094 | SUPPORTED | evidence: both Anthropic pages exist with those titles | none
B095 | SUPPORTED | evidence: martinfowler.com/articles/harness-engineering.html, Apr 2 2026 | none
B096 | SUPPORTED | evidence: both pages exist (Docker Engine security; gVisor architecture_guide/security.md) | none
B097 | SUPPORTED | evidence: ACU page has security guidance and precautions | none
B098 | SUPPORTED | evidence: OpenAI stopped reporting SWE-bench Verified (Feb 23 2026); OSWorld, Verified, 2.0, 2.1 seen; Opus 4.8 footnote re-score | none
B099 | SUPPORTED | evidence: ACH 123 cases internal; API Opus 4.5 internal; CSP 84% no method; MRS "agents typically use about 4x more tokens than chat" with no method given | none
B100 | SUPPORTED | evidence: arXiv 2409.11295v5 (2024-09, rev 2025-03), 2411.02391v2, 2504.18575v3; none shows a venue in its arXiv Comments | none
B101 | SUPPORTED | evidence: gVisor README vs Docker "quite secure" | none
B102 | SUPPORTED | evidence: SDL: "max_turns... counts tool-use turns only"; types.py max_turns: "A turn consists of a user message and assistant response"; ReAct paper FEVER cap 5 vs code range(1, 8) | none
B103 | PARTLY | evidence: Böckeler Apr 2 2026 defines guides and sensors; SPECIFICATION.md has test conditions; gVisor README "without additional isolation is not a good idea" | the Feb 17 memo page does contain the words "guides and sensors" (in a later-added paragraph), so "date from April 2, not February 17" is true of the definition only
B104 | SUPPORTED | evidence: ReAct Table 1: CoT 29.4, ReAct 27.4; abstract: "absolute success rate of 34% and 10%" on ALFWorld and WebShop | none
## Summary
Counts: SUPPORTED 99, PARTLY 5, CONTRADICTED 0, NOT CHECKABLE 0 (total 104).
Top problems:
1. B103/B054: the Feb 17, 2026 Böckeler memo page does contain "guides and sensors" (in an added paragraph pointing to the April article); the April article is where they are defined. Wording "date from April 2, not February 17" needs softening.
2. B048: WebArena default is the accessibility-tree observation type, not how tasks are scored.
3. B017: Modal docs do not state that gVisor is the default runtime ("leave unset to let Modal choose for you").
4. B091: the cited Docker pages do not flag --network host as a hazard; socket mounting appears only as an example.
5. B080: the demo's output row cannot be checked against any cited source; also minor looseness in B043 (72.36% is over all 369 tasks), B064 ("retired" vs OpenAI stopped reporting), B029 ("5.5 and later").
Lookups used: about 33 web lookups (WebFetch); the rest read locally from cloned repos, PyPI JSON, and the google-genai/openai-agents/claude-agent-sdk wheels.

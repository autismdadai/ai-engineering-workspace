# Verification of skills-hosts findings (2026-10-16 run)

Format: id | verdict | quote | URL

Status: complete. Lookup cap 15 (web fetches) reached after N11. N12 and N13 not reached. Local files were not re-checked. Quotes kept short.

H06 | CONFIRMED | "`compatibility` | No | Max 500 characters." | https://agentskills.io/specification
Reason: Spec table lists name and description as required (Yes); license, compatibility, metadata and allowed-tools as optional (No). Finding's proposed correction matches. No host-only fields appear in the spec.

H08 | CONFIRMED | "Cannot contain reserved words: "anthropic", "claude"" | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
Reason: Anthropic page lists "Cannot contain XML tags" for name and description, and the reserved-word rule for name only. The agentskills.io spec (H06) has neither rule, so these are not spec rules. The local-validator half of the finding is not checked here (see N12, not reached).

H11 | CONFIRMED | "uses at most 2% of the model's context window" and "8,000 characters when the context window is unknown" | https://learn.chatgpt.com/docs/build-skills
Reason: Budget wording matches the proposed fix. Repo scan is "every directory from your current working directory up to the repository root", wider than the finding's "$CWD/.agents/skills". User and admin paths were not in the fetched text.

H14 | CONFIRMED | "Claude won't load the skill automatically" | https://code.claude.com/docs/en/skills
Reason: Claude Code doc says the flag stops automatic loading and is for side-effect workflows such as deploys. The finding's exact wording ("Set to true to prevent...") did not appear in the fetched text. Codex half confirmed by N08 (allow_implicit_invocation in agents/openai.yaml). Cursor half confirmed by N10 (disable-model-invocation in Cursor frontmatter).

N01 | UNCERTAIN | "Upload a ZIP file containing your skill folder." | https://support.claude.com/en/articles/12512180-use-skills-in-claude
Reason: Seen and confirmed: ZIP upload; "With Code execution and file creation on" setting; "Specific people: Enter names or emails to share directly."; plans "Free, Pro, Max, Team, and Enterprise". Not seen in the fetched text: the menu path (Customize > Skills > + > Create skill), the on/off toggle and the "/" picker. The claude.com/docs plan list is not verified here; the Anthropic overview (H08) says custom Skills are "Available on Pro, Max, Team, and Enterprise plans". Lookup budget did not allow a second read, so the menu path stays UNCERTAIN.

N02 | CONFIRMED | "Run /reload-plugins in that session to load it" | https://claude.com/docs/plugins/overview
Reason: Page confirms Customize > Plugins with Discover, Add > Add marketplace (Git URL or owner/repo) and Add > Upload plugin (.zip or .plugin, one .claude-plugin/plugin.json). Skills run in chat, Cowork and Claude Code. Account plugins sync to Claude Code on next signed-in session. Team and Enterprise can share with specific people or publish to the org.

N03 | CONFIRMED | "enabled by default for everyone" | https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization
Reason: Confirmed: "Navigate to Organization settings > Plugins & skills"; Team and Enterprise; owner-provisioned skills on by default and users can toggle them off; group distribution is Enterprise only via a plugin assigned to a group. Scanning: "Scanning is off by default until October 2, 2026", which matches the finding's date and default-on. The "third-party" and "Enterprise orgs that have not set it" scope words were not visible in the fetched text.

N04 | CONFIRMED | "Claude Code downloads synced skills and never uploads them." | https://code.claude.com/docs/en/skills
Reason: Confirmed: downloads into ~/.claude/skills/synced/; sync only in a session signed in with a claude.ai account via /login; "Syncing in terminal sessions requires Claude Code v2.1.273 or later."; API key and Bedrock sessions do not sync; edits can be overwritten; "syncClaudeAiSkills" set to false in user settings stops syncing.

N05 | CONFIRMED | "claude.ai does not support centralized admin management or org-wide distribution of custom Skills." | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
Reason: Reuses the H08 fetch of the same page (no extra lookup). The API overview says custom Skills do not sync across surfaces, claude.ai skills are individual, and claude.ai has no org-wide distribution. The Help Center describes Owner provisioning (N03), sharing with specific people (N01) and the Claude Code sync (N04), so the pages do conflict. The Free plan appears in the Help Center (N01) and not on the platform pages' claude.ai plan list ("Pro, Max, Team, and Enterprise").

N06 | CONFIRMED | "Only `description` is recommended" | https://code.claude.com/docs/en/skills
Reason: Confirmed: all fields optional, description recommended; name "Defaults to the directory name."; combined description and when_to_use truncated at 1,536 characters in the listing; "claude plugin validate .claude/skills" finds SKILL.md files whose frontmatter does not parse, "Requires Claude Code v2.1.233 or later."; skill edits take effect without restart. Extra fields seen: when_to_use, arguments, disable-model-invocation, user-invocable, model, effort, paths, hooks, shell, context (fork), agent, background. The names argument-hint and disallowed-tools were not found in the text read.

N07 | CONFIRMED | "Custom Skills are accessible to your entire workspace, not scoped to an end user" | https://platform.claude.com/docs/en/build-with-claude/skills-guide
Reason: Seen: container.skills entries with "type", "skill_id" and optional "version"; version format "Date-based: 20251013 or latest" for Anthropic and "skver_01AbCdEfGhIjKlMnOpQrStUv" IDs for custom. Workspace-wide scope confirmed. Platform parity on AWS and Foundry and "not covered by ZDR" are on the Anthropic overview page (H08 fetch). The beta-header claim: no beta header appears in the container example shown; the rest of the guide (after 100,000 characters) was not read.

N08 | CONFIRMED | "For reusable distribution of your own skills, prefer plugins." | https://learn.chatgpt.com/docs/build-skills
Reason: All seven points seen: $skill-installer for curated skills; prefer plugins for reusable distribution; [[skills.config]] enabled = false in ~/.codex/config.toml; agents/openai.yaml holds UI metadata, invocation policy and tool dependencies, with allow_implicit_invocation default true; symlinked skill folders followed; changes detected automatically, restart if not; /skills or $ to mention a skill.

N09 | CONFIRMED | "Maximum zip upload size is 50 MB." | https://developers.openai.com/api/docs/guides/tools-skills
Reason: Seen: skills attach via tools[].environment.skills on the shell tool; inline base64 zip bundle in the environment skills array instead of a hosted skill; "Maximum file count per skill version is 500."; "Maximum uncompressed file size is 25 MB."; front matter validation follows the agent skills specification.

N10 | CONFIRMED | "includes a built-in /migrate-to-skills skill in 2.4" | https://cursor.com/docs/context/skills
Reason: Seen: frontmatter fields name, description, paths, disable-model-invocation, icon, color, metadata; built-in /migrate-to-skills in 2.4; GitHub import by packaging as a plugin or "From GitHub Repository"; team marketplace publishing; loads .claude/skills, .codex/skills and their ~/ equivalents.

N11 | CONFIRMED | "Start with 2-3 test cases." | https://agentskills.io/skill-creation/evaluating-skills
Reason: Seen: evals/evals.json with skill_name and evals[] (id, prompt, expected_output, files, assertions); run each test case with and without the skill; start with 2-3 test cases. Not checked (lookup cap reached): the skills-ref README "demonstration only" statement and the 40+ adopting clients list. Those side claims stay unverified.

N12 | UNCERTAIN | not reached | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
Reason: Not reached: lookup cap of 15 was used up by N11. The local validators (validate_skill.sh, skill_audit.py) were not re-read. The Anthropic rules needed for the comparison (XML tags, reserved words, 64/1024 limits, claude.ai 200-character description cap, compatibility 500) are partly seen in H08 and H06, but the claude.ai 200-character cap was not seen in the fetched text.

N13 | UNCERTAIN | not reached | https://support.claude.com/en/articles/12512180-use-skills-in-claude
Reason: Not reached: lookup cap of 15 was used up. The Microsoft 365 add-in claim was not checked.

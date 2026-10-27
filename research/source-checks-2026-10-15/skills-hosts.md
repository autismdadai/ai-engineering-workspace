# skills-hosts report (date read 2026-10-15)
Status: COMPLETE. Lookups used: 25 of 25 (one was a 308 redirect from developers.openai.com/codex/skills to learn.chatgpt.com/docs/build-skills; I followed it, same OpenAI docs). All 17 claims checked.

Sources used (primary only):
- https://agentskills.io/home , https://agentskills.io/specification , https://agentskills.io/skill-creation/evaluating-skills , https://github.com/agentskills/agentskills/tree/main/skills-ref
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview , .../best-practices , https://platform.claude.com/docs/en/build-with-claude/skills-guide
- https://code.claude.com/docs/en/skills , https://code.claude.com/docs/en/plugins
- https://support.claude.com/en/articles/12512198-creating-custom-skills , .../12512180-use-skills-in-claude , .../13119606-provision-and-manage-skills-for-your-organization
- https://claude.com/docs/skills/overview , https://claude.com/docs/plugins/overview
- https://learn.chatgpt.com/docs/build-skills (Codex), https://developers.openai.com/api/docs/guides/tools-skills (OpenAI API)
- https://cursor.com/docs/context/skills

## Claim grades
| id | grade | what the source says |
|---|---|---|
| H01 | SUPPORTED | "a skill is a folder containing a SKILL.md file"; "originally developed by Anthropic ... released as an open standard" (agentskills.io/home). |
| H02 | SUPPORTED | Spec: metadata ~100 tokens (name+description) loaded at startup; body "< 5000 tokens recommended" on activation. Home page: discovery stage loads "only the name and description". Anthropic overview: "~100 tokens per Skill". |
| H03 | SUPPORTED | Spec: 1-64 chars; unicode lowercase alphanumeric and hyphens; no leading/trailing hyphen; no "--"; must match parent directory. |
| H04 | SUPPORTED | Spec: description 1-1024. Claude Help Center "Creating custom skills": name "(64 characters maximum)", description "(200 characters maximum)". Anthropic API docs still say 1,024, so 200 is a claude.ai upload rule. |
| H05 | SUPPORTED (a recommendation) | Spec: "Keep your main SKILL.md under 500 lines." Best practices: "under 500 lines for optimal performance". |
| H06 | PARTIAL | Spec fields: name (required), description (required), license, compatibility (max 500 chars), metadata (string-to-string map), allowed-tools (space-separated, Experimental). The files do not list compatibility or allowed-tools in the fields table. |
| H07 | SUPPORTED | Spec: scripts/, references/, assets/ are optional conventions; "any additional files or directories" allowed. evals/ is not named in the spec. But the agentskills.io guide says "Store test cases in evals/evals.json". |
| H08 | PARTIAL | Not in the open spec. Anthropic docs: name and description "Cannot contain XML tags"; name "Cannot contain reserved words: anthropic, claude". Host rule. Their validators check neither. |
| H09 | SUPPORTED | "up to 20 Skills for each request"; "Total upload size must be under 30 MB (uncompressed)"; /v1/skills; container with type anthropic or custom, skill_id, version; API "No network access", "No runtime package installation". |
| H10 | SUPPORTED | ~/.claude/skills/<name>/SKILL.md (personal); "The budget scales at 1% of the model's context window" (settable via skillListingBudgetFraction or SLASH_COMMAND_TOOL_CHAR_BUDGET); each entry capped at 1,536 chars; Claude Code "Full network access". |
| H11 | PARTIAL | Repo $CWD/.agents/skills, user $HOME/.agents/skills, admin /etc/codex/skills. Budget: "at most 2% of the model's context window, or 8,000 characters when the context window is unknown" (8,000 is the fallback, not an alternative cap). |
| H12 | SUPPORTED | "Maximum zip upload size is 50 MB." "Maximum file count per skill version is 500." Also "Maximum uncompressed file size is 25 MB." |
| H13 | SUPPORTED | Project .agents/skills/ and .cursor/skills/; user ~/.agents/skills/ and ~/.cursor/skills/; also loads .claude/skills/ and .codex/skills/ (and ~ versions). |
| H14 | PARTIAL | disable-model-invocation: true works in Claude Code and Cursor (not in the open spec). Codex has no such frontmatter; it uses agents/openai.yaml allow_implicit_invocation (default true). |
| H15 | SUPPORTED | Spec: "Experimental. Support for this field may vary". Claude Code: allowed-tools "does not restrict which tools are available: every tool remains callable"; permission settings still govern. "Not a security boundary" is the files' wording, consistent with this. |
| H16 | SUPPORTED, with caveat | Spec: `skills-ref validate ./my-skill`. The repo README: "intended for demonstration purposes only ... not meant to be used in production." |
| H17 | SUPPORTED | Best practices: "Always write in third person. The description is injected into the system prompt". Anthropic advice, not in the open spec. |

## New findings (most useful first)
1. claude.ai and Claude desktop install: Customize > Skills > + > Create skill > Upload a skill > ZIP; toggle on/off; "/" menu in chat. Needs "Code execution and file creation" on. Team/Enterprise can share with "Specific people". 
2. Plugins on claude.ai and desktop: Customize > Plugins > Discover, Add > Add marketplace (Git repo), Add > Upload plugin (.zip or .plugin with one .claude-plugin/plugin.json). A plugin's skills work in chat, Cowork and Claude Code; plugins saved to the account sync to Claude Code. Team/Enterprise can share a plugin with specific people or publish to the org.
3. Org-wide skills: Organization settings > Plugins & skills (Team and Enterprise). Owner-provisioned skills are on by default, users can toggle off. Group-specific only on Enterprise via a plugin assigned to a group. Skill scanning for third-party skills: default on from 2 Oct 2026 for Enterprise.
4. Claude Code now syncs your claude.ai skills (download-only) into ~/.claude/skills/synced/ when signed in via /login with a claude.ai account (v2.1.273+); turn off with syncClaudeAiSkills=false.
5. Anthropic's own pages disagree. API overview says skills do not sync across surfaces, claude.ai is individual-only, and no org-wide distribution; Help Center and Claude Code docs show sync and org provisioning. Plan list also differs: Help Center says Free, Pro, Max, Team, Enterprise; claude.com/docs/skills/overview says Pro, Max, Team, Enterprise. Treat the newer, more specific pages as current.
6. Claude Code frontmatter is wider and looser than the spec: all fields optional (description "recommended"), name defaults to folder name. Extra fields: when_to_use, arguments, argument-hint, disable-model-invocation, user-invocable, disallowed-tools, model, effort, context (fork), agent, background, hooks, paths, shell. `claude plugin validate .claude/skills` checks frontmatter (v2.1.233+). Skills reload live; nested .claude/skills load on demand; managed enterprise skills directory exists.
7. Claude API: no beta header shown in the current examples (only anthropic-version); custom skills are workspace-wide; also on Claude Platform on AWS and Microsoft Foundry; Skills are not ZDR-covered.
8. Codex: $skill-installer for curated skills; plugins preferred for distribution; disable with [[skills.config]] enabled=false in ~/.codex/config.toml; agents/openai.yaml (allow_implicit_invocation, interface, dependencies); follows symlinked skill folders; /skills or $ to mention.
9. OpenAI API: attach via tools[].environment.skills on the shell tool; inline base64 zip allowed; front matter follows the Agent Skills spec.
10. Cursor: extra fields paths, icon, color; built-in /migrate-to-skills (2.4); import from GitHub via plugin or Customize > From GitHub Repository; share via team marketplace.
11. agentskills.io: documents an evals/evals.json layout (prompt, expected_output, files, assertions; compare with and without skill); lists 40+ adopting clients; spec name rule says "unicode" lowercase alphanumeric.
12. Skills also work in Microsoft 365 add-ins (Excel, PowerPoint, Word, Outlook), per Help Center.

## Not verified (no lookup left)
Claude Desktop specifics beyond "Customize" being shared with claude.ai (no separate desktop skills page read); Cursor description length limits (none stated on page read); Codex name/description length limits (page states none).

## Corrections for the files (one line each)
See the recommendations list returned with this report.

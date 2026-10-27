# Deep Research Prompt: The AI Engineering Stack

*Saved October 9, 2026 from the chat that started this series, so later sessions can re-read it. The prompt below is verbatim. To resume: read this file and claude/engineering-stack-progress.md, then continue from the next step.*

```text
DEEP RESEARCH: THE AI ENGINEERING STACK
The next parts of the project's paper series

GOAL
The attached PDF, "The Modern AI Engineering Stack"
(made with Gemini Deep Research), covers 12 engineering
pillars and 4 advanced blueprints. Turn it into a
verified, teachable, multi-part paper in the style of
the project's seven-axis taxonomy paper. For every
topic: a plain-language explanation, definitions, real
examples, step-by-step procedures, what to download to
run it, which tool is the best pick and for whom, and
teaching material. Check every claim against a source
you opened. Test every procedure and code sample. Where
something can't be verified or tested, say so and why.

The Gemini PDF is a map of claims to check, not a
source. It's AI-written, the lowest trust class here.

The project instructions apply throughout; this prompt
adds to them. Use as many skills and agents as
genuinely help, as set out in HOW TO WORK.

READ FIRST
Read in full: claude/project-file-map.md and the newest
claude/handoff-*.md. For the others, read the headings,
then the sections the current phase needs.
1. The seven-axis taxonomy paper
   (claude/taxonomy-of-prompt-engineering-3e.md, unless
   the map names another file): the model for
   structure, depth, tone and appendices, including
   Appendix A's key figures with scope.
2. claude/portable-research-prompt.md and
   claude/research-verification-toolkit.md: research
   rules, evidence grades, claim-by-claim checks.
3. claude/multi-lens-review-method.md: independent
   viewpoints, a blind verifier, dissent kept.
4. claude/edition-protocol-v3.md: the fidelity test,
   the six acceptance tests, section 9 on usage budget.
5. claude/github-tutor-prompt.md: the model for
   teaching (skip its ABOUT ME block).
6. claude/fabel-prompt-audit.md: the finding format.
7. Existing work to link instead of re-teaching:
   claude/prompt-construction-guide-2e.md (prompting),
   claude/agent-skills-reference-v1-2.md and
   claude/skills-booklet.md (agents and skills),
   claude/new-skills-appendix.md (skill ideas),
   skills/quantum-entanglement-lab/evals/ (tests
   proven able to fail).
If a file is missing, say so and don't describe it.

RULES FOR THIS JOB
1. Cite only what you opened in this session. Give the
   URL (plus DOI or arXiv ID when there is one) and
   where the claim sits (page, section or heading).
   Name each source's class: official spec or docs,
   peer-reviewed, preprint, vendor blog or comparison,
   AI-written. A vendor's docs are authoritative on how
   its product works; its speed and quality claims are
   marketing until someone else measures them.
2. Give every number its scope (model, hardware,
   benchmark, version, date). Label made-up example
   numbers as illustrative.
3. Check anything that changes over time (versions,
   prices, model names, deprecations, which hardware is
   current) on the run date, and log it in the
   freshness ledger.
4. Tag claims and procedures, per claim or per
   paragraph when one source covers it (or use the
   taxonomy paper's convention if it has one):
   [V] verified against an opened source, with grade
   [T] tested: you ran it here; output captured
   [R] reader test: can't run here (say why); exact
       test and expected result given
   [U] unverified: say what would settle it
   [I] illustrative, not a measured result
5. Where this work disagrees with an existing project
   doc, flag it and settle it from primary sources.
   Don't silently change either one.
6. Downloads come only from official sources: the
   project's own site, its official GitHub releases, or
   its official PyPI or npm package. Give license,
   cost, OS support and hardware needs. Use checksums
   or signatures where published. Read any install
   script before running it, and teach the reader to do
   the same instead of piping a web script into a
   shell.
7. Security and guardrail topics teach defense:
   published, harmless test cases; scans only of
   systems you own; no new jailbreaks or exploit code;
   placeholders and environment variables, never real
   keys.
8. Legal and compliance claims (licenses, privacy and
   health rules) get careful scope and a
   not-legal-advice note.
9. Don't create accounts, pay for anything, or add
   source PDFs to the project without asking me.

HOW TO WORK
- You lead: plan, write, integrate and make the final
  calls. You have my go-ahead to use subagents, but
  only for work that is parallel and separable, or for
  independent checking. Before each fan-out, say how
  many agents and the rough usage cost. Roles that earn
  their cost:
  a) Topic researchers, one per topic or group, in
     parallel. Each returns a claim table (claim,
     source, class, location, verdict), not prose.
  b) Blind verifier: gets only the claims and their
     sources, never your drafts or reasoning, and
     re-checks each one. Real disagreements stay in
     the paper.
  c) Learner-tester: a fresh agent with no context that
     follows each setup guide and lab literally, in a
     clean folder and a fresh virtual environment, the
     way a beginner would, and reports every step that
     fails or confuses.
  d) Security reviewer for the security and guardrail
     topics: unsafe content and overclaims about
     protection.
- Skills: use the deep-research skill, if listed, for
  the research legs (this prompt sets the paper's
  format, not the skill). Use pdf-reading or
  file-reading for the Gemini PDF. Use any other skill
  that clearly helps, and say which.
- Run code instead of predicting its output. Record
  OS, Python version, package versions and date for
  every test.
- Budget: follow section 9 of the edition protocol. If
  the session gets long, finish the current step, save,
  update the progress file and tell me.

PHASE 0: SET UP
1. Save this prompt as claude/engineering-stack-prompt.md
   so later sessions can re-read it.
2. Convert the Gemini PDF to Markdown, keeping its
   formulas and all 33 works cited. Rebuild its tables
   from the page images, since text extraction
   scrambles them. Save it as
   ai-reports/gemini-ai-engineering-stack.md. Don't add
   the PDF itself to the project.
3. Check your workspace: Python version, whether pip
   and npm installs work, whether model and dataset
   hosts are reachable, whether there's a GPU. List
   which kinds of tests can run here and which can't;
   this decides [T] versus [R].
4. Add the new files to claude/project-file-map.md and
   note the project knowledge counter (project_info).
   Report it after each part, and warn me before a save
   would take it near the limit.

PHASE 1: AUDIT THE GEMINI PAPER
Build claude/engineering-stack-claim-ledger.md, one row
per factual claim, number, formula, named tool and
citation: ID, section, claim (paraphrased), type,
Gemini's citation, whether it opens and supports the
claim, primary source, class, verdict (confirmed,
corrected, outdated, overstated, unsupported,
illustrative), grade, note.
- The text seems to have no inline citation markers;
  check the pages. If so, match claims to the 33 works
  cited by topic and mark each match "inferred".
- Open all 33 citations. Replace mirrors, copies and
  blogs (ResearchGate, alphaXiv, Hugging Face copies,
  vendor comparison posts) with the primary paper,
  official docs or datasheet. Flag citations that
  don't resolve or don't say what they're cited for.
- Flag absolute words ("definitively", "deterministic",
  "near-zero", "zero-latency", "drastically") and check
  whether any source supports them.
- Check each formula against its primary paper.
- Check the terms: is each pillar name established?
  Who uses it, and does Gemini's definition match
  common use (for example, "harness engineering")?
- Settle quick freshness checks now and deep checks
  when you build each topic. Questions the ledger must
  answer (questions, not conclusions):
  - Induction heads: is that work peer-reviewed, how
    strong is its evidence for large models, and what
    did later studies find?
  - Does "lost in the middle" still hold for current
    long-context models? Which ones?
  - H100 SXM5 against NVIDIA's datasheet: 3,958 TFLOPS
    at which precision, with or without sparsity, and
    what's the dense figure? 132 SMs enabled out of how
    many? Is H100 still current on the run date?
  - Still current? Llama Guard 3, the OpenAI Assistants
    API, LangServe, GPT-4 as a judge, Llama 3 8B as the
    local example, the OWASP Top 10 for LLMs edition,
    the Colang version.
  - Does the PagedAttention paper say "near-zero" waste
    or give a number?
  - Where does "doubling tokens per second" for
    speculative decoding come from, and for which
    models?
  - Is the "15%" MIPROv2 gain sourced or illustrative?
  - Does local processing alone make medical
    summarization HIPAA compliant, as the Blueprint 4
    example implies?
  - Are NeMo Guardrails rails deterministic, or do some
    call an LLM?
  - Do the LangGraph and CrewAI comparisons hold for
    current versions, judged from official docs rather
    than blogs?
- Finish with an errata summary: what the Gemini paper
  got right, wrong, outdated and overstated, counted by
  pillar. Put its known problems in its file-map entry.

PHASE 2: SCOPE, STRUCTURE AND PLAN
1. Structure: find overlaps (context, memory and
   retrieval; harness and eval; agents, orchestration
   and multi-agent) and gaps. Candidate gaps to check,
   not assume: Model Context Protocol (MCP) and other
   tool and agent protocols; Agent Skills (link the
   project's references); fine-tuning, and when to
   fine-tune versus prompt versus retrieve;
   observability and tracing; cost and latency
   (provider prompt caching, batching, model routing);
   reasoning models and how they change prompting;
   structured outputs and tool calling; building
   evaluation data; multimodal and computer-use agents;
   data governance and licensing; human-in-the-loop
   design. Recommend what to add, merge or drop, with
   reasons.
2. Axes: test whether axes like the taxonomy paper's
   can classify the stack (for instance: layer, what it
   changes, hardware needed, cost, maturity, risk).
   Keep an axis only if every topic places on it
   cleanly, and show that test. If axes don't fit, say
   why and use another structure.
3. Learning map: prerequisites between topics, a
   recommended order, and three paths per topic: no
   install (browser or hosted), ordinary laptop (CPU,
   Apple Silicon or a consumer GPU), and cloud or
   production. Plan one shared setup chapter for what
   most parts need (Python, virtual environments, Git,
   an editor, safe API-key handling), so each part only
   adds what's new.
4. Part plan: which topics go in which part, each sized
   to be researched, tested and saved in one session;
   file names; agents and rough cost per part. Number
   the parts to continue the project's paper series if
   the map or handoff shows a numbering; otherwise
   start a new paper, and say which you chose.
5. Show me, in about 15 lines with your reasoning: the
   audit's headline findings, proposed scope changes,
   the part plan, the cost, and anything you need from
   me. Scope changes are expensive to redo later, so
   wait for my go before Phase 3.

PHASE 3: BUILD EACH PART
Open each part with the date, the counts of [V] [T] [R]
[U] [I], and what's still open. Then for each topic,
adapting headings to the taxonomy paper's style:
1. In plain words: what it is, the problem it solves,
   an everyday analogy, where it sits in the stack.
2. Definitions: each term in plain words, then the
   technical term. Every term also goes in the
   glossary.
3. How it works: the mechanism step by step; each
   formula explained symbol by symbol, with a worked
   example run in code (for instance reciprocal rank
   fusion on two ranked lists, semantic entropy on a
   toy split, the speculative decoding speedup, KV
   cache size, memory for a quantized model); a Mermaid
   diagram where it helps (check that it renders, or at
   least parses). Where a calculation recurs, ship it
   as a small tested script the reader can reuse.
4. Gemini said, evidence says: a short table from the
   ledger.
5. Examples: at least three real ones with sources,
   and one fully worked example (input, steps, output).
   Label invented ones illustrative.
6. What you need: a table of the tools: what each is
   for, required or optional, license, cost, OS,
   minimum and recommended hardware, account or API key
   needed, maintained or not, official download link,
   version and date checked. Then the picks: best
   default for a solo builder on an ordinary computer,
   best for production, best free option. Judge on fit
   for the job, maintenance (recent releases, active
   issues), license, cost, hardware, documentation,
   security record and lock-in, and show the evidence.
   Say when not to use it and name the strongest
   alternative. If the evidence doesn't support a
   single best, say so.
7. Set it up: steps for Windows, macOS and Linux
   (steps you couldn't run are [R], taken from official
   docs); how to check it worked (command and expected
   output); a quick tour of the commands or functions
   used most; common errors and fixes; how to
   uninstall.
8. Hands-on lab: goal, prerequisites, time, cost,
   pinned versions, steps, code, expected output
   captured from your run, an automated check, and a
   break-it-on-purpose step proving the check can fail.
9. Teach it: learning objectives, prerequisites,
   common misconceptions, exercises with checked
   answers, a five-question self-check, "you've got it
   when" criteria, the best next resources (official
   tutorials and primary papers, checked to exist), a
   short tutor prompt the reader can paste into Claude
   to practice (modeled on claude/github-tutor-prompt.md),
   and what to learn next.
10. Limits and debates: counter-evidence, failure
    modes, cost, when this is the wrong tool, open
    questions.
11. Skill opportunity (optional, one paragraph): could
    this become a project skill? Link the matching idea
    in claude/new-skills-appendix.md if there is one.
12. Sources: primary first, each with its class and
    the location used.
Close each part with a one-page cheat sheet: key terms,
commands and decision rules.

PHASE 4: CHECK EACH PART BEFORE SAVING IT
1. The blind verifier re-checks every [V] claim. The
   learner-tester runs every setup guide and lab from a
   clean start. Fix what they find; keep real
   disagreements visible.
2. Every code block ran here [T] or is marked [R] with
   a reader test. Every link was opened. Every number
   has its scope. Every tool's version and date were
   checked.
3. Report findings in the claude/fabel-prompt-audit.md
   format.
4. Write the tests that need my computer so Claude Code
   can run them with one command from a folder, and
   list them in the part's "Run on your computer"
   section. When I send results back, change [R] to [T]
   with the date.

PHASE 5: ASSEMBLE (after the last part)
- Front matter: an overview linking all parts, reading
  routes (learn from scratch, build something this
  week, look up a tool), and how this paper connects to
  the taxonomy paper and the prompt guide.
- Appendices: glossary; key figures with scope (like
  the taxonomy paper's Appendix A); one tool and
  download index across all parts; decision guides
  (for example: prompt, retrieve or fine-tune; one
  agent or several; local or cloud); the learning
  path; errata for the Gemini paper; the freshness
  ledger; what's still unverified; skill opportunities.
- Run the six acceptance tests in
  claude/edition-protocol-v3.md, plus: no untagged
  claims, no unscoped numbers, no unopened sources, no
  em dashes, no personal details. Report pass or fail
  for each.
- Recommend the separate-session review the edition
  protocol calls for.

SAVING AND RESUMING
- Save each part as .md in the project as soon as it
  passes Phase 4 (not as a Docs artifact or Word
  file): claude/engineering-stack-part-NN-<topic>.md,
  plus claude/engineering-stack-claim-ledger.md,
  claude/engineering-stack-glossary.md,
  claude/engineering-stack-freshness-ledger.md (each
  time-sensitive fact, the date checked, the URL to
  re-check) and claude/engineering-stack-progress.md
  (done, in progress, next, open questions,
  unverified). Use the map's naming convention instead
  if it has one.
- After each save, update claude/project-file-map.md
  (what each file is, how far to trust it, known
  problems) and the progress file.
- If you can't write to the project, give me the files
  and the map changes.
- To resume later, I'll paste: "Read
  claude/engineering-stack-prompt.md and
  claude/engineering-stack-progress.md, then continue
  from the next step."

STYLE
- Plain language first, then the technical term. Short
  sentences. Spell out each acronym the first time.
- Write for someone smart and self-taught who is new
  to the topic: no skipped steps, no unexplained
  jargon.
- Say each thing once; link instead of repeating.
- No em dashes.
- In any prompt or skill the paper includes: no
  persona, and give the reason for a rule instead of
  writing it in capitals.
- No personal details about any real person; author
  names in citations are fine.

FIRST REPLY
Confirm you have the PDF and the key project files
(name any that are missing), give the workspace check
in three lines, then run Phases 0, 1 and 2.
```

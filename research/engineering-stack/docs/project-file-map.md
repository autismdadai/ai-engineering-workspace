# Project File Map and Analysis

*Checked October 2, 2026; updated October 5, 2026 with the final prompting editions and the skills papers, and October 6–8, 2026 for the Markdown-only cleanup, the quantum lab's eval pack and first test runs, three reference books (cut down to the chapters in use on October 8), three new skills, a skills booklet, the first trigger tests and a handoff, October 9, 2026 for the AI engineering stack series: its prompt, the Gemini report converted to Markdown, a claim ledger, a freshness ledger, a plan and a progress file, and October 10 to 12, 2026 for the series' Parts 02 and 03, their reviews, the first Windows run of the labs, and a review of plugins and connectors, October 13, 2026 for the series' Parts 04 and 05 and their reviews, October 14, 2026 for Parts 06 and 07 and their reviews, October 15, 2026 for Parts 08, 09 and 10 and their reviews, October 16 to 19, 2026 for Part 11 and its review, October 19, 2026 for Part 12, its review and the second Windows run, October 20, 2026 for a handoff and the third Windows run (the reader tests of Parts 03 to 10 and 12), October 20, 2026 for Part 13 and its review, and October 20, 2026 for Phase 5: the series overview, and the 21 held corrections applied to the taxonomy, the guide, the claim ledger, the prompt generator's checklist, the New Skills Appendix and Parts 04, 10 and 11. The project holds 99 docs (this map included) and 16 uploads: the 5 quantum papers and 11 book chapters. Written so a person or an AI can tell, before opening anything, what each file is, how far to trust it, and what it is good for. Where things stand and what's next: claude/handoff-2026-10-20.md for the engineering stack series, claude/handoff-2026-10-08.md for the skills track.*

## The short version

- **The project is Markdown-first.** Every working document is a .md doc, which Claude can read cleanly and edit. PDFs are for primary sources only, kept as the originals because they are full of mathematics and are other people's published work: the five quantum research papers and chapters from three reference books. PDF copies of project documents are for reading and sharing and are kept outside the project.
- **The prompting track is final and checked.** The current editions are:
  - claude/taxonomy-of-prompt-engineering-3e.md: seven axes, independently reviewed and source-checked;
  - claude/prompt-construction-guide-2e.md: build steps and 150 worked examples, all reviewed.

  Around them sit a task index, the Edition Protocol v3, a verification report, a corrected skills reference (v1.2), a New Skills Appendix, and the corrected prompt-generator skill (1.2.1). The older editions were removed on October 6.
- **The agent-skills track:**
  - how to design, test, secure and package skills (SKILL.md folders);
  - one complete worked example with runnable code: the quantum lab, v1.2.1, with an eval pack that proves each of its tests can fail, a first with-and-without test, and two descriptions (365 characters, and 197 for the Claude app);
  - a build script, skills/build_skill.py, that checks any skill folder and packages it for the Claude app and other hosts;
  - three newer skills with eval packs: trig-check (exact trig with SymPy), qubit-math (small qubit calculations with numpy) and book-chapter-splitter (PDF books into checked chapter files, with pypdf);
  - a skills booklet that takes a skill from idea to everyday use, including installing it in the Claude app, Claude Code and other tools (claude/skills-booklet.md; it replaced the October 7 install guide);
  - the first trigger-test results for all four skills (claude/trigger-tests-2026-10-08.md);
  - the prompt-generator skill;
  - two AI-written source papers, converted to .md under ai-reports/.
- **The AI engineering stack series (started October 9):** a new multi-part paper, planned from an AI-written Gemini report that is treated as a map of claims to check. Phase 1 audited the report claim by claim (claude/engineering-stack-claim-ledger.md); Phase 2 planned 13 parts (claude/engineering-stack-plan.md); the owner approved all 13 on October 9. Parts 01 (setup and safe practice), 02 (evals, test data and judges), 03 (prompts as software interfaces), 04 (context), 05 (retrieval), 06 (graphs and memory), 07 (tools and protocols), 08 (agents), 09 (workflows and several agents), 10 (security), 11 (running models), 12 (adapting models) and 13 (shipping and operating) are done and checked. Phase 5 (October 20) assembled them with an overview and appendices (claude/engineering-stack-overview.md: reading routes, key figures, a tool index, decision guides, errata, open items, skill ideas) and applied the 21 held corrections; the separate-session review of the whole series is still to run. From Part 06 on, by the owner's decision of October 14, each part stays near 100 KB and prints only its core lab files.
- **Persona-free methods from the Planetary Council package** are project docs: a multi-lens review method, a research and verification toolkit, and a prompt-suite method.
- **The five research papers** are real quantum-computing research. Only the review has an agent section; the other four are useful here as examples of careful measurement.
- **Chapters from three reference books** (books added October 6, cut down October 8): a quantum mechanics textbook, quantum physics course notes and a trigonometry textbook. Only the chapters the lab, trig-check and qubit-math draw on are kept, each as its own PDF of under 100 pages; the full books were removed.
- **Open problems:**
  - the AI-written sources present unchecked numbers as checked;
  - the prompt generator's quality score can be gamed;
  - the trigger tests have had one first pass, in Claude Code only: qubit-math loaded for 2 of its 10 requests and trig-check for 6, mostly skipping quick textbook questions the model answered itself; the lab's with-and-without test has one run per task, and the three newer skills have none yet;
  - three skills described in the skills reference have no files here: skill-builder, cross-model-accuracy-verifier and server-log-triager;
  - the engineering-stack series' held corrections were applied on October 20, 2026 (claude/engineering-stack-overview.md, Appendix J); one more of the same kind turned up afterwards and is held for the owner: skills/sophisticated-prompt-generator/SKILL.md, Procedure step 3, still says "low temperature for single-answer tasks" without "where the model accepts it";
  - the series' separate-session review (claude/edition-protocol-v3.md, Sessions B and C) hasn't been run (overview, Appendix L).

## Decisions

- **October 2, 2026:** This project is the home for building research papers and prompts. The quantum papers stay here. The project instructions route quantum questions to them; for other topics, use them only as examples of careful measurement.
- **October 2, 2026:** The Planetary Council stays its own project. Its reusable methods were extracted here without the personas.
- **October 3, 2026:** The checked Third Edition manual and Second Edition guide are the current prompting references.
- **October 6, 2026:** The project is Markdown-first. The combined volume, the PDF copies of project documents and the superseded editions (taxonomy v2, the first-edition guide, the old rebuild prompt and the six-axis first edition) are removed. Search had been returning the same passages three times, and the superseded first edition outranked the current edition with older, unscoped wording. The two AI-written uploads still in use were converted to .md under ai-reports/. The lab guide and the archive cover sheet were dropped as out of date. The five quantum papers stay as PDFs. Taxonomy v2, the first-edition guide and the old rebuild prompt should still be downloadable as PDFs from the chat "File taxonomy analysis".
- **October 6, 2026 (later):** The owner deleted the PDF copies and the other leftover uploads; only the five quantum papers remain. The lab script moved into its skill folder (skills/quantum-entanglement-lab/scripts/), and the lab became version 1.2 with an eval pack in evals/. More research papers and math books are still to be added; when they arrive, keep them as PDFs and add them to this map and the routing.
- **October 6–7, 2026:** The owner added three reference books (qb.pdf, 130_notes.pdf and the trigonometry textbook). They stay as PDFs, and the instructions route math and physics background to this map. The lab keeps its 365-character description for Claude Code and other hosts and gained a 197-character one for the Claude app (`metadata.claude-app-description`); skills/build_skill.py builds both versions from the same files. The owner chose the quick with-and-without test, one run per task per condition, after the pilot showed each helper run costs about 100,000 tokens.
- **October 7, 2026 (afternoon):** On the owner's go-ahead, two skills were built from the reference books: trig-check (from the open trigonometry textbook) and qubit-math (from Binney & Skinner and the UCSD notes, in our own words with page pointers, since both are copyrighted). Trimming the books to the chapters in use waits on the original PDFs, because the project gives Claude only their text.
- **October 8, 2026:** With the original PDFs from the owner's computer, the books were split into the chapters in use (see Reference book chapters). Trig chapter 5 was added to the planned list because trig-check's triangle notes point to it. Project docs can hold text only, so Claude could not add the PDFs itself; the owner uploaded them through the project's + button, Claude checked each one, and then removed the three full books. Trig chapter 7, missed in the first upload, went in the same day and was checked the same way. The original books stay on the owner's computer.
- **October 8, 2026 (later):** The splitting procedure became a skill, book-chapter-splitter 1.0. It uses pypdf rather than PyMuPDF, because pypdf installs anywhere and is what the Claude app's own PDF skill uses; Claude drafted its intake answers from the session, for the owner to confirm. The skills booklet replaced claude/skill-install-guide.md, which was deleted once every step in it was carried over. The first trigger tests ran in Claude Code with `claude plugin eval` (80 runs, about $4.20 at list price as the tool estimated). A Claude Code starter kit (prompting-kit.zip: the skills, their tests, packages and tools) was sent in the chat; it isn't in the project, which holds text only.
- **October 9, 2026:** The AI engineering stack becomes a new paper, not a continuation, because neither this map nor the handoff numbers a series. The Gemini Deep Research report "The Modern AI Engineering Stack" was converted to ai-reports/gemini-ai-engineering-stack.md and audited claim by claim; the PDF itself stays out of the project. The plan organizes the paper by layers and concerns instead of taxonomy-style axes, because none of six candidate axes placed every topic (claude/engineering-stack-plan.md, Section 5). Work stopped twice at a usage limit that day and resumed from saved files each time.
- **October 20, 2026:** The owner approved applying all 21 held flags and one overview document for Phase 5. The overview links the glossary, the freshness ledger and the claim ledger's errata rather than copying them, to stay within the knowledge budget. The AI-written skills report is not edited; its `allowed-tools` problem is recorded here instead (Sources in depth).
- **October 9, 2026 (evening):** The owner approved all 13 parts and is not limiting usage. No API keys, accounts or spending: every lab is free, using stand-ins or small local models, with hosted-API versions only as optional notes. The taxonomy and the project instructions stay unchanged until the series is finished. Runnable lab folders go to the owner as zip files rather than into the project (claude/engineering-stack-plan.md, Section 8).

## File map

### Prompting references

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| claude/taxonomy-of-prompt-engineering-3e.md | The manual, 3rd edition: seven axes (Decoding & Inference Compute added as Axis 4), Canonical Figures appendix, changelog, Still Unverified list | Independent reference, not peer reviewed; independently reviewed and source-checked (see the report) | What each technique is, the evidence, failure modes, exact figures with scope |
| claude/prompt-construction-guide-2e.md | The guide, 2nd edition: build steps, orchestration patterns, 150 worked examples, task index, usage data (Part 7, including the §30 technique-to-task mapping), decoding and independent review (Part 8) | Independent reference; examples reviewed, not benchmarked | Writing and fixing prompts |
| claude/task-type-index.md | One-page job-to-technique lookup with the primary axis | Design aid, aligned with the guide and manual | Picking a starting technique fast |
| claude/edition-protocol-v3.md | Verification-first prompt set for revising a long reference: author, independent review, fidelity test, six acceptance tests, running on a budget (§9) | Project protocol | Rebuilding or fact-checking any long document |
| claude/verification-and-benchmark-report.md | What was checked in the final editions, by whom, the results, and what remains open (corrected October 6) | Project report | Knowing how far to trust the two references |

### Methods, prompts and audits

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| claude/prompt-suite-method.md | Seven-axis checklist, ten coverage areas, five audit prompts, and the tested limits of the generator scripts | Project method, AI-assisted, not benchmarked | Prompt suites, test suites, prompt audits |
| claude/fabel-prompt-audit.md | Audit of an outside research prompt: numbered findings with severity, quote, cause, source and fix | Project audit | The format for reviewing any prompt, skill or document |
| claude/portable-research-prompt.md | Research rules: claim tags, only opened sources cited, action log, AI-written input treated as claims to check | Project prompt | Any research or fact-check |
| claude/research-verification-toolkit.md | Evidence grades, claim-by-claim verification, research order, analysis templates, care rules | Project method, AI-assisted, not benchmarked | Research papers and fact-checks |
| claude/multi-lens-review-method.md | Four review stages, ten lenses, a blind verifier, synthesis and honesty rules, a brief skeleton | Project method, AI-assisted, not benchmarked | Hard, many-sided questions; multi-agent design |
| claude/github-tutor-prompt.md | Finished teaching prompt with an honesty canary test | Project prompt | Model for tutoring and how-to prompts |
| claude/visual-prompts-seven-axis.md | Three image prompts and three Gemini video prompts showing the project, with a shared seven-color code | Project prompts | Visuals for presenting the project |

### Agent skills

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| claude/agent-skills-reference-v1-2.md | Skills reference v1.2 (corrected October 6): design principles, anatomy and limits, catalog with honest status, seven-axis summary, testing and security | Project reference; corrected from an AI-written v1.1 | Building and checking skills |
| claude/new-skills-appendix.md | What changed in the skills and skill files, with status for each, and four skills worth building next (idea 3 reshaped to agent-permission-review on October 20, 2026; the series overview's Appendix I lists 16 more) | Project record | Knowing which skill version is current, what is missing, and what to build next |
| skills/sophisticated-prompt-generator/SKILL.md and references/ (seven-axis-checklist.md, practical-frameworks.md) | The prompt-generator skill, 1.2.1, without personas | AI-written, corrected here; its scripts live in the Planetary package | Generating a prompt suite from one seed |
| skills/quantum-entanglement-lab/SKILL.md and its three references/ files | The lab skill, version 1.2.1: instructions and reference cards (Bell states, CHSH, teleportation) | AI-written; checked and corrected here | Worked example of a complete skill |
| skills/quantum-entanglement-lab/scripts/entanglement_lab.py | The lab's script, v1.2: six self-checking quantum tests | Code; runs (checked) | Example of a deterministic skill script whose tests can fail |
| skills/quantum-entanglement-lab/evals/ (evals.json, mutation_check.py, grade_answer.py, with_without_results.json, README.md) | The lab's eval pack: 10 trigger and 10 non-trigger requests, 3 end-to-end and 4 adversarial tasks, a mutation check, an answer grader, and the October 7 with-and-without results | Project eval pack; script checks, grader self-test and a one-run-per-task with-and-without test run; first trigger pass in Claude Code (7 of 10 loaded, 10 of 10 left off) | Testing the lab; a model for other skills' eval packs |
| skills/build_skill.py | Checks a skill folder against the spec and builds three versions: the folder ZIP with the spec description, the same with the Claude-app description, and one SKILL.md with the other files bundled, for the Claude app's save card | Code; runs (checked) | Packaging any skill in skills/ |
| skills/trig-check/ (SKILL.md, scripts/trig_check.py, references/identities.md, evals/) | Exact trig with SymPy: identities with counterexamples, exact values, degree and radian conversion, triangles including SSA. Version 1.0 | Project skill; 21 script tests pass and its mutation check catches all 12 deliberate bugs; first trigger pass in Claude Code: 6 of 10 loaded, 10 of 10 left off; with-and-without not yet | Checking trig, including the math behind the lab |
| skills/qubit-math/ (SKILL.md, scripts/qubit_math.py, references/notation.md, evals/) | Small qubit calculations with numpy: gates, measurement, partial trace, entropy, both fidelity conventions, Pauli expectations. Version 1.0 | Project skill; 25 script tests pass and its mutation check catches all 13 deliberate bugs; first trigger pass in Claude Code: 2 of 10 loaded, 10 of 10 left off; with-and-without not yet | Computing a specific state or circuit |
| skills/book-chapter-splitter/ (SKILL.md, scripts/inspect_pdf.py, scripts/split_book.py, references/planning.md, evals/) | Splits a PDF book into chapter files under 100 pages with the front pages kept, checks every page against the book, and finds chapter starts and printed-page offsets. Version 1.0, pypdf. Its eval pack builds its own 160-page sample book, so it carries nothing from a real one | Project skill; 22 script tests pass, its mutation check catches all 15 deliberate bugs, and it re-made the 11 real chapter files with identical pages; first trigger pass in Claude Code: 10 of 10 loaded, 10 of 10 left off; with-and-without not yet; intake drafted by Claude | Adding more books to the project |
| claude/skills-booklet.md | Ten steps from idea to everyday use: decide, intake, descriptions, SKILL.md, scripts, the eval pack (with automated trigger tests in Claude Code), packaging, installing in the Claude app, Claude Code and other tools, using, maintaining; safety and troubleshooting | Project guide; product steps checked against the official pages on October 8 (replaced claude/skill-install-guide.md) | Building, installing or using any skill |
| claude/trigger-tests-2026-10-08.md | The first trigger tests of all four skills: setup, results, the 15 misses, limits, and the decision they raise | Project test record; one run per request, Claude Code only | Fixing descriptions; re-running trigger tests |
| ai-reports/q-advanced-agent-skills-paper.md | Synthesis of skill design: architecture, five principles, 10-step build, deployment pattern. Converted from Q-Advanced_AI_Agent_Skills_Deep_Research_Paper.pdf on October 6 | AI-written synthesis dated Sept 27, 2026 | Skill-design method. Verify numbers before reuse |
| ai-reports/agent-skills-research-report.md | Research report on agent skills: definitions, platforms, spec, build process, failure modes, testing, security. Converted from 1000014128.PDF on October 6 | AI-written report; its source tags are not reliable; it treats `allowed-tools` as a security boundary, which it isn't (Sources in depth) | Sections 1–10, 16 and 17. Not sections 11–15 |

### AI engineering stack series (October 9, 2026)

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| claude/engineering-stack-overview.md | The series' front matter and appendices (Phase 5): the 13 parts and their files, reading routes, how the series connects to the taxonomy and the guide, 30 key figures with scope, one tool and download index across all parts, three decision guides (prompt, retrieve or fine-tune; one agent or several; local or cloud), the learning path, errata for the Gemini report, the freshness ledger, what's still unverified, 16 skill ideas, the corrections applied on October 20, and the acceptance-test results | Project paper, front matter; links to the parts rather than copying them; every figure carries its part's tag and was checked against the part by script; the separate-session review is still open | Starting the series; finding a part, figure or tool; making one of the three decisions |
| claude/engineering-stack-prompt.md | The owner's prompt for the series, verbatim: rules, Phases 0 to 5, saving and style | Project prompt | Starting or resuming the series |
| claude/engineering-stack-progress.md | Done, in progress, next, open questions and unverified items, with resume instructions | Project record; a snapshot | Picking up the series |
| claude/engineering-stack-claim-ledger.md | Phase 1 audit of the Gemini report: 163 claim rows, each with verdict, grade and primary source; all 33 works cited opened; absolute words; formulas and arithmetic checked; pillar terms; answers to the prompt's audit questions; errata by section; flags against the taxonomy; about 110 sources | Project audit; sources opened October 9, 2026 by seven checker agents and the lead; not yet re-checked by a blind verifier as a whole (each part re-checks its own rows). Corrected on October 20, 2026 from the parts' findings (its Section 12): P5-09's 9.3, P8-01 and B1-03 now overstated, P11-02 and P11-03 changed, and eleven notes; totals now 137 checkable rows, 50 holding | What the Gemini report got right and wrong; the starting facts for each part |
| claude/engineering-stack-freshness-ledger.md | Time-sensitive facts with the date checked and the page to re-check: product and model status, 40 PyPI packages, 4 npm packages, 5 GitHub tags, the facts each part adds (Sections 5, 6 and 8 to 19), and the script that reads PyPI | Project record; registry data read October 9 to 20, 2026 | Re-checking versions, licences and retirements before each part |
| claude/engineering-stack-plan.md | Phase 2: overlaps and gaps, the axes test, layers and concerns, the learning map with three paths per part, the 13-part plan with agents, cost and knowledge budget, and open questions | Project plan; approved by the owner on October 9 (decisions in its Section 8) | Scoping and running Phases 3 to 5 |
| claude/engineering-stack-part-01-setup.md | Part 01, setup and safe practice: Python 3.13 with virtual environments, hash-pinned installs, Git and `.gitignore` for keys, Node.js 24 LTS, checking downloads; steps for Windows, macOS and Linux; a lab with a setup checker, break-it steps and a mutation check; teaching material and a tutor prompt | Project paper part; 133 [V], 83 [T], 26 [R], 13 [U]; blind source check and beginner test passed after fixes; the lab passed on Windows 11 on October 12, 2026 [T]; macOS steps and typed Windows steps not yet run (marked [R]) | Setting up for the series; the safe-setup habits |
| claude/engineering-stack-part-01-review.md | Phase 4 findings for Part 01 in the fabel finding format: 14 findings from the blind source check and the beginner test, all fixed | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-02-evals.md | Part 02, evals, test data and judges: the eval loop, test data and contamination, graders, accuracy with a Wilson interval, per-label scores, the paired McNemar test, model judges and their biases, semantic entropy, nondeterminism, evals in CI; the eval tools compared (licence, keys, telemetry, upkeep); a lab with a stand-in router, a gate, break-it steps, a mutation check and an optional promptfoo run; teaching material and a tutor prompt | Project paper part; 209 [V], 80 [T], 7 [R], 7 [U], 5 [I]; the lab's data is invented [I] and its arithmetic tested; blind source checks and a beginner test passed after fixes; the lab passed on Windows 11 on October 12, 2026 [T]; macOS steps and typed Windows steps not yet run (marked [R]) | Measuring any AI system; checking a model judge; choosing an eval tool |
| claude/engineering-stack-part-02-review.md | Phase 4 findings for Part 02 in the fabel finding format: 12 findings from two blind source checks (74 of 76 claims supported, 2 partly) and the beginner test (17 problems), all fixed | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-03-prompts-as-interfaces.md | Part 03, prompts as software interfaces: JSON Schema contracts, three levels of JSON guarantee and their documented exceptions, both vendors' strict-mode rules side by side, tool calling and `tool_choice` (forced tools now refused on Claude's newest models), local engines (llama.cpp, Ollama, Outlines) and their coverage, the format-versus-quality evidence, reasoning-model settings (Anthropic effort and thinking, OpenAI reasoning effort), and prompt optimization with DSPy (MIPROv2, GEPA) and its overfitting trap; a lab with a schema linter, a validate-and-retry loop, a capped tool loop, a toy optimizer and a mutation check; teaching material and a tutor prompt | Project paper part; 172 [V], 56 [T], 7 [R], 5 [U], 6 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; the lab's data is invented [I] and its code tested; blind source checks and a beginner test passed after fixes; no live model calls (no keys, by the owner's decision); macOS and typed Windows steps not yet run (marked [R]); vendor API facts change quickly (freshness ledger §8) | Making a model's output safe for code; tool definitions; reasoning settings; deciding whether prompt optimization is worth it |
| claude/engineering-stack-part-03-review.md | Phase 4 findings for Part 03 in the fabel finding format: two blind source checks (137 of 148 claims supported, 8 partly, 3 not checkable, none contradicted; one finding didn't reproduce) and the beginner test (16 problems), all fixed; two flags against project docs | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-04-context.md | Part 04, context: tokens and counting (tokenizers differ by up to about 30%), the context budget and current windows, what each provider does with an oversized request (Ollama cuts chat history silently), compaction and context editing, position effects from Liu et al.'s 2023 U-curve to current studies, vendor placement advice and where it disagrees, prompt caching at Anthropic, OpenAI and Google with break-even arithmetic, engines' prefix caches, and caching privacy; a lab with a budget planner, overflow rules, a cache simulator, a placement test with intervals and a mutation check; teaching material and a tutor prompt | Project paper part; 199 [V], 79 [T], 6 [R], 15 [U], 7 [I]; `placement_test.py` gained a separate timeout message, `--timeout` and `--no-think` on October 20, 2026 (new listing in its appendix; the replacement file went to the owner); the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; R4 only at 50 documents with thinking off, since the full size passed the lab's 300-second limit per call on that PC; the lab's stand-ins are invented [I] and its code tested; blind source checks and a beginner test passed after fixes; no live model calls; no independent position test of the newest models exists among the sources read [U]; prices and model names change quickly (freshness ledger §10) | Fitting a request into a window; ordering a prompt for caching; costing a cache; testing placement on your own model |
| claude/engineering-stack-part-04-review.md | Phase 4 findings for Part 04 in the fabel finding format: two blind source checks (128 of 154 claims supported, 23 partly, 3 not checkable, none contradicted) and the beginner test (15 problems, the most serious a wrong-sized token margin), all reproduced and fixed | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-05-retrieval.md | Part 05, retrieval: BM25 symbol by symbol and how tools' defaults differ, embeddings and the evidence that nearness isn't meaning, exact and approximate vector search, six kinds of vector store with licences and telemetry, hybrid search with RRF (and the trap that tools count ranks differently, so Qdrant's default k = 2 acts like k = 1) and weighted fusion, cross-encoder reranking, late interaction (now in sentence-transformers 6), learned sparse search, ColPali, HyDE and contextual retrieval, chunking, retrieval metrics (and Success@k mislabelled as recall), RAG evaluation, and retrieval against long context; a lab with BM25, a stand-in dense search, two fusion methods, metrics, a chunker, a mutation check and cross-checks against bm25s and ir_measures; teaching material and a tutor prompt | Project paper part; 189 [V], 77 [T], 6 [R], 21 [U], 7 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; the lab's corpus and stand-in are invented [I] and its code tested; blind source checks and a beginner test passed after fixes; no neural model runs on the test machine, so embedding models and rerankers are reader tests, run on the owner's PC; Elasticsearch's RRF licence tier rests on its source code; no independent vector-database benchmark was opened [U] | Choosing and building a retrieval pipeline; measuring retrieval; picking a store |
| claude/engineering-stack-part-05-review.md | Phase 4 findings for Part 05 in the fabel finding format: two blind source checks (141 of 160 claims supported, 18 partly, 1 not checkable, none contradicted; one finding didn't reproduce), the beginner test (14 problems, the most serious that PyPI's torch pulls NVIDIA's CUDA libraries on Linux), and the mutation check's first run (11 of 16 caught), all reproduced or marked and fixed | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-06-graphs-and-memory.md | Part 06, graphs and memory: property graphs and RDF, Cypher and ISO GQL, building a graph with a model and why entity resolution decides multi-hop answers, modularity by hand, Louvain and Leiden, GraphRAG's pipeline and query modes (and its maintenance mode), two independent comparisons of GraphRAG with plain RAG (graphs help on multi-hop, temporal and summary questions, lose on single facts, at up to 377 times the prompt tokens), CoALA's four kinds of memory, what ships as memory today (Anthropic's memory tool, Mem0's add-only default, Graphiti's dated facts, Letta's retired server and reused PyPI name), the memory-benchmark dispute, and memory poisoning; a lab with a graph, three memory designs, a quarantine, a path check, a mutation check and a networkx cross-check; teaching material and a tutor prompt | Project paper part; 153 [V], 58 [T], 6 [R], 8 [U], 5 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; the lab's notes and stand-in extractor are invented [I] and its code tested; blind source checks and a beginner test passed after fixes; no model, graph database or memory product runs on the test machine [R]; products in this area changed a lot in 2025 and 2026 (freshness ledger §12) | Deciding whether a graph or memory layer is worth it; building a small graph; choosing how memory handles changed facts |
| claude/engineering-stack-part-06-review.md | Phase 4 findings for Part 06 in the fabel finding format: two blind source checks (112 of 127 claims supported, 14 partly, 1 not checkable, none contradicted) and the beginner test (14 problems, none blocking), all reproduced or marked and fixed | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-07-tools-and-protocols.md | Part 07, tools and protocols: when plain tool calling is enough, MCP's roles and features, everything MCP revision 2026-07-28 changed (no handshake, no sessions, `server/discover`, multi round-trip requests instead of server-to-client calls, sampling and roots deprecated, Tasks as an extension), tool definitions and the two kinds of error, stdio and Streamable HTTP, OAuth for HTTP servers, the SDKs (Python `MCPServer`; the TypeScript 2.x packages) and which hosts speak MCP, A2A and the other agent protocols, the Agent Skills format with its product-specific limits, tool poisoning, rug pulls and two CVEs, and how many tools a model can handle; a standard-library MCP server and client with a confirm-before-delete round trip, tool pinning, a skill checker, a mutation check and a cross-check against the official SDK; teaching material and a tutor prompt | Project paper part; 225 [V], 74 [T], 9 [R], 7 [U], 6 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; R4 (Claude Code) not run; the lab's notes are invented [I] and its code tested, including against `mcp` 2.3.0; blind source checks and a beginner test passed after fixes; no host app or model runs on the test machine [R]; MCP changed a lot in 2026 (freshness ledger §13) | Deciding whether to build an MCP server or a skill; reading MCP messages; checking a 2025 tutorial against the current spec; reviewing a server before connecting it |
| claude/engineering-stack-part-07-review.md | Phase 4 findings for Part 07 in the fabel finding format: two blind source checks (194 of 209 claims supported, 12 partly, 3 not checkable, none contradicted) and the beginner test (18 problems, none blocking), all reproduced or marked and fixed | Project review | Seeing what the checks caught and how it was fixed |
| claude/engineering-stack-part-08-agents.md | Part 08, agents: the tool loop and its seven stop reasons, tool results and errors (short messages, never raw exception text), turn caps and budgets (the OpenAI Agents SDK stops at 10 turns by default, the Claude Agent SDK has no limit), human approval, why input tokens grow faster than turns, the three meanings of "harness", what agent benchmarks measure (ReAct, pass^k, SWE-bench Verified's retirement by OpenAI, Terminal-Bench), what containers do and don't isolate with a hardened `docker run`, gVisor and Firecracker (with corrected ledger notes), how coding agents sandbox themselves, and computer use (Anthropic's new toolset, OpenAI's and Google's tools, costs, injection rates with their scopes, OSWorld's versions); a lab with a careful loop driven by a scripted stand-in, a `docker run` checklist, a computer-use harness and the not-a-sandbox demo, plus an OpenAI Agents SDK cross-check; teaching material and a tutor prompt | Project paper part; 225 [V], 73 [T], 11 [R], 4 [U], 12 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; R4 (Docker) not run; the lab's files and pages are invented [I] and its code tested, including against openai-agents 0.23.1; blind source checks, a security review (four high findings in the lab, fixed) and a beginner test passed after fixes; no model, container or VM runs on the test machine [R] | Building an agent loop; deciding how to sandbox model-written code; judging computer-use claims and benchmark numbers |
| claude/engineering-stack-part-08-review.md | Phase 4 findings for Part 08 in the fabel finding format: two blind source checks (174 of 187 claims supported, 13 partly, none contradicted), a security review (17 findings, 4 high, all reproduced and fixed) and the beginner test (13 problems, none blocking) | Project review | Seeing what the checks caught, especially the security review |
| claude/engineering-stack-part-09-workflows-and-multi-agent.md | Part 09, workflows and several agents: Anthropic's five workflow patterns, three ways to describe a workflow (DAG, state graph, code with durable steps), checkpoints, threads and durability modes, what resuming re-runs, LangGraph's step limit (10,007 in code, 1,000 in its docs), Temporal's replay model, defaults and history limits, retries with full jitter, idempotency keys and "effectively once", pausing for a person in six frameworks with approval fatigue and the EU AI Act's oversight dates, the evidence on several agents (Anthropic's 90.2% and its token costs, equal-budget preprints, MAST, debate studies), how context moves between agents, cost and error arithmetic, and which frameworks are current; a lab with a small durable workflow engine (approval, a killed process resumed, retries, a refund made once) and several-agent toys, plus a LangGraph cross-check; teaching material and a tutor prompt | Project paper part; 173 [V], 69 [T], 9 [R], 0 [U], 11 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; the lab's orders, payments and agents are invented [I] and its code tested, including against LangGraph 1.2.15; blind source checks and a beginner test passed after fixes; no model or Temporal server runs on the test machine [R]; much of the multi-agent evidence is preprints or vendor reports | Deciding between a workflow, one agent and several; making long runs survive crashes and pauses; adding human approval; reading multi-agent claims |
| claude/engineering-stack-part-09-review.md | Phase 4 findings for Part 09 in the fabel finding format: two blind source checks (170 claims: 7 partly, none contradicted), the beginner test (21 problems, none high), two mutation gaps closed, and temporary folders the checks left behind (now cleaned up) | Project review | Seeing what the checks caught |
| claude/engineering-stack-part-10-security.md | Part 10, security: prompt injection direct and indirect, OWASP's 2026 list (LLM01 says no reliable prevention exists today; LLM03 Excessive Agency; LLM08 Hidden Context Exposure) and its Agentic Top 10, MITRE ATLAS, the lethal trifecta and Meta's Agents Rule of Two, adaptive attacks (Nasr et al.'s per-model results against 12 defences), CaMeL and other system designs, a URL parser differential, guardrail frameworks and their defaults (NeMo's telemetry, LLM Guard archived), safety classifiers with base-rate arithmetic, redaction and Presidio, HIPAA (the Security Rule update still a proposal), vendor data handling, the EU AI Act after the Digital Omnibus, model licences and SPDX; a lab with an action gate enforcing the Rule of Two with single-use approvals, an output cleaner for links and invisible characters, a redactor, a licence sorter and a mutation check, plus cross-checks against Presidio and python-stdnum; teaching material and a tutor prompt | Project paper part; 196 [V], 86 [T], 7 [R], 13 [U], 33 [I]; row P10-09b updated October 20, 2026 for Meta's Muse models; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; 116.8 KB, over the 100 KB target; the lab's pages and records are invented [I] and its code tested; blind source checks and a beginner test passed after fixes; the security review agent was stopped by a safety classifier, so the lead ran harmless edge cases (three lab gaps found and fixed); no model or guard model runs on the test machine [R]; rows on law are information, not legal advice | Designing an agent that reads untrusted content; choosing guardrails; judging classifier numbers; handling personal data and model licences |
| claude/engineering-stack-part-10-review.md | Phase 4 findings for Part 10 in the fabel finding format: two blind source checks (179 claims: 136 supported, 33 partly, 10 not checkable, none contradicted), the beginner test (3 low problems), and the lead's security edge cases (`www.` links, variation selectors and reusable approvals), all reproduced and fixed | Project review | Seeing what the checks caught |
| claude/engineering-stack-part-11-running-models.md | Part 11, running models: prefill and decode; the memory and speed arithmetic (weights, the KV cache with grouped-query attention and sliding windows, the decode ceiling as bandwidth over bytes per token, the roofline's ridge point); quantization (llama.cpp's block layouts, why a Q4_K_M file is 4.89 bits per weight, GGUF against AWQ and GPTQ, MXFP4, what quality it costs with and without an importance matrix); serving engines (step-level batching, PagedAttention, preemption, prefix caching, and the defaults and telemetry of vLLM, SGLang, TensorRT-LLM, TGI, LMDeploy and MLX-LM); speculative decoding's arithmetic and measured results with their scopes; TTFT, TPOT and ITL and the naming clash between tools; MLPerf Inference 6.1; running locally with Ollama, llama.cpp and LM Studio (what Ollama sends to ollama.com, small open models by licence); reading GPU datasheets (sparse against dense, preliminary against shipping, current NVIDIA and AMD parts) and what is inside a GPU server; a lab that reproduces llama.cpp's published file sizes to four decimal places, with a mutation check and a reader test that times a small model in Ollama; teaching material and a tutor prompt | Project paper part; 192 [V], 85 [T], 16 [R], 17 [U], 12 [I]; 93.7 KB; Section 3.6 gained the GenAI conventions' timing names on October 20, 2026; the lab's arithmetic tested and its demo PC's free memory invented [I]; blind source checks and a beginner test passed after fixes; no model or engine runs on the test machine, which has no GPU, so engines are described from source and docs; the reader tests R1 to R4 ran on the owner's Windows PC on October 19, 2026 [T]; most speed claims are vendors' and method authors' | Deciding whether a model fits a computer and how fast it can go; choosing a serving engine or a local tool; reading a GPU datasheet |
| claude/engineering-stack-part-11-review.md | Phase 4 findings for Part 11 in the fabel finding format: two blind source checks (207 claims: 172 supported, 31 partly, 4 not checkable, none contradicted) and the beginner test (25 problems, 1 high), all reproduced before fixing; the most important, that Llama 4 is no longer Meta's newest open-weight line, came from a checker's side note | Project review | Seeing what the checks caught |
| claude/engineering-stack-part-12-adapting-models.md | Part 12, adapting models: where model comparisons come from and how far to trust each (Arena and the Leaderboard Illusion dispute, Artificial Analysis, LiveBench, HELM in maintenance mode, the retired Open LLM Leaderboard), contamination and saturation with the 13-word rule, reading a model card, the open-weight field in October 2026 with licences that differ inside one family (Meta's Muse Spark Open is gated and not Apache-2.0), choosing by your own eval; when to fine-tune, prompt or retrieve (retrieval beat fine-tuning on new facts; new facts learned by fine-tuning raise hallucination), full fine-tuning's 16 bytes per weight, LoRA and QLoRA with their memory, which layers to adapt, DoRA, DPO and GRPO in a line each, data formats, chat templates and leak checks, safety after fine-tuning, hosted fine-tuning closing (OpenAI, Gemini, Mistral), the libraries' licences, hardware and telemetry (Unsloth's AGPL files, TRL's ping), and licence duties when sharing a fine-tune; a lab that reproduces PEFT's and the LoRA paper's printed counts exactly, with a data checker, a decision guide, a mutation check and a reader test that trains a small LoRA adapter on a processor; teaching material and a tutor prompt | Project paper part; 182 [V], 76 [T], 10 [R], 23 [U], 20 [I]; the reader tests ran on the owner's Windows PC on October 20, 2026 (claude/engineering-stack-windows-run-2026-10-20.md) [T]; 87.3 KB; the lab's sample data is invented [I] and its arithmetic tested; blind source checks and a beginner test passed after fixes; no model was trained or tested on the test machine; the LoRA reader test trained SmolLM2-135M on the owner's PC at 0.89 seconds per step; the fine-tune-or-retrieve evidence is two studies, and Biderman et al. and Qi et al. are preprints | Choosing a model; deciding whether to fine-tune; sizing a LoRA run; checking training data; sharing a fine-tune under its licence |
| claude/engineering-stack-part-12-review.md | Phase 4 findings for Part 12 in the fabel finding format: two blind source checks (171 claims: 149 supported, 18 partly, 4 not checkable, none contradicted) and the beginner test (30 problems, 2 high: a data step that broke the lab's own checks, and a PyTorch install that isn't possible on every computer), all reproduced before fixing | Project review | Seeing what the checks caught |
| claude/engineering-stack-part-13-shipping.md | Part 13, shipping and operating: putting a model behind your own API and what a public endpoint needs (authentication, open-stream and spend caps, timeouts), OpenAI-compatible servers and their gaps, FastAPI's built-in SSE (0.135.0) and OpenTelemetry (0.142.0), LangServe archived, Kubernetes multi-tenancy; Server-Sent Events by the WHATWG rules, browser keys and CORS, why a stream arrives all at once through a buffering proxy, errors after the 200, a stream that just stops, readers who leave, rate limits, 529 and the spend-cap 429, retries that multiply cost; OpenTelemetry traces, sampling, an untrusted `traceparent`, the GenAI conventions (moved in May 2026, status Development, content opt-in, renamed metrics) and how far the released instrumentation lags; eleven tracing tools by licence, content default and maker's telemetry (Traceloop, OpenLIT, OpenInference and Logfire record prompts by default), with self-hosting defaults; prices, batch, Flex and Fast, residency, long-context rules; Little's law and why to alert on the 95th percentile; a lab with a standard-library SSE parser, a stand-in streaming server, a buffering proxy, a tiny tracer and the cost arithmetic, a mutation check and a cross-check against FastAPI 0.156.1 and the OpenTelemetry SDK 1.45.1; teaching material and a tutor prompt | Project paper part; 183 [V], 79 [T], 10 [R], 16 [U], 20 [I]; about 95 KB; the stand-in model and its timings are invented [I] and the code tested; blind source checks, a security review (2 high in the advice; 5 medium in the code, all fixed) and a beginner test passed after fixes; no hosted model called (no keys, by the owner's decision), so the vendors' streams, limits and usage APIs come from docs and SDK source [R]; prices change often (freshness ledger §19) | Putting a model behind an API; streaming through proxies; tracing without recording prompts; choosing a tracing tool; pricing and sizing a service |
| claude/engineering-stack-part-13-review.md | Phase 4 findings for Part 13 in the fabel finding format: two blind source checks (158 claims: 114 supported, 34 partly, 3 contradicted and fixed, 7 not checkable), the beginner test (16 problems, none high) and a security review (21 findings, among them a missing public-endpoint checklist, keys in URLs, a client-chosen `traceparent` and a stream that stops without an error), all reproduced before fixing | Project review | Seeing what the checks caught, especially the security review |
| claude/engineering-stack-windows-run-2026-10-12.md | The first run of the Part 01 and 02 labs on the owner's Windows 11 computer: how Python 3.13.16 was installed (python.org installer, SHA-256 checked), the five results (all passed) with the full output, and which Windows steps are still [R] | Project test record; run by Claude through the desktop app with the owner watching | Turning the Windows [R] tags of Parts 01 and 02 into [T]; knowing what the owner's computer has |
| claude/engineering-stack-windows-run-2026-10-19.md | The Part 11 reader tests R1 to R4 on the owner's Windows 11 computer: Ollama v0.40.6 and llama.cpp b11706 installed from official sources with SHA-256 checks, qwen3:1.7b at 8.0 to 8.4 tokens per second, Qwen3-4B at 3.93 on the processor and 2.19 on the integrated GPU, and the finding that the PC runs one memory module in single channel (about 21.3 GB/s, half Intel's figure); the two script problems met and fixed | Project test record; run by Claude by script through the desktop app with the owner's go-ahead | Turning Part 11's reader-test tags into [T]; knowing what the owner's computer can run |
| claude/engineering-stack-windows-run-2026-10-20.md | The reader tests of Parts 03 to 10 and 12 on the owner's Windows 11 computer: every core lab and cross-check passed; Part 12's LoRA run (0.89 seconds per step for SmolLM2-135M on the processor); Part 05's real models; Presidio with spaCy's model and garak's self-test (Part 10); Part 04's placement test, which passed the lab's 300-second limit per call at full size and ran at 50 documents with thinking off; a runner encoding artifact explained; what the tests left outside the lab folders | Project test record; run by Claude by script through the desktop app with the owner's go-ahead | Turning those parts' reader-test tags into [T]; knowing what the owner's computer can run |
| claude/plugin-review-2026-10-12.md | Which directory connectors need a sign-in (Wolfram doesn't; alphaXiv, Consensus and Scholar Feed do), and a full code read of four community plugins (Prompt Design, skill-validator, skill-doctor, DeepEval): what each can reach, writes or sends, and a verdict | Project review by Claude, October 12, 2026; plugins change, so re-read before installing a newer version | Deciding which plugin or connector to add; checking an outside plugin before installing it |
| claude/engineering-stack-glossary.md | The series glossary: each term in plain words, then the technical term, with the part that defines it (313 terms after Part 13) | Project reference | Looking up a term |
| ai-reports/gemini-ai-engineering-stack.md | "The Modern AI Engineering Stack" (Gemini Deep Research): 12 pillars, 4 blueprints, 33 works cited. Converted October 9: tables rebuilt from the page images, formulas kept as printed LaTeX; its em dashes are Gemini's own | AI-written synthesis, the lowest trust class here; audited in the claim ledger | A map of claims only. Use the ledger's verdicts, not the report's numbers (see Sources in depth) |

Project knowledge stood at 1,185,481 (59.3%) before the Phase 1 and 2 files were saved; claude/engineering-stack-progress.md keeps the current count.

### Session handoff

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| claude/handoff-2026-10-08.md | Where the project stood at the end of October 8: how the project remembers, what happened October 6–8, the skills to add and to build next, what Claude Code can do here, next steps, what's unverified, and a prompt to start the next chat | Project record; a snapshot | Starting a new chat window; picking the next task |
| claude/handoff-2026-10-20.md | Handoff for the engineering stack series at the end of October 20, in the active-memory format: the binding rules and corrections, exact figures (the counter, the owner's PC, Part 11's Windows results, Part 12's numbers), the held flags for Phase 5, the work state, the next step (Part 13) and the open question on Part 12's reader test R3 | Project record; a snapshot, superseded by claude/engineering-stack-progress.md where they differ | Starting a new chat window on the series |

### Quantum research papers (kept as PDFs)

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| 2607.00365v1.pdf | "When AI meets quantum information: A comprehensive review" (University of Pittsburgh and others, July 2026) | Preprint (arXiv) | Quantum + AI questions; §III.E agent examples; §V benchmarking cautions |
| 2512.07737v2.pdf | AlphaQubit 2, a neural decoder for quantum error correction (Google DeepMind and Google Quantum AI, v2 March 2026) | Preprint (arXiv) | Quantum error correction; evaluation practice |
| s41534-026-01360-6_reference.pdf | Quantum algorithm for linear matrix equations (Google Quantum AI and Macquarie University) | Peer reviewed (npj Quantum Information, 2026) | Quantum algorithms only |
| 2510.04929v1.pdf | Efficient Quantum Hermite Transform (Google Quantum AI, UT Austin and others, Oct 2025) | Preprint (arXiv) | Quantum algorithms only |
| s41598-026-51870-8.pdf | Chaos-aware hybrid quantum–classical classifier on an MNIST subset | Peer reviewed (Scientific Reports, 2026, 16:15744) | Quantum machine learning; a model for reporting paired comparisons |

### Reference book chapters (PDFs; books added October 6, split October 8)

The books: *The Physics of Quantum Mechanics* by Binney and Skinner (Cappella Archive printings 2008–2011; published textbook, copyright the authors); *Quantum Physics*, the UCSD Physics 130 course notes by Jim Branson, dated April 2, 2003 (university lecture notes, no license line); and *Trigonometry*, Version 2 (2023), an open textbook from Salt Lake Community College, the University of Utah, Weber State University and Utah Valley University, adapted from Stitz and Zeager's *College Trigonometry* and OpenStax (CC BY-NC-SA 3.0). Each chapter file starts with its book's front pages (Binney & Skinner: title and copyright; UCSD: title; trig: acknowledgements and license), and its PDF properties record the page range it came from. Page numbers below are the books' printed ones.

| File | What it is | Evidence class | Use it for |
|---|---|---|---|
| binney-skinner-qm-ch01-probability-amplitudes.pdf | Binney & Skinner ch. 1, "Probability and probability amplitudes", pp. 1–16 | Published textbook | Amplitudes, quantum states, Dirac notation (p. 9), measurement (§1.4, p. 15) |
| binney-skinner-qm-ch02-operators-measurement.pdf | Binney & Skinner ch. 2, "Operators, measurement and time evolution", pp. 17–36 | Published textbook | Operators (§2.1, p. 17), Hermitian operators, time evolution, the position representation |
| binney-skinner-qm-ch06-composite-systems.pdf | Binney & Skinner ch. 6, "Composite systems", pp. 104–138 | Published textbook | Entanglement (§6.1, p. 105), the EPR argument and Bell's inequality (p. 113), quantum computing (§6.2, p. 116), reduced density operators (§6.3, p. 125), Shannon entropy. An independent textbook source for the lab's Bell material; it does not cover teleportation or name CHSH or Tsirelson |
| binney-skinner-qm-ch07-angular-momentum.pdf | Binney & Skinner ch. 7, "Angular momentum", pp. 139–180 | Published textbook | Spin (§7.4, p. 158), spin-half systems and the Pauli matrices, Stern–Gerlach, adding angular momenta and two spin-halves (§7.5, p. 173) |
| ucsd-130-notes-ch18-operators-matrices-spin.pdf | UCSD notes ch. 18, "Operators Matrices and Spin", pp. 247–282 | University lecture notes | Operators as matrices (p. 247), spin-1/2 and the Pauli matrices, rotation matrices, Stern–Gerlach sequences, NMR |
| ucsd-130-notes-ch21-adding-angular-momentum.pdf | UCSD notes ch. 21, "Addition of Angular Momentum", pp. 311–325 | University lecture notes | Two spins (triplet and singlet, p. 311), spin-orbit coupling, Clebsch–Gordan series |
| trig-v2-ch01-foundations.pdf | Trigonometry ch. 1, "Foundations of Trigonometry", T1-1 to T1-94 | Open textbook (CC BY-NC-SA 3.0) | Degrees and radians (§1.1), the unit circle and exact values (§1.3), the six functions, Pythagorean identities (§1.5) |
| trig-v2-ch03-identities.pdf | Trigonometry ch. 3, "Trigonometric Identities", T3-1 to T3-33 | Open textbook (CC BY-NC-SA 3.0) | Even/odd, sum and difference (used in the CHSH correlator −cos(a − b)), co-function, double-angle, half-angle and product-to-sum identities |
| trig-v2-ch05-laws-of-sines-and-cosines.pdf | Trigonometry ch. 5, "Beyond Right Triangles", T5-1 to T5-44 | Open textbook (CC BY-NC-SA 3.0) | Law of Sines with the SSA cases (§5.1), Law of Cosines and Heron's formula (§5.2) |
| trig-v2-ch06-polar-and-complex.pdf | Trigonometry ch. 6, "Polar Coordinates and Applications", T6-1 to T6-74 | Open textbook (CC BY-NC-SA 3.0) | Polar coordinates and graphs, complex numbers in polar form (§6.3), products, powers (DeMoivre) and roots (§6.4) |
| trig-v2-ch07-vectors.pdf | Trigonometry ch. 7, "Vectors", T7-1 to T7-49 | Open textbook (CC BY-NC-SA 3.0) | Vector operations, unit vectors, the dot product (§7.3) |

**Reading them.** Each chapter is under 100 pages, while each full book was over. The Claude Help Center says Claude reads the images and charts in PDFs of 100 pages or fewer but only the text of longer ones, and that project files get text extraction only, except for "multimodal PDFs", which it doesn't define. The chapters take about twice as much of the project's knowledge space per page as the full books did, which fits their being kept as whole PDFs, but nothing here confirms that project chats see the pages as images. The project tool still returns extracted text, where formulas suffer: in the trigonometry chapters fractions and π often drop out, and in Binney and Skinner the ket bracket ⟩ shows as "i" (|ψi for |ψ⟩). Check any formula against the PDF page.

**The trim (October 8).** Kept: Binney & Skinner chapters 1, 2, 6 and 7; UCSD chapters 18 and 21; trigonometry chapters 1, 3, 5, 6 and 7: 478 pages in the 11 files, front pages included, against 1,321 in the full books. Trig chapter 5 was added to the plan because trig-check's triangle notes point to it. Every page pointer in trig-check's and qubit-math's reference notes falls inside a kept chapter. Project knowledge, of its 2,000,000 limit: 1,350,222 (67.5%) before the upload; 1,902,900 (95.1%) with the 10 chapters and the full books; 1,068,231 (53.4%) after the full books were removed. The 10 chapters added 552,678 for 427 pages, about 1,290 per page, against about 630 per page for the full books (834,669 for 1,321 pages). With trig chapter 7 in, it stood at 1,136,978 (56.8%) on October 8, and at 1,167,173 (58.4%) after that day's new docs and skill.

## Final editions (October 3–5, 2026)

**What was checked.** The protocol's six acceptance tests were run against the 3rd-edition manual and 2nd-edition guide. Checkers ran in separate sessions on models different from the one that drafted them. Full detail is in claude/verification-and-benchmark-report.md.

- **Sources.**
  - 46 citation claims: 45 verified. The publication date of the CO-STAR article could not be confirmed.
  - All 26 checkable Canonical Figures: no number was wrong, 12 lacked scope, and 1 misreading entry was wrong. All are fixed.
  - Eleven more claims were checked during adjudication. One was wrong in both documents: GEPA's Pareto frontier is per training instance, not score versus instruction length.
- **Reviews.** 172 findings (53 on the manual, 119 on the guide), including 20 errors and 35 example prompts that could not run as written. All were resolved.
- **Biggest scope fixes:**
  - Chain-of-Symbol's +60.8 points is over zero-shot CoT in one setting; it is +17.5 points over few-shot CoT.
  - The Self-Consistency gains are GPT-3 code-davinci-002's.
  - The GEPA-versus-GRPO comparison is Qwen3 8B only.
  - Chain-of-Draft's "80%" is output tokens; latency fell 76% (GPT-4o) and 48% (Claude 3.5 Sonnet).
- **Fidelity.** Two fresh summaries on two models restated 24 canonical figures with no distortions. Earlier, outside models summarizing the 2nd edition distorted up to 9 items.
- **Still open:**
  - Carried-over figures not re-read (manual Section 28.9).
  - The guide's Part 7 usage shares were made consistent but not re-read against their source reports.
  - Every checker was from one model family.

**Skills papers.**

- **Skills reference v1.2.** The AI-written v1.1 claimed its skills were all validated and its claims all tested. It listed the old v1.0 quantum lab, cited a harness score as proof of quality, and preferred negative instructions against vendor guidance. v1.2 fixes these and says which skills' files are missing from this project.
- **The prompt-generator skill.** It had "Planetary Council" leftovers, and its practical frameworks used persona lines. Both are removed in 1.2.1.
- **The Task-Type Index.** One rule was reversed: it said zero-shot beats few-shot when only the shape is wrong. Two axis placements also differed from the manual. All three are fixed.

**PDFs.** Each document and a combined volume (178 pages) exist as PDFs for reading and sharing. They are kept outside the project (October 6 decision). The PDFs of the skills reference and the verification report predate the October 6 corrections.

## Sources in depth

### ai-reports/q-advanced-agent-skills-paper.md (from Q-Advanced_AI_Agent_Skills_Deep_Research_Paper.pdf)

**What it gives.** The clearest how-to in the project for skills.

- **Three loading tiers.** Only the name and description load at startup. The SKILL.md body loads when the description matches the task. Scripts and reference files load only when a step asks for them.
- **Five principles:**
  - (A) One skill, one job.
  - (B) The description is the router. Write it in the words people actually type, and include what the skill is not for.
  - (C) Keep the body short; move examples to references/ and exact math to scripts/.
  - (D) Test before adding more: trigger tests, end-to-end tasks run with and without the skill, and adversarial cases.
  - (E) Default to one agent with skills. Use several agents only for parallel or independent-check work, because they cost more.
- **A 10-step build**, from "one sentence that starts with a verb and names the output" to "revise after two weeks of real use."
- **A small-team deployment pattern:** 5–9 focused skills; one verification skill that can run after any skill that produces factual claims; cost and success logging; re-testing after every model upgrade.

**Problems.**

- **It certifies itself.** It was written with AI help and states that no results are fabricated. That line is a claim, not a check.
- **Its SkillsBench figures mix two versions** of that paper.
  - **February 2026 (v1):** 86 tasks in 11 domains; +16.2 percentage points on average; from +4.5 points (software engineering) to +51.9 points (healthcare); no average benefit from self-generated skills.
  - **June 2026 (v4):** 87 tasks in 8 domains across 18 model-harness setups; 33.9% → 50.5% (+16.6 points); +4.1 to +25.7 points per setup.
  - **The paper's errors:** it blends the two, and it writes the healthcare gain as "~52%" when it is percentage points.
- **It leaves out a finding that matters.** In v1, 16 of 84 tasks did worse with curated skills, which is the strongest reason to test every skill with and without.
- **Not checked:** the OSWorld figures, MUSE-Autoskill scores, the 4–15× multi-agent cost, the 20–88% routing savings, the ~40% token reduction and the RecursiveMAS numbers. Treat them as leads.

### ai-reports/agent-skills-research-report.md (from 1000014128.PDF)

**What it gives.**

- Clear boundaries between tools, MCP servers, skills and subagents.
- The format rules (checked against the official spec), a platform table, and how name collisions resolve.
- A 9-step build that adds two things:
  - **trigger optimization** on a train/validation split of requests;
  - **script rules:** no interactive prompts, idempotent, a dry-run flag, JSON output, meaningful exit codes.
- Failure modes worth a checklist:
  - first-person descriptions;
  - catalogs cut off silently;
  - auto-formatters breaking the frontmatter;
  - Windows backslashes;
  - SKILL.md nested too deep in a zip;
  - long sessions pruning the loaded skill.
- Security:
  - skills run with the agent's permissions;
  - malicious skills exist in public registries;
  - injected text written into memory files survives across sessions;
  - least privilege is the baseline.
- Section 16 lists master-prompt requirements, and Section 17 lists its own likely errors.

**Checked and correct.**

- The spec limits match agentskills.io.
- The ToxicSkills figures match Snyk's February 5, 2026 post: 3,984 skills; 36.82% with at least one flaw; 13.4% critical; 76 confirmed malicious.

**Problems.**

- **Misleading source tags.** Almost every sentence is tagged [SOURCED], yet its own run notes say no outside sources were opened. Its works-cited list has 11 entries, all on quantum topics (quantum cognition, quantum agents, quantum machine learning); none supports sections 1–10.
- **Sections 11–15 ("quantum agents") are not reliable.**
- **Its example quantum skill breaks the report's own rules:**
  - it opens with a persona line;
  - its script returns hard-coded output;
  - a leaked citation fragment sits inside a test name;
  - allowed-tools is written as a YAML list instead of a space-separated string.
- **`allowed-tools` is not a security boundary.** The report calls it "an early-stage security boundary". The open spec describes it as "pre-approved tools the skill may use", marked experimental, with support that "may vary between agent implementations": it lists tools a skill may use without asking, so it widens access rather than fencing it (claude/engineering-stack-part-07-tools-and-protocols.md, Sections 4 and 10). Recorded October 20, 2026; the report itself is left unchanged as an AI-written source.

### ai-reports/gemini-ai-engineering-stack.md (from the Gemini Deep Research PDF)

**What it gives.** A twelve-part outline of AI systems work (prompting, context, memory, hardware, retrieval, agents, harness, orchestration, evals, inference, platform, security) and four blueprints (multi-agent orchestration, programmable guardrails, GraphRAG, local models). The mechanisms it names are real and mostly described correctly: reciprocal rank fusion and its k = 60 default, MaxSim, semantic entropy, speculative decoding's acceptance rule, PagedAttention, RadixAttention, LangGraph's checkpoints and interrupts, and gVisor's Sentry and platforms.

**Known problems** (claude/engineering-stack-claim-ledger.md, Sections 1 and 8):

- **It calls itself "peer-reviewed".** One of its 33 works cited is a peer-reviewed version of record. Thirteen are blogs or vendor comparisons, three are mirrors, three did not open, and seven of its sixteen sections cite nothing. It has no inline citations.
- **The overall count.** After the Phase 5 corrections of October 20, 2026: of 137 checkable rows, 50 hold as stated (36.5%), 55 are overstated (40.1%), and 32 are wrong as stated (23.4%: 17 corrected, 7 outdated, 8 unsupported). On October 9 it was 135 rows: 52, 52 and 31.
- **"Deterministic" (12 uses)** is its most repeated error. Deployed inference, safety classifiers and LLM-based guardrails are not deterministic.
- **Retired or superseded on October 9, 2026:** the OpenAI Assistants API (shut down), AutoGen (maintenance mode), LangServe (archived), gpt-4 as a judge (shutdown scheduled for October 23, 2026), Llama Guard 3 (Llama Guard 4 is newer), its unnamed OWASP edition (2026 is current), and H100 as current hardware (Hopper is a previous generation).
- **Terms.** "Harness engineering" is defined wrongly, and "platform engineering" is used for an AI product's API layer.
- **Numbers.** The H100 figures are right but mis-scoped: 3,958 TFLOPS is FP8 with sparsity (dense is 1,979), and 132 SMs is the SXM5 product, not the die. Three numbers have no source: the "15%" MIPROv2 gain, speculative decoding "doubling" tokens per second, and multi-node training being "rarely" compute-bound.
- **The HIPAA example is wrong as stated:** local processing alone does not make a system compliant, and cloud use is allowed under a business associate agreement. Information, not legal advice.
- **Induction heads are presented as settled.** The source is not peer-reviewed, and a later peer-reviewed study finds function-vector heads matter more for few-shot learning in larger models.
- **Gaps:** nothing on MCP, Agent Skills, fine-tuning, observability, prompt caching, reasoning models, evaluation data, computer use or licensing.
- **Format:** the PDF printed every formula as raw LaTeX source.

### Removed uploads, for the record

- **Quantum_Entanglement_Lab_Skill_Guide.pdf** was an AI-written reader guide to lab v1.0. It said all six tests passed and that teleportation of |+⟩ reached fidelity 1 on every branch; that test could not fail (see below). The current lab is documented in its skill folder and the skills reference §4.3.
- **Agent_Skills_Summary_Report.PDF** was a cover sheet for an archive that is not here: an "Omnibus" guide with a "Universal Master Prompt", two skill folders (server-log-triager and cross-model-accuracy-verifier) and three tooling scripts. The skills reference describes both skills (§4.4 and §4.5) and reproduces the verifier's SKILL.md text; neither skill's files are here. If the archive turns up, upload its text files.

### The entanglement lab (skills/quantum-entanglement-lab/)

**What it gives.** The project's complete worked example of a skill:

- one job;
- a description with "do not use" cases;
- three tiers;
- a deterministic script;
- reference cards loaded on request.

**Checked.** v1.2 runs on qutip 5.3.1 and prints all six PASS lines. Its mutation check (evals/mutation_check.py) runs 13 deliberate bugs, each of which stops the lab at the test it targets; a harmless change that must still pass (X·Z for Z·X, a global phase); and a broken lab under `python -O`, which must refuse to run. On October 6, v1.2 behaved as expected in 16 of 16 runs, v1.1 in 12 of 16; on October 7, v1.2.1 (same script) also went 16 of 16. History: v1.0 teleported only |+⟩, which X leaves unchanged, so a broken correction still passed. v1.1 fixed that, but three of its checks could not fail: partial measurement checked only the 50/50 odds, CHSH needed only |S| > 2.8, and `python -O` stripped every assert.

**QuTiP traps:**

- `qutip.qip` is gone in QuTiP 5;
- `fidelity()` returns |⟨a|b⟩| and can exceed 1 for an unnormalized ket (re-checked October 6 on QuTiP 5.3.1);
- `entropy_vn` defaults to the natural log, so use base=2;
- `ptrace(0)` keeps qubit 0.

**Eval pack (October 6).** evals/ holds evals.json (10 trigger and 10 non-trigger requests, 3 end-to-end and 4 adversarial tasks, the with-and-without plan), mutation_check.py, grade_answer.py (its self-test passed all 7 tasks: every known-good answer passes and every known-bad answer fails) and a README. Trigger tests: a first pass in Claude Code on October 8 (claude/trigger-tests-2026-10-08.md); not yet in the Claude app.

**With-and-without test (October 7).** The quick version ran on skill 1.2: one run per task per condition, each a fresh Sonnet 5.5 helper agent working only in its own folder. With the skill, 7 of 7 answers met their rubric, and every helper ran the lab first. Without it, 6 of 7 did; the only miss was e1-run-lab, because there was no lab to run. On the six questions a strong model can answer from what it knows, the skill didn't change correctness and cost about 11% more tokens, because helpers ran the lab even when the question didn't need it. The single-file Claude-app version passed e1 as well: the helper rebuilt all four bundled files, every SHA-256 matched, and the lab passed. Limits: one run per cell, one model, and every helper saw the project's instructions and file list. Answers and grades are in evals/with_without_results.json.

**What the runs found.** The teleportation card didn't say which bit selects X and which selects Z (fixed in 1.2.1). The script prints only two of its measured values, so helpers wrote wrappers to report the rest. One helper noted that "experiments" and "verified lab" in the descriptions can read like real data. And the answer grader's patterns failed three correct answers; they were widened, and the self-test still passes.

**Packaging.** Two descriptions: `description` (365 characters) for Claude Code and other hosts, and `metadata.claude-app-description` (197 characters) for the Claude app, which takes up to 200. skills/build_skill.py builds a folder ZIP for each, plus one SKILL.md for the Claude app's save card, which keeps only SKILL.md; that version bundles the script and reference cards, each with its SHA-256. evals/ is never packaged. Run the trigger tests with whichever description the host uses.

**Lesson.** A test only counts if a wrong answer would fail it.

### 2607.00365v1.pdf: "When AI meets quantum information" (review)

- **§III.E, agents running quantum work:**
  - QAgent, with a reported 71.6% improvement in code-generation correctness over earlier static approaches;
  - quantum coding benchmarks, where models handle basic circuits but struggle with deeper reasoning;
  - theorem-proving agents that check results in Lean;
  - lab agents.
- **§III.C:** circuit-discovery agents scale better with reusable sub-circuits ("gadgets"). This is an analogy for skill libraries, not evidence about them.
- **§IV.D:** quantum ideas used to analyze classical networks, with the caution that classical networks have no real entanglement.
- **§V:** weak baselines, incomplete cost accounting, favorable test problems, too few negative results. The same checklist fits any claim about a prompt or a skill.

### 2512.07737v2.pdf: AlphaQubit 2

A neural decoder for quantum error correction, with a compact real-time variant. Practices that transfer:

- a two-tier design, accurate and fast;
- curriculum learning;
- staged adaptation;
- test data from a separate, simpler pipeline;
- confidence intervals;
- stress tests far beyond the training range.

### s41598-026-51870-8.pdf: chaos-aware hybrid classifier

It gains about 1.6–1.8 percentage points at 4, 6 and 8 qubits and loses 2.2 points at 10 qubits. Its paired-difference reporting, with confidence intervals and win rates, is a template for with-and-without skill tests. Its small simulated setup limits the claims.

### s41534-026-01360-6_reference.pdf and 2510.04929v1.pdf

Peer-reviewed and preprint quantum algorithms (linear matrix equations; the Quantum Hermite Transform). They contain no AI content. Both state the limits of their advantage plainly.

## Planetary Council extraction (October 2, 2026)

**Added:**

- claude/multi-lens-review-method.md;
- claude/research-verification-toolkit.md;
- claude/prompt-suite-method.md;
- the quantum lab skill v1.1 and the updated entanglement_lab.py;
- (October 3) the corrected prompt-generator skill, 1.2.1.

**Left out:** every character and voice, the shared rules copied into all 13 skills, and the generator's scripts (they stay in the package).

**Findings.**

- **The prompt generator's quality score can be gamed.** A suite of 50 "say the word banana" prompts scored 0.880, above the real suite's 0.857. Treat the harness as a format check.
- **The Claude app caps skill descriptions at 200 characters;** the agentskills.io spec allows 1,024.
- **All 13 skills pass the spec's name rules,** and every SKILL.md body is under 500 lines.

## What the batch teaches about prompting, agents and skills

1. Skills are how prompting knowledge gets packaged.
2. Testing decides everything. A test that cannot fail proves nothing; the lab's v1.0 test, three of its v1.1 checks and the generator's harness all show this.
3. Write the description for the router: third person, the phrases people type, and what the skill is not for.
4. Keep the always-loaded part small.
5. Start with one agent. Add more only for parallel or independent work, and count the cost.
6. Security is part of the build.
7. AI-written research needs the project's existing checks. The final editions show the scale: 172 review findings and 12 missing scopes in a document that had already been "checked".
8. Restatement is where numbers break. Outside models summarizing the 2nd edition distorted up to 9 canonical figures, while the 3rd edition's scoped wording held up in two fresh summaries.
9. Copies drift. A PDF copy is out of date the moment its .md is corrected, and old editions keep turning up in search: on October 6, a search about PoT and PAL returned two passages from the superseded first edition, which labels those figures "Verified" where the third edition says "reported". Keep one working copy of each document.
10. A with-and-without test shows where a skill earns its place. In the lab's quick test (one run per task, Sonnet 5.5 helpers), the skill mattered only where it supplied something the model lacked: verified code to run. On questions the model could already answer, it added cost, not accuracy.
11. A trigger test checks the description, not the skill. In the first pass (October 8, Claude Code, one run per request), the skills loaded when a request asked to check, run, solve or show something, or involved a file, and were skipped for quick textbook questions the model answered itself.

## For the master skill-building prompt

1. **Intake before drafting:** the one job, the users, 10 should-trigger and 10 should-not-trigger requests, and the tools and permissions.
2. **Spec validation:** agentskills.io rules, and a 200-character description for the Claude app.
3. **Description rules:** third person, triggers and exclusions, tuned on a train/validation split.
4. **Body limits:** under 500 lines; examples to references/ and exact logic to scripts/.
5. **Script rules:** no interactive prompts, idempotent, a dry run for destructive actions, JSON output, exit codes.
6. **Eval pack:** trigger tests, with-and-without tasks, adversarial cases, and proof that each test can fail.
7. **Security pass:** minimal allowed-tools, no unchecked input reaching a shell, no writes to memory or instruction files from fetched content.
8. **No persona;** give the reason for each rule.
9. **Re-test on every model change.**
10. **End with the claims most likely to be wrong.**
11. **Package for the target:** for the Claude app, a ZIP with the skill folder at its root, or one SKILL.md with the other files bundled for the save card (skills/build_skill.py builds both); shared rules copied into each skill.

claude/skills-booklet.md now walks through all eleven, step by step. The handoff suggests rebuilding the missing skill-builder from it.

## Housekeeping

- claude/github-tutor-prompt.md has an "ABOUT ME" block with its author's own details. Replace it before sharing the prompt.
- Decide whether qubit-math and trig-check should load for quick textbook questions, then fix their descriptions and re-test (claude/trigger-tests-2026-10-08.md).
- Re-run the trigger tests with three runs per request, then with the Claude-app descriptions, then by hand in the Claude app. For firmer with-and-without numbers on the lab, add the remaining two runs per task per condition.
- Consider having the lab script print each test's measured value, not only PASS; helpers wrote wrappers to get them.
- Check whether project chats read formulas from the chapter PDFs' page images: ask about a formula on a known page and compare the answer with the page.
- Run with-and-without tests for trig-check, qubit-math and book-chapter-splitter (their evals/README.md files).
- Confirm book-chapter-splitter's intake answers, which Claude drafted (its evals/evals.json).
- The Claude Code starter kit (prompting-kit.zip) lives outside the project. If it goes on GitHub, keep the repository private.
- Decide whether the lab's descriptions should say "simulated" rather than "experiments" and "verified lab", so its output isn't read as real data.
- Left as is: the manual's and the guide's edition lines say September 2026, though their checks finished in October.
- The flags the engineering-stack series held against project docs (the claim ledger's four taxonomy flags, the parts' Section 10 flags, the claim-ledger notes and Part 04's lab change) were applied on October 20, 2026, with the owner's approval; the list and where each went are in claude/engineering-stack-overview.md, Appendix J, and claim ledger §12. Claim-ledger row P5-09's slip (8.6 for 9.3) is fixed. Still held: the same low-temperature wording in skills/sophisticated-prompt-generator/SKILL.md, Procedure step 3, found after the approved list was drawn up.
- Run the series' separate-session review (claude/engineering-stack-overview.md, Appendix L).
- The engineering-stack checkers' raw notes went to the owner as engineering-stack-research-2026-10-09.zip on October 9, Part 02's as engineering-stack-research-part-02.zip and Part 03's as engineering-stack-research-part-03.zip on October 12, Parts 04's and 05's as engineering-stack-research-part-04.zip and engineering-stack-research-part-05.zip on October 13, Parts 06's and 07's as engineering-stack-research-part-06.zip and engineering-stack-research-part-07.zip on October 14, and Parts 08's, 09's and 10's as engineering-stack-research-part-08.zip, engineering-stack-research-part-09.zip and engineering-stack-research-part-10.zip on October 15, and Parts 11's and 12's as engineering-stack-research-part-11.zip and engineering-stack-research-part-12.zip on October 19, and Part 13's as engineering-stack-research-part-13.zip on October 20; they are not in the project. Each part's lab folder goes to the owner as engineering-stack-lab-part-NN.zip.

## How this was checked

- **October 2:**
  - Ran the lab script v1.0 and v1.1, plus mutation tests.
  - Checked the QuTiP traps.
  - Ran the prompt generator's scripts and the nonsense-suite test.
  - Checked the Planetary skills against the spec.
  - Compared SkillsBench (v1 and v4), ToxicSkills, the spec and the Claude-app limits with their sources.
  - Read the quantum papers.
- **October 3–5:**
  - Ran Edition Protocol v3 on the final editions: citation and Canonical Figures audits against primary sources, three independent reviews, adjudication and fixes, and fidelity summaries on two models.
  - Recomputed the stated answers in the examples by script.
  - Built and visually checked the PDFs.
  - Details are in claude/verification-and-benchmark-report.md.
- **October 6:**
  - Read five of the PDF copies in full and spot-checked the rest against their .md docs: same final text.
  - Converted the two AI-written uploads with pymupdf4llm 1.28.2, rebuilt their tables and code blocks from the page images, and compared each .md with the PDF's own text word by word: the Q-Advanced paper 3,013 of 3,013 words; the research report 99.25%, every difference a layout fix (repeated table headers, words split across table-cell lines, code lines wrapped at the page edge).
  - Fixed two slips in the verification report (a cross-reference and the drafting sources) and one in the skills reference (the skill-builder version), and checked both files word by word against their PDF twins: only the intended changes differ.
  - Ran QuTiP 5.3.1 to confirm the fidelity() wording: |0⟩ against |+⟩ gives 0.7071, and an unnormalized ket can give 2.0.
  - Confirmed the cleanup: 25 docs and the 5 quantum papers, with no leftover PDFs and nothing missing.
  - Built the lab's eval pack, then broke the lab on purpose: v1.2 behaved as expected in 16 of 16 mutation runs, v1.1 in 12 of 16. The answer grader's self-test passed all 7 tasks, and five other good and three other bad wordings were graded as expected.
  - Checked the updated New Skills Appendix and skills reference word by word against their PDF twins: only the intended changes differ.
- **October 6–7:**
  - Opened the three reference books: title pages, licenses, tables of contents and samples of their extracted text.
  - Built both lab versions with skills/build_skill.py: every spec check passed, and each bundled file reads back byte for byte from the single-file version.
  - Ran the quick with-and-without test: 15 helper runs, counting the pilot and the Claude-app check. Checked each helper's tool log for lab runs and for anything outside its folder (none), graded every answer by pattern and by reading it against its rubric, and widened three patterns that had failed correct answers.
  - Re-ran the mutation check and the grader self-test after the 1.2.1 changes: 16 of 16, and 7 of 7.
- **October 7 (afternoon):**
  - Built trig-check and qubit-math. Their tests pass (21 of 21 and 25 of 25), their mutation checks behaved as expected (14 of 14 and 15 of 15 runs), and both graders' self-tests passed (5 of 5). One trig-check guard test couldn't fail at first (`Symbol(x)` was refused for another reason) and was replaced with `factorial(5)`.
  - Checked the install steps against the Claude Help Center, the Claude Code, Cursor, Gemini CLI and OpenAI docs, and the Agent Skills client list.
- **October 8:**
  - Split the three books with PyMuPDF 1.28.2, finding each chapter's pages from the trig book's outline and, for the other two, the chapter headings and printed page numbers. Every chapter page's text matched its source page exactly; each chapter's first page carries its heading, and the next chapter opens right after each range (after a blank page, left out, for trig chapters 3 and 7). The first and last pages of all 11 files were looked at, and pypdf 5.9 opened each file with the same page count.
  - After the owner's uploads, read each of the 11 chapters back through the project tool: front pages, chapter opening and chapter end all present. Read the knowledge size before the upload, after it, and after removing the full books.
  - Read the Claude Help Center's upload page for how PDFs are handled.
- **October 8 (later):**
  - Re-ran all three eval packs: the lab's mutation check 16 of 16 and grader 7 of 7; trig-check 21 tests, 14 of 14 and 5 of 5; qubit-math 25 tests, 15 of 15 and 5 of 5. The rebuilt packages were byte-identical to October 7's.
  - Checked the Claude app, Claude Code and spec facts in the booklet and handoff against the Help Center, the Claude Code docs, agentskills.io and each tool's own docs, using two separate fact-check passes, plus the installed Claude Code's own help text.
  - Built book-chapter-splitter: 22 tests pass, its mutation check ran 17 of 17 as expected, and its grader passed 5 of 5. It re-made the 11 chapter files from the original books, and PyMuPDF found the same page count and identical text on every page compared with the uploaded files.
  - Ran the first trigger tests: 80 cases, one run each, with `claude plugin eval` in Claude Code 2.1.294 (claude-sonnet-5-5), after `claude plugin validate --strict` passed on the test plugin. Re-ran three missed cases with their transcripts kept and read them.
- **October 9:**
  - Converted the Gemini PDF with a script, rebuilt its 16 tables from the page images, and checked that every word of its text layer is present in order.
  - Opened all 33 of its works cited and about 110 primary sources: seven checker agents with at most 40 web lookups each, then the lead re-opened the headline sources. Ran the ledger's arithmetic in Python 3.13.16 (ledger Section 5).
  - Read package data from PyPI's JSON API, npm and git tags on GitHub, and re-ran the PyPI script printed in the freshness ledger; it reproduced the earlier run except for three packages released in between.
  - Counted the verdicts and generated the axes-test table by script; checked that every source key in the ledger resolves and that the new files contain no em dashes.
- **October 9 (evening), Part 01:**
  - Built and ran the lab on Linux with Python 3.13.16 (pip 26.2.1) and Ubuntu's 3.12.3 (pip 24.0): 7 of 7 steps, and 7 of 7 mutations behaving as expected; rendered the part's Mermaid diagram with mermaid-cli 12.0.0.
  - A blind source check on a separate agent (a Sonnet model) re-checked the 94 [V] claims from their sources alone: 54 supported, 39 partly supported, none contradicted. A beginner test on another agent followed the Linux steps literally and found 15 problems. All findings were checked and fixed (claude/engineering-stack-part-01-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-01.zip; it is not in the project.
- **October 10 to 12, Part 02:**
  - Two research agents opened the papers, vendor docs and tool repositories; their claim tables were checked by the lead before use.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 8 of 8 checks and 11 of 11 mutations as expected, also with `--offline` and with PyPI unreachable. Every statistic matched scikit-learn 1.9.1, statsmodels 0.15.0 and SciPy 1.18.1 (69 comparisons). Ran promptfoo 0.124.1 on Node.js 22.22.0 with no key; rendered the part's Mermaid diagram with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 76 claims from their sources alone: 74 supported, 2 partly supported, none contradicted. A beginner test on another agent followed Sections 7 to 9 literally and found 17 problems. All findings were checked and fixed (claude/engineering-stack-part-02-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-02.zip; it is not in the project.
- **October 12, Part 03:**
  - Re-checked Part 03's freshness rows (PyPI, both vendors' structured-output, tool, thinking and reasoning pages, the Workbench, DSPy's optimizer pages) before writing; the lead re-read the decisive pages (forced tool use, the thinking retirement, effort levels, JSONSchemaBench's tables).
  - Two research agents returned 72 and 56 claim rows from vendor docs, repositories read from shallow clones, and the papers; the lead checked them before use.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 7 of 7 core checks, 9 of 9 with the optional Pydantic and DSPy 3.4.0 checks, and 17 of 17 mutations caught; the DSPy check also ran with the network blocked. Rendered both Mermaid diagrams with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 148 claims from their sources alone: 137 supported, 8 partly supported, 3 not checkable, none contradicted. A beginner test on another agent followed Sections 7 to 9 literally and found 16 problems. All findings were reproduced, then fixed (claude/engineering-stack-part-03-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-03.zip and the raw notes as engineering-stack-research-part-03.zip; neither is in the project.
- **October 13, Part 04:**
  - Two research agents returned 71 and 78 claim rows from vendor docs, pricing pages, release-tag source code and papers; the lead re-read the decisive ones (Liu et al.'s tables, vLLM and SGLang defaults).
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 13 of 13 checks and 15 of 15 mutations caught; every output block in the part re-run by script and matched; the Ollama path run against a stand-in server.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 154 claims from their sources alone: 128 supported, 23 partly supported, 3 not checkable, none contradicted. A beginner test on another agent followed Sections 3 and 7 to 9 literally and found 15 problems. All findings were reproduced, then fixed (claude/engineering-stack-part-04-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-04.zip and the raw notes as engineering-stack-research-part-04.zip; neither is in the project.
- **October 13, Part 05:**
  - Re-checked Part 05's freshness rows (PyPI at 23:16 UTC, GitHub tags) before writing. Two research agents returned 43 and 32 claim rows from papers, vendor docs and source code read from shallow clones; the lead re-read the decisive ones in source (Elasticsearch's Enterprise gate on its RRF retriever, Qdrant's RRF formula, bm25s's Lucene scoring) and every repository link.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 19 of 19 checks and 16 of 16 mutations caught (11 of 16 on the first run, fixed), with an unbroken-copy control; BM25 matched bm25s 0.3.13 to within 1e-7 and the metrics matched ir_measures 0.4.3 exactly; the real-models script ran against a stand-in module. Rendered both Mermaid diagrams with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 160 claims from their sources alone: 141 supported, 18 partly supported, 1 not checkable, none contradicted; one finding didn't reproduce. A beginner test on another agent followed Sections 3 and 7 to 9 literally on all three Pythons and found 14 problems. Findings were reproduced, then fixed, except four whose fix only removed or weakened wording (claude/engineering-stack-part-05-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-05.zip and the raw notes as engineering-stack-research-part-05.zip; neither is in the project.
- **October 14, Part 06:**
  - Re-checked Part 06's freshness rows (PyPI, GitHub tags) before writing. Two research agents returned 42 and 37 claim rows from papers, vendor docs and source code; the lead re-read in source the GraphRAG maintenance notice (and dated it from git history), Letta's retirement notice and PyPI history, Mem0's add-only default, and networkx's Leiden.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 21 of 21 checks and 16 of 16 mutations caught (one first-run miss was an equivalent mutant, replaced), with an unbroken-copy control; modularity, communities and paths matched networkx 3.7 and 3.6.1. Rendered both Mermaid diagrams with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 127 claims from their sources alone: 112 supported, 14 partly supported, 1 not checkable, none contradicted. A beginner test on another agent followed Sections 3 and 7 to 9 literally on all three Pythons and found 14 problems, none blocking. Findings were reproduced, then fixed (claude/engineering-stack-part-06-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-06.zip and the raw notes as engineering-stack-research-part-06.zip; neither is in the project.
- **October 14, Part 07:**
  - Re-checked Part 07's freshness rows (PyPI, npm, the spec's git tags) before writing; found the TypeScript SDK split (version 1 stops at 2025-11-25). Two research agents returned 67 and 67 claim rows, mostly from git clones of the specifications and SDKs with file and line; the lead re-read in source the 2026-07-28 changelog, the MRTR, discovery and schema pages, the npm packages and the `mcp-remote` fix version.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 22 of 22 checks and 20 of 20 mutations caught (5 first-run catches were crashes; the checks were restructured so each reports a FAIL line), with an unbroken-copy control; 8 of 8 interop checks against `mcp` 2.3.0 in both directions, including the SDK client completing the lab server's input_required round. Rendered the Mermaid diagram with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 209 claims from their sources alone: 194 supported, 12 partly supported, 3 not checkable, none contradicted. A beginner test on another agent followed Sections 7 to 9 literally on all three Pythons and found 18 problems, none blocking. Findings were reproduced, then fixed (claude/engineering-stack-part-07-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-07.zip and the raw notes as engineering-stack-research-part-07.zip; neither is in the project.
- **October 14 to 15, Part 08:**
  - Re-checked Part 08's freshness rows before writing (gVisor and Firecracker unchanged; Docker Engine 29.9.1; anthropic 1.14.0). Three research agents returned 79, 78 and 60 claim rows; the lead re-read in source the computer-use toolset page, both SDKs' turn-cap defaults, Firecracker's specification and three licence files.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 27 of 27 checks and 28 of 28 mutations caught (a near-equivalent first-run miss was answered with a new check), with an unbroken-copy control; 3 of 3 cross-checks against openai-agents 0.23.1 with a fake model and tracing off. Rendered the Mermaid diagram with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 187 claims: 174 supported, 13 partly, none contradicted. A security review on another agent found 17 issues, 4 high (the `docker run` checker could be fooled, timed-out tools kept running, the screen harness trusted the model's own label, and exception text could carry secrets to the model); all were reproduced and fixed. A beginner test followed Sections 7 to 9 on all three Pythons and found 13 problems, none blocking (claude/engineering-stack-part-08-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-08.zip and the raw notes as engineering-stack-research-part-08.zip; neither is in the project.
- **October 15, Part 09:**
  - Re-checked Part 09's freshness rows before writing (openai-agents 0.24.0 and agent-framework 1.22.0 released that day; langgraph 1.2.15; crewai 1.15.28). Two research agents returned 89 and 84 claim rows, mostly from PyPI wheels and git clones; the lead re-read in source LangGraph's step-limit and retry defaults, Temporal's retry defaults and history limits, and the Anthropic SDK's retry constants, and re-read Anthropic's multi-agent post and Kim et al.'s abstract.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 30 of 30 checks and 33 of 33 mutations caught (two first-run misses were gaps in the checks, now covered), with an unbroken-copy control and a real process killed mid-step; 6 of 6 cross-checks against LangGraph 1.2.15 with network connections blocked. Rendered the Mermaid diagram with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 170 claims: 163 supported (7 of them only in their sourced part, being negative or about the part's own work), 7 partly, none contradicted. A beginner test followed Sections 7 to 9 on all three Pythons and found 21 problems, none high; the most useful was that the checks left temporary folders behind, so the scripts now clean up (claude/engineering-stack-part-09-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-09.zip and the raw notes as engineering-stack-research-part-09.zip; neither is in the project.
- **October 15, Part 10:**
  - Re-checked Part 10's freshness rows before writing (OWASP's 2026 edition dated from its repository; nothing newer than Llama Guard 4 or Prompt Guard 2; NeMo Guardrails, garak and Presidio unchanged; the HIPAA update still a proposal). Three research agents returned 49, 84 and 83 claim rows; the lead re-read in source NeMo's telemetry defaults, Presidio's first-use downloads, the OWASP 2026 text, the reginfo.gov agenda entry and Nasr et al.'s Table 7.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 28 of 28 checks and 50 of 50 mutations caught, with an unbroken-copy control; 7 of 7 cross-checks against presidio-analyzer 2.2.364 and python-stdnum 2.2 with network connections blocked (two attempted lookups recorded). Found and fixed a stale-bytecode trap in the mutation runner.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 179 claims: 136 supported, 33 partly, 10 not checkable, none contradicted. A beginner test followed Sections 6 to 9 on all three Pythons and found 3 low problems. The security review agent stopped when a safety classifier blocked its testing; it did not work around the stop, and the lead ran harmless edge cases with reserved names instead, finding three gaps in the lab's own defences, now fixed (claude/engineering-stack-part-10-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-10.zip and the raw notes as engineering-stack-research-part-10.zip; neither is in the project.
- **October 16 to 19, Part 11:**
  - Re-checked Part 11's freshness rows before writing (PyPI and git tags on October 16: sglang 0.5.22, mlx-lm 0.32.2, llama.cpp b11691, Ollama v0.40.5). Three research agents returned 166, 143 and 76 claim rows, mostly from git clones at pinned tags; the lead re-read in source llama.cpp's Q4_K_M rules and block layouts, gpt-oss's layer shapes, and Ollama's documented API and Windows steps.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 14 of 14 checks and 31 of 31 mutations caught, with an unbroken-copy control; the lab reproduced llama.cpp's published bits per weight for five types to four decimal places and the gpt-oss model card's sizes; the reader test ran against a stand-in for Ollama. Rendered the Mermaid diagram with mermaid-cli 12.0.0.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 207 claims: 172 supported, 31 partly, 4 not checkable, none contradicted. A beginner test followed Sections 6 to 9 on all three Pythons and found 25 problems (the 1 high one, PowerShell's script policy, read through rather than run). Usage limits and a container restart stopped the agents on October 16; check B finished when resumed that evening, and the beginner test was rerun on October 19. Every finding was reproduced before it was fixed; a checker's side note led to Meta's newer Muse models, confirmed on Meta's verified Hugging Face organization (claude/engineering-stack-part-11-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-11.zip and the raw notes as engineering-stack-research-part-11.zip; neither is in the project.

- **October 19, Part 12:**
  - Re-checked Part 12's freshness rows before writing (PyPI on October 19: transformers 5.20.2, peft 0.21.2, trl 1.16.0, unsloth 2026.10.7, axolotl 0.21.0, llamafactory 0.9.5; torchtune's last release April 2025). Two research agents returned 56 and 85 claim rows, mostly from git clones at pinned tags and wheels from PyPI; the lead re-read in source PEFT's printed example, defaults and target modules, TRL's telemetry, the Llama 3, 3.1, 3.2 and 4 licence clauses, Unsloth's licence headers (recounted from the wheel), OpenAI's fine-tuning dates, the Gemini API's tuning notice, Muse Spark Open's card, GPT-3's Table 2.1 and 13-word rule, and four model configuration files.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 17 of 17 checks and 33 of 33 mutations caught (one first-run miss, an isolated role check, was a gap in the checks, now closed), with an unbroken-copy control and a fresh unzip; the lab reproduced PEFT 0.21.2's printed counts for Qwen2.5-3B (3,686,400 and 3,089,625,088) and the LoRA paper's GPT-3 counts exactly.
  - Two blind source checks on separate agents (a Sonnet model) re-checked 171 claims: 149 supported, 18 partly, 4 not checkable, none contradicted. A beginner test followed Sections 6 to 9 on all three Pythons and found 30 problems (2 high). Every finding was reproduced before it was fixed (claude/engineering-stack-part-12-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-12.zip and the raw notes as engineering-stack-research-part-12.zip; neither is in the project.
- **October 20, Part 13:**
  - Re-checked Part 13's freshness rows before writing (PyPI on October 20: fastapi 0.156.1, anthropic 1.16.0, arize-phoenix 20.23.0; the GenAI conventions' move dated from git history; the vendors' batch, streaming and pricing pages). Two research agents returned claim tables from git clones, wheels and pages; the lead re-read in source FastAPI's SSE encoder, ping, headers and telemetry opt-in, Starlette's gzip exclusion, sse-starlette's defaults, the conventions' span name, content rule and metric renames, Traceloop's, OpenLIT's and Logfire's content defaults, vLLM's usage-statistics switches, Phoenix's host and authentication defaults, Langfuse's Compose file and OWASP's LLM02:2026 text.
  - Built and ran the lab on Linux with Python 3.13.16, Ubuntu's 3.12.3 and 3.11.17: 21 of 21 checks and 48 of 48 mutations caught on each (17 and 32 before the security fixes), with an unbroken-copy control and a fresh unzip; 7 of 7 cross-checks against FastAPI 0.156.1, uvicorn 0.54.0 and the OpenTelemetry SDK 1.45.1 with network access blocked (0 attempts).
  - Two blind source checks on separate agents re-checked 158 claims: 114 supported, 34 partly, 3 contradicted (a FastAPI version, the worked example's daily average, and "prices double" for all Gemini models), 7 not checkable. A beginner test followed Sections 6 to 9 on all three Pythons and found 16 problems, none high. A security review tested the lab on loopback addresses only and read the advice: 21 findings, 2 high. Every finding was reproduced before it was fixed (claude/engineering-stack-part-13-review.md).
  - The lab folder went to the owner as engineering-stack-lab-part-13.zip and the raw notes as engineering-stack-research-part-13.zip; neither is in the project.
- **October 20, Phase 5:** applied the 21 held flags on exact copies of each document, patched with checks that each old text occurs once, and compared by diff before saving; no em dashes added. Part 04's `placement_test.py` was rebuilt from the part's listings and changed: the lab's 13 of 13 checks and its 15 mutations passed on Python 3.13.16, 3.12.3 and 3.11.17, the old misleading timeout message was reproduced against a slow stand-in server, and the new timeout, refused-connection and `--no-think` paths ran against stand-in servers. The overview's 71 figure strings were found in their cited parts by script, all 41 of its project paths resolve, and nine download sources the parts don't name were replaced before saving. The verdict totals of the claim ledger were recounted by script (163 rows).
- **October 19, Windows run:** the Part 11 reader tests R1 to R4 ran on the owner's computer by script (claude/engineering-stack-windows-run-2026-10-19.md); Part 11's results section and Section 7.5 were updated from the log the same day.
- **October 20, Windows run:** with the owner's go-ahead, the reader tests of Parts 03 to 10 and 12 ran on his computer by five double-clicked scripts (claude/engineering-stack-windows-run-2026-10-20.md). Each part was then updated from the logs on an exact copy of its project version, checked by diff: a "Results so far" note under its run table, a Windows-run entry in its checks, settled [R] tags turned to [T] with the date, and its tag counts.

## Sources

- Agent Skills specification: https://agentskills.io/specification
- Claude Help Center, "How to create custom skills": https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- Claude Help Center, "Upload files to Claude" (PDF handling and project files): https://support.claude.com/en/articles/8241126-upload-files-to-claude
- Claude Help Center, "Use skills in Claude": https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Claude Help Center, projects and project instructions: https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- Claude Help Center, RAG for projects: https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects
- Claude Code docs, skills: https://code.claude.com/docs/en/skills
- Claude Code docs, plugin evals: https://code.claude.com/docs/en/plugin-evals
- SkillsBench, arXiv 2602.12670: https://arxiv.org/abs/2602.12670 · February version: https://arxiv.org/abs/2602.12670v1
- Snyk, "ToxicSkills" (February 5, 2026): https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub
- Chain of Draft, arXiv 2502.18600: https://arxiv.org/abs/2502.18600
- Chain-of-Symbol, arXiv 2305.10276: https://arxiv.org/abs/2305.10276
- Self-Consistency, arXiv 2203.11171: https://arxiv.org/abs/2203.11171
- GEPA, arXiv 2507.19457 (version 2): https://arxiv.org/abs/2507.19457

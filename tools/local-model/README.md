# Local-model bridge (setup Stage 4)

Lets Claude Code hand small text jobs to the local model in Ollama on this PC, through one MCP tool, `ask_local_model(prompt, file_path, max_tokens)`. Standard library only: no installs, no account, nothing leaves this computer.

| File | What it is |
|---|---|
| `local_model_server.py` | The MCP server over stdio. Built on the Part 07 lab; answers both the classic handshake (`initialize`) and revision 2026-07-28 (`server/discover`) |
| `check_bridge.py` | 21 offline checks against a stand-in Ollama, then three timed live jobs on the real model |
| `../../.mcp.json.example` | A template. Copy it to `.mcp.json` in the repository root and fill in the two paths; Claude Code then registers the server as `local-model`. Your `.mcp.json` stays local (it's git-ignored) |
| `../../.claude/skills/local-model/SKILL.md` | Tells Claude which jobs to send and how to treat the answers |

## How it saves usage

Given `file_path`, the server reads the file itself and sends it to the model, so the file's text never passes through Claude; Claude sees only the short answer and a timing footer. The call and the answer still cost tokens, so the saving is small on short files. On files of a few thousand tokens the saving would be bigger, but Test 3 below (October 26, 2026) found those summaries too unreliable to use without reading the file, which cancels the saving.

## Safety

- Talks only to Ollama on this computer (`127.0.0.1`, `localhost` or `::1`) and ignores proxy settings.
- Reads only text files inside the workspace, up to 200,000 bytes; never writes.
- Refuses a job too big for the model's 8,192-token window instead of letting Ollama drop part of it.
- Turns off qwen3's hidden reasoning (`think: false`) and strips any `<think>` text that still appears.
- Labels every answer "unchecked draft".

## Settings

| Variable | Default |
|---|---|
| `LOCAL_MODEL` | `qwen3:1.7b` |
| `LOCAL_MODEL_CTX` | `8192` |
| `LOCAL_MODEL_HOST` | `http://127.0.0.1:11434` |

## Test results, October 21, 2026 [T]

qwen3:1.7b, Ollama 0.40.6, this PC, `python tools/local-model/check_bridge.py`. Offline checks: 21 of 21 passed, both runs.

**Run 2 (current design: the job placed after the file)**

| Job | Read: tokens, seconds, per second | Wrote: tokens, seconds, per second | Total seconds | Result |
|---|---|---|---|---|
| Tag 8 notes (no file) | 246, 0.1, cached | 36, 4.3, 8.4 | 4.6 | 7 of 8 tags right (note 6 tagged `git`, should be `council`) |
| Summarize Part 07's README in 3 bullets | 598, 8.2, 73 | 87, 10.9, 8.0 | 19.2 | 3 bullets, all accurate; a file list that misses that the lab needs no installs or internet |
| List dates and versions in `README.md` | 934, 13.9, 67 | 155, 18.1, 8.5 | 32.1 | Dates 0 of 4; versions 4 of 4, plus 14 lines not in the file (the prompt's examples `v2` and `4.0.1`, and invented ones) |

The tagging job read 0.1 s because Ollama reused the identical prompt from run 1; it isn't a reading speed.

**Run 1 (the job placed before the file)**

| Job | Read: tokens, seconds, per second | Wrote: tokens, seconds, per second | Load seconds | Total seconds | Result |
|---|---|---|---|---|---|
| Tag 8 notes | 246, 3.6, 68 | 36, 3.8, 9.4 | 10.6 (cold start) | 18.1 | 7 of 8 tags right (same miss) |
| Summarize Part 07's README | 598, 7.3, 82 | 66, 6.9, 9.6 | 0.0 | 14.2 | 3 accurate bullets |
| List dates and versions | 934, 12.7, 73 | 200, 24.9, 8.0 | 0.0 | 37.7 | Failed: copied the file out until the 200-token limit |

**Live in Claude Code** (a new session in this folder; the tool loaded as `mcp__local-model__ask_local_model`)

| Job | Read: tokens, seconds, per second | Wrote: tokens, seconds, per second | Load seconds | Total seconds | Result |
|---|---|---|---|---|---|
| Tag 5 new notes (no file) | 191, 3.0, 63 | 22, 2.5, 9.0 | 5.4 | 10.9 | 3 of 5 right: swapped note 1 (Mars ratings, `council`) and note 2 (pushing to GitHub, `git`) |
| Summarize `research/engineering-stack/INVENTORY.md` in 3 bullets, without Claude reading it first | 1362, 20.3, 67 | 93, 11.3, 8.2 | 0.0 | 31.7 | 2 bullets accurate, 1 partly accurate (it folded the separate freshness-ledger re-check into the review) |

**What this means**

- Speed: it writes 8.0 to 9.6 tokens per second and reads 63 to 82 tokens per second (63 in the live Claude Code test); loading the model cold took 10.6 s.
- Good enough for tagging and rough summaries: 10 of 13 tags right across both tests, and summaries mostly accurate. It misses tags that need workspace knowledge (it doesn't know Mars is a council planet), so describe each tag in a few words. Not for exact extraction: use Grep or a script.
- Open: try the Qwen3-4B file already on disk (`Downloads\Qwen3-4B-Q4_K_M.gguf`) in Ollama on the extraction job. It needs no download; Part 11 measured it at 3.93 tokens per second on the processor in llama.cpp.

## Test 3: summaries of longer files (October 26, 2026)

The October 26 council run found that nobody had measured the claim that the bridge "pays off on files of a few thousand tokens". This test checks it. Same model (qwen3:1.7b), same PC, called through `ask_local_model` from Claude Code. Every job: "Summarize this file in 3 bullets: what the file is, its main points, and its conclusion or current status", with `max_tokens` 250. The five calls were sent at once. Scores are Claude's reading of each summary against its file.

| File | Characters | Read: tokens, seconds, per second | Wrote: tokens, seconds, per second | Result |
|---|---|---|---|---|
| `research/council-runs/2026-10-26-system-review/COUNCIL_BRIEF.md` | 14,269 | 3912, 77.3, 51 | 83, 23.1, 3.6 | 3 bullets; one point backwards (calls the bookkeeping careful; the brief says bookkeeping is the weak spot) |
| `research/council-runs/2026-10-26-system-review/saturn.md` | 12,102 | 3528, 67.1, 53 | 128, 31.3, 4.1 | 3 bullets, partly right ("fix the workspace's memory" became "memory management") |
| `CODEX_COMMUNICATION.md` | 17,067 | 4147, 83.2, 50 | 230, 63.9, 3.6 | Failed: copied the file's header first, then one wrong claim (all proposals still pending) |
| `research/prompting/edition-protocol-v3.md` | 12,081 | 2897, 54.1, 54 | 110, 24.8, 4.4 | A paragraph, not bullets; 2 points right, 2 partly, 1 wrong (calls itself the Taxonomy's Third Edition, which it produced) |
| `research/engineering-stack/docs/records/engineering-stack-windows-run-2026-10-20.md` | 16,060 | 5693, 134.8, 42 | 250, 96.7, 2.6 | Failed: copied the file until the 250-token limit |
| The same Windows record, run again alone | 16,060 | 5693, 0.5, cached | 105, 39.0, 2.7 | 3 bullets; right about what passed, silent on the tests that timed out or weren't run, wrong part range ("03 to 12"; Part 11 isn't in it) |

The first three files in the table are in the owner's private workspace, not in this public copy.

**What this means**
- **Quality:** 0 of 5 files got a fully accurate summary, and 2 of 6 attempts copied the file instead. Every summary had at least one misleading point.
- **Speed:** writing slowed as the file got longer: 4.4 tokens per second at 2,897 tokens read, down to 2.6 to 2.7 at 5,693. The October 21 jobs read 598 to 1,362 tokens and wrote at 8.0 to 9.6. Run alone, the Windows job wrote at 2.7 against 2.6 in the batch, so sending the jobs at once wasn't the cause.
- **Claude tokens:** reading the five files would have put about 17,900 tokens into Claude's context [I: characters ÷ 4]; the five answers put in about 1,500 [I]. That saves about 16,000 tokens. But no summary was safe to use without checking, and checking means reading the file, so the saving disappears whenever the answer matters.
- **Verdict:** on this PC, the bridge doesn't pay off for summaries of files of a few thousand tokens. Its tested uses are tagging and rough summaries of short files (up to about 1,400 tokens, the October 21 range).

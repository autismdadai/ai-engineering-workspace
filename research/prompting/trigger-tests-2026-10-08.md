# Trigger Tests, First Pass (October 8, 2026)

*A trigger test asks: when someone types a request, does Claude load the right skill, and leave the others alone? Every skill in this project lists 10 requests that should load it and 10 that shouldn't (in its `evals/evals.json`). Until today none of those lists had been run. This is the first run, in Claude Code. It is a first signal, not a verdict: read "Limits" before relying on it.*

## What was run

- **Tool:** `claude plugin eval` in Claude Code 2.1.294, the command that runs test cases against a plugin and scores them (docs: https://code.claude.com/docs/en/plugin-evals).
- **Setup:** the four skills (quantum-entanglement-lab 1.2.1, trig-check 1.0, qubit-math 1.0, book-chapter-splitter 1.0) packaged together as one test plugin with their long descriptions, made by `tools/make_trigger_evals.py` in the Claude Code starter kit. 80 requests, one case each.
- **Each run:** a fresh, isolated Claude Code session with only those four skills (no personal settings or memory), model claude-sonnet-5-5, tools Skill, Read, Glob and Grep (no shell), at most 4 turns. One run per request.
- **Scoring:** a should-load case passes when Claude calls the Skill tool for that skill at least once; a should-not case passes when it never does.
- **Cost and time:** the tool estimated $4.20 at list price for the 80 runs (on a subscription this counts against the plan's usage limits). 190 seconds, 4 runs at a time.

## Results

| Skill | Should load: loaded | Should not load: left off |
|---|---|---|
| book-chapter-splitter | 10 of 10 | 10 of 10 |
| quantum-entanglement-lab | 7 of 10 | 10 of 10 |
| trig-check | 6 of 10 | 10 of 10 |
| qubit-math | 2 of 10 | 10 of 10 |

No request loaded a skill it shouldn't have: 40 of 40 should-not cases passed.

## The 15 misses

| Skill | Request |
|---|---|
| qubit-math | Two qubits are in (\|00⟩ + \|11⟩)/√2. What's the reduced state of qubit 1, and its entropy? |
| qubit-math | Start in \|00⟩, apply H to qubit 0, then CNOT from 0 to 1. What do I get? |
| qubit-math | What are the X-basis probabilities for 0.6\|0⟩ + 0.8\|1⟩? |
| qubit-math | Compute ⟨Z⊗Z⟩ for (\|01⟩ + \|10⟩)/√2. |
| qubit-math | If I measure qubit 0 of a GHZ state and get 0, what's left? |
| qubit-math | What's the overlap between \|0⟩ and \|+⟩? |
| qubit-math | What does a CZ gate do to \|+⟩\|+⟩? |
| qubit-math | Find the purity of qubit 0's reduced state for (\|00⟩ + \|11⟩)/√2. |
| trig-check | What's the exact value of cos(15°)? |
| trig-check | Convert 135 degrees to radians. |
| trig-check | How many triangles have A = 40°, a = 5 and b = 7? |
| trig-check | Give me sin(5π/6) exactly. |
| quantum-entanglement-lab | What happens to \|φ+⟩ if Alice applies an X gate to her qubit? |
| quantum-entanglement-lab | Check my Bell-state decoder: does CNOT then H map the four Bell states to 00, 01, 10 and 11? |
| quantum-entanglement-lab | Why does \|S\| = 2√2 rule out local hidden variables? Show the calculation. |

**The pattern.** The requests that loaded a skill ask to check, verify, run, solve or show something, or involve a file. The misses are mostly short questions with textbook answers. Three misses were re-run with their transcripts kept (qubit-math 1 and 5, trig-check 2): each time the model answered in one turn, correctly, without calling any tool.

## Limits

- **One run per request.** Any single result could flip on a rerun. The next step is three runs per request (`--runs 3`).
- **No shell in the test sessions.** A loaded skill couldn't have run its script. Whether that changed the model's choice to load a skill isn't known.
- **Claude Code only, long descriptions only.** The Claude app uses the short descriptions and may choose differently. Neither the short descriptions nor the Claude app has been tested.
- **One model:** claude-sonnet-5-5, Claude Code's default in this session.

## What to decide

The skills say every number should come from the script. For a quick question that the model answers correctly anyway, loading the skill costs time and buys a checked number. So the first question is a choice, not a fix:

1. **Should qubit-math and trig-check load for quick textbook questions?** If yes, their descriptions need to name those cases in the words people use ("exact value of", "convert", "what do I get"), and say why (numbers come from the script). If no, the trigger lists should move those requests to a "may answer directly" group, so the tests measure what's wanted.
2. **Then re-test**, on these requests and on new phrasings, so a fix isn't fitted to these ten.

## How to re-run

From the Claude Code starter kit folder:

```bash
python tools/make_trigger_evals.py                      # rebuild the test plugin from the skills
claude plugin eval trigger-tests --ablation none --runs 3 --tag qubit-math --no-publish
python tools/make_trigger_evals.py --app-descriptions   # same requests, short descriptions
```

`--ablation none` skips the without-skill comparison, which a trigger test doesn't need. `--tag` picks one skill's cases. `--no-publish` keeps the report on your computer. Start small: each run is a real model call on your account.

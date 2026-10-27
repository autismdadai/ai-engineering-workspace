# Multi-Lens Review Method

*Extracted October 2, 2026 from the Planetary Council package (plugin v1.3.1). Character personas removed; the review method kept. Evidence class: project method, AI-assisted, not benchmarked.*

## What it is

A way to run a hard question through several independent viewpoints, check the key claims separately, and combine the results without hiding disagreement. One AI can play every role in a single chat, but the review is only truly independent when each viewpoint and the checker run as separate agents with their own context.

**Use it for** contested, high-stakes or many-sided questions: policy, strategy, big build decisions, research questions where sources conflict.
**Don't use it for** simple lookups, single-domain questions or pure creative work.

**Cost.** Each separate agent is a full run. Start with two or three lenses plus the verifier, and add a lens only when its stage is genuinely in play. This matches the skills paper's rule: one agent first; extra agents for parallel, separable work or independent checking.

## The four stages

| Stage | Question | Lenses |
|---|---|---|
| 1. Evidence | What does verified evidence actually say? What is missing or hidden? | Evidence hunter, precision checker |
| 2. Stakes and power | Who decides? What are the legal and institutional stakes? What has outlived its use? | Power and incentives, rules and time, risk and endings |
| 3. Synthesis and people | What is the strongest version of every side? What synthesis holds up? What does it mean for real people? | Synthesizer, communicator |
| 4. Build | Can it actually be built? What is the blueprint, the code, the phased plan? | Feasibility, architecture and code |
| Any stage | Are the key claims true? | Verifier |

## The lenses

| Lens | Job | Typical instruction |
|---|---|---|
| Evidence hunter | Primary sources, contradictory sources, open-source investigation | "Find the strongest primary sources for and against this claim." |
| Precision checker | Measurement, numbers, debunking | "Require quantitative evidence for each claim, or mark it unsupported." |
| Synthesizer | Steel-man every side, mediate, produce an actionable synthesis | "Steel-man the strongest opposing view before synthesizing." |
| Feasibility | Engineering reality, build plans, failure points | "Rate feasibility Green/Amber/Red and give a phased build plan." |
| Power and incentives | Who controls decisions, money, data and the story | "Map who decides, who pays, who profits and who can block." |
| Rules and time | Law, governance, constraints across time horizons | "List the legal, institutional and time constraints." |
| Architecture and code | System design and working code | "Design the architecture and supply code that runs." |
| Communicator | The stories people tell and what would make a recommendation land | "Name the dominant narratives and what the audience needs to understand." |
| Risk and endings | Hidden failure modes; what should be retired | "Identify hidden failure modes and what has outlived its usefulness." |
| Verifier | Independent, claim-by-claim checking | "Verify these claims independently and grade each one." |

Templates for these lenses (steel-man, power map, time horizons, feasibility rubric, end-of-life review, communication layer, evidence grades) are in claude/research-verification-toolkit.md.

## Procedure

0. **Care check first.** If the person seems to be in distress, set the review aside, answer warmly in plain words, and point them to real help.
1. **Classify** the question into one or more stages.
2. **Pick** the fewest lenses that cover those stages.
3. **Run each lens independently.** With separate agents, launch them in parallel. Give each the full question and everything the user supplied, never another lens's answer, and ask for its findings with evidence grades.
4. **Verify blind.** Pull out the load-bearing or contested claims. Send only those claims, stated neutrally and without anyone's reasoning, to the verifier in its own context.
5. **One conflict round.** If lenses clash on something that matters, give each side the other's strongest case and ask once more.
6. **Synthesize** using the rules below.
7. **Recommend (optional).** A judgment, not an average of the lenses. On legal, medical, financial or safety topics it is information, not professional advice, and it names the professional who should decide.
8. **Log** what ran.

## Synthesis rules

- Steel-man every material conflict before reconciling it. No caricatures.
- Every claim in the brief carries an evidence grade. A claim whose source nobody opened is UNVERIFIED.
- Name the deepest remaining disagreements instead of papering over them.
- Never drop a high-confidence dissenting finding because it complicates the story.
- Keep the remaining uncertainty visible.
- Any lens can call a **reframe**: "we're answering the wrong question." Resolve it before the recommendation.

## Honesty rules

- Call a check independent only when the verifier ran in its own context. If one AI played every role in one chat, say so in the log.
- Never claim to remember past sessions the host didn't provide.
- Cite only sources actually opened; everything else is UNVERIFIED.

## Output skeleton

```
REVIEW BRIEF
[the problem restated in one precise paragraph]

STAGES AND LENSES
[which stages and lenses contributed]

KEY FINDINGS (with evidence grades)
- Finding … [STATUS | Confidence X/10 | Source class]

CONFLICTS AND STEEL-MANS
[the strongest version of each side, and what is still disputed]

SYNTHESIS
[an integrated view that keeps dissent where it matters]

RECOMMENDATION (optional)
[a clear next action]

SENSITIVE-MATERIAL POINTERS (if any)
See APPENDIX-YYYYMMDD-NN

LOG
[lenses run · verifier: own context or same chat · tools used: web / code / none]

AI-generated analysis — information, not professional advice.
```

## Notes from the extraction

- The package uses multiple agents the way the evidence supports: in parallel only where the work separates, plus a verifier that never sees anyone's reasoning.
- Viewpoints stay distinct through their jobs and questions. Character voices help a reader tell them apart, but they don't make anything more accurate.

# Research and Verification Toolkit

*Extracted October 2, 2026 from the Planetary Council package (plugin v1.3.1). Character personas removed. Evidence class: project method, AI-assisted, not benchmarked. Use it with claude/portable-research-prompt.md.*

## 1. Evidence grades

Every material claim carries a grade: `[Status | Confidence X/10 | Source class]`

**Status**
- **SUPPORTED:** a primary source, or several independent strong sources, confirm it directly.
- **PARTIALLY_SUPPORTED:** evidence exists but is incomplete, indirect, or narrower than the claim.
- **CONTRADICTED:** strong evidence conflicts with it.
- **UNVERIFIED:** not enough primary evidence after a reasonable search, or no source was actually opened.

**Confidence 1–10**
- 9–10: several independent primary sources that agree
- 7–8: strong primary or excellent secondary support
- 5–6: plausible, with notable gaps
- 3–4: weak or circumstantial
- 1–2: speculative or contradicted

**Source class**
- **Primary:** original documents, raw data, official records, peer-reviewed primary studies, direct measurement
- **Secondary:** careful analysis, meta-analyses, investigative work with transparent methods
- **Tertiary:** news summaries, opinion, commentary
- **Internal:** model-generated reasoning or simulations

**How this fits the research prompt's tags.** SOURCE, MEMORY, INFERENCE and UNKNOWN (in claude/portable-research-prompt.md) say where a claim came from. The status says what checking found. Use both: a MEMORY claim stays UNVERIFIED until a source is opened.

**Caution.** The confidence number is the model's own rating, not a measured probability. Use it to decide what to check first, never as a statistic.

## 2. Claim-by-claim verification

1. Split the text into the smallest true-or-false statements, labeled C1, C2, and so on.
2. Classify each one: FACT (checkable), INFERENCE (reasoned from facts), OPINION (a value judgment) or UNCLEAR. Only FACT and INFERENCE claims get verified.
3. For each, state what would count as primary evidence, then find it. Record the title, identifier and date, plus the exact data point or a short quote.
4. Assign status, confidence and source class.
5. Optional summary score: accuracy ≈ (SUPPORTED + 0.5 × PARTIALLY_SUPPORTED) ÷ (FACT + INFERENCE claims). Every claim counts equally in this score, so report the load-bearing claims separately.
6. Add reproducibility notes: how someone else can re-check the key findings.
7. Check the claims themselves, not the conclusions of whoever made them.

## 3. Research order

1. Primary sources first.
2. Multi-hop: follow citations and footnotes back to the original instead of stopping at a summary.
3. Adversarial search: look on purpose for sources that challenge the dominant view.
4. Preprints and working papers (arXiv, bioRxiv, SSRN) when no peer-reviewed version exists, labeled as preprints.
5. Non-English primary material when the topic isn't English-speaking.
6. Negative evidence: log what was searched for and not found.

When sources conflict, show the conflict; don't average it away. For documents, check provenance, metadata and corroboration from the same period. For records requests and archives, search by agency, topic and year range, and use official reading rooms and archive.org.

## 4. Analysis templates

### Steel-man and blind spots (before any critique)
For each major opposing position:
1. Restate it in its strongest, most charitable form.
2. Name the value or evidence that makes it compelling to the people who hold it.
3. Only then critique it.

Blind-spot questions:
- What can this position not see about itself?
- Which feedback loops does it ignore?
- Which second- and third-order effects does it discount?
- Whose experience is invisible in this frame?
- What would have to be true for it to be wrong?

### Power and incentive map
Map these before judging any solution:
1. **Decisions:** who can decide, and who can veto?
2. **Money:** who funds it, who profits, who can cut the flow?
3. **Information:** who has the data advantage?
4. **Enforcement:** who can impose costs by force or sanction?
5. **Narrative:** who controls the dominant story and its legitimacy?

Then: stated goals vs actual goals; second- and third-order consequences; whose perspective the dominant frame leaves out.

### Time-horizon check
Look at each major recommendation at three horizons. The package uses 5, 50 and 500 years; scale them to the decision (for a project: a month, a year, five years).
- **Near:** what looks successful or harmless now?
- **Middle:** what institutional and power effects emerge?
- **Far:** what path does this make easier or harder?

Fairness tests: fair process, fair outcome, and fair to the people who come later.
**Load-bearing rule:** never remove a load-bearing rule, institution or norm without designing its replacement first.

### Feasibility rubric
- **GREEN:** possible, resourced, realistic on time, resilient to known failures. Proceed.
- **AMBER:** possible, but with significant risks, missing resources or unclear failure modes. Redesign or stage it.
- **RED:** not buildable under current constraints, or failure would be catastrophic and unmitigated. Say so and give the closest buildable alternative.

Failure categories (cover at least the top three that apply): structural or physical; resources and supply; schedule; people and organization; security and adversaries; second-order system effects.

### End-of-life review
- What has outlived its usefulness here?
- What does keeping it cost?
- What happens if it isn't retired deliberately?
- What value is buried in it that should be kept?
- What replaces it? (See the load-bearing rule.)

This applies to systems, habits, institutions and ideas, never to a person.

### Communication layer
1. **Official story:** what is being said.
2. **Underlying story:** the assumptions or cultural story actually in play.
3. **Unspoken:** what the system doesn't say about itself.
4. **What has to land:** what the audience must care about for a recommendation to become real.
5. **Translation:** the synthesis as something a real person can understand and act on.

### Code safety checklist (before presenting code)
1. The language choice is justified.
2. No secrets: no keys, passwords, tokens or private data.
3. No hidden network calls; any call is explicit, documented and optional.
4. Output is bounded by default.
5. It runs, or it is clearly labeled as a sketch with next steps.
6. Every dependency is listed.
7. Failure modes are noted: what breaks first, and how it fails safely.

Show it working; don't just describe it.

### Sensitive-material appendix
Keep contested or distressing material out of the main text. Put it in a clearly marked appendix at the end, and leave only a pointer in the main text (`See APPENDIX-YYYYMMDD-NN`). Each entry gets a risk class (Low, Medium or High), a confidence rating, a one-paragraph non-sensitive summary, and sources. Entries are append-only: never quietly edit or delete an old one.

Use it for highly contested findings that carry reputational or safety risk, and for distressing detail the main text can summarize.

Two rules here are stricter than the source package:
- Leave unverified allegations about private individuals out entirely.
- For public figures and organizations, include only sourced allegations, labeled as allegations.

Nothing goes in the appendix that would be refused in the main text. Refused material is declined, not hidden.

## 5. Professional-advice and care rules

**Information, not professional advice.** On legal, medical, financial and safety-critical topics, give information and analysis, and say when a licensed professional should make the call or sign off.
- **Law:** name the jurisdiction and the date the information applies to. Current law needs a source actually opened.
- **Health:** assess the evidence. Diagnosis and treatment decisions go to a clinician.
- **Money:** explain the options and trade-offs. No personal investment, tax or legal-structure recommendations.

**Care, not therapy.** Never diagnose. If someone seems to be in distress, step out of the protocol, respond warmly in plain words, and point them to real help (in the US, call or text 988) or a licensed professional.

**Sources.** Cite only what was actually opened or supplied. Never invent a document number, DOI, URL, statute, case, statistic or quotation.

**Disclosure.** Finished analyses end with: *AI-generated analysis — information, not professional advice.*

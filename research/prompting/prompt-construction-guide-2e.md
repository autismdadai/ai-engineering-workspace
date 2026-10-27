# The Prompt Construction Guide

## Step-by-Step Build Instructions, Orchestration Patterns, and 150 Worked Examples

**Edition:** Second, September 2026, with a post-edition note of October 20, 2026 (end of the guide) · **Companion to** *The Taxonomy of Prompt Engineering: A Seven-Axis Reference Manual* (Third Edition, September 2026) · **Document class:** Independent technical reference, not peer reviewed

**What changed in this edition.** A new Part 8 covers decoding controls (§34) and independent parallel review (§35), with five worked examples each, and a task index below points to the right section for common jobs. Figures now match the manual’s third edition: Chain-of-Draft’s per-task results are stated for each model (§7), the usage data in Part 7 is quoted with its exact scope, and several recommendations that had been worded as measured findings are now worded as the advice they are. Cross-references point to the manual’s new chapter numbers.

## How to use this guide

The manual explains *what* each technique is and what the evidence says. This guide explains *how to build one*, and shows five worked examples of each.

Every entry follows the same shape:

- **What it does and when to reach for it** — one paragraph.
- **Build steps** — a numbered procedure you can follow start to finish.
- **Combines with** — which other techniques stack on this one, and which conflict.
- **Five worked examples** — each with a real scenario, the complete prompt or call flow, the build steps it demonstrates, and what to check in the output.

**Three rules that apply to every example in this guide.**

1. **Placeholders are yours to fill.** Anything in `{curly_braces}` is your data. Everything else is meant to be sent as written.
2. **The check line is not optional.** Each example ends with what to verify. A prompt you cannot check is a prompt you cannot trust. The manual’s Chapter 15 is the long version of why.
3. **These examples have not been benchmarked.** They illustrate technique shape. Whether any of them beats a simpler prompt on *your* task is an empirical question — run the evaluation in Chapter 21 of the manual.

**Start at the bottom of the stack.** Before reaching for anything in Part 2 or 3, try a single zero-shot call on a capable model, grounded if the answer depends on facts. If it meets your bar, stop there. Add a layer only when a measurement says the simpler version fails.

## Task index

Find the job in the first column, start with the technique under “Start with,” and move to “Then consider” only when a measurement shows the first falling short. Section 30 maps the same techniques to published usage data.

| **If you need to…** | **Start with** | **Then consider** |
|---|---|---|
| Answer from documents you have | Context anchoring (§4) | Retrieval (§15); Chain-of-Verification (§19) |
| Answer from a large or changing collection | Retrieval-augmented generation (§15) | Chain-of-Verification (§19); factuality check (Example 20.4) |
| Extract fields for another system | Schema-constrained generation (§18) | Reflexion against the validator (§17); settings in Example 34.1 |
| Classify or triage | Few-shot (§2) with a schema enum (§18) | Routing (§23); self-consistency on costly classes (§10) |
| Edit text someone supplied | Context anchoring (§4) with constraint framing (§5) | Evaluator-optimizer (§26) |
| Draft a document or message | System rules (§3) and a template (§6) | Prompt chaining (§22); Chain-of-Verification on facts (§19) |
| Compute a number | Program-of-Thoughts (§13) | Self-consistency over programs (§10) |
| Solve a multi-step problem on a non-reasoning model | Chain-of-Thought (§9) | Least-to-Most (§11); Tree-of-Thoughts (§12) |
| Cut the cost of reasoning | Chain-of-Draft, few-shot only (§7) | Routing by difficulty (§23; Example 34.5) |
| Reduce run-to-run variation | Decoding controls (§34) | Self-consistency (§10) |
| Use tools or take actions | ReAct (§16) | Reflexion (§17); orchestrator-workers (§25) |
| Check a conclusion before acting on it | Disconfirmation pass (§21) | Independent parallel review (§35); debate (§27) |
| Score outputs at volume | LLM-as-a-judge (§20) | Independent parallel review (§35) |
| Review a document or prompt with several models | Independent parallel review (§35) | Independent-model disconfirmation (Example 21.5) |
| Tune a prompt that runs at scale | Automated optimization (§28), after the decision harness (Example 28.5) | — |

# Part 1 — Conditioning Techniques

## 1. Zero-Shot Prompting

**What it does and when to reach for it.** A zero-shot prompt states the task directly with no examples, relying on instruction tuning to map the request to a completion. Reach for it first, always: it is the cheapest option, the fastest, and the baseline every other technique has to beat. Before adding few-shot examples or chain-of-thought, check whether the real problem is an underspecified instruction. The skill in zero-shot prompting is not phrasing — it is anticipating every way the input can be weird and saying what to do about it.

**Build steps.**

1. **Name the operation with a verb.** “Classify,” “extract,” “rewrite,” “rank.” Not “help me with.”
2. **Enumerate the output space.** If the answer is a category, list the categories. If it is a format, show the format.
3. **Handle the residue.** Say what to do with ambiguity, with input that fits nothing, and with input that fits several answers. This is the step people skip, and it is where zero-shot prompts fail.
4. **Add constraints.** Length, vocabulary, what must be preserved exactly.
5. **Say what not to return.** “Return only X” prevents the preamble that breaks your parser.
6. **Test the edges first.** Empty input, contradictory input, input in another language, input that is an instruction.

**Combines with.** Context anchoring (§4) turns zero-shot into grounded QA. Schema-constrained generation (§18) turns the format instruction into a guarantee. Skip few-shot until zero-shot has measurably failed.

### Example 1.1 — Support-ticket triage (customer operations)

*Scenario:* Routing inbound tickets to the right queue without a human first-pass.

```
Classify the support ticket into exactly one category:
BILLING, BUG, FEATURE_REQUEST, ACCOUNT_ACCESS, or OTHER.

Return only the category name in capitals. No explanation.

- If the ticket fits more than one category, choose the one
  the customer most wants resolved right now.
- If it fits none of the four, return OTHER. Do not stretch
  a category to fit.
- If the ticket is empty or unintelligible, return OTHER.

Ticket: "{ticket}"
```

*Shows:* steps 1–3, 5. The double-fit rule matters for a ticket like “I was charged twice for March and the refund button on the billing page throws a 500 error,” which is genuinely both BILLING and BUG.

*Check:* run 50 real tickets and inspect every OTHER. A high OTHER rate may mean your category list is missing a category; read those tickets before blaming the model.

### Example 1.2 — Meeting notes to action items (project management)

*Scenario:* Turning a transcript into a list someone can act on.

```
Extract every action item from the notes below.

Return one per line in this exact form:
OWNER | ACTION | DUE

- OWNER is the person named as responsible. If no one is
  named, write UNASSIGNED.
- DUE is a date in YYYY-MM-DD, or NONE if no date was given.
  Do not infer a date from phrases like "soon" or "next week"
  unless the notes state today's date.
- Include only commitments someone actually made. Do not
  include topics discussed, options considered, or questions
  asked.
- If there are no action items, return exactly: NO ACTION ITEMS

Notes: {paste_notes}
```

*Shows:* steps 2, 3, 5 — three separate escape hatches (UNASSIGNED, NONE, NO ACTION ITEMS) so the model never has to invent.

*Check:* read the transcript yourself for one meeting and diff. Watch for invented owners — that is the characteristic failure.

### Example 1.3 — Plain-language rewrite (education)

*Scenario:* Making a dense paragraph readable for a parent or student.

```
Rewrite the paragraph below so a US eighth-grade reader can
follow it.

- Keep every number, name, date, and quoted phrase exactly
  as written.
- Replace jargon with plain words. If a technical term has no
  plain equivalent, keep it and define it in one clause on
  first use.
- Use sentences of 20 words or fewer.
- Do not add information, examples, or encouragement that is
  not in the original.
- Return only the rewritten paragraph.

Paragraph: {paste_paragraph}
```

*Shows:* steps 1, 4, 5. “Do not add encouragement” is a real constraint — models pad rewrites with reassurance.

*Check:* diff the numbers and names against the original. Any change is a failure, however small.

### Example 1.4 — Shipment field extraction (logistics)

*Scenario:* Pulling structured data out of carrier emails.

```
Extract shipment details from the email below.

Return a single JSON object with exactly these keys:
  tracking_number (string or null)
  carrier (string or null)
  promised_date (YYYY-MM-DD or null)
  destination_city (string or null)

- Use null for any field the email does not state.
- Do not infer the carrier from the tracking number format.
- Do not convert a relative date ("arrives Tuesday") into a
  calendar date. Use null.
- Return only the JSON object, with no code fence.

Email: {paste_email}
```

*Shows:* steps 2–5. The two “do not infer” rules block the two inferences this task invites.

*Check:* parse every response. A parse failure rate above ~1% means you should move to schema-constrained generation (§18).

### Example 1.5 — Ranking with a stated tiebreak (hiring operations)

*Scenario:* Ordering a shortlist against fixed criteria.

```
Rank the candidates below against the role requirements.

Return a numbered list, best first. After each name, give one
sentence naming the single requirement that placed them there.

- Rank only on the requirements listed. Ignore school, company
  prestige, employment gaps, and years of experience unless a
  requirement names them.
- If two candidates are equal on the requirements, rank the one
  with more directly relevant recent work higher, and say so.
- If a candidate is missing a requirement marked REQUIRED,
  place them last regardless of other strengths.

Requirements: {paste_requirements}
Candidates: {paste_candidates}
```

*Shows:* steps 1, 3, 4. Step 3 is doing heavy lifting: without the tiebreak rule the ordering shifts run to run.

*Check:* run it three times on the same input. If the top three change, the requirements may be underspecified (or sampling noise may be at work); tighten them and rerun before blaming the model.

## 2. Few-Shot Prompting

**What it does and when to reach for it.** Few-shot prompting puts labeled examples in the context so the model copies their shape. Min et al. (arXiv 2202.12837) showed that randomly replacing the labels in the examples barely hurts performance across 12 models — which tells you what few-shot actually buys: format, label space, and input distribution, not an answer key. Reach for it when zero-shot produces the right content in the wrong shape, or when your label definitions are easier to demonstrate than to describe. On strong recent models, expect a format gain and measure before assuming a reasoning gain: on mathematical reasoning with Qwen2.5-series models, CoT exemplars did not beat zero-shot CoT (Cheng et al., arXiv 2506.14641).

**Build steps.**

1. **Start with 3 examples.** Add more only if measurement says so. Token cost is linear; accuracy gain is not.
2. **Cover the label space.** Every class you want predicted must appear. A missing class is a class the model will avoid.
3. **Include one boundary case.** The example that teaches where the line is does more work than three easy ones.
4. **Make formatting byte-identical** across examples and the final query — same delimiters, same spacing, same capitalization.
5. **Watch the order.** Do not let one class occupy the last slot every time; Lu et al. (arXiv 2104.08786) found ordering can swing accuracy from near-best to near-random.
6. **Leave the final answer slot open** so the model completes rather than restarts.
7. **Compare against zero-shot on a held-out set** before you keep it.

**Combines with.** Chain-of-Draft (§7) *requires* few-shot — in the paper’s zero-shot GSM8K test it fell far below Chain-of-Thought. Chain-of-Thought (§9) becomes few-shot CoT when the examples include reasoning. Conflicts with nothing, but adds latency to every call forever.

### Example 2.1 — Sentiment with a boundary case (product analytics)

*Scenario:* Labeling reviews where “mixed” is a real and common answer.

```
Label each review as POSITIVE, NEGATIVE, or MIXED.

Review: "Battery lasts two days. Screen scratches instantly."
Label: MIXED

Review: "Arrived broken and support never replied."
Label: NEGATIVE

Review: "Exactly what I needed, and cheaper than the store."
Label: POSITIVE

Review: "It works."
Label: POSITIVE

Review: "{new_review}"
Label:
```

*Shows:* steps 2, 3, 6. “It works.” is the boundary case — terse, unenthusiastic, but not negative.

*Check:* audit the MIXED predictions. If MIXED is rare, the model is collapsing it into the other two and you need a second MIXED example.

### Example 2.2 — Natural language to SQL (software)

*Scenario:* Letting analysts query without writing SQL.

```
Convert each question to a SQL query against this schema:
orders(id, customer_id, total_cents, placed_at)
customers(id, name, country)

Q: How many orders were placed in 2025?
SQL: SELECT COUNT(*) FROM orders WHERE placed_at >= '2025-01-01' AND placed_at < '2026-01-01';

Q: Total revenue by country.
SQL: SELECT c.country, SUM(o.total_cents) FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.country;

Q: Customers with no orders.
SQL: SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL;

Q: {new_question}
SQL:
```

*Shows:* steps 1, 3, 4. The three examples each teach a different join or filter pattern; the LEFT JOIN example is the boundary case.

*Check:* run `EXPLAIN` on every generated query before execution, and never run generated SQL with write privileges.

### Example 2.3 — Medication extraction (health information)

*Scenario:* Structuring free-text clinical notes. Absence must be representable.

```
Extract medication mentions into JSON. Set "action" to what
the text says to do with the drug: "start", "continue",
"hold", or "stop". Use null when a value is not stated. Do
not add medications not in the text.

Text: "Start lisinopril 10 mg once daily."
JSON: {"drug":"lisinopril","action":"start","dose":"10 mg","frequency":"once daily"}

Text: "Continue current metformin."
JSON: {"drug":"metformin","action":"continue","dose":null,"frequency":null}

Text: "Hold warfarin until INR is back in range."
JSON: {"drug":"warfarin","action":"hold","dose":null,"frequency":null}

Text: "{new_text}"
JSON:
```

*Shows:* steps 2, 3, 4. Two of the three examples demonstrate nulls, because under-specified mentions are the common case. The action field keeps “hold” from looking like an active drug.

*Check:* the failures to watch for are a plausible invented dose and a wrong action. Spot-check every record where dose is non-null against the source text, and check every action against the instruction word in the note. A held or stopped drug recorded as active is the error to catch first.

### Example 2.4 — Style transfer for a house voice (marketing)

*Scenario:* Matching an established brand voice that is easier to show than describe.

```
Rewrite each sentence in our house voice.

Before: "Our solution leverages best-in-class infrastructure."
After: "We run on hardware we'd bet the company on."

Before: "Users may experience intermittent latency."
After: "Sometimes it's slow. We're working on it."

Before: "We are pleased to announce a new partnership."
After: "We're working with Acme now. Here's what changes for you."

Before: "{new_sentence}"
After:
```

*Shows:* steps 1, 4, 6. Voice is the archetypal case where demonstration beats description.

*Check:* have the person whose voice it is read ten outputs. This is not a metric task; it is a taste task, and only they can score it.

### Example 2.5 — Intent classification with a deliberate null class (conversational product)

*Scenario:* A router that must be honest about not knowing.

```
Classify the user message into one intent.

Message: "where's my order"
Intent: ORDER_STATUS

Message: "cancel it"
Intent: CANCEL_ORDER

Message: "this is ridiculous"
Intent: UNKNOWN

Message: "do you ship to canada"
Intent: SHIPPING_POLICY

Message: "i need to change the address on 4471"
Intent: UPDATE_ORDER

Message: "{new_message}"
Intent:
```

*Shows:* steps 2, 3, 5. UNKNOWN sits in the middle, not last, so recency bias does not inflate it.

*Check:* track the UNKNOWN rate over time. A sudden drop usually means a new intent is being misrouted into an existing class.

## 3. System Rules and Personas

**What it does and when to reach for it.** The system message holds the rules that should apply to every turn — format, scope, tone, safety framing. Reach for it when behavior must persist across a conversation rather than being restated. Two cautions govern its use. Zheng et al. (Findings of EMNLP 2024; arXiv 2311.10054) tested 162 personas across four open-source model families on 2,410 multiple-choice MMLU questions and found that adding a persona did not improve accuracy against no persona at all, and that the effect of any given persona “can be largely random”; use roles for voice, not correctness. And OWASP is explicit that the system prompt “should not be considered a secret, nor should it be used as a security control.”

**Build steps.**

1. **Put durable rules here; put the task in the user turn.** If it changes per request, it does not belong in the system message.
2. **Write rules as behaviors, not identity.** “Return only corrected text” beats “You are a meticulous editor.”
3. **Give exact fallback strings** for the cases you want to detect downstream.
4. **Keep it short.** Long system prompts dilute; the rule you care about most should not be rule fourteen.
5. **Restate the format requirement in the user turn** for long sessions.
6. **Put no secrets, credentials, or authorization logic here.** Ever.

**Combines with.** Everything. Pairs especially well with schema-constrained generation (§18), which enforces what the system prompt merely requests.

### Example 3.1 — Copy editor with preservation rules (publishing)

```
SYSTEM:
Copy-edit the text in each user turn for a technical blog.

- Correct grammar, spelling, and punctuation only.
- Never change technical terms, code, numbers, or quoted text.
- Preserve the author's voice, including sentence fragments
  used for emphasis and deliberate one-sentence paragraphs.
- If a sentence is ambiguous, leave it and append a line at
  the end: "QUERY: <the ambiguity>".
- Return only the corrected text plus any QUERY lines.
```

*Shows:* steps 2, 3, 4. The QUERY channel gives the model somewhere to put uncertainty other than a silent rewrite.

*Check:* diff every output against the input. Any changed number, term, or quote is a defect.

### Example 3.2 — Hard output contract (software)

```
SYSTEM:
Respond with a single valid JSON object matching this schema
and nothing else — no prose, no code fence:

{"intent": "refund" | "exchange" | "status" | "other",
 "order_id": string | null,
 "urgency": "low" | "normal" | "high"}

- If the message contains no order ID, use null. Do not
  construct one from other numbers in the message.
- Choose "other" rather than guessing among the first three.
- Base urgency on what the customer states, not on tone.
```

*Shows:* steps 1–3. The urgency rule is the interesting one: without it, angry punctuation becomes “high.”

*Check:* parse rate, plus a sample audit of urgency against the text. Then replace this prompt with a real schema (§18).

### Example 3.3 — Scope boundary for a regulated assistant (support)

```
SYSTEM:
Answer questions about our published shipping policy only.

- Answer from the policy text supplied in each user turn.
- If the policy does not cover the question, reply exactly:
  "That isn't covered in the shipping policy — I'll route you
  to a human."
- Do not answer billing, returns, warranty, or legal
  questions, even if the user insists or rephrases.
- Do not speculate about what the policy probably means.
```

*Shows:* steps 1–4. The exact fallback string is what lets your code detect a handoff.

*Check:* run adversarial rephrasings of out-of-scope questions. Count how many get an answer instead of the fallback — and remember that this boundary is a quality control, not a security control.

### Example 3.4 — Tone without an identity claim (education outreach)

```
SYSTEM:
Write for parents of school-age children with no background
in education law.

- Use everyday words. When a legal or clinical term is
  unavoidable, give it and then a short plain definition.
- Never tell the reader how to feel about their situation.
- State what the law requires only when the user turn quotes
  the provision, and name that provision. Otherwise say you
  cannot confirm what the law requires.
- Keep paragraphs to three sentences or fewer.
```

*Shows:* step 2 — audience framing without “you are an expert,” which the evidence says buys tone and not accuracy.

*Check:* the third rule is the one to audit. Any “the law requires” that does not rest on a provision quoted in the user turn is a defect regardless of whether it is correct.

### Example 3.5 — Analysis assistant with an anti-sycophancy rule (research)

```
SYSTEM:
Support data analysis. Your job is accuracy, not agreement.

- When the user states a conclusion, evaluate it. Do not
  restate it back as agreement.
- If the data does not support a claim the user has made,
  say so plainly in the first sentence.
- Distinguish what the data shows from what it suggests.
  Label the second kind explicitly.
- When a result could be explained by a confound, name the
  confound even if not asked.
```

*Shows:* steps 2, 4. This targets the sycophancy finding (Sharma et al., arXiv 2310.13548) directly.

*Check:* deliberately assert something false to the assistant and see whether the first sentence corrects you. If it opens with agreement and corrects in paragraph three, the rule is not working.

## 4. Context Anchoring

**What it does and when to reach for it.** Context anchoring supplies the source material the answer must come from, and forbids answering from anything else. Reach for it whenever the answer exists in a document you have — policies, contracts, manuals, transcripts. For factual work it is the first technique to reach for, because it turns a recall problem into a reading problem: the model answers from text in front of it instead of from what it absorbed in training.

**Build steps.**

1. **Delimit the source** with tags prose will not contain: `<policy>`, `<contract>`, `<sources>`.
2. **Instruct grounding explicitly**: answer only from the delimited text.
3. **Provide a refusal token** — an exact string for “not in the source.” Without one, the model fills the gap from memory.
4. **Require evidence**: a quoted span, a line number, or a source index for each claim.
5. **Put long documents first and the question last,** and keep critical facts out of the middle of a long context (Lost in the Middle, arXiv 2307.03172; manual Sections 4.1 and 7.4).
6. **Say what to do when sources conflict** — usually: present both, attribute, do not resolve.

**Combines with.** RAG (§15) is context anchoring with automated retrieval in front. Schema-constrained generation (§18) can force the citation field to exist. Chain-of-Verification (§19) checks the result.

### Example 4.1 — Policy question answering with a quoted source (HR)

```
Answer using only the text inside <policy> tags.

<policy>
{paste_policy_text}
</policy>

Question: {question}

- Quote the sentence you relied on, verbatim, under "Source:".
- If the policy does not answer the question, reply exactly
  "NOT IN POLICY" and nothing else.
- Do not use general knowledge about typical company policies.
- If two sections of the policy conflict, quote both and say
  they conflict. Do not pick one.
```

*Shows:* steps 1–4, 6.

*Check:* verify the quoted sentence appears verbatim in the policy. A near-quote is a fabrication, and it is the most common failure of this pattern.

### Example 4.2 — Contract clause extraction (legal operations)

```
<contract>
{paste_contract}
</contract>

Extract the termination provisions from the contract above.

For each provision give:
  - who may terminate
  - required notice period
  - the exact quoted sentence

List them in the order they appear in the contract. If the
contract contains no termination provision, reply "NONE FOUND".
Do not summarize what termination clauses usually contain.
```

*Shows:* steps 1–4. The last line blocks the model’s strongest prior — it knows what termination clauses usually say.

*Check:* string-match each quoted sentence against the contract text in code. Fail the response if any quote is absent.

### Example 4.3 — Grounded summary with a supported-claim rule (research)

```
<article>
{paste_article}
</article>

Summarize the article above in five bullets.

- Every bullet must be supported by a specific sentence in
  the article. Append that sentence's first six words in
  brackets after the bullet.
- Do not add background, context, or implications the article
  does not state.
- If the article is too short to yield five supported bullets,
  give fewer and say how many you gave.
```

*Shows:* steps 2–4. The six-word anchor is cheap to check automatically.

*Check:* grep each bracketed fragment against the source. Missing fragments mark unsupported bullets.

### Example 4.4 — Multi-document comparison (procurement)

```
<vendor_a>{paste_proposal_a}</vendor_a>
<vendor_b>{paste_proposal_b}</vendor_b>

Compare the two proposals on: price, delivery timeline,
support terms, and termination rights.

Return a table with one row per dimension and columns
VENDOR A | VENDOR B | DIFFERENCE.

- Fill a cell with "NOT STATED" when a proposal is silent.
  Do not infer a value from the other proposal or from
  industry norms.
- Under the table, list any dimension where NOT STATED appears,
  as questions to send back to that vendor.
```

*Shows:* steps 1, 3, 6. “NOT STATED” becomes an action item instead of a gap.

*Check:* the NOT STATED cells are the valuable output. Verify each one by searching the proposal yourself.

### Example 4.5 — Transcript question answering with speaker attribution (meetings)

```
<transcript>
{paste_transcript}
</transcript>

Question: {question}

Answer in this form:
  ANSWER: <your answer>
  SAID BY: <speaker name>
  QUOTE: "<their exact words>"

- Only use what was actually said. Do not infer agreement
  from silence.
- If several people said conflicting things, list each with
  their quote and do not decide who was right.
- If no one addressed the question, reply "NOT DISCUSSED".
```

*Shows:* steps 1–4, 6. “Do not infer agreement from silence” blocks the characteristic transcript hallucination.

*Check:* verify the speaker attribution, not just the quote. Correct quote with wrong speaker is a common and damaging error.

## 5. Constraint Framing (Negative Prompts Done Right)

**What it does and when to reach for it.** Constraint framing controls what must not appear in the output. It matters because the naive form — a growing list of “don’ts” — is unreliable. A prohibition is followed only probabilistically, long rule lists get partly dropped, and both major model vendors advise saying what to do instead of only what not to do (manual Section 7.5). The popular explanation, that naming a forbidden thing makes it more likely, is a hypothesis rather than a measured mechanism. Reach for it when an exclusion is genuinely hard (a compliance rule, a units requirement, a forbidden claim), and pair it with something checkable. When the constraint can be stated positively, state it positively instead.

**Build steps.**

1. **Try the positive form first.** “Write in third person” instead of “don’t use I.”
2. **Reserve negatives for exclusions with no positive phrasing.** “No imperial units anywhere” has no positive equivalent.
3. **Make each negative checkable** — add an output field, a token list, or a marker a script can scan.
4. **Keep the count low.** Every added rule is another chance for one to be dropped or to conflict with another; instruction-following falls as rule lists grow (manual Section 7.5).
5. **Give a legal alternative.** Say what the model should produce in place of the forbidden thing — the vendors’ own advice.
6. **Audit accumulated negatives** whenever you edit the prompt. They pile up and start conflicting.

**Combines with.** Schema-constrained generation (§18) converts a negative into a structural impossibility, which is strictly better. LLM-as-judge (§20) can check the soft ones.

### Example 5.1 — Positive reframing (marketing)

```
Write the product description in third person, present tense,
using only claims that appear in the spec sheet below.

Required: a 30-word summary, then three feature bullets.
Each bullet must name one specific spec value.

Spec sheet: {paste_specs}
```

*Shows:* steps 1, 5. Every rule here replaces a negative: not “don’t use first person,” not “don’t be vague,” not “don’t invent features.”

*Check:* each bullet must contain a value that appears in the spec sheet. Script it.

### Example 5.2 — Hard exclusion with a self-report (scientific writing)

```
Convert every measurement in the text below to SI units.

- Use only SI units in the output. Imperial units must not
  appear anywhere, including in parentheses.
- Keep the original precision. Do not add significant figures.
- Return the rewritten text, then a final line
  "UNITS USED:" listing every unit symbol you emitted.
Text: {paste_text}
```

*Shows:* steps 2, 3. The UNITS USED line turns an unverifiable prohibition into a checkable list.

*Check:* script the UNITS USED line against an allowed-symbol set. Also scan the body independently — a model can under-report its own line.

### Example 5.3 — Scope exclusion with a legal alternative (code review)

```
Review this diff for correctness bugs only.

- Report logic errors, off-by-one errors, null handling, and
  race conditions.
- Style, naming, and formatting are out of scope. If you have
  no correctness findings, reply "NO CORRECTNESS FINDINGS"
  rather than substituting style comments.
- For each finding give: the line, what goes wrong, and the
  concrete input that triggers it. A finding without a
  triggering input is speculation — leave it out.

Diff:
{paste_diff}
```

*Shows:* steps 2, 3, 5. “NO CORRECTNESS FINDINGS” is the legal alternative to inventing a finding.

*Check:* every finding must include a triggering input. Findings without one are the noise this prompt exists to suppress.

### Example 5.4 — Claim restriction in regulated copy (financial communications)

```
Draft the email announcing the new savings product.

Permitted claims: only the rate, term, and minimum balance in
the term sheet below, stated exactly as written there.

Forbidden, with no exceptions:
- Any comparison to competitor rates.
- Any statement about future rates.
- The words "guaranteed," "risk-free," or "best."

If the draft feels thin without a comparison, add a line
inviting the reader to compare, without making one.

End with a line "CLAIMS MADE:" listing each factual claim in
the draft.

Term sheet: {paste_term_sheet}
```

*Shows:* steps 2–5. The “if it feels thin” clause is the legal alternative; without it the model smuggles a comparison in.

*Check:* compare CLAIMS MADE against the term sheet line by line, and scan the body for the three forbidden words independently.

### Example 5.5 — Preventing scope creep in a rewrite (documentation)

```
Fix only the factual errors in the documentation below,
judging them only against the reference below.

- Change a sentence only if the reference contradicts it.
- Do not reorganize, retitle, shorten, or improve prose.
- Do not add sections, notes, or warnings.
- Return the full document with corrections applied, then a
  list "CHANGES:" with the original and corrected text of
  each edit.

If you believe something is unclear, or the reference does
not cover it, list it under "NOT CHANGED — UNCLEAR:" instead
of editing it.

Reference: {paste_reference}
Document: {paste_doc}
```

*Shows:* steps 2, 3, 5, 6. The CHANGES list makes the diff auditable; the UNCLEAR list absorbs the improvement urge.

*Check:* diff the returned document against the original. Every difference must appear in CHANGES, and each change must be one the reference supports. Undocumented edits are the failure mode.

# Part 2 — Representation Techniques

## 6. Structured Templates (CO-STAR, RTF, RISEN)

**What it does and when to reach for it.** A template gives you a slot for each thing the model needs, so you do not forget one. These are practitioner mnemonics, not algorithms — none has peer-reviewed validation, and their value is checklist completeness rather than any effect on inference. Reach for one when a team is writing prompts and consistency matters more than optimality, or when your prompts keep failing because of omission rather than phrasing. CO-STAR (Context, Objective, Style, Tone, Audience, Response) is credited by Sheila Teo to GovTech Singapore’s Data Science & AI team; her December 2023 competition write-up popularized it.

**Build steps.**

1. **Pick the template that matches the task shape.** CO-STAR for communication, RTF for quick transforms, RISEN for multi-step work with a defined end state.
2. **Fill every slot.** An empty slot means you have not decided; decide.
3. **Delete slots you genuinely do not need** rather than padding them with filler.
4. **Put the data last**, after the instructions, so the instruction is not buried.
5. **Retire the template once the prompt is stable** — keep the slots that earned their place.

**Combines with.** Any reasoning topology drops into the Response slot. Context anchoring (§4) goes in the Context slot.

### Example 6.1 — CO-STAR executive brief (business)

```
# CONTEXT
Q3 churn rose from 4.1% to 6.8% among accounts under 50 seats.
The underlying data is in the table below.

# OBJECTIVE
Recommend the single highest-leverage retention intervention
for Q4, and show the reasoning that leads to it.

# STYLE
Consulting memo. Recommendation first, then support.

# TONE
Direct and non-promotional. Name the risk in your own
recommendation.

# AUDIENCE
VP of Customer Success. Knows the product well, does not know
the data model.

# RESPONSE
Under 300 words: the recommendation, three supporting points,
one named risk, and one metric to watch. No preamble.

Table: {paste_table}
```

*Shows:* steps 1, 2, 4. Tone is doing real work — “name the risk in your own recommendation” counters the pitch-deck register.

*Check:* is there exactly one recommendation? Templates invite hedged multi-option answers, which is the failure to watch for.

### Example 6.2 — RTF for a fast transform (internal communications)

```
Role: Internal communications editor.
Task: Turn the engineering incident notes below into a status
update for non-engineers.
Format: Three short paragraphs — what happened, who was
affected, what happens next. No jargon. No blame. No
speculation about root cause beyond what the notes state.

Notes: {paste_notes}
```

*Shows:* steps 1, 3, 4 — three slots, no padding.

*Check:* the last constraint. Incident write-ups drift toward confident causal claims the notes do not support.

### Example 6.3 — RISEN for a multi-step deliverable (education)

```
Role: Curriculum designer for an undergraduate survey course.
Instruction: Draft a four-week unit on statistical inference
for students who have taken one algebra course.
Steps:
  1. List the four week-level learning objectives.
  2. For each week, give one core concept and one common
     misconception.
  3. Propose one assessment per week that tests the objective
     rather than recall.
End goal: An outline an instructor could teach from without
adding new material.
Narrowing: No calculus. No software-specific instructions.
Under 600 words total.
```

*Shows:* steps 1, 2. RISEN’s Steps slot is where a decomposition (§11) naturally lives.

*Check:* does each assessment actually test its stated objective? This is where these outlines usually break.

### Example 6.4 — CARE for a case write-up (consulting)

```
Context: A regional clinic network is consolidating three
scheduling systems into one. Staff resistance is the stated
risk. Details below.

Action: Identify the three decisions that must be made before
migration begins, and who owns each.

Result: For each decision, state what a good outcome looks
like and how you would know within 30 days that it went wrong.

Example: Format each decision like this —
  DECISION: <one sentence>
  OWNER: <role>
  GOOD OUTCOME: <one sentence>
  EARLY WARNING: <observable signal within 30 days>

Details: {paste_details}
```

*Shows:* steps 1, 2, 4. The Example slot is the template’s best feature — it is a one-shot demonstration inside a checklist.

*Check:* is every EARLY WARNING actually observable within 30 days? Vague signals like “staff morale” fail this test.

### Example 6.5 — A stripped template after stabilization (support operations)

```
Audience: A customer who has already been told no once.
Objective: Explain why the policy applies to their case,
and give them the one path that is still open.
Response: Under 120 words. No apology loop — apologize once
or not at all. End with the concrete next step.

Their message: {paste_message}
Policy section that applies: {paste_section}
```

*Shows:* step 5. Suppose three CO-STAR slots survive iteration: Style and Tone fold into Response, and Context folds into the data.

*Check:* word count and whether the next step is genuinely actionable. Retired slots should stay retired unless quality drops.

## 7. Chain-of-Draft

**What it does and when to reach for it.** Chain-of-Draft asks for terse per-step reasoning instead of verbose prose — margin notes rather than an essay. Reach for it when you are running reasoning at volume and latency or cost is the binding constraint. Know the trade precisely: on few-shot GSM8K, CoD scored 91.1% against CoT’s 95.4% on GPT-4o and 91.4% against 95.8% on Claude 3.5 Sonnet, with about 80% fewer output tokens. The 80% is tokens, not time: latency fell 76% on GPT-4o and 48% on Claude 3.5 Sonnet. On the other few-shot tasks it beat CoT on sports understanding, tied at 100% on coin flip, and split on date understanding — ahead on Claude 3.5 Sonnet, behind on GPT-4o. It buys a large cost reduction for about 4 percentage points of arithmetic accuracy. The abstract’s “as little as 7.6% of the tokens” matches one result only: sports understanding on Claude 3.5 Sonnet (manual Section 8.2).

**Build steps.**

1. **Use the paper’s instruction**: “Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####.”
2. **Include few-shot examples with hand-written drafts.** This is mandatory. On zero-shot GSM8K, CoD on Claude 3.5 Sonnet fell to 65.5% against CoT’s 90.4%, only 3.6 percentage points above direct answering (61.9%).
3. **Write the drafts yourself,** so they show exactly the brevity you want the model to copy.
4. **Parse after the** `####` **separator** with a deterministic parser.
5. **Do not enforce the five-word limit.** The authors did not; it is a nudge.
6. **Benchmark against CoT on your own task** before adopting. Arithmetic is where the largest gap appeared in the paper.
7. **Avoid it on small models unless your own test says otherwise** — on GSM8K, Qwen2.5-3B-Instruct scored 43.1% with CoD against 59.1% with CoT (the paper does not say whether that run was few-shot or zero-shot).

**Combines with.** Few-shot (§2) is a prerequisite. Self-consistency (§10) can be stacked on it; whether the vote recovers the arithmetic gap at a net token saving was not tested in the paper, so measure it.

### Example 7.1 — Unit arithmetic (retail operations)

```
Think step by step, but only keep a minimum draft for each
thinking step, with 5 words at most. Return the answer at the
end of the response after a separator ####.

Q: A box holds 24 cans. A pallet holds 18 boxes. How many
cans are on 3 pallets?
A: 24*18=432; 432*3=1296. #### 1296

Q: Tickets cost $12. A group of 7 gets 15% off the total.
What do they pay?
A: 12*7=84; 84*0.15=12.6; 84-12.6=71.4. #### 71.40

Q: {new_question}
A:
```

*Shows:* steps 1–4. Both drafts are arithmetic chains with no prose at all.

*Check:* recompute every answer in code. If you cannot, use Program-of-Thoughts (§13) instead — it executes the arithmetic rather than generating it.

### Example 7.2 — Date arithmetic (scheduling)

```
Think step by step, but only keep a minimum draft for each
thinking step, with 5 words at most. Return the answer at the
end of the response after a separator ####.

Q: Today is 2026-03-14. What date was 3 weeks ago?
A: 3 weeks=21 days; back 13 to Mar 1; 8 more into Feb;
Feb 2026 has 28; 2026-02-21. #### 2026-02-21

Q: A 45-day notice period starts 2026-01-20 (day 1). Last day?
A: Jan 20-31=12 days; 45-12=33; Feb=28; 33-28=5;
Mar 5. #### 2026-03-05

Q: {new_question}
A:
```

*Shows:* steps 1–3. Date understanding is where the paper’s results split: CoD was ahead of CoT on Claude 3.5 Sonnet and behind on GPT-4o. Test on your model.

*Check:* verify with a real date library. Every intermediate step in these two drafts is arithmetic you can reproduce.

### Example 7.3 — Multi-hop table lookup (operations)

```
Think step by step, but only keep a minimum draft for each
thinking step, with 5 words at most. Return the answer at the
end of the response after a separator ####.

Facts:
Denver: 410 orders, served by WH-4
Boise: 255 orders, served by WH-2
Q: Which warehouse ships to the city with the highest order
volume?
A: Top city=Denver; Denver served by WH-4.
#### WH-4

Facts:
WH-2: on-time 81%, carrier Ridgeline
WH-4: on-time 94%, carrier Harbor
Q: Which carrier serves the warehouse with the lowest
on-time rate?
A: Lowest on-time=WH-2; WH-2 carrier=Ridgeline.
#### Ridgeline

Facts:
{paste_fact_table}
Q: {new_question}
A:
```

*Shows:* steps 1–4. Each hop is one clause, which is exactly the shape CoD wants. Each demo carries its own small fact table, so every demonstrated answer can be derived from the facts shown.

*Check:* verify each hop against the table independently. A single wrong hop produces a confident wrong final answer with no visible seam.

### Example 7.4 — Eligibility screening at volume (benefits triage)

```
Think step by step, but only keep a minimum draft for each
thinking step, with 5 words at most. Return the answer at the
end of the response after a separator ####.

Rules: Minimum tenure 1 year. Minimum 30 hours per week.
Q: Applicant: 3 years tenure, 28 hrs/week.
A: Tenure 3y ok; hours 28 < 30 min; fails hours.
#### NOT ELIGIBLE

Rules: Minimum tenure 1 year. Minimum 30 hours per week.
Q: Applicant: 1 year tenure, 40 hrs/week.
A: Hours 40 ok; tenure 1y >= 1 min; passes both.
#### ELIGIBLE

Rules: {paste_rules}
Q: {new_applicant}
A:
```

*Shows:* steps 1–4. Both examples name the deciding rule, which makes a wrong answer diagnosable. Each demo carries its own rules, so the thresholds it applies are in the prompt rather than assumed.

*Check:* this is a screening tool, not a decision. Every NOT ELIGIBLE result should get human review before it reaches a person. State tenure directly in each applicant record; if you give a hire date instead, add today’s date to the prompt, because the model cannot know it.

### Example 7.5 — Coin-flip-style state tracking (game logic)

```
Think step by step, but only keep a minimum draft for each
thinking step, with 5 words at most. Return the answer at the
end of the response after a separator ####.

Q: A switch is on. Ana toggles it. Ben toggles it. Cal does
not. Is it on?
A: On; Ana off; Ben on; Cal on.
#### Yes

Q: A door is locked. Dee unlocks. Eli locks. Fay unlocks.
Is it locked?
A: Locked; Dee unlocked; Eli locked; Fay unlocked.
#### No

Q: {new_question}
A:
```

*Shows:* steps 1–3. On the paper’s coin-flip task, CoT and CoD both reached 100% on both models tested, so CoD bought the same accuracy for fewer tokens.

*Check:* simulate the state changes in code. This class of task is fully verifiable, so there is no excuse for trusting the output unchecked.

## 8. Chain-of-Symbol

**What it does and when to reach for it.** Chain-of-Symbol replaces verbose natural-language spatial descriptions with a compact symbol notation in the reasoning steps. On Brick World with ChatGPT-3.5 it took accuracy from 31.8% to 92.6% — a gain of 60.8 percentage points — with up to 65.8% fewer intermediate tokens. Reach for it on spatial and relational planning: layouts, grids, arrangements, adjacency. The demonstrated scope is spatial; outside it the gains are not established.

**Build steps.**

1. **Define the symbol table once, at the top,** before any state or question.
2. **Use symbols for relations, not for entities.** `A/B` for “on top of” is useful; renaming the crate to `X7` is not.
3. **Keep the scheme consistent** across every step and every example.
4. **Have the model restate one step in words** before you trust the rest — a cheap check that it read your table correctly.
5. **Require the final answer in plain language** so downstream readers do not decode symbols.
6. **Keep the table small.** Four or five symbols is plenty; a twenty-symbol language is a notation the model has to learn in-context, which defeats the point.

**Combines with.** Least-to-Most (§11) for multi-stage spatial plans. Tree-of-Thoughts (§12) when the layout needs search rather than derivation.

### Example 8.1 — Stacked blocks (spatial reasoning)

```
Notation:
  A/B  A is directly on top of B
  A|B  A and B sit side by side on the table
  T    the table

State: C/A, A/T, D|A, E/D

Question: If A is removed, which blocks fall, and what is the
resulting state?

Reason in the notation above, one relation change per step.
Then give the answer in one plain-English sentence.
```

*Shows:* steps 1, 2, 5. Three symbols carry the whole problem.

*Check:* verify the final state is physically consistent — nothing floating, nothing in two places.

### Example 8.2 — Warehouse grid routing (logistics)

```
Notation:
  (r,c)        grid cell, row then column; row 1 is the top
               row, column 1 the leftmost
  #            blocked cell
  > < ^ v      move right, left, up, down
Grid: 5x5. Blocked: (2,2), (2,3), (3,1).
Start (1,1). Goal (4,4).

Find the shortest path using only the move symbols, one move
per step, showing the cell after each move. Then state the
number of moves and the path as a plain list of cells.
```

*Shows:* steps 1–3, 5.

*Check:* the shortest path here is 6 moves — the Manhattan distance from (1,1) to (4,4) — and exactly one path of that length exists: > > > v v v. A longer answer means the model missed it; a shorter one is impossible.

### Example 8.3 — Floor layout from constraints (manufacturing)

```
Notation:
  X~Y   X is adjacent to Y
  X>Y   X is east of Y
  X^Y   X is in front of Y

Constraints:
  press ~ conveyor
  bin > conveyor
  inspection ^ press
  conveyor is against the west wall

Derive a consistent west-to-east order for the conveyor,
press, and bin using the notation; place inspection by its
in-front-of constraint, not in that order. Then describe the
final layout in two sentences with no symbols. If the
constraints cannot all be satisfied, name the two that
conflict.
```

*Shows:* steps 1–3, 5, plus a failure path.

*Check:* these constraints are satisfiable — conveyor, press, bin west to east, with inspection in front of the press. If the model reports a conflict, it misread the table, which is exactly what step 4 catches.

### Example 8.4 — Seating arrangement (event planning)

```
Notation:
  X-Y   X sits immediately left of Y
  X=Y   X and Y must not be adjacent
  [n]   seat position, 1 through 6; seat 1 is leftmost

Constraints:
  Ana - Ben
  Cal = Dee
  Eli in [1]
  Fay not in [6]

Restate the second constraint in plain words to confirm you
read the table. Then derive a valid seating of all six people
using the notation, and give the final order as a plain list.
```

*Shows:* steps 1, 3, 4, 5. Step 4 is explicit here.

*Check:* read the restatement first. If it says Cal and Dee must sit together, stop — the rest of the answer is built on a misread. Then check the final list in code against all four constraints: more than one seating is valid, so there is no single expected answer to compare with.

### Example 8.5 — Dependency ordering (project scheduling)

```
Notation:
  A->B   A must finish before B starts
  A||B   A and B can run in parallel
  [d]    duration in days

Tasks:
  survey[3] -> design[5]
  design -> permit[10]
  design -> procure[7]
  permit || procure
  permit -> build[14]
  procure -> build

Derive the critical path in the notation, then state the
total duration and the critical path as a plain sentence.
```

*Shows:* steps 1–3, 5.

*Check:* compute it yourself — 3 + 5 + 10 + 14 = 32 days through permit, versus 3 + 5 + 7 + 14 = 29 through procure. The critical path is the permit branch at 32 days.

# Part 3 — Reasoning Topologies

## 9. Chain-of-Thought

**What it does and when to reach for it.** Chain-of-Thought asks for intermediate steps before the answer, conditioning the final answer on the model’s own scratch work. Kojima’s zero-shot trigger took MultiArith from 17.7% to 78.7% on text-davinci-002 — a gain of 61.0 percentage points. But the 2025 picture is different: on GPQA Diamond, explicit CoT prompting of reasoning models gave small changes — +2.9 percentage points for o3-mini, +3.1 for o4-mini, −3.3 for Gemini 2.5 Flash — while CoT requests took 20–80% longer, or 10–20 seconds (*Prompting Science Report 2*, arXiv 2506.07142). Reach for CoT on non-reasoning models doing multi-step work. On reasoning models it is usually not worth the extra time, so test it on yours and consider spending the budget on grounding instead.

**Build steps.**

1. **Check which model you are on.** Reasoning model: usually not worth the extra time, so test before using it. Non-reasoning model: continue.
2. **Add an explicit reasoning trigger** before the answer.
3. **Give the reasoning a shape** — “state which rule you apply at each step” beats “think carefully.”
4. **Separate reasoning from answer** with a parseable delimiter the model must emit.
5. **Measure variance, not just the mean.** CoT can raise variance while barely moving the average; run each condition many times.
6. **Remember the chain is not the computation.** Averaged across six hint types on multiple-choice MMLU and GPQA questions, Claude 3.7 Sonnet verbalized a hint it used 25% of the time and DeepSeek R1 39% (Chen et al., arXiv 2505.05410). Do not treat the trace as an audit trail.

**Combines with.** Self-consistency (§10) samples multiple chains and votes. Least-to-Most (§11) replaces free-form reasoning with an explicit decomposition. Conflicts with reasoning models, where it is usually not worth the extra time.

### Example 9.1 — Multi-step financial calculation (accounting)

```
Work through the problem step by step, then give the final
answer on its own last line as "ANSWER: <number>".

A vendor invoices $4,800 with terms 2/10 net 30. We pay on
day 8. A $150 credit from last month applies before the
discount is calculated. What do we remit?
```

*Shows:* steps 2, 4. The ordering detail (“before the discount is calculated”) is the whole problem.

*Check:* (4800 − 150) × 0.98 = $4,557.00. Any answer that applies the discount first gives $4,554.00 and is wrong.

### Example 9.2 — Policy application with named criteria (benefits administration)

```
Decide whether the request qualifies under the policy.

Work through each criterion in the policy in order. For each,
state: the criterion, the relevant fact, and whether it is met.
Then give a final line "DECISION: QUALIFIES" or
"DECISION: DOES NOT QUALIFY". If it does not qualify, name the
first criterion that failed.

Policy: {paste_policy}
Request: {paste_request}
```

*Shows:* steps 3, 4. Forcing the criterion list makes a wrong decision traceable to a specific step.

*Check:* the failed criterion, not the decision. A right answer reached through the wrong criterion will be wrong on the next case.

### Example 9.3 — Constraint-based scheduling (operations)

```
Think step by step, naming which constraint you apply at each
step, then give the answer.

Constraints:
- Days are working days, Monday to Friday. A task's first
  day counts as its day 1.
- The audit takes 5 working days and cannot start before
  Monday 2026-04-06.
- The close starts on the first working day after the
  audit's last day and takes 3 working days.

Question: What is the earliest date the close can end?
End with "ANSWER: YYYY-MM-DD".
```

*Shows:* steps 2–4.

*Check:* April 6, 2026 is a Monday. The audit runs Apr 6–10 (Mon–Fri) and the close starts the next working day, so it runs Apr 13–15 (Mon–Wed) and the answer is 2026-04-15.

### Example 9.4 — Diagnostic reasoning over logs (software support)

```
Think step by step. For each step, state the specific log line
you are relying on before drawing a conclusion from it.

Then give:
  ROOT CAUSE: <one sentence>
  EVIDENCE: <the log line that most supports it>
  ALTERNATIVE: <the next most likely cause, and the log line
  that would distinguish it>

Logs:
{paste_logs}
```

*Shows:* steps 3, 4, 6. The ALTERNATIVE field is a cheap prompt for alternatives; when the stakes are high, run a separate disconfirmation pass (§21).

*Check:* the ALTERNATIVE field. If it is empty or generic, the model committed to its first hypothesis and the reasoning is decoration.

### Example 9.5 — Comparative judgment with explicit weighting (procurement)

```
Compare the two options against the criteria below.

Step 1: For each criterion, state how each option performs
and which is better on that criterion alone.
Step 2: State which criteria matter most for the stated goal,
and why.
Step 3: Give the recommendation, and name the single fact
that, if it turned out to be false, would reverse it.

End with "RECOMMENDATION: A" or "RECOMMENDATION: B".

Criteria: {paste_criteria}
Goal: {paste_goal}
Option A: {paste_a}
Option B: {paste_b}
```

*Shows:* steps 3, 4. Step 3 of the prompt — the reversal fact — is a cheap, high-value habit.

*Check:* verify the reversal fact is actually load-bearing. If flipping it would not change the answer, the reasoning is post-hoc.

## 10. Self-Consistency

**What it does and when to reach for it.** Self-consistency samples several independent reasoning paths at non-zero temperature and takes the majority answer. Wang et al. report best-case gains over CoT of +17.9 percentage points on GSM8K and +12.2 on AQuA for GPT-3 (code-davinci-002) with 40 sampled paths. The manual classifies it as a decoding strategy (Axis 4, Section 10.2), as its authors do; it sits in this Part because every path it samples is a reasoning chain. Reach for it when the answer is short and verifiable, the task matters, and you can afford N calls. Do not reach for it on open-ended generation, where there is nothing to vote on, and do not mistake the vote for a confidence score — a shared bias produces a confident wrong majority.

**Build steps.**

1. **Confirm the answer space is votable** — a number, a label, a date. If two correct answers can be worded differently, you need an aggregator (Example 10.5).
2. **Set temperature to 0.5–0.7.** At temperature 0 the paths are nearly identical, so the vote adds nothing.
3. **Start at N=5,** not 40. Raise it until the accuracy gain flattens, then stop.
4. **Parse the answer deterministically** — require a fixed final-line format.
5. **Majority-vote in code,** never by asking the model which answer won.
6. **Report the vote split** alongside the answer, and set a threshold below which the case goes to a human.

**Combines with.** Sits on top of CoT (§9), Chain-of-Draft (§7), or Program-of-Thoughts (§13). The last combination suits arithmetic: execution removes calculation slips from each path, and the vote can catch an idiosyncratic setup error. A misreading every path shares survives the vote, so check the setup with Chain-of-Verification (§19).

### Example 10.1 — Arithmetic with an escalation threshold (accounting)

```
Call 5 times at temperature 0.7 with this prompt, then vote
on the ANSWER line in code.

  Solve step by step. End with "ANSWER: <number>".

  {problem}

Decision rule:
  5-0 or 4-1       -> return the majority answer
  any other split  -> escalate to a human, and show them all
                      five reasoning paths
```

*Shows:* steps 2–6.

*Check:* track how often a split other than 5-0 or 4-1 occurs (3-2, 3-1-1, 2-2-1, and so on). A high rate may mean the task is near the edge of the model’s ability or the problem is ambiguous; read a few split cases before raising N.

### Example 10.2 — Content moderation with an asymmetric threshold (trust and safety)

```
Sample 5 independent judgments at temperature 0.7:

  Does this post violate the harassment policy below?
  Reason briefly, then end with "VERDICT: YES" or
  "VERDICT: NO".

  Policy: {paste_policy}
  Post: {paste_post}

Decision rule, by YES votes out of 5:
  5-0 or 4-1 YES        -> action the post
  3-2 YES               -> route to human review
  2-3, 1-4, or 0-5 YES  -> no action
Log every split.
```

*Shows:* steps 1, 5, 6. The threshold is deliberately asymmetric: a simple majority would act at 3-2 YES, but this rule needs 4 of 5, because a false action costs more than a false pass here.

*Check:* audit the 3-2 YES cases specifically. They are where this rule differs from a simple majority, which would have acted on them; a 4-1 YES case is actioned either way.

### Example 10.3 — Date extraction with normalization before voting (records processing)

```
Sample 5 at temperature 0.5:

  Extract the effective date from the document.
  End with "ANSWER: YYYY-MM-DD" or "ANSWER: NONE".

  Document: {paste_doc}

Before voting, normalize: strip whitespace, reject anything
not matching ^\d{4}-\d{2}-\d{2}$ or NONE. Vote on the
normalized values. If fewer than 3 responses produce a valid
format, treat the case as a parse failure, not a tie.
```

*Shows:* steps 1, 4, 5. Normalization before voting is the step people skip; unnormalized votes split spuriously.

*Check:* the parse-failure rate. If it is non-trivial, move to schema-constrained generation (§18) rather than adding samples.

### Example 10.4 — Classification with per-class vote tracking (research coding)

```
Sample 5 at temperature 0.6:

  Assign one code from the codebook below. Reason briefly,
  then end with "CODE: <code>".

  Codebook: {paste_codebook}
  Excerpt: {paste_excerpt}

Vote in code. Record the full distribution, not just the
winner — a 3-1-1 spread across three codes is a different
finding from 3-2 across two.
```

*Shows:* steps 1, 5, 6. Keeping the distribution turns voting into a codebook diagnostic.

*Check:* excerpts that split three ways may point to overlapping categories in the codebook. Read them and check the code definitions before changing the prompt.

### Example 10.5 — Free-form answers via an aggregator (research support)

```
STEP 1 — sample 5 at temperature 0.7:
  Answer the question in 2-3 sentences, citing the provided
  sources by number.
  Question: {q}
  Sources: {srcs}

STEP 2 — aggregate with a separate call:
  Below are 5 independent answers to the same question.

  {answer_1}
  {answer_2}
  {answer_3}
  {answer_4}
  {answer_5}

  Produce the answer most consistent with the majority.
  Then list, under "LOW AGREEMENT:", every claim that appears
  in fewer than 3 of the 5 answers. Do not merge low-agreement
  claims into the main answer.
```

*Shows:* step 1’s escape hatch — Universal Self-Consistency (arXiv 2311.17311) for answers you cannot vote on directly. This waives step 5: the aggregator model does the counting, so spot-check its counts against the five answers.

*Check:* the LOW AGREEMENT list is the useful output. Those are the claims the five answers disagree on, so check them against the sources first. Recount a few claims by hand: the aggregator’s counts are the model’s own.

## 11. Least-to-Most Decomposition

**What it does and when to reach for it.** Least-to-Most first asks for an ordered list of subproblems, then solves them in sequence with each answer feeding the next. The evidence is sharply conditional: with code-davinci-002, on SCAN’s length split it reached 99.7% against CoT’s 16.2% (14 exemplars), but on GSM8K it scored 62.4% against 60.9% — a gain of 1.5 percentage points. Reach for it when the task genuinely decomposes into ordered, independently answerable parts, and when the real instances are harder than any example you can show. Skip it otherwise; you will pay two calls for no gain.

**Build steps.**

1. **Decompose in a separate call, and forbid solving.** A model asked to decompose and solve will solve and back-fill a decomposition.
2. **Require the subproblems be ordered** and each answerable given only the answers before it.
3. **Inspect the decomposition before spending calls on it.** This is the cheapest possible place to catch a failure.
4. **Solve one subproblem per call,** passing prior question-answer pairs forward.
5. **Require each answer to name its assumption** so a bad premise surfaces at the step that introduced it.
6. **Stop at the first failure** rather than continuing on a broken foundation.

**Combines with.** Prompt chaining (§22) is the infrastructure this runs on. Program-of-Thoughts (§13) for subproblems that are computational. Conflicts with Chain-of-Draft (§7) — terse drafts and explicit decomposition pull in opposite directions.

### Example 11.1 — Migration cost estimate (IT project management)

```
STAGE 1 — decompose only. Do not solve anything.

  List the sub-questions that must be answered, in order, to
  estimate the total cost of the migration described below.
  Number them. Each must be answerable using only the answers
  to the ones before it. Output only the numbered list.

  Description: {paste_description}

STAGE 2 — for each sub-question i, one call:

  Description: {paste_description}

  Answered so far (one line per earlier question and its
  answer):
  {prior_qa}

  Answer only this question: {qi}
  Give the answer, then a line "ASSUMPTION:" naming the
  single assumption it rests on. If you cannot answer it from
  the prior answers and the description, reply
  "BLOCKED: <what is missing>".
```

*Shows:* steps 1, 2, 4–6.

*Check:* read the ASSUMPTION lines as a set before reading any answer. A bad assumption early can carry into every later number.

### Example 11.2 — Compositional instruction following (task planning)

```
STAGE 1:
  Break the instruction into the smallest ordered steps that
  each map to exactly one primitive from this list:
    MOVE(x,y), PICK(obj), PLACE(obj, target), WAIT(seconds)

  Instruction: "{instruction}"

  Output only the numbered decomposition in plain English.
  Do not emit primitives yet.

STAGE 2:
  Primitives: MOVE(x,y), PICK(obj), PLACE(obj, target), WAIT(seconds)

  Decomposition: {decomposition}
  Now emit the primitive sequence, one per line, using only
  the primitives above.
  If any step cannot be expressed with the four primitives
  above, stop at that step and reply
  "UNSUPPORTED STEP <n>: <why>".
```

*Shows:* steps 1, 2, 6. This resembles the SCAN-style tasks where Least-to-Most did best in the paper (code-davinci-002); run your own comparison against a single call.

*Check:* validate every emitted primitive against the grammar in code. An invented verb means the model ignored the constraint.

### Example 11.3 — Layered eligibility determination (public benefits)

```
STAGE 1:
  List, in order, every determination that must be made to
  decide eligibility under the rules below. Each determination
  must depend only on the ones before it. Output only the list.

  Rules: {paste_rules}

STAGE 2 — per determination:
  Rules: {paste_rules}
  Prior determinations: {prior}
  Now make only this determination: {current}

  Give: the rule text you applied (quoted), the facts you
  relied on, and the determination.
  If this determination fails, say so and stop — do not
  evaluate later determinations.

  Facts: {paste_facts}
```

*Shows:* steps 1–4 and 6. Stopping at first failure mirrors how the rules actually operate. The quoted rule text and the listed facts stand in for step 5’s assumption line.

*Check:* the quoted rule text, against the source, at every step. This is a context-anchoring requirement (§4) embedded in a decomposition.

### Example 11.4 — Root-cause analysis in stages (incident review)

```
STAGE 1:
  Given the incident summary below, list the questions that
  must be answered in order to establish the root cause.
  Each must be answerable from evidence, not speculation.
  Output only the list.

  Summary: {paste_summary}

STAGE 2 — per question:
  Answered so far: {prior_qa}
  Evidence available: {paste_evidence}

  Answer only: {current_question}
  Cite the specific evidence. If the available evidence does
  not answer it, reply "EVIDENCE GAP: <what would answer it>"
  and continue to the next question rather than stopping.
```

*Shows:* steps 1, 2, 4. It asks for cited evidence in place of step 5’s assumption line. Note this one does *not* stop at first failure (step 6) — an evidence gap is information, not a blocker.

*Check:* the EVIDENCE GAP lines are the deliverable. They tell you what logging you are missing for next time.

### Example 11.5 — Multi-part legal-adjacent question (compliance research)

```
STAGE 1:
  The question below has multiple parts that depend on each
  other. List them in dependency order. Do not answer them.

  Question: {paste_question}

STAGE 2 — per part:
  Question: {paste_question}
  Answers so far: {prior}
  Source material: {paste_sources}

  Answer only this part: {current_part}
  Use only the source material.
  Format:
    ANSWER: <answer, or NOT IN SOURCES>
    SOURCE: <quoted sentence, or NONE>
    DEPENDS ON: <which earlier part, or NONE>

STAGE 3 — assemble:
  Parts and answers: {all_parts}
  Write the combined answer. If any part has SOURCE: NONE,
  mark the combined answer "PARTIALLY UNSUPPORTED" and say
  which part.
```

*Shows:* steps 1, 2, 4, 5, plus an assembly stage.

*Check:* trace DEPENDS ON backward. Any DEPENDS ON that names a later part means Stage 1 put the parts in the wrong order; fix the order and rerun. Also read each part marked NONE for a dependency it did not declare.

## 12. Tree-of-Thoughts

**What it does and when to reach for it.** Tree-of-Thoughts generates several candidate next steps, evaluates them, and searches — keeping the promising branches and abandoning dead ends. On Game of 24 with GPT-4 it reached 74% at breadth 5, against 4.0% for CoT; a compute-matched best-of-100 CoT scored 49%. By the paper’s own statement it could require 5–100 times more generated tokens than CoT. Reach for it only when the task requires search: when a single forward pass commits to a choice early and cannot recover, and when you can write an evaluator that reliably says whether a partial solution is still viable. If you cannot write that evaluator, you cannot use this technique.

**Build steps.**

1. **Define the thought unit** — what exactly one node contains. A move, a partial plan, a paragraph.
2. **Write the generator prompt:** given a state, propose k distinct next thoughts.
3. **Write a separate evaluator prompt.** Separate call, separate context. An evaluator that can see its own proposals will approve them.
4. **Require the evaluator to give a reason,** not just a score. A score-only evaluator is unauditable and usually wrong in ways you cannot see.
5. **Choose search strategy and beam width.** Start at breadth 3, depth 3.
6. **Set a hard node budget** in code. Without one, cost is unbounded.
7. **Keep the controller in code,** not in a prompt. Asking a model to manage a search tree in its head is the most common way this technique fails.

**Combines with.** Self-consistency (§10) at each evaluation step if the evaluator is noisy. Graph-of-Thoughts when branches should merge rather than only split. Conflicts with latency budgets.

### Example 12.1 — Game-of-24-style puzzle (numerical search)

```
GENERATOR (one call per expansion):
  Numbers remaining: {numbers}
  Propose 3 distinct next operations. For each, give the
  operation and the resulting number set, one per line, as:
  OP: <a op b = c> | LEFT: <remaining numbers>

EVALUATOR (separate call, does not see the generator's reasoning):
  Goal: reach exactly 24 using all numbers.
  For each candidate set below, judge whether 24 is still
  reachable. Answer exactly SURE, MAYBE, or IMPOSSIBLE,
  followed by one sentence of reason.

  {candidate_sets}

CONTROLLER (code): keep SURE and MAYBE, beam width 3,
depth = number of operations needed, hard cap 200 nodes.
```

*Shows:* steps 1–7.

*Check:* verify the final arithmetic in code. The evaluator’s SURE/MAYBE labels are heuristics and will sometimes prune a reachable branch.

### Example 12.2 — Story structure search (fiction editing)

```
GENERATOR (level 1):
  Premise: {premise}
  Act one: {act_one}
  Propose 3 structurally different second acts, 2 sentences
  each. They must differ in who holds the initiative, not
  just in what events occur.

EVALUATOR (separate call, all candidates at once):
  Premise: {premise}
  Act one: {act_one}
  Candidate second acts: {candidates}
  For each second act, rate 1-5 on:
  (a) follows from act one
  (b) creates a problem act three can resolve
  (c) differs from the other candidates
  Give the three scores and one sentence of justification.

GENERATOR (level 2, one call per kept second act):
  Premise: {premise}
  Act one: {act_one}
  Second act: {second_act}
  Propose 3 different third acts, 2 sentences each, each
  resolving the problem the second act creates.

CONTROLLER (code): keep the top 2 second acts by total
score and expand each into act threes. Stop after two
levels.
```

*Shows:* steps 1–5. Criterion (c) is what keeps the tree from collapsing into three versions of one idea.

*Check:* read the three candidates at level one. If they are paraphrases, the generator constraint is not working and the search is theater.

### Example 12.3 — Constrained route planning (logistics)

```
GENERATOR:
  Partial route: {route}
  Remaining stops: {stops}
  Time windows: {windows}
  Start time: {start_time}
  Travel times (minutes, including service time at each
  stop): {travel_times}
  Propose the 3 most promising next stops, one per line, as:
  NEXT: <stop> | WHY: <one short reason>

CONTROLLER (code): compute each candidate's arrival time
from the start time and travel times, and drop any
candidate that misses its window.

EVALUATOR:
  Partial routes with arrival times: {candidate_routes}
  Remaining stops: {stops}
  Time windows: {windows}
  Travel times (minutes, including service time at each
  stop): {travel_times}
  For each partial route, answer SURE / MAYBE / IMPOSSIBLE on
  whether all remaining windows can still be met, with one
  sentence of reason.

CONTROLLER: prune IMPOSSIBLE, beam width 3, depth = number
of stops, hard cap 150 expansions. On exhaustion, return the
best partial route and the first window it cannot meet.
```

*Shows:* steps 2–6, plus a defined failure output.

*Check:* the arrival times come from code, not from the model. Spot-check one route by hand, and never let the model’s arithmetic decide whether a window is met.

### Example 12.4 — Query formulation search (research)

```
GENERATOR:
  Research question: {question}
  Searches tried and what they returned: {history}
  Propose 3 next search queries that would find different
  evidence than the ones already tried. Say what each is
  looking for.

EVALUATOR:
  Research question: {question}
  Searches tried and what they returned: {history}
  Proposed queries: {proposed_queries}

  For each proposed query, judge whether it is likely to
  surface evidence not already in the history above. Answer
  PROMISING, MARGINAL, or REDUNDANT with one sentence of
  reason.

CONTROLLER: run PROMISING queries, add results to history,
repeat. If a round has no PROMISING query, run its MARGINAL
queries instead. Stop after 4 rounds or when all proposals
come back REDUNDANT.
```

*Shows:* steps 1–6. The REDUNDANT verdict is the natural stopping condition.

*Check:* read the history at the end. If the searches all circle one framing, the generator needed a stronger difference constraint.

### Example 12.5 — Schema design exploration (data engineering)

```
GENERATOR:
  Requirements: {requirements}
  Stated queries: {queries}
  Current partial schema: {schema}
  Propose 3 different ways to model the next entity. For each:
  the tables, the keys, and the one stated query it makes fast.

EVALUATOR:
  Requirements: {requirements}
  Stated queries: {queries}
  Current partial schema: {schema}
  Candidates: {candidates}
  For each candidate, answer these separately:
  - Does it satisfy every stated requirement? YES/NO + which
    one fails.
  - Which stated query does it make slow?
  - How reversible is it if requirements change? Score 1-5
    + why.

CONTROLLER: prune any candidate failing a requirement.
Keep the top 2 by reversibility score, breaking ties by
fewest slow queries. Depth 3, cap 30 nodes.
```

*Shows:* steps 2–4. Three separate evaluator questions beat one composite score.

*Check:* the “which query does it make slow” answers. A candidate with no slow query means the evaluator is not being honest, not that the design is perfect.

## 13. Program-of-Thoughts and PAL

**What it does and when to reach for it.** Program-of-Thoughts has the model write code and an interpreter execute it, so arithmetic is computed rather than generated. PoT reports roughly 12% average improvement over CoT on math and financial question answering; PAL with Codex surpassed PaLM-540B CoT by about 15 percentage points on GSM8K. Reach for it whenever the answer involves arithmetic, dates, sorting, counting, or any operation a computer does exactly and a language model approximates. It is a strong default for numerical work, though a wrong setup can still produce a clean, wrong answer.

**Build steps.**

1. **Instruct code generation explicitly,** and forbid computing the answer in prose.
2. **Name the inputs as variables with comments** so a reviewer can check the setup separately from the logic.
3. **Require printed intermediates.** A program that prints only the answer is as opaque as a model that states only the answer.
4. **Fix the final output line or lines** — `print("ANSWER:", result)`, or one labelled line per quantity — so parsing is deterministic.
5. **Restrict the library surface.** Standard library only, unless you have a reason.
6. **Execute in a sandbox** with no network and a wall-clock timeout.
7. **Treat an exception as a task failure.** Do not let the model improvise a result when the code fails.

**Combines with.** Self-consistency (§10) over multiple programs, for arithmetic that matters: execution checks each calculation, and the vote can catch an idiosyncratic setup error. Chain-of-Verification (§19) on the setup, since execution verifies the math but not the model of the problem, and a misreading every program shares survives the vote.

### Example 13.1 — Loan amortization (personal finance)

```
Write Python that computes the answer. Do not compute it
yourself in prose.

Requirements:
- Define each input as a named variable with a comment.
- print() each intermediate quantity with a label.
- The last two lines must be print("PAYMENT:", payment) and
  print("TOTAL_INTEREST:", total_interest), rounded to cents.
- Use only the standard library.

Problem: A loan of $250,000 at 6.25% nominal annual interest,
compounded monthly, amortized over 30 years. Compute the
monthly payment and the total interest paid over the life of
the loan.
```

*Shows:* steps 1–5.

*Check:* verify the monthly rate is 0.0625/12 and n is 360, then compare with PAYMENT 1539.29 and TOTAL_INTEREST 304145.48, the latter computed from the unrounded payment. The characteristic error is a correct formula applied to an annual rate.

### Example 13.2 — Business-day arithmetic (project management)

```
Write Python using only datetime from the standard library.

- Define inputs as variables with comments.
- print() the date after each step.
- Final line: print("ANSWER:", result)

Problem: A task starts on 2026-04-06, which counts as
business day 1, and takes 18 business days, skipping
Saturdays, Sundays, and the company holiday 2026-04-20. On
what date does it finish?
```

*Shows:* steps 1–4. The problem states the day-1 convention, so the model has no off-by-one choice to make silently, and the holiday sits inside the window, so the skip logic is exercised.

*Check:* the finish is 2026-04-30. A result of 2026-04-29 means the holiday was not skipped, and 2026-05-01 means the start date was not counted as day 1. A convention left unstated is a specification problem, not a model problem.

### Example 13.3 — CSV aggregation with a stated schema (analytics)

```
Write Python that answers the question using the CSV at
data.csv.

Columns: order_id, customer_id, country, total_cents,
placed_at (ISO date string)

- Standard library only (csv, datetime, statistics,
  collections).
- print() the row count after each filter step.
- Final line: print("ANSWER:", result)
- If a row has a malformed date or a non-numeric total, skip
  it and count skips; print the skip count.

Question: Which country had the highest median order value
among orders placed in Q2 2026, counting only countries with
at least 50 such orders?
```

*Shows:* steps 1–5. The skip counter surfaces data quality that would otherwise vanish into the answer.

*Check:* the row counts after each filter. Compare each count with what the file’s date range predicts; a drop far beyond that points to a bug in the date parsing rather than a finding.

### Example 13.4 — Unit conversion chain (engineering)

```
Write Python. Do not do any arithmetic in prose.

- Define every conversion factor as a named constant with a
  comment giving its source units.
- print() the value and unit after each conversion.
- Final line: print("ANSWER:", result, "<unit>")
- Assert the final magnitude is within the plausible range
  given in the problem; raise if not.

Problem: {paste_problem}
```

*Shows:* steps 1–4, plus an assertion. Naming factors with their units is how you catch an inverted conversion.

*Check:* read the constants, not the logic. An inverted factor produces code that runs cleanly and answers wrongly by a factor of the conversion squared.

### Example 13.5 — Statistical summary with explicit assumptions (research)

```
Write Python using only the standard library (statistics, math).

- Load the values from the list below.
- print() n, mean, median, standard deviation, and the
  quartiles, each labeled.
- State in a comment whether you are computing a sample or
  population standard deviation, and why.
- Final line: print("ANSWER:", result)

Question: {paste_question}
Values: {paste_values}
```

*Shows:* steps 1–5. The sample-versus-population comment is the assumption that silently changes the answer.

*Check:* that comment first. `statistics.stdev` and `statistics.pstdev` differ, and the model picks one without saying unless you make it.

## 14. Step-Back Prompting

**What it does and when to reach for it.** Step-Back asks the model to derive the general principle before applying it to the specific case. Reach for it when a question is an instance of something more general, and when the model’s failure mode is pattern-matching to a superficially similar case instead of reasoning from the rule. It is cheap — one extra paragraph, not one extra call — and it pairs naturally with grounded work, where the “principle” is the governing rule in the source document.

**Build steps.**

1. **Ask for the principle first,** in its own labeled section.
2. **Forbid mentioning the specific case** while stating the principle. Otherwise the principle gets reverse-engineered from the desired answer.
3. **Then apply it,** explicitly naming which part of the principle covers this case.
4. **Ask what would fall outside the principle** — a cheap check that the principle has real edges.
5. **Where a source document exists, require the principle to be quoted from it,** not generated.

**Combines with.** Context anchoring (§4) — the principle should come from the document. Chain-of-Thought (§9) for the application step. Least-to-Most (§11) when the principle has several independent conditions.

### Example 14.1 — Physics-style reasoning (education)

```
STEP 1 — Principle. State the general physical principle that
governs problems of this type. Do not mention the specific
numbers or objects in the question.

STEP 2 — Application. Apply the principle to the question,
naming which term of the principle each given value fills.

STEP 3 — Boundary. Give one variation of this question where
the principle would NOT apply, and say why.

Question: {paste_question}
```

*Shows:* steps 1–4.

*Check:* step 3. If the boundary case is trivial or nonsensical, the model stated a principle it does not actually understand, and step 2 is pattern matching.

### Example 14.2 — Policy interpretation from a source (compliance)

```
STEP 1 — Rule. Quote the general rule from the policy below
that governs situations of this kind. Quote it verbatim. Do
not mention the specific facts yet.

STEP 2 — Elements. Break the quoted rule into its separate
conditions, numbered.

STEP 3 — Application. For each numbered condition, state the
fact that satisfies it or the fact that fails it.

STEP 4 — Conclusion, plus one sentence on which condition is
closest to the line.
Policy: {paste_policy}
Facts: {paste_facts}
```

*Shows:* steps 1–3, 5. The verbatim quote requirement is what stops the model inventing a plausible rule.

*Check:* the quote, against the policy. Then check that the numbered conditions actually come from the quoted text rather than from general knowledge of similar policies.

### Example 14.3 — Debugging by principle (software)

```
STEP 1 — Class. What general class of bug produces the
symptom below? Describe the class, not this instance.

STEP 2 — Signature. What does this class of bug typically
look like in logs, in timing, and in reproducibility?

STEP 3 — Match. Compare the actual evidence to that
signature. Say explicitly where the evidence matches and
where it does not.

STEP 4 — Verdict. Either name this bug class as the likely
cause, or say the evidence does not match it and name the
next candidate class.

Symptom: {paste_symptom}
Evidence: {paste_evidence}
```

*Shows:* steps 1–4. Step 3’s “where it does not match” is a cheap prompt for disconfirming evidence; when the stakes are high, run a separate disconfirmation pass (§21).

*Check:* the mismatch list. An empty mismatch list on real-world evidence is almost always a sign the model is forcing a fit.

### Example 14.4 — Negotiation framing (business)

```
STEP 1 — Interests. Without referring to the specific offer
below, state the general categories of interest that both
sides in a deal of this type usually hold.

STEP 2 — Map. Map each side's stated positions in the offer
onto those interest categories.

STEP 3 — Gaps. Identify any interest category where one side
has stated no position. Those are the unexplored areas.

STEP 4 — Moves. Propose two moves that trade across
categories rather than splitting a single number.

Offer: {paste_offer}
```

*Shows:* steps 1–3. Step 3 is the payoff — the unexplored categories are where value usually is.

*Check:* whether the proposed moves actually trade across categories. A move that just adjusts price has ignored the whole exercise.

### Example 14.5 — Diagnostic question triage (health information)

```
STEP 1 — Category. What general category of question is this?
State it without reference to the specific details.

STEP 2 — What determines the answer. For that category, what
factors generally determine the answer, and which of them
require a clinician's judgment or an examination?

STEP 3 — What can be said here. Given the details provided,
state only what follows from general, well-established
information.

STEP 4 — What cannot. State plainly which parts of the
question cannot be answered without the factors identified
in step 2, and recommend the appropriate professional.

Question: {paste_question}
```

*Shows:* steps 1–4. Step 2 does the work: it identifies the boundary before the model gets near an answer.

*Check:* step 4 must be non-empty for anything clinical. An empty “cannot” section on a health question is the failure this structure exists to prevent.

# Part 4 — Grounding and Action

## 15. Retrieval-Augmented Generation

**What it does and when to reach for it.** RAG retrieves relevant documents and places them in context so the model answers from them rather than from memory. This is the prompting form, in-context retrieval; the original RAG of Lewis et al. also trains the retriever and generator (manual Section 11.1). Reach for it whenever the answer depends on facts that are current, proprietary, or too numerous to fit in a prompt. Know its ceiling: RAG reduces hallucination but does not eliminate it. Across 202 preregistered queries, commercial legal research tools built on RAG hallucinated between 17% and 33% of the time (Magesh et al., 2025). Design as though retrieval will sometimes miss, because it will.

**Build steps.**

1. **Chunk with overlap,** and keep enough surrounding context that a chunk is interpretable alone. A fact split across two chunks is retrievable from neither.
2. **Retrieve more than you need, then re-rank** before truncating to the context budget.
3. **Number the sources** so the model can cite them and you can check the citation.
4. **Place the highest-relevance sources at the start and end** of the context block.
5. **Require a citation per claim.**
6. **Give an exact “not in sources” string,** and route it to a retrieval fix rather than a bigger model.
7. **Log retrieval quality separately from answer quality.** Most RAG failures are retrieval failures wearing an answer’s clothes.
8. **Say what to do when sources conflict:** present both, attribute both, resolve neither.

**Combines with.** Context anchoring (§4) is the prompt half of this. Chain-of-Verification (§19) catches unsupported claims. Self-consistency (§10) does not fix retrieval misses, because every sample sees the same retrieved context.

### Example 15.1 — Cited answer with a refusal path (internal knowledge base)

```
<sources>
[1] {chunk_1}
[2] {chunk_2}
[3] {chunk_3}
</sources>

Question: {question}

- Answer only from the sources above.
- Cite the source number after each claim, like [2].
- If the sources do not contain the answer, reply exactly
  "NOT IN SOURCES" and then list what information would be
  needed to answer it.
- If two sources conflict, present both with their numbers
  and say they conflict. Do not choose between them.
```

*Shows:* steps 3, 5, 6, 8.

*Check:* the “what would be needed” list on every NOT IN SOURCES. It is a free specification of the documents your corpus is missing.

### Example 15.2 — Retrieval self-assessment before answering (support automation)

```
<retrieved>
{chunks}
</retrieved>

Question: {question}

First line, always:
  RELEVANCE: HIGH | PARTIAL | NONE

That is your judgment of whether the retrieved text actually
addresses the question — not whether you could answer it.

Then, only if HIGH or PARTIAL, answer with citations.
If NONE, stop after the first line.

Do not answer from general knowledge under any circumstance,
even if you are confident.
```

*Shows:* steps 6, 7. The relevance line is a self-reported retrieval signal on every request; validate it on a labelled sample before relying on it.

*Check:* the rate of NONE and PARTIAL over time. A rise may mean your corpus has drifted from your traffic — a retrieval problem rather than a prompting one — once the labelled sample confirms the signal.

### Example 15.3 — Multi-hop with explicit hop tracking (research)

```
<sources>{numbered_chunks}</sources>

Question: {multi_hop_question}

Answer in this form, with one HOP line per step the
question needs, numbered from 1, then a final ANSWER line:
  HOP <k>: <what you needed to find> -> <finding> [n]
  ANSWER: <final answer>

- If a hop cannot be completed from the sources, write
  "HOP <k>: UNSUPPORTED" and then "ANSWER: NOT IN SOURCES".
  Stop there. This applies to the first hop too.
- Do not bridge a gap with background knowledge, even an
  obvious one.
```

*Shows:* steps 3, 5, 6. Multi-hop is where RAG fails most quietly, because the bridge is usually plausible.

*Check:* each hop’s citation independently. A correct final answer reached through an uncited hop is a coin flip that happened to land right.

### Example 15.4 — Conflicting-sources handling (policy research)

```
<sources>{numbered_chunks}</sources>

Question: {question}

Answer only from the sources. If they do not address the
question, reply exactly "NOT IN SOURCES" and nothing else.

Before answering, scan the sources for disagreement.

If any two sources give different answers to the question:
  CONFLICT: yes
  POSITION A: <statement> [source n]
  POSITION B: <statement> [source m]
  DIFFERENCE: <what the sources actually disagree about>
  then stop. Do not synthesize.

If they agree:
  CONFLICT: no
  ANSWER: <answer with citations>
```

*Shows:* steps 3, 5, 6, 8, with step 8 as the primary structure rather than a footnote.

*Check:* every CONFLICT: no answer on a topic you know is contested. Silent synthesis of conflicting sources is the failure this prompt exists to catch.

### Example 15.5 — Freshness-aware answering (operations documentation)

```
<sources>
[1] (updated {date_1}) {chunk_1}
[2] (updated {date_2}) {chunk_2}
</sources>

Question: {question}

- Answer only from the sources.
- After the answer, add one line per source you used:
  "BASED ON: source [<n>], updated <date>".
- If sources of different ages disagree, present both with
  their numbers and update dates, and say they disagree. Do
  not choose between them.

AFTER THE CALL (code, not the model): if a source named in
BASED ON is more than 12 months old, append "STALE: this
source is <months> months old; verify before acting."
```

*Shows:* steps 3, 5, 8, with a freshness dimension.

*Check:* the STALE flags are a documentation backlog. Route them somewhere a human reads.

## 16. ReAct

**What it does and when to reach for it.** ReAct interleaves reasoning with tool calls in a single trajectory: think, act, observe, repeat. Reach for it when the task needs information the model cannot have — live data, private records, computation — and when the next action depends on what the last one returned. Note the honest scope: with PaLM-540B, ReAct’s exact match on HotpotQA was *below* CoT (27.4 versus 29.4); it beat CoT on FEVER (60.9 versus 56.3) and beat imitation- and reinforcement-learning baselines by 34 percentage points of absolute success rate on ALFWorld and 10 on WebShop. ReAct is for *acting*, not for thinking harder.

**Build steps.**

1. **Define a small tool set with typed arguments.** Every extra tool is another thing to choose wrong.
2. **Specify the Thought / Action / Observation format exactly,** and parse it in code.
3. **Never let the model write an Observation.** The system fills those. A model that writes its own observations is hallucinating with extra steps.
4. **Cap the loop** — maximum actions and wall-clock time.
5. **Define tool error handling in the prompt:** what the model must do when a call fails.
6. **Give tools least privilege.** Read-only by default; one write tool at most, called once.
7. **Define an explicit give-up output** so an exhausted loop returns something parseable.

**Combines with.** ReWOO when the plan is predictable and you want fewer calls. Reflexion (§17) when there is a success signal to retry against. Schema-constrained generation (§18) on the final answer.

### Example 16.1 — Two-tool record lookup (internal data)

```
Answer the question using the tools. Follow this format
exactly, one block at a time, and stop after "Finish:".
Thought: <your reasoning>
Action: search[<query>]  OR  lookup[<record_id>]
Observation: <filled in by the system — never write this>
... (repeat, at most 6 actions)
Thought: <final reasoning>
Finish: <answer>

Tools:
  search[query]      -> up to 5 record IDs with titles
  lookup[record_id]  -> the full record

Rules:
- If a tool returns an error, your next Thought must state
  the error and choose a different action.
- If you cannot answer within 6 actions, Finish with
  "INSUFFICIENT: <what was missing>".

Question: {question}
```

*Shows:* steps 1–5, 7.

*Check:* parse the transcript and assert every Observation came from your system. A model-authored Observation is the single most dangerous ReAct failure.

### Example 16.2 — Calculation agent with a computation tool (finance)

```
Answer the question using the tools. Follow this format
exactly, one block at a time, and stop after "Finish:".
Thought: <your reasoning>
Action: fetch_rate[<currency_pair>, <date>]  OR  calc[<python_expression>]
Observation: <filled in by the system — never write this>
... (repeat, at most 8 actions)
Thought: <final reasoning>
Finish: <answer>

Tools:
  fetch_rate[currency_pair, date] -> decimal
  calc[python_expression]         -> numeric result

Rules:
- Never do arithmetic inside a Thought. Use calc for every
  computation, including simple ones.
- Round only in the final Finish line, and state how many
  decimals you rounded to.
- If fetch_rate errors, Finish with
  "RATE UNAVAILABLE: <pair> <date>". Do not substitute a
  remembered or approximate rate.

Question: {question}
```

*Shows:* steps 1, 2, 5, 7. Forbidding Thought-arithmetic is what makes the trajectory auditable.

*Check:* scan Thoughts for digits and operators. Any arithmetic there bypassed the tool and is untrustworthy.

### Example 16.3 — Runbook triage agent (site reliability)

```
Triage the alert using the tools. Follow this format
exactly, one block at a time, and stop after "Finish:".
Thought: <your reasoning>
Action: read_status[<service>]  OR  read_log[<service>, <lines>]  OR  page_oncall[<service>, <msg>]
Observation: <filled in by the system — never write this>
... (repeat, at most 12 actions)
Thought: <final reasoning>
Finish: <result>

Tools:
  read_status[service]      -> current status string
  read_log[service, lines]  -> last N log lines
  page_oncall[service, msg] -> confirmation string
Rules:
- Gather evidence before acting. Do not call page_oncall
  until you have called both read_status and read_log.
- page_oncall is the only action with an external effect.
  Call it at most once, ever.
- Finish with: the service, the observed symptom, the exact
  log line you relied on in quotes, and whether you paged.
- If nothing looks wrong, Finish with "NO ACTION" and say
  what you checked.

Alert to triage: {alert}
```

*Shows:* steps 1, 4–7. The ordering rule and the single-call limit are the safety design.

*Check:* enforce the “at most once” in code, not in the prompt. A prompt rule is a preference; a code check is a guarantee.

### Example 16.4 — Fact verification against a source tool (editorial)

```
Check one claim using the tools. Follow this format
exactly, one block at a time, and stop after "Finish:".
Thought: <your reasoning>
Action: search_archive[<query>]  OR  get_article[<id>]
Observation: <filled in by the system — never write this>
... (repeat, at most 10 actions)
Thought: <final reasoning>
Finish: <verdict line>

Tools:
  search_archive[query] -> up to 5 article snippets with dates
  get_article[id]       -> full text

Task: Determine whether the claim below is SUPPORTED,
CONTRADICTED, or NOT FOUND.

Rules:
- NOT FOUND is a valid and common answer. Do not stretch a
  partially related source into SUPPORTED.
- Finish with one line:
  CLAIM: <verdict> | <article id or NONE> | <quoted sentence
  or NONE>
- If you reach 10 actions without a verdict, Finish with
  "CLAIM: UNRESOLVED | NONE | NONE".

Claim: {claim}
```

*Shows:* steps 1, 2, 4, 7. Run it once per claim, in code: in a single trajectory the model sees every earlier claim’s results, so only separate runs keep the verdicts independent. The task resembles FEVER-style verification, where ReAct beat CoT in the paper (PaLM-540B); run your own comparison.

*Check:* the quoted sentence for every SUPPORTED verdict. Verdicts without quotes are assertions.

### Example 16.5 — Booking-style flow with a confirmation gate (travel operations)

```
Find an option that meets the criteria using the tools.
Follow this format exactly, one block at a time, and stop
after "Finish:".
Thought: <your reasoning>
Action: search_options[<criteria>]  OR  get_details[<option_id>]  OR  hold[<option_id>]
Observation: <filled in by the system — never write this>
... (repeat, at most 10 actions)
Thought: <final reasoning>
Finish: <result>

Tools:
  search_options[criteria] -> list of options with IDs
  get_details[option_id]   -> full terms
  hold[option_id]          -> hold reference (expires 30 min)

Rules:
- Never call hold until you have called get_details on that
  exact option_id in a previous action.
- Call hold at most once.
- Before the hold, your Thought must state the total cost and
  the cancellation terms you read from get_details.
- Finish with: the held option, the hold reference, the total
  cost, and the cancellation deadline.
- If no option meets the criteria, Finish with
  "NO MATCH: <which criterion could not be met>".

Criteria: {criteria}
```

*Shows:* steps 1, 5–7. The “must have called get_details first” rule is a sequencing guard against acting on a summary.

*Check:* enforce the sequencing in code. Then have a human confirm before the hold becomes a booking — a 30-minute hold is a reversible action, and that is why this flow stops there.

## 17. Reflexion

**What it does and when to reach for it.** Reflexion retries a failed task with a written reflection on why the previous attempt failed, accumulated in memory. It reported HumanEval pass@1 of 91% against a cited GPT-4 baseline of 80%. The critical condition: it works when there is an **external** success signal — tests, a validator, an environment. Without one it degenerates into self-critique, which Huang et al. (arXiv 2310.01798) show can degrade performance. Reach for it only when you can automatically tell whether the attempt succeeded.

**Build steps.**

1. **Establish the external check first.** If you cannot write it, do not use this technique.
2. **Attempt the task** with whatever prompt you already have.
3. **Run the external check in code** and capture its concrete output — failing tests, validator errors, environment feedback.
4. **Reflect in a separate call:** given the failure output, name the specific wrong assumption. Forbid rewriting the solution in this step.
5. **Accumulate reflections** and pass all of them into the retry.
6. **Cap retries at 2 or 3,** and stop early if the external signal stops improving.
7. **Escalate on exhaustion** with the last attempt and the full reflection history attached.

**Combines with.** Program-of-Thoughts (§13) — execution is a free external signal. Evaluator-optimizer (§26) is the same loop with a model as the checker, which is weaker. Conflicts with tasks that have no automatic success criterion.

### Example 17.1 — Code against a test harness (software)

```
ATTEMPT:
  Implement the function to satisfy the docstring.
  {function_signature_and_docstring}

EXTERNAL CHECK (code, not the model): run the unit tests.

REFLECT (only on failure, separate call):
  The function to implement:
  {function_signature_and_docstring}
  Your implementation:
  {previous_attempt}
  It failed these tests:
  {failing_test_output}
  In 2-4 sentences: name the specific assumption in your
  implementation that was wrong, and what to do differently.
  Do not write any code in this step.

RETRY:
  Implement the function to satisfy the docstring.
  {function_signature_and_docstring}
  Previous attempts and reflections:
  {reflection_memory}
  Now reimplement the function.

Stop when tests pass or after 3 retries.
```

*Shows:* steps 1–7.

*Check:* read the reflections when a run exhausts its retries. Repeated identical reflections may mean the retry is ignoring the reflection, or that the model cannot act on its own diagnosis; compare each retry with the reflection before it, then escalate rather than adding retries.

### Example 17.2 — Extraction against a schema validator (operations)

```
ATTEMPT:
  Extract the requested fields from the text as JSON that
  matches the schema.
  Schema: {schema}
  Text: {source_text}

EXTERNAL CHECK: jsonschema validation in code.

REFLECT on validation errors:
  Schema: {schema}
  Your output:
  {previous_output}
  It failed schema validation:
  {validator_errors}

  Name the field-level mistake and which rule in the schema
  you misread. Do not output corrected JSON in this step.

RETRY: the ATTEMPT prompt again, followed by:
  Reflections so far:
  {reflection_memory}
Maximum 2 retries, then escalate to a human with the last
output and every reflection.
```

*Shows:* steps 1–7. Schema validation is the cheapest external signal available.

*Check:* if the same field fails repeatedly across tasks, the schema is ambiguous. Fix the schema rather than looping.

### Example 17.3 — SQL against a read-only replica (analytics)

```
ATTEMPT:
  Write SQL for the question.
  Schema: {schema}
  Question: {question}

EXTERNAL CHECK (code): run EXPLAIN; execute against a
read-only replica; compare row count and column names to
{expected_shape}, the shape you wrote down for this question.

REFLECT:
  Schema: {schema}
  Question: {question}
  Your query:
  {previous_query}
  It returned {n} rows with columns {cols}.
  The expected shape is {expected_shape}.
  State which join or filter produced the mismatch. Do not
  write SQL in this step.

RETRY: the ATTEMPT prompt again, followed by:
  Previous queries and reflections:
  {reflection_memory}
After the third attempt, return the query with a warning
rather than a result.
```

*Shows:* steps 1, 3, 4, 6, 7. Shape comparison is a weak but real external signal when you have no ground truth.

*Check:* returning a warned query rather than a wrong number is the correct terminal behavior. Make sure the warning survives into whatever renders the result.

### Example 17.4 — Document generation against a checklist validator (compliance)

```
ATTEMPT:
  Draft the document from the inputs.
  Inputs: {inputs}
  Required section headings: {required_headings}
  Required disclosure strings, to appear verbatim:
  {required_disclosures}
  Phrases that must not appear: {forbidden_phrases}

EXTERNAL CHECK (code): assert every required section heading
is present; assert every required disclosure string appears
verbatim; assert no forbidden phrase appears.

REFLECT:
  Your draft:
  {previous_draft}
  It failed these checks:
  {failed_assertions}

  For each failure, say whether you omitted the item, worded
  it differently, or judged it not applicable. Do not redraft
  in this step.

RETRY: the ATTEMPT prompt again, followed by:
  Reflections so far:
  {reflection_memory}
Maximum 2 retries.
```

*Shows:* steps 1, 3, 4. The three-way reflection — omitted, reworded, judged inapplicable — distinguishes a slip from a disagreement.

*Check:* “judged it not applicable” answers. Those are the ones a human must review; the other two are mechanical.

### Example 17.5 — Agent task against an environment signal (workflow automation)

```
ATTEMPT:
  Complete the task in the environment using the available
  actions.
  Task: {task}

EXTERNAL CHECK: the environment's own success flag plus the
final state.

REFLECT:
  Task: {task}
  The task did not complete. Final state: {final_state}
  Goal state: {goal_state}
  Actions you took: {action_trace}

  Identify the earliest action after which the state diverged
  from what you expected, and say what you expected it to do.
  Do not plan a new attempt in this step.

RETRY: the ATTEMPT prompt again, followed by:
  Reflections so far:
  {reflection_memory}
Maximum 3 attempts, then stop and report the reflection
history.
```

*Shows:* steps 1–7. “Earliest divergence” is the right question — later errors are usually consequences.

*Check:* whether the identified divergence point is actually the earliest. Models tend to blame the last action before failure, which is rarely the cause.

# Part 5 — Verification Techniques

## 18. Schema-Constrained Generation

**What it does and when to reach for it.** Constrained decoding masks the token distribution so only outputs permitted by a grammar or schema can be sampled — the output *cannot* violate the schema or grammar the decoder enforces, except in cases the vendors document: Anthropic lists a refusal and an answer cut off at `max_tokens`, and OpenAI documents refusals, so check for those before parsing (post-edition note). On OpenAI’s own evaluation of complex JSON-schema following (August 2024), gpt-4o-2024-08-06 with constrained decoding scored 100%, against under 40% for gpt-4-0613. Serving stacks differ in which schema keywords they enforce, and the examples below use `pattern`, `maxLength`, `minItems` and `uniqueItems`, so check your provider’s current documentation and validate those keywords in code. The manual files it under decoding (Axis 4, Section 10.5) because it acts inside the decoder; it sits in this Part because its purpose is a format guarantee. Reach for it any time a downstream system parses the output. It replaces a request with a guarantee. It guarantees *form*, never *truth*.

**Build steps.**

1. **Write the schema in code,** as the contract. The prompt describes the task; the schema defines the output.
2. **Enable constrained decoding in the serving stack.** Putting a schema in the prompt text is not this technique.
3. **Include a legal way to express absence** — nullable types, an `UNKNOWN` enum member, an “unreadable fields” array. Without one, the grammar forces a fabrication.
4. **Set** `additionalProperties: false` so extra invented fields are impossible.
5. **Add an evidence field** — a quoted span or source index — so the structured output stays checkable.
6. **Validate semantically after parsing,** and check in code any schema keyword your stack does not enforce. Schema-valid and correct are different properties.
7. **Test whether the constraint hurts reasoning on your task.** Tam et al. (arXiv 2408.02442) report format constraints can degrade reasoning; the dottxt rebuttal disputes the cause. It is unsettled — measure it.

**Combines with.** Anything whose output is consumed by software. Replaces the format half of most system prompts (§3). Pairs with an LLM judge (§20) for the semantic half.

### Example 18.1 — Invoice extraction with absence built in (accounts payable)

```
{
"type": "object",
"required": ["vendor", "invoice_total_cents", "invoice_date", "confidence", "unreadable_fields"],
"properties": {
"vendor": {"type": ["string", "null"]},
"invoice_total_cents": {"type": ["integer", "null"]},
"invoice_date": {"type": ["string", "null"],
"pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
"confidence": {"enum": ["high", "low"]},
"unreadable_fields": {"type": "array",
"items": {"type": "string"}}
},
"additionalProperties": false
}
```

*Shows:* steps 1, 3, 4. The nulls and `unreadable_fields` give a blurry scan somewhere to go other than a plausible invented number. Making `unreadable_fields` required means a missing key cannot be read as “nothing was unreadable.”

*Check:* route every `confidence: low` and every non-empty `unreadable_fields` to human review. That is the whole point of including them.

### Example 18.2 — Classification with mandatory evidence (customer support)

```
{
"type": "object",
"required": ["label", "evidence_span"],
"properties": {
"label": {"enum": ["BILLING","BUG","FEATURE","ACCESS","OTHER"]},
"evidence_span": {"type": "string", "maxLength": 200},
"secondary_label": {
"enum": ["BILLING","BUG","FEATURE","ACCESS","OTHER", null]
}
},
"additionalProperties": false
}
```

*Shows:* steps 1, 3–5. `secondary_label` handles the genuinely dual-category case that a single enum would force into a coin flip.

*Check:* assert `evidence_span` appears verbatim in the source text. A span that does not match is a fabricated justification for a possibly correct label.

### Example 18.3 — Grammar for a restricted command language (robotics-adjacent control)

```
root    ::= command+
command ::= move | pick | place | wait | noop
move    ::= "MOVE(" int "," int ")\n"
pick    ::= "PICK(" name ")\n"
place   ::= "PLACE(" name "," name ")\n"
wait    ::= "WAIT(" int ")\n"
noop    ::= "NOOP\n"
int     ::= [0-9]+
name    ::= [a-z_]+
```

*Shows:* steps 1–3. The model cannot emit a verb outside this set, so the executor never parses something it does not implement, and `NOOP` gives it a legal way to say there is nothing to do.

*Check:* the grammar guarantees syntax, not safety. Validate coordinate ranges and object names against the real environment before executing anything.

### Example 18.4 — Graded assessment output (education)

```
{
"type": "object",
"required": ["score", "rubric_hits", "evidence"],
"properties": {
"score": {"type": "integer", "minimum": 0, "maximum": 4},
"rubric_hits": {
"type": "array",
"items": {"enum": ["thesis","evidence","structure","mechanics"]},
"uniqueItems": true
},
"evidence": {
"type": "array",
"minItems": 1,
"items": {
"type": "object",
"required": ["criterion", "quote"],
"properties": {
"criterion": {"enum": ["thesis","evidence","structure","mechanics"]},
"quote": {"type": "string", "maxLength": 300}
},
"additionalProperties": false
}
}
},
"additionalProperties": false
}
```

*Shows:* steps 1, 4, 5. `minItems: 1` forces a non-empty evidence list, so a score cannot arrive with no evidence at all. It does not make an entry true or relevant, and it does not tie the evidence to `rubric_hits` (see the check below). If your stack does not enforce `minItems`, `uniqueItems` or `maxLength`, validate them in code.

*Check:* every quote against the student’s text, and every `criterion` in evidence against `rubric_hits`. A hit with no matching evidence entry is a scoring error.

### Example 18.5 — Risk register entry with a forced uncertainty field (project governance)

```
{
"type": "object",
"required": ["risk", "likelihood", "impact", "basis", "would_change_my_mind"],
"properties": {
"risk": {"type": "string", "maxLength": 200},
"likelihood": {"enum": ["low","medium","high","insufficient_information"]},
"impact": {"enum": ["low","medium","high","insufficient_information"]},
"basis": {"type": "string", "maxLength": 400},
"would_change_my_mind": {"type": "string", "maxLength": 200}
},
"additionalProperties": false
}
```

*Shows:* steps 1, 3–5. Two design choices matter: `insufficient_information` as a first-class rating, and a required field naming the evidence that would reverse the assessment.

*Check:* read `would_change_my_mind` before `likelihood`. If the reversal condition is vague or already known to be false, the rating is not grounded in anything.

## 19. Chain-of-Verification

**What it does and when to reach for it.** Chain-of-Verification drafts an answer, generates verification questions about its own claims, answers those questions **in a fresh context that does not contain the draft**, and revises. Reach for it on long-form factual output where errors are plausible-sounding rather than obvious. The independence of the answering step is the entire technique: answer the verification questions with the draft in context and you get self-agreement, which is worth nothing.

**Build steps.**

1. **Draft normally.**
2. **Generate verification questions** from the draft — one standalone question per factual claim. Forbid answering them in this call.
3. **Answer them in a fresh context.** Do not pass the draft. This is the step that gets implemented wrong.
4. **Keep the questions atomic.** A compound question gets a compound answer that verifies nothing.
5. **Revise against the answers,** removing any claim the verification cannot support.
6. **Require a removals list** so you can see what the process caught.
7. **Where sources exist, answer the verification questions against the sources,** not from memory.

**Combines with.** RAG (§15) for step 7, which is the strong version. Context anchoring (§4). Conflicts with latency budgets — this is four calls.

### Example 19.1 — Four-call CoVe for a factual brief (research)

```
CALL 1 — DRAFT:
  {question}

CALL 2 — PLAN (draft in context):
  Draft: {draft}

  List every factual claim in the draft as a standalone
  verification question — one that could be answered by
  someone who has not read the draft. One per line.
  Do not answer them.

CALL 3 — ANSWER (fresh context; the draft is NOT included):
  Answer each question independently and briefly. If you are
  not confident, say "UNCERTAIN" rather than guessing.
  {questions}

CALL 4 — REVISE:
  Draft: {draft}
  Verification Q&A: {qa_pairs}

  Rewrite the draft to be consistent with the verification
  answers. Remove any claim the verification contradicts or
  marks UNCERTAIN. List what you removed under "REMOVED:".
```

*Shows:* steps 1–6.

*Check:* assert in code that call 3’s payload does not contain the draft text. This is the implementation bug that silently disables the technique.

### Example 19.2 — Entity list verification (competitive research)

```
CALL 1: List the companies that {criteria}.

CALL 2: Companies: {companies}
  For each company, write the standalone question
  "Does <company> meet {criteria}?" One per line. Do not
  answer them.

CALL 3 (fresh context, with sources):
  <sources>{retrieved_chunks}</sources>
  Answer each question YES, NO, or NOT IN SOURCES, with the
  quoted sentence that supports it.
  {questions}

CALL 4: Companies: {companies}
  Answers: {answers}
  Return the final list containing only companies that got
  YES with a quote. Under "DROPPED:", list each company
  removed and why.
```

*Shows:* steps 2–7. List generation is where CoVe helps most — models pad lists to a satisfying length.

*Check:* the DROPPED list length. A long DROPPED list tells you the draft alone was not usable.

### Example 19.3 — Numerical claims in a summary (financial writing)

```
CALL 1: Summarize the report in five bullets.
  <report>{report}</report>

CALL 2: Summary: {summary}
  For every number in the summary, write a standalone
  question of the form "According to the report, what is
  <quantity>?" One per line. Do not answer.

CALL 3 (fresh context, report attached, summary NOT attached):
  <report>{report}</report>
  Answer each question with the exact figure from the report,
  or "NOT STATED".
  {questions}

CALL 4: Summary: {summary}
  Verification answers: {answers}
  Correct every number in the summary to match the
  verification answers. Remove any bullet whose number came
  back NOT STATED. List corrections as
  "WAS <x> NOW <y>".
```

*Shows:* steps 3, 4, 7. Numbers are the ideal CoVe target — atomic, checkable, and high-cost when wrong.

*Check:* the WAS/NOW list. Any correction means your draft-only pipeline was shipping wrong numbers.

### Example 19.4 — Procedural instructions (technical documentation)

```
CALL 1: Write the setup instructions for {task}.

CALL 2: Instructions: {instructions}
  For each step, write two standalone questions: "Is <action>
  required?" and "Does <action> come before <next_action>?"
  Skip the second question for the last step. One per line.

CALL 3 (fresh context, with the official documentation):
  <docs>{official_docs}</docs>
  Answer each question from the documentation only. If the
  documentation does not address it, say "NOT DOCUMENTED".
  {questions}

CALL 4: Instructions: {instructions}
  Verification answers: {answers}
  Revise the instructions. Mark any step with a NOT DOCUMENTED
  answer with "[unverified]" inline rather than removing it,
  and list those steps at the end.
```

*Shows:* steps 2–7, with a softer revision rule — undocumented is not the same as wrong.

*Check:* the `[unverified]` steps are your documentation gaps. Do not ship instructions where a destructive step carries that marker.

### Example 19.5 — Attribution verification (journalism-adjacent)

```
CALL 1: Write the summary of what each party said.
  <transcript>{transcript}</transcript>

CALL 2: Summary: {summary}
  For each attributed statement, write the question
  "Did <person> say <statement>?" One per line.

CALL 3 (fresh context, transcript attached, summary NOT attached):
  <transcript>{transcript}</transcript>
  For each question answer YES with the exact quote, NO, or
  "SAID BY SOMEONE ELSE: <name>".
  {questions}

CALL 4: Summary: {summary}
  Verification answers: {answers}
  Correct the attributions. Remove any statement that
  came back NO. For "SAID BY SOMEONE ELSE", reattribute and
  note the correction under "REATTRIBUTED:".
```

*Shows:* steps 2–7. Misattribution is a distinct failure from fabrication and needs its own verification verdict.

*Check:* the REATTRIBUTED list. A correct quote on the wrong person is the error most likely to survive casual review and do the most damage.

## 20. LLM-as-a-Judge

**What it does and when to reach for it.** An LLM judge scores outputs against criteria so you can evaluate at volume. In Zheng et al. (arXiv 2306.05685), GPT-4 as a judge reached over 80% agreement with human preferences on MT-Bench and Chatbot Arena (2023), the same level as agreement between humans, but judges also show position bias, verbosity bias, and self-enhancement bias, and LLM evaluators favor their own generations (Panickssery et al., arXiv 2404.13076). Reach for it to compare candidate prompts or monitor production quality. Treat it as a noisy instrument, never as ground truth.

**Build steps.**

1. **Use a different model family than the one that generated the output.** Self-preference is measured, not hypothetical.
2. **Randomize position** and run each comparison twice with the order swapped. If the winner flips, record a tie.
3. **State criteria in priority order,** and say explicitly that length is not a criterion.
4. **Require a per-criterion reason,** not a single number.
5. **Calibrate against human labels** on 50 examples before trusting the judge at scale.
6. **Re-calibrate whenever you change the judge model.**
7. **Never let a model judge its own output** in a production loop.

**Combines with.** Evaluation-driven development (§28 and manual Chapter 21). Evaluator-optimizer (§26) is this in a loop. Conflicts with self-refine, which is the same idea without the independence that makes it work.

### Example 20.1 — Pairwise comparison with bias controls (prompt evaluation)

```
You are evaluating two responses to the same task. They are
in random order; you do not know which system produced either.

Task: {task}
Response A: {a}
Response B: {b}

Judge on these criteria, in this order of importance:
1. Factual support — is every claim backed by the task's
   source material?
2. Instruction compliance — were all stated constraints met?
3. Clarity for the stated audience.

Rules:
- Length is not a criterion. A shorter response that meets
  the criteria wins.
- Judge only the criteria listed. Do not reward style you
  happen to prefer.
- If they are equivalent on all three, say TIE.

Output:
  WINNER: A | B | TIE
  REASON: one sentence per criterion
```

*Shows:* steps 1–4.

*Check:* run each pair three times: in the original order, in the original order again, and with A and B swapped. If the repeat agrees but the swapped run flips, suspect position bias; if the repeat itself flips, you are seeing sampling noise. Record TIE for any flip and count how often it happens — that rate is your judge’s noise floor.

### Example 20.2 — Rubric scoring with anchored levels (content quality)

```
Score the response against the rubric. For each criterion,
give the level and quote the text that put it there.

Criterion: Grounding
  4 — every claim cites a provided source
  3 — most claims cited; uncited claims are uncontroversial
  2 — some claims cited; at least one uncited factual claim
  1 — no citations

Criterion: Compliance
  4 — every stated constraint met
  3 — one minor constraint missed
  2 — a substantive constraint missed
  1 — the response ignores the format

Output per criterion:
  <criterion>: <level> | QUOTE: "<text>" | WHY: <one sentence>

Do not average the levels into an overall score.

Response: {response}
Task and sources: {task_and_sources}
```

*Shows:* steps 3, 4. Anchored levels with quotes are a rule-of-thumb improvement on a bare 1–10 scale, not a measured result.

*Check:* agreement with human scores on a 50-example calibration set, per criterion. An overall average hides a criterion the judge cannot score.

### Example 20.3 — Binary safety gate (production monitoring)

```
Does the response below violate any of these rules?

R1: States a fact not present in the provided sources.
R2: Gives specific advice in a regulated domain (medical,
    legal, financial) rather than general information.
R3: Claims certainty about a future outcome.

For each rule: PASS or FAIL, and if FAIL, the exact sentence
that violates it.

Then: OVERALL: PASS (all three pass) or FAIL (any fails).

Sources: {sources}
Response: {response}
```

*Shows:* steps 3, 4. Binary per-rule gates are easier to audit than a holistic safety score, because each FAIL comes with the sentence that triggered it.

*Check:* the false-positive rate on known-good responses. A gate that flags a lot of good output tends to be switched off, which is worse than no gate.

### Example 20.4 — Reference-free factuality check (summarization monitoring)

```
<source>{source_document}</source>
<summary>{summary}</summary>
For each sentence in the summary, classify it:
  SUPPORTED    — a sentence in the source states this
  INFERABLE    — follows from the source but is not stated
  UNSUPPORTED  — not derivable from the source
  CONTRADICTED — the source states otherwise

For SUPPORTED and CONTRADICTED, quote the source sentence.

Then: UNSUPPORTED COUNT: <n>, CONTRADICTED COUNT: <n>

Do not judge whether the summary is good. Judge only whether
each sentence is grounded.
```

*Shows:* steps 3, 4. Separating INFERABLE from SUPPORTED makes the judge say whether the source states a claim or only allows it.

*Check:* the INFERABLE bucket by hand on a sample. It is where the judge’s own reasoning enters, and where its errors concentrate.

### Example 20.5 — Judge calibration harness (evaluation infrastructure)

```
Run before trusting any judge prompt at scale.

1. Sample 50 outputs spanning the quality range, including
   10 you know are bad and 10 you know are good.
2. Have two humans label each independently against the same
   criteria the judge uses. Record human-human agreement.
3. Run the judge on all 50, twice, with positions swapped.
4. Report:
     judge-human agreement
     human-human agreement
     judge self-agreement across the two orderings
5. Accept the judge only if judge-human agreement is close to
   human-human agreement AND self-agreement is high.
6. Repeat steps 1–5 whenever you change the judge model.

A judge whose self-agreement is low is measuring position or
noise, not quality — fix the prompt before comparing it to
humans.
```

*Shows:* steps 2, 5, 6.

*Check:* treat human-human agreement as the practical benchmark: a judge is hard to trust beyond it. If two humans agree only 60% of the time, your criteria are probably ambiguous, and no judge will fix that.

## 21. The Disconfirmation Pass

**What it does and when to reach for it.** A disconfirmation pass assigns the model the job of arguing that a conclusion is wrong. It exists because “check this” invites agreement: sycophancy is a general property of preference-trained models (Sharma et al., arXiv 2310.13548), and unaided self-correction can degrade reasoning (Huang et al., arXiv 2310.01798). Reach for it before any consequential conclusion leaves your pipeline. It costs one extra call, and for decision support it is the first addition this guide recommends.

**Build steps.**

1. **Never ask “is this correct?”** Assign the opposing role outright.
2. **Forbid hedging and balance.** The pass has one job.
3. **Demand a specific objection,** not a category of concern.
4. **Ask for the one fact that would most damage the conclusion,** and whether the material rules it out.
5. **Run it in a fresh context** where possible, and on a different model family where it matters.
6. **Require a terminal verdict:** SURVIVES or DOES NOT SURVIVE.
7. **Feed the verdict back** — either revise, or attach the surviving objection to the output.

**Combines with.** Any reasoning topology, as a final gate. Risk analysis (manual Section 20.5), where the manual recommends it. Chain-of-Verification (§19) checks facts; this checks inference.

### Example 21.1 — Generic conclusion attack (decision support)

```
Below is a conclusion and the reasoning behind it.

{conclusion_and_reasoning}

Your task is to argue that this conclusion is WRONG. Do not
defend it. Do not hedge. Do not present both sides.

1. State the strongest specific objection.
2. Name the single piece of evidence that, if true, would
   most damage the conclusion — and say whether the material
   provided actually rules it out.
3. Identify any step where a plausible alternative reading
   leads somewhere else.
4. End with: SURVIVES or DOES NOT SURVIVE — whether the
   conclusion stands after your strongest attack.
```

*Shows:* steps 1–4, 6.

*Check:* a DOES NOT SURVIVE verdict with a vague objection is theater. Require the objection to name a specific claim or step.

### Example 21.2 — Risk-assessment disconfirmation (project governance)

```
Below is a risk assessment.

{risk_assessment}

Two passes. Do both.

PASS A — argue the risks are overstated. For each risk, give
the strongest reason it is less likely or less severe than
assessed. Name the assumption that inflates it.

PASS B — argue the assessment missed something. Name one risk
that is not on the list and should be, and the specific
condition under which it would materialize.

End with:
  OVERSTATED: <which risks, if any>
  MISSING: <which risks, if any>
```

*Shows:* steps 1 and 3; it ends with two lists, not a SURVIVES verdict. The two passes echo the manual’s Risk-Mapper architecture (Section 20.5), which follows its disconfirmation pass with an opportunity pass; here Pass B hunts for missed risks instead.

*Check:* Pass B is the valuable half. If MISSING is empty on a real project, prompt again with a category hint — vendor, regulatory, staffing, dependency.

### Example 21.3 — Data-analysis confound hunt (analytics)

```
Below is a finding and the analysis that produced it.

{finding_and_method}

Argue that this finding is an artifact, not a real effect.

1. Name the most likely confound and how it would produce
   exactly this pattern.
2. Name a selection or survivorship effect in how the data
   was collected that could produce it.
3. State what the result would look like if the effect were
   real but half the size — and whether the analysis could
   tell that apart from the reported result.
4. End with: ARTIFACT PLAUSIBLE or EFFECT LIKELY REAL.
```

*Shows:* steps 1, 3, 6. Item 3 is a power question disguised as a disconfirmation prompt.

*Check:* whether the named confound is actually measurable in your data. If it is, measure it before publishing the finding.

### Example 21.4 — Recommendation stress test (strategy)

```
Below is a recommendation.

{recommendation}

Argue against adopting it.

1. Under what specific conditions does this recommendation
   make things worse than doing nothing?
2. What does it assume about {the organization / the market /
   the timeline} that may not hold?
3. Who bears the cost if it fails, and is that the same party
   making the decision?
4. What would the person who most disagrees with this say,
   in their strongest form, not a caricature?
5. End with: ADOPT ANYWAY or RECONSIDER, and the single
   condition that decides it.
```

*Shows:* steps 1, 3, 4, 6. Item 3 catches misaligned incentives that pure reasoning passes miss.

*Check:* item 4. A weak version of the opposing view means the model is still on your side, and the pass has failed.

### Example 21.5 — Independent-model disconfirmation (high-stakes review)

*Setup:* run this on a different model family than the one that produced the conclusion, and leave out the original reasoning.

```
Conclusion: {conclusion_only}
Evidence available: {evidence}

You did not write this conclusion and have no stake in it.

1. Reason independently from the evidence to your own
   conclusion. Do this before evaluating theirs.
2. State where yours differs from the one above.
3. If they agree, say what evidence you would both be
   missing that would make you both wrong.
4. End with: AGREE, DISAGREE, or AGREE BUT FRAGILE, and one
   sentence on why.
```

*Shows:* steps 1, 5, 6. Reasoning first, comparing second, reduces anchoring on the given conclusion; the independence comes from leaving out the original reasoning and changing model family.

*Check:* read AGREE BUT FRAGILE first — two independent paths reaching the same place on a shared blind spot. Treat it as a request for evidence, not a confirmation.

# Part 6 — Orchestration Patterns

## 22. Prompt Chaining

**What it does and when to reach for it.** Prompt chaining breaks a task into sequential calls, each doing one thing, with gates between them. Reach for it when a single call produces output that is right in parts and wrong in others, when different steps need different models, or when you need an inspectable intermediate. The gain is not intelligence — it is that each step is simple enough to verify.

**Build steps.**

1. **Split at the point where the output type changes.** Extraction, then drafting, then formatting — not three vague “passes.”
2. **Make each step’s output machine-parseable,** even if a human will never read it.
3. **Put a gate after every step.** Parse, validate, assert the invariant that matters.
4. **Define what happens when a gate fails:** retry, escalate, or stop. Never “continue anyway.”
5. **Carry forward only what the next step needs.** Passing the whole history reintroduces the confusion you split to avoid.
6. **Assert invariants across the seam** — the thing that must be true in both the input and the output of a step.

**Combines with.** Least-to-Most (§11) is a chain whose steps the model designed. Routing (§23) picks which chain to run. Evaluator-optimizer (§26) is a chain with a loop.

### Example 22.1 — Transcript to follow-up email (meetings)

```
CALL 1 — extract:
  From the transcript below, extract every commitment made,
  as JSON: [{"who": ..., "what": ..., "when": ... | null}]
  Return only JSON.

  Transcript: {transcript}

GATE (code): parse the JSON. If parsing fails, or any "who"
is empty, stop the chain and alert. Do not pass a malformed
object downstream.

CALL 2 — draft:
  Turn these commitments into a follow-up email.
  {validated_json}
  One line per commitment, grouped by owner. No commitment
  may appear that is not in the JSON.

GATE (code): assert every "what" string from the JSON appears
in the draft. Assert the draft contains no owner name absent
from the JSON.

CALL 3 — tone:
  Draft: {draft}
  Rewrite for a client audience. Do not add, remove, or
  change any commitment.

GATE (code): a tone rewrite rewords the lines, so do not
repeat the verbatim check. Run call 1 again, with the rewrite
in place of the transcript, and assert the same number of
commitments, with the same "who" and "when" for each. Spot-check the "what" fields by hand.
```

*Shows:* steps 1–4, 6. The same invariant is asserted twice, because the tone call is where commitments quietly get “improved” — the second time by re-extraction, since a tone rewrite changes the wording.

*Check:* the gate-2 and gate-3 failure rates separately. They fail for different reasons and tell you different things.

### Example 22.2 — Research note to structured brief (analysis)

```
CALL 1 — claims:
  Extract every factual claim from the notes as JSON:
  [{"claim": ..., "source": ... | null}]

  Notes: {notes}

GATE: assert every claim with a null source is flagged.

CALL 2 — verify (RAG, once per claim; code retrieves the chunks):
  Claim: {claim}
  Chunks: {retrieved_chunks}
  Mark the claim SUPPORTED, CONTRADICTED, or NOT FOUND with a
  cited chunk.

GATE: drop CONTRADICTED. Hold NOT FOUND in a separate list.

CALL 3 — write:
  Write the brief using only these SUPPORTED claims:
  {supported_claims}
  End with a section "UNVERIFIED — NOT INCLUDED" listing these
  NOT FOUND claims verbatim:
  {not_found_claims}

GATE: assert no CONTRADICTED claim text appears anywhere in
the output.
```

*Shows:* steps 1–4, 6. The chain’s value is that “contradicted” is removed by code, not by a model deciding to leave it out.

*Check:* the UNVERIFIED section. If it is long, your corpus does not cover your notes and the brief is thinner than it looks.

### Example 22.3 — Code change pipeline (software)

```
CALL 1 — plan:
  Issue: {issue}
  File: {file}
  Given the issue and the file, describe the change in 3-5
  numbered steps. Do not write code.

GATE (human or code): does the plan touch only the intended
file? Reject plans that expand scope.

CALL 2 — implement:
  Plan: {plan}
  File: {file}
  Produce the full modified file. No other changes.

GATE (code): run the diff. Assert it touches only the
intended file and stays under a changed-line limit set in
advance. Run the test suite.

CALL 3 — explain:
  Diff: {diff}
  Write the commit message: what changed and why, in the
  imperative mood, under 72 characters for the subject.

GATE (code): lint the commit message format.
```

*Shows:* steps 1–4. The plan gate is where scope creep dies cheaply.

*Check:* the diff against the plan, every time. The characteristic failure is a correct change plus three uninvited refactors.

### Example 22.4 — Document translation with terminology control (localization)

```
CALL 1 — extract terms:
  Source: {source}
  List every product name, legal term, and unit of measure
  in the source. Return JSON: [{"term": ..., "type": ...}]

GATE: join against the approved glossary. Any term not in
the glossary goes to a human before the chain continues.

CALL 2 — translate:
  Source: {source}
  Translate the source document into {target}. Render each of these
  source terms as its approved target string, exactly as
  given (source term -> target string):
  {glossary_mappings}

GATE (code): assert every glossary target string appears in
the translation the same number of times as its source
string appeared in the source.

CALL 3 — back-translate check:
  Translation: {translation}
  Translate this back into {source_language}, literally.

GATE (code + human): diff the back-translation against the
original. Flag any sentence whose meaning shifted.
```

*Shows:* steps 1–4, 6. The count assertion in gate 2 is stronger than “please keep the terms.”

*Check:* the back-translation diff is a weak signal that catches strong errors. Do not treat matching back-translation as proof of a good translation.

### Example 22.5 — Data-quality report (analytics operations)

```
CALL 1 — profile (Program-of-Thoughts, §13):
  Write Python that profiles the CSV at {csv_path}: row count,
  null rate per column, distinct count per column, min/max for
  numeric columns. print() each labeled.

GATE (code): execute. If it raises, stop — do not let a model
describe data it could not read.

CALL 2 — interpret:
  Profile output: {stdout}
  Identify the three most likely data-quality problems.
  For each, cite the specific profile number that indicates
  it. Do not speculate beyond the profile.

GATE (code): assert every cited number appears in the stdout.

CALL 3 — recommend:
  Problems: {problems}
  For each, give one concrete check to add to the pipeline,
  written as a Python assert statement.

GATE (code): parse the reply. Assert there is one check per
problem and that each parses as a Python assert statement.
```

*Shows:* steps 1–4, 6. Call 1 produces ground truth; call 2 is forbidden from going beyond it.

*Check:* gate 2 catches the most common failure in this chain — a plausible data-quality claim with an invented supporting number.

## 23. Routing

**What it does and when to reach for it.** Routing classifies the input and dispatches it to the handler best suited to it — a different prompt, model, tool set, or a human. Reach for it when your traffic is heterogeneous and a single prompt is being pulled in incompatible directions, or when cost matters and most requests are easy. When the easy requests are the majority, it is a low-effort first orchestration step: send them to a small model and the hard remainder to a reasoning model.

**Build steps.**

1. **Derive categories from real traffic,** not from imagination. Sample 200 requests and cluster them.
2. **Make the router output a closed enum,** and nothing else. Schema-constrain it (§18).
3. **Include a fallback class** and route it to a human or a general handler.
4. **Keep the router small and fast.** A router that costs as much as the handler defeats the purpose.
5. **Log the label distribution.** A class that never fires or one that absorbs everything means the taxonomy is wrong.
6. **Measure per-class quality, not just overall.** An average hides one class failing badly.
7. **Route on what the request needs, not on how it sounds.** Urgency in tone is not urgency in substance.

**Combines with.** Everything downstream. Pairs naturally with parallelization (§24) when a request needs two handlers.

### Example 23.1 — Support triage with cost-aware dispatch (customer operations)

```
ROUTER (small model, schema-constrained to the enum):
  Classify into exactly one:
  SIMPLE_FAQ, ACCOUNT_ACTION, TECHNICAL, DISPUTE, UNCLEAR
  Choose by what the customer needs, not by how upset they
  sound. DISPUTE means the customer needs a staff decision on
  a charge, a refund, or a policy exception.
  Return only the label.

  Message: {message}

DISPATCH (code):
  SIMPLE_FAQ     -> small model + FAQ retrieval
  ACCOUNT_ACTION -> tool-using agent (§16), least privilege
  TECHNICAL      -> reasoning model + docs retrieval
  DISPUTE        -> human queue, no model response
  UNCLEAR        -> clarifying question, then re-route once
LOG (code): count the labels per day.
```

*Shows:* steps 2–5, 7.

*Check:* per-class resolution rate. If TECHNICAL resolves at half the rate of the others, the problem is the handler, not the router.

### Example 23.2 — Difficulty routing for cost control (general assistant)

```
ROUTER (small model):
  Rate the request's difficulty:
  EASY     — single fact, single step, no ambiguity
  MEDIUM   — multiple steps or requires a document
  HARD     — multi-step reasoning, conflicting constraints,
             or consequences if wrong

  Return only the label. Judge the task, not the tone or
  length of the request.

  Request: {request}

DISPATCH:
  EASY   -> small model, zero-shot
  MEDIUM -> mid model + retrieval
  HARD   -> reasoning model + disconfirmation pass (§21)
```

*Shows:* steps 2, 4, 7. The “judge the task, not the tone” instruction targets the characteristic router error.

*Check:* sample EASY-routed requests and have a person label the right answers. Compare the small model’s accuracy on that sample with the reasoning model’s; a disagreement rate alone mixes routing errors with errors by either model. The accuracy gap is the number that justifies or kills the whole scheme.

### Example 23.3 — Language and locale routing (global product)

```
ROUTER:
  Return JSON only:
  {"language": "<ISO 639-1>" | "unknown",
   "needs_locale_expert": true|false}

  Use "unknown" if you cannot tell the language.
  Set needs_locale_expert true if the request involves legal,
  tax, medical, or regulatory content where the answer differs
  by jurisdiction.

  Request: {request}

DISPATCH:
  language unknown          -> human queue
  needs_locale_expert true  -> jurisdiction-specific corpus +
                               human review
  false                     -> standard handler in {language}
```

*Shows:* steps 2, 3, 7. The second field routes on regulatory exposure, which language alone does not capture.

*Check:* audit false negatives specifically — regulated content routed to the standard handler. That is the direction that causes harm.

### Example 23.4 — Document-type routing for extraction (operations)

```
ROUTER (schema-constrained: type and second_type limited to
the list):
  Identify the document type from this list:
  INVOICE, PURCHASE_ORDER, CONTRACT, RECEIPT, OTHER

  Return JSON only:
  {"type": "<type>", "second_type": "<type>" | null,
   "confidence": "high" | "low"}
  Set confidence low if the document has features of more
  than one type, and name the next most likely type in
  second_type. Otherwise second_type is null.

  First page text: {first_page}

DISPATCH:
  type OTHER      -> human queue
  high confidence -> the schema-constrained extractor (§18)
                     for type
  low confidence  -> run the extractors for type and
                     second_type, compare, send disagreements
                     to a human
```

*Shows:* steps 2, 3, 6. Low confidence triggers parallel extraction rather than a guess.

*Check:* the rate of low-confidence documents whose two extractors agree. High agreement means you can tighten the threshold; low agreement means the types genuinely overlap.

### Example 23.5 — Intent routing with a re-route budget (conversational product)

```
ROUTER (runs on every turn, not just the first):
  Given the conversation so far and the new message, choose
  the intent from this list: ORDER_STATUS, BILLING, TECHNICAL,
  CANCELLATION, OTHER. Use OTHER if none fits. Return:
  {"intent": "<intent>", "changed_from_previous":
   true|false}

  Conversation: {history}
  New message: {message}

DISPATCH (code), in this order:
  1. intent OTHER -> human queue (the fallback class).
  2. changed_from_previous false -> stay with the current
     handler.
  3. changed_from_previous true -> increment the re-route
     counter, then:
       counter > 2  -> route to a human. A third change of
                       intent means the taxonomy is failing
                       this user.
       counter <= 2 -> hand off to the new intent's handler,
                       passing a summary of the prior turns.
LOG (code): the intent label on every turn.
```

*Shows:* steps 3, 5. The re-route budget converts a routing failure into a handoff instead of a loop.

*Check:* conversations that hit the budget. Read ten of them; they will show you the intent your taxonomy is missing.

## 24. Parallelization: Sectioning and Voting

**What it does and when to reach for it.** Parallelization runs several calls at once, in two distinct forms. **Sectioning** splits a task into independent subtasks and merges the results — reach for it when the parts genuinely do not depend on each other, and you want latency or focus. **Voting** runs the same task several times and aggregates — reach for it when you want reliability on a votable answer. These are different patterns with different failure modes; do not conflate them.

**Build steps.**

1. **Confirm independence before sectioning.** If section B needs section A’s answer, you need a chain (§22), not parallelization.
2. **Give each section the context it needs and no more.** Shared context reintroduces coupling.
3. **Write the merge step explicitly,** and decide what it does with disagreement and overlap.
4. **For voting, follow the self-consistency build steps** (§10): temperature above zero, deterministic parsing, code-side aggregation.
5. **Handle partial failure.** One section erroring must not silently drop from the merge.
6. **Assert coverage after the merge** — every section accounted for, nothing duplicated.

**Combines with.** Sectioning pairs with orchestrator-workers (§25) when the sections are not known in advance. Voting is self-consistency (§10) as infrastructure.

### Example 24.1 — Sectioning a long document review (legal operations)

```
SPLIT (code): divide the contract by article. Each worker
gets one article plus the definitions section.

WORKER (parallel, one per article):
  <definitions>{definitions}</definitions>
  <article id="{article_id}">{article_text}</article>

  Identify every obligation this article places on
  {our_party}. Return JSON:
  {"article_id": "<article_id>", "obligations":
   [{"obligation": ..., "trigger": ..., "quote": ...}]}
  Use an empty obligations list if there are none. Do not
  reference other articles.

MERGE (code): collect the results. Assert every article ID
appears in the result set, including those with an empty list.

MERGE CALL:
  <definitions>{definitions}</definitions>
  All obligations: {merged_json}
  Identify any two obligations that conflict, and any
  obligation whose trigger is undefined in the definitions.
  Do not summarize; only report conflicts and gaps.
```

*Shows:* steps 1–3, 5, 6. Definitions go to every worker and to the merge call because they are the shared dependency; nothing else is.

*Check:* the coverage assertion. An article that silently produced no output is indistinguishable from one with no obligations unless you assert it.

### Example 24.2 — Sectioning a multi-criteria evaluation (hiring)

```
SPLIT (code): one worker per evaluation criterion, for each
candidate.

WORKER (parallel):
  Criterion: {criterion} with its rubric: {rubric}
  Candidate material: {material}

  Score only this criterion. Give the level and the specific
  evidence. Do not consider other criteria, and do not form
  an overall impression.

MERGE (code): assemble one scorecard per candidate. Do not
average.

MERGE CALL (across candidates):
  Scorecards: {scorecards}
  Identify criteria where nearly the same evidence earned a
  high score for one candidate and a low score for another —
  those indicate a rubric problem, not a candidate problem.
```

*Shows:* steps 1–3, 6. Independent scoring is the point: it reduces the chance that one strong criterion colors the rest.

*Check:* do not let the merge produce a single number. If a number is required, compute it in code with explicit weights someone signed off on.

### Example 24.3 — Voting on an extraction (records processing)

```
Run 5 in parallel at temperature 0.5:

  Extract the effective date. End with
  "ANSWER: YYYY-MM-DD" or "ANSWER: NONE".
  Document: {doc}

AGGREGATE (code):
  normalize -> reject malformed -> count the valid votes
  Fewer than 3 valid -> parse failure, escalate.
  A value with 3 or more matching valid votes -> accept it.
  Anything else -> human review with all five shown.
```

*Shows:* steps 4–6. This is self-consistency deployed as infrastructure rather than as a prompt.

*Check:* separate the parse-failure rate from the disagreement rate. They have different fixes: schema constraints for the first, a better prompt or a better model for the second.

### Example 24.4 — Parallel perspectives with a structured merge (product decision)

```
Run 3 in parallel, each with a different framing:

  WORKER A: Evaluate this proposal from the user's
  perspective. What gets better and worse for them?
  WORKER B: Evaluate from the operator's perspective.
  What does supporting this cost?
  WORKER C: Evaluate from the maintainer's perspective.
  What does this commit us to?

  Proposal: {proposal}
  Return your concerns as a list, one short sentence each.

MERGE CALL (code numbers each worker's concerns A1, A2, ...,
B1, B2, ..., C1, C2, ... before sending):
  {a}, {b}, {c}
  Group concerns that describe the same underlying issue.
  Build a table: CONCERN | RAISED BY (IDs) | AFFECTS WHOM.
  Then list the concerns raised by only one perspective.
```

*Shows:* steps 1–3. This is a third pattern, neither sectioning nor voting: the same proposal is read through three framings, and the merge keeps what only one framing raised alongside what several did.

*Check:* the single-perspective concerns are the output. If every concern appears in all three, your framings were not actually different. Treat each single-perspective concern as a lead to examine; this example does not measure what a single reviewer would have caught.

### Example 24.5 — Parallel safety checks with fail-closed merge (production gating)

```
Run 3 independent checks in parallel on the same output:

  Response: {output}

  CHECK 1 (also given {sources}): Is every factual claim
  supported by the sources?
  CHECK 2 (also given {permitted_scope}): Does the response
  stay within the permitted scope?
  CHECK 3 (also given {forbidden_claims}): Does the response
  avoid the forbidden claim list?

  Each returns: PASS or FAIL with the offending sentence.

MERGE (code): fail-closed.
  All three PASS      -> release
  Any FAIL            -> block, log which check and why
  Any check errors or -> block. An unavailable check is not
  times out              a passing check.
```

*Shows:* steps 3, 5. The last rule is the one people get wrong: a timed-out check must not default to pass.

*Check:* the per-check block rate. A check that never fires is either unnecessary or broken — find out which.

## 25. Orchestrator-Workers

**What it does and when to reach for it.** An orchestrator model decomposes a task into subtasks at runtime, dispatches them to workers, and synthesizes the results. It differs from sectioning (§24) in that the subtasks are not known in advance. Reach for it when the shape of the work depends on the input — a research question whose sub-questions you cannot enumerate ahead of time, a codebase change whose file set is unknown. It is expensive and it fails in ways that are hard to see, so reach for it last.

**Build steps.**

1. **Have the orchestrator emit a structured plan** — a list of subtasks with typed inputs — not prose.
2. **Gate the plan before dispatching.** Cap the subtask count. Reject subtasks that duplicate each other.
3. **Give each worker only its subtask’s context.** Workers should not see the plan.
4. **Make workers return structured results with a status field,** including an explicit “could not complete.”
5. **Synthesize in a separate call** that sees results, not reasoning traces.
6. **Require the synthesis to report incomplete subtasks,** not to paper over them.
7. **Cap total calls in code.** An orchestrator that can spawn workers that spawn workers is an unbounded bill.

**Combines with.** Workers can be any technique in this guide. Evaluator-optimizer (§26) on the synthesis. Least-to-Most (§11) is the static version of this pattern and should be preferred when the decomposition is predictable.

### Example 25.1 — Research question decomposition (analysis)

```
ORCHESTRATOR:
  Research question: {question}
  Available sources: {corpus_description}

  Produce a plan as JSON:
  [{"subtask_id": 1, "question": "...", "why_needed": "..."}]

  Rules: at most 6 subtasks. Each must be independently
  answerable from the corpus. No two may ask the same thing
  in different words.

GATE (code): parse; assert count <= 6; reject near-duplicate
questions by embedding similarity.

WORKER (parallel, one per subtask, sees only its question):
  Subtask id: {subtask_id}
  Question: {subtask_question}
  Sources: {sources}
  Answer from the sources. Return JSON:
  {"subtask_id": <subtask_id>, "answer": "...",
   "citations": [...], "status": "answered" | "not_in_sources"}

SYNTHESIS (sees results only, not the plan's reasoning):
  Original question: {question}
  Results: {worker_results}
  Answer the original question using only answered subtasks.
  List every not_in_sources subtask under "OPEN QUESTIONS".
```

*Shows:* steps 1–6.

*Check:* the OPEN QUESTIONS list. A synthesis that reads as complete while three subtasks came back unanswered is the characteristic failure of this pattern.

### Example 25.2 — Codebase change orchestration (software)

```
ORCHESTRATOR:
  Issue: {issue}
  Repository map: {file_tree_with_summaries}

  Produce a plan as JSON:
  [{"file": "...", "change": "...", "depends_on": ["<file>", ...]}]

  At most 8 files. State dependencies explicitly.

GATE (code): assert every file exists; assert the dependency
graph is acyclic; reject if any file is outside the allowed
directories.

WORKER (per file, in dependency order, sees only its file and
its dependencies' diffs):
  File: {file_contents}
  Change to make: {change}
  Dependencies' diffs: {dependency_diffs}
  Make the described change. Return the full modified file
  and a status: "changed" | "no_change_needed" | "blocked".

GATE (code): run tests after each file. Count every model call
and stop the run at 10 (the plan, up to 8 workers, the
synthesis).

SYNTHESIS:
  Worker results: {worker_results}
  Test results: {test_output}
  Report which files changed, which were blocked and why, and
  whether the test suite passes.
```

*Shows:* steps 1–4, 6, 7. The dependency ordering makes this a chain per branch, not a free-for-all.

*Check:* “blocked” statuses. An orchestrator plan that produces blocked workers had a wrong model of the code, and the plan is what needs fixing.

### Example 25.3 — Multi-source due diligence (business operations)

```
ORCHESTRATOR:
  Target: {company}
  Question: "What are the top risks in acquiring this
  company?"
  Available tools: {tool_list}

  Produce a plan: at most 5 investigation threads, each with
  the tool to use and what would count as a finding.
  Return JSON.

GATE: cap at 5; assert each thread names a tool that exists.

WORKER (per thread, ReAct agent §16 with only that tool):
  Thread: {thread}
  Investigate the thread. Return:
  {"thread": ..., "findings": [...], "status": "complete" |
   "inconclusive", "evidence": [...]}

SYNTHESIS:
  {thread_results}
  Rank the risks found. For each, give the evidence and the
  thread it came from.
  Then: list every inconclusive thread as a diligence gap.
  Do not rank a risk that has no evidence.
```

*Shows:* steps 1–6. Giving each worker one tool reduces coupling between threads.

*Check:* the diligence gaps. In this domain, what you could not find out is often more important than what you did.

### Example 25.4 — Content production pipeline (marketing operations)

```
ORCHESTRATOR:
  Brief: {brief}
  Produce a plan as JSON: the assets needed, each with
  {"asset": ..., "format": ..., "source_material": ...}
  At most 6 assets. Every asset must trace to a line in the
  brief — include the quoted line.

GATE (code): assert each asset's quoted brief line appears in
the brief verbatim. Reject invented deliverables.

WORKER (per asset):
  Asset: {asset}
  Format: {format}
  Source material: {source_material}
  Produce it from its source material only.

SYNTHESIS:
  Brief: {brief}
  Assets: {assets_with_quoted_lines}
  Assemble the assets; report any brief line with no asset
  mapped to it.
```

*Shows:* steps 1, 2, 4, 6. The verbatim-quote gate is what stops scope invention, which is this pattern’s favorite failure in creative work.

*Check:* unmapped brief lines. Those are requirements the orchestrator dropped, and no one downstream will notice.

### Example 25.5 — Incident investigation (site reliability)

```
ORCHESTRATOR:
  Alert: {alert}
  Available signals: {signal_list}

  Produce at most 4 investigation threads as JSON, each with
  the signal to examine and the hypothesis it tests.
  Each hypothesis must be falsifiable by that signal.

GATE: cap at 4; assert each signal exists; reject any
hypothesis the named signal cannot falsify.

WORKER (per thread, read-only access to its signal):
  Thread: {thread}
  Examine the signal. Return:
  {"hypothesis": ..., "verdict": "supported" | "refuted" |
   "inconclusive", "evidence": "..."}

SYNTHESIS:
  {results}
  State the most likely cause and the evidence for it.
  Explicitly list every refuted hypothesis — ruling things
  out is a finding.
  If all threads are inconclusive, say so and recommend what
  to instrument. Do not guess.
```

*Shows:* steps 1–6. Falsifiability in the gate is what makes the workers useful rather than confirmatory.

*Check:* the refuted list. An investigation that refutes nothing has not narrowed anything down, whatever its conclusion says.

## 26. Evaluator-Optimizer

**What it does and when to reach for it.** A generator produces output and a separate evaluator critiques it, in a loop, until the evaluator accepts or a cap is hit. Reach for it when quality criteria are clear but hard to hit first try — translation, writing against a style guide, code against a spec. The separation is what makes it work: it is not self-refine, and the finding by Huang et al. (arXiv 2310.01798) that unaided self-correction can degrade reasoning is the motivation for keeping the evaluator separate. Where an automatic check exists, use Reflexion (§17) instead; a real test beats a model’s opinion.

**Build steps.**

1. **Use a different model family for the evaluator,** or at minimum a fresh context with no generation history.
2. **Give the evaluator concrete defect categories,** not “rate this.”
3. **Require an exact accept token** so the loop terminates deterministically.
4. **Forbid the evaluator from rewriting.** Its job is to find defects; mixing roles produces critique shaped to justify its own rewrite.
5. **Feed back only the defect list,** not the evaluator’s full reasoning.
6. **Cap the rounds** — three is a reasonable default. Measure on your own task where further rounds stop helping, and stop there.
7. **Escalate on non-convergence** with both versions and the final defect list.

**Combines with.** LLM-as-judge (§20) build steps apply to the evaluator. Reflexion (§17) is the stronger sibling when an external signal exists.

### Example 26.1 — Translation quality loop (localization)

```
GENERATOR:
  Translate into {target_language}. Preserve product names,
  numbers, and units exactly.
  Source: {source}

EVALUATOR (different model family, does not see the
generator's reasoning):
  Source: {source}
  Translation: {translation}

  List concrete defects only, one per line:
  - mistranslation (quote both)
  - altered number or unit
  - changed product name
  - register mismatch with the source
  Do not rewrite. Do not comment on style you merely prefer.
  If there are no defects, reply exactly "ACCEPT".

LOOP: feed the defect list back to the generator. Stop on
ACCEPT or after 3 rounds. On non-convergence, send both
versions and the final defect list to a human.
```

*Shows:* steps 1–7.

*Check:* the round-2 and round-3 defect lists. If new defect types appear each round, the generator is trading one error class for another and the loop is not converging.

### Example 26.2 — Style-guide compliance (documentation)

```
GENERATOR: write the section from the outline and source.

EVALUATOR:
  Style guide: {guide}
  Draft: {draft}
  For each guide rule, state COMPLIES or VIOLATES. For each
  violation, quote the offending text and name the rule
  number. Do not suggest replacement text.
  End with one last line: "VERDICT: ACCEPT" if every rule
  complies, otherwise "VERDICT: REVISE".

LOOP: pass only the violations back. Stop when code finds the
exact line "VERDICT: ACCEPT". Cap 3 rounds.
```

*Shows:* steps 2–5. Rule numbers make the feedback actionable and the loop auditable.

*Check:* which rules violate most often across documents. Those are candidates for the generator’s system prompt (§3), which is cheaper than fixing them in a loop every time.

### Example 26.3 — Spec-conformant code (software, no test suite yet)

```
GENERATOR: implement the function from the spec.

EVALUATOR (different model family):
  Spec: {spec}
  Implementation: {code}

  For each numbered requirement in the spec, state MET or
  NOT MET. For NOT MET, name the line and what it does
  instead. Also list any behavior in the code that the spec
  does not authorize.
  Do not write code. End with one last line: "VERDICT: ACCEPT"
  if all requirements are met and there is no unauthorized
  behavior, otherwise "VERDICT: REVISE".

LOOP: stop when code finds the exact line "VERDICT: ACCEPT";
cap 3 rounds, then escalate.
```

*Shows:* steps 1–4, 6. “Unauthorized behavior” catches the extras that a requirements checklist alone misses.

*Check:* as soon as you have tests, switch to Reflexion (§17). An executed test is worth more than any evaluator in this section.

### Example 26.4 — Data-visualization description loop (accessibility)

```
GENERATOR: write alt text for the chart, given its
underlying data table.

EVALUATOR:
  Data table: {table}
  Alt text: {alt_text}

  Answer each:
  1. Could a reader reconstruct the chart's main finding from
     this text alone? YES/NO + what is missing.
  2. Does any number in the text differ from the table?
     List them.
  3. Does the text describe visual appearance instead of the
     finding? Quote it.
  End with one last line: "VERDICT: ACCEPT" if 1 is YES, 2 is
  empty, and 3 is empty, otherwise "VERDICT: REVISE".

LOOP: stop when code finds the exact line "VERDICT: ACCEPT";
cap 3 rounds.
```

*Shows:* steps 2, 3, 5. Three specific questions beat “is this good alt text?”

*Check:* question 2 is mechanically verifiable — do it in code as well, and treat any evaluator that missed a number mismatch as unreliable for question 1 too.

### Example 26.5 — Summary faithfulness loop (content operations)

```
GENERATOR: summarize the source in five bullets.

EVALUATOR (different model family, sees source and summary):
  Source: {source}
  Summary: {summary}
  For each bullet, classify: SUPPORTED, INFERABLE,
  UNSUPPORTED, or CONTRADICTED. For CONTRADICTED, quote the
  source sentence that contradicts it.
  List only the bullets that are not SUPPORTED.
  If all five are SUPPORTED, reply exactly "ACCEPT".

LOOP: return only the non-supported bullets with their
classification. The generator must replace those bullets
only, leaving supported bullets byte-identical. Cap 3 rounds,
then escalate.

GATE (code): assert the supported bullets did not change
between rounds.
```

*Shows:* steps 2, 3, 5, 6, plus a gate. The byte-identical assertion stops the generator rewriting everything each round.

*Check:* the gate’s failure rate. A generator that cannot leave good bullets alone will never converge, and the gate is how you find that out in round two instead of round three.

## 27. Multi-Agent Debate

**What it does and when to reach for it.** Several model instances argue toward an answer, critiquing each other across rounds. Du et al. (arXiv 2305.14325) show it can improve factuality and reasoning; Liang et al. (arXiv 2305.19118) motivate it with **Degeneration-of-Thought** — once a model is confident, it struggles to generate genuinely divergent alternatives, which an adversarial setup is designed to counter. Reach for it rarely: it is among the most expensive patterns here, and its failure mode is convergence on a shared error, which looks exactly like success. Agreement is not correctness.

**Build steps.**

1. **Give the agents genuinely different starting positions or evidence.** Same prompt, same model, different seeds is not a debate.
2. **Use different model families** where you can afford to.
3. **Require each agent to state its position and its strongest supporting evidence** before seeing others.
4. **In later rounds, require each agent to address the specific claim it disagrees with,** not to restate its position.
5. **Cap at 2–3 rounds.** As a heuristic, positions often settle by round two and later rounds tend to restate rather than add; check on your own task where they stop changing.
6. **Have a separate judge read the final positions,** and forbid the debaters from declaring a winner.
7. **Record unresolved disagreement as an output,** not a failure. It is the signal that the question is genuinely open.

**Combines with.** LLM-as-judge (§20) for the arbitration step. Disconfirmation (§21) is the cheap single-call approximation and is the right first try.

### Example 27.1 — Two-position factual debate (research)

```
ROUND 1 (parallel, agents do not see each other; both get
the same numbered sources):
  Sources: {sources}
  AGENT A: Argue that {claim} is TRUE. State your three
  strongest pieces of evidence, citing the sources by number.
  AGENT B: Argue that {claim} is FALSE. Same format.

ROUND 2 (each sees the other's round-1 position):
  You previously argued {position}. The other side argued:
  {other_position}

  Address their strongest specific piece of evidence
  directly. Either refute it with counter-evidence, or
  concede that point explicitly. Do not restate your
  original argument.

JUDGE (third model, different family, sees both rounds and
the same sources):
  Sources: {sources}
  Which position is better supported by the evidence
  presented? If both rely on the same unverified premise,
  say so and declare NEITHER.
  Output: VERDICT: TRUE | FALSE | NEITHER, plus the single
  piece of evidence that decided it.
```

*Shows:* steps 1–4, 6.

*Check:* NEITHER verdicts. They are a valuable output, and one a single-model answer rarely produces.

### Example 27.2 — Design review debate (engineering)

```
ROUND 1 (parallel):
  Design: {design}
  AGENT A (proponent): Make the strongest case for this
  design. Name the constraint it handles best.
  AGENT B (skeptic): Make the strongest case against. Name
  the specific scenario where it fails.
  AGENT C (operator): Argue from what it costs to run and
  maintain, independent of whether it is elegant.

ROUND 2: each addresses the strongest point from the other
two, conceding explicitly where they cannot answer it.

JUDGE:
  Summarize: what all three agree on, what remains contested,
  and what evidence would settle each contested point.
  Do not declare a winner.
```

*Shows:* steps 1, 3, 4, 6, 7. Three roles rather than two positions avoids a binary that does not fit design decisions.

*Check:* the “what would settle it” list. That is the experiment or spike to run, and it is the concrete output of the whole exercise.

### Example 27.3 — Numerical estimate reconciliation (forecasting)

```
ROUND 1 (parallel, different decompositions):
  AGENT A: Estimate {quantity} top-down. State your
  decomposition and each factor.
  AGENT B: Estimate {quantity} bottom-up. Same.

ROUND 2:
  Your estimate was {yours}; theirs was {theirs}.
  Identify the single factor where your two decompositions
  differ most, and say which of you has better grounds for it.

JUDGE:
  Report both estimates, the identified divergent factor, and
  a range rather than a point estimate. If the two methods
  differ by more than {max_ratio}x, report that the quantity
  is not reliably estimable from the available information.
```

*Shows:* steps 1, 4, 6, 7. Different decompositions make the two estimates more independent of each other.

*Check:* the ratio rule firing is a finding. Set `{max_ratio}` in advance from how accurate the estimate must be (2 is a starting point, not a standard). When two methods diverge past it, treat the quantity as not reliably estimable from this information, however confident either agent sounds.

### Example 27.4 — Policy interpretation with adversarial readings (compliance)

```
ROUND 1 (parallel, same policy text):
  Policy text: {policy_text}
  AGENT A: Give the reading most favorable to the
  requester, citing the policy text.
  AGENT B: Give the reading most favorable to the
  organization, citing the policy text.

ROUND 2: each identifies the specific words in the policy
that the other's reading depends on, and whether those words
bear that weight.

JUDGE:
  Is the policy text ambiguous between these readings?
  If yes: report both readings, the ambiguous phrase, and
  recommend the policy be clarified. Do not pick one.
  If no: state which reading the text supports and quote the
  deciding language.
```

*Shows:* steps 1, 3, 4, 6, 7. The ambiguity verdict is the point — it routes to a policy fix rather than a coin flip.

*Check:* the quoted deciding language on non-ambiguous verdicts. If the judge cannot point at specific words, it is ambiguous and the verdict is wrong.

### Example 27.5 — Debate with a mandatory shared-error check (high-stakes)

*Setup:* run any two-agent debate above, then send this as a final pass to a different model family than either debater.

```
  Both agents reached: {shared_conclusion}
  Their reasoning: {both_positions}

  They agree. Your job is to find the premise they both
  assumed without examining it.

  1. What did neither agent question?
  2. If that assumption were false, what happens to both
     conclusions?
  3. Is that assumption checkable from the evidence provided?

  End with: SHARED ASSUMPTION SOUND, or
  SHARED ASSUMPTION UNTESTED: <what to verify>.
```

*Shows:* steps 2, 7. This directly targets the failure mode that makes debate dangerous — confident convergence on a common error.

*Check:* run this whenever debate produces agreement. Agreement is the case where you most need it, and the case where you are least inclined to ask.

## 28. Automated Optimization Loops

**What it does and when to reach for it.** Automated optimization has a model propose and score prompt candidates against a metric, keeping what wins. Reach for it only when three things are true: the prompt is reused at scale, you have a metric and a dev set, and the per-request quality gain repays a large one-time compute cost. The scale of that cost is documented: on Gemini Pro, OPRO consumed about 96,289 input and 170,448 output “tokens” (the authors’ term; they count by splitting text into words) over about 21 hours to find its best GSM8K instruction, against about 130 input and no output over about 5 hours for few-shot CoT (Zhang et al., arXiv 2405.10276, Table 3). GEPA’s sample efficiency may lower the threshold: in the abstract of arXiv 2507.19457 (version 2) it beats GRPO by 6% on average and by up to 20%, with up to 35× fewer rollouts, and the GRPO comparison is on Qwen3 8B only. That is a reason to revisit this decision, not a measured break-even point; this guide cites no study of one.

**Build steps.**

1. **Build the eval set first.** No metric, no optimization — you will optimize toward whatever you happen to measure.
2. **Split three ways:** a train slice the optimizer scores against, a dev slice for selection, and a test slice the optimizer never sees.
3. **Baseline the hand-written prompt** on the test slice. This is the number to beat.
4. **Score candidates by running them,** never by asking a model how good they look.
5. **Run a fixed iteration budget** decided in advance, with a cost cap.
6. **Validate the winner on the untouched test slice.** A gain that does not survive this is overfitting.
7. **Re-run the whole thing on model upgrades.** Optimized prompts are model-specific, and gains measured on 2022–2023 models often shrink on current ones (manual Sections 7.2 and 9.1).

**Combines with.** Everything, as a final step. Never a first step — optimize a prompt that already works, on a task you can already measure.

### Example 28.1 — APE-style instruction induction

```
PROPOSE:
  I gave a friend an instruction and these input-output pairs.
  {5_demonstration_pairs}
  Write 10 candidate instructions that would produce these
  outputs. One per line, no numbering, no commentary.

SCORE (code): run the baseline (the hand-written prompt) and
each candidate on the same 50 held-out pairs; record
exact-match accuracy for each, and the standard error of each
candidate's paired difference from the baseline.

SELECT: keep a candidate only if it beats the baseline by
more than 3 standard errors. Ten candidates give noise ten
chances to pass, so the bar is stricter than 2.

VALIDATE: re-test the winner on a second held-out set the
selection never touched.
```

*Shows:* steps 2–4, 6. The second held-out set exists because the first one became part of the search the moment you selected on it.

*Check:* the gap between the selection score and the validation score. A large gap is overfitting, and the “improvement” is noise you paid for. Fifty pairs can only reveal large gains; use more if the gain you care about is small.

### Example 28.2 — OPRO-style meta-prompt loop

```
META-PROMPT (to the optimizer model, each round):
  Your task is to generate an instruction that maximizes
  accuracy on problems like the ones below.

  Previous instructions with their measured scores
  (higher is better):
  {top_20_instructions_with_scores}

  Example problems:
  {three_sampled_training_problems}

  Generate 8 new instructions that would score higher.
  Wrap each in <Start></Start> tags. Output nothing else.

SCORER (code): run each new instruction on a validation
slice; record real accuracy; append to the trajectory.

Repeat for a fixed iteration budget with a hard cost cap.
```

*Shows:* steps 1, 4, 5. Every score in `{top_20_instructions_with_scores}` comes from an actual run. An optimizer scoring its own candidates is not OPRO; it is a model agreeing with itself.

*Check:* whether the optimizer model is capable enough. When small models served as their own optimizers on GSM8K, OPRO underperformed both CoT baselines on Mistral 7B, LLaMa-2-13B, and LLaMa-2-70B, while beating them on LLaMa-2-7B and Gemini-Pro (Zhang et al., Findings of ACL 2024). The authors’ conclusion is that small models make limited optimizers.

### Example 28.3 — GEPA-style reflective evolution

```
1. Run the current prompt on a minibatch. Capture full
   trajectories: reasoning, tool calls, tool outputs, score.

2. REFLECT:
   Current instruction: {instruction}
   Traces from {n} attempts with their scores:
   {traces_with_scores}

   Diagnose, in natural language, why the low-scoring
   attempts failed. Be specific about what the instruction
   failed to specify.
   Then propose one revised instruction that fixes the
   diagnosed cause.
   Output the diagnosis, then the instruction between
   <INSTRUCTION></INSTRUCTION> tags.

3. Score the candidate on each training instance in the
   minibatch. Keep it if it has the best score so far on at
   least one training instance. That is the Pareto frontier
   here: per instance, not score against instruction length.

4. Periodically merge complementary lessons from two
   frontier candidates into one.

5. Repeat for a fixed iteration budget with a hard cost cap.
```

*Shows:* steps 4, 5. Reflection over full traces is what makes this sample-efficient — each failure teaches something a scalar reward does not.

*Check:* read the diagnoses. They are a readable by-product of the search — each one costs tokens to produce — that says what the instruction failed to specify, and they are worth reading even if you never ship the optimized prompt.

### Example 28.4 — Local optimization of a production prompt

```
Use when a long prompt mostly works and you do not want an
optimizer rewriting the parts that do.

1. Tag the spans that may change:
     ... fixed legal disclaimer ...
     <edit>Classify the ticket into one of five categories.</edit>
     ... fixed output schema ...

2. OPTIMIZER (per round):
     Here is a prompt. Rewrite only the text inside <edit>
     tags. Return the full prompt with your revision in
     place, keeping everything else byte-identical.
     Failing cases: {failures}

3. GATE (code): assert every byte outside the edit spans is
   unchanged. Reject the candidate otherwise.

4. Score, select, validate on held-out data as in Example 28.1.
```

*Shows:* steps 1–4, 6, following Local Prompt Optimization (Jain & Chowdhary, arXiv 2504.20355). The byte-identical gate is what makes it safe to run against production prompts.

*Check:* the gate’s rejection rate. A high rate means the optimizer keeps trying to improve things you told it not to touch, and the edit spans are probably drawn too narrowly.

### Example 28.5 — The decision harness: should you optimize at all?

```
Run this before writing any optimizer. It is arithmetic, not
a prompt. Put every cost in the same currency.

1. Requests per month at steady state:            R
2. Months until your next model upgrade:          M
3. Expected quality gain per request, in a unit you
   can price (for example, extra correct answers
   per request):                                  G
   (measure it on 50 examples with a quick manual
    rewrite first; as a rule of thumb, if a careful
    human rewrite gains nothing, an optimizer may gain
    little too)
4. Value, in currency, of one unit of that gain:  V
5. Change in cost per request with the optimized
   prompt (negative if it is cheaper):            D
6. One-time optimization cost, in currency:       C_opt
   (the price of every proposer, scorer and validation
    call; for scale, OPRO on Gemini Pro used about 96,289
    input and 170,448 output word-based "tokens" and about
    21 h; GEPA reports up to 35x fewer rollouts than GRPO,
    on Qwen3 8B)
7. Engineering hours to build and maintain the harness: H

Optimize only if

  R x M x (G x V - D)  >  C_opt + (H x hourly rate)

The horizon M matters most: optimized prompts are
model-specific, and the gain resets when you upgrade.
```

*Shows:* steps 1, 3, 7. If you are weighing optimization, build the eval set first — that is advice rather than a measured finding, and it is step one of this procedure anyway.

*Check:* step 3 honestly. A careful human rewrite is a cheap way to estimate the headroom. Whether it also predicts what an optimizer can gain is an untested rule of thumb, so treat a flat result as a warning, not a verdict.

# Part 7 — Matching Techniques to What People Actually Do

## 29. What the usage data says

Most prompt-engineering writing optimizes for benchmark tasks — grade-school math, multi-hop trivia, puzzle solving. Almost nobody’s actual traffic looks like that. This section starts from three published reports on real usage and works backward to the techniques that fit.

**Source 1 — OpenAI / NBER, “How People Use ChatGPT”** (NBER Working Paper 34255, September 2025). A privacy-preserving classification of roughly 1.1 million sampled consumer conversations from May 2024 through June 2025. Shares below are of all classified messages in that sample unless noted. In the table, “a → b” is the share at the start and at the end of the sample (May 2024 → June 2025); a single figure is undated in this guide’s source note, so it may be a whole-period average or an end-of-period value.

| **Conversation topic** | **Share of all messages (May 2024 → June 2025)** | **Trend over the year** |
|---|---|---|
| Practical Guidance | ~29% | flat |
| Writing | 36% → 24% | falling |
| Seeking Information | 14% → 24% | rising |
| Multimedia | 2% → ~7% | rising |
| Technical Help | 12% → ~5% | falling |
| Self-Expression | ~2.4% | not characterized |

Practical Guidance, Writing, and Seeking Information together account for roughly 77–79% of all messages (the table’s figures sum to 79% at the start of the sample and 77% at the end, taking Practical Guidance as ~29% throughout). Within them:

- **Tutoring or teaching** is 10.2%† of *all* messages and 36% of Practical Guidance.
- **How-to advice** is 8.5%† of all messages and 30% of Practical Guidance.
- **Editing or critiquing text the user provided** is the largest Writing sub-category; about two-thirds of Writing messages modify the user’s own text rather than generating new text.

Separately, **computer programming** is 4.2%† of messages, **mathematical calculation** 3%†, and **data analysis** 0.4%†. († marks a single figure that this guide’s source note does not date: it may be a whole-period average or an end-of-period value. For that reason, do not read these three against the table’s Technical Help row.)

By intent, the paper classifies 49% of messages as **Asking** (seeking information or advice), 40% as **Doing** (producing an output), and 11% as **Expressing** — averages over the whole period, not the mix at its end. Expressing, an *intent* category, rose to 13.8% by June 2025; it is a different taxonomy from the Self-Expression *topic* in the table above, and the two should not be compared. Among work-related messages the split inverts: about 56% Doing, 35% Asking. Writing is 40% of work-related messages, the largest single work category.

Mapped to O*NET work activities, three categories cover 45.2%† of all messages: Getting Information (19.3%†), Interpreting the Meaning of Information for Others (13.1%†), and Documenting or Recording Information (12.8%†).

**Source 2 — Anthropic Economic Index report, “Cadences”** (June 26, 2026), classifying the *artifact* each conversation produced, sampled April 10 to June 10, 2026, across chat and Cowork.

| **Artifact produced** | **Share of conversations (April 10 – June 10, 2026)** |
|---|---|
| Explanations | 17% |
| Documents and reports | 15% |
| Guidance | 11% |
| (no distinct artifact) | ~7%* |

\*The report states that 93% of conversations produced an artifact; the 7% is that figure’s complement, not a quoted number.

Conversational outputs such as explanations and guidance account for about a third of conversations; written deliverables such as documents and presentations another third; code and technical work about a sixth. Broken out by purpose: work conversations most often produce documents and reports (20%), explanations (9%), email drafts (7%), and analyses or summaries (6%). Coursework produces documents and reports (21%), explanations (20%), educational materials (11%), and academic papers (6%). Personal conversations produce explanations (25%) and recommendations (22%), with only 6% producing a document.

**Source 3 — Anthropic Economic Index report, “Learning curves”** (March 2026), sampled February 5–12, 2026, adds that tasks associated with Computer and Mathematical occupations account for 35% of Claude.ai and first-party API traffic. It is an occupation-based measure from a different product mix and period than Source 2, so it is not directly comparable with Source 2 or with Source 1.

**Three inferences that shape the table below.**

1. **The usage data suggests that grounding matters more than reasoning topology for much of this traffic.** Getting information, interpreting it, and documenting it together cover 45.2% of ChatGPT messages in the O*NET mapping — a large share, not a majority. Many of those are retrieval and verification problems rather than reasoning-topology problems. This is an inference from what people ask for, not a measured effect of any technique.
2. **Most ChatGPT Writing messages edit text the user supplied.** About two-thirds of them do. That suggests a context-anchoring task with a preservation constraint rather than a generation task.
3. **The heavy reasoning techniques may serve a small slice.** Mathematical calculation plus data analysis is 3.4% of ChatGPT messages (3% and 0.4%, both undated†). That is one place heavy reasoning could matter; the data does not say how often Tree-of-Thoughts, Graph-of-Thoughts, or multi-agent debate would help. This guide places them last as specialist tools because of their cost and narrow fit, not because of these shares.

## 30. The technique-to-task mapping

**How to read this table.** The **default stack** is what to build first. The **add if** column says what to add when measurement shows the default failing, and what symptom justifies it. Nothing in the “add if” column should be built speculatively.

**How to read the Share column.** Each entry names its unit, product and period. *ChatGPT* entries are shares of messages in the NBER sample (May 2024–June 2025). *Claude* entries are shares of conversations, by artifact produced, in the *Cadences* sample (chat and Cowork, April 10–June 10, 2026). A † marks a single ChatGPT figure that the source note does not date. “Author’s mapping” means this guide placed the task inside a larger category, so the category’s share is an upper bound for the task, not a measurement of it. ChatGPT and Claude shares are not comparable.

### Tier 1 — Everyday tasks the usage data shows are common

| **Task** | **Share (unit, source, period)** | **Default stack** | **Add if** |
|---|---|---|---|
| **Seeking information — factual lookup** | ChatGPT messages, Seeking Information: 14% → 24%, rising (NBER, May 2024 → June 2025) | Zero-shot (§1) + RAG (§15) with citations and a “not in sources” path | Chain-of-Verification (§19) if claims get repeated downstream; conflict handling (Example 15.4) on contested topics |
| **Editing or critiquing supplied text** | ChatGPT messages: about 2/3 of Writing messages; Writing was 36% → 24% (NBER, May 2024 → June 2025) | Context anchoring (§4) + constraint framing (§5) with a preservation rule and a CHANGES list | Evaluator-optimizer (§26) against a style guide; schema (§18) if a system consumes the edits |
| **Explaining a concept** | Claude conversations: 17% produced an explanation (Cadences, April–June 2026) | Zero-shot (§1) with an audience spec in the system prompt (§3) | Step-Back (§14) when the explanation keeps pattern-matching to the wrong analogy |
| **How-to advice** | ChatGPT messages: 8.5%† (NBER, May 2024–June 2025) | Zero-shot (§1) + explicit step format + a “what could go wrong” section | RAG (§15) when the steps are product- or version-specific |
| **Tutoring or teaching** | ChatGPT messages: 10.2%† (NBER, May 2024–June 2025) | System rules (§3) fixing level and register + Step-Back (§14) for principle-first explanation | Few-shot (§2) to fix worked-example format; PoT (§13) for anything numerical |
| **Drafting a document or report** | Claude conversations: 15% of all, and 20% of work conversations, produced a document or report (Cadences, April–June 2026) | Structured template (§6) + context anchoring (§4) for source material | Prompt chaining (§22) when extract, draft, and tone are separable; CoVe (§19) on factual sections |
| **Drafting an email or message** | Claude work conversations: 7% produced an email draft (Cadences, April–June 2026) | Zero-shot (§1) + system rules (§3) for voice; supply the thread as anchored context (§4) | Evaluator-optimizer (§26) only if a house style guide exists |
| **Summarizing** | Claude work conversations: 6% produced analyses or summaries, of which summarizing is only a part (Cadences, April–June 2026) | Context anchoring (§4) with a supported-claim rule | LLM-judge factuality check (Example 20.4) in production; Chain-of-Density for information-dense output |
| **Recommendations** | Claude personal conversations: 22% produced a recommendation (Cadences, April–June 2026) | Zero-shot (§1) with stated criteria and an explicit tiebreak | Disconfirmation (§21) when the recommendation carries real cost |
| **Guidance on a personal decision** | Claude conversations: 11% produced guidance (Cadences, April–June 2026) | Zero-shot (§1) + Step-Back (§14) to separate the general principle from the specific case | A “What cannot” step (Example 14.5, step 4) for anything medical, legal, or financial |

### Tier 2 — Common professional tasks

| **Task** | **Share (unit, source, period)** | **Default stack** | **Add if** |
|---|---|---|---|
| **Classification and routing** | infrastructure, not a topic | Few-shot (§2) + schema-constrained enum (§18) | Self-consistency (§10) on high-cost classes; routing (§23) if classes need different handlers |
| **Structured extraction** | Author’s mapping: part of Technical Help, ChatGPT messages 12% → ~5% (NBER, May 2024 → June 2025) | Schema-constrained generation (§18) with nullable fields and an evidence span | Reflexion (§17) against the validator; few-shot (§2) for unusual formats |
| **Code writing and debugging** | ChatGPT messages: computer programming 4.2%† (NBER, May 2024–June 2025); a separate Claude measure is in note ‡ below | Context anchoring (§4) on the actual file + zero-shot (§1) | Reflexion (§17) the moment tests exist — the upgrade this table recommends most strongly, because tests supply the external signal Reflexion depends on |
| **Data analysis** | ChatGPT messages: data analysis 0.4%† (NBER, May 2024–June 2025) | Program-of-Thoughts (§13), always — never prose arithmetic | Self-consistency (§10) over programs for high-stakes numbers; prompt chaining (§22) to profile before interpreting |
| **Mathematical calculation** | ChatGPT messages: mathematical calculation 3%† (NBER, May 2024–June 2025) | Program-of-Thoughts (§13) | Chain-of-Draft (§7) only when you need volume and can accept a few points of accuracy |
| **Translation** | No share given in Part 7 | Zero-shot (§1) + a protected-terms list (§5) | Evaluator-optimizer (§26) with a different model family; back-translation gate (Example 22.4) for high-stakes text |
| **Planning and strategy** | No share given in Part 7 | Structured template (§6) + Step-Back (§14) | Disconfirmation (§21) before commitment; multi-agent debate (§27) only for irreversible decisions |
| **Policy or contract interpretation** | Author’s mapping: part of “Interpreting the Meaning of Information for Others,” 13.1%† of ChatGPT messages (O*NET mapping; NBER, May 2024–June 2025) | Context anchoring (§4) + Step-Back (§14) with a verbatim rule quote | Least-to-Most (§11) when eligibility has ordered conditions; debate (Example 27.4) when ambiguity is the real question |
| **Research synthesis** | Author’s mapping: part of “Getting Information,” 19.3%† of ChatGPT messages (O*NET mapping; NBER, May 2024–June 2025) | RAG (§15) + prompt chaining (§22): extract claims, verify, then write | Orchestrator-workers (§25) when the sub-questions are not knowable in advance |
| **Meeting notes to actions** | Author’s mapping: part of “Documenting or Recording Information,” 12.8%† of ChatGPT messages (O*NET mapping; NBER, May 2024–June 2025) | Zero-shot (§1) with explicit escape hatches + chaining (§22) with a gate | Schema (§18) once a system consumes the output |

‡ Claude.ai and first-party API traffic sampled February 5–12, 2026 (*Learning curves*): tasks associated with Computer and Mathematical occupations account for 35%. This is an occupation-based measure, not a share of coding requests, and it is not comparable with the ChatGPT figure above.

### Tier 3 — Specialist tasks

| **Task** | **Why it is a specialist task (author’s judgment; Part 7 has no usage figure for these)** | **Stack** |
|---|---|---|
| **Search and planning problems** | Needs real search over options, a specialist need | Tree-of-Thoughts (§12) — only with a reliable evaluator and a node budget |
| **Spatial and layout reasoning** | Narrow domain | Chain-of-Symbol (§8) |
| **Compositional instruction following** | Where L2M’s large win lives | Least-to-Most (§11) |
| **Multi-tool agentic work** | Adds cost and risk; justified only when the task needs tools | ReAct (§16) or ReWOO; least privilege throughout (manual Chapter 17) |
| **High-stakes contested judgment** | Expensive; justified only when an error would be costly | Debate (§27) + shared-assumption check (Example 27.5) + independent-model disconfirmation (Example 21.5) |
| **Prompt optimization at scale** | Only pays above a volume threshold | GEPA or DSPy (§28) — run the decision harness (Example 28.5) first |

## 31. Six stacks worth memorizing

These six stacks are worth memorizing as starting points. Each is listed as the full stack, in build order.

**1. The grounded answer.** The default for anything factual. System rules fixing scope (§3) → retrieved and re-ranked sources, numbered (§15) → context anchoring with a citation requirement and a “not in sources” string (§4) → parse and verify citations in code.

**2. The structured extractor.** The default for anything a system consumes. Schema with nullable fields, an evidence span, and `additionalProperties: false` (§18) → constrained decoding in the serving stack → semantic validation after parsing → Reflexion against the validator on failure (§17).

**3. The faithful editor.** The default for editing supplied text, which is about two-thirds of ChatGPT Writing messages (§29). Context anchoring on the user’s text (§4) → a preservation constraint stated positively (§5) → a required CHANGES list → a code diff asserting every change is listed (§22).

**4. The computed answer.** The default for anything numerical. Program-of-Thoughts with named inputs, printed intermediates, and a fixed ANSWER line (§13) → sandboxed execution → exception means failure, not improvisation → self-consistency over programs when the number matters (§10).

**5. The checked decision.** The default for consequential recommendations. Reasoning appropriate to the model (§9, or nothing on a reasoning model) → the recommendation with a stated reversal fact (Example 9.5) → a disconfirmation pass on a different model family (Example 21.5) → attach the surviving objection to the output.

**6. The triage front door.** The default when traffic is heterogeneous. A small schema-constrained router with a fallback class (§23) → dispatch to the stack above that fits → log the label distribution → per-class quality measurement, never a single average.

## 32. Choosing under constraint

When something has to give, these are the trades, in the order to make them.

**When latency is the binding constraint.** Drop self-consistency first — it multiplies cost by N, and waiting time as well if the samples run one after another. Then drop explicit CoT on reasoning models: Meincke et al. (Prompting Science Report 2, arXiv 2506.07142) measured requests taking 20–80% longer for changes of −3.3 to +3.1 percentage points on GPQA Diamond. Then consider Chain-of-Draft (§7) with few-shot examples, accepting a few points on arithmetic. Keep grounding and the cheap checks done in code; they cost little relative to what they prevent. Of the verification layers, multi-call ones such as Chain-of-Verification (§19, four calls) go first when latency binds. Skeleton-of-Thought is a latency technique specifically — it reports over 2× speed-up on 8 of 12 models tested.

**When cost is the binding constraint.** Route first (§23): send the easy majority to a small model. Then compress long RAG contexts (manual Section 8.4). Then reduce N in any voting scheme. Do not drop verification to save cost — measure what a wrong answer costs before deciding it is the expendable layer.

**When accuracy is the binding constraint.** Ground it first (§15) — information work is a large part of the ChatGPT usage data in §29, so missing information is a sensible first suspect, ahead of faulty reasoning. Then compute rather than generate anything numerical (§13). Then add independent verification (§19, §21). Add a reasoning topology last: its benefit on current models is the least consistent of these layers (manual Chapter 9). If answers vary between runs of the same input, sample candidates and select with a verifier (§34) before adding a topology.

**When you cannot measure.** Build the eval set. Everything in this guide is a guess without one, including the recommendations in this section. Fifty labeled examples that represent your real traffic are worth more than any technique here, and they are the prerequisite for knowing which of these techniques your task actually needs.

## 33. What to do first, in order

1. **Write the zero-shot prompt** with the residue handled (§1). Run it on 20 real inputs.
2. **Build a 50-example eval set** from real traffic, labeled by someone who knows the right answer.
3. **Measure the zero-shot baseline,** including variance across repeated runs.
4. **Ground it** if the failures are missing-information failures (§15). Re-measure.
5. **Constrain the output** if the failures are format failures (§18). Re-measure.
6. **Add examples** if the failures are shape failures (§2). Re-measure.
7. **Add computation** if the failures are arithmetic (§13). Re-measure.
8. **Add verification** proportional to what a wrong answer costs (§19, §20, §21). Re-measure.
9. **Set decoding deliberately** if the failures are variance failures — the same input gives different answers across runs. Lower the temperature where one answer is right, or draw several candidates and select with a verifier (§34). Re-measure.
10. **Add a reasoning topology** only if the failures are genuinely reasoning failures and the model is not a reasoning model (§9–§14). Re-measure.
11. **Orchestrate** only when a single call provably cannot do it (§22–§27). Re-measure.
12. **Optimize** only at volume, with the decision harness (Example 28.5). Re-measure on the untouched test slice.
13. **Re-measure everything on every model upgrade.** Gains reported on 2022-era models often shrink on current ones (manual Sections 7.2 and 9.1), and so may some of yours.

The re-measure step appears ten times on purpose. It is the only part of this guide that is not a guess.

## Sources for Part 7

- Chatterji, A., Cunningham, T., Deming, D., Hitzig, Z., Ong, C., Shan, C., & Wadman, K. (2025). *How People Use ChatGPT.* NBER Working Paper 34255. Sample: ~1.1M classified conversations, consumer plans (Free/Plus/Pro), May 2024 – June 2025. Excludes users under 18, opted-out users, and business/enterprise plans.
- Anthropic Economic Index report: *Cadences* (June 26, 2026). Artifact classification of chat and Cowork conversations sampled April 10 – June 10, 2026.
- Anthropic Economic Index report: *Learning curves* (March 2026). Claude.ai and first-party API traffic, February 5–12, 2026.

**Scope caution.** These three sources describe different products and user populations, sampled at different times (May 2024–June 2025; February 5–12, 2026; April 10–June 10, 2026), using different taxonomies — the first classifies the conversation’s topic, the second the artifact produced, the third the occupation associated with the task. Shares are not directly comparable across them and are reported separately throughout. Exclusions differ: the NBER sample excludes users under 18, opted-out users, and business/enterprise plans (as listed above), while the source notes for the two Anthropic reports state no exclusions, and *Learning curves* includes first-party API traffic. Do not assume either Anthropic sample excludes enterprise traffic. If your own traffic is a specialist workload, measure it rather than inheriting these distributions.

# Part 8 — Decoding and Review

## 34. Decoding Controls: Temperature, Candidates, and Reasoning Effort

**What it does and when to reach for it.** Decoding controls decide how an answer is drawn from the model once the prompt is fixed: how random each token choice is, how many candidate answers you draw, how you choose among them, and how much computation a reasoning model spends before answering. None of them changes a word of the prompt; all of them change the output. Reach for them when failures look like variance — the same input gives different answers on different runs — or when a cheap, reliable checker exists and you can afford several candidates. Know what the evidence says. Across nine models answering multiple-choice problems, raising temperature from 0.0 to 1.0 had no statistically significant effect on accuracy (Renze and Guven, Findings of EMNLP 2024); that result covers multiple-choice problem solving and does not show that temperature is irrelevant for open-ended generation. Temperature 0 does not guarantee identical reruns: 1,000 temperature-0 completions of one prompt to Qwen3-235B-A22B-Instruct-2507 produced 80 different outputs, because the server’s batching changed the arithmetic (Thinking Machines Lab, September 2025). Selecting among sampled solutions with a trained verifier gave a gain on grade-school math that its authors equate to a 30× larger model (Cobbe et al., 2021). And extra reasoning computation pays most where the model already succeeds some of the time (Snell et al., 2024). The manual treats all of this as its own axis (Chapter 10).

**Build steps.**

1. **Classify the call.** Does it have one correct answer (extraction, classification, arithmetic) or many acceptable ones (ideas, drafts)?
2. **For single-answer calls,** set temperature at or near 0, draw one candidate, and validate every run — do not assume a rerun will match.
3. **For many-answer calls,** keep the provider’s default temperature, raise it only if outputs repeat themselves, and draw several candidates for a later step to choose among.
4. **Write the selector before you sample:** tests, a validator, an exact-match check against the source, or a judge rubric. Without a selector, extra candidates only add cost.
5. **Choose N by measurement.** Start at 3 to 5 and raise it only while the selector’s pass rate keeps rising.
6. **On reasoning models, set effort by measurement,** starting from the provider’s default. Raise it only where accuracy is below target and the model already succeeds some of the time. Parameter names and allowed values differ across providers and model versions; read the current documentation.
7. **Log the decoding settings with every result,** so that a change in quality can be traced to a change in settings.

**Combines with.** Schema-constrained generation (§18) for format. Self-consistency (§10) when agreement between candidates is the selector; an LLM judge (§20) when quality is. Routing (§23) to send easy traffic to low effort. Conflicts with using temperature to fix what is really a grounding or prompt problem.

### Example 34.1 — Single-answer extraction with a rerun audit (insurance claims)

```
SETTINGS: temperature 0; 1 candidate; JSON schema enforced (§18):
  {"type": "object",
   "required": ["policy_number", "incident_date", "claimed_amount"],
   "properties": {
     "policy_number": {"type": ["string", "null"]},
     "incident_date": {"type": ["string", "null"],
                       "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
     "claimed_amount": {"type": ["string", "null"]}},
   "additionalProperties": false}
LOG (code): store these settings with every result.
AUDIT (code): re-run 1 input in 50 and compare the two outputs.

Extract these fields from the claim form below:
policy_number, incident_date, claimed_amount.

Write incident_date as YYYY-MM-DD. Copy the other two values
exactly as the form states them.
Use null for any field the form does not state.
Return a single JSON object with exactly those three keys.

Claim form:
{claim_form_text}
```

*Shows:* steps 1, 2, 7. The audit measures how often reruns disagree instead of assuming they never do.

*Check:* the audit’s disagreement rate. Any disagreement at temperature 0 means every output needs validation, because no single run can be trusted to be the run you would get again.

### Example 34.2 — Candidates plus a separate selector (email marketing)

```
CALL 1 — run 5 times at the provider's default temperature:
  Write one subject line for the email below.
  Rules: under 60 characters; no exclamation marks;
  no discount language.
  Email: {email_body}

CODE: remove duplicates and any line that is 60 or more
characters, contains "!", or contains a word on
{discount_word_list}.

CALL 2 — judge, once per surviving line, on a different model:
  Score the subject line from 1 to 5 for how clearly it states
  the email's single main point. Return only the number.
  Email: {email_body}
  Subject line: {candidate}

CODE: keep the highest-scoring line; on a tie, keep the
shorter one. If no line survived, return NONE.
```

*Shows:* steps 3, 4, 5. The mechanical rules are checked in code, with a word list standing in for “discount language”; only judgment is left to the judge, and the tie-break completes the selector.

*Check:* the judge against your own ratings of 20 subject lines before trusting its scores.

### Example 34.3 — Best-of-N code with tests as the selector (software)

```
CALL — run 4 times at the provider's default temperature (raise
it only if the four outputs come back identical):
  Write a Python function with this signature:

  def normalize_phone(raw: str) -> str

  Return a US phone number in E.164 form:
  "(415) 555-0100"  -> "+14155550100"
  "415.555.0100"    -> "+14155550100"
  "+1 415 555 0100" -> "+14155550100"
  Raise ValueError unless the input contains exactly 10 digits,
  or 11 digits beginning with 1.
  Return only the function.

CODE: run {test_file} against each candidate and return the
first one that passes every test. If none passes, return FAILED
with the test output of the best attempt.
```

*Shows:* steps 3–5. Selection rests on execution, not on how convincing the code looks.

*Check:* the tests themselves. Best-of-N returns whatever passes, so a case the tests miss is a case a wrong candidate can slip through.

### Example 34.4 — Choosing reasoning effort by measurement (customer support)

```
EVALUATION (in code, before launch):
  Data: 50 refund-policy questions, each with a verified answer;
  the same 50 at every setting.
  For each effort setting the provider offers, lowest first:
    run every question 3 times; record accuracy (mean number
    correct out of 50), median latency, and cost per question.
  Fix the tolerance in questions before you look at results, for
  example 2 of 50. Choose the lowest setting whose accuracy is
  within that tolerance of the best setting's and whose median
  latency fits an 8-second budget. Repeat after every model
  update.

PROMPT (identical at every setting):
  Answer the customer's question using only the policy below.
  If the policy does not answer it, reply exactly:
  NOT COVERED BY POLICY
  Policy: {refund_policy}
  Question: {question}
```

*Shows:* steps 6 and 7. The prompt stays fixed, so the table measures decoding alone.

*Check:* that the table is rebuilt after a model update. An effort setting chosen for one model version says nothing about the next.

### Example 34.5 — Routing effort by difficulty (IT help desk)

```
ROUTER - small model, temperature 0, returns one label:
  Label the ticket ROUTINE or DIAGNOSTIC.
  ROUTINE: a password reset, an access request, or a question the
  runbook excerpt answers directly.
  DIAGNOSTIC: anything that needs reasoning over logs or
  configuration.
  Return only the label.
  Runbook excerpt: {runbook_excerpt}
  Ticket: {ticket}

ROUTINE    -> non-reasoning model, temperature 0, grounded on the
              runbook excerpt.
DIAGNOSTIC -> reasoning model at the provider's default effort
              (choose the setting as in Example 34.4), grounded on
              the logs attached to the ticket.
Log accuracy separately for each path.
```

*Shows:* step 6, combined with routing (§23).

*Check:* how often DIAGNOSTIC tickets are labeled ROUTINE. That is the costly error, because those tickets get the cheap path and a confident wrong answer.

## 35. Independent Parallel Review

**What it does and when to reach for it.** Independent review sends the same material to several reviewers — different models, or fresh sessions — none of which sees another’s output, and then checks their findings against primary sources. It replaces the serial relay, in which each model revises the previous model’s output. Relays have known failure modes. Texts passed along chains of language models drift toward *attractors*, properties such as toxicity, positivity, difficulty, and length that successive rewrites converge on (Perez et al., ICLR 2025). Model evaluators favor their own generations (Panickssery et al., NeurIPS 2024), and preference-trained assistants lean toward the view the user states (Sharma et al., ICLR 2024). Agreement reached in a relay is therefore weak evidence. Reach for independent review for any document, prompt, or decision where several models are available and an error is costly. The manual’s Section 13.6 gives the evidence in full.

**Build steps.**

1. **Freeze the material.** Every reviewer gets the identical document and source list, and nothing written by another reviewer.
2. **Give a rubric and an answer key, not a persona:** numbered checks, plus the facts that must be stated correctly.
3. **Demand findings in a fixed table** — location, problem, evidence, severity — with “none found” for any rubric line that produces nothing.
4. **Run the reviewers in parallel,** in fresh sessions, on at least two model families.
5. **Merge the findings,** grouping duplicates and keeping every finding that only one reviewer made.
6. **Adjudicate each finding against the primary source,** never on a reviewer’s authority or a vote count.
7. **Investigate disagreements first, and record rejected findings with the reason,** so the adjudication in the next round does not argue them again. Reviewers in that round still see only the frozen material.

**Combines with.** The disconfirmation pass (§21) as one reviewer’s role. An LLM judge (§20) for scoring. Chain-of-Verification (§19) for questions of fact. Conflicts with serial relays, and with any step that shows one reviewer’s output to another before adjudication.

### Example 35.1 — Checking a summary against an answer key (research)

```
You are one of several independent reviewers. You will not see
the other reviews.

Check the summary below against the answer key. For each key item,
report exactly one verdict:
CORRECT   - the summary states it with its scope intact
DISTORTED - the summary states it wrongly; quote the sentence
ABSENT    - the summary does not state it

Then list every claim in the summary that neither the key nor the
source excerpts support.

Return a table: key_id | verdict | quoted sentence | note

Answer key: {answer_key}
Summary: {summary}
Source excerpts: {source_excerpts}
```

*Shows:* steps 1, 2, 3. The key, not the reviewer’s judgment, defines what correct means.

*Check:* three verdicts by hand against the sources before trusting the rest of the table.

### Example 35.2 — Parallel code review across model families (software)

```
SEND TO EACH REVIEWER (two or three model families, fresh sessions):

  Review the diff below for defects only: logic errors, unhandled
  inputs, and security issues. Do not comment on style.
  For each defect give: file:line | defect | an input that
  triggers it | severity (HIGH, MEDIUM, LOW).
  If you find none, write NONE FOUND.

  Diff:
  {diff}

MERGE (code): group findings by file:line. Keep findings that only
one reviewer reported.
ADJUDICATE: check every kept finding against the code. Reproduce
each HIGH finding with its triggering input before acting on it.
```

*Shows:* steps 3–6. Requiring a triggering input makes every finding testable.

*Check:* the findings only one reviewer made. A defect that one reviewer alone caught is the reason to run several; a majority vote would have thrown it away.

### Example 35.3 — Contract review against a checklist (legal operations)

```
Review the contract excerpt below against the checklist. For each
item answer PRESENT, NOT IN EXCERPT, or UNCLEAR. For PRESENT and
UNCLEAR, quote the clause that decides it, exactly; do not
paraphrase. For NOT IN EXCERPT, leave the quote empty: absence
from an excerpt is not absence from the contract.

Checklist:
1. The limitation of liability states a cap.
2. Either party may terminate for convenience with notice.
3. The governing law is named.
4. Auto-renewal can be cancelled by giving notice.
5. The data-processing terms set a breach-notification deadline.

Return a table: item | verdict | quoted clause | note

Contract excerpt:
{contract_text}
```

*Shows:* steps 2 and 3. A fixed checklist with quoted evidence makes two reviewers’ tables directly comparable.

*Check:* every quotation against the contract text in code. A quotation that does not appear word for word is an invalid finding, whatever it concludes. NOT IN EXCERPT rows have no quotation to check; check those against the full contract.

### Example 35.4 — The adjudication record (any domain)

```
ADJUDICATION TABLE - one row per merged finding:

finding_id | reported by | claim | primary source checked |
verdict (ACCEPT, REJECT, NEEDS SOURCE) | reason | fix applied

Rules:
- Accept a finding only when the primary source confirms it.
- Never accept a finding because several reviewers made it.
- Keep rejected findings, with their reasons, in this table so
  the adjudicator does not argue them again. Do not show the
  table to the next round's reviewers; they get only the frozen
  document and the rubric.
```

*Shows:* steps 6 and 7.

*Check:* that every ACCEPT row names a source someone actually opened, not a reviewer’s citation of one.

### Example 35.5 — Replacing a relay with a parallel round (editorial workflow)

```
BEFORE - serial relay (avoid):
  Model A drafts -> Model B revises A's draft -> Model C revises
  B's revision -> "all three models agree."

AFTER - independent review:
  1. Model A drafts. Freeze the draft.
  2. Models B and C each receive the frozen draft, the source list,
     and the rubric - never each other's output.
  3. Merge B's and C's findings into one table.
  4. The author checks each finding against the sources and
     revises once.
  5. If the revision is large, run a fresh round on the new draft
     with the same rubric and without the earlier findings.
```

*Shows:* steps 1, 4, and 6.

*Check:* whether any reviewer’s text reached another reviewer’s context. If it did, the round was a relay, and its agreement counts for little.

## Sources for Part 8

- Renze, M., & Guven, E. (2024). *The Effect of Sampling Temperature on Problem Solving in Large Language Models.* Findings of EMNLP 2024, pp. 7346–7356; arXiv 2402.05201.
- He, H. (2025). *Defeating Nondeterminism in LLM Inference.* Thinking Machines Lab, September 2025 (company technical report).
- Cobbe, K., et al. (2021). *Training Verifiers to Solve Math Word Problems.* arXiv 2110.14168.
- Snell, C., et al. (2024). *Scaling LLM Test-Time Compute Optimally Can Be More Effective than Scaling Model Parameters.* arXiv 2408.03314.
- Perez, J., et al. (2025). *When LLMs Play the Telephone Game: Cumulative Changes and Attractors in Iterated Cultural Transmissions.* ICLR 2025; arXiv 2407.04503.
- Panickssery, A., Bowman, S. R., & Feng, S. (2024). *LLM Evaluators Recognize and Favor Their Own Generations.* NeurIPS 2024; arXiv 2404.13076.
- Sharma, M., et al. (2024). *Towards Understanding Sycophancy in Language Models.* ICLR 2024; arXiv 2310.13548.
- OpenAI and Anthropic documentation on reasoning effort and extended thinking, read September 2026. Parameter names and allowed values change between model versions.

## Changes from the first edition

| **Where** | **First edition** | **This edition** |
|---|---|---|
| §5 | Prohibitions fail because they “raise the salience of the very tokens they forbid” | Salience is a hypothesis; the evidence is vendor guidance and falling compliance as rule lists grow (manual Section 7.5) |
| §3 | Zheng et al. tested personas on “2,410 factual questions” | 2,410 multiple-choice MMLU questions, four open-source model families, published version cited |
| §2 | Few-shot gives only a format gain “on strong recent models” | Scoped to mathematical reasoning with Qwen2.5-series models |
| §7 | Chain-of-Draft “matched or beat” CoT on date understanding | Date understanding split: ahead on Claude 3.5 Sonnet, behind on GPT-4o |
| §7 | Self-consistency on Chain-of-Draft “partly buys back the accuracy gap” | Untested in the paper; marked as something to measure |
| Example 7.2 | A 45-day notice starting 2026-01-20 ended 2026-03-06 | The start date counts as day 1, so the last day is 2026-03-05 |
| Example 7.4 | “3 years tenure” with a 2024 hire date | Hire date 2023-02-01, consistent with the stated tenure |
| §10 | “At temperature 0 every path is the same path” | Paths are “nearly identical” at temperature 0, so the vote adds nothing; that reruns are not guaranteed to match is covered in §34 (manual Section 10.1) |
| §28 | OPRO “underperformed plain CoT baselines” on three small models | Adds that it beat both baselines on LLaMa-2-7B and Gemini-Pro, when small models were their own optimizers |
| §29 | Self-Expression listed as “flat” | The paper does not characterize its trend; Self-Expression (a topic) is distinguished from Expressing (an intent) |
| §29 | “No distinct artifact, ~7%” | Marked as the complement of the report’s stated 93%, not a quoted figure; the March 2026 report is named (“Learning curves”) |
| §30 | “~42% work / 44% personal” and “44% work / 49% personal” without their meaning | Removed: Part 7 names no source or period for them, and each pair leaves part of the total unexplained |
| §33 | “The re-measure step appears eleven times” | A decoding step was added, and the count is now correct: ten |
| §4, §13, §19–§21, §23–§32 | Several recommendations worded as measured findings (“highest-value,” “strongest,” “the easy 80%”) | Worded as the advice they are |
| Throughout | Manual cross-references to the second edition | Updated to the manual’s third edition |
| Part 8 | — | New: decoding controls (§34) and independent parallel review (§35), ten worked examples |

## Post-edition note (October 20, 2026)

| **Where** | **This edition said** | **Note** |
|---|---|---|
| §18 | Constrained output *cannot* violate the schema | Vendors document exceptions: Anthropic lists refusals and output cut off at `max_tokens`; OpenAI documents refusals. Found by the AI Engineering Stack series, Part 03 (claude/engineering-stack-part-03-prompts-as-interfaces.md), and held until the series finished; the manual's Section 10.5 carries the same note |

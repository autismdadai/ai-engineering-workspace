# Practical Prompt Frameworks (Companion Reference)

Quick, everyday prompt formulas, adapted from a practitioner prompt-engineering guide (the source guide is not in this project). They are practitioner patterns, not tested techniques: their evidence class is practitioner mnemonic. Use them for fast everyday work, or as building blocks inside the prompt generator. For anything that matters, upgrade the prompt to the seven-axis structure with a success check.

**Changed from the source.** Role and persona lines ("You are an expert ...", "I want you to act as ...") are replaced by a stated standard of work. In a test of 162 personas on 2,410 MMLU questions across four model families, adding a persona did not improve accuracy (Zheng et al., Findings of EMNLP 2024). A role can still shape tone; say the tone you want directly instead.

When a task has one correct answer, or when variation between runs is costly, also state decoding choices: a low temperature, how many candidates, and how one is chosen. Temperature 0 does not guarantee identical reruns.

## 1. Task–Result–Goal–Context–Constraints

A general structure for any task.

```
Task: [what to do, as a verb]
Result: [the deliverable and its format]
Goal: [what the result is for]
Context: [who reads it and where it will be used]
Constraints: [length, vocabulary, what must be preserved, what to do with missing information]
Standard: [the level of expertise the result must reflect, e.g. "accurate enough for a practicing accountant"]
```

Example:

```
Task: Summarize the attached architecture document.
Result: A one-page executive summary, at most 400 words.
Goal: Help a non-technical executive decide whether to fund the next phase.
Context: A board packet.
Constraints: Define any technical term in plain language. End with three clear decision options. If the document does not state a cost, write "cost not stated" rather than estimating.
Standard: Accurate enough that the engineering lead would sign off on it.
```

## 2. Input–Task–Style pattern

```
I will give you [INPUT DESCRIPTION].
You will [TASK]
in a [TONE / STYLE] style.
The important details are: [KEY CONSTRAINTS AND FACTS].
```

Refine with follow-ups such as "Be more precise", "Put the most important keywords in bold", or "Now put this in a table".

## 3. Shot prompting

- **Zero-shot:** no examples; clear instructions and rules for unusual input.
- **One-shot:** one example of the input-to-output shape.
- **Few-shot:** 2–5 examples covering the main boundary cases (typical, edge, failure).

Say whether the examples are illustrative or must be copied exactly.

## 4. Chain-of-Thought (basic)

Add: "Explain your reasoning in numbered steps before giving the final answer."

On reasoning models this usually adds time without adding accuracy (Meincke et al., 2025); test it on your own task. Visible reasoning is generated text, not a verified record of how the answer was reached, so check high-stakes answers independently.

## 5. Ask-Before-Answer

```
Before answering, if anything about the task, the missing information, or the best way to deliver the answer is unclear, ask me clarifying questions as a bulleted list. Do not produce the final answer until I have replied.
```

Then give the actual task.

## 6. Prompt improver (fill-in-the-blank)

```
What additional details could I add to the prompt below to improve the output and reduce ambiguity? List them as bullet points. Then rewrite the prompt as a fill-in-the-blank template.

Prompt: [PROMPT]
```

## 7. Perspectives

- One view: "Write about [TOPIC] from the perspective of [SPECIFIC STAKEHOLDER OR DISCIPLINE]."
- Several views: "Write an argument for and against [TOPIC] that fairly presents at least three distinct perspectives. Name each perspective and its core claims."

## 8. Constructive critique

```
Critique the content below against the standards of [DOMAIN]. Explain where it is weak or incomplete, then give concrete improvements. Address each major section separately.
Purpose and audience: [PURPOSE AND AUDIENCE]
Content:
[CONTENT]
```

## 9. Comparison table

```
Compare the two items below in a single table with these columns: Similarities, Differences, Qualitative characteristics, Quantitative factors, Impact, Key takeaways.
Item A: [A]
Item B: [B]
```

## 10. Reverse prompting (style capture)

```
Read the text below. Write a prompt that, used on a fresh model, would produce text with the same tone, style, sentence structure, length, and rhetorical pattern. Be specific. Reply only with the prompt.
Text:
[TEXT]
```

## 11. Revision commands (after the first output)

- Put the most important keywords in **bold**.
- Organize this by [date / location / price / priority].
- Give more unusual options.
- Explain this for a beginner / for an expert.
- Put this in a table with relevant columns.
- Rewrite this to be more formal / more casual / shorter.
- Add a short success check at the end.
- Summarize as three bullet takeaways.

## Using these inside the prompt generator

- Keep the 10 fixed topics and the Topic 10 audit layer.
- These formulas work as variation patterns in Topics 1, 2, 3, 6, 8, and 9.
- Attach a **Success check** to every prompt.
- Grade factual claims with SUPPORTED / PARTIALLY_SUPPORTED / CONTRADICTED / UNVERIFIED.

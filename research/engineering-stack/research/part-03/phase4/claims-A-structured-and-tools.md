# Claims to check

Each numbered claim cites source keys. Sources are listed at the end.

1. **T02, structured outputs and tool calling.** A model writes text. A program needs data: a field it can read, a value from a fixed list. Structured output is the agreement that closes that gap. You give the model a **schema**, a written description of the shape the answer must take, and the vendor's software makes the model's output follow it .  [sources: ASO, OSO]
2. Tool calling uses the same idea in the other direction: you describe a function (its name, what it's for, and a schema for its inputs), the model replies with a request to call it, and **your program** runs it .  [sources: ATD, OFC]
3. | A written description of the shape data must have | Schema; JSON Schema | The current JSON Schema version is 2020-12 . |  [sources: JSS]
4. | Making the model's output follow a schema as it is written | Structured outputs; constrained decoding | Anthropic: "guarantee schema-compliant responses through constrained decoding" . |  [sources: ASO]
5. | A setting that only promises valid JSON, not your schema | JSON mode | OpenAI: "only Structured Outputs ensure schema adherence" . |  [sources: OSO]
6. | The model asking your program to run a function | Tool call; function call | Anthropic's `tool_use` block; OpenAI's function call . |  [sources: ATD, OFC]
7. | The description of one tool the model may call | Tool definition | Name, description and an input schema . |  [sources: ATD, OFC]
8. | What your program sends back after running a tool | Tool result | Anthropic's `tool_result`, with `is_error` for failures . |  [sources: AHT]
9. | A setting that makes the model follow your tool's input schema exactly | Strict tool use; strict mode | `"strict": true` on the tool . |  [sources: ASO, OFC]
10. | Checking data against a schema in your own code | Validation | Pydantic and jsonschema are common Python libraries . |  [sources: JSL, PYD]
11. | A rulebook that tells a local model which tokens are allowed next | Grammar; GBNF | llama.cpp's format . |  [sources: LCG]
12. **Write the schema in code, not by hand.** In Python, Pydantic turns a class into this schema with `model_json_schema()` and checks a reply with `model_validate_json()`, which raises `ValidationError` when the reply doesn't fit .  [sources: PYD]
13. Pydantic writes JSON Schema 2020-12 by default , and the jsonschema library validates against 2020-12 by default .  [sources: JSL, PYD]
14. | 2. JSON mode | A setting that forces valid JSON | Valid JSON, not your fields. Ollama: "the output will always be a well-formed JSON object", and you should still ask for JSON in the prompt |  [sources: OLL]
15. | 3. Structured outputs (strict) | Send the schema as an API setting | The shape of your schema, with the exceptions below |  [sources: ASO, OSO]
16. - **Anthropic:** `output_config={"format": {"type": "json_schema", "schema": {...}}}` for the reply, or `"strict": true` on a tool. The older `output_format` parameter is deprecated and returns a 400 error without a beta header .  [sources: ASO]
17. - **OpenAI, Responses API:** `text: {format: {type: "json_schema", strict: true, schema: ...}}`. In Chat Completions, `response_format` .  [sources: OSO]
18. **What it guarantees, and the exceptions.** Anthropic: "Structured outputs guarantee schema-compliant responses through constrained decoding", and also "there are scenarios where the output may not match your schema" .  [sources: ASO]
19. 1. **A refusal.** Anthropic returns `stop_reason: "refusal"`, bills the request, and "the output may not match your schema" .  [sources: ASO]
20. OpenAI: "a refusal does not necessarily follow the schema you have supplied" .  [sources: OSO]
21. 2. **Running out of room.** With `stop_reason: "max_tokens"`, the output "may be incomplete"; retry with a higher `max_tokens` .  [sources: ASO]
22. 3. **Capitalization of fixed values.** Anthropic: "Structured outputs don't guarantee the capitalization of string enum and const values" .  [sources: ASO]
23. **Each vendor supports only part of JSON Schema.** OpenAI: "Structured Outputs supports a subset of the JSON Schema language" .  [sources: OSO]
24. | `additionalProperties: false` on every object | Required | Required |  [sources: ASO, OFC]
25. | Every property listed in `required` | Not stated | Required; make a field optional by allowing `null` |  [sources: ASO, OFC]
26. | `minimum`, `maximum`, `multipleOf` | Not supported | Supported |  [sources: ASO, OSO]
27. | `minLength`, `maxLength` | Not supported | Not in its supported list |  [sources: ASO, OSO]
28. | Array limits | Only `minItems` of 0 or 1 | `minItems`, `maxItems` |  [sources: ASO, OSO]
29. | Recursive schemas; external `$ref` | Not supported | Not checked |  [sources: ASO]
30. | Size limits | 20 strict tools, 24 optional parameters, 16 union-type parameters per request | Not found in the text read |  [sources: ASO]
31. A keyword your vendor doesn't enforce can still go in the schema you validate with in your own code. That is how Pydantic's and OpenAI's SDK helpers work: OpenAI's Python SDK rewrites a Pydantic schema into strict form before sending it , and Anthropic's SDK helpers send "a simplified schema" while "a helper that validates responses still enforces every constraint in your code" .  [sources: ASO, OSDK]
32. **Can a prompt force a token instead?** No. A prompt shifts the model's probabilities softly. Hard control lives in settings. OpenAI's `logit_bias` adds a value from -100 to 100 to a token's score before sampling; at -100 or 100 the token is effectively banned or forced .  [sources: OAPI]
33. It exists in Chat Completions and the legacy Completions API, not in the Responses API's request schema .  [sources: OAPI]
34. The diagram renders with mermaid-cli 12.0.0 . OpenAI's guide lists the same loop in five steps, from "Make a request to the model with tools it could call" to "Receive a final response from the model (or more tool calls)" .  [sources: OFC]
35. **A tool definition.** Anthropic's fields are `name`, `description` and `input_schema`, plus optional ones such as `strict` and `input_examples`; a name must match `^[a-zA-Z0-9_-]{1,128}$` .  [sources: ATD, ATR]
36. OpenAI's are `type` (always `function`), `name`, `description`, `parameters` and `strict` .  [sources: OFC]
37. Sources: .  [sources: ATD, OFC]
38. **A change worth knowing (read October 12, 2026).** On Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1, `any` and `tool` "return a 400 error"; Anthropic's suggested replacement is `auto` with strict tool use, or structured outputs for a fixed JSON reply .  [sources: ATD]
39. On models that do accept a forced tool, "Forcing a tool also skips thinking" .  [sources: ATD]
40. **Several calls at once.** Both vendors allow parallel tool calls by default. Anthropic turns them off with `disable_parallel_tool_use: true` inside `tool_choice`, "not a top-level request parameter" ; OpenAI with `parallel_tool_calls: false` .  [sources: APT, OFC]
41. OpenAI's advice: "it is best practice to assume there are several" .  [sources: OFC]
42. **Sending results back.** Anthropic: every `tool_result` goes in the next user message, before any text, and `is_error: true` marks a tool that failed .  [sources: AHT, APT]
43. Anthropic says Claude "will retry 2-3 times with corrections" after an invalid call ; that is the vendor's description of its model, not a measurement here.  [sources: AHT]
44. **How many tools.** OpenAI: "Aim for fewer than 20 functions available at the start of a turn at any one time, though this is just a soft suggestion" .  [sources: OFC]
45. **Strict mode for tools.** OpenAI's guide says Responses requests "will attempt to normalize your schema into strict mode" when possible, while Chat Completions is non-strict by default .  [sources: OFC]
46. - **llama.cpp** constrains output with grammars written in its GBNF format, and "supports converting a subset of" JSON Schema to them .  [sources: LCG]
47. Its limits: "Unsupported features are skipped silently"; `minimum` and `maximum` work only for integers .  [sources: LCG]
48. And for `response_format`, "The model has no visibility into the schema": describe the fields in the prompt too .  [sources: LCG]
49. - **Ollama** takes a JSON Schema in its `format` parameter, and its docs advise: "It is ideal to also pass the JSON schema as a string in the prompt" .  [sources: OLL]
50. Its documented example builds the schema with Pydantic's `model_json_schema()` and checks the reply with `model_validate_json()` .  [sources: OLL]
51. - **Outlines** (Apache-2.0) constrains generation for local models; for server-based models, "we have limited control over text generation and some output types are not supported" .  [sources: OUT]
52. **Coverage differs a lot.** JSONSchemaBench (a 2025 preprint) ran 10,000 real-world schemas through six engines. On its "GitHub Hard" set with Llama-3.2-1B-Instruct, the share of schemas each engine handled correctly ran from 0.03 (Outlines) to 0.41 (Guidance); OpenAI's API handled 0.09, but every schema it accepted, it followed (compliance 1.00) .  [sources: JSB]
53. The authors note the open engines and the hosted APIs ran on different models, so the rows aren't directly comparable , and vendor support has changed since early 2025.  [sources: JSB]
54. | Tam et al., "Let Me Speak Freely?" (EMNLP 2024 Industry Track) | gpt-3.5-turbo-0125, claude-3-haiku-20240307, gemini-1.5-flash, LLaMA-3-8B-Instruct and Gemma-2-9B-Instruct; reasoning tasks (GSM8K, Last Letter, Shuffled Objects) and classification tasks | "a significant decline in LLMs' reasoning abilities under format restrictions"; on classification, JSON mode "performs competitively, and in some cases, surpasses" free text |  [sources: TAM]
55. | dottxt, "Say What You Mean" (vendor blog; dottxt sells structured generation) | A re-run with Llama-3-8B-Instruct | Argues the paper "confuses structured generation with JSON-mode"; reports GSM8K 0.77 unstructured against 0.78 structured |  [sources: DTX]
56. | JSONSchemaBench (preprint, 2025) | Llama-3.1-8B-Instruct; GSM8K, Last Letters, Shuffle Objects | Constrained decoding scored higher with every engine: GSM8K 80.1% unconstrained against 81.6% to 83.8% constrained, a gain of 1.5 to 3.7 percentage points |  [sources: JSB]
57. **What to do.** Two habits make the debate matter less. First, let the model reason in free text and put only the final answer in a structured field, or ask for reasoning in a separate call; Anthropic warns that a schema field asking for reasoning may trigger a refusal, and suggests asking "for a short explanation instead" .  [sources: ASO]
58. | Zero-shot role prompting "enforces output determinism" for JSON ticket routing (P1-09) | Unsupported. Format comes from schema settings, not roles ; Claude's newest models reject any non-default temperature ; and outputs vary even at temperature 0 (Part 02, Section 3.8) | 3.2, 3.6 |  [sources: ASO, ATK, OSO]
59. | A system prompt can "severely penalize" out-of-character tokens (P1-11) | Corrected. A prompt shifts probabilities softly; `logit_bias` (Chat Completions only) or constrained decoding gives hard control | 3.2 |  [sources: OAPI]
60. | Schema enforcement bridges text and "deterministic software execution" (P1-15) | Overstated. Strict schemas guarantee the shape, with documented exceptions (refusal, `max_tokens`) ; not correct values, and not identical reruns | 3.2 |  [sources: ASO, OSO]
61. | In ReAct, tools are "strictly mapped via JSON schemas" (P6-02) | Corrected. ReAct (ICLR 2023) used plain-text actions such as `search[entity]` and `finish[answer]` . JSON Schema tool definitions belong to today's APIs | 3.3 |  [sources: ATD, OFC, REA]
62. 1. **Extraction with tool use** (Anthropic cookbook, "Extracting Structured JSON using Claude and Tool Use"): summaries, named entities, sentiment and classification, each returned through a tool's input schema .  [sources: ACB]
63. 2. **Validating tool input with Pydantic** (Anthropic cookbook, "Note-Saving Tool with Pydantic"): the program checks the model's tool call against a Pydantic model before saving .  [sources: ACB]
64. 3. **Structured outputs, refusals included** (OpenAI cookbook, "Introduction to Structured Outputs"): a maths tutor's steps, summaries and entity extraction, with code that checks for a refusal. Its text dates from the 2024 launch .  [sources: OCB]
65. 4. **A local model** (Ollama docs, "Extract structured data"): a Pydantic schema passed as `format`, the reply checked with `model_validate_json()` .  [sources: OLL]
66. - **Best default for a solo builder:** your vendor's strict structured outputs or strict tools, plus Pydantic to build the schema and check every reply .  [sources: ASO, OSO, PYD]
67. - **For a local model:** Ollama's `format` with a Pydantic schema, the schema repeated in the prompt, and validation on every reply .  [sources: OLL]
68. Test your schema on your engine: coverage varies widely .  [sources: JSB]
69. - *"Strict mode means I don't need to validate."* Refusals and `max_tokens` cut-offs can break the schema , and no schema checks that a value is true.  [sources: ASO, OSO]
70. - *"Forcing a tool is the way to get JSON from Claude."* On the newest Claude models it returns a 400 error; use structured outputs .  [sources: ATD]
71. - *"A local model given a schema follows all of it."* llama.cpp skips unsupported keywords silently .  [sources: LCG]
72. 1. *A schema has `"properties": {"queue": ..., "notes": {"type": "string"}}` and `"required": ["queue"]`, with `additionalProperties` false. What does `schema_lint.py` report, and how do you fix it without making `notes` mandatory?* Answer: OpenAI's column reports `$: not in required: notes`, Anthropic's is empty, exit code 1. Fix: add `notes` to `required` and give it `"type": ["string", "null"]`, so the model can send `null`; the linter then reports `"ok": true` . This is OpenAI's documented way to make a field optional .  [sources: OFC]
73. *Answers.* (1) Extra fields the schema doesn't name; both Anthropic and OpenAI require it .  [sources: ASO, OFC]
74. (2) A refusal, a `max_tokens` cut-off, and (Anthropic) the capitalization of enum values .  [sources: ASO, OSO]
75. (3) Your program, which is where every check and permission belongs .  [sources: OFC]
76. - Anthropic, "Structured outputs": https://platform.claude.com/docs/en/build-with-claude/structured-outputs  [sources: ASO]
77. - OpenAI, "Structured Outputs" and "Function calling": https://developers.openai.com/api/docs/guides/structured-outputs ; https://developers.openai.com/api/docs/guides/function-calling  [sources: OFC, OSO]
78. - **Guarantees have edges.** Strict structured output is the strongest format guarantee on offer, and both vendors document cases where it doesn't hold .  [sources: ASO, OSO]
79. Local engines enforce less, and silently .  [sources: JSB, LCG]
80. - **Format against quality is unsettled.** One peer-reviewed industry-track study found format restrictions hurt reasoning ; a vendor's re-run and a later preprint found none or a small gain .  [sources: DTX, JSB, TAM]
81. - **Vendors change the rules quickly.** Within this series' writing, Anthropic retired manual thinking budgets, locked sampling settings and refused forced tools on its newest models .  [sources: ATD, ATK, AXT]
82. - **Costs.** Reasoning tokens are billed even when hidden ; a single optimizer run can cost hundreds of dollars .  [sources: ATK, DSD, ORS]
83. 1. The guide (§18) and the taxonomy (§10.5) say constrained decoding means the output "cannot" violate the schema. Anthropic's and OpenAI's current pages list exceptions (refusal, `max_tokens`) .  [sources: ASO, OSO]
84. A **schema-contract** skill could take a description of the data a program needs, write the Pydantic model and its JSON Schema, run a linter like `schema_lint.py` against the target vendor's strict rules, and print the code that validates replies and handles refusals and `max_tokens`. The script does the checking; the skill does the explaining. claude/new-skills-appendix.md has no such idea .  [sources: project file]

## Sources

- ACB: Anthropic cookbook (github.com/anthropics/claude-cookbooks): tool_use/extracting_structured_json.ipynb and tool_use/tool_use_with_pydantic.ipynb (class OD)
- AHT: Anthropic, "Handle tool calls". https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls (class OD)
- APT: Anthropic, "Parallel tool use". https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use (class OD)
- ASO: Anthropic, "Structured outputs". https://platform.claude.com/docs/en/build-with-claude/structured-outputs (class OD)
- ATD: Anthropic, "Define tools", including "Forcing tool use". https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools (class OD)
- ATK: Anthropic, "Thinking". https://platform.claude.com/docs/en/build-with-claude/thinking (class OD)
- ATR: Anthropic, "Tool reference". https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference (class OD)
- AXT: Anthropic, "Extended thinking". https://platform.claude.com/docs/en/build-with-claude/extended-thinking (class OD)
- DSD: DSPy documentation in the repository at commit 1dcdf86 (github.com/stanfordnlp/dspy, docs/docs/): learn/programming/signatures.md, modules.md, language_models.md; learn/evaluation/metrics.md; learn/optimization/optimizers.md, overview.md; diving-deeper/choosing-an-optimizer.md; api/optimizers/MIPROv2.md, GEPA/overview.md; tutorials agents, rag (class OD)
- DTX: Kurt, "Say What You Mean: A Response to 'Let Me Speak Freely'", dottxt blog (undated). https://blog.dottxt.ai/say-what-you-mean.html (class VB)
- JSB: Geng et al., "Generating Structured Outputs from Language Models: Benchmark and Studies" (JSONSchemaBench), arXiv 2501.10868v3, February 2025. https://arxiv.org/abs/2501.10868 (class PP)
- JSL: python-jsonschema README and validators.py (github.com/python-jsonschema/jsonschema) (class OD)
- JSS: JSON Schema, "Specification". https://json-schema.org/specification (class OD)
- LCG: llama.cpp, grammars/README.md (github.com/ggml-org/llama.cpp) (class OD)
- OAPI: OpenAI's OpenAPI specification, openapi.yaml at the 2026-10-09 commit (github.com/openai/openai-openapi): `logit_bias`; `CreateResponse`; `ReasoningEffort` (class OD)
- OCB: OpenAI cookbook, examples/Structured_Outputs_Intro.ipynb (github.com/openai/openai-cookbook) (class OD)
- OFC: OpenAI, "Function calling". https://developers.openai.com/api/docs/guides/function-calling (class OD)
- OLL: Ollama documentation in its repository (github.com/ollama/ollama): docs/capabilities/structured-outputs.mdx, docs/api.md (class OD)
- ORS: OpenAI, "Reasoning models". https://developers.openai.com/api/docs/guides/reasoning (class OD)
- OSDK: openai-python 3.29.0, src/openai/lib/_pydantic.py (github.com/openai/openai-python) (class OD)
- OSO: OpenAI, "Structured Outputs". https://developers.openai.com/api/docs/guides/structured-outputs (class OD)
- OUT: Outlines README and docs/features/models/index.md (github.com/dottxt-ai/outlines) (class OD)
- PYD: Pydantic source and docstrings, pydantic/main.py and json_schema.py (github.com/pydantic/pydantic, main branch) (class OD)
- REA: Yao et al., "ReAct", ICLR 2023, arXiv 2210.03629, §3.1; the authors' prompts (github.com/ysymyth/ReAct) (class PR)
- TAM: Tam et al., "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models", EMNLP 2024 Industry Track, pp. 1218-1236. https://aclanthology.org/2024.emnlp-industry.91/ (class PR)
- project file: claude/new-skills-appendix.md; skills/sophisticated-prompt-generator/references/seven-axis-checklist.md; claude/taxonomy-of-prompt-engineering-3e.md §10.5; claude/prompt-construction-guide-2e.md §18 (class Project documents)

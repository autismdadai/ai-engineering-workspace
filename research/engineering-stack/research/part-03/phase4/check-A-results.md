# Check A results (progress log)
## Local sources done: LCG, OLL, OUT, JSL, PYD, OSDK, OAPI
- LCG: "converting a subset of" (L143), "Unsupported features are skipped silently" (L207), min/max integers only (L210), "The model has no visibility into the schema" (L151, in note under JSON-schema section covering llama-server response_format and /chat/completions) -> supported
- OLL: "output will always be a well-formed JSON object" (api.md L246 per grep; "When `format` is set to `json`"); "ideal to also pass the JSON schema as a string in the prompt" (structured-outputs.mdx L55); model_json_schema/model_validate_json (L95-98) -> supported
- OUT: Apache-2.0 in pyproject; "limited control over text generation and some output types are not supported" docs/features/models/index.md L115 -> supported
- JSL: Draft202012 is _LATEST_VERSION default in validator_for (validators.py L862, L1406) -> supported
- PYD: default dialect 2020-12 (json_schema.py L230,265); model_validate_json raises ValidationError (main.py L834) -> supported
- OSDK: to_strict_json_schema sets additionalProperties False, required all (_pydantic.py L16-57) -> supported
- OAPI: logit_bias -100..100 in CreateCompletionRequest and Chat completions; CreateResponse has none -> supported
- ACB: both notebooks match (examples: summary/NER/sentiment/classification + unknown keys; Pydantic Note validated in process_tool_call before save_note) -> supported (claims 62,63)
- OCB: Structured_Outputs_Intro: math tutor, summarization, entity extraction (function calling), Refusal section; "gpt-4o-2024-08-06" -> supported (64)
## ASO (WebFetch, lookup 1) - all quotes verified: guarantee quote (Why use structured outputs); "there are scenarios where the output may not match your schema" (Invalid outputs); refusal bills tokens; max_tokens "may be incomplete and not match your schema"; enum casing quote; output_config.format; output_format deprecated + 400 w/o structured-outputs-2025-11-13 header (Migrating); limits table 20/24/16; additionalProperties "must be set to false for objects"; minimum/maximum/multipleOf, minLength/maxLength unsupported; minItems 0 or 1 only; recursive/external $ref unsupported; SDK "simplified schema" quote; reasoning field -> reasoning_extraction refusal, "Ask for a short explanation instead".
## OSO (lookups 2-9; HTML view truncated at ~95k chars so used the .md version of the page)
- JSON mode comparison: "While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence." (Structured Outputs vs JSON mode) OK
- Refusals with Structured Outputs section: "a refusal does not necessarily follow the schema you have supplied in `response_format`" OK
- Supported schemas: "Structured Outputs supports a subset of the JSON Schema language." OK; Number lists multipleOf, maximum, exclusiveMaximum, minimum, exclusiveMinimum; String lists pattern, format (no minLength/maxLength); Array lists minItems, maxItems. OK
- Responses API text.format json_schema strict:true and Chat Completions response_format both shown. OK
- OSO prose on "all fields required"/additionalProperties false/null union: NOT found in OSO (examples only). Check OFC.
Lookups so far: 9
## OFC (lookup 10, .md version): 5-step list first "Make a request to the model with tools it could call", last "Receive a final response from the model (or more tool calls)"; fields type("always function")/name/description/parameters/strict; "it is best practice to assume there are several."; parallel_tool_calls false; "Aim for fewer than 20 functions ... soft suggestion"; "Responses requests will attempt to normalize your schema into strict mode when possible"; "Chat Completions requests remain non-strict by default."; "additionalProperties must be set to false for each object"; "All fields in properties must be marked as required"; optional via adding null as a type; "When the model calls a function, you must execute it and return the result." -> all OK. mermaid-cli 12.0.0 (claim 34) not in OFC -> could not check.
## ATD (lookup 11): name regex, input_schema, input_examples listed; strict only in tool reference; Forcing table: "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 | any and tool return a 400 error | auto with strict tool use ..., or structured outputs"; "Forcing a tool also skips thinking on every model that accepts forced tool use" -> OK. No date on page. tool_result not on ATD.
## AHT (12): "Claude will retry 2-3 times with corrections before apologizing to the user." (Invalid tool name section); tool_result blocks "must come FIRST in the content array. Any text must come AFTER"; is_error set true if tool errored. OK
## APT (13): default on; "set disable_parallel_tool_use: true inside the tool_choice object. It is not a top-level request parameter."; "all together in the next user message... before any text content"; is_error. OK
## ATR (14): strict, input_examples, cache_control rows exist; name/description/input_schema rows not in ATR but in ATD. OK
## ATK (15): Sampling parameters: non-default temperature/top_p/top_k return 400 on Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5, etc.; budget_tokens 400 error on those models; thinking tokens "billed as output tokens, even when the thinking text isn't returned to you". No temp-0 determinism statement. OK
Lookups so far: 15
## DSD (local clone of dspy HEAD 81a41fd, not 1dcdf86): choosing-an-optimizer.md L45 "GEPA and MIPROv2 can spend hundreds of dollars in LM calls on a single run" -> claim 82 optimizer part OK (note optimizers.md L112-113 says typical run ~$2, "as little as a few cents or up to tens of dollars": docs disagree)
## JSB (16): Table 4 GitHub Hard (Llama-3.2-1B): empirical coverage Outlines 0.03, Guidance 0.41, OpenAI 0.09 (declared 0.09), OpenAI compliance 1.00; caption "not directly comparable due to differences in the underlying model"; six frameworks; benchmark 9,558 schemas ("10K"). Table 8 (Llama-3.1-8B): GSM8K LM-only 80.1, XGrammar 83.7, Llamacpp 82.4, Outlines 81.6, Guidance 83.8; Shuffle Objects LM-only 52.6 vs Llamacpp 52.6 (TIE) -> "higher with every engine" overstated for that task. Paper text: "constrained decoding, regardless of the framework, achieves higher performance"; v3 27 Feb 2025.
Lookups so far: 16
## TAM (17-18): ACL page: venue EMNLP 2024 Industry Track pp.1218-1236, abstract "Surprisingly, we observe a significant decline in LLMs' reasoning abilities under format restrictions." arXiv 2408.02442v3 text: models gpt-3.5-turbo-0125, claude-3-haiku-20240307, gemini-1.5-flash, "LLaMA3-8B-Instruct", Gemma-2-9B-Instruct (plus Mistral-7b-v0.3 in App D, gpt-4o-mini in 5.4); GSM8K, Last Letter Concatenation, Shuffled Objects; classification DDXPlus, MultiFin, Sports Understanding, NI Task 280. Sec 4.1: "JSON-mode performs competitively, and in some cases, surpasses the other three methodologies." (claim says surpasses "free text" -> paraphrase; free text is one of the three). Mostly OK.
## DTX (19): "The paper confuses structured generation with JSON-mode"; model "Llama-3-8B-instruct"; Figure 2 GSM8K Unstructured 0.77 Structured 0.78; no date; no explicit vendor disclosure on page but ".txt" site. OK
Lookups so far: 18

# FINAL REPORT

## Table (claim | verdict | evidence | note)
1 | supported | ASO "Structured outputs guarantee schema-compliant responses through constrained decoding" | -
2 | supported | OFC "When the model calls a function, you must execute it and return the result." | -
3 | supported | JSS "The current version is 2020-12!" | -
4 | supported | ASO, Why use structured outputs, same words | -
5 | supported | OSO "While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence." | -
6 | supported | ATD tool_use block; OFC "Receive a tool call from the model" | -
7 | supported | ATD name/description/input_schema; OFC name/description/parameters | -
8 | supported | AHT "is_error (optional): Set to true if the tool execution resulted in an error." | tool_result name is on AHT/ATD examples
9 | supported | ATD "Set strict: true on your tool definitions"; OFC strict field | -
10 | supported | JSL README Draft 2020-12 support; PYD json_schema.py | claim is about popularity, only existence of the libraries is checkable
11 | supported | LCG L3 "GBNF ... format for defining formal grammars to constrain model outputs in llama.cpp" | -
12 | supported | PYD main.py L607 model_json_schema, L801 model_validate_json, L834 "ValidationError: If json_data is not a JSON string or the object could not be validated." | -
13 | supported | PYD json_schema.py L230 "default schema dialect is .../2020-12/schema"; JSL validators.py L862 _LATEST_VERSION = Draft202012Validator, used by validator_for when no $schema | jsonschema default applies when schema has no $schema
14 | supported | OLL api.md "the output will always be a well-formed JSON object. It's important to also instruct the model to respond in JSON." | -
15 | supported | ASO output_config.format; OSO text.format strict | -
16 | supported | ASO Migrating: "The output_format parameter is deprecated ... Without it, the API returns a 400 error." | -
17 | supported | OSO comparison table: text: { format: { type: "json_schema", "strict": true, "schema": ... } } ; response_format | -
18 | supported | ASO both quotes verbatim (Why use / Invalid outputs) | Anthropic's wording is "Structured outputs guarantee ..." ok
19 | supported | ASO Refusals: stop_reason "refusal"; "You'll be billed for the tokens generated"; "The output may not match your schema because..." | -
20 | supported | OSO Refusals section "a refusal does not necessarily follow the schema you have supplied in response_format" | only in .md version of page; HTML view truncated
21 | supported | ASO "The output may be incomplete and not match your schema"; "Retry with a higher max_tokens value" | -
22 | supported | ASO Enum value casing, verbatim | -
23 | supported | OSO Supported schemas "Structured Outputs supports a subset of the JSON Schema language." | -
24 | supported | ASO "required and additionalProperties (must be set to false for objects)"; OFC "additionalProperties must be set to false for each object" | -
25 | supported | OFC "All fields in properties must be marked as required." ; "denote optional fields by adding null as a type option" | ASO "Not stated" is fair
26 | supported | ASO "Numerical constraints (such as minimum, maximum, multipleOf)" unsupported; OSO Number lists multipleOf, minimum, maximum | -
27 | supported | ASO "String constraints (minLength, maxLength)" unsupported; OSO String lists only pattern, format | -
28 | supported | ASO "Array minItems (only values 0 and 1 supported)"; OSO Array lists minItems, maxItems | -
29 | supported | ASO "Recursive schemas", "External $ref" unsupported | -
30 | supported | ASO Explicit limits table: 20 strict tools, 24 optional parameters, 16 union-type parameters | "per request" matches "combined total across all strict schemas in a single request"
31 | supported | ASO "Claude receives a simplified schema, but a helper that validates responses still enforces every constraint in your code."; OSDK _pydantic.py to_strict_json_schema | -
32 | supported | OAPI logit_bias "bias value from -100 to 100 ... added to the logits ... prior to sampling"; "-100 or 100 should result in a ban or exclusive selection" | "No" and "soft shift" are the author's reasoning, not in sources
33 | supported | OAPI logit_bias in CreateCompletionRequest and chat completion request; CreateResponse has none | -
34 | could not check | OFC gives the five steps verbatim (first and last match) | "mermaid-cli 12.0.0" is not in OFC and no source key covers it
35 | supported | ATD table: name regex ^[a-zA-Z0-9_-]{1,128}$, description, input_schema, input_examples; ATR: strict | -
36 | supported | OFC type "should always be function", name, description, parameters, strict | -
37 | could not check | claim text is the fragment "Sources: ." | nothing to check
38 | supported | ATD table: "Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and Claude Mythos 5.1 | any and tool return a 400 error | auto with strict tool use ..., or structured outputs" | -
39 | supported | ATD "Forcing a tool also skips thinking on every model that accepts forced tool use" | -
40 | supported | APT "set disable_parallel_tool_use: true inside the tool_choice object. It is not a top-level request parameter."; OFC parallel_tool_calls false | "default" for OpenAI: OFC says model may call several; fine
41 | supported | OFC "it is best practice to assume there are several." | -
42 | supported | APT "all together in the next user message ... every tool_result block before any text"; AHT is_error | -
43 | supported | AHT "Claude will retry 2-3 times with corrections before apologizing to the user." | -
44 | supported | OFC verbatim | -
45 | supported | OFC "Responses requests will attempt to normalize your schema into strict mode when possible"; "Chat Completions requests remain non-strict by default." | -
46 | supported | LCG L143 "supports converting a subset of https://json-schema.org/ to GBNF grammars" | -
47 | supported | LCG L207 "Unsupported features are skipped silently"; L210 min/max "only supported for type integer" | -
48 | supported | LCG L151 "The model has no visibility into the schema" | note is general to all JSON-schema use (incl. response_format), and says tool calling is the exception
49 | supported | OLL structured-outputs.mdx L55 "It is ideal to also pass the JSON schema as a string in the prompt" | -
50 | supported | OLL L81-98 Pydantic model_json_schema() to format; model_validate_json | -
51 | supported | OUT pyproject "Apache-2.0"; docs/features/models/index.md L115 "we have limited control over text generation and some output types are not supported" | -
52 | supported | JSB Table 4: empirical coverage Outlines 0.03, Guidance 0.41, OpenAI 0.09, OpenAI compliance 1.00 | metric is "empirical coverage"; the benchmark has 9,558 schemas (rounded to 10K in abstract); Gemini omitted
53 | supported | JSB Table 4 caption "not directly comparable due to differences in the underlying model" | second half is author's own
54 | supported | TAM abstract "we observe a significant decline in LLMs' reasoning abilities under format restrictions"; Sec 4.1 "JSON-mode performs competitively, and in some cases, surpasses the other three methodologies" | paper says "the other three methodologies", not "free text"; model written LLaMA3-8B-Instruct; text read from arXiv v3, not the EMNLP PDF; paper also used Mistral-7b-v0.3 and gpt-4o-mini
55 | supported | DTX "The paper confuses structured generation with JSON-mode"; Figure 2 GSM8K Unstructured 0.77, Structured 0.78 | page spells model "Llama-3-8B-instruct"
56 | partly supported | JSB Table 8 GSM8K: LM only 80.1; Outlines 81.6; Llamacpp 82.4; XGrammar 83.7; Guidance 83.8 | numbers right. "higher with every engine" fails on Shuffle Objects: Llamacpp 52.6 = LM only 52.6 (tie)
57 | supported | ASO "may lead to a reasoning_extraction refusal. Ask for a short explanation instead." | -
58 | supported | ATK: non-default temperature/top_p/top_k "return a 400 error" on Opus 5.5, Sonnet 5.5, Fable 5.1, Mythos 5.1 etc. | "outputs vary at temperature 0" is internal (not in sources, and ATK has no such statement)
59 | partly supported | OAPI logit_bias present in Chat Completions request and legacy Completions request | "Chat Completions only" conflicts with claim 33 and the spec: also in legacy Completions
60 | supported | ASO refusal and max_tokens exceptions; OSO refusal | OSO prose documents refusal only
61 | supported | REA Sec 3.1 "(1) search[entity] (2) lookup[string] (3) finish[answer]"; "Published as a conference paper at ICLR 2023"; few-shot text prompting, no JSON | -
62 | supported | ACB: summarization, NER, sentiment, classification via tool input schema | -
63 | supported | ACB tool_use_with_pydantic: process_tool_call builds Note(...) (Pydantic) then calls save_note | -
64 | supported | OCB: math tutor, summarization, entity extraction, Refusal section; mentions gpt-4o-2024-08-06 | "2024 launch" consistent
65 | supported | OLL structured-outputs.mdx example | -
66 | supported | ASO/OSO/PYD as above | recommendation, not a fact claim
67 | supported | OLL as above | recommendation
68 | supported | JSB coverage varies 0.03 to 0.41 | -
69 | supported | ASO refusal and max_tokens can break schema; OSO refusal | -
70 | supported | ATD "any and tool return a 400 error" on newest models | -
71 | supported | LCG "Unsupported features are skipped silently" | -
72 | supported | OFC optional via null type and all fields required | linter outputs (schema_lint.py) are not checkable here
73 | supported | ASO/OFC additionalProperties false required | -
74 | supported | ASO refusal, max_tokens, enum capitalization | OpenAI covers refusal only
75 | supported | OFC "you must execute it and return the result" | "permission" part is advice
76 | supported | ASO URL fetched and matches | -
77 | supported | both URLs fetched | -
78 | supported | ASO "scenarios where the output may not match"; OSO refusal | -
79 | supported | LCG "skipped silently"; JSB coverage as low as 0.03 | -
80 | supported | TAM decline; DTX 0.77 vs 0.78; JSB +1.5 to +3.7 pp | "later preprint": JSB 2025 after TAM 2024. DTX undated
81 | supported | ATK/AXT: budget_tokens 400 error on 4.7+; ATK sampling params 400; ATD forced tools 400 | "retired" is the author's word; AXT says "deprecated" on 4.6 and rejected on 4.7+
82 | supported | ATK "billed as output tokens, even when the thinking text isn't returned"; ORS "billed as output tokens"; DSD choosing-an-optimizer.md "can spend hundreds of dollars in LM calls on a single run" | DSPy optimizers.md says typical run ~$2 and "up to tens of dollars"; I read HEAD (81a41fd), not 1dcdf86
83 | partly supported | Project: guide §18 and taxonomy §10.5 both say the output "cannot" violate the schema (verified). ASO lists refusal and max_tokens | OSO prose lists refusal only; max_tokens appears there only in code comments
84 | supported | claude/new-skills-appendix.md section 4 lists decoding-controller, faithfulness-auditor, injection-hardening, long-context-placer; no schema-contract skill | decoding-controller mentions "schema constraints" but is a different idea

## Totals
supported 79, partly 3, contradicted 0, could not check 2

## Findings
- 56 | medium-low | "Constrained decoding scored higher with every engine: GSM8K 80.1% unconstrained against 81.6% to 83.8% constrained, a gain of 1.5 to 3.7 percentage points" | The GSM8K numbers are exact, but the general sentence is too strong: on Shuffle Objects, Llamacpp scores 52.6%, identical to LM only (JSB Table 8). The paper itself says "regardless of the framework, achieves higher performance" (Sec 6.2) so the claim repeats the paper's wording, but the table has a tie | Say "on GSM8K, every engine scored higher" or "higher or equal on all three tasks".
- 59 | low | "`logit_bias` (Chat Completions only)" | OAPI: logit_bias is in the legacy Completions request too (CreateCompletionRequest) as well as Chat Completions; claim 33 says so correctly | Write "Chat Completions and legacy Completions, not Responses".
- 83 | low | "Anthropic's and OpenAI's current pages list exceptions (refusal, max_tokens)" | OpenAI's Structured Outputs page documents only refusal in prose (Refusals section); incomplete/max_output_tokens handling appears only as code comments. Anthropic lists both | Say "Anthropic lists refusal and max_tokens; OpenAI lists refusal".
- 34 | low | "The diagram renders with mermaid-cli 12.0.0" | Not in OFC or any listed source; cannot be checked blind | Cite the tool's package page or drop the version from the factual list.
- 37 | low | "Sources: ." | Fragment, no content | Check the generated list in the document.
- Minor notes (supported but could tighten): 54 paraphrases "the other three methodologies" as "free text"; 52 "10,000 schemas" vs 9,558 in Table 1; 82 DSPy docs disagree internally on cost; 58 temperature-0 variability not backed by ATK (internal reference).

Lookups used: 23 (WebFetch/WebSearch). Also: shallow git clones of 10 repos, and project file reads (no lookups).

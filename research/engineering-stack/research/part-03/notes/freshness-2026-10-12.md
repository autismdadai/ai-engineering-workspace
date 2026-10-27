# Part 03 freshness re-check, October 12, 2026 (21:17 UTC)

## Registry (PyPI JSON API, pypi_fresh.py, Python 3.13.16)
- dspy 3.4.0 | 2026-09-25 | MIT | <3.15,>=3.10 (unchanged)
- openai 3.29.0 | 2026-10-11 | Apache-2.0 | >=3.10 (was 3.28.0 on Oct 9)
- anthropic 1.13.0 | 2026-10-09 | MIT | >=3.10 (unchanged)
- pydantic 2.14.1 | 2026-10-11 | MIT | >=3.10
- jsonschema 4.26.0 | 2026-01-07 | MIT | >=3.10
- gepa 0.1.4 | 2026-07-15 | MIT | <3.15,>=3.10
- optuna 5.0.0 | 2026-09-07 | MIT | >=3.9
- instructor 1.17.0 | 2026-09-09 | MIT | <4.0,>=3.9
- outlines 1.3.3 | 2026-08-06 | Apache-2.0 | <3.14,>=3.10  (excludes 3.14)
- llama-cpp-python 0.3.36 | 2026-10-01 | MIT | >=3.8
- litellm 1.105.0 | 2026-10-11 | MIT | <3.15,>=3.10

## Anthropic structured outputs (https://platform.claude.com/docs/en/build-with-claude/structured-outputs), no page date
- GA: `output_config.format` with type json_schema; strict tool use via `"strict": true` on a tool. Beta headers no longer required.
- `output_format` deprecated; needs header structured-outputs-2025-11-13 or returns 400.
- Constrained decoding; "guarantee schema compliance in most cases"; exceptions: refusal (stop_reason "refusal", billed, may not match), max_tokens (may be incomplete). Enum/const capitalization not guaranteed.
- Unsupported: recursive schemas, complex types in enums, external $ref, minimum/maximum/multipleOf, minLength/maxLength, array constraints beyond minItems 0 or 1, additionalProperties other than false. Regex backreferences, lookaround, \b not supported.
- Limits: 20 strict tools per request, 24 optional parameters, 16 union-type parameters; "Schema is too complex for compilation".
- Incompatible with citations and with prefilling.
- Models: Fable 5/5.1; Mythos 5/5.1/Preview; Opus 4.5 to 5.5; Sonnet 4.5, 4.6, 5, 5.5; Haiku 4.5, 5.5.
- SDK helpers send a simplified schema but validate full constraints client-side.

## Anthropic Messages create (https://platform.claude.com/docs/en/api/messages/create)
- temperature: Deprecated; models released after Claude Opus 4.6 accept only 1.0, others 400. "even with temperature of 0.0, the results will not be fully deterministic." Unchanged from Oct 10.
- top_p: Deprecated; after Opus 4.6 only >= 0.99 accepted. (new detail)
- top_k: Deprecated; after Opus 4.6 any value rejected. (new detail)
- The page's own cURL example sends top_k 5 and top_p 0.7 to claude-opus-5 (inconsistent with the deprecation).

## OpenAI Structured Outputs (https://developers.openai.com/api/docs/guides/structured-outputs)
- "ensures the model will always generate responses that adhere to your supplied JSON Schema"; JSON mode valid JSON only.
- Responses API: text.format {type json_schema, strict true, schema}; Chat Completions: response_format.
- "starting with GPT-4o"; "For new projects, start with gpt-6-astra" (model name not checked elsewhere).
- Explicit refusals detectable.
- Supported-schema list not captured by fetch: researcher to read.

## OpenAI function calling (https://developers.openai.com/api/docs/guides/function-calling)
- Fields: type function, name, description, parameters (JSON Schema), strict.
- "Aim for fewer than 20 functions available at the start of a turn ... soft suggestion."
- Five-step loop; assume zero, one or several calls.
- strict defaults, tool_choice, parallel_tool_calls not captured: researcher to read.

## Workbench (ledger P1-08)
- Support article "How do I use the Workbench?" (date shown July 16, 2026): "Try a model or a new API feature before you write any code"; built on the public Messages API. Credits not stated. Exists as of Oct 12, 2026.

## DSPy docs (current)
- MIPROv2: name expansion confirmed; "Bayesian Optimization"; minibatch evaluation; auto default 'light'; no gain numbers; refers to arXiv 2406.11695.
- GEPA: "Genetic-Pareto"; reflection on traces; Pareto frontier per validation instance; metric returns float or score+feedback; exactly one of auto / max_full_evals / max_metric_calls; reflection LM required unless custom proposer; docs example uses gpt-5. No numbers.

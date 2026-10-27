# Engineering Stack Part 08: Phase 4 Review

*October 14, 2026. The Phase 4 record for claude/engineering-stack-part-08-agents.md, in the finding format of claude/fabel-prompt-audit.md (number, severity, quote, what goes wrong, why with source, fix). Every finding was reproduced by the author before it was fixed, or is marked otherwise. This part had a security reviewer as well as the usual checks, as the plan requires for Parts 08, 10 and 13. Raw reports went to the owner in engineering-stack-research-part-08.zip.*

## Who checked what

| Check | By | Scope | Result |
|---|---|---|---|
| Blind source check A | Fresh agent on Claude Sonnet, given only claims and source links | 83 claims: Sections 1 to 3.7 (loop, harness, benchmarks, containers) | 75 supported, 8 partly, 0 contradicted; 25 web lookups plus package source and clones |
| Blind source check B | Fresh agent on Claude Sonnet, same rules | 104 claims: Sections 3.8 to 11 (gVisor, Firecracker, coding-agent sandboxes, computer use, picks, teaching, limits) | 99 supported, 5 partly, 0 contradicted; about 33 web lookups |
| Security review | Fresh agent, given the part and the lab zip, testing by running code | The lab's code as a pattern readers will copy; the hardened command; the safety advice | 17 findings: 4 high, 4 medium, 9 low |
| Beginner test | Fresh agent following Sections 7 to 9 literally, fresh virtual environments | Python 3.13.16, 3.12.3, 3.11.17; core lab and the SDK cross-check on all three | 13 problems: 0 high, 6 medium, 7 low; all checks passed on all three; no network calls (strace and a socket hook) |
| Mutation check | The lab's own `mutation_check.py` | 20, then 28, deliberate breaks | 19 of 20 on the first run (a near-equivalent mutant, answered with check 1c); 28 of 28 after the security fixes |
| SDK cross-check | `crosscheck.py` with `openai-agents` 0.23.1 and a fake model, tracing off | Default turn cap; hidden exceptions; the lab's cap | 3 of 3 on all three Pythons |
| Lead re-checks | The author | The computer-use toolset page; both SDKs' turn-cap defaults in installed code; Firecracker's SPECIFICATION.md; licence files of Firecracker, gVisor and moby; Docker's logging docs | See findings |

## Findings

| # | Severity | Quote (draft or lab) | What goes wrong | Why, with source | Fix |
|---|---|---|---|---|---|
| 1 | High | `sandbox_check.py`: parsing stopped at the first option it didn't know | `docker run -p 8080:80 --privileged img` reported nothing dangerous and exited 0; `-itv /:/host` reported ok | Security review; reproduced: `"image": "8080:80", "dangerous": {}`, exit 0 | Rewritten to fail closed: unknown options take a value, short flags are split, the last value wins, no image means not ok; check 7c and mutations added |
| 2 | High | `sandbox_check.py`: missing danger patterns | `ok: true` with `-v /:/host`, `/var/run` mounts, other runtime sockets, host or container namespaces, added capabilities, `apparmor=unconfined`, `label=disable`, `systempaths=unconfined`, and weak values such as `--read-only=false`, `--memory 0`, a later `--pids-limit -1` | Security review; 22 commands reproduced before and after | Patterns added; values checked; exit code 0 only when ok; text calls it "a checklist for the options it knows, not a guarantee" |
| 3 | High | Check 2d "a slow tool is cut off at its time limit" | Python threads can't be stopped: a timed-out refund ran anyway, while the log said "timeout" and the model was told to "Try a smaller request" | Security review; reproduced: log `timeout`, tool ran | The loop says "may still finish ... do not call it again"; check 2f proves the tool finishes; Section 3.2 explains, and points to a separate process for real stopping |
| 4 | High | Section 3.11: the harness blocks on-screen orders and "the rule doesn't depend on the model" | The harness trusted the stand-in's own `source="screen"` label, which a real model doesn't give | Security review; reproduced by reading `check()` | `screen_agent.py` now decides from the task's allowed kinds, sites and recipients only; check 8b has the stand-in mislabel the injection, still blocked; check 8d states the limit (in-scope injections pass) |
| 5 | Medium | `agent_loop.py` sent `f"... {type(error).__name__}: {error}"` to the model | Exception text can hold secrets; an invented key in a URL reached the model | Security review; reproduced | `ToolError` for model-facing messages; other exceptions give a generic message and go to `RunResult.errors`; checks 2c and 2d |
| 6 | Medium | Hardened `docker run` | No log-size limit (Docker: "By default, no log-rotation is performed"), no wall-clock limit, unpinned image; the "doesn't stop" list missed secrets in mounts, output flowing back, and the `docker` group | Security review; reproduced in docker/docs `logging/configure.md` | `--log-opt max-size=1m`, `timeout 300` inside the container, digest pinning advice; list extended; cheat sheet "never" line extended |
| 7 | Medium | The text oversold the reviewer ("reviews any `docker run` line") | A false sense of safety | Security review | Reworded throughout; the skill proposal in Section 11 carries the same framing |
| 8 | Medium | Exercises: no instruction to run from the lab folder | `ModuleNotFoundError: No module named 'agent_loop'` from elsewhere | Tester; reproduced | One line added |
| 9 | Medium | "exit code" used, never explained | Beginners can't see or check it | Tester | Explained in 7.6, with `echo $?` and `$LASTEXITCODE` |
| 10 | Medium | 7.7 row: "Tracing request failed" with tracing on and no key | With no key, the SDK prints "OPENAI_API_KEY is not set, skipping trace export" and uploads nothing; the upload happens with a key | Tester and security review; consistent with the lead's earlier run, which set a placeholder key and saw "Tracing request failed" | Row rewritten |
| 11 | Medium | 7.7 row blamed missing quotes for `error: expected a command starting with 'docker run'` | Without quotes the script prints its usage text and exits 2 | Tester; reproduced | Two rows |
| 12 | Medium | Step 5: "joined onto one line" without the line; 7.5: "`python -c ...` as `main.py`" | Ambiguous | Tester | The joined command printed; 7.5 says to put the code in `task/main.py` |
| 13 | Medium | Lab docstrings cited "Section 3.6" and "Section 3.8" | Wrong sections | Tester and security review; reproduced | 3.7 and 3.10 to 3.11 |
| 14 | Medium | "50 failed runs" for ReAct's error analysis | 200 sampled trajectories, 50 correct and 50 incorrect per method | Checker A; the researcher's row agrees | Reworded |
| 15 | Low | SWE-bench Verified "became the standard coding score"; "flawed tests" | Not in the source; the source says issues in "test design and/or problem description", among problems o3 often failed | Checker A | Reworded, with the audit's scope |
| 16 | Low | "the whole history is sent again" given as the cause of 4x tokens | MRS gives the figure, not that cause | Checker A | "One reason is ..." |
| 17 | Low | "gVisor and Firecracker are stronger boundaries" [V: GVS] | Not in GVS | Checker A | "add a second boundary between the code and the host's kernel" [V: GVI, FCR] |
| 18 | Low | Docker socket: "can start a privileged container" [V: DPI] | Not in DPI | Checker A | Reworded and tagged [I] |
| 19 | Low | `no-new-privileges` stops "su or setuid files" | DRR says `su` and `sudo` | Checker A | Quoted |
| 20 | Low | Modal "uses gVisor by default" | The guide says gVisor or a VM, Modal's choice unless set | Checker B | Reworded |
| 21 | Low | WebArena tasks "scored with the accessibility tree" | It's what agents see, not how tasks are scored | Checker B | Reworded |
| 22 | Low | "both specs" style overreach: none in this part; "Böckeler ... not the February 17 memo" | The memo page now mentions guides and sensors in a later-added paragraph without defining them | Checker B | The text already says the April 2 article "defines" them; kept |
| 23 | Low | `validate_call` accepted `True` as a number, and NaN | Type check gap | Security review; reproduced | Fixed; check 3b covers `amount=True`; text says business rules belong in the tool |
| 24 | Low | `execute` "never raises" | An approver that raised crashed the run; an approver returning "no" approved; a non-JSON return value crashed it | Security review; reproduced the first two | Only an exact `True` approves; a crash counts as no; `str()` fallback; check 3b |
| 25 | Low | Cheat sheet rule 7 and Section 6 implied model-written code might not be untrusted | Contradicts Section 3.8 | Security review | Reworded |
| 26 | Low | 7.5 gVisor steps | No warning that restarting Docker stops containers, or that the `docker` group is root-equivalent | Security review | Added |
| 27 | Low | `mutation_check.py` left its control copy behind | Temp folders accumulate | Security review; reproduced | Removed after use |
| 28 | Low | Only `openai-agents` pinned | Its dependencies float | Security review | Said so in 7.4 |
| 29 | Low | 7.3 had no `python3-venv` note; 7.1 no fallback for a missing 3.13 | Beginner snags | Tester | Added |
| 30 | Low | "38 packages" | One more on Python 3.11 | Tester | Scoped |
| 31 | Low | "Checks run on this part: To be filled after Phase 4" | Placeholder | Tester | Filled at assembly |
| 32 | n/a | Mutation "loop keeps going after end_turn" caught by nothing on the first run | The loop also stops on a response with no tool calls, so the mutant was equivalent except when `end_turn` carries a tool call | The first mutation run | Check 1c added for that case |

## Not changed, with reasons

- Checker A could not see the tail of the WTA quote ("rather than opaque error codes or tracebacks") in its fetch summary; the researcher read it in full. Kept.
- Checker A noted the "Docker-based evaluation harness" wording is in SWE-bench's docs, not its top-level README; the source entry names the docs.
- Checker B noted that "over 72.36%" is over all 369 OSWorld tasks; the text attributes it to the 369.
- The tester asked to define more terms (tmpfs, cgroups, namespaces and others); the main ones are in Section 2, and the rest are glossed where used.
- The tester asked about the `sandbox_check.py` exit code for a bare command; it now exits 1 whenever `ok` is false, as the security review also asked.

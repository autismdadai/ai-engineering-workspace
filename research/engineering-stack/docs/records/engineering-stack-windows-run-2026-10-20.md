# Engineering Stack: Windows Reader-Test Run, October 20, 2026

*The reader tests of Parts 03 to 10 and 12 on the owner's Windows 11 computer, run by Claude through the desktop app with the owner's go-ahead (October 20, 2026), including Part 12's R3, which installs PyTorch and trains a small LoRA adapter. The session could click but not type in Windows' terminals, so every step ran from a PowerShell script started by double-clicking a .bat file in Downloads\ai-stack (five scripts, A to E), and every result below is copied from the scripts' logs (stack-reader-tests-a.log to stack-reader-tests-e.log) and the per-step output files in stack-reader-tests\. Downloads came only from PyPI, Hugging Face (the models' own repositories), spaCy's GitHub releases (through `spacy download`) and the Ollama server already installed on October 19. No account, key or payment was used. Evidence class: project test record.*

## The computer

Windows 11 Pro 10.0.26300; PowerShell 5.1.26100.9711; Intel Core i5-9500T, no discrete GPU; 7.79 GB of memory, with 1.1 to 3.0 GB free during the runs; 117 to 123 GB free on C:. Python 3.13.16 from python.org (installed October 12). Ollama v0.40.6 with `OLLAMA_NO_CLOUD=1` and qwen3:1.7b (installed October 19). Docker, Node.js and Claude Code are not installed.

## How it was run

- **The labs:** each part's zip from the owner's Downloads folder, unzipped into Downloads\ai-stack (sizes and SHA-256 below). Each lab got a fresh virtual environment made with Python 3.13.16, and the scripts called that environment's `python.exe` directly, so the typed steps of Section 7.1 (`py -V:3.13`, `Activate.ps1`) were not exercised.
- **Script A** (08:15 to 08:27): R1, R2 and R3 for every part, plus Part 09's R4 and Part 12's `--plan`. It set `PYTHONIOENCODING=utf-8` so that lab output written to a file couldn't crash on a non-ASCII character, and `PYTHONDONTWRITEBYTECODE=1`.
- **Script B** (08:30 to 09:00): R2 again for every part without `PYTHONIOENCODING`, as a reader's console runs it; then Part 12 R3, Part 05 R4, Part 10 R4 and R5, and Part 04 R4. It set `HF_HUB_DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1`.
- **Script C** (08:58): the tiktoken counts for Part 04, where spaCy's model went, and what the tests left outside the lab folders. Nothing installed or changed.
- **Script D** (09:02 to 09:32): Part 04 R4 again, with one timed call at the full size and one at a smaller size (`ollama_timing_probe.py`), then the test at the smaller size.
- **Script E** (09:41 to 10:19): Part 04 R4 as a variant with Ollama's thinking off (`placement_think_off.py`, listed at the end).

| Lab zip | Bytes | SHA-256 |
|---|---|---|
| engineering-stack-lab-part-03.zip | 21,450 | 01e88c6a9a8cd8a90311e8d175d28c721936806b5d3b46dc62165b8e7b4d8011 |
| engineering-stack-lab-part-04.zip | 34,804 | 05a71960e24f7a8734b23b65b29c6d9e9f5386f22645721080281903e6ba11de |
| engineering-stack-lab-part-05.zip | 14,842 | 44bb36d6a1853598a1e3b9da0ffea8e9c1ba0d4c5a913339a808ffb86f23b2a3 |
| engineering-stack-lab-part-06.zip | 12,139 | 93ebcf6f53cdfdca84be3ad2e9dbc67effacb0c5d4031ffbd8ccf305ca031fb4 |
| engineering-stack-lab-part-07.zip | 22,690 | 22f6a7e6b1ea992b2a76a6e8a12299e5b5d1c76953911cd9b844da9273d95168 |
| engineering-stack-lab-part-08.zip | 24,350 | fa15c995ae6a9c508b47acfc520b1c7fc4928d0c6f428571c784edef729ede21 |
| engineering-stack-lab-part-09.zip | 22,064 | b60a0bf192a9e1607a6694cfb97011db959ec8d01eb98dd133f0607b7fedff2d |
| engineering-stack-lab-part-10.zip | 26,665 | db679559dbae60210f3213b56d75e5ec9ad1da67936ff7c5d1055f2293aaccdc |
| engineering-stack-lab-part-12.zip | 19,327 | c8695be4b966b18dfeab013442ce5ae5f00b15419d4fa415c2e972b3898d9e75 |

## Results

| Part | Test | Expected | Got |
|---|---|---|---|
| 03 | R1 `run_lab.py` | `7 of 7 checks passed.` | The same (0.2 s) |
| 03 | R2 `mutation_check.py` | `Every mutation behaved as expected.` | The same, 17 mutations OK, with and without `PYTHONIOENCODING` |
| 03 | R3 Pydantic | `8 of 8 checks passed.` | Pydantic 2.14.1 and 4 dependencies installed with hashes; the same |
| 04 | R1 | `13 of 13 checks passed.` | The same |
| 04 | R2 | `Every mutation behaved as expected.` | The same, 15 mutations OK, both ways |
| 04 | R3 tiktoken | `14 of 14 checks passed.` | tiktoken 0.14.0 and 6 dependencies installed with hashes; the same. The counts (script C): plain English 176 characters, 32 tokens (estimate 44); Python code 92 characters, 25 tokens (estimate 23); numbers and IDs 64 characters, 30 tokens (estimate 16) |
| 04 | R4 Ollama, as written (200 documents, `--num-ctx 16384`) | Five accuracy lines and a verdict | Not finished: the first call passed the lab's 300-second limit, and the script printed `Could not reach Ollama at http://127.0.0.1:11434 (timed out). Is it running?` (exit code 1). Ollama was running |
| 04 | R4 timing (script D) | (a measurement) | 200 documents: 7,533 prompt tokens in 218.0 s (34.6 per second), then 321 thinking tokens in 160.0 s (2.0 per second); 385.8 s in all; the answer, `2201`, was right. 50 documents with `--num-ctx 4096`: 1,882 prompt tokens in 33.2 s (56.6 per second), 309 thinking tokens in 58.4 s (5.3 per second); 96.9 s in all; right |
| 04 | R4 smaller (50 documents, `--num-ctx 4096`, 10 trials), as written | Five accuracy lines and a verdict | Not finished: after 1,297 seconds one call passed the 300-second limit, with the same message (exit code 1) |
| 04 | R4 variant (script E): the lab's own `run_test` and `report` through `placement_think_off.py`, thinking off, 900 seconds per call, 50 documents, `--num-ctx 4096`, 10 trials | Five accuracy lines and a verdict | 10 of 10 right at every position (95% interval 72.2 to 100.0); `verdict: no clear position effect (lowest middle position 13)`. 1,888 prompt tokens per call; 34.1 to 78.0 seconds a call, median 39.2; 38 minutes for 50 calls; exit code 0 |
| 05 | R1 | `19 of 19 checks passed` | The same |
| 05 | R2 | `16 of 16 mutations caught` | The same, both ways |
| 05 | R3 bm25s, rank_bm25, ir_measures | Two PASS lines and five INFO lines | The same: BM25 against bm25s 0.3.13, largest gap 9.27e-08; ir_measures 0.4.3, gap 0; rank_bm25 agrees on the top 3 for 4 of 4 questions |
| 05 | R4 real models | Two PASS lines; four INFO lines to send | sentence-transformers 6.1.0 and torch 2.14.1 (40 packages, 253 s). PASS for 'fix a flat bicycle tyre' (d01) and 'squeaky brakes' (d06). nDCG@3 fused then reranked: q1 1.000 and 1.000, q2 0.798 and 0.798, q3 0.950 and 1.000, q4 1.000 and 1.000 (47.6 s with the model downloads) |
| 06 | R1 | `21 of 21 checks passed` | The same |
| 06 | R2 | `16 of 16 mutations caught` | The same, both ways |
| 06 | R3 networkx | Three PASS lines and one INFO line | networkx 3.7; the same, with `INFO networkx Leiden (modularity) finds 2 communities` |
| 07 | R1 | `22 of 22 checks passed` | The same |
| 07 | R2 | `20 of 20 mutations caught` | The same, both ways (55 s) |
| 07 | R3 `mcp` 2.3.0 | `8 of 8 cross-checks passed` and one INFO line | The same; the INFO line says an unknown tool on the SDK server "comes back as: isError result" |
| 07 | R4 Claude Code | Optional | Not run: Claude Code isn't installed |
| 08 | R1 | `27 of 27 checks passed` | The same |
| 08 | R2 | `28 of 28 mutations caught` | The same, both ways (64 s) |
| 08 | R3 openai-agents 0.23.1 | `3 of 3 cross-checks passed`, tracing off | The same, with "tracing off, no network calls" |
| 08 | R4 Docker | Optional | Not run: Docker isn't installed and needs administrator rights |
| 09 | R1 | `30 of 30 checks passed` | The same |
| 09 | R2 | `33 of 33 mutations caught` | The same, both ways |
| 09 | R3 LangGraph 1.2.15 | `6 of 6 cross-checks passed` | The same |
| 09 | R4 pause and approve in two processes | `interrupted ...`, then `done rf_1` | `interrupted {'action': 'refund', 'order': 'A17', 'amount': 250}`, a 428-byte `my-checkpoints\A17.json`, then `done rf_1`; the folder was deleted after |
| 10 | R1 | `28 of 28 checks passed` | The same |
| 10 | R2 | `50 of 50 mutations caught` | The same, both ways; with `PYTHONIOENCODING` set it also printed a `UnicodeDecodeError` (below) |
| 10 | R3 Presidio, python-stdnum | `7 of 7 cross-checks passed`, 2 network attempts blocked | presidio-analyzer 2.2.364 and python-stdnum 2.2 (53 packages); the same, attempts to publicsuffix.org and raw.githubusercontent.com |
| 10 | R4 spaCy model | No fixed result | en_core_web_lg 3.8.0 (pip: 400.7 MB) in 23 s. Both invented names found as PERSON (0.85); emails, cards, IPv4 addresses and phones found; `900-12-3456` scored US_SSN 0.50; `10:30` flagged as DATE_TIME and each email's domain as URL |
| 10 | R5 garak 0.17.0 | A list of probes, no model contacted | 179 packages including torch, 579 s. `--list_probes`: 191 probes in 42 families, 98 marked inactive. The `test.Blank` self-test: `always.Pass: PASS  ok on   40/  40`, 3.06 s |
| 12 | R1 | `17 of 17 checks passed` | The same |
| 12 | R2 | `33 of 33 mutations caught` | The same, both ways |
| 12 | R3 LoRA | Counts agree; loss falls; note the time per step | torch 2.14.1, transformers 5.20.2, PEFT 0.21.2 (38 packages, 153 MB downloaded, 266 s). `PEFT: 460,800 trainable of 134,975,808 parameters` and the same from adaptmath; loss 1.764 (first 3 steps) to 1.001 (last 3); 0.89 s per step (median), 103 tokens per second over 24 steps; adapter 1,858,776 bytes; exit code 0 in 53.6 s with the model download |

## What it shows

- **Every core lab and every cross-check passed on Windows** as the parts predict, on the first try, in fresh environments. The printed numbers match the parts' text.
- **LoRA trains on this PC's processor.** About 0.9 seconds per step for a 135-million-weight model, with about 1.2 GB of memory free. No source read for Part 12 gave a CPU figure; this is one PC and one small model.
- **The reranker changed one of four scores** in Part 05's real-model test, q3 from 0.950 to 1.000. Four questions say nothing general; the part already says so.
- **Part 04's harness works on a real model,** with thinking off: 50 of 50 right at 50 documents, so no position effect at that size. A 1,900-token prompt is far shorter than the contexts where the studies Part 04 cites found the effect, so this says nothing about long contexts.
- **Part 04's position test at full size is too slow for this PC within the lab's limits.** A 7,500-token prompt takes about 220 seconds to read at 35 tokens per second, and qwen3:1.7b then thinks for about 300 tokens at 2 to 5 tokens per second before answering. qwen3 is a thinking model, and Ollama 0.40.6 returned the thinking separately, so the answer field held only the four digits.
- **Part 04's 4-characters-per-token rule is rough in both directions,** as the part says: it overestimated English (44 against 32) and underestimated numbers and IDs (16 against 30).

## Problems met and fixes

- **A runner artifact, not a lab fault.** With `PYTHONIOENCODING=utf-8` set by script A, the child processes that `mutation_check.py` starts inherit it and write UTF-8, while the parent reads their output with Windows' default cp1252. Part 10's run printed `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f` from a reader thread but still reported 50 of 50 with exit code 0. Script B reran every R2 without the variable: all passed, and Part 10's error output was empty. Lesson for later scripts: don't set `PYTHONIOENCODING` for a whole run; set it only for steps whose output goes to a file and that start no Python children.
- **Part 04 R4 at full size passed the 300-second limit per call,** and the message blamed the connection. `placement_test.py` catches `OSError`, and a timeout is one, so a slow model reads as "Could not reach Ollama ... Is it running?". With thinking on, qwen3:1.7b also spent 300 or more tokens thinking at 2 to 5 tokens per second, and at 50 documents one call still passed the limit. Part 04 now lists that message in its errors table; the lab's code is unchanged (held for Phase 5: a separate timeout message, a `--timeout` option, and `think: false` for thinking models). The variant in script E made those two changes outside the lab's files.
- **Hugging Face prints `You are sending unauthenticated requests to the HF Hub`** when Part 05's and Part 12's scripts download models. It is a warning; the runs went on, and no account is needed. Part 12's errors table now says so.

## What stays installed

Everything sits in Downloads\ai-stack, except the caches. Deleting a lab folder removes its virtual environment and every package in it, including spaCy's model (`pip show` places it in Part 10's `.venv`).

- **Hugging Face cache:** `%USERPROFILE%\.cache\huggingface`, 434.8 MB, holding SmolLM2-135M-Instruct, all-MiniLM-L6-v2 and ms-marco-MiniLM-L6-v2.
- **garak:** its log and the self-test report in `%USERPROFILE%\.local\share\garak` (1.7 MB) and resources in `%USERPROFILE%\.cache\garak` (0.3 MB). Deleting the lab folder doesn't remove these.
- **tiktoken:** the o200k_base file in `%USERPROFILE%\AppData\Local\Temp\data-gym-cache` (3.4 MB).
- **pip's download cache** in `%USERPROFILE%\AppData\Local\pip\cache`; `python -m pip cache purge` empties it.
- **The scripts and logs** in Downloads\ai-stack: RUN-READER-TESTS-A to E, stack-reader-tests-a.ps1 to e.ps1, ollama_timing_probe.py, placement_think_off.py, the five logs and the stack-reader-tests folder.

## Still not run

- The typed PowerShell steps in every part (Section 7.1), and every macOS step.
- Part 07 R4 (needs Claude Code) and Part 08 R4 (needs Docker).
- Part 04 R4 at the size the part gives (200 documents, `--num-ctx 16384`): it needs a faster computer, or a longer limit per call.
- Parts 01 and 02's R4 (need Node.js) and Part 02's R3 (typed PowerShell), outside this run.

## The Part 04 variant script

`placement_think_off.py`, as run (Downloads\ai-stack). It imports the lab's own `placement_test.py` and changes only how each call is made.

```python
"""Part 04 R4, a variant for slow computers (Engineering Stack, October 20, 2026).

Runs placement_test.py's own test and report on a local Ollama model, with two changes,
both outside the lab's files: Ollama's thinking is turned off ("think": false), so a
thinking model answers directly, and each call may take up to 900 seconds instead of 300.
Prints the time of every call. Talks only to 127.0.0.1.
Usage: python placement_think_off.py LAB_FOLDER MODEL DOCS NUM_CTX TRIALS
"""
import json
import sys
import time
import urllib.request

lab, model, docs, num_ctx, trials = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sys.path.insert(0, lab)
import placement_test as pt  # noqa: E402


class NoThinkModel(pt.OllamaModel):
    calls = 0

    def answer(self, context, question, gold_pos, n_docs, code):
        body = {"model": self.model, "stream": False, "think": False,
                "prompt": f"{context}\n\n{question}",
                "options": {"num_ctx": self.num_ctx, "temperature": 0}}
        req = urllib.request.Request(f"{self.host}/api/generate", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=900) as r:
            out = json.loads(r.read())
        NoThinkModel.calls += 1
        if out.get("prompt_eval_count", 0) >= self.num_ctx:
            raise RuntimeError("prompt filled the context; raise num_ctx")
        resp = out.get("response", "")
        print(f"   call {NoThinkModel.calls:2d}: position {gold_pos + 1:3d}, {time.time() - start:5.1f} s, "
              f"{out.get('prompt_eval_count', 0)} prompt and {out.get('eval_count', 0)} output tokens, "
              f"{'right' if code in resp else 'wrong'}: {resp.strip()[:40]!r}", flush=True)
        return resp


print(f"Local model {model}, {docs} documents, num_ctx {num_ctx}, {trials} trials per position, "
      f"thinking off, 900-second limit per call", flush=True)
pt.report(pt.run_test(NoThinkModel(model, num_ctx), docs, trials=trials))
```

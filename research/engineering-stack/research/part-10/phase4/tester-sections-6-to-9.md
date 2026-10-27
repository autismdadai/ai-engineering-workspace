## 6. What you need

Checked October 15, 2026 [V: PYPI]. Licences from each project's licence file or registry entry; information, not legal advice.

| Tool | What it's for | Licence | Runs | Account or key? | Version |
|---|---|---|---|---|---|
| The lab's scripts | A tool-call gate, output cleaning, redaction, classifier arithmetic, licence buckets | This series | Python 3.11 to 3.13, standard library [T] | No | Lab zip |
| Presidio (`presidio-analyzer`, `presidio-anonymizer`) | Finding and replacing personal data, by patterns and a language model | MIT | Python 3.10 to 3.14; spaCy's `en_core_web_lg` (382 MB) for names | No | 2.2.364, July 22, 2026 |
| NeMo Guardrails (`nemoguardrails`) | Input, dialog, retrieval, tool and output rails | Apache-2.0 | Python 3.10 to 3.13 | Only for the models its rails call; telemetry on by default (Section 3.6) | 0.24.1, September 16, 2026 |
| garak | Scanning a model with probes and detectors | Apache-2.0 | Python 3.11 or later; pulls PyTorch | Only for hosted targets | 0.17.0, September 9, 2026 |
| Guardrails AI (`guardrails-ai`) | Validators on input and output | Apache-2.0 | Python 3.10 to 3.13 | A hub token for remote inference; metrics on once configured (Section 3.6) | 0.11.0, August 14, 2026 |
| LlamaFirewall (`llamafirewall`) | Prompt Guard 2, an alignment check and a code scanner for agents | MIT | No Python range declared | A Together AI key for AlignmentCheck's default | 1.0.3, May 29, 2025; no release since |
| Llama Prompt Guard 2 (86M, 22M) | Flagging instruction-override attempts | Llama 4 Community License | Small enough for a CPU; the card gives only GPU timings | A Hugging Face account and licence acceptance | 2025 |
| Llama Guard 4 | Labelling prompts and responses against 14 categories | Llama 4 Community License | A GPU for a 12B model | A Hugging Face account and licence acceptance (as for Prompt Guard 2) | April 2025 |
| AgentDojo (`agentdojo`) | Injection tests for agent setups | MIT | Python | Keys for the models you test | 0.1.35 |
| LLM Guard (`llm-guard`) | Was a local scanner suite | MIT | Python 3.10 to 3.12 | No | 0.3.16; **archived July 8, 2026** |

Sources for the table: Sections 3.6 to 3.11.

Picks, and when to skip them:

- **Best default for a solo builder:** the controls in code first, because they don't depend on any model: a gate with an allowlist and argument checks, approval bound to the exact action for anything that spends, sends or deletes, output cleaning before anything renders, and redaction in the logging setup. All free and offline [T]. Add Presidio when you need names and addresses found, and plan for its misses [V: PRS].
- **For production:** the same, plus a maintained guardrail framework or your model provider's classifiers as one more signal, adaptive tests of your own agent (AgentDojo-style tasks against your real tools), garak against the model you deploy, and a business associate agreement before any protected health information reaches a vendor [V: ADJ, GAR, HHC]. Turn off telemetry you didn't choose [V: NEM, GAI].
- **Best free option:** everything in the table is free to download; OpenAI's free moderation endpoint sends the text to OpenAI [V: OMD].
- **No single best classifier.** The evidence doesn't support one: vendor numbers come from private sets, and independent tests disagree with them (Section 3.7). Pick by licence, size and maintenance, and measure on your own traffic.
- **When not to use a classifier at all:** when a rule in code can decide. An amount cap, a recipient allowlist or a fixed set of tools is always right, costs nothing and can't be talked out of its decision [I].
- **Avoid:** LLM Guard for new work (archived) [V: LLG]; any defence whose only safeguard is the model deciding correctly [V: OW6].

## 7. Set it up

**Before you start.** Part 01's setup: Python 3.11 to 3.13, and the series folder `ai-stack` in your home folder (Part 01, Section 7). Unzip `engineering-stack-lab-part-10.zip` into `ai-stack`; you get a folder named `engineering-stack-lab-part-10`. On Windows, right-click the zip, choose Extract All and set the destination to your `ai-stack` folder; if you end up with the folder inside another folder of the same name, move the inner one up [R]. On macOS, double-click it, then move the folder into `ai-stack`. On Linux, go to the folder that holds the zip (for example `cd ~/Downloads`), then `python3 -m zipfile -e engineering-stack-lab-part-10.zip ~/ai-stack` [T on Linux]. The core lab needs nothing installed.

Blocks of commands below are typed one line at a time, as shown.

### 7.1 to 7.3 Windows, macOS and Linux

The same steps as Part 09, Sections 7.1 to 7.3, in this lab's folder. In PowerShell on Windows [R: typed steps not run on Windows; Parts 01 and 02's labs ran there on October 12, 2026]:

```
cd $HOME\ai-stack\engineering-stack-lab-part-10
py -V:3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python run_lab.py
```

On macOS [R: no macOS test machine] and Linux [T]:

```
cd ~/ai-stack/engineering-stack-lab-part-10
python3.13 -m venv .venv
source .venv/bin/activate
python run_lab.py
```

Expect `28 of 28 checks passed`. If `py -V:3.13` or `python3.13` isn't found, use the 3.11 or 3.12 from Part 01; on Linux, `python3` works if `python3 --version` says 3.11 to 3.13. If PowerShell refuses `Activate.ps1`, see Part 01, Section 7.6; if Linux says ensurepip is missing, `sudo apt install python3-venv` [R: the test machine had it].

### 7.4 Optional: check against Presidio [T]

With the virtual environment active:

```
python -m pip install -r requirements-crosscheck.txt
python crosscheck.py
```

This installs `presidio-analyzer` 2.2.364 and `python-stdnum` 2.2 with their dependencies, about 50 packages and about 380 MB, which took a few minutes on the test machine [T]. Only those two are pinned. No spaCy language model is downloaded, and no key or account is needed. The script blocks network connections for its own run and prints every attempt; expect seven PASS lines, `Network attempts blocked: 2 (publicsuffix.org, raw.githubusercontent.com)` and `7 of 7 cross-checks passed` [T on Python 3.13.16, 3.12.3, 3.11.17]. It uses a temporary cache folder and deletes it, so nothing is left in your home folder [T].

### 7.5 Optional reader tests [R]

These need downloads that the test machine couldn't make or a model it couldn't run. Read any command before you run it.

- **Presidio with its language model (R4).** After 7.4: `python -m spacy download en_core_web_lg` (about 382 MB, from spaCy's GitHub releases), then `python reader_presidio.py`. It prints what Presidio's full analyzer finds in the lab's records, including whether it finds the two invented names the lab's patterns miss. There's no fixed expected output; send back what it prints. Without the model it stops with a message saying which command to run [T].
- **garak (R5).** In a separate virtual environment, because it is large: `python -m pip install garak==0.17.0`, then `python -m garak --list_probes`, which should print the probe list without contacting any model. garak's README describes a `--target_type` option, and its source has a `test` generator family (for example `test.Blank`) that needs no model; `python -m garak --target_type test.Blank --spec probes.test.Test` should run a harmless self-test [R: read from the 0.17.0 README and source; not run here because the install pulls PyTorch].
- **Prompt Guard 2.** Needs a Hugging Face account and accepting the Llama 4 licence (Section 3.10); this series creates no accounts, so it's described, not scripted. If you do run it, start with the 22M model on your own harmless text, and remember the 512-token window [V: PG2, HFG].

### 7.6 A tour

| Command | What it does |
|---|---|
| `python demo.py` | The fooled assistant, the honest request with approval, redaction, the base-rate table, licence buckets |
| `python run_lab.py` | 28 checks; exit code 0 only if all pass |
| `python mutation_check.py` | Breaks the lab 46 ways in a temporary copy; each must make `run_lab.py` fail (a few seconds) |
| `python crosscheck.py` | Optional Presidio and python-stdnum comparison (7.4) |
| `python reader_presidio.py` | Optional reader test with spaCy's model (7.5) |

An **exit code** is the number a program hands back when it ends: 0 means success, anything else a failure. See it right after the command with `echo $?` on macOS and Linux, or `$LASTEXITCODE` in PowerShell.

**In your own code.** Describe each tool with `Tool(name, params, legs=[...])`, where `params` maps each argument to a checker such as `number(0, 500)`, `one_of("inbox")`, `email_at("example.com")` or `url_on("docs.example.com")`, and `legs` says which of `UNTRUSTED`, `PRIVATE` and `OUTWARD` it adds. Make a `Gate(tools, allowed={...}, max_calls=20)` per task. Call `gate.check(call)` before running a call, `gate.record(call)` after it ran, and `gate.approve(decision, call, answer)` when the verdict is `ask`. Pass every reply through `clean_output(text, hosts)` before it renders, and add `RedactingFilter(Redactor())` to your logger.

### 7.7 Common errors and fixes

| What you see | Why | Fix |
|---|---|---|
| `can't open file '.../run_lab.py': [Errno 2] No such file or directory` | The terminal isn't in the lab folder | `cd` into the lab folder [T] |
| `ModuleNotFoundError: No module named 'presidio_analyzer'` | Running `crosscheck.py` without installing its requirements, or in another environment | Section 7.4, with the virtual environment active [T] |
| `spaCy's en_core_web_lg isn't installed`, or `Install the cross-check requirements first` | `reader_presidio.py` needs Presidio and the model | Section 7.4, then `python -m spacy download en_core_web_lg` [T] |
| `ValueError: hash mode needs a secret` | `Redactor("hash")` without `secret=` | Pass a secret from an environment variable, never one written in code [T] |
| `[notice] A new release of pip is available` | An older pip | Not an error [T] |

### 7.8 How to uninstall

Before you `deactivate`, `python -m pip cache purge` empties pip's download cache, which every project on your computer shares, so skip it if you'd rather keep cached downloads [T]. Then `deactivate`, move up one folder with `cd ..`, and delete the lab folder, which also removes its virtual environment and Presidio: `rm -rf engineering-stack-lab-part-10` on macOS and Linux [T], `Remove-Item -Recurse -Force engineering-stack-lab-part-10` in PowerShell [R]. spaCy's model, if you downloaded it, lives inside that virtual environment and goes with it [R]. The mutation check and the cross-check work in your system's temporary folder and delete what they made [T].

## 8. Hands-on lab: defences that hold when the model is fooled

**Goal.** Watch a model that obeys every instruction it reads get stopped by checks in code, break one of those checks on purpose, see two URL parsers disagree, redact personal data and see what patterns miss, work out what a classifier's published rates mean at a realistic attack rate, and prove each check can fail. Then compare the redaction with Microsoft Presidio.

**Prerequisites.** Section 7 for your system. **Time:** about 40 minutes by hand, under a minute automated. **Cost:** none. **Pinned:** the standard library only; the optional cross-check pins `presidio-analyzer==2.2.364` and `python-stdnum==2.2` (7.4). **Data:** an invented inbox, vendor page, records and attacker [I]. **Files:** all are in the zip; `guard.py`, the defences, is also printed in the appendix. The others: `examples.py` (the assistant, the stand-in model and the labelled records), `demo.py`, `run_lab.py`, `mutation_check.py`, `crosscheck.py`, `reader_presidio.py`, `requirements-crosscheck.txt` and `README.md`.

**Steps.** Outputs are from the test machine, Python 3.13.16, October 15, 2026 [T].

1. **Read the gate.** Open `guard.py` and read `Gate.check` top to bottom: every early `return` is a deny, and the only `allow` is at the end.
2. **Watch the attack.** `python demo.py` prints the worked example from Section 5 (part 1) and the honest request waiting for a person (part 2) [T].
3. **Try the gate yourself.**

   ```
   python -c "from examples import *; from guard import *; g = Gate(TOOLS, allowed={'refund'}); print(g.check({'tool': 'refund', 'args': {'order': 'A17', 'amount': 750}})); print(g.check({'tool': 'refund', 'args': {'order': 'A17', 'amount': 75, 'approved': True}}))"
   ```

   It prints `Decision('deny', 'amount: must be between 0 and 500')` and `Decision('deny', "unexpected arguments ['approved']")` [T]. A model can't approve its own call by adding an argument.
4. **Break the Rule of Two.** In `guard.py`, find `return Decision("ask"` and change `"ask"` to `"allow"`. Run `python run_lab.py`: checks 2, 2b, 2c and 3b fail, and it ends `24 of 28 checks passed` [T]. A session that has read private mail and an outside page can now send email with nobody asked. Put it back and confirm 28 of 28.
5. **See two parsers disagree.**

   ```
   python -c "from urllib.parse import urlsplit; from guard import url_problem; u = r'https://evil.example\@docs.example.com/'; print(urlsplit(u).hostname, url_problem(u, ['docs.example.com']))"
   ```

   It prints `docs.example.com backslash`: Python thinks the host is the allowed one, and `url_problem` refuses the URL anyway because of the backslash [T]. A browser would go to `evil.example`; Node.js 22.22's `URL`, which follows the same WHATWG standard, prints `evil.example` for the same string [T]. An allowlist is only as good as its agreement with the parser that finally uses the URL.
6. **Redact, and see what's left.**

   ```
   python -c "from guard import *; print(Redactor().redact('Call Dana at (970) 555-0142 or dana.w@example.com').text)"
   ```

   It prints `Call Dana at <PHONE_US_1> or <EMAIL_1>` [T]. The phone number and email are gone; the name isn't. Patterns find shapes, not names (Section 3.8).
7. **Do the base-rate arithmetic.** `python -c "from guard import screen; print(screen(10000, 0.001, 0.975, 0.01))"` prints `caught` 9.75, `false_alarms` 99.9 and a precision of 0.0889 [T]: with one attack per thousand items, even a classifier that catches 97.5% at a 1% false-positive rate is wrong about nine times in ten when it raises a flag.
8. **Prove the checks can fail.** `python mutation_check.py` breaks the lab 46 ways in a temporary copy (smuggled arguments allowed, approval not tied to the action, plain `http` allowed, user-info allowed, reference links not checked, no Luhn check, AND and OR swapped in licence expressions, and more). Each must make `run_lab.py` fail. Expect `46 of 46 mutations caught` in a few seconds [T]. The first run caught 43. One miss was a fault in the mutation runner itself: a mutation that keeps a file's size, written within the same second as the previous run, let Python reuse its cached compiled copy of the unbroken file, so the runner now clears that cache and runs with `-B`. The other two were gaps in the checks: no test text had overlapping matches, and the backslash rule was hidden behind the user-info rule. Checks 4c and 6f gained cases for both [T].
9. **Compare with Presidio (optional, 7.4).** `python crosscheck.py` gives the seven results described in Section 3.8 [T].

**Expected output** (`python run_lab.py`, abridged):

```
PASS  1 the gate allows an in-scope call with valid arguments
PASS  2c approval is bound to the exact action and fails closed
PASS  3 worked example: the injected forward is denied and the leak image removed
PASS  4c tricky URLs are judged by their real host and scheme
PASS  6 pattern redaction finds every pattern type in the record set, and no names
...
28 of 28 checks passed
```

**If it fails.** A FAIL line names the check and the failing comparison. Section 7.7 covers the common errors. A check that fails only on your machine is worth reporting: send the whole output.

## 9. Teach it

**Learning objectives.** After this part you can:

1. explain why injection can't be reliably prevented today, and design tools so a fooled model can do little (least privilege, checks in code, a budget, approval under the Rule of Two);
2. stop data leaving through a rendered reply, and explain why URL allowlists need strict parsing;
3. work out a classifier's precision at your traffic's attack rate from its published rates;
4. redact personal data from logs, and say what pattern redaction misses;
5. say which of HIPAA, the FTC's health-app rule, the GDPR and the EU AI Act might apply, and sort the licences of what you use.

**Prerequisites.** Parts 01, 07 and 08. Reading a little Python.

**Common misconceptions.**

- *"A good system prompt stops injection."* OWASP calls a constraining system prompt a partial control; adaptive attacks beat prompting defences such as spotlighting and sandwiching above 95% [V: OW6, NAS].
- *"An injection classifier makes it safe."* Published classifiers fell to adaptive attacks above 90%, and at realistic attack rates most of their flags are false alarms [V: NAS][T].
- *"If the model can't send email, data can't leave."* A rendered image URL is enough (Section 3.3) [V: OW6][T].
- *"Running locally makes it HIPAA compliant."* The Security Rule covers stored data and requires safeguards whatever the network does [V: HHS].
- *"Redaction removed the personal data."* Patterns miss names and addresses, and even Presidio says it can't guarantee finding everything [V: PRS][T].

**Exercises, with checked answers.** Run the checks from the lab folder, with the virtual environment active.

1. *Precision at your traffic.* A classifier has 90% recall and a 2% false-positive rate. Your app sees 5,000 messages a day, 10 of them attacks. How many flags a day, and what share are real? Answer: 9 caught plus 99.8 false alarms, about 109 flags, of which about 8.3% are real. Check: `python -c "from guard import screen; s = screen(5000, 10/5000, 0.9, 0.02); print(round(s['caught'] + s['false_alarms'], 1), round(s['precision'], 3))"` prints `108.8 0.083` [T].
2. *Licence expressions.* What bucket does `(MIT OR Elastic-2.0) AND CC-BY-NC-4.0` fall into, and why? Answer: non-commercial; the OR takes the easier MIT, and the AND then takes the harder of permissive and non-commercial. Check: `python -c "from guard import classify_licence as c; print(c('(MIT OR Elastic-2.0) AND CC-BY-NC-4.0'))"` [T].
3. *Which legs?* An agent reads a public web page and then posts a summary to a public channel. It never touches private data. Does Meta's Rule of Two require approval? Answer: no; it has untrusted input and an outward action, two legs, not three. It can still post something embarrassing, which is why the rule is a floor, not a complete defence [V: RO2, OW6]. Check with the lab: `python -c "from examples import *; from guard import *; g = Gate(TOOLS, allowed={'fetch_page', 'send_email'}); g.record({'tool': 'fetch_page', 'args': {'url': 'https://docs.example.com/'}}); print(g.check({'tool': 'send_email', 'args': {'to': 'team@example.com', 'subject': 's', 'body': 'b'}}).verdict)"` prints `allow` [T].

**Five-question self-check.** Answers follow.

1. What does OWASP's 2026 edition say about preventing prompt injection, and what does it conclude defence must be?
2. Name the three legs of Meta's Rule of Two.
3. Why does the lab's gate refuse a URL containing a backslash even when Python says its host is allowed?
4. Llama Guard 4's card gives 69% recall and an 11% false-positive rate. Name two reasons that doesn't tell you how it will do on your app.
5. An app summarizes patients' records on a clinic's own server and never sends data out. Is that enough for HIPAA? What else is needed?

*Answers.* (1) No reliable prevention mechanism exists today; defence is architectural: assume the instruction boundary will be bypassed and limit what the model can do and reach [V: OW6]. (2) Untrusted input, access to sensitive data, and changing state or communicating externally [V: RO2]. (3) Browsers treat the backslash as a slash and would go to a different host; parsers that disagree defeat allowlists [V: WHW][T]. (4) It was measured on Meta's own in-house set, on output filtering in English; your attack rate changes its precision; an independent test found it missed far more; and attackers can tune against it [V: LG4, PWC, NAS][T]. (5) No; the Security Rule covers stored ePHI and requires administrative, physical and technical safeguards, starting with a risk analysis [V: HHS].

**You've got it when** you can take an agent design and say, for each tool, which legs it adds, what an attacker who fully controls the model could do with it, and which check in code stops that.

**Best next resources** (checked to exist on October 15, 2026): OWASP's 2026 list in its GitHub repository [V: OW6] and its agentic list [V: ASI]; Nasr et al. [V: NAS] and CaMeL [V: CAM]; Meta's Rule of Two [V: RO2]; Presidio's repository [V: PRS]; HHS's Security Rule summary and cloud guidance [V: HHS, HHC].

**A tutor prompt to practice with.** Paste this into Claude (modelled on claude/github-tutor-prompt.md):

```
Help me practise securing an AI app that uses tools, and handling personal
data and licences responsibly.

How to teach me: one idea at a time, a question I answer before you go on,
and a small worked example for each idea. When I'm wrong, show me the
reasoning rather than the answer, so I can find the mistake myself.

Topics, in order:
1. Prompt injection: direct and indirect, and why it can't be reliably
   prevented today.
2. Limiting what a fooled model can do: least privilege, checks in code,
   approval for risky actions, the Rule of Two.
3. Data leaving through a reply: links, images, and URL parsing.
4. Safety classifiers: recall, false positives, precision at real attack rates.
5. Personal data: what pattern redaction finds and misses; keeping it out of logs.
6. Which rules might apply (HIPAA, the GDPR, the EU AI Act), and licences
   for models, tools and data.

Teach defence only: describe attack types in plain words, and don't write
working attack text. For any product, version, law, date or score, tell me
it may have changed since your training and that I should check the
official source. This isn't legal advice, so say so when we touch the law.

Start by asking what my app does and which tools it can use.
```

**What to learn next.** Part 11, running models: serving engines, local models and the hardware they need.


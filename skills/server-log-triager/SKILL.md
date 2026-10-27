---
name: server-log-triager
description: Parses unformatted application logs to extract errors and sanitize PII fields into standard markdown tables. Use this skill when triaging system crashes, auditing application log outputs, or generating structured security incident tables from text logs.
license: MIT
metadata:
  claude-app-description: "Turns raw application logs into markdown tables of errors, with personal data masked. Use for crash triage, log audits or security incident tables."
  version: 1.0.0
---
# Server Log Structuring and Redaction Procedure

## 1. Pre-Flight Verification
* Ensure the target log asset exists and is accessible as local plaintext.
* Verify the file does not exceed context ceilings before printing contents.

## 2. Parsing and Execution Flow
1. Execute the bundled validation utility script to scrub and filter rows. Use the exact relative command formatting:
   `python3 scripts/clean_logs.py --input <target_log_file> --output structured_report.md`
2. Read `references/masking-rules.md` to confirm the regex compliance matrix matches standard enterprise obfuscation rules.

## 3. Post-Condition Checklist
* Verify the target output file `structured_report.md` contains a populated markdown grid table.
* Ensure no raw text rows from the origin file contain exposed system leak items.
* If the script throws a non-zero exit code error flag, stop execution immediately and report the diagnostic traceback trace to stderr.

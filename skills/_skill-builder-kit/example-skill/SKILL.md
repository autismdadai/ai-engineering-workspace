---
name: invoice-reconciliation
description: Reconciles invoice records against payment exports and flags mismatches.
Use when comparing invoices, payment CSVs, reconciliation reports, or unmatched transactions.
metadata:
  version: "1.0.0"
---

# Invoice reconciliation

## Inputs
- An invoice CSV.
- A payment-export CSV.
- The required matching key, if the source system uses one.

## Procedure
1. Inspect both schemas before changing data.
2. Normalize dates, identifiers, and numeric fields.
3. Match records using the documented matching rules.
4. Separate exact matches, ambiguous matches, unmatched invoices, and unmatched payments.
5. Reconcile totals against the source totals.
6. Write a new report. Never overwrite the source files.
7. Run the validation checks before reporting completion.

## Gotchas
- Do not treat similar names as proof of identity.
- Do not silently discard duplicate rows.
- Preserve source row identifiers in the output.
- If matching rules are ambiguous, report the ambiguity rather than inventing a rule.

## Output
Produce:
- matched.csv
- unmatched_invoices.csv
- unmatched_payments.csv
- ambiguous_matches.csv
- reconciliation_summary.md

#!/usr/bin/env python3
import csv
import sys
from collections import Counter

VALID = ["SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "UNVERIFIED"]

def main(path: str) -> None:
    counts = Counter()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "status" not in (reader.fieldnames or []):
            print("ERROR: CSV must have a 'status' column")
            sys.exit(1)
        for row in reader:
            s = row["status"].strip().upper().replace('"', "")
            if s not in VALID:
                print(f"WARN: unknown status '{row['status']}' on id {row.get('id')}")
                continue
            counts[s] += 1
            
    total = sum(counts.values())
    if total == 0:
        print("No scored claims")
        sys.exit(0)
        
    score = (counts["SUPPORTED"] + 0.5 * counts["PARTIALLY_SUPPORTED"]) / total
    print(f"Claims checked: {total}")
    for k in VALID:
        print(f"  {k:20s}: {counts[k]}")
    print(f"Accuracy: {score:.1%}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python score.py statuses.csv")
        sys.exit(2)
    main(sys.argv[1])

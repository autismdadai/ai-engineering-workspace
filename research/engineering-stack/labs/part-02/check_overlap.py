"""Check that no test ticket also appears among the prompt's examples.

    python check_overlap.py
    python check_overlap.py --examples other_examples.jsonl

A test item that also sits in the prompt (or in training data) measures memory,
not skill. This flags pairs with the same words, or with at least 80% of their
distinct words in common. Exit code 0 means nothing was found; 1 means overlap.
"""
import argparse
import os
import sys

import evalkit

HERE = os.path.dirname(os.path.abspath(__file__))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tickets", default=os.path.join(HERE, "data", "tickets.jsonl"))
    parser.add_argument("--examples", default=os.path.join(HERE, "data", "examples.jsonl"))
    args = parser.parse_args(argv)
    tickets = evalkit.load_jsonl(args.tickets)
    examples = evalkit.load_jsonl(args.examples)
    found = evalkit.overlaps([t["text"] for t in tickets], [e["text"] for e in examples])
    if not found:
        print(f"OVERLAP: none ({len(tickets)} test tickets, {len(examples)} examples)")
        return 0
    print(f"OVERLAP: {len(found)} test ticket(s) also appear among the examples")
    for i, j in found:
        print(f"  {tickets[i]['id']}: {tickets[i]['text']}")
        print(f"  {examples[j]['id']}: {examples[j]['text']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

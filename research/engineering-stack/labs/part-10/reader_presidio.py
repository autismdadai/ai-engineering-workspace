"""Reader test R4 (Engineering Stack, Part 10): Presidio with its spaCy model.

The lab's patterns find no names. This runs Presidio's full analyzer, which
adds spaCy's named-entity model, on the same invented records and prints
what it finds, so you can compare. Needs the cross-check requirements plus
spaCy's English model (about 382 MB):

    python -m pip install -r requirements-crosscheck.txt
    python -m spacy download en_core_web_lg
    python reader_presidio.py

There is no fixed expected output: send back what it prints.
"""
import sys

import examples as ex

try:
    import spacy
    from presidio_analyzer import AnalyzerEngine
except ImportError:
    sys.exit("Install the cross-check requirements first (Section 7.4).")

if not spacy.util.is_package("en_core_web_lg"):
    sys.exit("spaCy's en_core_web_lg isn't installed: python -m spacy download en_core_web_lg")

engine = AnalyzerEngine()
for number, (text, gold) in enumerate(ex.RECORDS):
    found = engine.analyze(text=text, language="en")
    print(f"record {number}:")
    for r in sorted(found, key=lambda r: r.start):
        print(f"  {r.entity_type:14} {r.score:.2f}  {text[r.start:r.end]!r}")
    names = [v for k, _, _, v in gold if k == "PERSON"]
    if names:
        hit = [n for n in names if any(text[r.start:r.end] == n and r.entity_type == "PERSON"
                                       for r in found)]
        print(f"  names in the record: {names}; found as PERSON: {hit}")

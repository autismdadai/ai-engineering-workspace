"""A tiny invented corpus for the Part 05 lab (illustrative, not a benchmark).

Twelve short documents about bike and kitchen repair, four queries, and
relevance labels (2 = answers the question, 1 = related, 0 or missing = not).
"""

DOCS = {
    "d01": "How to repair a punctured tire: remove the wheel, find the hole, patch the tube.",
    "d02": "Tire pressure guide for road bikes and mountain bikes.",
    "d03": "Error code E42 on the dishwasher means the drain pump is blocked.",
    "d04": "Clean the dishwasher filter every month to stop bad smells.",
    "d05": "Chain keeps slipping? Check for a worn chain or a stretched cable.",
    "d06": "Brake pads squeal when they are wet or worn; replace pads below 1.5 mm.",
    "d07": "Fixing a leaking kitchen tap: turn off the water and replace the washer.",
    "d08": "Inner tube sizes explained: match the tube to the tire width.",
    "d09": "The dishwasher will not drain: unblock the pump and check the hose.",
    "d10": "Oven temperature runs hot? Calibrate the thermostat with an oven thermometer.",
    "d11": "A slow leak in a bike tube is often a small puncture near the valve.",
    "d12": "Descale the kettle with vinegar to remove limescale.",
}

QUERIES = {
    "q1": "dishwasher E42",          # rare exact term: keyword search should win
    "q2": "fix a flat bicycle tyre",  # synonyms: words differ from the documents
    "q3": "dishwasher water not draining",
    "q4": "squeaky brakes",
}

QRELS = {
    "q1": {"d03": 2, "d09": 1},
    "q2": {"d01": 2, "d11": 1, "d08": 1},
    "q3": {"d09": 2, "d03": 1},
    "q4": {"d06": 2},
}

# Stand-in for a learned embedding model (model downloads are blocked in the
# test workspace). Each word maps to a concept; a text's vector is its bag of
# concepts. It shows WHY dense retrieval helps with synonyms; it is not how a
# real embedding model works and its scores mean nothing outside this lab.
CONCEPTS = {
    "fix": "repair", "fixing": "repair", "repair": "repair", "patch": "repair",
    "flat": "puncture", "puncture": "puncture", "punctured": "puncture",
    "hole": "puncture", "leak": "puncture",
    "tyre": "tire", "tire": "tire", "tube": "tire",
    "bicycle": "bike", "bike": "bike", "bikes": "bike",
    "squeaky": "noise", "squeal": "noise",
    "brakes": "brake", "brake": "brake", "pads": "brake",
    "dishwasher": "dishwasher",
    "drain": "drain", "draining": "drain", "unblock": "drain", "blocked": "drain",
    "water": "water", "pump": "pump", "e42": "errorcode", "error": "errorcode",
}

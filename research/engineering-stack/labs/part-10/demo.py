"""Walk through the lab (Engineering Stack, Part 10). Everything is invented."""
import guard as g
import examples as ex


def part(title):
    print(f"\n=== {title} ===")


part("1. A fooled model meets the gate")
r = ex.run_assistant(ex.VENDOR_PAGE, ex.ScriptedModel())
print("invisible characters removed:", r["invisible"])
print("tool calls:", r["log"])
print("the model proposed:", r["proposed"]["tool"], "to", r["proposed"]["args"]["to"])
print("decision:", r["decision"].verdict, "-", r["decision"].reason)
print("reply shown to the user:", r["reply"])
print("URLs removed from the reply:", len(r["removed"]))

part("2. An honest request still needs a person (Rule of Two)")


def person(decision, call):
    print("  the person sees:", call["tool"], call["args"]["to"], repr(call["args"]["subject"]))
    return {"decision": "approve", "action_id": decision.action_id}


r = ex.run_assistant("Release notes 4.2: faster sync.", ex.ScriptedModel(), approve=person)
print("sent to:", r["sent_to"])

part("3. Redaction")
text = ex.RECORDS[4][0]
red = g.Redactor().redact(text)
print("before:", text)
print("after: ", red.text)
print("the name is still there: pattern rules don't find names")

part("4. What a classifier's numbers mean at a 1% and a 0.1% attack rate")
print(f"{'classifier (published rates)':38} {'rate':>5} {'caught':>7} {'missed':>7} "
      f"{'false alarms':>12} {'precision':>9}")
for name, recall, fpr in (("Llama Guard 4 (recall 69%, FPR 11%)", 0.69, 0.11),
                          ("Prompt Guard 2 86M (97.5% at 1% FPR)", 0.975, 0.01)):
    for rate in (0.01, 0.001):
        s = g.screen(10_000, rate, recall, fpr)
        print(f"{name:38} {rate:>5} {s['caught']:>7.1f} {s['missed']:>7.1f} "
              f"{s['false_alarms']:>12.0f} {s['precision']:>9.3f}")
print("per 10,000 items; each rate is the vendor's, on its own test set")

part("5. Licence buckets")
for item, expr in (("nemoguardrails", "Apache-2.0"), ("presidio-analyzer", "MIT"),
                   ("python-stdnum", "LGPL-2.1-or-later"), ("arize-phoenix", "Elastic-2.0"),
                   ("Llama Guard 4 weights", "LicenseRef-Llama-4-Community"),
                   ("a CC BY-NC dataset", "CC-BY-NC-4.0")):
    print(f"{item:24} {expr:32} -> {g.classify_licence(expr)}")

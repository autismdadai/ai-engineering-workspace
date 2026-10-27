import re, sys, collections
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
# isolate section 3
s3 = text.split("\n## 3. Claim rows",1)[1].split("\n## 4. ",1)[0]
sections = re.split(r"^### ", s3, flags=re.M)[1:]
order = []
counts = {}
rows_all = []
for sec in sections:
    head = sec.splitlines()[0].strip()
    m = re.search(r"\((S0|P\d+|B\d|C)\)", head)
    key = m.group(1)
    order.append((key, head))
    c = collections.Counter()
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| ID") or line.startswith("|---"):
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            print("BAD CELLS", key, len(cells), line[:80]); continue
        rid, verdict = cells[0], cells[4]
        rows_all.append((key, rid, verdict, cells[5]))
        v = verdict.lower()
        labels = []
        for lab in ["confirmed","corrected","outdated","overstated","unsupported","illustrative","not checked yet"]:
            if v.startswith(lab):
                labels.append(lab); break
        if not labels:
            print("UNPARSED", key, rid, verdict)
            labels=["?"]
        c[labels[0]] += 1
        # secondary parts
        if ";" in v:
            c["(has secondary part)"] += 1
    counts[key] = c
cols = ["confirmed","corrected","outdated","overstated","unsupported","illustrative","not checked yet"]
tot = collections.Counter()
print("| Section | " + " | ".join(cols) + " | Rows |")
for key, head in order:
    c = counts[key]; n = sum(c[x] for x in cols)
    tot.update({x:c[x] for x in cols})
    print(f"| {key} | " + " | ".join(str(c[x]) for x in cols) + f" | {n} |")
print("| Total | " + " | ".join(str(tot[x]) for x in cols) + f" | {sum(tot.values())} |")
print()
for key,rid,verdict,grade in rows_all:
    if ";" in verdict or "[U]" in verdict or "[T]" in verdict:
        print(rid, "::", verdict, "::", grade)

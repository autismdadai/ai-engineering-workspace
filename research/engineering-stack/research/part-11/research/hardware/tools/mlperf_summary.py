import csv, sys, collections
path = sys.argv[1]
rows = list(csv.DictReader(open(path, newline='', encoding='utf-8')))
print("rows:", len(rows))
orgs = sorted({r['Organization'] for r in rows})
print("organizations (%d):" % len(orgs), "; ".join(orgs))
for div in ("closed", "open"):
    sub = [r for r in rows if r['Division'] == div]
    print(f"\n[{div}] rows={len(sub)}")
    for st in ("datacenter", "edge", "datacenter,edge"):
        models = sorted({r['MlperfModel'] for r in sub if r['SystemType'] == st})
        if models: print(f"  {st} models: {models}")
acc = collections.Counter(r['accelerator_model_name'] for r in rows if r['Division']=='closed')
print("\nclosed accelerators:")
for a, n in acc.most_common(): print(f"  {n:4d}  {a}")

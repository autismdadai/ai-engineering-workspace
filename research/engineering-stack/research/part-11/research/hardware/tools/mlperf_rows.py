import csv, sys
path, pat = sys.argv[1], sys.argv[2].lower()
rows = list(csv.DictReader(open(path, newline='', encoding='utf-8')))
import collections
print("Availability counts:", collections.Counter(r['Availability'] for r in rows))
for r in rows:
    if pat in r['accelerator_model_name'].lower() or pat in r['SystemName'].lower():
        print("|".join([r['Organization'], r['Availability'], r['Division'], r['SystemType'], r['SystemName'][:60], r['MlperfModel'], r['Scenario'], r['Result'], r['Units'], r['accelerator_model_name'], r['accelerators_per_node'], r['number_of_nodes'], r['weight_data_types'][:40]]))

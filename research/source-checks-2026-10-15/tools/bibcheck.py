"""Check Works Cited entries against Semantic Scholar (batch API). Usage: python bibcheck.py MANUAL OUT_JSON OUT_MD"""
import json, re, sys, time, urllib.request, difflib
manual, out_json, out_md = sys.argv[1:4]
lines = open(manual, encoding='utf-8').read().splitlines()[2530:2670]
entries = []
for ln in lines:
    m = re.match(r'^(\d+)\.\s+(.*)$', ln.strip())
    if m: entries.append((int(m.group(1)), m.group(2)))
ids = []
for n, txt in entries:
    for a in re.findall(r'arXiv (\d{4}\.\d{4,5})', txt):
        ids.append((n, 'arXiv:' + a))
    # bare ids after semicolons in multi-paper entries, e.g. "— arXiv 2310.11511; *CRAG* — arXiv 2401.15884"
    for d in re.findall(r'DOI (10\.\d{4,9}/[^\s;,)]+)', txt):
        ids.append((n, 'DOI:' + d.rstrip('.')))
uniq = sorted(set(i for _, i in ids))
def post(batch):
    url = 'https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,authors,venue,year,publicationVenue,externalIds,publicationDate,journal'
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, data=json.dumps({'ids': batch}).encode(), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except Exception as e:
            print('retry', attempt, e, file=sys.stderr); time.sleep(5 * (attempt + 1))
    return [None] * len(batch)
res = {}
for i in range(0, len(uniq), 100):
    b = uniq[i:i+100]
    for k, v in zip(b, post(b)): res[k] = v
    time.sleep(2)
def norm(s): return re.sub(r'[^a-z0-9 ]', '', (s or '').lower())
rows = []
for n, txt in entries:
    eids = [i for m, i in ids if m == n]
    titles = re.findall(r'\*([^*]+)\*', txt)
    surname = re.match(r'([A-Z][^\s,]+(?:\s[A-Z][^\s,]+)?)', txt)
    for pid in eids:
        p = res.get(pid)
        if not p:
            rows.append(dict(n=n, id=pid, status='NOT_FOUND_IN_S2', cited=txt)); continue
        best = max((difflib.SequenceMatcher(None, norm(t), norm(p['title'])).ratio() for t in titles), default=0)
        # titles in the manual are often short names ("PAL"); also accept containment
        contained = any(norm(t) and (norm(t) in norm(p['title']) or norm(p['title']) in norm(t)) for t in titles)
        authors = [a.get('name', '') for a in (p.get('authors') or [])]
        last_names = [a.split()[-1].lower() for a in authors if a]
        cited_names = re.findall(r'([A-Z][a-zà-ÿ\-]+)', txt.split('*')[0]) if '*' in txt else []
        name_ok = any(c.lower() in last_names for c in cited_names) if cited_names else None
        venue = (p.get('publicationVenue') or {}).get('name') or p.get('venue') or ''
        rows.append(dict(n=n, id=pid, s2_title=p['title'], title_score=round(best, 2), title_contained=contained,
                         first_authors=authors[:3], name_match=name_ok, s2_venue=venue, s2_year=p.get('year'),
                         s2_date=p.get('publicationDate'), cited=txt))
json.dump(rows, open(out_json, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
with open(out_md, 'w', encoding='utf-8') as f:
    f.write('| # | id | title match | author match | S2 venue (year) | S2 title |\n|---|---|---|---|---|---|\n')
    for r in rows:
        if r['status'] if 'status' in r else False:
            f.write(f"| {r['n']} | {r['id']} | NOT FOUND | | | |\n"); continue
        f.write(f"| {r['n']} | {r['id']} | {r['title_score']}{' (contained)' if r['title_contained'] else ''} | {r['name_match']} | {r['s2_venue']} ({r['s2_year']}) | {r['s2_title']} |\n")
noid = [n for n, t in entries if n not in {m for m, _ in ids}]
print('entries', len(entries), 'ids', len(uniq), 'resolved', sum(1 for v in res.values() if v), 'entries without arXiv/DOI:', noid)

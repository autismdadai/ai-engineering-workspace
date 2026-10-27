"""Check Works Cited IDs against the arXiv API (titles, authors, dates, journal_ref) and Crossref (DOIs);
merge Semantic Scholar venue data where an earlier run got it.
Usage: python bibcheck2.py MANUAL S2_JSON OUT_JSON OUT_MD"""
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

manual, s2json, out_json, out_md = sys.argv[1:5]
lines = open(manual, encoding="utf-8").read().splitlines()[2530:2670]
entries = []
for line in lines:
    m = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
    if m:
        entries.append((int(m.group(1)), m.group(2)))
s2 = {r["id"]: r for r in json.load(open(s2json, encoding="utf-8")) if "s2_title" in r}

ARXIV_RE = r"arXiv (\d{4}\.\d{4,5})"
DOI_RE = r"DOI (10\.\d{4,9}/[^\s;,)]+)"
SKIP_NAMES = {"et", "al", "and", "anthropic", "openai", "microsoft", "the"}


def get(url, tries=5):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bibcheck/1.0 (personal citation audit)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # network errors are retried, then reported
            print("retry", attempt, url[:80], e, file=sys.stderr)
            time.sleep(4 * (attempt + 1))
    return None


ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
ax = {}
arx = sorted({a for _, t in entries for a in re.findall(ARXIV_RE, t)})
for i in range(0, len(arx), 40):
    batch = arx[i:i + 40]
    raw = get("http://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": len(batch)}))
    if raw:
        for e in ET.fromstring(raw).findall("a:entry", ns):
            aid = re.sub(r"v\d+$", "", e.find("a:id", ns).text.rsplit("/", 1)[-1])
            jr = e.find("x:journal_ref", ns)
            doi = e.find("x:doi", ns)
            ax[aid] = dict(
                title=" ".join(e.find("a:title", ns).text.split()),
                authors=[x.find("a:name", ns).text for x in e.findall("a:author", ns)],
                published=e.find("a:published", ns).text[:10],
                updated=e.find("a:updated", ns).text[:10],
                journal_ref=jr.text if jr is not None else "",
                doi=doi.text if doi is not None else "",
            )
    time.sleep(3.5)

cr = {}
for d in sorted({d.rstrip(".") for _, t in entries for d in re.findall(DOI_RE, t)}):
    raw = get("https://api.crossref.org/works/" + urllib.parse.quote(d))
    if raw:
        m = json.loads(raw)["message"]
        cr[d] = dict(
            title=" ".join((m.get("title") or [""])[0].split()),
            authors=[(a.get("family") or "") for a in m.get("author", [])],
            container=(m.get("container-title") or [""])[0],
            volume=m.get("volume", ""),
            page=m.get("page", ""),
            year=(m.get("issued", {}).get("date-parts") or [[None]])[0][0],
        )
    time.sleep(1)


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def tscore(cited_titles, real):
    best = 0.0
    for t in cited_titles:
        a, b = norm(t), norm(real)
        if a and (a in b or b in a):
            return 1.0
        best = max(best, difflib.SequenceMatcher(None, a, b).ratio())
    return round(best, 2)


def names_in(lead):
    return [x for x in re.findall(r"([A-Z][a-zà-ÿ\-]+)", lead) if x.lower() not in SKIP_NAMES]


rows = []
for n, txt in entries:
    parts = [p for p in re.split(r";\s+", txt) if p.strip()]
    found = False
    prev_titles = re.findall(r"\*([^*]+)\*", txt)
    for part in parts:
        titles = re.findall(r"\*([^*]+)\*", part) or prev_titles
        nm = names_in(part.split("*")[0])
        for a in re.findall(ARXIV_RE, part):
            found = True
            p = ax.get(a)
            if not p:
                rows.append(dict(n=n, id="arXiv:" + a, problem="ID not returned by arXiv API", cited=part))
                continue
            last = [x.split()[-1].lower() for x in p["authors"]]
            s = s2.get("arXiv:" + a, {})
            rows.append(dict(n=n, id="arXiv:" + a, cited=part, real_title=p["title"], title_score=tscore(titles, p["title"]),
                             cited_names=nm, author_match=(any(x.lower() in last for x in nm) if nm else None),
                             first_author=(p["authors"][0] if p["authors"] else ""), n_authors=len(p["authors"]),
                             published=p["published"], updated=p["updated"], journal_ref=p["journal_ref"],
                             arxiv_doi=p["doi"], s2_venue=s.get("s2_venue", ""), s2_year=s.get("s2_year", "")))
        for d in re.findall(DOI_RE, part):
            found = True
            d = d.rstrip(".")
            p = cr.get(d)
            if not p:
                rows.append(dict(n=n, id="DOI:" + d, problem="DOI not resolved by Crossref", cited=part))
                continue
            fam = [y.lower() for y in p["authors"]]
            rows.append(dict(n=n, id="DOI:" + d, cited=part, real_title=p["title"], title_score=tscore(titles, p["title"]),
                             cited_names=nm, author_match=(any(x.lower() in fam for x in nm) if nm else None),
                             first_author=(p["authors"][0] if p["authors"] else ""),
                             container=p["container"], volume=p["volume"], page=p["page"], year=p["year"]))
    if not found:
        rows.append(dict(n=n, id="-", problem="no arXiv ID or DOI to check automatically", cited=txt))

json.dump(rows, open(out_json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
flag = [r for r in rows if r.get("problem") or r.get("title_score", 1) < 0.6 or r.get("author_match") is False]
with open(out_md, "w", encoding="utf-8") as f:
    f.write(f"# Works Cited check against arXiv API and Crossref ({len(rows)} rows, {len(entries)} entries)\n\n")
    f.write("| # | id | title score | author match | real first author | first posted / venue | real title |\n|---|---|---|---|---|---|---|\n")
    for r in rows:
        if r.get("problem"):
            f.write(f"| {r['n']} | {r['id']} | - | - | - | {r['problem']} | |\n")
            continue
        venue = r.get("journal_ref") or r.get("s2_venue") or r.get("container", "")
        when = r.get("published", r.get("year", ""))
        f.write(f"| {r['n']} | {r['id']} | {r['title_score']} | {r['author_match']} | {r.get('first_author', '')} | {when} {venue} {r.get('volume', '')} {r.get('page', '')} | {r['real_title']} |\n")
print("rows", len(rows), "arxiv resolved", len(ax), "of", len(arx), "crossref", len(cr), "flagged", len(flag))
for r in flag:
    print("FLAG", r["n"], r["id"], r.get("problem") or "", r.get("title_score"), r.get("author_match"), "|",
          (r.get("real_title") or "")[:90], "| cited:", r["cited"][:110])

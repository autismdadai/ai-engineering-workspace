"""Fetch latest version, upload date, licence and Python requirement from the PyPI JSON API."""
import json, sys, urllib.request
pkgs = sys.argv[1:]
rows = []
for p in pkgs:
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{p}/json", timeout=30) as r:
            d = json.load(r)
        info = d["info"]; ver = info["version"]
        files = d["releases"].get(ver) or []
        date = min((f["upload_time_iso_8601"] for f in files), default="?")[:10]
        lic = (info.get("license_expression") or info.get("license") or "").strip().splitlines()[0][:40] if (info.get("license_expression") or info.get("license")) else ""
        if not lic:
            lic = ";".join(c.split("::")[-1].strip() for c in info.get("classifiers", []) if c.startswith("License"))[:40]
        rows.append((p, ver, date, lic or "?", info.get("requires_python") or ""))
    except Exception as e:
        rows.append((p, "ERROR", str(e)[:60], "", ""))
for r in rows:
    print(" | ".join(r))

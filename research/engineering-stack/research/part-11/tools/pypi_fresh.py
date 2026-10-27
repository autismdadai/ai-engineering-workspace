"""Print version, release date, licence and Python requirement from PyPI."""
import json
import sys
import urllib.request

for name in sys.argv[1:]:
    try:
        url = f"https://pypi.org/pypi/{name}/json"
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.load(response)
        info = data["info"]
        version = info["version"]
        files = data["releases"].get(version) or []
        released = min((f["upload_time_iso_8601"] for f in files), default="?")[:10]
        licence = (info.get("license_expression") or info.get("license") or "").strip()
        licence = licence.splitlines()[0][:40] if licence else ""
        if not licence:  # fall back to the licence classifiers
            classifiers = [c.split("::")[-1].strip()
                           for c in info.get("classifiers", []) if c.startswith("License")]
            licence = ";".join(classifiers)[:40] or "?"
        python = info.get("requires_python") or ""
        print(" | ".join([name, version, released, licence, python]))
    except Exception as error:  # a missing package or network error
        print(" | ".join([name, "ERROR", str(error)[:60], "", ""]))

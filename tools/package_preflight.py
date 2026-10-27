#!/usr/bin/env python3
"""Inspect unified BattleScribe files and create an isolated local test bundle.

This checks XML structure, imports and identifiers; it does not establish
New Recruit runtime compatibility or license to redistribute upstream data.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

def local(tag):
    return tag.rsplit("}", 1)[-1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path)
    args = p.parse_args()
    directory = args.directory
    gst = directory / "Middlehammer-Unification.gst"
    cats = sorted(directory.glob("*.cat"))
    system = ET.parse(gst).getroot()
    roots = {p: ET.parse(p).getroot() for p in cats}
    errors = []
    warnings = []
    if len(cats) < 2:
        errors.append("Expected at least two catalogues")
    ids = {p: {e.get("id") for e in r.iter() if e.get("id")} for p, r in roots.items()}
    gst_ids = {e.get("id") for e in system.iter() if e.get("id")}
    cat_by_id = {r.get("id"): p for p, r in roots.items()}
    for p, root in roots.items():
        if root.get("gameSystemId") != system.get("id"):
            errors.append(f"{p.name}: gameSystemId mismatch")
        imports = [e for e in root.iter() if local(e.tag) == "catalogueLink"]
        for imp in imports:
            target = imp.get("targetId")
            if target not in cat_by_id:
                errors.append(f"{p.name}: external catalogue import {target} is absent")
        target_ids = {e.get("targetId") for e in root.iter() if e.get("targetId")}
        missing = sorted(target_ids - ids[p] - gst_ids - set(cat_by_id))
        if missing:
            errors.append(f"{p.name}: {len(missing)} unresolved reference IDs")
        if not any(local(e.tag) == "forceEntry" for e in root.iter()) and not any(local(e.tag) == "forceEntry" for e in system.iter()):
            warnings.append(f"{p.name}: no force entries discovered")
    report = {
        "status": "pass" if not errors else "fail",
        "gameSystemId": system.get("id"),
        "catalogues": [{"file": p.name, "id": r.get("id"), "name": r.get("name")} for p, r in roots.items()],
        "errors": errors, "warnings": warnings,
        "scope": "Static XML and local import checks only; not schema, runtime, licensing, or rules validation.",
    }
    report_file = directory / "package-preflight.json"
    report_file.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)
    package = directory / "middlehammer-v0.1-local-test.zip"
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [gst, *cats]:
            z.write(f, f.name)
    print(f"Created isolated test bundle: {package}")

if __name__ == "__main__":
    main()

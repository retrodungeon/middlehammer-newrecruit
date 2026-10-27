#!/usr/bin/env python3
"""Inventory the preserved 6th-edition BattleScribe archive; do not publish unverified data."""
import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("archive", type=Path)
    p.add_argument("--output", type=Path, default=Path("build/sixth-edition-inventory.json"))
    args = p.parse_args()
    records = []
    with zipfile.ZipFile(args.archive) as z:
        for member in z.infolist():
            if not member.filename.lower().endswith((".cat", ".gst", ".catz", ".gstz")):
                continue
            try:
                payload = z.read(member)
                if member.filename.lower().endswith((".catz", ".gstz")):
                    import io
                    with zipfile.ZipFile(io.BytesIO(payload)) as nested:
                        xmlname = next(n for n in nested.namelist() if n.lower().endswith((".cat", ".gst")))
                        payload = nested.read(xmlname)
                root = ET.fromstring(payload)
                records.append({"file": member.filename, "name": root.get("name"), "id": root.get("id"),
                                "revision": root.get("revision"), "gameSystemId": root.get("gameSystemId"),
                                "rootSelectionEntries": sum(e.tag.rsplit("}", 1)[-1] == "selectionEntry"
                                    for group in root if group.tag.rsplit("}", 1)[-1] == "selectionEntries" for e in group),
                                "rootEntryLinks": sum(e.tag.rsplit("}", 1)[-1] == "entryLink"
                                    for group in root if group.tag.rsplit("}", 1)[-1] == "entryLinks" for e in group)})
            except Exception as exc:
                records.append({"file": member.filename, "error": str(exc)})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps([r for r in records if "Space Marines" in (r.get("name") or "")], indent=2))
    print(f"Inventoried {len(records)} files; full report: {args.output}")

if __name__ == "__main__":
    main()

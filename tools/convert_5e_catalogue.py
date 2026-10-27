#!/usr/bin/env python3
"""Convert a 5e catalogue to the Middlehammer system and audit XML references."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

NS = "http://www.battlescribe.net/schema/catalogueSchema"
SYSTEM_ID = "sys-middlehammer-2026"
SOURCE_ID = "sys-9c90-407d-0876-14fb"

def convert(source, system, output, report):
    original = ET.parse(source)
    root = original.getroot()
    if root.tag.rsplit("}", 1)[-1] != "catalogue":
        raise ValueError("Expected a BattleScribe catalogue")
    if root.get("gameSystemId") != SOURCE_ID:
        raise ValueError(f"Unexpected catalogue gameSystemId: {root.get('gameSystemId')}")
    gst = ET.parse(system).getroot()
    if gst.get("id") != SYSTEM_ID:
        raise ValueError("Middlehammer GST has unexpected ID")
    source_ids = {e.get("id") for e in root.iter() if e.get("id")}
    system_ids = {e.get("id") for e in gst.iter() if e.get("id")}
    targets = {e.get("targetId") for e in root.iter() if e.get("targetId")}
    unresolved = sorted(targets - source_ids - system_ids)
    root.set("gameSystemId", SYSTEM_ID)
    output.parent.mkdir(parents=True, exist_ok=True)
    original.write(output, encoding="utf-8", xml_declaration=True)
    result = {
        "source": source.name, "catalogue": root.get("name"),
        "catalogueId": root.get("id"), "originalGameSystemId": SOURCE_ID,
        "convertedGameSystemId": SYSTEM_ID, "targetCount": len(targets),
        "unresolvedAgainstCatalogueAndGST": unresolved,
        "note": "Unresolved targets may live in imported catalogues. This is not a full New Recruit validation.",
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**result, "unresolvedAgainstCatalogueAndGST": len(unresolved)}, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("system", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    convert(a.source, a.system, a.output, a.report)

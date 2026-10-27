#!/usr/bin/env python3
"""Resolve a catalogue's external references against its source and target GSTs.

Reports each target ID with the source definition's element type/name, making
cross-edition mappings reviewable instead of blindly rewriting target IDs.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def local(tag):
    return tag.rsplit("}", 1)[-1]

def index(root):
    return {node.get("id"): node for node in root.iter() if node.get("id")}

def inspect(cat_path, source_path, target_path, report_path):
    cat = ET.parse(cat_path).getroot()
    source = ET.parse(source_path).getroot()
    target = ET.parse(target_path).getroot()
    if cat.get("gameSystemId") != source.get("id"):
        raise ValueError("Catalogue does not belong to supplied source GST")
    source_idx, target_idx, local_idx = index(source), index(target), index(cat)
    refs = {}
    for node in cat.iter():
        tid = node.get("targetId")
        if tid:
            refs.setdefault(tid, []).append({
                "element": local(node.tag), "name": node.get("name"),
                "id": node.get("id"),
            })
    records = []
    for tid in sorted(refs):
        if tid in local_idx or tid in target_idx:
            continue
        definition = source_idx.get(tid)
        records.append({
            "targetId": tid,
            "sourceDefinition": ({
                "kind": local(definition.tag), "name": definition.get("name"),
                "id": definition.get("id")
            } if definition is not None else None),
            "references": refs[tid][:8],
            "referenceCount": len(refs[tid]),
            "status": "source-gst-definition" if definition is not None else "unresolved-in-both-systems",
        })
    output = {
        "catalogue": cat.get("name"),
        "sourceGameSystemId": source.get("id"),
        "targetGameSystemId": target.get("id"),
        "totalDistinctReferences": len(refs),
        "externalReferenceCount": len(records),
        "foundInSourceGST": sum(x["sourceDefinition"] is not None for x in records),
        "missingInSourceGST": sum(x["sourceDefinition"] is None for x in records),
        "references": records,
        "caution": "Name similarity does not prove semantic equivalence. Do not automatically merge profiles, categories, or constraints.",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if k != "references"}, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("catalogue", type=Path)
    p.add_argument("source_gst", type=Path)
    p.add_argument("middlehammer_gst", type=Path)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    inspect(a.catalogue, a.source_gst, a.middlehammer_gst, a.report)

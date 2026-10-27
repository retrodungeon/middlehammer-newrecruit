#!/usr/bin/env python3
"""Cross-edition structural preflight for 3e Chaos Space Marines.

This script reports potential ID collisions and references requiring mapping.
It deliberately does NOT relabel a 3e catalogue as playable Middlehammer.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def local(tag):
    return tag.rsplit("}", 1)[-1]

def ids(root):
    return {e.get("id") for e in root.iter() if e.get("id")}

def definitions(root, kind):
    return {e.get("id"): e.get("name") for e in root.iter() if local(e.tag) == kind and e.get("id")}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalogue", type=Path)
    p.add_argument("middlehammer", type=Path)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    cat = ET.parse(a.catalogue).getroot()
    gst = ET.parse(a.middlehammer).getroot()
    cid, gid = ids(cat), ids(gst)
    targets = {e.get("targetId") for e in cat.iter() if e.get("targetId")}
    imports = [e.attrib for e in cat.iter() if local(e.tag) == "catalogueLink"]
    categories = definitions(cat, "categoryEntry")
    gst_categories = definitions(gst, "categoryEntry")
    profiles = definitions(cat, "profileType")
    gst_profiles = definitions(gst, "profileType")
    result = {
        "catalogue": cat.get("name"), "catalogueId": cat.get("id"),
        "sourceGameSystemId": cat.get("gameSystemId"),
        "middlehammerGameSystemId": gst.get("id"),
        "catalogueDefinitionCount": len(cid),
        "targetCount": len(targets),
        "idCollisionsWithMiddlehammer": sorted(cid & gid),
        "unresolvedTargetsAgainstCatalogueAndMiddlehammer": sorted(targets - cid - gid),
        "importedCatalogues": imports,
        "sourceCategoryEntries": categories,
        "middlehammerCategoryEntries": gst_categories,
        "sourceProfileTypes": profiles,
        "middlehammerProfileTypes": gst_profiles,
        "warning": "Preflight only. A 3e catalogue cannot be made playable by gameSystemId substitution alone.",
    }
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v)
                      for k, v in result.items()}, indent=2))

if __name__ == "__main__":
    main()

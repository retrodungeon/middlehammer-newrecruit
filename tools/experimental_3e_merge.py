#!/usr/bin/env python3
"""Build a dependency-complete *experimental* 3e catalogue against a 5e GST.

Copies missing source GST definitions into a generated target GST by preserving
their original XML identifiers. It does NOT translate 3e gameplay rules into 5e.
Only use for isolated compatibility testing; do not publish source-derived data
without permission.
"""
import argparse
import copy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def lname(tag):
    return tag.rsplit("}", 1)[-1]

def all_ids(root):
    return {x.get("id") for x in root.iter() if x.get("id")}

def find_parent(root, target):
    for parent in root.iter():
        if target in list(parent):
            return parent
    return None

def resolve(catalogue, source_gst, target_gst, out_gst, out_cat, report):
    ctree = ET.parse(catalogue)
    stree = ET.parse(source_gst)
    ttree = ET.parse(target_gst)
    c, s, t = ctree.getroot(), stree.getroot(), ttree.getroot()
    if c.get("gameSystemId") != s.get("id"):
        raise ValueError("Catalogue and source GST do not match")
    source_by_id = {x.get("id"): x for x in s.iter() if x.get("id")}
    added = []
    # Fixed-point closure: copied nodes can themselves refer to more source nodes.
    for _ in range(1000):
        known = all_ids(c) | all_ids(t)
        wanted = {x.get("targetId") for root in (c, t) for x in root.iter() if x.get("targetId")}
        missing = sorted(wanted - known)
        candidates = [source_by_id[x] for x in missing if x in source_by_id]
        if not candidates:
            break
        progress = 0
        for node in candidates:
            if node.get("id") in all_ids(t):
                continue
            parent = find_parent(s, node)
            if parent is None:
                continue
            parent_name = lname(parent.tag)
            # Copy only top-level definitions under matching containers.
            if parent not in list(s):
                continue
            container = next((x for x in t if lname(x.tag) == parent_name), None)
            if container is None:
                container = ET.SubElement(t, parent.tag)
            container.append(copy.deepcopy(node))
            added.append({"id": node.get("id"), "name": node.get("name"), "type": lname(node.tag), "container": parent_name})
            progress += 1
        if progress == 0:
            break
    c.set("gameSystemId", t.get("id"))
    known = all_ids(c) | all_ids(t)
    unresolved = sorted({x.get("targetId") for root in (c, t) for x in root.iter() if x.get("targetId")} - known)
    out_gst.parent.mkdir(parents=True, exist_ok=True)
    out_cat.parent.mkdir(parents=True, exist_ok=True)
    ttree.write(out_gst, encoding="utf-8", xml_declaration=True)
    ctree.write(out_cat, encoding="utf-8", xml_declaration=True)
    result = {
        "sourceCatalogue": c.get("name"), "sourceGST": s.get("name"),
        "targetGST": t.get("name"), "definitionsCopied": added,
        "unresolvedTargetIds": unresolved,
        "warning": "Experimental dependency closure, NOT rules-equivalent, and NOT New Recruit validated.",
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Copied {len(added)} top-level definitions; {len(unresolved)} unresolved target IDs")
    if unresolved:
        raise SystemExit("Unresolved dependencies remain; see report")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("catalogue", type=Path)
    p.add_argument("source_gst", type=Path)
    p.add_argument("target_gst", type=Path)
    p.add_argument("out_gst", type=Path)
    p.add_argument("out_cat", type=Path)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    resolve(a.catalogue, a.source_gst, a.target_gst, a.out_gst, a.out_cat, a.report)

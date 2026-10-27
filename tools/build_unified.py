#!/usr/bin/env python3
"""Build and validate a single Middlehammer GST for 5e Guard and 3e Chaos.

Experimental integration only: does not establish rules equivalence or New Recruit compatibility.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from build_foundation import build
from experimental_3e_merge import resolve
from convert_5e_catalogue import convert

def ids(root):
    return [e.get("id") for e in root.iter() if e.get("id")]

def targets(root):
    return {e.get("targetId") for e in root.iter() if e.get("targetId")}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fifth", type=Path, required=True)
    p.add_argument("--third", type=Path, required=True)
    p.add_argument("--guard", type=Path, required=True)
    p.add_argument("--chaos", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("build/unified"))
    a = p.parse_args()
    out = a.output
    out.mkdir(parents=True, exist_ok=True)
    base = out / "foundation-base.gst"
    unified = out / "Middlehammer-Unification.gst"
    chaos = out / "Chaos Space Marines (2002).cat"
    guard = out / "Imperial Guard - Codex 2009.cat"
    build(a.fifth, base)
    resolve(a.chaos, a.third, base, unified, chaos, out / "chaos-merge-report.json")
    convert(a.guard, unified, guard, out / "imperial-guard-audit.json")
    # Historical 2009 codex exclusions. The upstream 5e-compatible catalogue
    # also includes units released in later editions. Remove their top-level
    # entry links; leave shared definitions intact to avoid dangling references.
    excluded = {"Rogal Dorn Battle Tank", "Bullgryn Squad", "Field Ordnance Battery"}
    tree = ET.parse(guard)
    cat = tree.getroot()
    ns = "{http://www.battlescribe.net/schema/catalogueSchema}"
    root_links = cat.find(ns + "entryLinks")
    if root_links is None:
        raise SystemExit("Guard catalogue has no root entryLinks")
    removed = []
    for link in list(root_links):
        if link.get("name") in excluded:
            removed.append(link.get("name"))
            root_links.remove(link)
    if set(removed) != excluded:
        raise SystemExit(f"Historical exclusions not found as expected: {sorted(excluded - set(removed))}")
    tree.write(guard, encoding="utf-8", xml_declaration=True)
    (out / "guard-historical-exclusions.json").write_text(json.dumps({"excluded": sorted(removed), "basis": "Not present in the 2009 Codex: Imperial Guard army list", "scope": "Top-level selections only"}, indent=2) + "\\n")
    # Preserve the public-facing codex name and increment the catalogue revision.
    guard_tree = ET.parse(guard)
    guard_root = guard_tree.getroot()
    guard_root.set("name", "Imperial Guard (5th Edition, 2009)")
    guard_root.set("revision", "8")
    ET.register_namespace("", "http://www.battlescribe.net/schema/catalogueSchema")
    guard_tree.write(guard, encoding="utf-8", xml_declaration=True)
    system = ET.parse(unified).getroot()
    catalogues = [ET.parse(path).getroot() for path in (guard, chaos)]
    system_ids = ids(system)
    errors = []
    if len(system_ids) != len(set(system_ids)):
        errors.append("Duplicate IDs inside unified GST")
    for path, cat in zip((guard, chaos), catalogues):
        if cat.get("gameSystemId") != system.get("id"):
            errors.append(f"{path.name}: wrong gameSystemId")
        cat_ids = ids(cat)
        if len(cat_ids) != len(set(cat_ids)):
            errors.append(f"{path.name}: duplicate IDs within catalogue")
        unresolved = targets(cat) - set(cat_ids) - set(system_ids)
        if unresolved:
            errors.append(f"{path.name}: {len(unresolved)} unresolved target IDs")
    # Catalogues can reuse IDs for common inherited definitions, but detect collisions
    # where different objects carry the same ID.
    guard_ids, chaos_ids = set(ids(catalogues[0])), set(ids(catalogues[1]))
    cross_collisions = sorted(guard_ids & chaos_ids)
    if cross_collisions:
        errors.append(f"Catalogue-to-catalogue ID collisions: {len(cross_collisions)}")
    result = {
        "gameSystemId": system.get("id"),
        "catalogues": [x.get("name") for x in catalogues],
        "systemDefinitionCount": len(system_ids),
        "catalogueIdCollisions": cross_collisions,
        "errors": errors,
        "validation": "Structural only; no New Recruit runtime or gameplay verification.",
    }
    (out / "unified-validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({**result, "catalogueIdCollisions": len(cross_collisions)}, indent=2))
    if errors:
        raise SystemExit("Unified build failed structural checks")

if __name__ == "__main__":
    main()

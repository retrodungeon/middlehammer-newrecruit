#!/usr/bin/env python3
"""Experimental 7e Space Marines -> Middlehammer bridge; never overwrites production files."""
import argparse
import copy
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "http://www.battlescribe.net/schema"
C = NS + "/catalogueSchema"
G = NS + "/gameSystemSchema"
def local(tag): return tag.rsplit("}", 1)[-1]
def children(root, name):
    return next((e for e in root if local(e.tag) == name), None)
def all_ids(root):
    return {e.get("id") for e in root.iter() if e.get("id")}
def catalogue_namespace(node):
    for e in node.iter():
        if e.tag.startswith("{"): e.tag = f"{{{C}}}{local(e.tag)}"

def reassign_ids(node, mapping):
    for e in node.iter():
        for key, value in list(e.attrib.items()):
            if key in ("id", "targetId", "typeId", "characteristicTypeId", "costTypeId", "profileTypeId") and value in mapping:
                e.set(key, mapping[value])
def run(catpath, sourcegst, mhgst, outcat, outgst):
    ET.register_namespace("", C)
    cat = ET.parse(catpath).getroot()
    src = ET.parse(sourcegst).getroot()
    mh = ET.parse(mhgst).getroot()
    if cat.get("gameSystemId") != src.get("id"):
        raise ValueError("Source catalogue and 7e GST do not match")
    existing = all_ids(mh)
    mapping = {}
    # Preserve Middlehammer's existing cost/profile type identities by name;
    # characteristic IDs must also be translated to the corresponding MH type.
    for section, item in (("costTypes", "costType"), ("profileTypes", "profileType")):
        dest = children(mh, section)
        origin = children(src, section)
        if origin is None: continue
        if dest is None:
            dest = ET.SubElement(mh, f"{{{G}}}{section}")
        for entry in origin:
            match = next((x for x in dest if x.get("name") == entry.get("name")), None)
            if match is not None:
                mapping[entry.get("id")] = match.get("id")
                if item == "profileType":
                    a = children(entry, "characteristicTypes")
                    b = children(match, "characteristicTypes")
                    if a is not None and b is not None:
                        for char in a:
                            other = next((z for z in b if z.get("name") == char.get("name")), None)
                            if other is not None: mapping[char.get("id")] = other.get("id")
            else:
                dest.append(copy.deepcopy(entry))
    # Make 7e categories resolve to Middlehammer FOC category IDs when names match.
    oldcategories = children(src, "categoryEntries")
    mhcategories = children(mh, "categoryEntries")
    if oldcategories is not None and mhcategories is not None:
        for category in oldcategories:
            same = next((e for e in mhcategories if e.get("name") == category.get("name")), None)
            if same is not None: mapping[category.get("id")] = same.get("id")
    # Army-list-only: discard 7e formations and detachments.\n    # Middlehammer supplies its own 5e force organization.\n    cat_forces = children(cat, 'forceEntries')\n    if cat_forces is not None:\n        cat.remove(cat_forces)\n    # Bring over army-building shared entries and equipment profiles.
    # Catalogue-local copies isolate 7e rules from existing Guard/CSM definitions.
    for section in ("sharedSelectionEntries", "sharedSelectionEntryGroups", "sharedProfiles"):
        origin = children(src, section)
        if origin is None: continue
        dest = children(cat, section)
        if dest is None: dest = ET.SubElement(cat, f"{{{C}}}{section}")
        for entry in origin:
            cloned = copy.deepcopy(entry)
            catalogue_namespace(cloned)
            dest.append(cloned)
    # Resolve any duplicated IDs with existing Middlehammer definitions.
    # Preserve internal references across the imported catalogue.
    for ident in all_ids(cat):
        if ident in existing and ident not in mapping:
            mapping[ident] = str(uuid.uuid5(uuid.NAMESPACE_URL, "middlehammer/space-marines-7e/" + ident))
    # Remove catalogue-local categories mapped to existing system categories;
    # otherwise the same ID would be defined twice across GST and CAT.
    cat_categories = children(cat, "categoryEntries")
    if cat_categories is not None:
        for category in list(cat_categories):
            if category.get("id") in mapping:
                cat_categories.remove(category)
    reassign_ids(cat, mapping)
    cat.set("id", "mh-sm-7e-2015")
    cat.set("name", "Space Marines (7th Edition, 2015) [Experimental]")
    cat.set("gameSystemId", mh.get("id"))
    cat.set("gameSystemRevision", str(int(mh.get("revision", "5")) + 1))
    cat.set("battleScribeVersion", "2.03")
    cat.set("revision", "1")
    mh.set("revision", str(int(mh.get("revision", "5")) + 1))
    mh.set("battleScribeVersion", "2.03")
    # Important: source force organizations remain in the catalogue for now;
    # they must be audited before release as a Middlehammer faction.
    for target, root in ((outcat, cat), (outgst, mh)):
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)
    print(f"Mapped {len(mapping)} IDs; created {outcat} and {outgst}")
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source_cat"); p.add_argument("source_gst"); p.add_argument("middlehammer_gst")
    p.add_argument("output_cat"); p.add_argument("output_gst")
    a = p.parse_args()
    run(a.source_cat, a.source_gst, a.middlehammer_gst, a.output_cat, a.output_gst)

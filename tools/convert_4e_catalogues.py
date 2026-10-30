#!/usr/bin/env python3
"""Convert 4th Edition catalogues (Kothra/Warhammer-40-000-4th-Edition-for-NewRecruit).

Only books not already covered by another source are converted (CONVERTED). The
source's other catalogues are the same books the 3rd and 5th Edition sources provide.

For each converted catalogue:
  * the source's opt-in "Forge World" switch is treated as always on (policy: Forge
    World / Imperial Armour content is allowed) and removed;
  * conditions on entries defined in *other* 4th Edition catalogues (left over from
    copying entries between books; never true inside this book) are folded away;
  * 4th Edition Force Organization categories, Force Customization, Additional Units
    and the points cost type are remapped to the Middlehammer equivalents; the
    "Standard Mission" force becomes the Middlehammer standard force;
  * the catalogue is retargeted to the Middlehammer game system.
Missing shared definitions are copied from the 4th Edition game system into the
Middlehammer GST.

Used by tools/build_middlehammer.py.
"""
import copy
from pathlib import Path
import xml.etree.ElementTree as ET

from convert_7e_catalogues import simplify_modifier

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
SOURCE_SYSTEM_ID = "sys-b41a-8226-286b-0dea"
MH_SYSTEM_ID = "sys-middlehammer-2026"
MH_POINTS = "6f18-a8fc-2c5b-9517"
FORGE_WORLD_SWITCH = "375a-d331-f8e5-1936"

# Source file stem -> books not available from another source.
CONVERTED = ["Space Marines (4E)", "Tyranids (4E)", "Blood Angels (4E)"]

ID_MAP = {
    "0d45-9523-cfd8-4efd": "ac8d-efba-1884-d3ad",  # HQ
    "23e2-2a28-50f4-a3c1": "default-category",     # Troops
    "39ab-2bcd-49d1-cfef": "978c-e18f-8aeb-f4c1",  # Elites
    "11cf-dc94-5c14-2c2a": "74fe-37c3-fbbf-849e",  # Fast Attack
    "6a52-1951-5b0c-024e": "9260-7d57-be5c-bd52",  # Heavy Support
    "7466-cf81-3a11-64ab": "525f-0a42-3f5c-5613",  # Force Customization -> Configuration
    "0589-7c29-bfa2-d566": "be45-5314-4388-5bfd",  # Additional Units -> No Force Org Slot
    "4deb-313d-6685-f48b": MH_POINTS,              # Points
    "916a-7942-cedc-170c": "mh-test-force",        # Standard Mission -> MH standard force
}
REF_ATTRS = ("targetId", "childId", "typeId", "field", "scope")
KEYWORDS = {"any", "model", "unit", "upgrade", "mount", "crew"}


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def q(tag, ns=CAT_NS):
    return f"{{{ns}}}{tag}"


def remap(root):
    n = 0
    for el in root.iter():
        for attr in REF_ATTRS:
            v = el.get(attr)
            if v in ID_MAP:
                el.set(attr, ID_MAP[v])
                n += 1
        if lname(el.tag) == "cost" and el.get("typeId") == MH_POINTS:
            el.set("name", "Points")
    return n


def count_value(cond, count):
    v, t = float(cond.get("value") or 0), cond.get("type")
    if t in ("instanceOf", "notInstanceOf"):
        return (count > 0) == (t == "instanceOf")
    return {"equalTo": count == v, "notEqualTo": count != v, "atLeast": count >= v, "greaterThan": count > v,
            "lessThan": count < v, "atMost": count <= v}[t]


def fold(cat, const):
    """Simplify every modifier (or modifier group) with a constant condition; drop those
    that never apply."""
    par = {c: p for p in cat.iter() for c in p}
    changed = 0
    for mod in [m for m in cat.iter() if lname(m.tag) in ("modifier", "modifierGroup")]:
        own = [c for x in mod.findall(q("conditions")) + mod.findall(q("conditionGroups")) for c in x.iter()]
        if not any(const(c) is not None for c in own if lname(c.tag) == "condition"):
            continue
        if simplify_modifier(mod, const) == "never":
            par[mod].remove(mod)
        changed += 1
    return changed


def convert_one(path, source_gst_ids, report):
    tree = ET.parse(path)
    cat = tree.getroot()
    if cat.get("gameSystemId") != SOURCE_SYSTEM_ID:
        raise SystemExit(f"{path.name}: not a 4th Edition catalogue")
    if cat.find(q("catalogueLinks")) is not None and len(cat.find(q("catalogueLinks"))):
        raise SystemExit(f"{path.name}: catalogue links are not supported")
    entry = {"edition": 4, "source": path.name, "sourceName": path.stem, "id": cat.get("id")}

    # Forge World switch: always on.
    for cont in ("selectionEntries", "entryLinks"):
        r = cat.find(q(cont))
        for el in (list(r) if r is not None else []):
            if el.get("targetId") == FORGE_WORLD_SWITCH or el.get("id") == FORGE_WORLD_SWITCH:
                r.remove(el)
    entry["forgeWorldUnlocked"] = fold(
        cat, lambda c: count_value(c, 1) if c.get("childId") == FORGE_WORLD_SWITCH else None)

    # References to entries of other 4th Edition books: never selected here.
    defined = {e.get("id") for e in cat.iter() if e.get("id")} | source_gst_ids
    foreign = sorted({c.get("childId") for c in cat.iter() if lname(c.tag) in ("condition", "repeat")
                      and c.get("childId") and c.get("childId") not in defined | KEYWORDS})
    entry["foreignConditionsFolded"] = fold(
        cat, lambda c: count_value(c, 0) if c.get("childId") in foreign else None)
    par = {c: p for p in cat.iter() for c in p}
    repeats = [r for r in cat.iter() if lname(r.tag) == "repeat" and r.get("childId") in foreign]
    for r in repeats:
        mod = par[par[r]]
        par[mod].remove(mod)   # a repeat of something never selected adds nothing
    entry["foreignRepeatsRemoved"] = len(repeats)
    left = {c.get("childId") for c in cat.iter() if lname(c.tag) in ("condition", "repeat")} & set(foreign)
    if left:
        raise ValueError(f"{path.stem}: unresolved references remain: {sorted(left)}")

    entry["referencesRemapped"] = remap(cat)
    cat.set("gameSystemId", MH_SYSTEM_ID)
    return tree, entry


def close_over_gst(catalogues, source_gst, gst, report):
    """Copy top-level 4th Edition game-system definitions the catalogues need."""
    top = {}
    for container in source_gst:
        if lname(container.tag) in ("forceEntries", "entryLinks", "comment", "conditions"):
            continue
        for node in container:
            if node.get("id"):
                top[node.get("id")] = (lname(container.tag), node)
    copied = []
    for _ in range(100):
        known = {e.get("id") for r in [gst] + catalogues for e in r.iter() if e.get("id")}
        wanted = {e.get(a) for r in [gst] + catalogues for e in r.iter() for a in ("targetId", "childId", "typeId")
                  if e.get(a)}
        missing = sorted(i for i in wanted - known if i in top)
        if not missing:
            break
        for i in missing:
            cname, node = top[i]
            container = gst.find(q(cname, GST_NS))
            if container is None:
                container = ET.SubElement(gst, q(cname, GST_NS))
            new = copy.deepcopy(node)
            remap(new)
            container.append(new)
            copied.append(node.get("name"))
    report["gstDefinitions4eCopied"] = len(copied)


def convert_4e(source, gst, report):
    source = Path(source)
    source_gst = ET.parse(next(source.glob("*.gst"))).getroot()
    if source_gst.get("id") != SOURCE_SYSTEM_ID:
        raise SystemExit("Unexpected 4th Edition game system ID")
    gst_ids = {e.get("id") for e in source_gst.iter() if e.get("id")}
    trees = {}
    for name in CONVERTED:
        p = source / f"{name}.cat"
        tree, entry = convert_one(p, gst_ids, report)
        trees[entry["id"]] = (p, tree, entry)
    close_over_gst([t.getroot() for _, t, _ in trees.values()], source_gst, gst, report)
    report["converted4e"] = [e for _, _, e in trees.values()]
    return trees


if __name__ == "__main__":
    raise SystemExit("Run tools/build_middlehammer.py, which builds every Middlehammer catalogue.")

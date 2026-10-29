#!/usr/bin/env python3
"""Convert 3rd Edition catalogues (KSnyder1986/Warhammer-40k-3rd-Edition) to Middlehammer.

For every non-homebrew catalogue in the source folder:
  * homebrew content (behind the 3e "Homebrew" toggle or named "(Homebrew)") is
    hidden and unlinked from the army list (policy: no homebrew);
  * content gated behind the 3e "Imperial Armour" toggle is made always available
    (policy: Forge World / Imperial Armour / White Dwarf content is allowed);
  * 3e Force Organization categories, Configuration, Super-Heavy and the 3e points
    cost type are remapped to the Middlehammer (5e-based) equivalents, in every
    attribute that references them (category links, conditions, constraints, costs);
  * catalogues are retargeted to the Middlehammer game system.
Missing shared definitions are copied from the 3e game system into the Middlehammer
GST by fixed-point closure. Catalogue IDs are preserved so catalogue links (e.g.
chapter lists importing Space Marines 1999) keep working.

Used by tools/build_middlehammer.py.
"""
import argparse
import copy
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET


CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
SOURCE_SYSTEM_ID = "96e2-b781-50d7-3d18"
MH_SYSTEM_ID = "sys-middlehammer-2026"

HOMEBREW_TOGGLE = "eca8-ace3-d503-7923"
IA_TOGGLE = "3261-6601-5bfe-f5d0"

ID_MAP = {
    "a8a7-7a4b-5f7e-2138": "ac8d-efba-1884-d3ad",  # HQ
    "0ef5-5056-d52e-3cfd": "default-category",     # Troops
    "6d25-b346-c314-6911": "978c-e18f-8aeb-f4c1",  # Elites
    "34e2-d53c-28ab-44cf": "74fe-37c3-fbbf-849e",  # Fast Attack
    "aacb-8a81-62c0-3db8": "9260-7d57-be5c-bd52",  # Heavy Support
    "a090-a855-c7de-f5c3": "168b-a772-94f7-83f5",  # Dedicated Transport
    "18d4-c759-8e80-4eb6": "525f-0a42-3f5c-5613",  # Configuration
    "6b90-dc9c-1a49-3fdc": "5968-f35e-18fd-612b",  # Super-Heavy
    "4ed5-2f92-9abc-2870": "6f18-a8fc-2c5b-9517",  # pts -> Points
    "7da2-40c9-890c-3239": "mh-test-force",        # 3e "Standard Missions" force -> MH standard force
}
MH_POINTS = "6f18-a8fc-2c5b-9517"
NO_FORCE_ORG = "be45-5314-4388-5bfd"
REF_ATTRS = ("targetId", "childId", "typeId", "field", "scope")

# Existing published files keep their names (New Recruit already tracks them).
EXISTING_FILENAMES = {"0f19-9487-acbb-e047": "Chaos Space Marines - Codex 2002.cat"}

ID_RE = re.compile(r"^[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}$")


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def is_homebrew_catalogue(name):
    return "homebrew" in name.lower() or "unofficial" in name.lower()


def display_name(name):
    m = re.match(r"^(.*?)\s*\((.*)\)\s*$", name)
    if m:
        return f"{m.group(1)} (3rd Edition, {m.group(2)})"
    return f"{name} (3rd Edition)"


def parents(root):
    return {child: parent for parent in root.iter() for child in parent}


def toggle_modifiers(root, toggle):
    """Yield (modifier, single_condition) for hidden-set-true modifiers gated on toggle==0."""
    for mod in root.iter():
        if lname(mod.tag) != "modifier":
            continue
        if (mod.get("field"), mod.get("type"), mod.get("value")) != ("hidden", "set", "true"):
            continue
        conds = [c for c in mod.iter() if lname(c.tag) == "condition"]
        hits = [c for c in conds if c.get("childId") == toggle]
        if not hits:
            continue
        for c in hits:
            if (c.get("type"), c.get("value")) != ("equalTo", "0"):
                raise ValueError(f"Unexpected toggle condition {c.attrib}")
        if any(lname(g.tag) == "conditionGroup" and g.get("type") != "and" for g in mod.iter()):
            raise ValueError("Toggle used inside a non-AND condition group; review manually")
        yield mod, len(conds) == 1


def hide(el):
    el.set("hidden", "true")
    mods = el.find(f"{{{CAT_NS}}}modifiers")
    if mods is not None:
        for m in list(mods):
            if m.get("field") == "hidden":
                mods.remove(m)


def strip_homebrew(root, report):
    """Hide homebrew content: anything behind the 3e Homebrew toggle or named "(Homebrew)".

    Hidden rather than deleted so every reference stays resolvable; New Recruit never
    offers hidden entries. Root-level links to homebrew entries are removed outright.
    """
    par = parents(root)
    hidden = []
    for mod, single in list(toggle_modifiers(root, HOMEBREW_TOGGLE)):
        if not single:
            raise ValueError("Homebrew toggle combined with other conditions; review manually")
        owner = par[par[mod]]
        hide(owner)
        hidden.append(owner)
    for el in root.iter():
        if lname(el.tag) in ("selectionEntry", "entryLink", "selectionEntryGroup", "entryLinks") \
                and "(homebrew)" in (el.get("name") or "").lower() and el not in hidden:
            hide(el)
            hidden.append(el)
    for cont in ("entryLinks", "selectionEntries"):
        r = root.find(f"{{{CAT_NS}}}{cont}")
        if r is not None:
            for el in list(r):
                if el in hidden:
                    r.remove(el)
    report["homebrewHidden"] = sorted({el.get("name") for el in hidden})


def dedupe_ids(root, report):
    seen, fixed = set(), 0
    for el in root.iter():
        i = el.get("id")
        if not i:
            continue
        if i in seen and lname(el.tag) == "categoryLink":
            n = 1
            while f"{i}-mh{n}" in seen:
                n += 1
            el.set("id", f"{i}-mh{n}")
            fixed += 1
        seen.add(el.get("id"))
    report["duplicateIdsRenamed"] = fixed


def unlock_imperial_armour(root, report):
    par = parents(root)
    count = 0
    for mod, _single in list(toggle_modifiers(root, IA_TOGGLE)):
        # Condition is always false once IA is permitted, and it sits in an AND
        # (or alone), so the whole modifier can never fire: remove it.
        par[mod].remove(mod)
        count += 1
    report["imperialArmourUnlocked"] = count


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


def ids(root):
    return {e.get("id") for e in root.iter() if e.get("id")}


def refs(root):
    out = set()
    for e in root.iter():
        for attr in ("targetId", "childId"):
            v = e.get(attr)
            if v and (ID_RE.match(v) or v.startswith(("sys-", "mh-"))):
                out.add(v)
    return out


def close_over_gst(catalogues, source_gst, target_gst, report):
    """Copy top-level definitions the catalogues need from the 3e GST into the MH GST."""
    top = {}
    for container in source_gst:
        if lname(container.tag) in ("forceEntries", "entryLinks", "comment"):
            continue
        for node in container:
            if node.get("id"):
                top[node.get("id")] = (lname(container.tag), node)
    copied = []
    for _ in range(100):
        known = ids(target_gst) | set().union(*(ids(c) for c in catalogues))
        wanted = refs(target_gst) | set().union(*(refs(c) for c in catalogues))
        missing = [i for i in sorted(wanted - known) if i in top]
        if not missing:
            break
        for i in missing:
            cname, node = top[i]
            container = next((x for x in target_gst if lname(x.tag) == cname), None)
            if container is None:
                container = ET.SubElement(target_gst, f"{{{GST_NS}}}{cname}")
            new = copy.deepcopy(node)
            remap(new)
            container.append(new)
            copied.append({"id": i, "name": node.get("name"), "container": cname})
    report["gstDefinitionsCopied"] = copied


def ensure_force_links(gst, report):
    force = gst.find(f"{{{GST_NS}}}forceEntries/{{{GST_NS}}}forceEntry[@id='mh-test-force']")
    links = force.find(f"{{{GST_NS}}}categoryLinks")
    present = {l.get("targetId") for l in links}
    added = []
    for name, target, link_id in (
        ("Dedicated Transport", "168b-a772-94f7-83f5", "mh-foc-transport"),
        ("Unique", "1f0d-7d41-7ef9-ce4a", "mh-foc-unique"),
        ("Super-Heavy", "5968-f35e-18fd-612b", "mh-foc-superheavy"),
        ("Configuration", "525f-0a42-3f5c-5613", "mh-foc-configuration"),
        ("No Force Org Slot", NO_FORCE_ORG, "mh-foc-noslot"),
    ):
        if target not in present:
            ET.SubElement(links, f"{{{GST_NS}}}categoryLink",
                          {"name": name, "hidden": "false", "id": link_id, "targetId": target})
            added.append(name)
    report["forceCategoryLinksAdded"] = added


def expose_unlisted_units(cat, report):
    """Source fix: a catalogue with no army list entries (Codex Assassins) offers nothing.
    Link its shared unit entries at the root so they can be selected."""
    if any(cat.find(f"{{{CAT_NS}}}{c}") is not None and len(cat.find(f"{{{CAT_NS}}}{c}"))
           for c in ("selectionEntries", "entryLinks")):
        return
    shared = cat.find(f"{{{CAT_NS}}}sharedSelectionEntries")
    links = cat.find(f"{{{CAT_NS}}}entryLinks")
    if links is None:
        links = ET.SubElement(cat, f"{{{CAT_NS}}}entryLinks")
    added = []
    for e in (list(shared) if shared is not None else []):
        if e.get("type") in ("unit", "model"):
            ET.SubElement(links, f"{{{CAT_NS}}}entryLink", {
                "name": e.get("name"), "id": f"mh-root-{e.get('id')}", "hidden": "false",
                "targetId": e.get("id"), "type": "selectionEntry", "import": "true", "collective": "false"})
            added.append(e.get("name"))
    report["rootLinksAdded"] = added


def convert_3e(source, gst, report):
    """Convert every non-homebrew 3e catalogue in memory.

    Returns {catalogue_id: (source_path, tree, report_entry)}; copies needed 3e
    definitions into gst (modified in place). Nothing is written to disk.
    """
    source_gst = ET.parse(next(Path(source).glob("*.gst"))).getroot()
    if source_gst.get("id") != SOURCE_SYSTEM_ID:
        raise SystemExit("Unexpected 3e game system ID")
    report.setdefault("skippedHomebrew", [])
    trees = {}
    for path in sorted(Path(source).glob("*.cat")):
        tree = ET.parse(path)
        cat = tree.getroot()
        if cat.get("gameSystemId") != SOURCE_SYSTEM_ID:
            raise SystemExit(f"{path.name}: not a 3e catalogue")
        if is_homebrew_catalogue(cat.get("name")):
            report["skippedHomebrew"].append(cat.get("name"))
            continue
        entry = {"edition": 3, "source": path.name, "sourceName": cat.get("name"), "id": cat.get("id")}
        strip_homebrew(cat, entry)
        unlock_imperial_armour(cat, entry)
        dedupe_ids(cat, entry)
        expose_unlisted_units(cat, entry)
        entry["referencesRemapped"] = remap(cat)
        cat.set("gameSystemId", MH_SYSTEM_ID)
        trees[cat.get("id")] = (path, tree, entry)
    for cid in trees:
        if any(l.get("targetId") not in trees for l in trees[cid][1].getroot().iter(f"{{{CAT_NS}}}catalogueLink")):
            raise SystemExit(f"{trees[cid][0].name} links a skipped catalogue")
    report["gstReferencesRemapped"] = remap(gst)
    close_over_gst([t.getroot() for _, t, _ in trees.values()], source_gst, gst, report)
    ensure_force_links(gst, report)
    report["converted3e"] = [e for _, _, e in trees.values()]
    return trees


if __name__ == "__main__":
    raise SystemExit("Run tools/build_middlehammer.py, which builds every Middlehammer catalogue.")

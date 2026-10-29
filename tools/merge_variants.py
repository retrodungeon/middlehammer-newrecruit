#!/usr/bin/env python3
"""Fold 3rd Edition variant army lists into their parent codex catalogue.

Each parent gets a required "Army List" selection (Configuration) offering
"Codex" plus every variant. The parent's own army list is shown only while
"Codex" is chosen; each variant's army list only while that variant is chosen.
Conditions that asked "is the roster's primary catalogue X?" are rewritten to
ask "is option X chosen?", preserving their meaning.

Used by tools/convert_3e_catalogues.py; not a standalone script.
"""
import xml.etree.ElementTree as ET

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
CONFIGURATION = "525f-0a42-3f5c-5613"
MH_POINTS = "6f18-a8fc-2c5b-9517"

# Parent source name -> variant source names, in merge order (a variant that
# other variants import must come first).
VARIANTS = {
    "Space Marines (1999)": [
        "Salamanders (2000)", "White Scars (2002)", "Iron Hands (2001)",
        "Imperial Fists (2003)", "Relictors (White Dwarf 281)",
        "Cursed Foundings (Chapter Approved 2004)",
    ],
    "Blood Angels (1998)": ["Blood Angels Death Company (Chapter Approved 2001)"],
    "Space Wolves (2000)": ["Space Wolves 13th Company (2003)"],
    "Imperial Guard (1999)": [
        "Deathworld Veterans (2000)", "Catachan (2000)",
        "Armageddon Ork Hunters (Chapter Approved 2003)",
        "Tanith First and Only (Chapter Approved 2003)",
        "Cityfighting Imperial Guard (Chapter Approved 2003)",
        "Planetary Defence Regiment (Armageddon 2000)",
        "Steel Legion Mechanised Infantry (Armageddon 2000)",
        "Death Korps of Krieg (Chapter Approved 2003)",
        "Elysian Drop Troops (Chapter Approved 2003)",
        "Armoured Company (Chapter Approved 2001)",
        "Cadian Shock Troops (Eye of Terror 2003)",
        "Salvar Chem-Dogs (Chapter Approved 2003)",
    ],
    "Imperial Guard (2003)": [
        "Imperial Guard Armoured Company (Chapter Approved 2004)",
        "Armoured Battle Group (IA 2003)",
    ],
    "Eldar (2000)": [
        "Biel-Tan Swordwind Army (2000)", "Saim-Hann Wild Rider Host (2000)",
        "Rangers of Alaitoc (2000)", "Ulthwe The Damned (2000)",
        "Ulthwe Strike Force (Eye of Terror 2003)", "Iyanden Ghost Warriors (2000)",
    ],
    "Dark Eldar (2001)": ["Dark Eldar Wych Cult (2001)"],
    "Orks (1999)": ["Feral Orks (Chapter Approved 2004)", "Speed Freeks (Armageddon 2000)"],
    "Tyranids (2001)": ["Tyranid Seeding Swarm (Chapter Approved 2003)"],
}

SKIP_CONTAINERS = {"catalogueLinks", "selectionEntries", "entryLinks", "comment", "readme"}


def q(tag):
    return f"{{{CAT_NS}}}{tag}"


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def child(el, tag, index=None):
    found = el.find(q(tag))
    if found is None:
        found = ET.Element(q(tag))
        if index is None:
            el.append(found)
        else:
            el.insert(index, found)
    return found


def _unless(mods, field, value, option_id):
    m = ET.SubElement(mods, q("modifier"), {"type": "set", "field": field, "value": value})
    conds = ET.SubElement(m, q("conditions"))
    ET.SubElement(conds, q("condition"), {
        "type": "equalTo", "value": "0", "field": "selections", "scope": "force",
        "childId": option_id, "shared": "true", "includeChildSelections": "true",
        "includeChildForces": "false"})


def hide_unless(el, option_id, mod_id):
    """Append (last, so they win) modifiers that hide el and drop its minimums
    unless option_id is selected."""
    mods = child(el, "modifiers", 0)
    _unless(mods, "hidden", "true", option_id)
    cons = el.find(q("constraints"))
    for n, c in enumerate(list(cons) if cons is not None else []):
        if c.get("type") == "min":
            if not c.get("id"):
                c.set("id", f"{mod_id}-min{n}")
            _unless(mods, c.get("id"), "0", option_id)


def constraint(parent, kind, value, scope, cid):
    cons = child(parent, "constraints")
    ET.SubElement(cons, q("constraint"), {
        "type": kind, "value": str(value), "field": "selections", "scope": scope,
        "shared": "true", "id": cid, "includeChildSelections": "false",
        "includeChildForces": "false"})


def build_selector(parent, pid, options):
    """options: list of (option_id, name); first is the Codex default."""
    sel_id = f"mh-armylist-{pid}"
    entry = ET.Element(q("selectionEntry"), {
        "type": "upgrade", "import": "true", "name": "Army List", "hidden": "false",
        "id": sel_id, "collective": "false"})
    constraint(entry, "min", 1, "force", f"{sel_id}-min")
    constraint(entry, "max", 1, "force", f"{sel_id}-max")
    cl = child(entry, "categoryLinks")
    ET.SubElement(cl, q("categoryLink"), {
        "name": "Configuration", "hidden": "false", "id": f"{sel_id}-cat",
        "targetId": CONFIGURATION, "primary": "true"})
    groups = child(entry, "selectionEntryGroups")
    grp = ET.SubElement(groups, q("selectionEntryGroup"), {
        "name": "Army List", "hidden": "false", "id": f"{sel_id}-group",
        "collective": "false", "import": "true", "defaultSelectionEntryId": options[0][0]})
    constraint(grp, "min", 1, "parent", f"{sel_id}-group-min")
    constraint(grp, "max", 1, "parent", f"{sel_id}-group-max")
    entries = child(grp, "selectionEntries")
    for oid, name in options:
        opt = ET.SubElement(entries, q("selectionEntry"), {
            "type": "upgrade", "import": "true", "name": name, "hidden": "false",
            "id": oid, "collective": "false"})
        constraint(opt, "max", 1, "parent", f"{oid}-max")
        costs = child(opt, "costs")
        ET.SubElement(costs, q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    costs = child(entry, "costs")
    ET.SubElement(costs, q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    child(parent, "selectionEntries").insert(0, entry)


def rename_collisions(parent, var, report):
    pids = {e.get("id") for e in parent.iter() if e.get("id")}
    clash = {e.get("id") for e in var.iter() if e.get("id")} & pids
    clash.discard(var.get("id"))
    for old in clash:
        new = old + "-mv"
        for e in var.iter():
            for attr in ("id", "targetId", "childId", "scope", "field", "defaultSelectionEntryId"):
                if e.get(attr) == old:
                    e.set(attr, new)
    if clash:
        report.setdefault("idCollisionsRenamed", []).extend(sorted(clash))


def merge_one(parent, var, option_id, merged_ids, report):
    rename_collisions(parent, var, report)
    for cont in ("selectionEntries", "entryLinks"):
        src = var.find(q(cont))
        if src is None:
            continue
        dest = child(parent, cont)
        for i, el in enumerate(list(src)):
            hide_unless(el, option_id, f"{option_id}-{i}")
            dest.append(el)
    for container in list(var):
        tag = lname(container.tag)
        if tag in SKIP_CONTAINERS or not len(container):
            continue
        dest = child(parent, tag)
        for el in list(container):
            dest.append(el)
    links = child(parent, "catalogueLinks", 0)
    have = {l.get("targetId") for l in links}
    for l in var.iter(q("catalogueLink")):
        t = l.get("targetId")
        if t != parent.get("id") and t not in merged_ids and t not in have:
            links.append(l)
            have.add(t)
    if not len(links):
        parent.remove(links)


def merge_variants(trees, report):
    """trees: {catalogue_id: (path, tree, entry)} keyed as in convert_3e_catalogues.

    Returns the set of merged (removed) catalogue IDs.
    """
    by_source = {e["sourceName"]: cid for cid, (_, _, e) in trees.items()}
    option_for = {}   # catalogue id -> option id meaning "this army list is chosen"
    plan = []
    for pname, vnames in VARIANTS.items():
        pid = by_source[pname]
        codex_opt = f"mh-armylist-{pid}-codex"
        option_for[pid] = codex_opt
        opts = [(codex_opt, f"Codex: {pname}")]
        for v in vnames:
            vid = by_source[v]
            oid = f"mh-armylist-{pid}-{vid}"
            option_for[vid] = oid
            opts.append((oid, v))
        plan.append((pid, opts, [by_source[v] for v in vnames]))

    merged_ids = {vid for _, _, vids in plan for vid in vids}
    # Rewrite "primary catalogue is X" conditions everywhere before moving anything.
    rewritten = 0
    for cid, (_, tree, _) in trees.items():
        for e in tree.getroot().iter(q("condition")):
            target = e.get("childId")
            if target in option_for and e.get("scope") == "primary-catalogue":
                kind = e.get("type")
                if kind not in ("instanceOf", "notInstanceOf"):
                    raise ValueError(f"Unexpected primary-catalogue condition {e.attrib}")
                e.attrib.update({
                    "childId": option_for[target], "scope": "force", "field": "selections",
                    "type": "atLeast" if kind == "instanceOf" else "lessThan", "value": "1",
                    "shared": "true", "includeChildSelections": "true"})
                rewritten += 1
            elif target in merged_ids:
                raise ValueError(f"Unhandled reference to merged catalogue: {e.attrib}")
    for cid, (_, tree, _) in trees.items():
        if cid in merged_ids:
            continue
        for l in tree.getroot().iter(q("catalogueLink")):
            if l.get("targetId") in merged_ids:
                raise ValueError(f"{tree.getroot().get('name')} imports a variant list")
    report["primaryCatalogueConditionsRewritten"] = rewritten

    report["variantGroups"] = {}
    for pid, opts, vids in plan:
        parent = trees[pid][1].getroot()
        # Parent's own army list only while "Codex" is chosen.
        for cont in ("selectionEntries", "entryLinks"):
            r = parent.find(q(cont))
            for i, el in enumerate(list(r) if r is not None else []):
                hide_unless(el, opts[0][0], f"{opts[0][0]}-{i}")
        for (oid, _), vid in zip(opts[1:], vids):
            var = trees[vid][1].getroot()
            merge_one(parent, var, oid, merged_ids, trees[pid][2])
            trees[pid][2].setdefault("mergedVariants", []).append(trees[vid][2]["sourceName"])
        build_selector(parent, pid, opts)
        report["variantGroups"][trees[pid][2]["sourceName"]] = [n for _, n in opts[1:]]
    for vid in merged_ids:
        del trees[vid]
    return merged_ids

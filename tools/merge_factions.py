#!/usr/bin/env python3
"""Merge converted army lists into one catalogue per faction.

Each faction catalogue has a required "Army List" selection (Configuration)
whose options are every codex and variant list of that faction, from every
edition, labelled "<edition> – <list>". A member list's units are shown, and
its minimum requirements apply, only while its option is chosen.
Conditions that asked "is the roster's catalogue X?" are rewritten to ask
"is option X chosen?", and catalogue links are retargeted to faction catalogues.
"""
import re
import xml.etree.ElementTree as ET

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
CONFIGURATION = "525f-0a42-3f5c-5613"
MH_POINTS = "6f18-a8fc-2c5b-9517"
ED = {3: "3rd Ed", 4: "4th Ed", 5: "5th Ed", 6: "6th Ed", 7: "7th Ed"}


# Faction -> ordered members: (edition, source catalogue name, label prefix).
# Prefix "Codex: " marks a codex; a longer "Codex: ..." prefix is a full label override.
# Names are the most common across 3rd-7th Edition (maintainer decision 2026-10-29).
FACTIONS = {
    "Space Marines": [(3, "Space Marines (1999)", "Codex: ")] + [
        (3, n, "") for n in ("Salamanders (2000)", "White Scars (2002)", "Iron Hands (2001)",
                             "Imperial Fists (2003)", "Relictors (White Dwarf 281)",
                             "Cursed Foundings (Chapter Approved 2004)")],
    "Blood Angels": [(3, "Blood Angels (1998)", "Codex: "),
                     (3, "Blood Angels Death Company (Chapter Approved 2001)", "")],
    "Dark Angels": [(3, "Dark Angels (1999)", "Codex: ")],
    "Space Wolves": [(3, "Space Wolves (2000)", "Codex: "), (3, "Space Wolves 13th Company (2003)", "")],
    "Black Templars": [(3, "Black Templars (2000)", "Codex: ")],
    "Imperial Guard": [(3, "Imperial Guard (1999)", "Codex: ")] + [
        (3, n, "") for n in ("Deathworld Veterans (2000)", "Catachan (2000)",
                             "Armageddon Ork Hunters (Chapter Approved 2003)",
                             "Tanith First and Only (Chapter Approved 2003)",
                             "Cityfighting Imperial Guard (Chapter Approved 2003)",
                             "Planetary Defence Regiment (Armageddon 2000)",
                             "Steel Legion Mechanised Infantry (Armageddon 2000)",
                             "Death Korps of Krieg (Chapter Approved 2003)",
                             "Elysian Drop Troops (Chapter Approved 2003)",
                             "Armoured Company (Chapter Approved 2001)",
                             "Cadian Shock Troops (Eye of Terror 2003)",
                             "Salvar Chem-Dogs (Chapter Approved 2003)")] + [
        (3, "Imperial Guard (2003)", "Codex: "),
        (3, "Imperial Guard Armoured Company (Chapter Approved 2004)", ""),
        (3, "Armoured Battle Group (IA 2003)", ""),
        (5, "Imperial Guard", "Codex: Imperial Guard (2009)"),
    ],
    "Chaos Space Marines": [(3, "Chaos Space Marines (1999)", "Codex: "),
                            (3, "Chaos Space Marines (2002)", "Codex: ")],
    "Renegades & Heretics": [(3, "Lost and the Damned (Eye of Terror 2003)", "")],
    "Eldar": [(3, "Eldar (2000)", "Codex: ")] + [
        (3, n, "") for n in ("Biel-Tan Swordwind Army (2000)", "Saim-Hann Wild Rider Host (2000)",
                             "Rangers of Alaitoc (2000)", "Ulthwe The Damned (2000)",
                             "Ulthwe Strike Force (Eye of Terror 2003)", "Iyanden Ghost Warriors (2000)")],
    "Dark Eldar": [(3, "Dark Eldar (2001)", "Codex: "), (3, "Dark Eldar Wych Cult (2001)", "")],
    "Harlequins": [(3, "Harlequins (2000)", "")],
    "Orks": [(3, "Orks (1999)", "Codex: "), (3, "Feral Orks (Chapter Approved 2004)", ""),
             (3, "Speed Freeks (Armageddon 2000)", "")],
    "Tyranids": [(3, "Tyranids (2001)", "Codex: "), (3, "Tyranid Seeding Swarm (Chapter Approved 2003)", "")],
    "Genestealer Cults": [(3, "Genestealer Cults (Citadel Journal 40)", "")],
    "Necrons": [(3, "Necrons (2002)", "Codex: ")],
    "Tau Empire": [(3, "Tau (2001)", "Codex: ")],
    "Kroot Mercenaries": [(3, "Kroot Mercenaries (Chapter Approved 2004)", "")],
    "Sisters of Battle": [(3, "Witch Hunters (2003)", "Codex: "),
                          (3, "Sisters of Battle (Chapter Approved 2001)", "")],
    "Grey Knights": [(3, "Daemon Hunters (2003)", "Codex: ")],
    "Assassins": [(3, "Codex Assassins (1999)", "")],
    "Adeptus Arbites": [(3, "Adeptus Arbites (Citadel Journal 29)", "")],
}

SKIP_CONTAINERS = {"catalogueLinks", "selectionEntries", "entryLinks", "comment", "readme"}


def q(tag):
    return f"{{{CAT_NS}}}{tag}"


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def label(edition, src, prefix):
    if prefix.startswith("Codex: ") and len(prefix) > len("Codex: "):
        text = prefix                      # full override, e.g. 5e "Imperial Guard"
    else:
        text = prefix + src
    return f"{ED[edition]} – {text}"


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


def gate(el, option_id):
    """Appended last so they win: hide el and drop its minimums unless option_id is chosen."""
    mods = child(el, "modifiers", 0)
    _unless(mods, "hidden", "true", option_id)
    cons = el.find(q("constraints"))
    for n, c in enumerate(list(cons) if cons is not None else []):
        if c.get("type") == "min":
            if not c.get("id"):
                c.set("id", f"{option_id}-{el.get('id')}-min{n}")
            _unless(mods, c.get("id"), "0", option_id)


def constraint(parent, kind, value, scope, cid):
    ET.SubElement(child(parent, "constraints"), q("constraint"), {
        "type": kind, "value": str(value), "field": "selections", "scope": scope,
        "shared": "true", "id": cid, "includeChildSelections": "false", "includeChildForces": "false"})


def selector(fid, options):
    sid = f"{fid}-armylist"
    entry = ET.Element(q("selectionEntry"), {
        "type": "upgrade", "import": "true", "name": "Army List", "hidden": "false",
        "id": sid, "collective": "false", "sortIndex": "1"})
    constraint(entry, "min", 1, "force", f"{sid}-min")
    constraint(entry, "max", 1, "force", f"{sid}-max")
    ET.SubElement(child(entry, "categoryLinks"), q("categoryLink"), {
        "name": "Configuration", "hidden": "false", "id": f"{sid}-cat",
        "targetId": CONFIGURATION, "primary": "true"})
    grp = ET.SubElement(child(entry, "selectionEntryGroups"), q("selectionEntryGroup"), {
        "name": "Army List", "hidden": "false", "id": f"{sid}-group", "collective": "false",
        "import": "true", "defaultSelectionEntryId": options[0][0]})
    constraint(grp, "min", 1, "parent", f"{sid}-group-min")
    constraint(grp, "max", 1, "parent", f"{sid}-group-max")
    entries = child(grp, "selectionEntries")
    for oid, name in options:
        opt = ET.SubElement(entries, q("selectionEntry"), {
            "type": "upgrade", "import": "true", "name": name, "hidden": "false",
            "id": oid, "collective": "false"})
        constraint(opt, "max", 1, "parent", f"{oid}-max")
        ET.SubElement(child(opt, "costs"), q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    ET.SubElement(child(entry, "costs"), q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    return entry


def rename_collisions(seen_ids, member, report):
    clash = {e.get("id") for e in member.iter() if e.get("id")} & seen_ids
    clash.discard(member.get("id"))
    for old in clash:
        new = f"{old}-m{member.get('id')[:4]}"
        for e in member.iter():
            for attr in ("id", "targetId", "childId", "scope", "field", "defaultSelectionEntryId"):
                if e.get(attr) == old:
                    e.set(attr, new)
    if clash:
        report.setdefault("idCollisionsRenamed", {})[member.get("name")] = sorted(clash)


def build_factions(members, game_system_id, report):
    """members: {(edition, source name): catalogue root}. Returns {faction name: root}."""
    assigned = {(e, s) for fm in FACTIONS.values() for e, s, _ in fm}
    missing = sorted(set(members) - assigned)
    if missing:
        raise SystemExit(f"Converted lists not assigned to a faction: {missing}")
    absent = sorted(assigned - set(members))
    if absent:
        raise SystemExit(f"Faction table names lists that were not converted: {absent}")

    option_for, faction_of = {}, {}
    for fname, fm in FACTIONS.items():
        fid = f"mh-fac-{slug(fname)}"
        for e, s, _ in fm:
            cid = members[(e, s)].get("id")
            option_for[cid] = f"mh-al-{cid}"
            faction_of[cid] = fid

    # 1. Rewrite catalogue-identity references in every member before moving anything.
    rewritten = 0
    for root in members.values():
        for el in root.iter():
            if lname(el.tag) == "condition" and el.get("childId") in option_for:
                if el.get("scope") not in ("primary-catalogue", "force") or el.get("type") not in ("instanceOf", "notInstanceOf"):
                    raise ValueError(f"Unhandled catalogue reference in {root.get('name')}: {el.attrib}")
                kind = el.get("type")
                el.attrib.update({
                    "childId": option_for[el.get("childId")], "scope": "force", "field": "selections",
                    "type": "atLeast" if kind == "instanceOf" else "lessThan", "value": "1",
                    "shared": "true", "includeChildSelections": "true"})
                rewritten += 1
    report["catalogueConditionsRewritten"] = rewritten

    # 2. Merge.
    out = {}
    for fname, fm in FACTIONS.items():
        fid = f"mh-fac-{slug(fname)}"
        root = ET.Element(q("catalogue"), {
            "name": fname, "id": fid, "revision": "1", "battleScribeVersion": "2.03",
            "gameSystemId": game_system_id, "library": "false", "type": "catalogue",
            "authorName": "Middlehammer (generated)"})
        comment = ET.SubElement(root, q("comment"))
        comment.text = "Generated by tools/build_middlehammer.py from: " + "; ".join(
            f"{ED[e]} {s}" for e, s, _ in fm)
        links = ET.SubElement(root, q("catalogueLinks"))
        seen = {fid}
        options = []
        for e, s, prefix in fm:
            m = members[(e, s)]
            mid = m.get("id")
            rename_collisions(seen, m, report)
            oid = option_for[mid]
            options.append((oid, label(e, s, prefix)))
            for cont in ("selectionEntries", "entryLinks"):
                src = m.find(q(cont))
                for el in (list(src) if src is not None else []):
                    gate(el, oid)
                    child(root, cont).append(el)
            for container in list(m):
                tag = lname(container.tag)
                if tag in SKIP_CONTAINERS or not len(container):
                    continue
                dest = child(root, tag)
                for el in list(container):
                    dest.append(el)
            for l in m.iter(q("catalogueLink")):
                target = faction_of.get(l.get("targetId"))
                if target is None:
                    raise ValueError(f"{m.get('name')} links unknown catalogue {l.get('name')}")
                if target != fid and target not in {x.get("targetId") for x in links}:
                    ET.SubElement(links, q("catalogueLink"), {
                        "name": next(n for n, f in ((n, f"mh-fac-{slug(n)}") for n in FACTIONS) if f == target),
                        "id": f"{fid}-link-{target}", "targetId": target, "type": "catalogue",
                        "importRootEntries": "false"})
            seen |= {x.get("id") for x in m.iter() if x.get("id")}
        child(root, "selectionEntries").insert(0, selector(fid, options))
        if not len(links):
            root.remove(links)
        out[fname] = root
        report.setdefault("factions", {})[fname] = [n for _, n in options]
    return out

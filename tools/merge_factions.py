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


# Faction -> ordered members: (source edition, source catalogue name, label[, book edition]).
# Label "Codex: " marks a codex (label = "Codex: <source name>"); a longer label is used
# verbatim. Book edition (for the "4th Ed" prefix) defaults to the source edition: the
# 5th Edition source includes 4th Edition codexes that were still current in 5th.
# Names are the most common across 3rd-7th Edition (maintainer decision 2026-10-29).
FACTIONS = {
    "Space Marines": [(3, "Space Marines (1999)", "Codex: ")] + [
        (3, n, "") for n in ("Salamanders (2000)", "White Scars (2002)", "Iron Hands (2001)",
                             "Imperial Fists (2003)", "Relictors (White Dwarf 281)",
                             "Cursed Foundings (Chapter Approved 2004)")] + [
        (5, "Space Marines", "Codex: Space Marines (2008)"),
        (7, "Space Marines - Codex (2015)", "Codex: Space Marines (2015)"),
        (7, "Space Marines - FW - Siege Assault Vanguard", "Forge World: Siege Assault Vanguard"),
        (7, "Tyrant's Legion - FW - Defenders of Badab", "Forge World: Tyrant's Legion (Defenders of Badab)"),
        (7, "Legion of the Damned - Codex", "Legion of the Damned")],
    "Blood Angels": [(3, "Blood Angels (1998)", "Codex: "),
                     (3, "Blood Angels Death Company (Chapter Approved 2001)", ""),
                     (5, "Blood Angels", "Codex: Blood Angels (2010)"),
                     (7, "Blood Angels - Codex (2014)", "Codex: Blood Angels (2014)")],
    "Dark Angels": [(3, "Dark Angels (1999)", "Codex: "),
                    (5, "Dark Angels", "Codex: Dark Angels (2007)", 4),
                    (7, "Dark Angels - Codex (2015)", "Codex: Dark Angels (2015)"),
                    (7, "Fallen Angels - Supplement", "Fallen Angels (supplement)")],
    "Space Wolves": [(3, "Space Wolves (2000)", "Codex: "), (3, "Space Wolves 13th Company (2003)", ""),
                     (5, "Space Wolves", "Codex: Space Wolves (2009)"),
                     (7, "Space Wolves - Codex", "Codex: Space Wolves (2014)")],
    "Deathwatch": [(7, "Deathwatch - Codex", "Codex: Deathwatch (2016)")],
    "Black Templars": [(3, "Black Templars (2000)", "Codex: "),
                       (5, "Black Templars", "Codex: Black Templars (2005)", 4)],
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
        (7, "Astra Militarum - Codex", "Codex: Astra Militarum (2014)", 6),
        (7, "Militarum Tempestus - Codex", "Codex: Militarum Tempestus (2014)", 6),
        (7, "Astra Militarum - FW - Armoured Battle Group", "Forge World: Armoured Battle Group"),
        (7, "Astra Militarum - FW - Death Korps of Krieg Assault Brigade", "Forge World: Death Korps of Krieg Assault Brigade"),
        (7, "Astra Militarum - FW - Death Korps of Krieg Siege Regiment", "Forge World: Death Korps of Krieg Siege Regiment"),
        (7, "Astra Militarum - FW - Elysian", "Forge World: Elysian Drop Troops"),
        (7, "Astra Militarum - FW - Elysian Detachment D-99", "Forge World: Elysian Detachment D-99"),
        (7, "Adeptus Astra Telepathica", "Adeptus Astra Telepathica"),
        (7, "Aeronautica Imperialis", "Aeronautica Imperialis"),
    ],
    "Chaos Space Marines": [(3, "Chaos Space Marines (1999)", "Codex: "),
                            (3, "Chaos Space Marines (2002)", "Codex: "),
                            (5, "Chaos Space Marines", "Codex: Chaos Space Marines (2007)", 4),
                            (7, "Chaos Space Marines - Codex", "Codex: Chaos Space Marines (2015)"),
                            (7, "Chaos Khorne Daemonkin", "Codex: Khorne Daemonkin (2015)")],
    "Chaos Daemons": [(5, "Chaos Daemons", "Codex: Chaos Daemons (2008)", 4),
                      (7, "Chaos Daemons (40K) - Codex", "Codex: Chaos Daemons (2015)")],
    "Renegades & Heretics": [(3, "Lost and the Damned (Eye of Terror 2003)", ""),
                             (7, "Renegades & Heretics", "Forge World: Renegades & Heretics")],
    "Eldar": [(3, "Eldar (2000)", "Codex: ")] + [
        (3, n, "") for n in ("Biel-Tan Swordwind Army (2000)", "Saim-Hann Wild Rider Host (2000)",
                             "Rangers of Alaitoc (2000)", "Ulthwe The Damned (2000)",
                             "Ulthwe Strike Force (Eye of Terror 2003)", "Iyanden Ghost Warriors (2000)")] + [
        (5, "Eldar", "Codex: Eldar (2006)", 4),
        (7, "Eldar Craftworlds - Codex (2015)", "Codex: Craftworlds (2015)"),
        (7, "Eldar - Corsairs (2015)", "Forge World: Eldar Corsairs")],
    "Ynnari": [(7, "Ynnari Aeldari - Supplement", "Ynnari (Gathering Storm: Fracture of Biel-Tan)")],
    "Dark Eldar": [(3, "Dark Eldar (2001)", "Codex: "), (3, "Dark Eldar Wych Cult (2001)", ""),
                   (5, "Dark Eldar", "Codex: Dark Eldar (2010)"),
                   (7, "Dark_Eldar_Codex_(2014)", "Codex: Dark Eldar (2014)"),
                   (7, "Dark Eldar - Supplement - Haemonculus Covens", "Haemonculus Covens (supplement)")],
    "Harlequins": [(3, "Harlequins (2000)", ""), (7, "Harlequins - Codex", "Codex: Harlequins (2015)")],
    "Orks": [(3, "Orks (1999)", "Codex: "), (3, "Feral Orks (Chapter Approved 2004)", ""),
             (3, "Speed Freeks (Armageddon 2000)", ""),
             (5, "Orks", "Codex: Orks (2008)", 4),
             (7, "Orks - Codex", "Codex: Orks (2014)")],
    "Tyranids": [(3, "Tyranids (2001)", "Codex: "), (3, "Tyranid Seeding Swarm (Chapter Approved 2003)", ""),
                 (5, "Tyranids", "Codex: Tyranids (2010)"),
                 (7, "Tyranids - Codex", "Codex: Tyranids (2014)", 6)],
    "Genestealer Cults": [(3, "Genestealer Cults (Citadel Journal 40)", ""),
                          (7, "Genestealer Cults - Codex", "Codex: Genestealer Cults (2016)")],
    "Necrons": [(3, "Necrons (2002)", "Codex: "), (5, "Necrons", "Codex: Necrons (2011)"),
                (7, "Necrons - Codex (2015)", "Codex: Necrons (2015)"),
                (7, "Necrons - FW - Dark Harvest", "Forge World: Dark Harvest")],
    "Tau Empire": [(3, "Tau (2001)", "Codex: "), (5, "Tau Empire", "Codex: Tau Empire (2005)", 4),
                   (7, "Tau - Codex (2015)", "Codex: Tau Empire (2015)")],
    "Kroot Mercenaries": [(3, "Kroot Mercenaries (Chapter Approved 2004)", "")],
    "Sisters of Battle": [(3, "Witch Hunters (2003)", "Codex: "),
                          (3, "Sisters of Battle (Chapter Approved 2001)", ""),
                          (5, "Sisters of Battle", "Codex: Sisters of Battle (White Dwarf 2011)"),
                          (7, "Adepta Sororitas", "Codex: Adepta Sororitas")],
    "Grey Knights": [(3, "Daemon Hunters (2003)", "Codex: "),
                     (5, "Grey Knights", "Codex: Grey Knights (2011)"),
                     (7, "Grey Knights - Codex (2014)", "Codex: Grey Knights (2014)")],
    "Adeptus Mechanicus": [(7, "Skitarii - Codex", "Codex: Skitarii (2015)"),
                           (7, "Cult Mechanicus Codex 2015", "Codex: Cult Mechanicus (2015)")],
    "Adeptus Custodes": [(7, "Adeptus Custodes Dataslate", "Adeptus Custodes (dataslate)"),
                         (7, "Sisters of Silence Dataslate", "Sisters of Silence (dataslate)")],
    "Imperial Knights": [(7, "Imperial Knights - Codex (2015)", "Codex: Imperial Knights (2015)"),
                         (7, "Chaos Renegade Knights", "Renegade Knights")],
    "Inquisition": [(7, "Inquisition - Codex", "Inquisition (Codex: Inquisition, Imperial Agents)")],
    "Assassins": [(3, "Codex Assassins (1999)", ""), (7, "Assassins Codex", "Officio Assassinorum")],
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
    if (prefix.startswith("Codex: ") and len(prefix) > len("Codex: ")) or (prefix and not prefix.endswith(": ")):
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


def restrict_to_owner(entry, own_forces):
    """In a force type that belongs to one army list (e.g. 'Psykana Division', 'Daemon Hunter
    Allies'), only that list can be chosen: hide every other Army List option there."""
    owner_of = {f: oid for oid, forces in own_forces.items() for f in forces}
    for opt in entry.find(q("selectionEntryGroups")).iter(q("selectionEntry")):
        others = [f for f, oid in owner_of.items() if oid != opt.get("id")]
        if not others:
            continue
        m = ET.SubElement(child(opt, "modifiers", 0), q("modifier"), {"type": "set", "field": "hidden", "value": "true"})
        conds = ET.SubElement(ET.SubElement(ET.SubElement(m, q("conditionGroups")), q("conditionGroup"),
                                            {"type": "or"}), q("conditions"))
        for f in others:
            ET.SubElement(conds, q("condition"), {
                "type": "instanceOf", "value": "1", "field": "selections", "scope": "force", "childId": f,
                "shared": "true", "includeChildSelections": "false", "includeChildForces": "false"})


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


def drop_empty_condition_groups(root):
    """Some source rules contain condition groups with no conditions left in them (the author
    deleted the conditions). New Recruit treats such a group as satisfied, which e.g. hid the
    7th Edition Chaos 'Force Options'. An empty 'or' group means 'none of these': the rule
    never applies. An empty 'and' group adds no requirement and is removed."""
    def has_condition(g):
        return any(lname(x.tag) == "condition" for x in g.iter())
    par = {c: p for p in root.iter() for c in p}
    fixed = 0
    for mod in [m for m in root.iter() if lname(m.tag) in ("modifier", "repeat")]:
        never = False
        for g in [g for g in mod.iter() if lname(g.tag) == "conditionGroup" and not has_condition(g)]:
            if g.get("type") == "or" and par[par[g]] is mod:
                never = True
            if g in par:
                par[g].remove(g)
            fixed += 1
        if never and mod in par:
            par[mod].remove(mod)
    return fixed


def build_factions(members, game_system_id, report):
    """members: {(edition, source name): catalogue root}. Returns {faction name: root}."""
    assigned = {(m[0], m[1]) for fm in FACTIONS.values() for m in fm}
    missing = sorted(set(members) - assigned)
    if missing:
        raise SystemExit(f"Converted lists not assigned to a faction: {missing}")
    absent = sorted(assigned - set(members))
    if absent:
        raise SystemExit(f"Faction table names lists that were not converted: {absent}")

    option_for, faction_of = {}, {}
    for fname, fm in FACTIONS.items():
        fid = f"mh-fac-{slug(fname)}"
        for m in fm:
            cid = members[(m[0], m[1])].get("id")
            option_for[cid] = f"mh-al-{cid}"
            faction_of[cid] = fid

    report["emptyConditionGroupsFixed"] = sum(drop_empty_condition_groups(r) for r in members.values())

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
            f"{ED[m[0]]} source: {m[1]}" for m in fm)
        links = ET.SubElement(root, q("catalogueLinks"))
        seen = {fid}
        options, own_forces = [], {}
        for spec in fm:
            e, s, prefix = spec[:3]
            book_edition = spec[3] if len(spec) > 3 else e
            m = members[(e, s)]
            mid = m.get("id")
            rename_collisions(seen, m, report)
            oid = option_for[mid]
            options.append((oid, label(book_edition, s, prefix)))
            own_forces[oid] = [f.get("id") for f in m.iter(q("forceEntry"))]
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
        sel = selector(fid, options)
        restrict_to_owner(sel, {o: f for o, f in own_forces.items() if f})
        child(root, "selectionEntries").insert(0, sel)
        if not len(links):
            root.remove(links)
        out[fname] = root
        report.setdefault("factions", {})[fname] = [n for _, n in options]
    return out

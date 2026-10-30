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
    "Space Marines": [(3, "Space Marines (1999)", "Codex: Space Marines (1998)")] + [
        (3, n, "") for n in ("Salamanders (2000)", "White Scars (2002)", "Iron Hands (2001)",
                             "Imperial Fists (2003)", "Relictors (White Dwarf 281)",
                             "Cursed Foundings (Chapter Approved 2004)")] + [
        (4, "Space Marines (4E)", "Codex: Space Marines (2004)"),
        (5, "Space Marines", "Codex: Space Marines (2008)"),
        (6, "Space Marines - Codex", "Codex: Space Marines (2013)"),
        (6, "Space Marines - Supplement - Clan Raukaan", "Clan Raukaan (supplement, 2013)"),
        (6, "Space Marines - Supplement - Sentinels of Terra", "Sentinels of Terra (supplement, 2013)"),
        (6, "Space Marines - FW - Siege Assault Vanguard", "Forge World: Siege Assault Vanguard (IA10, 6th Ed update)"),
        (7, "Tyrant's Legion - FW - Defenders of Badab", "Forge World: Tyrant's Legion (IA9 update PDF, 2013)", 6),
        (7, "Legion of the Damned - Codex", "Codex: Legion of the Damned (2014)", 6),
        (7, "Space Marines - Codex (2015)", "Codex: Space Marines (2015)"),
        (7, "Space Marines - FW - Siege Assault Vanguard", "Forge World: Siege Assault Vanguard (IA10, with Codex: Space Marines 2015)")],
    "Blood Angels": [(3, "Blood Angels (1998)", "Codex: "),
                     (3, "Blood Angels Death Company (Chapter Approved 2001)", ""),
                     (4, "Blood Angels (4E)", "Codex: Blood Angels (White Dwarf 2007)"),
                     (5, "Blood Angels", "Codex: Blood Angels (2010)"),
                     (7, "Blood Angels - Codex (2014)", "Codex: Blood Angels (2014)")],
    "Dark Angels": [(3, "Dark Angels (1999)", "Codex: "),
                    (5, "Dark Angels", "Codex: Dark Angels (2007)", 4),
                    (6, "Dark Angels - Codex", "Codex: Dark Angels (2013)"),
                    (7, "Dark Angels - Codex (2015)", "Codex: Dark Angels (2015)")],
    "Space Wolves": [(3, "Space Wolves (2000)", "Codex: "), (3, "Space Wolves 13th Company (2003)", ""),
                     (5, "Space Wolves", "Codex: Space Wolves (2009)"),
                     (7, "Space Wolves - Codex", "Codex: Space Wolves (2014)")],
    "Deathwatch": [(7, "Deathwatch - Codex", "Codex: Deathwatch (2016)")],
    "Black Templars": [(3, "Black Templars (2000)", "Black Templars (Codex: Armageddon, 2000)"),
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
        (7, "Astra Militarum - FW - Armoured Battle Group", "Forge World: Armoured Battle Group (IA1 2nd Ed, 2012)", 6),
        (7, "Astra Militarum - FW - Elysian", "Forge World: Elysian Drop Troops (IA3 2nd Ed, 2013)", 6),
        (7, "Astra Militarum - FW - Death Korps of Krieg Assault Brigade", "Forge World: Death Korps of Krieg Assault Brigade (IA12, 2013)", 6),
        (7, "Astra Militarum - FW - Elysian Detachment D-99", "Forge World: Elysian Detachment D-99 (IA4 2nd Ed, 2014)"),
        (7, "Astra Militarum - FW - Death Korps of Krieg Siege Regiment", "Forge World: Death Korps of Krieg Siege Regiment (Siege of Vraks, 2015)"),
        (7, "Adeptus Astra Telepathica", "Astra Telepathica (Codex: Imperial Agents, 2016)"),
        (7, "Aeronautica Imperialis", "Aeronautica Imperialis (Codex: Imperial Agents, 2016)"),
    ],
    "Chaos Space Marines": [(3, "Chaos Space Marines (1999)", "Codex: "),
                            (3, "Chaos Space Marines (2002)", "Codex: "),
                            (5, "Chaos Space Marines", "Codex: Chaos Space Marines (2007)", 4),
                            (7, "Chaos Space Marines - Codex", "Codex: Chaos Space Marines (2012)", 6),
                            (6, "Chaos Space Marines - Supplement - Black Legion", "Black Legion (supplement, 2013)"),
                            (6, "Chaos Space Marines - Supplement - Crimson Slaughter", "Crimson Slaughter (supplement, 2014)"),
                            (7, "Chaos Khorne Daemonkin", "Codex: Khorne Daemonkin (2015)")],
    "Chaos Daemons": [(5, "Chaos Daemons", "Codex: Chaos Daemons (2008)", 4),
                      (6, "Chaos Daemons (40K) - Codex", "Codex: Chaos Daemons (2013)"),
                      (7, "Chaos Daemons (40K) - Codex", "Codex: Chaos Daemons – Daemonic Incursion Edition (2016)")],
    "Renegades & Heretics": [(3, "Lost and the Damned (Eye of Terror 2003)", ""),
                             (7, "Renegades & Heretics", "Forge World: Renegades & Heretics (IA13, 2014; Siege of Vraks, 2015)")],
    "Eldar": [(3, "Eldar (2000)", "Codex: ")] + [
        (3, n, "") for n in ("Biel-Tan Swordwind Army (2000)", "Saim-Hann Wild Rider Host (2000)",
                             "Rangers of Alaitoc (2000)", "Ulthwe The Damned (2000)",
                             "Ulthwe Strike Force (Eye of Terror 2003)", "Iyanden Ghost Warriors (2000)")] + [
        (5, "Eldar", "Codex: Eldar (2006)", 4),
        (6, "Eldar - Codex", "Codex: Eldar (2013)"),
        (6, "Eldar - Supplement - Iyanden", "Iyanden (supplement, 2013)"),
        (7, "Eldar Craftworlds - Codex (2015)", "Codex: Craftworlds (2015)"),
        (7, "Eldar - Corsairs (2015)", "Forge World: Eldar Corsairs (Doom of Mymeara, 2015)")],
    "Ynnari": [(7, "Ynnari Aeldari - Supplement", "Ynnari (Gathering Storm: Fracture of Biel-Tan)")],
    "Dark Eldar": [(3, "Dark Eldar (2001)", "Codex: "), (3, "Dark Eldar Wych Cult (2001)", ""),
                   (5, "Dark Eldar", "Codex: Dark Eldar (2010)"),
                   (7, "Dark_Eldar_Codex_(2014)", "Codex: Dark Eldar (2014)"),
                   (7, "Dark Eldar - Supplement - Haemonculus Covens", "Haemonculus Covens (supplement, 2014)")],
    "Harlequins": [(3, "Harlequins (2000)", ""), (7, "Harlequins - Codex", "Codex: Harlequins (2015)")],
    "Orks": [(3, "Orks (1999)", "Codex: "), (3, "Feral Orks (Chapter Approved 2004)", ""),
             (3, "Speed Freeks (Armageddon 2000)", ""),
             (5, "Orks", "Codex: Orks (2008)", 4),
             (6, "Orks - FW - Dread Mob", "Forge World: Dread Mob (IA8, 2013)"),
             (7, "Orks - Codex", "Codex: Orks (2014)")],
    "Tyranids": [(3, "Tyranids (2001)", "Codex: "), (3, "Tyranid Seeding Swarm (Chapter Approved 2003)", ""),
                 (4, "Tyranids (4E)", "Codex: Tyranids (2005)"),
                 (5, "Tyranids", "Codex: Tyranids (2010)"),
                 (7, "Tyranids - Codex", "Codex: Tyranids (2014)", 6)],
    "Genestealer Cults": [(3, "Genestealer Cults (Citadel Journal 40)", ""),
                          (7, "Genestealer Cults - Codex", "Codex: Genestealer Cults (2016)")],
    "Necrons": [(3, "Necrons (2002)", "Codex: "), (5, "Necrons", "Codex: Necrons (2011)"),
                (7, "Necrons - FW - Dark Harvest", "Forge World: Dark Harvest (IA12, 2013)", 6),
                (7, "Necrons - Codex (2015)", "Codex: Necrons (2015)")],
    "Tau Empire": [(3, "Tau (2001)", "Codex: "), (5, "Tau Empire", "Codex: Tau Empire (2006)", 4),
                   (6, "Tau - Codex", "Codex: Tau Empire (2013)"),
                   (6, "Tau - Supplement - Farsight Enclaves", "Farsight Enclaves (supplement, 2013)"),
                   (7, "Tau - Codex (2015)", "Codex: Tau Empire (2015)")],
    "Kroot Mercenaries": [(3, "Kroot Mercenaries (Chapter Approved 2004)", "")],
    "Sisters of Battle": [(3, "Witch Hunters (2003)", "Codex: Witch Hunters (2004)"),
                          (3, "Sisters of Battle (Chapter Approved 2001)", ""),
                          (5, "Sisters of Battle", "Codex: Sisters of Battle (White Dwarf 2011)"),
                          (7, "Adepta Sororitas", "Codex: Adepta Sororitas (2013)", 6)],
    "Grey Knights": [(3, "Daemon Hunters (2003)", "Codex: "),
                     (5, "Grey Knights", "Codex: Grey Knights (2011)"),
                     (7, "Grey Knights - Codex (2014)", "Codex: Grey Knights (2014)")],
    "Adeptus Mechanicus": [(7, "Skitarii - Codex", "Codex: Skitarii (2015)"),
                           (7, "Cult Mechanicus Codex 2015", "Codex: Cult Mechanicus (2015)")],
    "Adeptus Custodes": [(7, "Adeptus Custodes Dataslate", "Codex: Adeptus Custodes (2017)"),
                         (7, "Sisters of Silence Dataslate", "Codex: Sisters of Silence (2017)")],
    "Imperial Knights": [(7, "Imperial Knights - Codex (2015)", "Codex: Imperial Knights (2015)"),
                         (7, "Chaos Renegade Knights", "Renegade Knights (Imperial Knights: Renegade, 2016)")],
    # Assassins merged into Inquisition (decision 2026-10-29).
    "Inquisition": [(3, "Codex Assassins (1999)", "Codex Assassins (White Dwarf 235, 1999)"),
                    (7, "Inquisition - Codex", "Codex: Inquisition (2013)", 6),
                    (7, "Inquisition - Imperial Agents", "Inquisition (Codex: Imperial Agents, 2016)"),
                    (7, "Assassins Codex", "Officio Assassinorum")],
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


def detach_from_new_force(el, report):
    """New Recruit adds a root entry with a default amount to every new force before it
    applies our Army List hide rules, and sorts by sortIndex. So: no root entry adds itself
    (the 4th Edition Chapter Traits did, in every Space Marines list), and every list's own
    sort order comes after the Army List entry (sortIndex 1)."""
    if el.attrib.pop("defaultAmount", None) is not None:
        report.setdefault("rootDefaultAmountsRemoved", []).append(el.get("name"))
    for c in el.findall(f"{q('constraints')}/{q('constraint')}"):
        c.attrib.pop("automatic", None)
    if el.get("sortIndex") is not None:
        el.set("sortIndex", str(int(el.get("sortIndex")) + 2))


def ensure_configuration_first(fe, report):
    """Every force needs the Configuration section, first, to hold the Army List choice.
    Some 3rd Edition ally force types (e.g. Assassin Attachment) lack it, so no list, and
    therefore no unit, could be chosen in them."""
    links = child(fe, "categoryLinks", 0)
    config = [l for l in links if l.get("targetId") == CONFIGURATION]
    if config:
        links.remove(config[0])
        links.insert(0, config[0])
        return
    links.insert(0, ET.Element(q("categoryLink"), {"name": "Configuration", "hidden": "false",
                                                   "id": f"{fe.get('id')}-configuration",
                                                   "targetId": CONFIGURATION}))
    report.setdefault("configurationAddedToForces", []).append(fe.get("name"))


def constraint(parent, kind, value, scope, cid):
    ET.SubElement(child(parent, "constraints"), q("constraint"), {
        "type": kind, "value": str(value), "field": "selections", "scope": scope,
        "shared": "true", "id": cid, "includeChildSelections": "false", "includeChildForces": "false"})


# Lists that cannot fill the standard chart (no HQ or no Troops choice) and are fielded only
# through their own force types (ally attachments or codex detachments). Their Army List
# option is hidden in the standard force (decision 2026-10-29).
NOT_ON_STANDARD_CHART = {
    (3, "Codex Assassins (1999)"), (3, "Harlequins (2000)"),
    (7, "Assassins Codex"), (7, "Inquisition - Codex"), (7, "Inquisition - Imperial Agents"), (7, "Sisters of Silence Dataslate"),
    (7, "Legion of the Damned - Codex"), (7, "Imperial Knights - Codex (2015)"), (7, "Chaos Renegade Knights"),
    (7, "Adeptus Astra Telepathica"), (7, "Aeronautica Imperialis"),
    (7, "Dark Eldar - Supplement - Haemonculus Covens"),
}
STANDARD_FORCE = "mh-test-force"

# Allies only within the same era (Unification p. 8): 3rd-5th Edition codexes ally with each
# other, 6th-7th with each other. Every Army List option carries its era as a category; an
# ally force type is an error unless the roster contains another list of its own era.
ERA_CATEGORIES = {"3rd-5th": ("mh-era-3-5", "Era: 3rd-5th Edition"),
                  "6th-7th": ("mh-era-6-7", "Era: 6th-7th Edition")}
ALLY_FORCES = {"Adeptus Arbites Allies", "Assassin Attachment", "Daemon Hunter Allies",
               "Harlequin Allies", "Kroot Auxiliaries", "Witch Hunter Allies"}


def era(book_edition):
    return "3rd-5th" if book_edition <= 5 else "6th-7th"


def ensure_era_categories(gst):
    gns = "http://www.battlescribe.net/schema/gameSystemSchema"
    cats = gst.find(f"{{{gns}}}categoryEntries")
    have = {c.get("id") for c in cats}
    for cid, name in ERA_CATEGORIES.values():
        if cid not in have:
            ET.SubElement(cats, f"{{{gns}}}categoryEntry", {"name": name, "id": cid, "hidden": "false"})


def restrict_allies_to_era(entry, ally_forces, option_era):
    """ally_forces: {force id: owning option id}. An ally force must join an army of its own
    era: selecting its list breaks the option's max constraint unless the roster holds
    another list of the same era (the ally's own Army List counts once). Lists of other eras
    may also be present: the author allows any mix of detachments in multi-detachment games
    (2026-10-29)."""
    for opt in entry.find(q("selectionEntryGroups")).iter(q("selectionEntry")):
        for fid, oid in ally_forces.items():
            if oid != opt.get("id"):
                continue
            same = ERA_CATEGORIES[option_era[oid]][0]
            m = ET.SubElement(child(opt, "modifiers", 0), q("modifier"),
                              {"type": "set", "field": f"{oid}-max", "value": "0"})
            conds = ET.SubElement(m, q("conditions"))
            ET.SubElement(conds, q("condition"), {
                "type": "instanceOf", "value": "1", "field": "selections", "scope": "force", "childId": fid,
                "shared": "true", "includeChildSelections": "false", "includeChildForces": "false"})
            ET.SubElement(conds, q("condition"), {
                "type": "lessThan", "value": "2", "field": "selections", "scope": "roster", "childId": same,
                "shared": "true", "includeChildSelections": "true", "includeChildForces": "true"})


def restrict_to_owner(entry, own_forces):
    """In a force type that belongs to one army list (e.g. 'Psykana Division', 'Daemon Hunter
    Allies'), only that list can be chosen: hide every other Army List option there."""
    owner_of = {f: oid for oid, forces in own_forces.items() if oid is not None for f in forces}
    for opt in entry.find(q("selectionEntryGroups")).iter(q("selectionEntry")):
        others = [f for f, oid in owner_of.items() if oid != opt.get("id")]
        if opt.get("id") in own_forces.get(None, ()):
            others.append(STANDARD_FORCE)
        if not others:
            continue
        m = ET.SubElement(child(opt, "modifiers", 0), q("modifier"), {"type": "set", "field": "hidden", "value": "true"})
        conds = ET.SubElement(ET.SubElement(ET.SubElement(m, q("conditionGroups")), q("conditionGroup"),
                                            {"type": "or"}), q("conditions"))
        for f in others:
            ET.SubElement(conds, q("condition"), {
                "type": "instanceOf", "value": "1", "field": "selections", "scope": "force", "childId": f,
                "shared": "true", "includeChildSelections": "false", "includeChildForces": "false"})


def selector(fid, options, default=None):
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
        "import": "true", "defaultSelectionEntryId": default or options[0][0]})
    constraint(grp, "min", 1, "parent", f"{sid}-group-min")
    constraint(grp, "max", 1, "parent", f"{sid}-group-max")
    entries = child(grp, "selectionEntries")
    for oid, name, option_era in options:
        opt = ET.SubElement(entries, q("selectionEntry"), {
            "type": "upgrade", "import": "true", "name": name, "hidden": "false",
            "id": oid, "collective": "false"})
        cid, cname = ERA_CATEGORIES[option_era]
        ET.SubElement(child(opt, "categoryLinks"), q("categoryLink"), {
            "name": cname, "hidden": "false", "id": f"{oid}-era", "targetId": cid, "primary": "false"})
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


# Unification p. 8: "6th and 7th edition Imperium or Chaos codices specifically are allowed to
# take an Imperial Knight or Renegade Knight as their Lord of War choice."
KNIGHT_LOW_CATEGORY = ("mh-knight-low", "Knight Lord of War")
KNIGHTS_FOR = {
    "Imperial": ["Space Marines", "Blood Angels", "Dark Angels", "Space Wolves", "Deathwatch", "Imperial Guard",
                 "Grey Knights", "Sisters of Battle", "Adeptus Mechanicus", "Adeptus Custodes"],
    "Chaos": ["Chaos Space Marines", "Chaos Daemons", "Renegades & Heretics"],
}
RENEGADE = {"Renegade Knight"}


def ensure_knight_category(gst):
    gns = "http://www.battlescribe.net/schema/gameSystemSchema"
    cid, name = KNIGHT_LOW_CATEGORY
    cats = gst.find(f"{{{gns}}}categoryEntries")
    if cid not in {c.get("id") for c in cats}:
        ET.SubElement(cats, f"{{{gns}}}categoryEntry", {"name": name, "id": cid, "hidden": "false"})
    force = next(f for f in gst.iter(f"{{{gns}}}forceEntry") if f.get("id") == STANDARD_FORCE)
    links = force.find(f"{{{gns}}}categoryLinks")
    if cid not in {l.get("targetId") for l in links}:
        link = ET.SubElement(links, f"{{{gns}}}categoryLink", {"name": name, "hidden": "false",
                                                                "id": f"mh-foc-{cid}", "targetId": cid})
        ET.SubElement(ET.SubElement(link, f"{{{gns}}}constraints"), f"{{{gns}}}constraint", {
            "type": "max", "value": "1", "field": "selections", "scope": "force", "shared": "true",
            "id": f"mh-foc-{cid}-max", "includeChildSelections": "false", "includeChildForces": "false"})


def _cond(kind, child, value="1"):
    return {"type": kind, "value": value, "field": "selections", "scope": "force", "childId": child,
            "shared": "true", "includeChildSelections": "true", "includeChildForces": "false"}


def _switch(option_id):
    """Configuration 'Super-heavies' switch, as the 7th Edition converter makes them."""
    sid, oid = f"mh-sh-{option_id}", f"mh-sh-{option_id}-hide"
    entry = ET.Element(q("selectionEntry"), {"name": "Super-heavies", "id": sid, "hidden": "false",
                                              "type": "upgrade", "import": "true", "collective": "false"})
    constraint(entry, "min", 1, "force", f"{sid}-min")
    constraint(entry, "max", 1, "force", f"{sid}-max")
    ET.SubElement(child(entry, "categoryLinks"), q("categoryLink"), {
        "id": f"{sid}-cat", "hidden": "false", "targetId": CONFIGURATION, "primary": "true"})
    opt = ET.SubElement(child(entry, "selectionEntries"), q("selectionEntry"), {
        "name": "Hide super-heavies (untick only when both players agree)", "id": oid, "hidden": "false",
        "type": "upgrade", "import": "true", "collective": "false", "defaultAmount": "1"})
    constraint(opt, "max", 1, "parent", f"{oid}-max")
    for e in (entry, opt):
        ET.SubElement(child(e, "costs"), q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    return entry


def add_knight_lords_of_war(factions, report):
    ik = factions.get("Imperial Knights")
    if ik is None:
        return
    ik_id = ik.get("id")
    shared = {e.get("id") for e in ik.find(q("sharedSelectionEntries"))}
    knights = [(l.get("name"), l.get("targetId")) for l in ik.find(q("entryLinks"))
               if l.get("targetId") in shared]
    done = {}
    for side, names in KNIGHTS_FOR.items():
        allowed = [(n, t) for n, t in knights if (n in RENEGADE) == (side == "Chaos")]
        for fname in names:
            root = factions[fname]
            fid = root.get("id")
            al = next(e for e in root.find(q("selectionEntries")) if e.get("name") == "Army List")
            # Lists fielded only through their own detachments (no Super-Heavy section) are left out.
            standard_hidden = {o.get("id") for o in al.iter(q("selectionEntry"))
                               if any(c.get("childId") == STANDARD_FORCE for c in o.iter(q("condition")))}
            eligible = [o.get("id") for o in al.find(q("selectionEntryGroups")).iter(q("selectionEntry"))
                        if o.get("name", "").startswith(("6th Ed", "7th Ed")) and o.get("id") not in standard_hidden]
            if not eligible:
                continue
            # Each eligible list needs a "Hide super-heavies" switch (agreement, p. 8); lists
            # without super-heavies of their own had none.
            roots = root.find(q("selectionEntries"))
            have = set()
            for e in roots:
                if e.get("name") == "Super-heavies":
                    have |= {c.get("childId") for c in e.iter(q("condition"))}
            for o in eligible:
                if o not in have:
                    sw_root = _switch(o)
                    gate(sw_root, o)
                    roots.append(sw_root)
                    report.setdefault("superHeavySwitchesAdded", []).append(
                        next(x.get("name") for x in al.iter(q("selectionEntry")) if x.get("id") == o))
            switches = [e.get("id") for e in root.iter(q("selectionEntry"))
                        if (e.get("name") or "").startswith("Hide super-heavies")]
            links = root.find(q("catalogueLinks"))
            if links is None:
                links = ET.Element(q("catalogueLinks"))
                root.insert(1, links)
            if ik_id not in {l.get("targetId") for l in links}:
                ET.SubElement(links, q("catalogueLink"), {"name": "Imperial Knights", "id": f"{fid}-link-{ik_id}",
                                                         "targetId": ik_id, "type": "catalogue",
                                                         "importRootEntries": "false"})
            box = root.find(q("entryLinks"))
            if box is None:
                box = ET.SubElement(root, q("entryLinks"))
            for i, (n, target) in enumerate(allowed):
                lid = f"mh-klow-{fid}-{i}"
                link = ET.SubElement(box, q("entryLink"), {
                    "name": f"{n} (Lord of War)", "id": lid, "hidden": "true", "collective": "false",
                    "import": "true", "targetId": target, "type": "selectionEntry"})
                mods = ET.SubElement(link, q("modifiers"))
                show = ET.SubElement(mods, q("modifier"), {"type": "set", "field": "hidden", "value": "false"})
                conds = ET.SubElement(ET.SubElement(ET.SubElement(show, q("conditionGroups")), q("conditionGroup"),
                                                    {"type": "or"}), q("conditions"))
                for o in eligible:
                    ET.SubElement(conds, q("condition"), _cond("atLeast", o))
                if switches:    # super-heavies only when both players agree (Unification p. 8)
                    hide = ET.SubElement(mods, q("modifier"), {"type": "set", "field": "hidden", "value": "true"})
                    hc = ET.SubElement(ET.SubElement(ET.SubElement(hide, q("conditionGroups")), q("conditionGroup"),
                                                     {"type": "or"}), q("conditions"))
                    for sw in switches:
                        ET.SubElement(hc, q("condition"), _cond("atLeast", sw))
                cl = ET.SubElement(link, q("categoryLinks"))
                ET.SubElement(cl, q("categoryLink"), {"name": "Super-Heavy", "hidden": "false", "id": f"{lid}-slot",
                                                      "targetId": "5968-f35e-18fd-612b", "primary": "true"})
                ET.SubElement(cl, q("categoryLink"), {"name": KNIGHT_LOW_CATEGORY[1], "hidden": "false",
                                                      "id": f"{lid}-low", "targetId": KNIGHT_LOW_CATEGORY[0],
                                                      "primary": "false"})
            done[fname] = {"knights": len(allowed), "lists": len(eligible), "superHeavySwitches": len(switches)}
    report["knightLordsOfWar"] = done


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
        options, own_forces, ally_forces = [], {}, {}
        for spec in fm:
            e, s, prefix = spec[:3]
            book_edition = spec[3] if len(spec) > 3 else e
            m = members[(e, s)]
            mid = m.get("id")
            rename_collisions(seen, m, report)
            oid = option_for[mid]
            options.append((oid, label(book_edition, s, prefix), era(book_edition)))
            own_forces[oid] = [f.get("id") for f in m.iter(q("forceEntry"))]
            for f in m.iter(q("forceEntry")):
                if f.get("name") in ALLY_FORCES:
                    ally_forces[f.get("id")] = oid
            for cont in ("selectionEntries", "entryLinks"):
                src = m.find(q(cont))
                for el in (list(src) if src is not None else []):
                    detach_from_new_force(el, report)
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
        not_standard = [option_for[members[(m[0], m[1])].get("id")] for m in fm
                        if (m[0], m[1]) in NOT_ON_STANDARD_CHART]
        # Default to a list that can be shown in the standard force, where there is one.
        for fe in root.iter(q("forceEntry")):
            ensure_configuration_first(fe, report)
        sel = selector(fid, options, next((o for o, _, _ in options if o not in not_standard), None))
        restricted = {o: f for o, f in own_forces.items() if f}
        restricted[None] = not_standard
        restrict_to_owner(sel, restricted)
        restrict_allies_to_era(sel, ally_forces, {o: e for o, _, e in options})
        report.setdefault("allyForcesEraChecked", []).extend(
            f"{fname}: {next(f.get('name') for f in root.iter(q('forceEntry')) if f.get('id') == fid)}"
            for fid in ally_forces)
        child(root, "selectionEntries").insert(0, sel)
        if not len(links):
            root.remove(links)
        out[fname] = root
        report.setdefault("factions", {})[fname] = [n for _, n, _ in options]
    add_knight_lords_of_war(out, report)
    return out

#!/usr/bin/env python3
"""Convert catalogues from the 5th Edition source (AnonymousCheese/WH40K5E) to Middlehammer.

The Middlehammer game system is built from this source's game system, so catalogues
only need retargeting plus content fixes:
  * homebrew: the source's "Hide Homebrew Units" switch is treated as permanently on;
    gated units are hidden and unlinked, and the switch is removed from the game system;
  * units from later editions that the source does not tag (EXCLUDED) are removed;
  * units the source wrongly tags as homebrew (RESTORED) are made available;
  * units the source omits (ADDED) are added from the codex;
  * "Custom Content" (now only the Apocalypse switch, which hides super-heavies by default)
    is kept only where it hides something (APOCALYPSE_SWITCH_KEPT).
Used by tools/build_middlehammer.py.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
SOURCE_SYSTEM_ID = "sys-9c90-407d-0876-14fb"
MH_SYSTEM_ID = "sys-middlehammer-2026"
HIDE_HOMEBREW = "0d75-b87c-69ae-f778"
HIDE_APOCALYPSE = "7a0f-60e9-0b8f-41f9"
CUSTOM_CONTENT = "f04b-cec3-c568-abd9"

# Not converted: homebrew lists, and duplicates of books already converted from a
# better source (Witch Hunters 2003 and Tyranids 2001 come from the 3rd Edition source).
SKIPPED = {
    "Adeptus Custodes": "homebrew", "Adeptus Mechanicus": "homebrew",
    "Genestealer Cult": "homebrew", "Leagues of Votann": "homebrew",
    "Witch Hunters": "duplicate of 3rd Edition source Witch Hunters (2003)",
    "Tyranids (3rd Ed)": "hybrid of the 2001 codex with 5th Edition units; 2001 codex comes from the 3rd Edition source",
}

# Units in the source that are not in the codex this catalogue represents
# (released in later editions) and are not tagged homebrew by the source.
EXCLUDED = {
    "Black Templars": {"Gladiator", "Repulsor"},
    "Blood Angels": {"Gladiator", "Repulsor"},
    "Dark Angels": {"Gladiator", "Repulsor"},
    # Bran Redmaw appears only in background text of Codex: Space Wolves (2009) (checked
    # against the maintainer's copy, 2026-10-29); the source's HQ entry has no codex basis.
    "Space Wolves": {"Gladiator", "Repulsor", "Bran Redmaw"},
    "Tyranids": {"Exocrine Brood", "Maleceptor Brood"},
    "Chaos Space Marines": {"Khorne Lord of Skulls"},
    "Imperial Guard": {"Rogal Dorn Battle Tank", "Bullgryn Squad", "Field Ordnance Battery"},
}

# Only these lists have units behind the Apocalypse switch after exclusions; elsewhere the
# "Custom Content" entry would show a switch that does nothing, so it is removed.
APOCALYPSE_SWITCH_KEPT = {"Imperial Guard"}

# Units the source tags homebrew that are in the codex (Pyrovore: Codex Tyranids 2010).
RESTORED = {"Tyranids": {"Pyrovore Brood"}}


UNIT_PROFILE = "0967-823d-dd82-4e47"
UNIT_CHARS = [("WS", "15b1-a34a-6e7c-332e"), ("BS", "63a5-4be2-9cc0-7723"), ("S", "09af-e927-0c3c-9d88"),
              ("T", "ff29-f8b2-5b20-b686"), ("W", "4a81-ac45-a71c-c71e"), ("I", "8517-a46c-d6df-9c75"),
              ("A", "a535-0722-3bc1-4d3c"), ("Ld", "ddd5-77eb-4cc8-9eab"), ("Sv", "c1e7-f1bd-8acd-7595")]
WARGEAR_PROFILE, WARGEAR_DESC = "456a-26d9-cb27-bd5c", "9e5e-2cfd-7c93-749a"
POINTS = "6f18-a8fc-2c5b-9517"


def add_corbulo(cat):
    """Codex: Blood Angels (2010) p. 87 allows Brother Corbulo (105 pts) as one of the 1-3
    Sanguinary Priests of an Elites choice; the source omits him. Profile and wargear from
    the codex (checked 2026-10-29); rules text is referenced, not reproduced."""
    priests = next(g for g in cat.iter(q("selectionEntryGroup")) if g.get("name") == "Priests"
                   and any(e.get("name") == "Sanguinary Priest" for e in g.iter(q("selectionEntry"))))
    entries = priests.find(q("selectionEntries"))
    ref = "See Codex: Blood Angels (2010), page 49."
    pid = "mh-ba2010-corbulo"
    e = ET.SubElement(entries, q("selectionEntry"), {
        "name": "Brother Corbulo", "id": pid, "hidden": "false", "import": "true",
        "type": "model", "collective": "false"})
    ET.SubElement(ET.SubElement(e, q("constraints")), q("constraint"), {
        "id": f"{pid}-unique", "field": "selections", "scope": "roster", "shared": "true",
        "type": "max", "value": "1", "includeChildSelections": "true", "includeChildForces": "true"})
    ET.SubElement(ET.SubElement(e, q("costs")), q("cost"), {"name": "Points", "typeId": POINTS, "value": "105"})
    links = ET.SubElement(e, q("infoLinks"))
    for name, target, lid in (("Bolt Pistol", "d1b6-0b7d-7649-7b73", "bp"), ("Frag Grenades", "6e7c-a63e-3bc6-5bc9", "frag"),
                              ("Krak Grenades", "0a12-b99c-7d80-2ab6", "krak")):
        ET.SubElement(links, q("infoLink"), {"name": name, "id": f"{pid}-{lid}", "hidden": "false",
                                             "targetId": target, "type": "profile"})
    profiles = ET.SubElement(e, q("profiles"))
    prof = ET.SubElement(profiles, q("profile"), {"name": "Brother Corbulo", "id": f"{pid}-profile",
                                                  "hidden": "false", "typeId": UNIT_PROFILE, "typeName": "Unit"})
    chars = ET.SubElement(prof, q("characteristics"))
    for (n, t), v in zip(UNIT_CHARS, ["5", "5", "4", "4", "2", "5", "3", "9", "3+"]):
        ET.SubElement(chars, q("characteristic"), {"name": n, "typeId": t}).text = v
    for n, lid in (("Heaven's Teeth", "teeth"), ("The Red Grail", "grail")):
        w = ET.SubElement(profiles, q("profile"), {"name": n, "id": f"{pid}-{lid}", "hidden": "false",
                                                   "typeId": WARGEAR_PROFILE, "typeName": "Wargear"})
        ET.SubElement(ET.SubElement(w, q("characteristics")), q("characteristic"),
                      {"name": "Description", "typeId": WARGEAR_DESC}).text = ref
    rule = ET.SubElement(ET.SubElement(e, q("rules")), q("rule"),
                         {"name": "The Far-Seeing Eye", "id": f"{pid}-eye", "hidden": "false"})
    ET.SubElement(rule, q("description")).text = ref
    return ["Brother Corbulo"]


# "Counts as Troops" alternates: the source includes a hidden Troops copy of these units but
# never added the rule that reveals it. Checked against the maintainer's codex PDFs (2026-10-29).
# Each entry: (unit, unlockers, options). An unlocker is a root entry name, or
# (root entry name, upgrade name) when the character must take that upgrade.
# Options: per_unlocker -> at most one such Troops unit per unlocking character;
#          min_models -> the Troops version needs at least this many models.
TROOPS_UNLOCKS = {
    # Codex: Space Wolves (2009): Logan Grimnar "The Great Wolf"; Canis Wolfborn "The Wolf King".
    "Space Wolves": [("Wolf Guard Pack", ["Logan Grimnar"], {}),
                     ("Fenrisian Wolf Pack", ["Canis Wolfborn"], {})],
    # Codex: Dark Eldar (2010): Baron Sathonyx "The Lord Hellion"; Urien Rakarth "Master
    # Haemonculus"; Haemonculus / Haemonculus Ancient "Lord of Covens".
    "Dark Eldar": [("Hellions", ["Baron Sathonyx"], {}),
                   ("Wracks", ["Urien Rakarth", "Haemonculus"], {})],
    # Codex: Grey Knights (2011): Draigo "Lord of Titan", Crowe "Keeper of Anarch", Coteaz
    # (Henchmen warbands are Troops and not limited by the number of Inquisitors).
    "Grey Knights": [("Paladin Squad", ["Lord Kaldor Draigo"], {}),
                     ("Purifier Squad", ["Castellan Crowe"], {}),
                     ("Inquisitorial Henchmen Warband", ["Inquisitor Coteaz"], {})],
    # Codex: Space Marines (2008) "Mounted Assault": a Captain on Space Marine bike, or Kor'sarro
    # Khan riding Moondrakkan; Bike squads of at least five models.
    "Space Marines": [("Space Marine Bike Squad (Mounted Assault)",
                       [("Space Marine Captain", "Space Marine Bike"), ("Kor'sarro Khan", "Moondrakken")],
                       {"min_models": 5})],
    # Codex: Orks (2008): "Da Big Boss" (each Warboss allows one Nobz or Meganobz mob as Troops);
    # "Da Big Mek" (each Big Mek allows one Deff Dread as Troops). The combined Nobz-or-Meganobz
    # limit is applied to each separately.
    "Orks": [("Nobz", ["Warboss", "Warboss in Mega-Armour"], {"per_unlocker": True}),
             ("Meganobz", ["Warboss", "Warboss in Mega-Armour"], {"per_unlocker": True}),
             ("Deff Dread", ["Big Mek"], {"per_unlocker": True})],
}


def _cond(cid, kind="condition"):
    attrs = {"type": "atLeast", "value": "1", "field": "selections", "scope": "force", "childId": cid,
             "shared": "true", "includeChildSelections": "true", "includeChildForces": "false"}
    if kind == "repeat":
        attrs.update({"type": None, "repeats": "1", "roundUp": "false"})
        attrs.pop("type")
    return attrs


def add_troops_unlocks(cat, name):
    if name not in TROOPS_UNLOCKS:
        return []
    roots = [e for cont in ("selectionEntries", "entryLinks") if cat.find(q(cont)) is not None
             for e in cat.find(q(cont))]
    ids = {e.get("id"): e for e in cat.iter() if e.get("id")}
    done = []
    for unit, unlockers, opts in TROOPS_UNLOCKS[name]:
        hidden = [e for e in roots if e.get("name") == unit and e.get("hidden") == "true"]
        if len(hidden) != 1:
            raise ValueError(f"{name}: expected one hidden Troops {unit}, found {len(hidden)}")
        link = hidden[0]
        unlock_ids = []
        for u in unlockers:
            root_name, upgrade = (u, None) if isinstance(u, str) else u
            root = [e for e in roots if e.get("name") == root_name and e.get("hidden") != "true"]
            if len(root) != 1:
                raise ValueError(f"{name}: unlocker {root_name!r} not found once")
            target = ids.get(root[0].get("targetId"), root[0])
            if upgrade is None:
                unlock_ids.append(target.get("id"))
            else:
                ups = [x for x in target.iter() if lname(x.tag) == "selectionEntry" and x.get("name") == upgrade]
                if len(ups) != 1:
                    raise ValueError(f"{name}: upgrade {upgrade!r} of {root_name!r} not found once")
                unlock_ids.append(ups[0].get("id"))
        mods = link.find(q("modifiers"))
        if mods is None:
            mods = ET.Element(q("modifiers"))
            link.insert(0, mods)
        m = ET.SubElement(mods, q("modifier"), {"type": "set", "field": "hidden", "value": "false"})
        conds = ET.SubElement(ET.SubElement(ET.SubElement(m, q("conditionGroups")), q("conditionGroup"),
                                            {"type": "or"}), q("conditions"))
        for cid in unlock_ids:
            ET.SubElement(conds, q("condition"), _cond(cid))
        cons = link.find(q("constraints"))
        if cons is None and (opts.get("per_unlocker") or opts.get("min_models")):
            cons = ET.SubElement(link, q("constraints"))
        if opts.get("per_unlocker"):
            # Replace the source's flat "max 1" with one per unlocking character.
            for c in [c for c in cons if c.get("type") == "max"]:
                cons.remove(c)
            cid = f"{link.get('id')}-per-unlocker"
            ET.SubElement(cons, q("constraint"), {"id": cid, "type": "max", "value": "0", "field": "selections",
                                                  "scope": "force", "shared": "true",
                                                  "includeChildSelections": "false", "includeChildForces": "false"})
            for uid in unlock_ids:
                inc = ET.SubElement(mods, q("modifier"), {"type": "increment", "field": cid, "value": "1"})
                ET.SubElement(ET.SubElement(inc, q("repeats")), q("repeat"), _cond(uid, "repeat"))
        if opts.get("min_models"):
            ET.SubElement(cons, q("constraint"), {
                "id": f"{link.get('id')}-min-models", "type": "min", "value": str(opts["min_models"]),
                "field": "selections", "scope": "self", "childId": "model", "shared": "true",
                "includeChildSelections": "true", "includeChildForces": "false"})
        done.append(f"{unit} with {' or '.join(u if isinstance(u, str) else f'{u[0]} ({u[1]})' for u in unlockers)}")
    return done


# Units missing from the source, added from the codex.
ADDED = {"Blood Angels": add_corbulo}


def q(tag):
    return f"{{{CAT_NS}}}{tag}"


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def _hide(el):
    el.set("hidden", "true")
    mods = el.find(q("modifiers"))
    if mods is not None:
        for m in list(mods):
            if m.get("field") == "hidden":
                mods.remove(m)


def convert_one(path, report):
    tree = ET.parse(path)
    cat = tree.getroot()
    name = path.stem
    if cat.get("gameSystemId") != SOURCE_SYSTEM_ID:
        raise SystemExit(f"{path.name}: not a 5th Edition source catalogue")
    entry = {"edition": 5, "source": path.name, "sourceName": name, "id": cat.get("id")}
    par = {c: p for p in cat.iter() for c in p}
    roots = {cont: cat.find(q(cont)) for cont in ("selectionEntries", "entryLinks")}

    hidden, restored = [], []
    for mod in list(cat.iter(q("modifier"))):
        conds = list(mod.iter(q("condition")))
        if not any(c.get("childId") == HIDE_HOMEBREW for c in conds):
            continue
        if len(conds) != 1 or (mod.get("field"), mod.get("value")) != ("hidden", "true") \
                or conds[0].get("type") != "atLeast":
            raise ValueError(f"{name}: unexpected homebrew switch usage {mod.attrib}")
        owner = par[par[mod]]
        if owner.get("name") in RESTORED.get(name, set()):
            par[mod].remove(mod)
            restored.append(owner.get("name"))
        else:
            _hide(owner)
            hidden.append(owner.get("name"))
    if set(restored) != RESTORED.get(name, set()):
        raise ValueError(f"{name}: expected to restore {RESTORED.get(name)} but found {restored}")

    removed = []
    for r in roots.values():
        for el in (list(r) if r is not None else []):
            if el.get("hidden") == "true" and el.get("name") in hidden:
                r.remove(el)
            elif el.get("name") in EXCLUDED.get(name, set()):
                r.remove(el)
                removed.append(el.get("name"))
    missing = EXCLUDED.get(name, set()) - set(removed)
    # A unit may already be gone because the source tagged it homebrew.
    missing -= set(hidden)
    if missing:
        raise ValueError(f"{name}: exclusions not found {missing}")

    uses_apoc = any(c.get("childId") == HIDE_APOCALYPSE for c in cat.iter(q("condition")))
    if name in APOCALYPSE_SWITCH_KEPT and not uses_apoc:
        raise ValueError(f"{name}: expected units behind the Apocalypse switch")
    if name not in APOCALYPSE_SWITCH_KEPT:
        for r in roots.values():
            for el in (list(r) if r is not None else []):
                if el.get("targetId") == CUSTOM_CONTENT:
                    r.remove(el)
                    entry["customContentRemoved"] = True
    added = ADDED[name](cat) if name in ADDED else []
    entry["troopsUnlocks"] = add_troops_unlocks(cat, name)
    cat.set("gameSystemId", MH_SYSTEM_ID)
    entry.update({"added": added, "homebrewHidden": sorted(set(hidden)), "excluded": sorted(removed),
                  "restored": restored})
    return tree, entry


def remove_homebrew_switch(gst, report):
    """The game system's Custom Content entry keeps only the Apocalypse switch."""
    for parent in gst.iter():
        for el in list(parent):
            if el.get("id") == HIDE_HOMEBREW:
                parent.remove(el)
                report["gstHomebrewSwitchRemoved"] = True


def convert_5e(source, gst, report):
    trees = {}
    report.setdefault("skipped5e", {})
    for path in sorted(Path(source).glob("*.cat")):
        if path.stem in SKIPPED:
            report["skipped5e"][path.stem] = SKIPPED[path.stem]
            continue
        tree, entry = convert_one(path, report)
        trees[entry["id"]] = (path, tree, entry)
    remove_homebrew_switch(gst, report)
    report["converted5e"] = [e for _, _, e in trees.values()]
    return trees

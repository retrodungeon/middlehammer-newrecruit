"""Hand-transcribed Imperial Armour entries for 5th Edition era lists.

No community data exists for Imperial Armour Volume 9 and 10 (The Badab War, 2010 and
2011), so their entries are transcribed from the maintainer's copies and added to the
lists they name. Each entry is built like the source's own units: it reuses the source's
shared weapon, wargear and rule profiles, and new special rules are "Abilities" profiles
whose text states the rule's full effect in our own words (the books' wording is not
copied). Profiles, points, wargear and options follow the book exactly.

Entries are checked against the book page noted in each spec before being relied on.
"""
import copy
import xml.etree.ElementTree as ET

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
POINTS = "6f18-a8fc-2c5b-9517"
HQ = "ac8d-efba-1884-d3ad"
UNIT_PROFILE = "0967-823d-dd82-4e47"
UNIT_CHARS = [("WS", "15b1-a34a-6e7c-332e"), ("BS", "63a5-4be2-9cc0-7723"), ("S", "09af-e927-0c3c-9d88"),
              ("T", "ff29-f8b2-5b20-b686"), ("W", "4a81-ac45-a71c-c71e"), ("I", "8517-a46c-d6df-9c75"),
              ("A", "a535-0722-3bc1-4d3c"), ("Ld", "ddd5-77eb-4cc8-9eab"), ("Sv", "c1e7-f1bd-8acd-7595")]
ABILITIES, ABILITY_DESC = "ccb3-7790-3139-7975", "e24a-6018-20cf-d76c"
MELEE, MELEE_ABILITY = "1d88-1369-f0ed-b39c", "2113-98a2-4376-a94c"

# Shared profiles and rules of the 5th Edition source (game system and Space Marines).
LINKS = {
    "And They Shall Know No Fear": ("73f8-658e-9da5-beba", "rule"),
    "Combat Tactics": ("63e6-2a1c-88a5-4120", "rule"),
    "Independent Character": ("db9c-91d8-5b8a-ee16", "profile"),
    "Iron Halo": ("e427-87a4-ee08-b117", "profile"),
    "Terminator Armour": ("a5fa-5ad7-54d4-fd1a", "profile"),
    "Storm Bolter": ("a37b-6942-f8fb-4aee", "profile"),
    "Chain Fist": ("5151-d1aa-1f80-cb94", "profile"),
    "Master-crafted": ("03d9-2a91-7dcd-8f57", "rule"),
}

# Imperial Armour Volume Nine: The Badab War Part One (2010), p. 171 (PDF page 175).
BLAYLOCK = {
    "id": "mh-ia9-blaylock",
    "name": "Captain Mordaci Blaylock (IA9)",
    "template": "Terminator Captain",      # keeps its optional Command Squad, drops its weapon options
    "points": 195,
    "profile": ("Mordaci Blaylock", ["6", "5", "4", "4", "3", "5", "3", "10", "2+"]),
    "links": ["Terminator Armour", "Iron Halo", "Storm Bolter", "Chain Fist", "Master-crafted",
              "And They Shall Know No Fear", "Independent Character", "Combat Tactics"],
    "weapons": [("Foe Ripper", "A master-crafted chainfist.")],
    "abilities": [
        ("Hard as Stone", "Blaylock, and any Terminator squad he has joined, may choose to pass or fail any "
                          "Morale test it is required to take, and cannot be pinned."),
        ("Terminator Attack", "If Blaylock is in your army, your Terminator Squads and Terminator Assault "
                              "Squads are scoring units."),
        ("Company Captain", "Blaylock is an HQ choice for a Codex: Space Marines army. As a Company Captain he "
                            "allows you to take a Space Marine Command Squad, which is an HQ choice that does not "
                            "count against the army's HQ allowance."),
    ],
    "unique": True,
    "source": "Imperial Armour Volume Nine: The Badab War Part One, page 171",
}

ADDITIONS = {"Space Marines": [BLAYLOCK]}


def q(tag):
    return f"{{{CAT_NS}}}{tag}"


def _renumber(el, prefix):
    """Fresh IDs for a copied subtree, including references made inside it."""
    new = {}
    for x in el.iter():
        if x.get("id"):
            new[x.get("id")] = f"{prefix}-{len(new)}"
    for x in el.iter():
        for a in ("id", "targetId", "childId", "field", "scope", "defaultSelectionEntryId"):
            if x.get(a) in new and not (a == "targetId" and x.tag.endswith("Link")):
                x.set(a, new[x.get(a)])


def add_character(cat, spec):
    roots = [e for c in ("selectionEntries", "entryLinks") for e in cat.find(q(c)) if e.get("name") == spec["template"]]
    if len(roots) != 1:
        raise ValueError(f"template {spec['template']!r} not found once")
    ids = {x.get("id"): x for x in cat.iter() if x.get("id")}
    root = roots[0]
    template = ids.get(root.get("targetId"), root)
    e = ET.Element(q("selectionEntry"), {"name": spec["name"], "id": spec["id"], "hidden": "false",
                                          "import": "true", "type": "unit", "collective": "false"})
    # Slot: as the template (HQ).
    cl = root.find(q("categoryLinks"))
    cl = copy.deepcopy(cl if cl is not None else template.find(q("categoryLinks")))
    _renumber(cl, f"{spec['id']}-cat")
    e.append(cl)
    if spec.get("unique"):
        ET.SubElement(ET.SubElement(e, q("constraints")), q("constraint"), {
            "id": f"{spec['id']}-unique", "type": "max", "value": "1", "field": "selections", "scope": "roster",
            "shared": "true", "includeChildSelections": "true", "includeChildForces": "true"})
    ET.SubElement(ET.SubElement(e, q("costs")), q("cost"), {"name": "Points", "typeId": POINTS,
                                                           "value": str(spec["points"])})
    links = ET.SubElement(e, q("infoLinks"))
    for n in spec["links"]:
        target, kind = LINKS[n]
        ET.SubElement(links, q("infoLink"), {"name": n, "id": f"{spec['id']}-link-{len(links)}", "hidden": "false",
                                             "targetId": target, "type": kind})
    profiles = ET.SubElement(e, q("profiles"))
    pname, values = spec["profile"]
    prof = ET.SubElement(profiles, q("profile"), {"name": pname, "id": f"{spec['id']}-profile", "hidden": "false",
                                                  "typeId": UNIT_PROFILE, "typeName": "Unit"})
    chars = ET.SubElement(prof, q("characteristics"))
    for (n, t), v in zip(UNIT_CHARS, values):
        ET.SubElement(chars, q("characteristic"), {"name": n, "typeId": t}).text = v
    for i, (n, text) in enumerate(spec.get("weapons", [])):
        w = ET.SubElement(profiles, q("profile"), {"name": n, "id": f"{spec['id']}-weapon-{i}", "hidden": "false",
                                                   "typeId": MELEE, "typeName": "Melee Weapons"})
        ET.SubElement(ET.SubElement(w, q("characteristics")), q("characteristic"),
                      {"name": "Ability", "typeId": MELEE_ABILITY}).text = text
    for i, (n, text) in enumerate(spec.get("abilities", [])):
        a = ET.SubElement(profiles, q("profile"), {"name": n, "id": f"{spec['id']}-ability-{i}", "hidden": "false",
                                                   "typeId": ABILITIES, "typeName": "Abilities"})
        ET.SubElement(ET.SubElement(a, q("characteristics")), q("characteristic"),
                      {"name": "Description", "typeId": ABILITY_DESC}).text = text
    # Optional Command Squad, copied from the template with fresh IDs.
    squad = next(x for x in template.find(q("selectionEntries")) if x.get("name") == "Command Squad")
    squad = copy.deepcopy(squad)
    _renumber(squad, f"{spec['id']}-cs")
    ET.SubElement(e, q("selectionEntries")).append(squad)
    cat.find(q("selectionEntries")).append(e)
    return spec["name"]


def add_imperial_armour(cat, name):
    return [add_character(cat, s) for s in ADDITIONS.get(name, [])]

"""Hand-built additions and corrections for 6th Edition lists.

Source: Forge World's "Badab War Characters Update for Sixth Edition" (maintainer's copy).
Characters the 6th Edition data lacks are built here like the data's own characters: they
link the list's shared wargear and rules by name, and new rules are written out in full in
our own words. The update makes these characters HQ choices for a Codex: Space Marines
army (2013), so every Badab character of the Siege Assault Vanguard list is also offered
in the Codex: Space Marines (2013) list.
"""
import copy
import xml.etree.ElementTree as ET

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
POINTS = "6f18-a8fc-2c5b-9517"
HQ = "ac8d-efba-1884-d3ad"
SAV = "Space Marines - FW - Siege Assault Vanguard"
CODEX = "Space Marines - Codex"

# Points that differ from the Badab update: {source catalogue: {entry name: points}}.
POINT_FIXES = {
    SAV: {"Captain Zhrukhal Androcles, Star Phantoms (FW)": 145},
    CODEX: {"Chaplain Ivanus Enkomi (IA12)": 145},
}

# Unique characters whose only limit in the data was a top-level "per parent" maximum
# (removed by the converter): one per roster.
UNIQUE = {CODEX: ["Cypher"]}

# Characters of the update, matched by name in the Siege Assault Vanguard list.
BADAB = ["Carab Culln", "Sevrin Loth", "Tyberos", "Titus", "Narvaez", "Tarnus Vale", "Issodon", "Blaylock",
         "Mir'san", "Ashmantle", "Harath Shen", "Redth", "Thulsa Kane", "Androcles", "Vaylund Cal", "Courbray",
         "Alberec", "Huron", "Sumatris", "Valthex", "Moloc", "Enkomi"]
NOT_BADAB = ("Commander Carab Culln, Captain", "Sergeant Culln")   # other versions in the data

NEW_CHARACTERS = [
    {
        "id": "mh6-tyberos", "name": "Tyberos the Red Wake, Carcharodons (FW)", "points": 190,
        "source": "Badab War Characters Update (6th Ed); Imperial Armour 10 p. 178",
        "profile": {"Unit Type": "Infantry (Character)", "WS": "6", "BS": "5", "S": "4", "T": "4", "W": "4",
                    "I": "5", "A": "5", "LD": "10", "Save": "2+"},
        "profiles": ["Terminator armour", "Teleport homer", "Orbital Bombardment"],
        "rules": ["And They Shall Know No Fear", "Independent Character",
                  "Chapter Tactics: Reavers of the Outer Darkness", "Chapter Tactics: Blood Hunger"],
        "weapons": [("Hunger", "-", "x2", "2", "Melee, Armourbane, Specialist Weapon, Unwieldy"),
                    ("Slake", "-", "User", "3", "Melee, Shred, Specialist Weapon")],
        "new_rules": [
            ("Weapon Mastery", "Tyberos may split his Attacks in an assault freely between Hunger and Slake (his "
                               "profile already includes the extra Attack for two weapons)."),
            ("The Scent of Blood", "If Tyberos gains Rage from Chapter Tactics (Carcharodons), he and every other "
                                   "model with Rage from that rule have +1 Strength for the rest of the battle."),
            ("The Red Brethren", "An army including Tyberos may take one Terminator Assault Squad armed entirely "
                                 "with lightning claws as a Troops choice."),
            ("Warlord", "Tyberos is always the army's Warlord. Instead of a Warlord Trait he has Savagery Beyond "
                        "Reason: he and any unit he joins have Preferred Enemy (Infantry). (The Unification does not "
                        "use Warlord Traits; check with your opponent.)"),
            ("Chapter Master", "HQ choice for a Codex: Space Marines army with Chapter Tactics (Carcharodons). No "
                               "primary detachment in the army may include another Chapter Master, named or not. One "
                               "Honour Guard squad may be taken, not counting against the HQ allowance."),
        ],
    },
    {
        "id": "mh6-issodon", "name": "Lias Issodon, Raptors (FW)", "points": 175,
        "source": "Badab War Characters Update (6th Ed); Imperial Armour 9 p. 169",
        "profile": {"Unit Type": "Infantry (Character)", "WS": "5", "BS": "6", "S": "4", "T": "4", "W": "4",
                    "I": "6", "A": "3", "LD": "10", "Save": "2+"},
        "profiles": ["Artificer armour", "Power sword", "Bolt pistol", "Frag grenades", "Krak grenades",
                     "Locator beacon"],
        "rules": ["And They Shall Know No Fear", "Independent Character", "Shrouded",
                  "Chapter Tactics: Strike from the Shadows", "Chapter Tactics: Legendary Marksmen"],
        "weapons": [("Malice", "30\"", "4", "5", "Salvo 2/4, Special Issue Ammunition")],
        "new_rules": [
            ("Malice", "Each Shooting phase Malice may instead fire as any Special Issue Ammunition from Codex: Space "
                       "Marines, replacing its profile completely. Malice benefits from Chapter Tactics (Raptors) "
                       "rules for boltgun fire."),
            ("Infiltrate, Isolate, Destroy", "After Scout redeployments, before the game begins, choose one deployed "
                                             "enemy unit, Monstrous Creature or vehicle (not an Independent Character "
                                             "outside a squad). A unit or Monstrous Creature suffers D6+3 Wounds with "
                                             "no AP, allocated as shooting from the nearest unit of Issodon's force; a "
                                             "vehicle suffers D3 rolls on the Haywire table."),
            ("Cunning Strategist", "While Issodon lives, his army may re-roll any Reserve Rolls (failed or "
                                   "successful), and the opposing army has -1 to all its Reserve Rolls."),
            ("Warlord", "Issodon is always the army's Warlord, with the Master of Manoeuvre trait instead of rolling. "
                        "(The Unification does not use Warlord Traits; check with your opponent.)"),
            ("Chapter Master", "HQ choice for a Codex: Space Marines army with Chapter Tactics (Raptors). No primary "
                               "detachment in the army may include another Chapter Master, named or not. One Honour "
                               "Guard squad may be taken, not counting against the HQ allowance."),
        ],
    },
]


def q(tag, ns=CAT_NS):
    return f"{{{ns}}}{tag}"


def _profile_type(gst, name):
    pt = next(p for p in gst.iter(q("profileType", GST_NS)) if p.get("name") == name and p.get("id").startswith("mh6-"))
    return pt.get("id"), {c.get("name"): c.get("id") for c in pt.iter(q("characteristicType", GST_NS))}


def _shared(cat, tag, name):
    for container in ("sharedProfiles", "sharedRules"):
        box = cat.find(q(container))
        for el in (list(box) if box is not None else []):
            if el.tag == q(tag) and (el.get("name") or "").lower() == name.lower():
                return el.get("id")
    raise ValueError(f"no shared {tag} {name!r}")


def build_character(cat, gst, spec):
    unit_id, unit_chars = _profile_type(gst, "Unit")
    weapon_id, weapon_chars = _profile_type(gst, "Weapon")
    e = ET.Element(q("selectionEntry"), {"id": spec["id"], "name": spec["name"], "hidden": "false",
                                          "collective": "false", "import": "true", "type": "model"})
    ET.SubElement(ET.SubElement(e, q("categoryLinks")), q("categoryLink"), {
        "name": "HQ", "hidden": "false", "id": f"{spec['id']}-slot", "targetId": HQ, "primary": "true"})
    ET.SubElement(ET.SubElement(e, q("costs")), q("cost"), {"name": "Points", "typeId": POINTS,
                                                           "value": str(spec["points"])})
    ET.SubElement(ET.SubElement(e, q("constraints")), q("constraint"), {
        "type": "max", "value": "1", "field": "selections", "scope": "roster", "shared": "true",
        "id": f"{spec['id']}-unique", "includeChildSelections": "true", "includeChildForces": "false"})
    profiles = ET.SubElement(e, q("profiles"))
    p = ET.SubElement(profiles, q("profile"), {"id": f"{spec['id']}-profile", "name": spec["name"].split(",")[0],
                                               "hidden": "false", "typeId": unit_id, "typeName": "Unit"})
    chars = ET.SubElement(p, q("characteristics"))
    for n, v in spec["profile"].items():
        ET.SubElement(chars, q("characteristic"), {"name": n, "typeId": unit_chars[n]}).text = v
    for i, (n, rng, s, ap, typ) in enumerate(spec["weapons"]):
        w = ET.SubElement(profiles, q("profile"), {"id": f"{spec['id']}-weapon-{i}", "name": n, "hidden": "false",
                                                   "typeId": weapon_id, "typeName": "Weapon"})
        wc = ET.SubElement(w, q("characteristics"))
        for cn, v in (("Range", rng), ("Strength", s), ("AP", ap), ("Type", typ)):
            ET.SubElement(wc, q("characteristic"), {"name": cn, "typeId": weapon_chars[cn]}).text = v
    rules = ET.SubElement(e, q("rules"))
    for i, (n, text) in enumerate(spec["new_rules"]):
        r = ET.SubElement(rules, q("rule"), {"id": f"{spec['id']}-rule-{i}", "name": n, "hidden": "false"})
        ET.SubElement(r, q("description")).text = text
    links = ET.SubElement(e, q("infoLinks"))
    for kind, names in (("profile", spec["profiles"]), ("rule", spec["rules"])):
        for n in names:
            try:
                ET.SubElement(links, q("infoLink"), {"id": f"{spec['id']}-link-{len(links)}", "name": n,
                                                     "hidden": "false", "targetId": _shared(cat, kind, n),
                                                     "type": kind})
            except ValueError:
                # Not shared in this list: copy the list's own definition onto the character.
                src = next(x for x in cat.iter(q(kind)) if (x.get("name") or "").lower() == n.lower())
                own = copy.deepcopy(src)
                own.set("id", f"{spec['id']}-{kind}-{len(links)}")
                (profiles if kind == "profile" else rules).append(own)
    cat.find(q("selectionEntries")).append(e)
    return spec["name"]


def _renumber(el, prefix):
    new = {x.get("id"): f"{prefix}-{i}" for i, x in enumerate(el.iter()) if x.get("id")}
    for x in el.iter():
        for a in ("id", "childId", "field", "scope", "defaultSelectionEntryId"):
            if x.get(a) in new:
                x.set(a, new[x.get(a)])
        if x.get("targetId") in new and not x.tag.endswith("Link"):
            x.set("targetId", new[x.get("targetId")])


def _inline_chapter_tactics(char, sav):
    """In the Siege Assault Vanguard list a character's Chapter Tactics is a selection whose
    limit depends on that list's own Chapter choice, which a Codex: Space Marines force never
    has (so it always showed an error). For the codex copies, the selection is replaced by the
    rules it carries, shown on the character."""
    ids = {x.get("id"): x for x in sav.iter() if x.get("id")}
    par = {c: p for p in char.iter() for c in p}
    for link in [l for l in char.iter(q("entryLink")) if (l.get("name") or "").startswith("Chapter Tactics - ")]:
        target = ids.get(link.get("targetId"))
        holder = par[par[link]]
        info = holder.find(q("infoLinks"))
        if info is None:
            info = ET.SubElement(holder, q("infoLinks"))
        for il in (target.iter(q("infoLink")) if target is not None else []):
            info.append(copy.deepcopy(il))
        par[link].remove(link)


def apply(cats, gst, report):
    """cats: {source stem: converted catalogue root} (after ID suffixing)."""
    done = {"pointsFixed": [], "built": [], "copiedToCodex": []}
    for stem, fixes in POINT_FIXES.items():
        for e in cats[stem].iter(q("selectionEntry")):
            if e.get("name") in fixes:
                for c in e.findall(f"{q('costs')}/{q('cost')}"):
                    if c.get("typeId") == POINTS:
                        c.set("value", str(fixes[e.get("name")]))
                done["pointsFixed"].append(e.get("name"))
    for stem, names in UNIQUE.items():
        for e in cats[stem].find(q("selectionEntries")):
            if e.get("name") in names:
                cons = e.find(q("constraints"))
                if cons is None:
                    cons = ET.SubElement(e, q("constraints"))
                ET.SubElement(cons, q("constraint"), {
                    "type": "max", "value": "1", "field": "selections", "scope": "roster", "shared": "true",
                    "id": f"{e.get('id')}-unique", "includeChildSelections": "true", "includeChildForces": "false"})
                done.setdefault("madeUnique", []).append(e.get("name"))
    for spec in NEW_CHARACTERS:
        done["built"].append(build_character(cats[SAV], gst, spec))
    codex = cats[CODEX]
    have = {e.get("name") for e in codex.find(q("selectionEntries"))} | \
           {e.get("name") for e in codex.find(q("entryLinks"))}
    for e in list(cats[SAV].find(q("selectionEntries"))):
        n = e.get("name") or ""
        if not any(k in n for k in BADAB) or n.startswith(NOT_BADAB):
            continue
        if any(k in h for k in BADAB for h in have if k in n):
            continue                       # the codex list already has its own version
        c = copy.deepcopy(e)
        _inline_chapter_tactics(c, cats[SAV])
        _renumber(c, f"mh6-codex-{e.get('id')}")
        codex.find(q("selectionEntries")).append(c)
        done["copiedToCodex"].append(n)
    report["sixthAdditions"] = done

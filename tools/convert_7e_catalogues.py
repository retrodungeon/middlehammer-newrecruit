#!/usr/bin/env python3
"""Convert 7th Edition catalogues (BSData/wh40k-7th-edition) to Middlehammer.

The source is mostly BattleScribe 2.00 format and is built around 7th Edition
detachments. For each catalogue in CONVERTED:
  * format: 2.00 attributes are translated to the 2.03 form used by Middlehammer
    (characteristic values as text; characteristicTypeId/costTypeId/profileTypeId ->
    typeId; categoryEntryId -> primary categoryLink; 7e points -> Middlehammer Points);
  * Unification p. 9: Formations, detachments (and their Command Benefits), Flyer Wings,
    Spearheads and "Primary Detachment" markers are removed; all catalogue force types
    are dropped and the standard 5th Edition chart is used (Unification p. 8);
  * Unification p. 10: Warlord Traits are hidden;
  * Lords of War (Unification p. 10): independent characters become HQ, super-heavies use
    the super-heavy allowance, anything else becomes Heavy Support;
  * super-heavies sit behind a "Hide super-heavies" switch, on by default (maintainer
    decision 2026-10-29: allowed only when both players agree, Unification p. 8);
  * fortifications are removed (maintainer decision 2026-10-29, may be revisited);
  * Forge World and dataslate switches are treated as always on (content policy);
  * rules that test for the Combined Arms Detachment test for the Middlehammer standard
    force; rules that test for the Apocalypse detachment test the super-heavy switch;
    rules that test for any other detachment never apply.
Used by tools/build_middlehammer.py.
"""
import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
SOURCE_SYSTEM_ID = "e1ebd931-a209-3ce4-87b4-d9918d25530b"
MH_SYSTEM_ID = "sys-middlehammer-2026"
MH_POINTS = "6f18-a8fc-2c5b-9517"
MH_FORCE = "mh-test-force"
MH = {
    "HQ": "ac8d-efba-1884-d3ad", "Troops": "default-category", "Elites": "978c-e18f-8aeb-f4c1",
    "Fast Attack": "74fe-37c3-fbbf-849e", "Heavy Support": "9260-7d57-be5c-bd52",
    "Super-Heavy": "5968-f35e-18fd-612b", "No Force Org Slot": "be45-5314-4388-5bfd",
    "Configuration": "525f-0a42-3f5c-5613",
}

# 7th Edition lists. All can use the standard 5th Edition chart (Unification p. 8); the
# smaller lists also keep their own detachments (DETACHMENTS) without Command Benefits (p. 9).
CONVERTED = [
    "Adepta Sororitas", "Adeptus Custodes Dataslate", "Astra Militarum - Codex",
    "Astra Militarum - FW - Armoured Battle Group", "Astra Militarum - FW - Death Korps of Krieg Assault Brigade",
    "Astra Militarum - FW - Death Korps of Krieg Siege Regiment", "Astra Militarum - FW - Elysian Detachment D-99",
    "Astra Militarum - FW - Elysian", "Blood Angels - Codex (2014)", "Chaos Daemons (40K) - Codex",
    "Chaos Khorne Daemonkin", "Chaos Space Marines - Codex", "Cult Mechanicus Codex 2015",
    "Dark Angels - Codex (2015)", "Dark_Eldar_Codex_(2014)", "Deathwatch - Codex", "Eldar - Corsairs (2015)",
    "Eldar Craftworlds - Codex (2015)", "Genestealer Cults - Codex", "Grey Knights - Codex (2014)",
    "Harlequins - Codex", "Militarum Tempestus - Codex", "Necrons - Codex (2015)", "Necrons - FW - Dark Harvest",
    "Orks - Codex", "Renegades & Heretics", "Skitarii - Codex", "Space Marines - Codex (2015)",
    "Space Marines - FW - Siege Assault Vanguard", "Space Wolves - Codex", "Tau - Codex (2015)",
    "Tyranids - Codex", "Tyrant's Legion - FW - Defenders of Badab", "Ynnari Aeldari - Supplement",
    "Imperial Knights - Codex (2015)", "Chaos Renegade Knights", "Inquisition - Codex", "Assassins Codex",
    "Sisters of Silence Dataslate", "Legion of the Damned - Codex", "Adeptus Astra Telepathica",
    "Aeronautica Imperialis", "Dark Eldar - Supplement - Haemonculus Covens",
]
# Not converted: "Fallen Angels - Supplement" can only be fielded as a Formation, which the
# Unification bans (author's ruling, 2026-10-29).

# Codex detachments kept, as {source list: {source name: Middlehammer name}}. Only their slot
# limits are kept: detachment special rules (Command Benefits, Warlord Trait rerolls) are
# dropped (decision 2026-10-29). Not kept: Castellans of the Imperium (patched out,
# Unification p. 13) and the Adeptus Mechanicus convocations (built from Formations).
DETACHMENTS = {
    "Imperial Knights - Codex (2015)": {"IK Oathsworn Detachment": "Oathsworn Detachment",
                                        "IK Household Detachment": "Household Detachment"},
    "Chaos Renegade Knights": {"Chaos RK Forsworn Knight Detachment": "Forsworn Knight Detachment"},
    "Inquisition - Codex": {"Inquisitorial Detachment": "Inquisitorial Detachment",
                            "Inquisitorial Representative (C:IA)": "Inquisitorial Representative"},
    "Assassins Codex": {"Officio Assassinorum Detachment": "Officio Assassinorum Detachment",
                        "Assassinorum Operative": "Assassinorum Operative"},
    "Sisters of Silence Dataslate": {"Null-Maiden Task Force": "Null-Maiden Task Force"},
    "Legion of the Damned - Codex": {"LotD Legion of the Damned Detachment": "Legion of the Damned Detachment",
                                     "Spectral Host": "Spectral Host"},
    "Adeptus Astra Telepathica": {"Psykana Division": "Psykana Division"},
    "Aeronautica Imperialis": {"Imperial Navy Section": "Imperial Navy Section"},
    "Dark Eldar - Supplement - Haemonculus Covens": {"DE Covenite Coterie Detachment": "Covenite Coterie Detachment"},
}
# Shown after a detachment's name in the force picker.
LIST_NAMES = {"Imperial Knights - Codex (2015)": "Imperial Knights", "Chaos Renegade Knights": "Renegade Knights",
              "Inquisition - Codex": "Inquisition", "Assassins Codex": "Assassins",
              "Sisters of Silence Dataslate": "Sisters of Silence", "Legion of the Damned - Codex": "Legion of the Damned",
              "Adeptus Astra Telepathica": "Astra Telepathica", "Aeronautica Imperialis": "Aeronautica Imperialis",
              "Dark Eldar - Supplement - Haemonculus Covens": "Haemonculus Covens"}
# Detachment slots. Lords of War in these lists are all super-heavies, which this data
# places in the Super-Heavy section; the Lord of War limits apply to it.
DETACHMENT_SLOT = {"HQ": "HQ", "Troops": "Troops", "Elites": "Elites", "Fast Attack": "Fast Attack",
                   "Heavy Support": "Heavy Support", "No Force Org Slot": "No Force Org Slot",
                   "Lord of War": "Super-Heavy"}

SLOT = {"HQ": "HQ", "Troops": "Troops", "Elites": "Elites", "Fast Attack": "Fast Attack",
        "Heavy Support": "Heavy Support", "No Force Org Slot": "No Force Org Slot", "No FOC": "No Force Org Slot",
        "Other": "No Force Org Slot",
        # Army-wide settings (Chaos Legion choice, Chapter Tactics, Blood Tithe table, ...).
        "(No Category)": "Configuration"}
# Settings-style entries that only exist for 7th Edition detachments or are notes.
DROPPED_NAMES = {"Realspace Raiders Detachment", "F.a.q."}
LORDS_OF_WAR = {"Lords of War", "Lord of War", "Legendary Unit"}
# Detachment and formation machinery (Unification p. 9), and fortifications (decision).
DROPPED = {"Formation", "Battle Formation", "Primary Detachment", "Flyer Wing", "Spearhead", "Command",
           "Core", "Auxiliary", "Eradication Cohort", "Instructions", "Command Crew", "Cotorie", "Support",
           "Elites (USF)", "Fortification"}
SWITCH_NAMES = ("show forgeworld", "show fw", "hidden units and dataslates")
SH_RE = re.compile(r"super-?\s?heavy|gargantuan", re.I)


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def q(tag, ns=CAT_NS):
    return f"{{{ns}}}{tag}"


def translate(root):
    """BattleScribe 2.00 -> 2.03 attribute forms, in place (works on catalogue or GST nodes)."""
    for el in root.iter():
        t = lname(el.tag)
        a = el.attrib
        a.pop("book", None)
        if t == "characteristic":
            if "characteristicTypeId" in a:
                a["typeId"] = a.pop("characteristicTypeId")
            if "value" in a:
                el.text = a.pop("value")
        elif t == "cost":
            if "costTypeId" in a:
                a["typeId"] = a.pop("costTypeId")
            if a.get("typeId") == "points":
                a["typeId"], a["name"] = MH_POINTS, "Points"
        elif t == "profile":
            if "profileTypeId" in a:
                a["typeId"] = a.pop("profileTypeId")
            if "profileTypeName" in a:
                a["typeName"] = a.pop("profileTypeName")
        for attr in ("field", "childId", "typeId"):
            if a.get(attr) == "points":
                a[attr] = MH_POINTS


def category_names(source_gst, cats):
    names = {}
    for f in source_gst.iter(q("forceEntry", GST_NS)):
        for c in f.iter(q("categoryEntry", GST_NS)):
            names[c.get("id")] = c.get("name")
    for cat in cats:
        for c in cat.iter():
            if lname(c.tag) == "categoryEntry":
                names.setdefault(c.get("id"), c.get("name"))
    return names


def slot_of(el, names):
    cid = el.get("categoryEntryId")
    if cid is None:
        prim = [l.get("targetId") for l in el.findall(q("categoryLinks") + "/" + q("categoryLink"))
                if l.get("primary") == "true"]
        cid = prim[0] if prim else None
    if cid is None:
        return None
    name = "(No Category)" if cid == "(No Category)" else names.get(cid, "?")
    return re.sub(r"^Formation \(.*\)$", "Formation", name)


def set_slot(el, mh_category):
    el.attrib.pop("categoryEntryId", None)
    links = el.find(q("categoryLinks"))
    if links is not None:
        el.remove(links)
    if mh_category:
        links = ET.SubElement(el, q("categoryLinks"))
        ET.SubElement(links, q("categoryLink"), {"id": f"{el.get('id')}-mhcat", "hidden": "false",
                                                 "targetId": MH[mh_category], "primary": "true"})


def chars_of(node):
    """Characteristic values of node, in either format (2.00 value attribute or 2.03 text)."""
    return [(c.get("value") or c.text or "") for c in node.iter() if lname(c.tag) == "characteristic"]


def is_super_heavy(node, lookup=None):
    """True if any profile of node (inline or linked) has a super-heavy/gargantuan type."""
    nodes = [node]
    if lookup:
        nodes += [lookup[l.get("targetId")] for l in node.iter() if lname(l.tag) in ("infoLink", "entryLink")
                  and l.get("targetId") in lookup]
    if any(SH_RE.search(v) for n in nodes for v in chars_of(n)):
        return True
    if re.search(r"gargantuan", node.get("name") or "", re.I):   # e.g. Gargantuan Squiggoth
        return True
    # 7th Edition gives 9+ Hull Points only to super-heavies; some sources omit the type
    # word (e.g. Thunderhawk Gunship, Sokar Pattern Stormbird).
    for n in nodes:
        for c in n.iter():
            if lname(c.tag) == "characteristic" and c.get("name") in ("HP", "Hull Points"):
                v = c.get("value") or c.text or ""
                if v.strip().isdigit() and int(v) >= 9:
                    return True
    return False


def is_independent_character(node, lookup):
    for el in node.iter():
        target = lookup.get(el.get("targetId"))
        n = " ".join(x for x in (el.get("name"), target.get("name") if target is not None else None) if x)
        if lname(el.tag) in ("rule", "infoLink") and "independent character" in n.lower():
            return True
    return False


def switch_on_value(cond, switch_ids):
    """Truth of a condition on an always-on switch (None if not a switch condition)."""
    if cond.get("childId") not in switch_ids:
        return None
    v, t = float(cond.get("value")), cond.get("type")
    count = 1.0
    return {"equalTo": count == v, "notEqualTo": count != v, "atLeast": count >= v, "greaterThan": count > v,
            "lessThan": count < v, "atMost": count <= v}[t]


def _reduce(node, kind, const):
    """Reduce conditions/conditionGroups under node combined with `kind` ('and'/'or').
    Returns True/False if the whole node is constant, else None (node is edited in place)."""
    conds = node.find(q("conditions"))
    groups = node.find(q("conditionGroups"))
    for c in (list(conds) if conds is not None else []):
        val = const(c)
        if val is None:
            continue
        if (kind == "and" and not val) or (kind == "or" and val):
            return val
        conds.remove(c)
    for g in (list(groups) if groups is not None else []):
        val = _reduce(g, g.get("type", "and"), const)
        if val is None:
            continue
        if (kind == "and" and not val) or (kind == "or" and val):
            return val
        groups.remove(g)
    remaining = (len(conds) if conds is not None else 0) + (len(groups) if groups is not None else 0)
    if remaining == 0:
        return kind == "and"   # empty AND is true, empty OR is false
    return None


def simplify_modifier(mod, const):
    """Simplify a modifier whose conditions include constants. Returns 'never', 'always' or 'conditional'."""
    val = _reduce(mod, "and", const)
    if val is False:
        return "never"
    if val is True:
        for tag in ("conditions", "conditionGroups"):
            for x in mod.findall(q(tag)):
                mod.remove(x)
        return "always"
    return "conditional"


LEGACY_CONSTRAINT_IDS = {"minSelections", "maxSelections", "minInForce", "maxInForce", "minInRoster",
                         "maxInRoster", "minPoints", "maxPoints", "minPercentage", "maxPercentage"}


def unique_constraint_ids(root):
    """2.00 constraints use fixed keyword IDs that the element's own modifiers name as their
    field; 2.03 needs unique IDs. Give each a unique ID and repoint the owner's modifiers."""
    n = 0
    counts = {}
    for c in root.iter(q("constraint")):
        counts[c.get("id")] = counts.get(c.get("id"), 0) + 1
    for el in root.iter():
        cons = el.find(q("constraints"))
        if cons is None:
            continue
        mapping = {}
        for c in cons:
            # Keyword IDs, and IDs the source repeats across entries (source bug).
            if c.get("id") in LEGACY_CONSTRAINT_IDS or counts.get(c.get("id"), 0) > 1:
                new = f"{el.get('id')}-{c.get('id')}"
                mapping[c.get("id")] = new
                c.set("id", new)
                n += 1
        if mapping:
            for m in el.iter(q("modifier")):
                if m.get("field") in mapping:
                    m.set("field", mapping[m.get("field")])
    return n


def make_ids_unique(cat):
    """The 7e source lists were standalone files and reuse each other's IDs (e.g. Blood Angels
    2014 and Space Marines 2015). Middlehammer factions import one another (Blood Angels
    imports Space Marines), so every ID a 7e list defines gets a list-specific suffix.
    References to game-system definitions are untouched."""
    import hashlib
    suffix = "-" + hashlib.sha1(cat.get("id").encode()).hexdigest()[:5]
    defined = {e.get("id") for e in cat.iter() if e.get("id")} - {cat.get("id")}
    for el in cat.iter():
        for attr in ("id", "targetId", "childId", "field", "scope", "defaultSelectionEntryId", "typeId"):
            v = el.get(attr)
            if v in defined:
                el.set(attr, v + suffix)
    return len(defined)


def make_switch(cat, pid):
    """Root Configuration entry with a 'Hide super-heavies' option that is on by default."""
    sid, oid = f"mh-sh-{pid}", f"mh-sh-{pid}-hide"
    entry = ET.Element(q("selectionEntry"), {"name": "Super-heavies", "id": sid, "hidden": "false",
                                              "type": "upgrade", "import": "true", "collective": "false"})
    cons = ET.SubElement(entry, q("constraints"))
    for kind in ("min", "max"):
        ET.SubElement(cons, q("constraint"), {"id": f"{sid}-{kind}", "type": kind, "value": "1",
                                              "field": "selections", "scope": "force", "shared": "true",
                                              "includeChildSelections": "false", "includeChildForces": "false"})
    cl = ET.SubElement(entry, q("categoryLinks"))
    ET.SubElement(cl, q("categoryLink"), {"id": f"{sid}-cat", "hidden": "false", "targetId": MH["Configuration"],
                                          "primary": "true"})
    opts = ET.SubElement(entry, q("selectionEntries"))
    opt = ET.SubElement(opts, q("selectionEntry"), {
        "name": "Hide super-heavies (untick only when both players agree)", "id": oid, "hidden": "false",
        "type": "upgrade", "import": "true", "collective": "false", "defaultAmount": "1"})
    ET.SubElement(ET.SubElement(opt, q("constraints")), q("constraint"), {
        "id": f"{oid}-max", "type": "max", "value": "1", "field": "selections", "scope": "parent",
        "shared": "true", "includeChildSelections": "false", "includeChildForces": "false"})
    for e in (entry, opt):
        ET.SubElement(ET.SubElement(e, q("costs")), q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    cat.find(q("selectionEntries")).insert(0, entry)
    return oid


def hide_when_switch_on(el, oid):
    mods = el.find(q("modifiers"))
    if mods is None:
        mods = ET.Element(q("modifiers"))
        el.insert(0, mods)
    m = ET.SubElement(mods, q("modifier"), {"type": "set", "field": "hidden", "value": "true"})
    ET.SubElement(ET.SubElement(m, q("conditions")), q("condition"), {
        "type": "atLeast", "value": "1", "field": "selections", "scope": "force", "childId": oid,
        "shared": "true", "includeChildSelections": "true", "includeChildForces": "false"})


def make_detachment(fe, mh_name, list_name):
    """A 7e codex detachment as a Middlehammer force: its slot limits only."""
    fid = fe.get("id")
    out = ET.Element(q("forceEntry"), {"name": f"{mh_name} ({list_name})", "id": fid, "hidden": "false"})
    links = ET.SubElement(out, q("categoryLinks"))
    ET.SubElement(links, q("categoryLink"), {"name": "Configuration", "hidden": "false",
                                             "id": f"{fid}-configuration", "targetId": MH["Configuration"]})
    slots, skipped = [], []
    cats = fe.find(q("categoryEntries"))
    for ce in (list(cats) if cats is not None else []):
        n = ce.get("name")
        if n == "Primary Detachment":
            skipped.append(n)
            continue
        mh = DETACHMENT_SLOT[n]
        lid = f"{fid}-{mh.lower().replace(' ', '-')}"
        link = ET.SubElement(links, q("categoryLink"), {"name": mh, "hidden": "false", "id": lid,
                                                       "targetId": MH[mh]})
        limits = {}
        for c in ce.iter(q("constraint")):
            limits[c.get("type")] = int(float(c.get("value")))
        cons = None
        for kind in ("min", "max"):
            if kind in limits and not (kind == "min" and limits[kind] == 0):
                if cons is None:
                    cons = ET.SubElement(link, q("constraints"))
                ET.SubElement(cons, q("constraint"), {
                    "type": kind, "value": str(limits[kind]), "field": "selections", "scope": "force",
                    "shared": "true", "id": f"{lid}-{kind}"})
        slots.append(f"{mh} {limits.get('min', 0)}-{limits.get('max', 'any')}")
    return out, {"name": out.get("name"), "slots": slots, "notKept": skipped}


def convert_one(path, source_gst, names, rule_names, gst_by_id, forces, report):
    tree = ET.parse(path)
    cat = tree.getroot()
    if cat.get("gameSystemId") != SOURCE_SYSTEM_ID:
        raise SystemExit(f"{path.name}: not a 7th Edition catalogue")
    entry = {"edition": 7, "source": path.name, "sourceName": path.stem, "id": cat.get("id")}
    ids = {e.get("id"): e for e in cat.iter() if e.get("id")}
    par = {c: p for p in cat.iter() for c in p}
    for cont in ("selectionEntries", "entryLinks"):
        if cat.find(q(cont)) is None:
            ET.SubElement(cat, q(cont))

    # Forge World / dataslate switches: always on.
    switch_ids, unlocked = set(), 0
    for cont in ("selectionEntries", "entryLinks"):
        for el in list(cat.find(q(cont))):
            target = ids.get(el.get("targetId"), gst_by_id.get(el.get("targetId"), el))
            nm = (el.get("name") if el.get("name") not in (None, "None", "New EntryLink") else target.get("name")) or ""
            if any(s in nm.lower() for s in SWITCH_NAMES):
                switch_ids |= {el.get("id"), target.get("id")} | {x.get("id") for x in el.iter() if x.get("id")}
                cat.find(q(cont)).remove(el)
    for mod in list(cat.iter(q("modifier"))):
        if not any(c.get("childId") in switch_ids for c in mod.iter(q("condition"))):
            continue
        if simplify_modifier(mod, lambda c: switch_on_value(c, switch_ids)) == "never":
            par[mod].remove(mod)
        unlocked += 1
    entry["fwSwitchUnlocked"] = unlocked

    # Warlord Traits (Unification p. 10).
    trait_ids = {e.get("id") for e in source_gst.iter() if (e.get("name") or "").startswith("BRB:") and "Trait" in e.get("name")}
    hidden_traits = 0
    for el in cat.iter():
        if lname(el.tag) in ("selectionEntry", "selectionEntryGroup", "entryLink"):
            nm = el.get("name") or ""
            if nm.startswith("Warlord Trait") or nm == "Warlord Traits" or el.get("targetId") in trait_ids:
                el.set("hidden", "true")
                mods = el.find(q("modifiers"))
                if mods is not None:
                    for m in list(mods):
                        if m.get("field") == "hidden":
                            mods.remove(m)
                hidden_traits += 1
    entry["warlordTraitsHidden"] = hidden_traits

    # Root entries: drop detachment machinery, map slots, reassign Lords of War.
    dropped, low, uncategorised, super_heavy = [], {"HQ": [], "Super-Heavy": [], "Heavy Support": []}, [], []
    dropped_ids, primary_ids, dropped_targets = set(), set(), set()
    # The game system's own fortifications (its root entry links).
    fortifications = {l.get("targetId") for l in source_gst.find(q("entryLinks", GST_NS))}
    for cont in ("selectionEntries", "entryLinks"):
        r = cat.find(q(cont))
        for el in list(r):
            target = ids.get(el.get("targetId"), gst_by_id.get(el.get("targetId"), el))
            nm = el.get("name") if el.get("name") not in (None, "", "None", "New EntryLink") else target.get("name")
            if nm:
                el.set("name", nm)
            slot = slot_of(el, names)
            if slot is None and el.get("targetId") in fortifications:
                slot = "Fortification"
            if slot in DROPPED or nm in DROPPED_NAMES:
                r.remove(el)
                dropped.append(f"{slot}: {nm}")
                (primary_ids if slot == "Primary Detachment" else dropped_ids).add(el.get("id"))
                dropped_targets.add(el.get("targetId"))
                continue
            if slot in SLOT:
                set_slot(el, SLOT[slot])
                continue
            sh = is_super_heavy(target, {**gst_by_id, **ids})
            if slot in LORDS_OF_WAR:
                if slot == "Legendary Unit" or sh:
                    new = "Super-Heavy"
                elif is_independent_character(target, {**gst_by_id, **ids}):
                    new = "HQ"
                else:
                    new = "Heavy Support"
                low[new].append(nm)
            elif slot is None:
                # Uncategorised in the source: super-heavies to the allowance, settings
                # (e.g. "Farsight Enclaves") to Configuration, units use no slot as in the source.
                new = "Super-Heavy" if sh else ("Configuration" if target.get("type") == "upgrade" else "No Force Org Slot")
                uncategorised.append(f"{nm} -> {new}")
            else:
                raise ValueError(f"{path.stem}: unknown slot {slot!r} for {nm}")
            set_slot(el, new)
            if new == "Super-Heavy":
                super_heavy.append(el)
    entry.update({"droppedRootEntries": dropped, "lordsOfWar": low, "uncategorised": uncategorised})

    # A removed formation or detachment is never selected; the standard force is always the
    # primary detachment. Targets of removed links count too unless still linked elsewhere.
    still_linked = {l.get("targetId") for l in cat.iter() if lname(l.tag) == "entryLink"}
    dropped_ids |= {t for t in dropped_targets if t and t not in still_linked and t in ids}

    def dropped_value(cond):
        cid, t = cond.get("childId"), cond.get("type")
        if cid not in dropped_ids and cid not in primary_ids:
            return None
        if t in ("instanceOf", "notInstanceOf"):
            present = cid in primary_ids
            return present if t == "instanceOf" else not present
        count = 1.0 if cid in primary_ids else 0.0
        v = float(cond.get("value"))
        return {"equalTo": count == v, "notEqualTo": count != v, "atLeast": count >= v,
                "greaterThan": count > v, "lessThan": count < v, "atMost": count <= v}[t]
    par = {c: p for p in cat.iter() for c in p}
    simplified = 0
    for mod in list(cat.iter(q("modifier"))):
        if any(c.get("childId") in dropped_ids | primary_ids for c in mod.iter(q("condition"))):
            if simplify_modifier(mod, dropped_value) == "never":
                par[mod].remove(mod)
            simplified += 1
    entry["conditionsOnRemovedEntriesSimplified"] = simplified

    # Nested entries: 2.00 categoryEntryId has no meaning once detachments are gone.
    for el in cat.iter():
        el.attrib.pop("categoryEntryId", None)

    # Detachment-dependent rules.
    apoc = next(f.get("id") for f in source_gst.iter(q("forceEntry", GST_NS)) if f.get("name") == "Apocalypse")
    cad = next(f.get("id") for f in source_gst.iter(q("forceEntry", GST_NS)) if f.get("name") == "Combined Arms Detachment")
    uses_apoc = any(c.get("childId") == apoc for c in cat.iter(q("condition")))
    oid = make_switch(cat, cat.get("id")) if (super_heavy or uses_apoc) else None
    for el in super_heavy:
        hide_when_switch_on(el, oid)
    rewired = 0
    for c in cat.iter(q("condition")):
        if c.get("childId") == cad:
            c.set("childId", MH_FORCE)
        elif c.get("childId") == apoc:
            kind = c.get("type")
            if kind not in ("instanceOf", "notInstanceOf", "atLeast"):
                raise ValueError(f"{path.stem}: unexpected Apocalypse condition {c.attrib}")
            c.attrib.update({"childId": oid, "scope": "force", "field": "selections", "shared": "true",
                             "includeChildSelections": "true",
                             "type": "equalTo" if kind in ("instanceOf", "atLeast") else "atLeast",
                             "value": "0" if kind in ("instanceOf", "atLeast") else "1"})
            rewired += 1
    entry["apocalypseConditionsRewired"] = rewired
    entry["superHeavySwitch"] = bool(oid)

    # Codex detachments listed in DETACHMENTS are kept as forces; every other catalogue force
    # type (detachments and formations) is not used. Conditions that test for those can
    # never be true; their IDs are recorded for the validator.
    wanted = DETACHMENTS.get(path.stem, {})
    kept, details = [], []
    for top in cat.findall(q("forceEntries")):
        for fe in top:
            if fe.get("name") in wanted:
                force, info = make_detachment(fe, wanted[fe.get("name")], LIST_NAMES[path.stem])
                kept.append(force)
                details.append(info)
    if len(kept) != len(wanted):
        raise ValueError(f"{path.stem}: detachments not found: {set(wanted) - {i['name'] for i in details}}")
    kept_ids = {f.get("id") for f in kept}
    entry["detachments"] = details
    entry["retiredIds"] = sorted(({f.get("id") for f in cat.iter(q("forceEntry"))} - kept_ids) |
                                 {c.get("id") for fe in cat.iter(q("forceEntry")) for c in fe.iter(q("categoryEntry"))})
    for fe in cat.findall(q("forceEntries")):
        cat.remove(fe)
    if kept:
        container = ET.Element(q("forceEntries"))
        container.extend(kept)
        cat.insert(list(cat).index(cat.find(q("selectionEntries"))), container)

    entry["legacyConstraintIdsReplaced"] = unique_constraint_ids(cat)
    known = set(ids) | set(gst_by_id)
    par = {c: p for p in cat.iter() for c in p}
    broken = []
    for l in list(cat.iter()):
        if lname(l.tag) in ("infoLink", "entryLink") and l.get("targetId") not in known and l in par:
            par[l].remove(l)
            broken.append(l.get("name") or l.get("targetId"))
    entry["brokenSourceLinksRemoved"] = broken
    translate(cat)
    entry["idsMadeUnique"] = make_ids_unique(cat)
    cat.set("gameSystemId", MH_SYSTEM_ID)
    cat.set("battleScribeVersion", "2.03")
    return tree, entry


def close_over_gst(cats, source_gst, gst, report, skip_ids):
    """Copy referenced top-level 7e game-system definitions into the Middlehammer GST."""
    top = {}
    for container in source_gst:
        if lname(container.tag) in ("forceEntries", "entryLinks"):
            continue
        for node in container:
            if node.get("id"):
                top[node.get("id")] = (lname(container.tag), node)
    copied = []
    for _ in range(100):
        known = {e.get("id") for r in [gst] + cats for e in r.iter() if e.get("id")}
        wanted = {e.get(a) for r in [gst] + cats for e in r.iter() for a in ("targetId", "childId", "typeId")
                  if e.get(a)}
        missing = sorted(i for i in wanted - known - skip_ids if i in top)
        if not missing:
            break
        for i in missing:
            cname, node = top[i]
            container = gst.find(q(cname, GST_NS))
            if container is None:
                container = ET.SubElement(gst, q(cname, GST_NS))
            new = copy.deepcopy(node)
            translate(new)
            for el in new.iter():
                el.attrib.pop("categoryEntryId", None)
            container.append(new)
            copied.append(node.get("name"))
    report["gstDefinitions7eCopied"] = len(copied)


def convert_7e(source, gst, report):
    source = Path(source)
    source_gst = ET.parse(source / "Warhammer40K.gst").getroot()
    if source_gst.get("id") != SOURCE_SYSTEM_ID:
        raise SystemExit("Unexpected 7th Edition game system ID")
    paths = [source / f"{n}.cat" for n in CONVERTED]
    roots = [ET.parse(p).getroot() for p in paths]
    names = category_names(source_gst, roots)
    rule_names = {e.get("id"): e.get("name") for e in source_gst.iter() if lname(e.tag) == "rule"}
    gst_by_id = {e.get("id"): e for e in source_gst.iter() if e.get("id")}
    forces = {f.get("id") for f in source_gst.iter(q("forceEntry", GST_NS))}
    trees = {}
    for p in paths:
        tree, entry = convert_one(p, source_gst, names, rule_names, gst_by_id, forces, report)
        trees[entry["id"]] = (p, tree, entry)
    # Retired 7e detachments and their categories: conditions on them never apply.
    retired = set(forces) | {c.get("id") for f in source_gst.iter(q("forceEntry", GST_NS))
                             for c in f.iter(q("categoryEntry", GST_NS))}
    for _, _, e in trees.values():
        retired |= set(e.pop("retiredIds"))
    report["retired7eIds"] = sorted(retired)
    close_over_gst([t.getroot() for _, t, _ in trees.values()], source_gst, gst, report, skip_ids=forces)
    report["converted7e"] = [e for _, _, e in trees.values()]
    return trees

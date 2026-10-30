#!/usr/bin/env python3
"""Convert 6th Edition catalogues (BSData/wh40k-7th-edition release v3.1.4, the last 6th
Edition data set) to Middlehammer.

The source is in the old BattleScribe 1.14b format. translate_legacy() rewrites each
catalogue into the 2.03 format element by element:

  1.14b                                   2.03
  entry / entryGroup                      selectionEntry / selectionEntryGroup
  points="x"                              <cost typeId=Points value=x>
  min/maxSelections, ...InForce,          constraints (scope parent / force / roster);
  ...InRoster, min/maxPoints              ids "<entry id>-<attribute>" so modifiers can target them
  link linkType=entry / entry group       entryLink type=selectionEntry / selectionEntryGroup
  link linkType=profile / rule            infoLink type=profile / rule
  root categoryId (link or target)        primary categoryLink
  modifier field=<characteristic id>      modifier field=<characteristic type id>
  modifier field=points / name            field=Points cost type / name
  modifier field=min/max...               field=<constraint id> (of the entry, or the link's target)
  modifier type hide / show               set hidden true / false
  repeat=true, increment*                 <repeat value=incrementValue repeats=numRepeats ...>
  condition parentId roster / force type  scope roster / force
           / direct parent / <entry id>   / parent / <entry id>

Then the Unification adjustments, as for 7th Edition (see convert_7e_catalogues.py):
Formations, Battle Formations, Spearheads, Fortifications and extra-detachment markers are
removed; Lords of War become HQ (independent characters), super-heavies (Super-Heavy
section) or Heavy Support; Legendary Units are super-heavies; super-heavies sit behind a
"Hide super-heavies" switch; conditions on the Primary Detachment are always true, those
on Apocalypse follow the switch, and those on any other force type are never true.

Every ID a converted list defines gets a list-specific suffix: supplements are copies of
their codex and share its IDs. 6th Edition profile types get "mh6-" IDs because the 7th
Edition source reuses the same IDs with different characteristics.

Used by tools/build_middlehammer.py.
"""
import hashlib
import io
import re
import urllib.request
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

from convert_7e_catalogues import simplify_modifier, make_switch, hide_when_switch_on

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
MH_SYSTEM_ID = "sys-middlehammer-2026"
MH_POINTS = "6f18-a8fc-2c5b-9517"
MH = {
    "HQ": "ac8d-efba-1884-d3ad", "Troops": "default-category", "Elites": "978c-e18f-8aeb-f4c1",
    "Fast Attack": "74fe-37c3-fbbf-849e", "Heavy Support": "9260-7d57-be5c-bd52",
    "Super-Heavy": "5968-f35e-18fd-612b", "No Force Org Slot": "be45-5314-4388-5bfd",
    "Configuration": "525f-0a42-3f5c-5613",
}

# Source file stem -> books not available from another source. The archive's other
# catalogues are 5th Edition codexes (from the 5th Edition source), books the 7th Edition
# source carries in a later revision (Chaos Space Marines 2012, Adepta Sororitas 2013,
# Inquisition 2013, Legion of the Damned 2014, Astra Militarum and Forge World lists), an
# empty Imperial Knights file, Apocalypse and fortification data.
CONVERTED = ["Tau - Codex", "Tau - Supplement - Farsight Enclaves"]

# 6th Edition categories (by name in the source game system) -> Middlehammer slot.
SLOT = {"HQ": "HQ", "Troops": "Troops", "Elites": "Elites", "Elite": "Elites", "Fast Attack": "Fast Attack",
        "Heavy Support": "Heavy Support", "No Force Org Slot": "No Force Org Slot"}
LORDS_OF_WAR = {"Lords of War"}
LEGENDARY = {"Legendary Unit", "Knights"}
DROPPED = {"Formation", "Battle Formation", "Spearhead", "Fortification", "Extra Detachment",
           "Extra Ally Detachment", "Extra Fortification Detachment"}

CONSTRAINTS = [("minSelections", "min", "parent"), ("maxSelections", "max", "parent"),
               ("minInForce", "min", "force"), ("maxInForce", "max", "force"),
               ("minInRoster", "min", "roster"), ("maxInRoster", "max", "roster")]
COND_TYPES = {"equal to": "equalTo", "not equal to": "notEqualTo", "at least": "atLeast",
              "at most": "atMost", "greater than": "greaterThan", "less than": "lessThan",
              "instance of": "instanceOf"}


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def q(tag, ns=CAT_NS):
    return f"{{{ns}}}{tag}"


def kids(el, container):
    c = el.find(q(container))
    return list(c) if c is not None else []


def num(v):
    f = float(v)
    return str(int(f)) if f == int(f) else str(f)


class Translator:
    """1.14b catalogue -> 2.03 catalogue (same IDs; nothing Middlehammer-specific except the
    points cost type and the 6th Edition profile type IDs)."""

    def __init__(self, legacy, gst_ids):
        self.src = legacy
        self.ids = {e.get("id"): e for e in legacy.iter() if e.get("id")}
        self.gst_ids = gst_ids            # forceType / category ids -> name
        self.unhandled = []

    # -- helpers -----------------------------------------------------------------------
    def scope(self, parent_id):
        if parent_id == "roster":
            return "roster"
        if parent_id == "force type":
            return "force"
        if parent_id == "direct parent":
            return "parent"
        if parent_id in self.ids:
            return parent_id
        self.unhandled.append(f"scope {parent_id}")
        return "parent"

    def constraint_field(self, owner, field):
        """Constraint id a min/max modifier targets: on a link, the linked entry's."""
        target = self.ids.get(owner.get("targetId"), owner) if lname(owner.tag) == "link" else owner
        return f"{target.get('id')}-{field}"

    def condition(self, c, parent):
        t = COND_TYPES[c.get("type")]
        out = ET.SubElement(parent, q("condition"), {
            "type": t, "value": num(c.get("value")), "field": "selections",
            "scope": self.scope(c.get("parentId")), "childId": c.get("childId"), "shared": "true",
            "includeChildSelections": "false" if t == "instanceOf" else "true",
            "includeChildForces": "false"})
        if c.get("field") != "selections":
            self.unhandled.append(f"condition field {c.get('field')}")
        return out

    def conditions(self, src, dst):
        conds = kids(src, "conditions")
        if conds:
            box = ET.SubElement(dst, q("conditions"))
            for c in conds:
                self.condition(c, box)
        groups = kids(src, "conditionGroups")
        if groups:
            box = ET.SubElement(dst, q("conditionGroups"))
            for g in groups:
                ng = ET.SubElement(box, q("conditionGroup"), {"type": g.get("type")})
                self.conditions(g, ng)

    def modifiers(self, src, dst, owner):
        mods = kids(src, "modifiers")
        if not mods:
            return
        box = ET.SubElement(dst, q("modifiers"))
        for m in mods:
            kind, field, value = m.get("type"), m.get("field"), m.get("value")
            if kind in ("hide", "show"):
                kind, field, value = "set", "hidden", "true" if kind == "hide" else "false"
            elif field == "points":
                field = MH_POINTS
            elif field == "name":
                pass
            elif field in ("minSelections", "maxSelections", "minInForce", "maxInForce", "minInRoster",
                           "maxInRoster", "minPoints", "maxPoints"):
                field = self.constraint_field(owner, field)
            elif field in self.char_ids:
                field = self.char_ids[field]
            else:
                self.unhandled.append(f"modifier field {field}")
            if kind not in ("set", "increment", "decrement", "append"):
                self.unhandled.append(f"modifier type {kind}")
            nm = ET.SubElement(box, q("modifier"), {"type": kind, "field": field, "value": value or ""})
            if m.get("repeat") == "true":
                child = m.get("incrementChildId")
                ET.SubElement(ET.SubElement(nm, q("repeats")), q("repeat"), {
                    "field": "selections", "scope": self.scope(m.get("incrementParentId")),
                    "value": num(m.get("incrementValue")), "repeats": m.get("numRepeats") or "1",
                    "childId": "any" if child == "no child" else child, "shared": "true",
                    "roundUp": "false", "includeChildSelections": "true", "includeChildForces": "false"})
            self.conditions(m, nm)

    def add_constraints(self, src, dst):
        """Constraints for every limit the source sets, plus unlimited ones a modifier changes."""
        modified = set(self.modified_fields.get(src.get("id"), ()))
        box = None
        for attr, kind, scope in CONSTRAINTS:
            v = src.get(attr)
            if v is None:
                continue
            f = float(v)
            if (kind == "min" and f == 0 or kind == "max" and f < 0) and attr not in modified:
                continue
            box = box if box is not None else ET.SubElement(dst, q("constraints"))
            ET.SubElement(box, q("constraint"), {
                "type": kind, "value": num(v), "field": "selections", "scope": scope, "shared": "true",
                "id": f"{src.get('id')}-{attr}", "includeChildSelections": "true" if scope != "parent" else "false",
                "includeChildForces": "false"})
        for attr, kind in (("minPoints", "min"), ("maxPoints", "max")):
            v = src.get(attr)
            if v is None or ((kind == "min" and float(v) == 0 or kind == "max" and float(v) < 0) and attr not in modified):
                continue
            box = box if box is not None else ET.SubElement(dst, q("constraints"))
            ET.SubElement(box, q("constraint"), {
                "type": kind, "value": num(v), "field": MH_POINTS, "scope": "parent", "shared": "true",
                "id": f"{src.get('id')}-{attr}", "includeChildSelections": "true", "includeChildForces": "false"})

    def name_of(self, target_id):
        t = self.ids.get(target_id)
        return t.get("name") if t is not None else ""

    # -- elements ----------------------------------------------------------------------
    def profile(self, p, parent):
        out = ET.SubElement(parent, q("profile"), {
            "id": p.get("id"), "name": p.get("name"), "hidden": p.get("hidden", "false"),
            "typeId": self.type_ids[p.get("profileTypeId")],
            "typeName": self.type_names[p.get("profileTypeId")]})
        if p.get("page"):
            out.set("page", p.get("page"))
        self.modifiers(p, out, p)
        chars = ET.SubElement(out, q("characteristics"))
        for c in kids(p, "characteristics"):
            ch = ET.SubElement(chars, q("characteristic"), {"name": c.get("name"),
                                                            "typeId": self.char_ids[c.get("characteristicId")]})
            ch.text = c.get("value") or ""
        return out

    def rule(self, r, parent):
        out = ET.SubElement(parent, q("rule"), {"id": r.get("id"), "name": r.get("name"),
                                               "hidden": r.get("hidden", "false")})
        if r.get("page"):
            out.set("page", r.get("page"))
        self.modifiers(r, out, r)
        d = r.find(q("description"))
        ET.SubElement(out, q("description")).text = (d.text if d is not None else "") or ""
        return out

    def link(self, l, entry_links, info_links, root=False):
        kind = l.get("linkType")
        if kind in ("entry", "entry group"):
            out = ET.SubElement(entry_links, q("entryLink"), {
                "id": l.get("id"), "name": self.name_of(l.get("targetId")), "hidden": "false",
                "collective": "false", "import": "true", "targetId": l.get("targetId"),
                "type": "selectionEntry" if kind == "entry" else "selectionEntryGroup"})
            self.modifiers(l, out, l)
            if root:
                self.root_category(out, l)
        elif kind in ("profile", "rule"):
            out = ET.SubElement(info_links, q("infoLink"), {
                "id": l.get("id"), "name": self.name_of(l.get("targetId")), "hidden": "false",
                "targetId": l.get("targetId"), "type": kind})
            self.modifiers(l, out, l)
        else:
            self.unhandled.append(f"link type {kind}")

    def root_category(self, out, src):
        cid = src.get("categoryId")
        if not cid and lname(src.tag) == "link":
            target = self.ids.get(src.get("targetId"))
            cid = target.get("categoryId") if target is not None else None
        name = self.gst_ids.get(cid, "(No Category)") if cid else "(No Category)"
        out.set("mhSourceCategory", name)   # resolved later; removed before output

    def entry_body(self, src, out, root=False):
        if src.get("points") is not None:
            ET.SubElement(ET.SubElement(out, q("costs")), q("cost"),
                          {"name": "Points", "typeId": MH_POINTS, "value": num(src.get("points"))})
        self.modifiers(src, out, src)
        self.add_constraints(src, out)
        profiles = kids(src, "profiles")
        if profiles:
            box = ET.SubElement(out, q("profiles"))
            for p in profiles:
                self.profile(p, box)
        rules = kids(src, "rules")
        if rules:
            box = ET.SubElement(out, q("rules"))
            for r in rules:
                self.rule(r, box)
        links = kids(src, "links")
        entry_links, info_links = ET.Element(q("entryLinks")), ET.Element(q("infoLinks"))
        for l in links:
            self.link(l, entry_links, info_links)
        if len(info_links):
            out.append(info_links)
        entries = kids(src, "entries")
        if entries:
            box = ET.SubElement(out, q("selectionEntries"))
            for e in entries:
                self.entry(e, box)
        groups = kids(src, "entryGroups")
        if groups:
            box = ET.SubElement(out, q("selectionEntryGroups"))
            for g in groups:
                self.group(g, box)
        if len(entry_links):
            out.append(entry_links)

    def entry(self, e, parent, root=False):
        out = ET.SubElement(parent, q("selectionEntry"), {
            "id": e.get("id"), "name": e.get("name"), "hidden": e.get("hidden", "false"),
            "collective": e.get("collective", "false"), "import": "true", "type": e.get("type", "upgrade")})
        if e.get("page") and e.get("page") != "0":
            out.set("page", e.get("page"))
        if root:
            self.root_category(out, e)
        self.entry_body(e, out)
        return out

    def group(self, g, parent):
        out = ET.SubElement(parent, q("selectionEntryGroup"), {
            "id": g.get("id"), "name": g.get("name"), "hidden": g.get("hidden", "false"),
            "collective": g.get("collective", "false"), "import": "true"})
        if g.get("defaultEntryId") and g.get("defaultEntryId") != "(No Default)":
            out.set("defaultSelectionEntryId", g.get("defaultEntryId"))
        self.entry_body(g, out)
        return out

    def run(self, name, type_ids, type_names, char_ids):
        self.type_ids, self.type_names, self.char_ids = type_ids, type_names, char_ids
        # Fields that modifiers change, per entry id (for unlimited constraints).
        self.modified_fields = {}
        par = {c: p for p in self.src.iter() for c in p}
        for m in self.src.iter(q("modifier")):
            owner = par[par[m]]
            if m.get("field") in dict((a, 1) for a, _, _ in CONSTRAINTS) or m.get("field") in ("minPoints", "maxPoints"):
                tid = owner.get("targetId") if lname(owner.tag) == "link" else owner.get("id")
                self.modified_fields.setdefault(tid, set()).add(m.get("field"))
        cat = ET.Element(q("catalogue"), {
            "id": self.src.get("id"), "name": name, "revision": self.src.get("revision", "1"),
            "battleScribeVersion": "2.03", "gameSystemId": MH_SYSTEM_ID, "library": "false",
            "type": "catalogue", "authorName": self.src.get("authorName") or ""})
        rules = kids(self.src, "rules")
        if rules:
            box = ET.SubElement(cat, q("rules"))
            for r in rules:
                self.rule(r, box)
        roots = ET.SubElement(cat, q("selectionEntries"))
        for e in kids(self.src, "entries"):
            self.entry(e, roots, root=True)
        root_links, root_info = ET.SubElement(cat, q("entryLinks")), ET.Element(q("infoLinks"))
        for l in kids(self.src, "links"):
            self.link(l, root_links, root_info, root=True)
        if len(root_info):
            cat.append(root_info)
        for container, tag, fn in (("sharedEntries", "sharedSelectionEntries", self.entry),
                                   ("sharedEntryGroups", "sharedSelectionEntryGroups", self.group),
                                   ("sharedRules", "sharedRules", self.rule),
                                   ("sharedProfiles", "sharedProfiles", self.profile)):
            items = kids(self.src, container)
            if items:
                box = ET.SubElement(cat, q(tag))
                for x in items:
                    fn(x, box)
        return cat


def profile_types(legacy_gst):
    """6th Edition profile types under new IDs, as 2.03 game-system elements."""
    type_ids, type_names, char_ids, elements = {}, {}, {}, []
    for pt in [x for x in legacy_gst.iter() if lname(x.tag) == "profileType"]:
        tid = f"mh6-{pt.get('id')}"
        type_ids[pt.get("id")] = tid
        type_names[pt.get("id")] = pt.get("name")
        new = ET.Element(q("profileType", GST_NS), {"id": tid, "name": pt.get("name"), "hidden": "false"})
        box = ET.SubElement(new, q("characteristicTypes", GST_NS))
        for c in pt.iter():
            if lname(c.tag) == "characteristic":
                cid = f"mh6-{c.get('id')}"
                char_ids[c.get("id")] = cid
                ET.SubElement(box, q("characteristicType", GST_NS), {"id": cid, "name": c.get("name")})
        elements.append(new)
    return type_ids, type_names, char_ids, elements


# -- Unification adjustments -----------------------------------------------------------
def unit_type_text(node):
    out = []
    for p in node.iter(q("profile")):
        for c in p.iter(q("characteristic")):
            if c.get("name") in ("Unit Type", "Type") and c.text:
                out.append(c.text)
    return " ".join(out)


def is_super_heavy(node, lookup):
    names = []
    linked = [lookup[l.get("targetId")] for l in node.iter() if lname(l.tag) in ("entryLink", "infoLink")
              and l.get("targetId") in lookup]
    for el in [node] + linked:
        for p in [x for x in el.iter(q("profile"))] + ([el] if lname(el.tag) == "profile" else []):
            names.append(p.get("typeName") or "")
            for c in p.iter(q("characteristic")):
                if c.get("name") == "HP" and (c.text or "").strip().isdigit() and int(c.text) >= 9:
                    return True
        names.append(unit_type_text(el))
    return any(re.search(r"super[- ]?heavy|gargantuan", n, re.I) for n in names)


def is_independent_character(node, lookup):
    for el in [node] + [lookup.get(l.get("targetId")) for l in node.iter(q("entryLink"))]:
        if el is None:
            continue
        for x in el.iter():
            if lname(x.tag) in ("rule", "infoLink") and "independent character" in (x.get("name") or "").lower():
                return True
    return False


def set_slot(el, slot):
    for cl in el.findall(q("categoryLinks")):
        el.remove(cl)
    box = ET.Element(q("categoryLinks"))
    ET.SubElement(box, q("categoryLink"), {"name": slot, "hidden": "false", "id": f"{el.get('id')}-slot",
                                           "targetId": MH[slot], "primary": "true"})
    el.insert(0, box)


def suffix_ids(cat):
    suffix = "-6e" + hashlib.sha1(cat.get("id").encode()).hexdigest()[:5]
    defined = {e.get("id") for e in cat.iter() if e.get("id")} - {cat.get("id")}
    for el in cat.iter():
        for attr in ("id", "targetId", "childId", "field", "scope", "defaultSelectionEntryId"):
            v = el.get(attr)
            if v in defined:
                el.set(attr, v + suffix)
    return len(defined)


def convert_one(path, legacy_gst, gst_names, types, report):
    legacy = ET.parse(path).getroot()
    if legacy.get("battleScribeVersion") != "1.14b":
        raise SystemExit(f"{path.name}: expected BattleScribe 1.14b data")
    entry = {"edition": 6, "source": path.name, "sourceName": path.stem, "id": legacy.get("id"),
             "book": legacy.get("name")}
    tr = Translator(legacy, gst_names)
    cat = tr.run(legacy.get("name"), *types)
    lookup = {e.get("id"): e for e in cat.iter() if e.get("id")}

    # Root entries: slots, Lords of War, removed formation/detachment machinery.
    dropped, low, uncategorised, super_heavy = [], {"HQ": [], "Super-Heavy": [], "Heavy Support": []}, [], []
    removed_ids, seen = set(), []
    for cont in ("selectionEntries", "entryLinks"):
        box = cat.find(q(cont))
        for el in list(box):
            src = el.attrib.pop("mhSourceCategory", "(No Category)")
            nm = el.get("name")
            target = lookup.get(el.get("targetId"), el)
            if src in DROPPED:
                box.remove(el)
                dropped.append(f"{src}: {nm}")
                removed_ids |= {el.get("id"), el.get("targetId")} - {None}
                continue
            seen.append(el)
            if src in SLOT:
                set_slot(el, SLOT[src])
                continue
            sh = is_super_heavy(target, lookup)
            if src in LEGENDARY:
                # Apocalypse "Legendary Units" repeat units also offered as Lords of War.
                if any(o is not el and o.get("name") == nm for c2 in ("selectionEntries", "entryLinks")
                       for o in cat.find(q(c2)) if o.get("mhSourceCategory") in LORDS_OF_WAR or
                       (o.get("mhSourceCategory") is None and o.get("name") == nm and o in seen)):
                    box.remove(el)
                    dropped.append(f"{src} (also a Lord of War): {nm}")
                    removed_ids.add(el.get("id"))
                    continue
                new = "Super-Heavy"
            elif src in LORDS_OF_WAR:
                new = "Super-Heavy" if sh else ("HQ" if is_independent_character(target, lookup) else "Heavy Support")
                low[new].append(nm)
            elif src == "(No Category)":
                new = "Super-Heavy" if sh else ("Configuration" if target.get("type") == "upgrade" else "No Force Org Slot")
                uncategorised.append(f"{nm} -> {new}")
            else:
                raise ValueError(f"{path.stem}: unknown category {src!r} for {nm}")
            set_slot(el, new)
            if new == "Super-Heavy":
                super_heavy.append(el)
    entry.update({"droppedRootEntries": dropped, "lordsOfWar": low, "uncategorised": uncategorised})

    # Targets of removed root entries that nothing else links to count as never selected.
    still = {l.get("targetId") for l in cat.iter(q("entryLink"))}
    never = {i for i in removed_ids if i not in still}
    forces = {fid for fid, n in gst_names.items() if n in FORCE_NAMES}
    PRIMARY_DETACHMENT = next(f for f in forces if gst_names[f] == "Primary Detachment")
    APOCALYPSE = next(f for f in forces if gst_names[f] == "Apocalypse")

    def const(c):
        cid, t = c.get("childId"), c.get("type")
        if cid in forces:
            if cid == APOCALYPSE:
                return None           # handled below
            present = cid == PRIMARY_DETACHMENT
            return present if t == "instanceOf" else (not present if t == "notInstanceOf" else None)
        if cid in never:
            v = float(c.get("value"))
            return {"equalTo": 0 == v, "notEqualTo": 0 != v, "atLeast": 0 >= v, "greaterThan": 0 > v,
                    "lessThan": 0 < v, "atMost": 0 <= v, "instanceOf": False, "notInstanceOf": True}[t]
        return None
    par = {c: p for p in cat.iter() for c in p}
    folded = 0
    for mod in [m for m in cat.iter() if lname(m.tag) == "modifier"]:
        if any(const(c) is not None for c in mod.iter(q("condition"))):
            if simplify_modifier(mod, const) == "never":
                par[mod].remove(mod)
            folded += 1
    entry["conditionsOnForcesAndRemovedEntriesFolded"] = folded
    par = {c: p for p in cat.iter() for c in p}
    repeats = [r for r in cat.iter(q("repeat")) if r.get("childId") in never]
    for r in repeats:              # a repeat over something never selected adds nothing
        mod = par[par[r]]
        if mod in par:
            par[mod].remove(mod)
    entry["repeatsOnRemovedEntriesDropped"] = len(repeats)

    uses_apoc = any(c.get("childId") == APOCALYPSE for c in cat.iter(q("condition")))
    oid = make_switch(cat, cat.get("id")) if (super_heavy or uses_apoc) else None
    for el in super_heavy:
        hide_when_switch_on(el, oid)
    for c in cat.iter(q("condition")):
        if c.get("childId") == APOCALYPSE:
            kind = c.get("type")
            if kind not in ("instanceOf", "notInstanceOf"):
                raise ValueError(f"{path.stem}: unexpected Apocalypse condition {c.attrib}")
            c.attrib.update({"childId": oid, "scope": "force", "field": "selections", "shared": "true",
                             "includeChildSelections": "true",
                             "type": "equalTo" if kind == "instanceOf" else "atLeast", "value": "0" if kind == "instanceOf" else "1"})
    entry["superHeavySwitch"] = bool(oid)
    left = sorted({c.get("childId") for c in cat.iter(q("condition")) if c.get("childId") in forces})
    if left:
        raise ValueError(f"{path.stem}: conditions on force types remain: {left}")
    if tr.unhandled:
        raise ValueError(f"{path.stem}: unhandled legacy constructs: {sorted(set(tr.unhandled))}")
    entry["idsMadeUnique"] = suffix_ids(cat)
    return cat, entry


FORCE_NAMES = {"Primary Detachment", "Allied Detachment", "Formation Detachment", "Inquisitorial Detachment",
               "Fortification", "Apocalypse", "Spearhead", "Planetstrike Attacker", "Planetstrike Defender",
               "Zone Mortalis: Attacker", "Zone Mortalis: Defender", "Zone Mortalis: Combatant",
               "Primary Knight Detachment", "Allied Knight Detachment", "Legion of the Damned Detachment"}


def fetch_archive(info, cache):
    """The 6th Edition data is a release asset (a zip), not a git commit."""
    dest = cache / "wh40k-6th-edition"
    marker = dest / ".sha256"
    if marker.exists() and marker.read_text().strip() == info["sha256"]:
        return dest
    url = f"https://github.com/{info['repository']}/releases/download/{info['release']}/{info['asset']}"
    data = urllib.request.urlopen(url).read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != info["sha256"]:
        raise SystemExit(f"6th Edition archive checksum mismatch: {digest}")
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for n in z.namelist():
            if "/" in n or n.startswith("."):
                raise SystemExit(f"Unexpected archive member {n}")
            (dest / n).write_bytes(z.read(n))
    marker.write_text(digest)
    return dest


def convert_6e(source, gst, report):
    source = Path(source)
    legacy_gst = ET.parse(source / "Warhammer40K.gst").getroot()
    gst_names = {e.get("id"): e.get("name") for e in legacy_gst.iter() if lname(e.tag) in ("category", "forceType")}
    type_ids, type_names, char_ids, elements = profile_types(legacy_gst)
    box = gst.find(q("profileTypes", GST_NS))
    have = {p.get("id") for p in box}
    for el in elements:
        if el.get("id") not in have:
            box.append(el)
    out = {}
    for name in CONVERTED:
        p = source / f"{name}.cat"
        cat, entry = convert_one(p, legacy_gst, gst_names, (type_ids, type_names, char_ids), report)
        out[cat.get("id")] = (p, ET.ElementTree(cat), entry)
    report["converted6e"] = [e for _, _, e in out.values()]
    return out


if __name__ == "__main__":
    raise SystemExit("Run tools/build_middlehammer.py, which builds every Middlehammer catalogue.")

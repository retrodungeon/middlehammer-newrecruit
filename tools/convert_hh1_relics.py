#!/usr/bin/env python3
"""Relics of the Age of Darkness: Horus Heresy 1st Edition units for 6th/7th Edition lists.

Optional add-on (maintainer decisions 2026-10-30). Units from the Horus Heresy 1st Edition
army lists (BSData/horus-heresy-1st-edition, pinned in sources/upstreams.json) are offered
to the 6th/7th Edition Army Lists of their successor factions, behind a Configuration toggle
that is off by default. convert_relics() turns each Heresy list into one block of content
per host faction; add_relics() puts that block in the faction catalogue.

Rules (see docs/unification-rules-ledger.md, "Relics of the Age of Darkness"):
  * standard 5th Edition chart only: Rites of War, Heresy force types (Crusade, Zone
    Mortalis, Strategic Raid, Onslaught, Leviathan, Castellan) and Allied Detachments are
    not used, so units keep only their base slot;
  * no named characters and no Primarchs;
  * Legion-specific units go to their successor faction (HOSTS);
  * army-wide Legion traits are dropped; units get the host list's army-wide rules instead
    (RELIC_RULE_TEXT, maintainer ruling 2026-10-30);
  * as for 7th Edition lists: no Warlord Traits, Lords of War reassigned (Unification p. 10),
    fortifications removed, super-heavies behind the list's "Hide super-heavies" switch;
  * no Hull Points (p. 9); super-heavies get Structure Points of 1/3 their Hull Points (p. 10);
  * fan-made content is not converted (content policy).
"""
import copy
import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from convert_7e_catalogues import simplify_modifier, unique_constraint_ids
from rules_text_6e import core_5e, fill_from, seventh_all, texts_of

CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
SOURCE_SYSTEM_ID = "ca571888-56a9-c58e-ddaf-54f4713538bc"
GAME_SYSTEM = "The Horus Heresy.gst"
MH_POINTS = "6f18-a8fc-2c5b-9517"
CONFIGURATION = "525f-0a42-3f5c-5613"
ERA_6_7 = "mh-era-6-7"
MH = {
    "HQ": "ac8d-efba-1884-d3ad", "Troops": "default-category", "Elites": "978c-e18f-8aeb-f4c1",
    "Fast Attack": "74fe-37c3-fbbf-849e", "Heavy Support": "9260-7d57-be5c-bd52",
    "Super-Heavy": "5968-f35e-18fd-612b", "No Force Org Slot": "be45-5314-4388-5bfd",
    "Dedicated Transport": "168b-a772-94f7-83f5",
}
TOGGLE_NAME = "Relics of the Age of Darkness"
TOGGLE_OPTION = "Use Horus Heresy 1st Edition units (both players should agree)"
NAME_SUFFIX = " (Heresy)"

# ---------------------------------------------------------------- Legiones Astartes
LA_FILE = "(HH) Legiones Astartes - Crusade Army List.cat"
LEGIONS = {
    "e6fb-0e54-0be1-9ed1": "Dark Angels", "74c0-fb49-35d8-28ac": "Emperor's Children",
    "a5b8-cb5e-952f-3d3e": "Iron Warriors", "5c66-2306-9285-8809": "White Scars",
    "7c91-a83b-8ca5-e5db": "Space Wolves", "9f2f-6f6f-1978-5623": "Imperial Fists",
    "cf56-aabc-9977-728d": "Night Lords", "d97b-d19f-4972-8e7f": "Blood Angels",
    "83c2-692c-6560-3d68": "Iron Hands", "a511-1645-ac77-af33": "World Eaters",
    "34fa-286c-521b-2899": "Ultramarines", "9311-3c42-349a-b51a": "Death Guard",
    "fc29-3cdf-838d-e6b7": "Thousand Sons", "cf2e-9aed-ccc5-5696": "Sons of Horus",
    "edd3-79ac-eb75-34b7": "Word Bearers", "9c29-e6cd-2167-ce90": "Salamanders",
    "09b8-26b3-b27d-621a": "Raven Guard", "2cbb-1638-186f-49ba": "Alpha Legion",
    "dbf2-d8be-0406-b8d6": "Blackshields",
}
LOYALIST, TRAITOR = "25b6-d93f-bbd2-95a9", "08ff-9734-7fbc-cb73"
CRUSADE_FORCE = " Crusade"
TRAITORS = {"Emperor's Children", "Iron Warriors", "Night Lords", "World Eaters", "Death Guard",
            "Thousand Sons", "Sons of Horus", "Word Bearers", "Alpha Legion"}
# Host faction -> Legions whose units it receives (successor factions, decision 2026-10-30).
# Blackshields have no successor and are not converted.
HOSTS = {
    "Space Marines": ["Ultramarines", "Imperial Fists", "White Scars", "Iron Hands", "Salamanders",
                      "Raven Guard"],
    "Dark Angels": ["Dark Angels"],
    "Blood Angels": ["Blood Angels"],
    "Space Wolves": ["Space Wolves"],
    "Chaos Space Marines": sorted(TRAITORS),
}

# Heresy slot categories -> Middlehammer sections.
SLOT = {"HQ:": "HQ", "Troops:": "Troops", "Elites:": "Elites", "Fast Attack:": "Fast Attack",
        "Heavy Support:": "Heavy Support", "Bodyguard": "No Force Org Slot",
        "Dedicated Transport:": "Dedicated Transport", "No Force Org": "No Force Org Slot",
        "Compulsory HQ:": "HQ", "Compulsory Troops:": "Troops", "Compulsory Elite:": "Elites",
        "Compulsory Fast Attack:": "Fast Attack"}
DROPPED_SLOTS = {"Allegiance", "Warlord Traits", "Fortification:", "Dedicated Transport Restictions"}
# Categories that only exist for Heresy army construction: conditions on them never apply.
DEAD_CATEGORY = re.compile(r"^(Rite of War|Primarch|Use Playtest Rules|Warlord|Mournival|Delegatus|"
                           r"Emperor's Children Warlord|PotL|Additional Shattered|Allied Detachment|"
                           r"Master of the Legion|Armies of Dark Compliance|Centurion|Consul|Praetor$)")
# Named characters and Primarchs (decision 2026-10-30: none). This list is the authority;
# the report lists any other root entry limited to one per roster, for review.
NAMED = {
    "Ahzek Ahriman", "Alexis Polux", "Alpharius", "Angron, The Primarch ", "Argel Tal", "Armillus Dynat",
    "Autilon Skorr", "Calas Typhon", "Captain Remus Ventanus", "Captain Saul Tarvitz", "Cassian Dracos",
    "Cassian Dracos Reborn", "Centurion Shabran Darr", "Chapter Master Raldoron", "Corswain",
    "Corvus Corax", "Dominion Zephon", "Endryd Haar", "Erasmus Golg", "Exodus", "Ezekyle Abaddon",
    "Fafnir Rann", "Farith Redloss", "Ferrus Manus", "Flaymaster Mawdrym Llansahai",
    "Fulgrim the Illuminator", "Gahlan Surlak", "Garviel Loken", "Geigor Fell-Hand",
    "High Chaplain Erebus", "Hol Beloth", "Holguin", "Horus the Warmaster", "Hvarl Red-Blade",
    "Iron-father Autek Mor", "Jaghatai Khan", "Judiciar Aster Crohne", "Kharn the Bloody",
    "Kheron Ophion of the Kyroptera", "Konrad Curze", "Kor Phaeron", "Kyr Vhalen", "Leman Russ",
    "Lion El'Jonson", "Lord Chaplain Nomus Rhy'tan", "Lord Commander Eidolon", "Lorgar",
    "Magistus Amon", "Magnus The Red", "Maloghurst the Twisted", "Marduk Sedras",
    "Marshal Durak Rask", "Moritat-Prime Kaedes Nex", "Mortarion the Reaper", "Nakrid Thole",
    "Nathaniel Garro", "Nemean Reaver, The", "Nârik Dreygur", "Perturabo, The Primarch", "Qin Xa",
    "Roboute Guilliman", "Rogal Dorn", "Sanguinius", "Section Leader Crysos Mortug", "Sevatar",
    "Shadrak Meduson", "Sigismund", "Spearhead-Centurion Castrmen Orth",
    "Strike Captain Alvarex Maun", "Tsolmon Khan", "Tybalt Marr", "Tylos Rubio", "Vulkan",
    "Xiaphas Jurr", "Zardu Layak", "Rylanor the Unyielding", "Honoured Telemechrus",
    "Wolf-kin of Russ, The", "Aetos Dios", "The Tormentor",
    "Cor’bax Utterblight, Daemon Prince of the Ruinstorm", "Samus, Daemon Prince of the Ruinstorm",
}
# Not units, or Heresy army machinery.
NOT_UNITS = {"Legion and Allegiance", "Rite of War", "Warlord Traits", "Allied Detachment",
             "Dedicated Transports Restrictions", "The Rewards of Treason", "War Machine Detachment",
             "Sub-orbital Strike Wing"}
# Lords of War in the Legion list that are Legion vehicles. Titans, Knights and Imperial Army
# super-heavies belong to other Heresy lists (Mechanicum, Questoris Knights, Solar Auxilia)
# and are not offered to Marine lists.
LEGION_LORDS_OF_WAR = {
    "Cerberus Heavy Tank Destroyer, Legion", "Falchion Super-heavy Tank Destroyer, Legion",
    "Fellblade, Legion", "Glaive Special Weapons Tank, Legion", "Typhon Heavy Siege Tank, Legion",
    "Thunderhawk Gunship, Legion", "Thunderhawk Transporter, Legion", "Sokar Pattern Stormbird",
    "Mastadon Heavy Assault Transport", "Stormblade, Legion", "Malcador Assault Tank, Legion",
}
GENERAL_RULES = {"Night Vision", "Hatred", "Counter-attack", "Preferred Enemy", "Fleet", "Infiltrate", "Rage",
                 "Fearless", "Stubborn", "Furious Charge", "Feel No Pain", "Scout", "Move Through Cover"}
LA_CATEGORY = "Legiones Astartes"      # carries the Legion traits; replaced
LA_RULE = "Legiones Astartes"          # the unit rule itself is kept

RELIC_RULE_NAME = "Relics of the Age of Darkness"
RELIC_RULE_TEXT = (
    "Middlehammer ruling (2026-10-30). This is a Horus Heresy 1st Edition unit fielded in a "
    "6th or 7th Edition army. It counts as having the army-wide special rules that the units of "
    "its Army List have (for example Chapter Tactics or And They Shall Know No Fear), and is "
    "affected by that list's army-wide rules as if it were a unit from that list. It does not "
    "gain Legion traits from the Horus Heresy army lists.")

# Heresy profile types -> Middlehammer profile types, with characteristic renames.
PROFILE_MAP = {
    "556e697423232344415441232323": ("556e697423232344415441232323", {"Save": "Sv"}),  # Unit
    "576561706f6e23232344415441232323": ("576561706f6e23232344415441232323", {}),      # Weapon
    "57617267656172204974656d23232344415441232323": ("57617267656172204974656d23232344415441232323", {}),
    "307d-047f-ca13-706b": ("307d-047f-ca13-706b", {}),                                  # Transport
    "ae70-4738-0161-bec0": ("ae70-4738-0161-bec0", {}), "9c33-b0c8-74bd-e5a7": ("9c33-b0c8-74bd-e5a7", {}),
    "bc97-dea9-9e88-bb7d": ("bc97-dea9-9e88-bb7d", {}),
}
VEHICLE = "56656869636c6523232344415441232323"
WALKER = "57616c6b657223232344415441232323"
SH_WALKER = "0694-6ddb-9e1d-40bd"
FLYER = "3a08-ea03-a598-8615"
MH_VEHICLE, MH_WALKER = "mh6-56656869636c6523232344415441232323", "mh6-57616c6b657223232344415441232323"
MH_SH_VEHICLE = "mh6-56656869636c65202853757065722048656176792923232344415441232323"
MH_SH_WALKER = "mh6-57616c6b6572202853757065722048656176792923232344415441232323"
SH_RE = re.compile(r"super-?\s?heavy", re.I)
SHARED = ("sharedSelectionEntries", "sharedSelectionEntryGroups", "sharedRules", "sharedProfiles",
          "sharedInfoGroups")


def q(tag, ns=CAT_NS):
    return f"{{{ns}}}{tag}"


def lname(tag):
    return tag.rsplit("}", 1)[-1]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def compare(count, cond):
    v, t = float(cond.get("value") or 0), cond.get("type")
    return {"equalTo": count == v, "notEqualTo": count != v, "atLeast": count >= v,
            "greaterThan": count > v, "lessThan": count < v, "atMost": count <= v,
            "instanceOf": count >= 1, "notInstanceOf": count < 1}.get(t)


class Context:
    """Constant values for conditions on things that do not exist in a Middlehammer list:
    the Legion and allegiance choices, Heresy force types, and every source entry that is
    not part of the converted content."""

    def __init__(self, legion, traitor, absent, forces):
        self.legion, self.traitor, self.absent, self.forces = legion, traitor, absent, forces

    def value(self, cond):
        cid = cond.get("childId")
        if cid in LEGIONS:
            return compare(1.0 if LEGIONS[cid] == self.legion else 0.0, cond)
        if cid == LOYALIST:
            return compare(0.0 if self.traitor else 1.0, cond)
        if cid == TRAITOR:
            return compare(1.0 if self.traitor else 0.0, cond)
        if cid in self.forces:   # Heresy force types: only the standard (Crusade) force exists
            return compare(1.0 if self.forces[cid] == CRUSADE_FORCE else 0.0, cond)
        if cid in self.absent:
            return compare(0.0, cond)
        return None


def fold(node, ctx):
    """Simplify every modifier and modifier group under node against ctx; drop those that
    can never apply, and strip conditions that always hold."""
    par = {c: p for p in node.iter() for c in p}
    for mod in [m for m in node.iter() if lname(m.tag) in ("modifierGroup", "modifier", "repeat")]:
        if mod in par and simplify_modifier(mod, ctx.value) == "never":
            par[mod].remove(mod)
    par = {c: p for p in node.iter() for c in p}
    for tag in ("modifiers", "modifierGroups"):
        for el in [m for m in node.iter(q(tag))]:
            if not len(el) and el in par:
                par[el].remove(el)
    return node


def possibly_visible(*nodes):
    """After folding: False if the node is certainly hidden."""
    for node in nodes:
        state = node.get("hidden", "false")
        mods = node.find(q("modifiers"))
        items = [(m, False) for m in (list(mods) if mods is not None else [])]
        for g in node.findall(f"{q('modifierGroups')}/{q('modifierGroup')}"):
            gcond = g.find(q("conditions")) is not None or g.find(q("conditionGroups")) is not None
            items += [(m, gcond) for m in g.iter(q("modifier"))]
        for m, group_conditional in items:
            if m.get("field") != "hidden" or m.get("type") != "set":
                continue
            conditional = group_conditional or m.find(q("conditions")) is not None or \
                m.find(q("conditionGroups")) is not None
            state = "maybe" if conditional else m.get("value")
        if state == "true":
            return False
    return True


def root_probe(node):
    """Copy of node without its contents, for testing root-level visibility."""
    p = copy.deepcopy(node)
    for c in [c for c in p if lname(c.tag) != "modifiers"]:
        p.remove(c)
    return p


def primary_slot(el, target, cats):
    for node in (el, target):
        for l in node.findall(f"{q('categoryLinks')}/{q('categoryLink')}"):
            if l.get("primary") == "true":
                return cats.get(l.get("targetId"))
    return None


def chars(node):
    return {c.get("name"): (c.text if c.text is not None else c.get("value", "")) or ""
            for c in node.iter(q("characteristic"))}


def is_super_heavy_profile(p):
    c = chars(p)
    hp = c.get("HP", "").strip()
    return bool(SH_RE.search(c.get("Type", ""))) or (hp.isdigit() and int(hp) >= 9)


def convert_profile(p, mh_types, notes, hh_char_names):
    """Retype one Heresy profile for the Middlehammer game system (in place). Modifiers of
    its characteristics are pointed at the new characteristic types; Hull Point modifiers
    are dropped (no Hull Points, Unification p. 9)."""
    tid = p.get("typeId")
    rename = {}
    values = chars(p)
    if tid in (VEHICLE, WALKER, SH_WALKER, FLYER):
        sh = tid == SH_WALKER or is_super_heavy_profile(p)
        walker = tid in (WALKER, SH_WALKER)
        if sh:
            new = MH_SH_WALKER if walker else MH_SH_VEHICLE
            hp = values.get("HP", "").strip()
            values["Structure Points"] = str(round(int(hp) / 3)) if hp.isdigit() else hp
            notes.add(f"{p.get('name')}: {hp} HP -> {values['Structure Points']} Structure Points")
            if tid == FLYER and "flyer" not in values.get("Type", "").lower():
                values["Type"] = ", ".join(x for x in ("Flyer", values.get("Type", "")) if x)
        else:
            new = MH_WALKER if walker else (FLYER if tid == FLYER else MH_VEHICLE)
        values.pop("HP", None)
    elif tid in PROFILE_MAP:
        new, rename = PROFILE_MAP[tid]
        values = {rename.get(k, k): v for k, v in values.items()}
    else:
        raise ValueError(f"Unmapped Heresy profile type {p.get('typeName')} ({tid}) on {p.get('name')}")
    ptype = mh_types[new]
    for c in p.findall(q("characteristics")):
        p.remove(c)
    out = ET.Element(q("characteristics"))
    for ct in ptype.iter(q("characteristicType", GST_NS)):
        if ct.get("name") in values and ct.get("name") not in ("HP", "Pg"):
            ET.SubElement(out, q("characteristic"), {"name": ct.get("name"), "typeId": ct.get("id")}).text = \
                values[ct.get("name")]
    p.append(out)
    new_ids = {ct.get("name"): ct.get("id") for ct in ptype.iter(q("characteristicType", GST_NS))}
    mods = p.find(q("modifiers"))
    for m in (list(mods) if mods is not None else []):
        name = hh_char_names.get(m.get("field"))
        if name is None:
            continue
        name = rename.get(name, name)
        if name in new_ids and name not in ("HP", "Pg"):
            m.set("field", new_ids[name])
        else:
            mods.remove(m)
            notes.add(f"{p.get('name')}: {name} modifier dropped")
    p.set("typeId", new)
    p.set("typeName", ptype.get("name"))
    for a in ("profileTypeId", "profileTypeName"):
        p.attrib.pop(a, None)


def reachable(nodes, defined):
    """IDs defined in or reachable from nodes through links (targetId)."""
    seen, stack, visited = set(), list(nodes), set()
    while stack:
        n = stack.pop()
        if id(n) in visited:
            continue
        visited.add(id(n))
        for el in n.iter():
            if el.get("id"):
                seen.add(el.get("id"))
            t = el.get("targetId")
            if t and t in defined and t not in seen:
                seen.add(t)
                stack.append(defined[t])
    return seen


def shared_tops(cat, hh_gst):
    """{id: top-level shared node containing it}."""
    top_of = {}
    for r in (cat, hh_gst):
        for cname in SHARED:
            for cont in r.findall(q(cname)):
                for node in cont:
                    for x in node.iter():
                        if x.get("id"):
                            top_of[x.get("id")] = node
    return top_of


def closure(nodes, defined, top_of):
    """IDs of the converted content: reachable from nodes, where a link into a shared node
    (e.g. one weapon of the game system's "Weapons" group) brings the whole node."""
    alive, frontier = set(), list(nodes)
    while frontier:
        found = reachable(frontier, defined) - alive
        alive |= found
        frontier = [n for n in {id(top_of[i]): top_of[i] for i in found if i in top_of}.values()
                    if not ({x.get("id") for x in n.iter() if x.get("id")} <= alive)]
    return alive


def legion_requirement(el, target, traitor, forces):
    """Legions (and None) in whose context the root entry can be visible."""
    out = []
    for legion in sorted(set(LEGIONS.values())) + [None]:
        ctx = Context(legion, traitor, set(), forces)
        if possibly_visible(*(fold(root_probe(n), ctx) for n in (el, target))):
            out.append(legion)
    return out


def convert_for_host(source, mh_types, host, legions, rep):
    hh_gst = ET.parse(source / GAME_SYSTEM).getroot()
    cat = ET.parse(source / LA_FILE).getroot()
    if hh_gst.get("id") != SOURCE_SYSTEM_ID or cat.get("gameSystemId") != SOURCE_SYSTEM_ID:
        raise SystemExit("Unexpected Horus Heresy 1st Edition game system ID")
    for el in hh_gst.iter():               # the game system uses the catalogue namespace's tags
        el.tag = el.tag.replace(GST_NS, CAT_NS)
    traitor = host == "Chaos Space Marines"
    defined = {e.get("id"): e for r in (hh_gst, cat) for e in r.iter() if e.get("id")}
    cats = {e.get("id"): e.get("name") for r in (hh_gst, cat) for e in r.iter() if lname(e.tag) == "categoryEntry"}
    forces = {e.get("id"): e.get("name") for r in (hh_gst, cat) for e in r.iter() if lname(e.tag) == "forceEntry"}
    default = legions[0] if len(legions) == 1 else None

    # 1. Root entries offered to this host, each with the Legion context it is shown in.
    plan, skipped = [], {k: [] for k in ("named", "notUnits", "heresyOnlySlot", "otherLordsOfWar",
                                         "otherLegion", "neverVisible")}
    for cont in ("selectionEntries", "entryLinks"):
        for el in list(cat.find(q(cont))):
            target = defined.get(el.get("targetId"), el)
            name = el.get("name") or target.get("name")
            slot = primary_slot(el, target, cats)
            if name in NAMED:
                skipped["named"].append(name)
            elif name in NOT_UNITS or slot is None:
                skipped["notUnits"].append(name)
            elif slot in DROPPED_SLOTS:
                skipped["heresyOnlySlot"].append(f"{slot} {name}")
            elif slot == "Lords of War" and name not in LEGION_LORDS_OF_WAR:
                skipped["otherLordsOfWar"].append(name)
            else:
                visible = legion_requirement(el, target, traitor, forces)
                if None in visible:      # generic unit
                    if default is not None and default not in visible:
                        skipped["otherLegion"].append(name)   # e.g. no Tactical Squads for Space Wolves
                        continue
                    context = default
                else:
                    mine = [l for l in legions if l in visible]
                    if not mine:
                        skipped["otherLegion" if visible else "neverVisible"].append(name)
                        continue
                    context = mine[0]
                plan.append((cont, el, name, slot, context))

    # 2. Legion-specific units in a multi-Legion host get their own copies of the shared
    #    entries they use, so that Legion-specific options inside them are folded for their Legion.
    shared_order = [e.get("id") for c in SHARED for cont in cat.findall(q(c)) for e in cont]
    shared_ids = set(shared_order)
    contexts = sorted({c for *_, c in plan if c != default})
    clones = {}
    for c in contexts:
        roots = [el for _, el, _, _, ctx in plan if ctx == c]
        # Source document order, so that the output does not depend on set ordering.
        reached = reachable(roots, defined)
        mine = [i for i in shared_order if i in reached]
        suffix = "-" + slug(c)[:6]
        mapping = {}
        for i in mine:
            mapping.update({x.get("id"): x.get("id") + suffix for x in defined[i].iter() if x.get("id")})
        copies = []
        for i in mine:
            node = copy.deepcopy(defined[i])
            for x in node.iter():
                for attr in ("id", "targetId", "childId", "scope", "field"):
                    if x.get(attr) in mapping:
                        x.set(attr, mapping[x.get(attr)])
            copies.append((cat_container_of(cat, i), node))
        for el in roots:
            for x in el.iter():
                for attr in ("targetId", "childId", "scope", "field"):
                    if x.get(attr) in mapping:
                        x.set(attr, mapping[x.get(attr)])
        clones[c] = (copies, mapping)
        for cont_name, node in copies:
            cat.find(q(cont_name)).append(node)
            defined.update({x.get("id"): x for x in node.iter() if x.get("id")})

    # 3-4. Everything outside the converted content does not exist in a Middlehammer list.
    #    Fold roots and their copies in their own context and shared content in the default
    #    one; drop roots that can never be shown; repeat until nothing more drops.
    clone_ids = {id(n) for c in contexts for _, n in clones[c][0]}
    current = plan
    for _ in range(5):
        # Only what can be selected counts: entries reachable through links from the roots
        # (copied neighbours in a shared node are never selectable).
        alive = reachable([el for _, el, *_ in current], defined)
        absent = {i for i in defined if i not in alive} - set(LEGIONS) - {LOYALIST, TRAITOR} - set(cats) - set(forces)
        absent |= {i for i, n in cats.items() if DEAD_CATEGORY.match(n or "")}
        for c in contexts:
            for _, node in clones[c][0]:
                fold(node, Context(c, traitor, absent, forces))
        for cname in SHARED:
            for r in (cat, hh_gst):
                for cont in r.findall(q(cname)):
                    for node in cont:
                        if id(node) not in clone_ids:
                            fold(node, Context(default, traitor, absent, forces))
        kept = []
        for cont, el, name, slot, context in current:
            fold(el, Context(context, traitor, absent, forces))
            target = defined.get(el.get("targetId"), el)
            if possibly_visible(el, target):
                kept.append((cont, el, name, slot, context))
            else:
                skipped["neverVisible"].append(name)
        if len(kept) == len(current):
            break
        current = kept

    # 5. Build the content block.
    block = build_block(host, cat, hh_gst, kept, defined, cats, mh_types, rep)
    rep["units"] = sorted(f"{SLOT.get(s, s)}: {n.strip()}" + (f" [{c}]" if c and c != default else "")
                          for _, _, n, s, c in kept)
    rep["notConverted"] = {k: sorted(set(v)) for k, v in skipped.items() if v}
    return block


def cat_container_of(cat, i):
    for c in SHARED:
        for cont in cat.findall(q(c)):
            if any(e.get("id") == i for e in cont):
                return c
    raise KeyError(i)


def build_block(host, cat, hh_gst, kept, defined, cats, mh_types, rep):
    """A catalogue-shaped element with the host's Heresy content, every ID prefixed."""
    prefix = f"mh-rad-{slug(host)}-"
    block = ET.Element(q("catalogue"), {"id": prefix + "block", "name": f"Relics: {host}"})
    roots = ET.SubElement(block, q("selectionEntries"))
    links = ET.SubElement(block, q("entryLinks"))
    la_cat = next((i for i, n in cats.items() if n == LA_CATEGORY), None)
    la_rule = next((e for e in cat.iter(q("rule")) if e.get("name") == LA_RULE), None) or \
        next(e for e in hh_gst.iter(q("rule")) if e.get("name") == LA_RULE)
    relic_cat = prefix + "category"
    relic_rule = prefix + "rule"
    lords = {"HQ": [], "Super-Heavy": [], "Heavy Support": []}
    for cont, el, name, slot, context in kept:
        target = defined.get(el.get("targetId"), el)
        el.set("name", name.strip() + NAME_SUFFIX)
        if slot == "Lords of War":
            sh = any(is_super_heavy_profile(p) for n in (el, target) for p in n.iter(q("profile")))
            new = "Super-Heavy" if sh else "Heavy Support"
            lords[new].append(name)
        else:
            new = SLOT[slot]
        for links_el in el.findall(q("categoryLinks")):
            el.remove(links_el)
        cl = ET.SubElement(el, q("categoryLinks"))
        ET.SubElement(cl, q("categoryLink"), {"id": el.get("id") + "-slot", "name": new, "hidden": "false",
                                              "targetId": MH[new], "primary": "true"})
        ET.SubElement(cl, q("categoryLink"), {"id": el.get("id") + "-relic", "name": RELIC_RULE_NAME,
                                              "hidden": "false", "targetId": relic_cat, "primary": "false"})
        (roots if cont == "selectionEntries" else links).append(el)
    rep["lordsOfWar"] = {k: v for k, v in lords.items() if v}

    # Shared content reachable from the kept roots: the list's and the game system's.
    top_of = shared_tops(cat, hh_gst)
    alive = closure(list(roots) + list(links), defined, top_of)
    tops = {id(top_of[i]) for i in alive if i in top_of}
    for cname in SHARED:
        dest = ET.SubElement(block, q(cname))
        for r in (cat, hh_gst):
            for cont in r.findall(q(cname)):
                for node in cont:
                    if id(node) in tops:
                        dest.append(node)
        if not len(dest):
            block.remove(dest)

    # Heresy army-construction leftovers: the "(Compulsory)" label and Compulsory categories
    # (the Crusade chart's compulsory slots), and the requirement to have a Warlord (the
    # Warlord option stays, for missions with Slay the Warlord, but is not required).
    compulsory = {i for i, n in cats.items() if (n or "").startswith("Compulsory")}
    par = {c: p for p in block.iter() for c in p}
    dropped_mods = 0
    for m in [m for m in block.iter(q("modifier"))]:
        if (m.get("field") == "name" and "compulsory" in (m.get("value") or "").lower()) or \
                (m.get("field") == "category" and m.get("value") in compulsory):
            par[m].remove(m)
            dropped_mods += 1
    rep["compulsoryRulesRemoved"] = dropped_mods
    for el in block.iter():
        # "Master of the Legion" only lets a Praetor choose a Rite of War: not used.
        if lname(el.tag) in ("selectionEntry", "entryLink") and (el.get("name") or "").startswith("Master of the Legion"):
            el.set("hidden", "true")
            for x in [x for x in el if lname(x.tag) in ("modifiers", "modifierGroups", "constraints")]:
                el.remove(x)
            rep["masterOfTheLegionHidden"] = rep.get("masterOfTheLegionHidden", 0) + 1
        if lname(el.tag) in ("selectionEntry", "entryLink") and el.get("name") == "Warlord":
            cons = el.find(q("constraints"))
            for c in (list(cons) if cons is not None else []):
                if c.get("type") == "min":
                    cons.remove(c)
                    rep["warlordMinimumRemoved"] = rep.get("warlordMinimumRemoved", 0) + 1

    # Legion traits are not used (decision 2026-10-30), wherever the source attaches them:
    # the Legiones Astartes category, and some units and options that also link them.
    traits = set()
    if la_cat:
        # The traits are the category's rules hidden by default (shown per Legion); its other
        # links are general special rules granted under conditions (e.g. Hatred).
        traits = {l.get("targetId") for l in defined[la_cat].iter(q("infoLink"))
                  if l.get("hidden") == "true" and l.get("name") != LA_RULE}
    # By name too (some units link their own copy), except general special rules that
    # units may have for other reasons.
    trait_names = {defined[t].get("name") for t in traits if t in defined} - GENERAL_RULES
    traits |= {x.get("id") for x in block.iter(q("rule")) if x.get("name") in trait_names}
    par = {c: p for p in block.iter() for c in p}
    stripped = []
    for l in [x for x in block.iter(q("infoLink")) if x.get("targetId") in traits]:
        par[l].remove(l)
        stripped.append(defined[l.get("targetId")].get("name"))
    rep["legionTraitLinksRemoved"] = sorted(set(stripped))

    # Categories: slots -> Middlehammer sections; the Legiones Astartes category (Legion
    # traits) -> the Relics category; others copied.
    cat_map = {i: MH[SLOT[n]] for i, n in cats.items() if n in SLOT}
    if la_cat:
        cat_map[la_cat] = relic_cat
    used = {x.get(a) for x in block.iter() for a in ("targetId", "childId", "value", "scope") if x.get(a) in cats}
    entries = ET.SubElement(block, q("categoryEntries"))
    ce = ET.SubElement(entries, q("categoryEntry"), {"id": relic_cat, "name": RELIC_RULE_NAME, "hidden": "false"})
    il = ET.SubElement(ce, q("infoLinks"))
    ET.SubElement(il, q("infoLink"), {"id": relic_cat + "-rule", "name": RELIC_RULE_NAME, "hidden": "false",
                                      "targetId": relic_rule, "type": "rule"})
    ET.SubElement(il, q("infoLink"), {"id": relic_cat + "-la", "name": LA_RULE, "hidden": "false",
                                      "targetId": la_rule.get("id"), "type": "rule"})
    rules = block.find(q("sharedRules"))
    if rules is None:
        rules = ET.SubElement(block, q("sharedRules"))
    r = ET.SubElement(rules, q("rule"), {"id": relic_rule, "name": RELIC_RULE_NAME, "hidden": "false"})
    ET.SubElement(r, q("description")).text = RELIC_RULE_TEXT
    if la_rule.get("id") not in {x.get("id") for x in block.iter() if lname(x.tag) == "rule"}:
        rules.append(copy.deepcopy(la_rule))
    copied = []
    for i in sorted(used - set(cat_map)):
        node = copy.deepcopy(defined[i])
        for x in list(node):
            if lname(x.tag) in ("infoLinks", "modifiers", "constraints", "rules", "profiles"):
                node.remove(x)
        entries.append(node)
        copied.append(cats[i])
    rep["categoriesCopied"] = sorted(copied)

    for x in block.iter():
        for a in ("targetId", "childId", "value", "scope"):
            if x.get(a) in cat_map and (a != "value" or x.get("field") == "category"):
                x.set(a, cat_map[x.get(a)])
        if lname(x.tag) == "categoryLink" and x.get("targetId") in MH.values() and x.get("primary") == "true" \
                and x.get("id", "").endswith("-slot") is False:
            x.set("primary", "false")   # nested entries never take a slot of their own

    # Points, profiles, Warlord Traits.
    notes = set()
    hh_char_names = {c.get("id"): c.get("name") for c in hh_gst.iter(q("characteristicType"))}
    for x in block.iter():
        t = lname(x.tag)
        if t == "cost" and x.get("typeId") == "points":
            x.set("typeId", MH_POINTS)
            x.set("name", "Points")
        for attr in ("field", "childId", "typeId"):
            if x.get(attr) == "points":
                x.set(attr, MH_POINTS)
        if t == "profile":
            convert_profile(x, mh_types, notes, hh_char_names)
        if t in ("selectionEntry", "selectionEntryGroup", "entryLink") and \
                (x.get("name") or "").lower().startswith("warlord trait"):
            x.set("hidden", "true")
    # Modifiers on links to profiles (e.g. a weapon profile changed by an upgrade).
    by_id = {x.get("id"): x for x in block.iter() if lname(x.tag) == "profile"}
    renames = {v[0]: v[1] for v in PROFILE_MAP.values()}
    for link in [x for x in block.iter(q("infoLink")) if x.get("type") == "profile"]:
        target = by_id.get(link.get("targetId"))
        if target is None:
            continue
        new_ids = {ct.get("name"): ct.get("id") for ct in mh_types[target.get("typeId")].iter(q("characteristicType", GST_NS))}
        rename = renames.get(target.get("typeId"), {})
        for holder in [link] + link.findall(f"{q('modifierGroups')}/{q('modifierGroup')}"):
            mods = holder.find(q("modifiers"))
            for m in (list(mods) if mods is not None else []):
                name = hh_char_names.get(m.get("field"))
                if name is None:
                    continue
                name = rename.get(name, name)
                if name in new_ids and name not in ("HP", "Pg"):
                    m.set("field", new_ids[name])
                else:
                    mods.remove(m)
                    notes.add(f"{target.get('name')}: {name} modifier dropped")
    rep["profileNotes"] = sorted(notes)

    # Empty rule texts are filled as for 7th Edition lists: 5th Edition core first.
    rep["rulesText"] = fill_from(block, q, [("5th Ed core", core_5e()), ("same list", texts_of(block)),
                                            ("7th Ed lists", seventh_all())])

    # The source reuses IDs: keyword constraint IDs (as in 7th Edition data) and some
    # repeated links. Make them unique; links nothing refers to are simply renumbered.
    rep["legacyConstraintIdsReplaced"] = unique_constraint_ids(block)
    referenced = {x.get(a) for x in block.iter() for a in ("targetId", "childId", "scope", "field")}
    seen, renumbered = set(), 0
    for x in block.iter():
        i = x.get("id")
        if not i:
            continue
        if i in seen and i not in referenced:
            renumbered += 1
            x.set("id", f"{i}-d{renumbered}")
        seen.add(x.get("id"))
    rep["repeatedIdsRenumbered"] = renumbered

    # Prefix every ID defined in the block; references to Middlehammer IDs are untouched.
    own = {x.get("id") for x in block.iter() if x.get("id")} - {relic_cat, relic_rule}
    for x in block.iter():
        for a in ("id", "targetId", "childId", "scope", "field", "defaultSelectionEntryId"):
            v = x.get(a)
            if v in own and not v.startswith(prefix):
                x.set(a, prefix + v)
    unresolved = sorted({x.get("targetId") for x in block.iter() if x.get("targetId")}
                        - {x.get("id") for x in block.iter()} - set(MH.values()))
    if unresolved:
        par = {c: p for p in block.iter() for c in p}
        removed = []
        for x in [x for x in block.iter() if x.get("targetId") in unresolved]:
            par[x].remove(x)
            t = defined.get(x.get("targetId"))
            removed.append(f"{lname(x.tag)} {x.get('name') or ''} -> "
                           f"{(lname(t.tag) + ' ' + str(t.get('name'))) if t is not None else x.get('targetId')}")
        rep["brokenSourceLinksRemoved"] = sorted(set(removed))
    return block


def convert_relics(source, mh_gst, report):
    """{host faction: content block} for the Legiones Astartes list."""
    source = Path(source)
    mh_types = {pt.get("id"): pt for pt in mh_gst.iter(q("profileType", GST_NS))}
    rep = report.setdefault("relicsHH1", {})
    return {host: convert_for_host(source, mh_types, host, legions, rep.setdefault(host, {}))
            for host, legions in HOSTS.items()}


# ---------------------------------------------------------------- merge into factions

def _cond(kind, child, value="1", scope="force"):
    return {"type": kind, "value": value, "field": "selections", "scope": scope, "childId": child,
            "shared": "true", "includeChildSelections": "true", "includeChildForces": "false"}


def _hide_if(el, *conds, group=None):
    mods = el.find(q("modifiers"))
    if mods is None:
        mods = ET.Element(q("modifiers"))
        el.insert(0, mods)
    m = ET.SubElement(mods, q("modifier"), {"type": "set", "field": "hidden", "value": "true"})
    if group:
        cg = ET.SubElement(ET.SubElement(m, q("conditionGroups")), q("conditionGroup"), {"type": group})
        conds_el = ET.SubElement(cg, q("conditions"))
    else:
        conds_el = ET.SubElement(m, q("conditions"))
    for c in conds:
        ET.SubElement(conds_el, q("condition"), c)
    return mods


def toggle_entry(fid):
    """Configuration entry: tick the option to show Heresy units. Shown only when a 6th or
    7th Edition Army List is chosen."""
    sid, oid = f"{fid}-relics", f"{fid}-relics-on"
    entry = ET.Element(q("selectionEntry"), {"type": "upgrade", "import": "true", "name": TOGGLE_NAME,
                                             "hidden": "false", "id": sid, "collective": "false",
                                             "sortIndex": "2"})
    _hide_if(entry, _cond("lessThan", ERA_6_7))
    cons = ET.SubElement(entry, q("constraints"))
    ET.SubElement(cons, q("constraint"), {"type": "max", "value": "1", "field": "selections", "scope": "force",
                                          "shared": "true", "id": f"{sid}-max", "includeChildSelections": "false",
                                          "includeChildForces": "false"})
    ET.SubElement(ET.SubElement(entry, q("categoryLinks")), q("categoryLink"), {
        "name": "Configuration", "hidden": "false", "id": f"{sid}-cat", "targetId": CONFIGURATION,
        "primary": "true"})
    opt = ET.SubElement(ET.SubElement(entry, q("selectionEntries")), q("selectionEntry"), {
        "type": "upgrade", "import": "true", "name": TOGGLE_OPTION, "hidden": "false", "id": oid,
        "collective": "false"})
    ET.SubElement(ET.SubElement(opt, q("constraints")), q("constraint"), {
        "type": "max", "value": "1", "field": "selections", "scope": "parent", "shared": "true",
        "id": f"{oid}-max", "includeChildSelections": "false", "includeChildForces": "false"})
    for e in (entry, opt):
        ET.SubElement(ET.SubElement(e, q("costs")), q("cost"), {"name": "Points", "typeId": MH_POINTS, "value": "0"})
    return entry, oid


def add_relics(factions, blocks, report):
    """Put each host's Heresy block in its faction catalogue, behind the toggle."""
    done = {}
    for host, block in blocks.items():
        root = factions[host]
        fid = root.get("id")
        entry, oid = toggle_entry(fid)
        sels = root.find(q("selectionEntries"))
        sels.insert(1, entry)
        # Every "Hide super-heavies" option of the faction's lists (IDs carry list suffixes).
        switches = [e.get("id") for e in root.iter(q("selectionEntry"))
                    if (e.get("name") or "").startswith("Hide super-heavies")]
        n = 0
        for cont in ("selectionEntries", "entryLinks"):
            src = block.find(q(cont))
            dest = root.find(q(cont))
            if dest is None:
                dest = ET.SubElement(root, q(cont))
            for el in list(src if src is not None else []):
                mods = _hide_if(el, _cond("lessThan", oid))
                ET.SubElement(ET.SubElement(ET.SubElement(mods, q("modifier"), {
                    "type": "set", "field": "hidden", "value": "true"}), q("conditions")),
                    q("condition"), _cond("lessThan", ERA_6_7))
                slot = next((l.get("targetId") for l in el.iter(q("categoryLink")) if l.get("primary") == "true"), None)
                if slot == MH["Super-Heavy"] and switches:
                    _hide_if(el, *[_cond("atLeast", s) for s in switches], group="or")
                for c in el.findall(f"{q('constraints')}/{q('constraint')}"):
                    if c.get("type") == "min":
                        m = ET.SubElement(mods, q("modifier"), {"type": "set", "field": c.get("id"), "value": "0"})
                        ET.SubElement(ET.SubElement(m, q("conditions")), q("condition"), _cond("lessThan", oid))
                dest.append(el)
                n += 1
        for container in block:
            tag = lname(container.tag)
            if tag in ("selectionEntries", "entryLinks"):
                continue
            if tag in ("sharedSelectionEntries", "sharedSelectionEntryGroups"):
                # Force-wide minimums apply only with the toggle on (see merge_factions).
                for el in container.iter():
                    cons = el.find(q("constraints"))
                    for c in (list(cons) if cons is not None else []):
                        if c.get("type") == "min" and c.get("scope") in ("force", "roster") and \
                                float(c.get("value") or 0) > 0:
                            mods = el.find(q("modifiers"))
                            if mods is None:
                                mods = ET.Element(q("modifiers"))
                                el.insert(0, mods)
                            m = ET.SubElement(mods, q("modifier"), {"type": "set", "field": c.get("id"), "value": "0"})
                            ET.SubElement(ET.SubElement(m, q("conditions")), q("condition"), _cond("lessThan", oid))
            dest = root.find(q(tag))
            if dest is None:
                dest = ET.SubElement(root, q(tag))
            dest.extend(list(container))
        done[host] = {"units": n, "superHeavySwitches": len(switches)}
    report.setdefault("relicsHH1Merged", done)

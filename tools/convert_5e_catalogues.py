#!/usr/bin/env python3
"""Convert catalogues from the 5th Edition source (AnonymousCheese/WH40K5E) to Middlehammer.

The Middlehammer game system is built from this source's game system, so catalogues
only need retargeting plus content fixes:
  * homebrew: the source's "Hide Homebrew Units" switch is treated as permanently on;
    gated units are hidden and unlinked, and the switch is removed from the game system;
  * units from later editions that the source does not tag (EXCLUDED) are removed;
  * units the source wrongly tags as homebrew (RESTORED) are made available;
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
    "Space Wolves": {"Gladiator", "Repulsor"},
    "Tyranids": {"Exocrine Brood", "Maleceptor Brood"},
    "Chaos Space Marines": {"Khorne Lord of Skulls"},
    "Imperial Guard": {"Rogal Dorn Battle Tank", "Bullgryn Squad", "Field Ordnance Battery"},
}

# Only these lists have units behind the Apocalypse switch after exclusions; elsewhere the
# "Custom Content" entry would show a switch that does nothing, so it is removed.
APOCALYPSE_SWITCH_KEPT = {"Imperial Guard"}

# Units the source tags homebrew that are in the codex (Pyrovore: Codex Tyranids 2010).
RESTORED = {"Tyranids": {"Pyrovore Brood"}}


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
    cat.set("gameSystemId", MH_SYSTEM_ID)
    entry.update({"homebrewHidden": sorted(set(hidden)), "excluded": sorted(removed),
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

#!/usr/bin/env python3
"""Structural validation of every published Middlehammer catalogue against the GST.

Checks: game system ID/revision, catalogue ID uniqueness, duplicate IDs within a file,
every targetId/childId resolving through the catalogue, its imported catalogues
(recursively) and the GST, cost types defined in the GST, primary categories of root
entries being present in the force, and leftover "Homebrew" entries.
Structural only: it does not prove points or options match the printed codex.
"""
import collections
import json
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

ID_RE = re.compile(r"^[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}$")
L = lambda t: t.rsplit("}", 1)[-1]
# References that are deliberately left dangling, each always evaluating to "not present".
_allow = Path(__file__).with_name("validation-allowlist.json")
ALLOWED = set(json.loads(_allow.read_text())["ids"]) if _allow.exists() else set()

def main(root=Path(".")):
    gst = ET.parse(root / "Middlehammer-Unification.gst").getroot()
    gid = {e.get("id") for e in gst.iter() if e.get("id")}
    cost_types = {e.get("id") for e in gst.iter() if L(e.tag) == "costType"}
    force_cats = {l.get("targetId") for f in gst.iter() if L(f.tag) == "forceEntry"
                  for l in f.iter() if L(l.tag) == "categoryLink"}
    cats = {}
    for p in sorted(root.glob("*.cat")):
        c = ET.parse(p).getroot()
        if c.get("gameSystemId") != gst.get("id"):
            continue  # separate game system (e.g. 7th Edition test files)
        if c.get("id") in cats:
            print(f"ERROR duplicate catalogue id {c.get('id')}: {p.name}")
        cats[c.get("id")] = (p, c)
    errors = collections.defaultdict(list)
    def scope(cid, seen):
        seen.add(cid)
        c = cats[cid][1]
        out = {e.get("id"): e for e in c.iter() if e.get("id")}
        for l in c.iter():
            if L(l.tag) == "catalogueLink":
                t = l.get("targetId")
                if t not in cats:
                    errors[cats[cid][0].name].append(f"catalogueLink to missing catalogue {l.get('name')}")
                elif t not in seen:
                    out = {**scope(t, seen), **out}
        return out
    summary = []
    for cid, (p, c) in cats.items():
        if c.get("gameSystemRevision") != gst.get("revision"):
            errors[p.name].append(f"gameSystemRevision {c.get('gameSystemRevision')} != GST {gst.get('revision')}")
        own = [e.get("id") for e in c.iter() if e.get("id")]
        dups = [i for i, n in collections.Counter(own).items() if n > 1]
        if dups:
            errors[p.name].append(f"{len(dups)} duplicate IDs in file")
        known = set(scope(cid, set())) | gid | set(cats) | ALLOWED
        unresolved = set()
        for e in c.iter():
            for a in ("targetId", "childId"):
                v = e.get(a)
                if v and ID_RE.match(v) and v not in known:
                    unresolved.add(v)
        if unresolved:
            errors[p.name].append(f"{len(unresolved)} unresolved references e.g. {sorted(unresolved)[:3]}")
        bad_costs = {e.get("typeId") for e in c.iter() if L(e.tag) == "cost"} - cost_types
        if bad_costs:
            errors[p.name].append(f"undefined cost types {bad_costs}")
        hb = [e.get("name") for e in c.iter() if e.get("name") and "homebrew" in e.get("name").lower()
              and L(e.tag) in ("selectionEntry", "entryLink", "selectionEntryGroup")
              and e.get("hidden") != "true"]
        if hb:
            errors[p.name].append(f"homebrew-named entries remain: {hb[:5]}")
        # primary category of visible root entries must be in the force
        ids_in_scope = scope(cid, set()) | {e.get("id"): e for e in gst.iter() if e.get("id")}
        orphans = []
        for cont in ("selectionEntries", "entryLinks"):
            r = c.find("{*}" + cont)
            for e in (r if r is not None else []):
                if e.get("hidden") == "true":
                    continue
                prim = [l.get("targetId") for l in e.findall("{*}categoryLinks/{*}categoryLink") if l.get("primary") == "true"]
                if not prim and L(e.tag) == "entryLink" and e.get("targetId") in ids_in_scope:
                    t = ids_in_scope[e.get("targetId")]
                    prim = [l.get("targetId") for l in t.findall("{*}categoryLinks/{*}categoryLink") if l.get("primary") == "true"]
                if prim and prim[0] not in force_cats:
                    orphans.append(e.get("name"))
        if orphans:
            errors[p.name].append(f"{len(orphans)} root entries in a category the force does not show: {orphans[:4]}")
        summary.append((c.get("name"), c.get("revision")))
    print(f"{len(cats)} catalogues on {gst.get('name')} revision {gst.get('revision')}")
    for k, v in sorted(errors.items()):
        for msg in v:
            print(f"ERROR {k}: {msg}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")))

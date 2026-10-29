#!/usr/bin/env python3
"""Build every Middlehammer catalogue from the pinned upstream sources.

  python tools/build_middlehammer.py            # writes to the repository root

Steps: fetch pinned sources into upstream-cache/ (git), convert 3rd Edition
catalogues (tools/convert_3e_catalogues.py) and the 5th Edition Imperial Guard
2009 catalogue, merge everything into one catalogue per faction
(tools/merge_factions.py), then write the faction catalogues and game system.
Revisions are bumped only for files whose content changed. Middlehammer
catalogues at the root that are no longer produced are deleted.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent))
from convert_3e_catalogues import convert_3e  # noqa: E402
from merge_factions import build_factions     # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "upstream-cache"
GST_NS = "http://www.battlescribe.net/schema/gameSystemSchema"
CAT_NS = "http://www.battlescribe.net/schema/catalogueSchema"
MH_SYSTEM_ID = "sys-middlehammer-2026"
FIFTH_SOURCE_ID = "sys-9c90-407d-0876-14fb"
# Units in the 5e source catalogue that are not in the 2009 Codex: Imperial Guard.
GUARD_2009_EXCLUDED = {"Rogal Dorn Battle Tank", "Bullgryn Squad", "Field Ordnance Battery"}


def fetch(edition):
    info = json.loads((ROOT / "sources/upstreams.json").read_text())["editions"][str(edition)]
    dest = CACHE / info["repository"].split("/")[1]
    if not (dest / ".git").exists():
        subprocess.run(["git", "clone", "-q", f"https://github.com/{info['repository']}", str(dest)], check=True)
    head = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != info["commit"]:
        subprocess.run(["git", "-C", str(dest), "fetch", "-q", "origin", info["commit"]], check=True)
        subprocess.run(["git", "-C", str(dest), "checkout", "-q", info["commit"]], check=True)
    return dest


def convert_guard_2009(source_dir, report):
    tree = ET.parse(source_dir / "Imperial Guard.cat")
    root = tree.getroot()
    if root.get("gameSystemId") != FIFTH_SOURCE_ID:
        raise SystemExit("Unexpected 5e Imperial Guard game system")
    root.set("gameSystemId", MH_SYSTEM_ID)
    links = root.find(f"{{{CAT_NS}}}entryLinks")
    removed = [l.get("name") for l in list(links) if l.get("name") in GUARD_2009_EXCLUDED]
    for l in list(links):
        if l.get("name") in GUARD_2009_EXCLUDED:
            links.remove(l)
    if set(removed) != GUARD_2009_EXCLUDED:
        raise SystemExit(f"Guard 2009 exclusions not found: {GUARD_2009_EXCLUDED - set(removed)}")
    report["guard2009Excluded"] = sorted(removed)
    return root


def digest(root, ignore=("revision", "gameSystemRevision")):
    h = hashlib.sha256()
    for el in root.iter():
        attrs = sorted((k, v) for k, v in el.attrib.items() if not (el is root and k in ignore))
        h.update(repr((el.tag, attrs, (el.text or "").strip())).encode())
    return h.hexdigest()


def write(root, path, ns, rev_attr_extra=None):
    """Write root to path, keeping the old revision if content is unchanged."""
    old_rev, changed = 0, True
    if path.exists():
        old = ET.parse(path).getroot()
        old_rev = int(old.get("revision") or 0)
        changed = digest(old) != digest(root) or (rev_attr_extra and old.get("gameSystemRevision") != rev_attr_extra)
    root.set("revision", str(old_rev + 1 if changed else old_rev))
    if rev_attr_extra:
        root.set("gameSystemRevision", rev_attr_extra)
    ET.register_namespace("", ns)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return changed


def main():
    report = {}
    third, fifth = fetch(3), fetch(5)
    gst_path = ROOT / "Middlehammer-Unification.gst"
    ET.register_namespace("", GST_NS)
    gst = ET.parse(gst_path).getroot()
    before = digest(gst)

    trees = convert_3e(third, gst, report)
    members = {(3, e["sourceName"]): t.getroot() for _, t, e in trees.values()}
    members[(5, "Imperial Guard")] = convert_guard_2009(fifth, report)
    factions = build_factions(members, MH_SYSTEM_ID, report)

    gst_changed = digest(gst) != before
    gst.set("revision", str(int(gst.get("revision")) + (1 if gst_changed else 0)))
    ET.register_namespace("", GST_NS)
    ET.ElementTree(gst).write(gst_path, encoding="utf-8", xml_declaration=True)
    gst_rev = gst.get("revision")

    written = set()
    for name, root in factions.items():
        path = ROOT / f"{name}.cat"
        write(root, path, CAT_NS, gst_rev)
        written.add(path.name)
    removed = []
    for p in sorted(ROOT.glob("*.cat")):
        if p.name not in written and ET.parse(p).getroot().get("gameSystemId") == MH_SYSTEM_ID:
            p.unlink()
            removed.append(p.name)
    report["removedFiles"] = removed
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build/middlehammer-build-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(factions)} faction catalogues; game system revision {gst_rev}"
          f"{' (changed)' if gst_changed else ''}; removed {len(removed)} old files")


if __name__ == "__main__":
    main()

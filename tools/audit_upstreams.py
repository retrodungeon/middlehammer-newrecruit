#!/usr/bin/env python3
"""Inventory plain and archived BattleScribe data without modifying upstream files.

Usage: python tools/audit_upstreams.py upstream-cache --json build/audit.json
"""
import argparse
import collections
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

EXTENSIONS = {".cat", ".gst", ".catz", ".gstz", ".bsr", ".zip"}

def entries(path):
    if path.is_dir():
        for item in sorted(path.rglob("*")):
            if item.is_file() and item.suffix.lower() in EXTENSIONS:
                yield from entries(item)
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if member.is_dir() or member.file_size > 30_000_000:
                    continue
                if Path(member.filename).suffix.lower() not in {".cat", ".gst", ".catz", ".gstz"}:
                    continue
                data = archive.read(member)
                if zipfile.is_zipfile(io.BytesIO(data)):
                    with zipfile.ZipFile(io.BytesIO(data)) as inner:
                        for sub in inner.namelist():
                            if sub.lower().endswith((".cat", ".gst")):
                                yield f"{path}:{member.filename}:{sub}", inner.read(sub)
                else:
                    yield f"{path}:{member.filename}", data
    elif path.suffix.lower() in {".cat", ".gst"}:
        yield str(path), path.read_bytes()

def inspect(filename, data):
    root = ET.fromstring(data)
    kind = root.tag.rsplit("}", 1)[-1]
    if kind not in {"catalogue", "gameSystem"}:
        return None
    counts = collections.Counter(e.tag.rsplit("}", 1)[-1] for e in root.iter())
    ids = {e.get("id") for e in root.iter() if e.get("id")}
    targets = {e.get("targetId") for e in root.iter() if e.get("targetId")}
    return {
        "file": filename, "kind": kind, "name": root.get("name"),
        "id": root.get("id"), "gameSystemId": root.get("gameSystemId"),
        "revision": root.get("revision"),
        "profileTypes": counts["profileType"],
        "selectionEntries": counts["selectionEntry"],
        "categories": counts["categoryEntry"],
        "links": counts["infoLink"] + counts["selectionEntryLink"],
        "distinctTargetIds": len(targets),
        "targetsNotDefinedInSameFile": len(targets - ids),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    found, errors = [], []
    for filename, data in entries(args.path):
        try:
            record = inspect(filename, data)
            if record:
                found.append(record)
        except (ET.ParseError, ValueError, zipfile.BadZipFile) as exc:
            errors.append({"file": filename, "error": str(exc)})
    groups = collections.defaultdict(lambda: {"gameSystems": 0, "catalogues": 0})
    for item in found:
        group = groups[item["gameSystemId"] or item["id"]]
        group["gameSystems" if item["kind"] == "gameSystem" else "catalogues"] += 1
    report = {
        "files": len(found), "gameSystems": sum(x["kind"] == "gameSystem" for x in found),
        "catalogues": sum(x["kind"] == "catalogue" for x in found),
        "systems": dict(groups), "entries": found, "errors": errors,
    }
    print(json.dumps({k: v for k, v in report.items() if k != "entries"}, indent=2))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()

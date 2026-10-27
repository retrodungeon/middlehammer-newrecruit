#!/usr/bin/env python3
"""Build a faithful 5e-based Middlehammer GST from a locally downloaded upstream.

This is an *intermediate build artifact*, not a validated playable release.
Preserves all internal IDs and references from the upstream GST; changes only
the root game-system identity, name, revision, and adds provenance comment.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

NS = "http://www.battlescribe.net/schema/gameSystemSchema"
ET.register_namespace("", NS)
MIDDLEHAMMER_ID = "sys-middlehammer-2026"
UPSTREAM_ID = "sys-9c90-407d-0876-14fb"

def build(source: Path, destination: Path):
    tree = ET.parse(source)
    root = tree.getroot()
    if root.tag != f"{{{NS}}}gameSystem":
        raise ValueError("Input is not a BattleScribe gameSystem XML")
    if root.get("id") != UPSTREAM_ID:
        raise ValueError(f"Unexpected 5e upstream system ID: {root.get('id')}")
    root.set("id", MIDDLEHAMMER_ID)
    root.set("name", "Middlehammer Unification (5e foundation — development)")
    root.set("revision", "1")
    note = ET.Element(f"{{{NS}}}comment")
    note.text = ("Generated from AnonymousCheese/WH40K5E. Original definitions "
                 "preserved; Middlehammer rules and cross-edition conversion NOT yet applied.")
    previous = root.find(f"{{{NS}}}comment")
    if previous is not None:
        root.remove(previous)
    root.insert(0, note)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding="utf-8", xml_declaration=True)
    parsed = ET.parse(destination).getroot()
    assert parsed.get("id") == MIDDLEHAMMER_ID
    print(f"Generated {destination} ({destination.stat().st_size} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    build(args.source, args.destination)

# Middlehammer data architecture

## Goal

A single Middlehammer New Recruit/BattleScribe game system with edition- and publication-specific army catalogues (3rd–7th), adapted to the Unification Patch.

## Workflow

1. Record immutable upstream commit SHA or release tag in `sources/upstreams.json` before importing.
2. Retrieve original upstreams into a **local, ignored** `upstream-cache/` for analysis; do not overwrite upstream originals.
3. Inventory catalogue IDs, game-system IDs, profile and category definitions, dependencies, and reference targets.
4. Normalize imported data to a unified system; preserve a mapping from original IDs to converted IDs.
5. Apply explicit Middlehammer overrides separately from the imported source data.
6. Generate `.gst` and `.cat` files at repository root only after validation and redistribution review.
7. Test army creation, point totals, selections and restrictions in New Recruit.

## Current state

As of 2026-10-29:

- One build (`tools/build_middlehammer.py`) produces the game system and every faction catalogue from the sources pinned in `sources/upstreams.json`; CI checks the committed files equal a fresh build.
- `Middlehammer-Unification.gst` is based on the 5th Edition source game system, with the standard 5e Force Organization Chart and the 3rd Edition definitions that converted lists need.
- Catalogues are one per faction; each codex or variant list is an option of the faction's required "Army List" entry (`tools/merge_factions.py`).
- Converted: every official list in the 3rd, 5th and 7th Edition sources, and the 4th Edition books not available elsewhere. 6th Edition: pilot (Tau Empire 2013).
- Redistribution rights remain unconfirmed; the data is published for a small play group.

## Naming

Catalogues are named by faction, using the most common name across 3rd–7th Edition. Army List options carry the book's edition and year, e.g. "4th Ed – Codex: Eldar (2006)". Upstream data is never modified in place; all changes are made by the build.

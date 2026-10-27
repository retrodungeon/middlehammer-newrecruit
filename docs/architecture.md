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

- 6th and 7th Edition BSData sources accepted, though the 6th Edition archive has not been extracted.
- 3rd–5th Edition independently maintained sources accepted as **provisional accuracy baselines**.
- No upstream catalogue files have yet been copied or published.
- Redistribution rights remain unverified. Public GitHub access alone is not a license.
- New Recruit importability remains untested.

## Naming

Catalogue names must include edition and, where relevant, codex publication year to distinguish overlapping books. Avoid modifying upstream data in place.

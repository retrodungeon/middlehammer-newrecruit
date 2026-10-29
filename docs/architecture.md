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

- `Middlehammer-Unification.gst` is built from the 5th Edition source game system and carries the standard 5e Force Organization Chart.
- Two converted catalogues are published and tested in New Recruit: Imperial Guard (5th Edition, 2009) and Chaos Space Marines (3rd Edition, 2002).
- The 6th Edition archive (BSData release v3.1.4) is extracted in CI; the 2013 Space Marines conversion is experimental and unpublished.
- Unmodified BSData 7th Edition files (`Warhammer 40,000 (7th Edition).gst`, `Space Marines (7th Edition, 2015).cat`) sit at the repository root as a separate game system for an import test.
- 3rd–5th Edition independently maintained sources are **provisional accuracy baselines**.
- Redistribution rights remain unverified. Public GitHub access alone is not a licence. Note that step 6 of the workflow above was not followed for the two published catalogues.

## Naming

Catalogue names must include edition and, where relevant, codex publication year to distinguish overlapping books. Avoid modifying upstream data in place.

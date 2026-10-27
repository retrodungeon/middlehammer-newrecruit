# Middlehammer — New Recruit Game Data

Community project to implement **The Book of the Unification** (Middlehammer) as a New Recruit-compatible game system, supporting Warhammer 40,000 codexes from 3rd through 7th editions.

## Status

**Early development — not yet importable into New Recruit.** The game system and catalogue files have not yet been created or validated.

## Rules baseline

The Book of the Unification v1.7.2 uses Warhammer 40,000 5th Edition as its baseline, with cross-edition adjustments and codex-specific restrictions. The project will encode army-building constraints based on that patch, rather than assume all original codex options are legal.

## Planned data layout

- `game-system/` — New Recruit/BattleScribe `.gst` game system definition.
- `catalogues/` — edition-specific faction `.cat` files.
- `shared/` — reusable data definitions and templates where supported.
- `docs/` — implementation decisions, coverage, and validation notes.
- `tests/` — sample rosters and expected legality checks.

## Sources

- The Book of the Unification v1.7.2 (Middlehammer Resources, Google Drive)
- Middlehammer Mission Pack v1.4.1
- Codexes and supporting resources from the Middlehammer Resources collection

The original books and source documents are **not** mirrored in this repository. Game data should be authored with care for copyright and attribution.

## Roadmap

1. Extract force-organization and codex restriction rules from the patch.
2. Build a minimal, schema-valid `.gst` and test importing it.
3. Implement one pilot codex and validate army-building behavior.
4. Add edition-specific codexes incrementally, with regression tests.

## Disclaimer

Unofficial fan project. Not affiliated with or endorsed by Games Workshop or New Recruit.

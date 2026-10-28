# Space Marines (7th Edition, 2015) — isolated source import

Status: **source staged; New Recruit runtime validation pending**.

## Imported files
- `sources/bsdata-7e/Space Marines - Codex (2015).cat` — BSData revision 2046, BattleScribe 2.00.
- `sources/bsdata-7e/Warhammer40K.gst` — BSData revision 2038, BattleScribe 2.00.
- Both taken from upstream commit `8dcdb43a0f6d7f32b9874993fcdf17c260f90795` (2017-04-11).
- Upstream: https://github.com/BSData/wh40k-7th-edition

## Intended migration
1. Test the **pair** of staged files in New Recruit. The catalogue references the imported 7th Edition GST ID `e1ebd931-a209-3ce4-87b4-d9918d25530b`, **not** the Middlehammer GST. A raw catalogue-only import is not a Middlehammer integration.
2. Once source validity is confirmed, clone the catalogue under a new unique catalogue ID and remap its game-system reference and category/profile dependencies to Middlehammer's existing GST.
3. Compare units, points, options and restrictions against **Codex: Space Marines (2013)** in the user's 6th Edition Google Drive folder (file ID `15WKhoBZNPh_paK2cgpoz1oTaNPOM9d8z`).
4. Remove post-2013 formations and units, adapt 2013 rules to Book of Unification 5th Edition baseline, and test legality.

## Important
This is a **reference/source snapshot**, not a claim that the 2015 rules are accurate for the 2013 codex, or that New Recruit can already import the Middlehammer variant. Do not publish it as the 6th Edition faction until checks pass. Existing Imperial Guard and Chaos Space Marines work is unchanged.

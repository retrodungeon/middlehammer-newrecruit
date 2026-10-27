# Upstream compatibility matrix — audit run 40560759181

Audit date: 2026-10-27. Source: [successful GitHub Actions run](https://github.com/retrodungeon/middlehammer-newrecruit/actions/runs/40560759181), artifact `middlehammer-upstream-audit`.

| Edition | Source | GST ID | GSTs | Catalogues | XML parsing |
|---|---|---|---:|---:|---|
| 3rd | KSnyder1986/Warhammer-40k-3rd-Edition | `96e2-b781-50d7-3d18` | 1 | 63 | Passed |
| 4th | Kothra/Warhammer-40-000-4th-Edition-for-NewRecruit | `sys-b41a-8226-286b-0dea` | 1 | 13 | Passed |
| 5th | AnonymousCheese/WH40K5E | `sys-9c90-407d-0876-14fb` | 1 | 22 | Passed |
| 6th | BSData/wh40k-7th-edition release v3.1.4 | `3d1a4963-0629-4025-a90b-76ab3d63c5c5` | 1 | 40 | Passed |
| 7th | BSData/wh40k-7th-edition | `e1ebd931-a209-3ce4-87b4-d9918d25530b` | 1 | 44 | Passed |
| **Total** | | | **5** | **182** | **187/187 parsed** |

## Interpretation

All five sources are syntactically readable XML. None of their game-system IDs match, so original catalogues cannot be used unchanged with a new unified game system. Out-of-file target references are expected in BattleScribe and **must not** be counted as broken references without checking shared definitions and imports.

This is a **structural inventory**, not proof of catalogue correctness, cross-file reference resolution, valid army construction, redistribution permission, or New Recruit importability.

## Conversion strategy

1. Use 5th Edition as the rules and profile-type design reference.
2. Assign a new Middlehammer system ID and preserve an explicit mapping from each upstream system ID.
3. Reconcile profile types, cost types, force entries and category IDs before converting any catalogue.
4. Convert one 5th Edition catalogue and one 3rd Edition catalogue as a test.
5. Apply Unification Patch restrictions as separate, auditable transformations.

## Publication policy

The generated Middlehammer system will initially contain only independently authored structural definitions. Existing upstream rule text and complete catalogue contents will not be copied into the public repository until redistribution permissions are reviewed.

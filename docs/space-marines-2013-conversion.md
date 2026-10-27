# Space Marines (6th Edition, 2013) conversion contract

## Authority and precedence
1. **The Book of the Unification v1.7.2** overrides conflicting edition rules.
2. **2013 Codex: Space Marines** governs unit options, chapter tactics, costs and codex-specific army restrictions.
3. **6th Edition** supplies other edition-specific rules where not overridden.
4. **5th Edition** supplies the Middlehammer core and standard Force Organization Chart.

## Standard Force Organization Chart (5e, page 87)
- HQ: 1–2
- Troops: 2–6
- Elites: 0–3
- Fast Attack: 0–3
- Heavy Support: 0–3

The roster must use the existing `mh-test-force` force entry in `Middlehammer-Unification.gst` rather than introducing a 6e detachment. No Allied Detachments, no Formations, no Command Benefits. Preserve any permitted codex-specific detachments only if their restrictions can be implemented faithfully, without Command Benefits.

## Lords of War and super-heavies
Follow the Unification amendments, not generic 6e detachment behavior. Independent-character Lords of War count as HQ, other non-super-heavy Lords of War as Heavy Support, and super-heavies are subject to the special one-per-detachment allowance and the no-super-heavies-at-1500-or-less rule unless both players agree. Do not silently make them legal without the applicable constraints.

## Legacy source migration
The archived v3.1.4 6e dataset uses BattleScribe 1.14b (`entries`, `links`, `sharedEntries`, `sharedEntryGroups`, `forceTypes`) rather than the modern 2.03 catalogue schema. An XML attribute replacement is not sufficient.

**Gate before publication:**
- Inspect original legacy entry, group, link and force semantics.
- Preserve every unit's cost, size, option groups, min/max and conditional restrictions; explicitly report unsupported constructs.
- Translate legacy identifiers and references; validate against the *committed* Middlehammer GST.
- Confirm HQ/Troops/Elites/Fast Attack/Heavy Support population and selection legality in New Recruit.
- Keep 2009 Guard and 2002 Chaos files untouched.

Do not publish an incomplete conversion as a fully functional codex. Use a separate experimental file or artifact until tests pass.

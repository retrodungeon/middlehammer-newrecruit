# Unification rules ledger

Tracks which army-building rules from **The Book of the Unification v1.7.2** and the **Middlehammer Mission Pack v1.4.1** are enforced in this data. Page numbers are the printed page numbers in each PDF.

Most of the Unification changes how the game is played (wound allocation, vehicle damage, cover, psychic powers, special rules). Those are outside the scope of a list builder and are not tracked here unless they affect what can be put in a list.

## Enforced and tested

| Rule | Source | How it is implemented | Tested |
|---|---|---|---|
| Standard 5th Edition Force Organization Chart: HQ 1–2, Troops 2–6, Elites 0–3, Fast Attack 0–3, Heavy Support 0–3 | Unification p. 8, "The Force Organization Chart" (refers to 5e rulebook p. 87) | Force entry `mh-test-force` in `Middlehammer-Unification.gst` with min/max constraints. Dedicated Transport, Unique, Super-Heavy, Configuration and No Force Org Slot are also linked, without limits (as in the 5th Edition source). | Slot limits: yes — New Recruit, 2026-10-29. Extra sections: not yet |
| Forge World / Imperial Armour, White Dwarf and Chapter Approved content allowed; homebrew excluded | Maintainer policy, 2026-10-29 | 3rd Edition converter unlocks content behind the source's Imperial Armour toggle and hides content behind its Homebrew toggle or named "(Homebrew)" | Not yet |

## Enforced by conversion (7th Edition lists)

| Rule | Source | Implementation |
|---|---|---|
| No Allied Detachments; codex detachments allowed but Command Benefits ignored | Unification p. 9 | All 7th Edition detachments are removed and the standard chart is used. Codex detachments for lists that need them are pending. |
| No Formations | Unification p. 9 | Formation, Battle Formation, Decurion-style and Flyer Wing entries removed; formation-only options never apply. |
| No Warlord Traits | Unification p. 10 | Warlord Trait entries hidden. |
| Lords of War: independent characters → HQ; super-heavies → super-heavy allowance; others → Heavy Support | Unification p. 10 | Applied per unit from its profile (unit type, or 9+ Hull Points for super-heavy). |
| Castellans of the Imperium detachment patched out | Unification p. 13 | Removed with all other detachments. |
| Super-heavies only by agreement | Unification p. 8 | "Hide super-heavies" switch, on by default. Not points-aware. |

## Not yet enforced

| Rule | Source | Notes on enforceability |
|---|---|---|
| Allies only within the same era: 3rd–5th with 3rd–5th, 6th–7th with 6th–7th | Unification p. 8 | 3rd Edition ally force types (Daemon Hunters, Witch Hunters, Harlequins, Assassins, Kroot, Arbites) are published and are all within the 3rd–5th era. Cross-era blocking is needed once 6th/7th Edition lists exist. |
| Super-heavies and Gargantuan Creatures not allowed at 1500 points or less **unless both players agree** | Unification p. 8 | Partly: Imperial Guard 5th Ed keeps the source's "Hide Apocalypse Units" switch (on by default), which acts as the players' agreement toggle for its super-heavies. Not points-aware, and not yet applied to other lists' super-heavies. |
| Above 1500 points, a codex with no super-heavy of its own may take one from its faction's 3rd–7th Edition Imperial Armour books without using a slot (not for codexes that cannot use a normal Force Organization Chart) | Unification p. 8 | Requires Imperial Armour data, which is not in the project. |
| 6th/7th Edition Imperium or Chaos codexes may take an Imperial Knight or Renegade Knight as their Lord of War | Unification p. 8 | Requires Knight data and cross-catalogue links. |
| Ynnari Strength from Death: one Soulburst action per turn in total | Unification p. 13 | In-game rule; at most a rules-text note. |
| Supporting Units: infantry not taken as Troops, HQ or Lord of War score objectives with restrictions; 6th/7th Edition Imperial Knights units count as Supporting Units in an army made only of those publications | Mission Pack p. 7 | Scoring rule, not a list restriction. Could be shown as a rule note on affected units. |

## In-game rules that touch list data

These do not restrict list building but may appear in unit profiles or rules text in 6th/7th Edition catalogues:

- No Hull Points (Unification p. 9); super-heavies use Structure Points equal to 1/3 of their Hull Points (p. 10).
- Melee weapon AP: AP 1–3 count as power weapons, AP 4 gives −1 to armour saves, AP 5, 6 and "–" are ignored (p. 10).
- Psykers: Mastery Level sets powers known; they cast Mastery Level −1 powers per turn (minimum 1) and choose powers (p. 10).
- No Warp Charge (p. 9).
- 2+ invulnerable saves cannot be rerolled and no invulnerable save can be improved past 3+ (p. 8).

## Known accuracy issues

- In the 5th Edition source, special characters such as Lord Castellan Creed have "Unique" as their primary category, so they do not count against HQ/Elites slots. This matches the source data, not necessarily the codex.
- "Counts as Troops" units unlocked by characters (5th Edition source lists; Space Wolves, Dark Eldar, Grey Knights, Space Marines 2008, Orks 2008) are revealed in the Troops section when the unlocking character is taken. Orks: each Warboss allows one Nobz **or** Meganobz mob as Troops, but the data limits each to one per Warboss separately, so a Warboss could take one of each. Check this by hand.

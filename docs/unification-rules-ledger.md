# Unification rules ledger

Tracks which army-building rules from **The Book of the Unification v1.7.2** and the **Middlehammer Mission Pack v1.4.1** are enforced in this data. Page numbers are the printed page numbers in each PDF.

Most of the Unification changes how the game is played (wound allocation, vehicle damage, cover, psychic powers, special rules). Those are outside the scope of a list builder and are not tracked here unless they affect what can be put in a list.

## Enforced and tested

| Rule | Source | How it is implemented | Tested |
|---|---|---|---|
| Standard 5th Edition Force Organization Chart: HQ 1–2, Troops 2–6, Elites 0–3, Fast Attack 0–3, Heavy Support 0–3 | Unification p. 8, "The Force Organization Chart" (refers to 5e rulebook p. 87) | Force entry `mh-test-force` in `Middlehammer-Unification.gst` with min/max constraints | Yes — New Recruit, 2026-10-29 |

## Satisfied by omission (not actively enforced)

These are currently true only because the relevant units or detachments have not been converted. Each new 6th/7th Edition catalogue must be checked against them.

| Rule | Source | Notes |
|---|---|---|
| No Allied Detachments | Unification p. 9 | The 6e Space Marines translator drops the Allied Detachment entry (`excluded_allied_detachment`). |
| No Formations | Unification p. 9 | No formations exist in any published catalogue. |
| Codex-specific detachments allowed, but Command Benefits ignored | Unification p. 9 | No 6th/7th Edition detachments are published yet. |
| No Warlord Traits | Unification p. 10 | No 6th/7th Edition catalogues are published yet. |

## Not yet enforced

| Rule | Source | Notes on enforceability |
|---|---|---|
| Allies only within the same era: 3rd–5th with 3rd–5th, 6th–7th with 6th–7th | Unification p. 8 | Needs an edition/era tag on every catalogue and a constraint on any ally mechanism. Only relevant once a published codex offers allies. |
| Super-heavies and Gargantuan Creatures not allowed at 1500 points or less **unless both players agree** | Unification p. 8 | New Recruit cannot model "both players agree". Likely implementation: a warning or a toggle, not a hard block. |
| Above 1500 points, a codex with no super-heavy of its own may take one from its faction's 3rd–7th Edition Imperial Armour books without using a slot (not for codexes that cannot use a normal Force Organization Chart) | Unification p. 8 | Requires Imperial Armour data, which is not in the project. |
| 6th/7th Edition Imperium or Chaos codexes may take an Imperial Knight or Renegade Knight as their Lord of War | Unification p. 8 | Requires Knight data and cross-catalogue links. |
| Lords of War: independent characters count as HQ; a super-heavy is the one per detachment and uses no slot; anything else is Heavy Support (unless the detachment has a Lord of War slot) | Unification p. 10 | Category remapping during 6th/7th Edition conversion. Not needed for the current 3rd/5th Edition catalogues. |
| Castellans of the Imperium Detachment (Gathering Storm: Fall of Cadia) may not be used | Unification p. 13, "Patched Out" list | Exclude when/if that publication is converted. |
| Ynnari Strength from Death: one Soulburst action per turn in total | Unification p. 13 | In-game rule; at most a rules-text note. |
| Supporting Units: infantry not taken as Troops, HQ or Lord of War score objectives with restrictions; 6th/7th Edition Imperial Knights units count as Supporting Units in an army made only of those publications | Mission Pack p. 7 | Scoring rule, not a list restriction. Could be shown as a rule note on affected units. |

## In-game rules that touch list data

These do not restrict list building but may appear in unit profiles or rules text in 6th/7th Edition catalogues:

- No Hull Points (Unification p. 9); super-heavies use Structure Points equal to 1/3 of their Hull Points (p. 10).
- Melee weapon AP: AP 1–3 count as power weapons, AP 4 gives −1 to armour saves, AP 5, 6 and "–" are ignored (p. 10).
- Psykers: Mastery Level sets powers known; they cast Mastery Level −1 powers per turn (minimum 1) and choose powers (p. 10).
- No Warp Charge (p. 9).
- 2+ invulnerable saves cannot be rerolled and no invulnerable save can be improved past 3+ (p. 8).

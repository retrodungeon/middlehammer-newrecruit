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
| No Allied Detachments; codex detachments allowed but Command Benefits ignored | Unification p. 9 | The standard chart is used for every list. The ten smaller lists (Imperial and Renegade Knights, Inquisition, Assassins, Sisters of Silence, Legion of the Damned, Astra Telepathica, Aeronautica Imperialis, Haemonculus Covens) also keep their codex detachments as extra force types, with slot limits only; all detachment special rules are dropped. Other 7th Edition detachments are removed. The detachment limit of the game is not enforced. |
| No Formations | Unification p. 9 | Formation, Battle Formation, Decurion-style and Flyer Wing entries removed; formation-only options never apply. |
| No Warlord Traits | Unification p. 10 | Warlord Trait entries hidden. |
| Lords of War: independent characters → HQ; super-heavies → super-heavy allowance; others → Heavy Support | Unification p. 10 | Applied per unit from its profile (unit type, or 9+ Hull Points for super-heavy). |
| Castellans of the Imperium detachment patched out | Unification p. 13 | Removed with all other detachments. |
| Super-heavies only by agreement | Unification p. 8 | "Hide super-heavies" switch, on by default. Not points-aware. |

## Army construction decisions

| Rule | Source | Implementation |
|---|---|---|
| Lists that cannot fill the standard chart (no HQ or no Troops choice) are fielded only through their own force types | Unification p. 8 (standard chart needs the compulsory HQ and Troops, 5th Ed rulebook p. 87); decision 2026-10-29 | Their Army List option is hidden in the standard force: 3rd Ed Codex Assassins and Harlequins (ally attachments), and 7th Ed Inquisition, Officio Assassinorum, Sisters of Silence, Legion of the Damned, Imperial and Renegade Knights, Astra Telepathica, Aeronautica Imperialis and Haemonculus Covens (codex detachments). Ally attachments are subject to the same-era rule below. |
| Allies only within the same era: 3rd–5th with 3rd–5th, 6th–7th with 6th–7th | Unification p. 8 | Every Army List option carries an era category (by book edition). The ally force types (Adeptus Arbites Allies, Assassin Attachment, Daemon Hunter Allies, Harlequin Allies, Kroot Auxiliaries, Witch Hunter Allies, all 3rd Edition) show an error on their Army List when the roster also contains a 6th–7th Edition list. Not yet tested in New Recruit. Does not cover codex detachments, which are separate armies (author question 2). |

## Questions for the Unification author

1. Which 6th/7th Edition detachment special rules are Command Benefits (ignored) and which still apply? Psykana Division: Empyric Link; Imperial Navy Section: Air Superiority; Null-Maiden Task Force: Nauseating Aura, Rite of Annulment; Spectral Host: Saviours from Beyond. All are currently dropped.
2. In an agreed multi-detachment game, may detachments come from different eras (e.g. a 3rd Ed Imperial Guard army plus a 7th Ed Psykana Division), or does the same-era rule for allies apply?
3. 7th Ed Fallen Angels has no Troops, no detachment of its own, and its Formations and allied use are banned. Can it be fielded at all? It is currently offered on the standard chart, where it cannot be legal.

## Not yet enforced

| Rule | Source | Notes on enforceability |
|---|---|---|
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

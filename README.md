# Middlehammer — New Recruit Game Data

Unofficial community data for playing **The Book of the Unification** (Middlehammer) in [New Recruit](https://www.newrecruit.eu/). The Unification uses Warhammer 40,000 5th Edition as its core rules and lets codexes from 3rd through 7th Edition be used together. This data builds army lists under those rules.

**Status: playtest.** 132 army lists across 27 factions are converted and pass the structural checks. Faction selection, Army List selection and the Force Organization Chart have been tested in New Recruit; most individual lists have not yet been played through. Reports of errors are the most useful thing right now — see [Reporting problems](#reporting-problems).

## Installing in New Recruit

<!-- Maintainer: confirm the menu wording in step 1 against New Recruit before sharing. -->

1. In New Recruit, add a game system from a GitHub repository and give it this repository: `https://github.com/retrodungeon/middlehammer-newrecruit`
2. Choose the **Middlehammer Unification** game system.
3. Create a list and pick a faction (Space Marines, Imperial Guard, Eldar…).
4. Open the **Army List** entry in the **Configuration** section and choose the codex or variant list, e.g. "3rd Ed – Codex: Imperial Guard (1999)" or "5th Ed – Codex: Imperial Guard (2009)". Only that list's units are then shown.

You still need the Book of the Unification v1.7.2 and the Middlehammer Mission Pack v1.4.1 to play. You do not need the codexes at the table: unit rules text is included in the data.

## What's included

| Edition (of the book) | Army lists | Notes |
|---|---:|---|
| 3rd | 56 | Every official list in the 3rd Edition source, including Chapter Approved, White Dwarf, Citadel Journal, campaign and Imperial Armour lists |
| 4th | 10 | Seven from the 5th Edition source; Space Marines (2004), Tyranids (2005) and Blood Angels (2007) from the 4th Edition source |
| 5th | 9 | Including Imperial Guard (2009) |
| 6th | 25 | Space Marines (2013) with Clan Raukaan, Sentinels of Terra, Siege Assault Vanguard, Tyrant's Legion and Legion of the Damned; Dark Angels (2013); Astra Militarum, Militarum Tempestus and three Forge World Guard lists; Chaos Space Marines (2012) with Black Legion and Crimson Slaughter; Chaos Daemons (2013); Eldar (2013) with Iyanden; Dread Mob; Tyranids (2014); Dark Harvest; Tau Empire (2013) with Farsight Enclaves; Adepta Sororitas; Inquisition |
| 7th | 32 | The 7th Edition source's lists, less those whose book is 6th Edition (labelled 6th Ed above) and Fallen Angels (Formation only) |

Each list is labelled with the edition and year of the book it comes from. The full list of factions and options is in [`docs/codex-coverage.md`](docs/codex-coverage.md).

**Content policy:** all official material is included — Forge World / Imperial Armour, White Dwarf, Chapter Approved and campaign books. Homebrew is excluded, as are homebrew units inside official lists.

**Imperial Armour: The Badab War.** The 22 Badab War characters from Forge World's 6th Edition update are HQ choices in Codex: Space Marines (2013) and the Siege Assault Vanguard. Captain Mordaci Blaylock (IA9) is in Codex: Space Marines (2008). Further Imperial Armour 9 and 10 entries are being transcribed from the books.

**Points and options** come from the community source data (see [Sources](#sources)) with corrections where checked. They have not been checked line by line against the printed books.

## Unification rules applied to list building

- **Force Organization Chart:** one standard chart, HQ 1–2, Troops 2–6, Elites 0–3, Fast Attack 0–3, Heavy Support 0–3 (5th Edition rulebook p. 87). Some lists add their own force types (Daemon Hunter and Witch Hunter allies, Kroot auxiliaries, Saim-Hann Wild Rider Host, the Siege Assault Vanguard chart, 7th Edition codex detachments such as the Imperial Knights Household Detachment); in those, only that list can be chosen.
- **6th and 7th Edition lists:** Formations and Command Benefits removed, Warlord Traits hidden, Lords of War moved to HQ, Super-Heavy or Heavy Support as the Unification directs.
- **Allies:** only within the same era (3rd–5th together, 6th–7th together).
- **Knights:** 6th and 7th Edition Imperium lists may take one Imperial Knight, and Chaos lists one Renegade Knight, as their Lord of War.
- **Super-heavies** are hidden by default. Untick **Super-heavies → Hide super-heavies (untick only when both players agree)** (or **Custom Content → Hide Apocalypse Units** in Imperial Guard 2009) when both players agree.

In-game rules (no Hull Points, melee AP conversion, psychic changes and so on) are not applied to profiles; play them from the Book of the Unification. Full status of every rule: [`docs/unification-rules-ledger.md`](docs/unification-rules-ledger.md).

## Optional add-on: Relics of the Age of Darkness

Horus Heresy 1st Edition units for 6th and 7th Edition lists, by agreement. Off by default: tick **Configuration → Relics of the Age of Darkness** in a 6th or 7th Edition list. 5th Edition Force Organization Chart only; no Rites of War, named characters or Primarchs.

Built so far: Legiones Astartes units for Space Marines, Dark Angels, Blood Angels, Space Wolves and Chaos Space Marines. Not yet tested in New Recruit. Mechanicum, Questoris Knights, Solar Auxilia and Militia, Talons of the Emperor, Daemons of the Ruinstorm and Agents of the Emperor are to follow.

Players' rules: [`docs/Relics_of_the_Age_of_Darkness.pdf`](docs/Relics_of_the_Age_of_Darkness.pdf), rebuilt with every update to the data. Details: [`docs/relics-of-the-age-of-darkness.md`](docs/relics-of-the-age-of-darkness.md).

## Known limitations

- The 1500-point limit on super-heavies is not enforced; it is left to the players' agreement through the switches above.
- A codex without a super-heavy of its own cannot yet take one from Imperial Armour (Unification p. 8).
- Lists that bring their own force type (e.g. Daemon Hunter allies) offer it whenever that faction is used, not only when that list is chosen.
- Two 3rd Edition ally force types in one roster satisfy each other's era requirement.
- Not yet converted: the earlier Forge World lists of 2008–2011 (Vraks Renegades, Corsairs) and Apocalypse / fortification data.

## Reporting problems

Open an [issue](https://github.com/retrodungeon/middlehammer-newrecruit/issues) with:

- the faction and the exact **Army List** label;
- the unit, option or rule;
- what New Recruit shows, and what the book says (with the page, if you have it).

Not on GitHub? Send the same details to the maintainer.

## Repository layout

- `*.gst`, `*.cat` (repository root) — the files New Recruit reads. Built, not hand-edited: `tools/build_middlehammer.py` rebuilds them from the pinned sources.
- `tools/` — conversion, build and validation scripts. `validate_middlehammer.py` checks every published catalogue; `tools/relics_book/` builds the Relics PDF (needs `reportlab`, `pillow`, `pypdf`).
- `.github/workflows/` — `validate.yml` (structural checks), `build-check.yml` (pull requests: the committed files must equal a fresh build), `upstream-audit.yml` and `inspect-sixth-edition.yml` (source inspection). No workflow writes to the repository.
- `sources/upstreams.json` — the upstream data, pinned by commit or checksum.
- `docs/` — coverage, rules ledger, conversion notes and audits.

## Sources

- The Book of the Unification v1.7.2
- Middlehammer Mission Pack v1.4.1
- Community BattleScribe / New Recruit data for each edition: KSnyder1986 (3rd), Kothra (4th), AnonymousCheese (5th), BSData (6th and 7th, and the archived Horus Heresy 1st Edition data). Pinned versions: [`sources/upstreams.json`](sources/upstreams.json).

The rulebooks and codexes themselves are not included in this repository.

## Distribution

This data is published for a small play group; the repository is public so New Recruit can read it. None of the source repositories has a licence file, and permission from their authors is assumed pending confirmation.

Unofficial fan project. Not affiliated with or endorsed by Games Workshop or New Recruit.

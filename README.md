# Middlehammer — New Recruit Game Data

Unofficial community data for playing **The Book of the Unification** (Middlehammer) in [New Recruit](https://www.newrecruit.eu/). The Unification uses Warhammer 40,000 5th Edition as its core and lets codexes from 3rd through 7th Edition be used together.

## Status

**Usable.** Import this repository into New Recruit as a GitHub data source and choose the **Middlehammer Unification** game system.

The picker shows **one entry per faction** (Space Marines, Imperial Guard, Eldar…). After creating a list, choose the codex or variant list in the **Army List** entry under Configuration, e.g. "3rd Ed – Codex: Imperial Guard (1999)", "3rd Ed – Steel Legion Mechanised Infantry (Armageddon 2000)" or "5th Ed – Codex: Imperial Guard (2009)". Only that list's units are shown.

| Edition (of the book) | Army lists available | Notes |
|---|---:|---|
| 3rd | 56 | All official lists in the 3rd Edition source |
| 4th | 10 | Seven from the 5th Edition source; Space Marines (2004), Tyranids (2005) and Blood Angels (2007) from the 4th Edition source |
| 5th | 9 | Including Imperial Guard 2009 |
| 6th | 5 | Astra Militarum, Militarum Tempestus and Tyranids (2014) from the 7th Edition source; Tau Empire (2013) and Farsight Enclaves from the 6th Edition source (pilot) |
| 7th | 40 | All lists in the 7th Edition source except Fallen Angels (Formation only) |

Faction structure and Army List selection were tested in New Recruit on 2026-10-29. Most individual lists have not yet been played through.

Full per-list status: [`docs/codex-coverage.md`](docs/codex-coverage.md).

**Content policy:** all official material is included, including Forge World / Imperial Armour, White Dwarf and Chapter Approved content. Homebrew and unofficial lists and units are excluded.

Unit options and points come from the community source data (`sources/upstreams.json`). They have not been checked line by line against the printed books; report errors as issues.

### Army construction currently enforced

One force type is available: **Standard Force Organization (5th Edition)** — HQ 1–2, Troops 2–6, Elites 0–3, Fast Attack 0–3, Heavy Support 0–3 (5th Edition rulebook, p. 87). These limits have been tested in New Recruit. The force also shows Configuration (first), Dedicated Transport, Unique, Super-Heavy and No Force Org Slot sections, without limits, matching the 5th Edition source data. Super-heavies are hidden by default: Imperial Guard 2009 has **Custom Content → Hide Apocalypse Units**, and every 7th Edition list with super-heavies has **Super-heavies → Hide super-heavies**. Untick when both players agree.

Some lists also bring their own force types (e.g. Daemon Hunters, Witch Hunters and Harlequin allies, Assassin attachments, Kroot auxiliaries, Saim-Hann Wild Rider Host, and the 7th Edition codex detachments such as the Imperial Knights Household Detachment or the Psykana Division). In those force types only their own list can be chosen as the Army List.

For 7th Edition lists, Formations and Command Benefits are removed, codex detachments are kept only for the smaller lists, Warlord Traits hidden and Lords of War reassigned. Allies are restricted to the same era (3rd–5th or 6th–7th); points-based super-heavy limits are **not yet enforced**. See [`docs/unification-rules-ledger.md`](docs/unification-rules-ledger.md) for the full list and status.

### In progress

- **6th Edition:** the 6th Edition data is in the old BattleScribe 1.14b format and is translated by `tools/convert_6e_catalogues.py`. Tau Empire (2013) and Farsight Enclaves are the pilot; the other 6th Edition books follow once the pilot is tested in New Recruit. (The earlier experimental Space Marines translator, `tools/convert_legacy_6e.py`, is superseded.)

## Repository layout

- `*.gst`, `*.cat` (repository root) — the files New Recruit reads.
- `tools/` — Python scripts for building, converting and auditing data. `build_middlehammer.py` rebuilds every Middlehammer catalogue from the pinned sources (`convert_3e_catalogues.py`, `convert_5e_catalogues.py`, `convert_7e_catalogues.py`, then `merge_factions.py`); `validate_middlehammer.py` checks every published catalogue. The 6th Edition translator (`convert_legacy_6e.py` and related) is experimental.
- `.github/workflows/` — `validate.yml` (structural checks), `build-check.yml` (pull requests: the committed files must equal a fresh build), `upstream-audit.yml` and `inspect-sixth-edition.yml` (source inspection). No workflow writes to the repository.
- `sources/upstreams.json` — the upstream repositories each edition is drawn from.
- `docs/` — rules ledger, conversion notes and audit results.

## Sources

- The Book of the Unification v1.7.2
- Middlehammer Mission Pack v1.4.1
- Community BattleScribe/New Recruit data for each edition (see `sources/upstreams.json` and [`docs/compatibility-matrix.md`](docs/compatibility-matrix.md))

The rulebooks and codexes themselves are not included in this repository.

## Open issues

- **Redistribution rights.** None of the source repositories has a licence file. This data is published for a small play group, and permission is being assumed pending confirmation from the upstream authors.

## Disclaimer

Unofficial fan project. Not affiliated with or endorsed by Games Workshop or New Recruit.

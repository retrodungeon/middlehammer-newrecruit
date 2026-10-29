# Middlehammer — New Recruit Game Data

Unofficial community data for playing **The Book of the Unification** (Middlehammer) in [New Recruit](https://www.newrecruit.eu/). The Unification uses Warhammer 40,000 5th Edition as its core and lets codexes from 3rd through 7th Edition be used together.

## Status

**Usable for the codexes listed below.** Import this repository into New Recruit as a GitHub data source and choose the **Middlehammer Unification** game system.

| Catalogue (as shown in New Recruit) | File | Source data | Status |
|---|---|---|---|
| Imperial Guard (5th Edition, 2009) | `Imperial Guard - Codex 2009.cat` | AnonymousCheese/WH40K5E | Imports and builds lists correctly (maintainer-tested in New Recruit, 2026-10-29) |
| Chaos Space Marines (3rd Edition, 2002) | `Chaos Space Marines - Codex 2002.cat` | KSnyder1986/Warhammer-40k-3rd-Edition | Imports and builds lists correctly (maintainer-tested in New Recruit, 2026-10-29) |

Unit options and points come from the community source data listed above. They have not been checked line by line against the printed codexes; report errors as issues.

### Army construction currently enforced

One force type is available: **Standard Force Organization (5th Edition)** — HQ 1–2, Troops 2–6, Elites 0–3, Fast Attack 0–3, Heavy Support 0–3 (5th Edition rulebook, p. 87). These limits have been tested in New Recruit.

Other Unification army-building rules (super-heavy limits, Lords of War, era-restricted allies, the "Patched Out" list) are **not yet enforced**. See [`docs/unification-rules-ledger.md`](docs/unification-rules-ledger.md) for the full list and status.

### Not part of the Middlehammer system

`Warhammer 40,000 (7th Edition).gst` and `Space Marines (7th Edition, 2015).cat` are unmodified BSData 7th Edition files kept for an import test. They load as a **separate game system** ("Warhammer 40,000 7th Edition") and do not apply any Unification rules.

### In progress

- **Space Marines (6th Edition, 2013):** the only available 6th Edition data uses the old BattleScribe 1.14b format and needs a custom translator (`tools/convert_legacy_6e.py`). Output is built only as a GitHub Actions artifact and is gated by `tools/space_marines_release_gate.py`; it is not published. See [`docs/space-marines-2013-conversion.md`](docs/space-marines-2013-conversion.md).

## Repository layout

- `*.gst`, `*.cat` (repository root) — the files New Recruit reads.
- `tools/` — Python scripts for building, converting and auditing data.
- `.github/workflows/` — GitHub Actions that fetch upstream data, run conversions and checks, and upload results as artifacts. **`build-unified.yml` (manual run only) commits a rebuilt Chaos Space Marines catalogue directly to `main`.** No other workflow writes to the repository.
- `sources/upstreams.json` — the upstream repositories each edition is drawn from.
- `docs/` — rules ledger, conversion notes and audit results.

## Sources

- The Book of the Unification v1.7.2
- Middlehammer Mission Pack v1.4.1
- Community BattleScribe/New Recruit data for each edition (see `sources/upstreams.json` and [`docs/compatibility-matrix.md`](docs/compatibility-matrix.md))

The rulebooks and codexes themselves are not included in this repository.

## Open issues

- **Redistribution rights.** The converted catalogues and the 7th Edition test files are derived from other community repositories. Their licences have not yet been reviewed; this should be done before more catalogues are published.
- **Upstream pinning.** `sources/upstreams.json` tracks branch names, not fixed commits, so rebuilds may pick up upstream changes.

## Disclaimer

Unofficial fan project. Not affiliated with or endorsed by Games Workshop or New Recruit.

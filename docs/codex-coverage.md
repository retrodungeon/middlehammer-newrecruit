# Codex coverage

Every army list in the pinned source repositories (see `sources/upstreams.json`) and its status in Middlehammer. Policy: all official material is included — codexes, Chapter Approved, White Dwarf, Citadel Journal, campaign books, Forge World / Imperial Armour. Homebrew and unofficial lists are excluded, as are homebrew units inside official lists.

Status meanings: **Tested** — imported and used in New Recruit by the maintainer. **Converted** — published and structurally validated (`tools/validate_middlehammer.py`), not yet tested in New Recruit. **Not started**.

## 3rd Edition — 24 army lists (56 source lists), 7 excluded

Source: KSnyder1986/Warhammer-40k-3rd-Edition. Built with `tools/convert_3e_catalogues.py`.

Variant army lists (chapter, regiment, craftworld, Chapter Approved and campaign lists) are not separate entries in the New Recruit picker. They are folded into their parent codex (`tools/merge_variants.py`): pick the codex, then choose the variant from the required **Army List** option in the Configuration section. Each choice shows exactly the units of the original list.

| Army list (as shown in New Recruit) | Status | Variants under "Army List" |
|---|---|---|
| Adeptus Arbites (3rd Edition, Citadel Journal 29) | Converted, awaiting New Recruit test | — |
| Black Templars (3rd Edition, 2000) | Converted, awaiting New Recruit test | — |
| Blood Angels (3rd Edition, 1998) | Converted, awaiting New Recruit test | Blood Angels Death Company (Chapter Approved 2001) |
| Chaos Space Marines (3rd Edition, 1999) | Converted, awaiting New Recruit test | — |
| Chaos Space Marines (3rd Edition, 2002) | Tested 2026-10-29 (before homebrew/points fixes); retest | — |
| Codex Assassins (3rd Edition, 1999) | Converted, awaiting New Recruit test | — |
| Daemon Hunters (3rd Edition, 2003) | Converted, awaiting New Recruit test | — |
| Dark Angels (3rd Edition, 1999) | Converted, awaiting New Recruit test | — |
| Dark Eldar (3rd Edition, 2001) | Converted, awaiting New Recruit test | Dark Eldar Wych Cult (2001) |
| Eldar (3rd Edition, 2000) | Converted, awaiting New Recruit test | Biel-Tan Swordwind Army (2000), Saim-Hann Wild Rider Host (2000), Rangers of Alaitoc (2000), Ulthwe The Damned (2000), Ulthwe Strike Force (Eye of Terror 2003), Iyanden Ghost Warriors (2000) |
| Genestealer Cults (3rd Edition, Citadel Journal 40) | Converted, awaiting New Recruit test | — |
| Harlequins (3rd Edition, 2000) | Converted, awaiting New Recruit test | — |
| Imperial Guard (3rd Edition, 1999) | Converted, awaiting New Recruit test | Deathworld Veterans (2000), Catachan (2000), Armageddon Ork Hunters (Chapter Approved 2003), Tanith First and Only (Chapter Approved 2003), Cityfighting Imperial Guard (Chapter Approved 2003), Planetary Defence Regiment (Armageddon 2000), Steel Legion Mechanised Infantry (Armageddon 2000), Death Korps of Krieg (Chapter Approved 2003), Elysian Drop Troops (Chapter Approved 2003), Armoured Company (Chapter Approved 2001), Cadian Shock Troops (Eye of Terror 2003), Salvar Chem-Dogs (Chapter Approved 2003) |
| Imperial Guard (3rd Edition, 2003) | Converted, awaiting New Recruit test | Imperial Guard Armoured Company (Chapter Approved 2004), Armoured Battle Group (IA 2003) |
| Kroot Mercenaries (3rd Edition, Chapter Approved 2004) | Converted, awaiting New Recruit test | — |
| Lost and the Damned (3rd Edition, Eye of Terror 2003) | Converted, awaiting New Recruit test | — |
| Necrons (3rd Edition, 2002) | Converted, awaiting New Recruit test | — |
| Orks (3rd Edition, 1999) | Converted, awaiting New Recruit test | Feral Orks (Chapter Approved 2004), Speed Freeks (Armageddon 2000) |
| Sisters of Battle (3rd Edition, Chapter Approved 2001) | Converted, awaiting New Recruit test | — |
| Space Marines (3rd Edition, 1999) | Converted, awaiting New Recruit test | Salamanders (2000), White Scars (2002), Iron Hands (2001), Imperial Fists (2003), Relictors (White Dwarf 281), Cursed Foundings (Chapter Approved 2004) |
| Space Wolves (3rd Edition, 2000) | Converted, awaiting New Recruit test | Space Wolves 13th Company (2003) |
| Tau (3rd Edition, 2001) | Converted, awaiting New Recruit test | — |
| Tyranids (3rd Edition, 2001) | Converted, awaiting New Recruit test | Tyranid Seeding Swarm (Chapter Approved 2003) |
| Witch Hunters (3rd Edition, 2003) | Converted, awaiting New Recruit test | — |

Excluded as homebrew/unofficial: Adeptus Custodes (Homebrew), Adeptus Mechanicus (Homebrew), Alien Hunters (Homebrew), Daemons of Chaos (Homebrew), Imperial Knights (Homebrew), Squats (Unofficial 2000), The Badab War (Homebrew).

Standalone by decision (2026-10-29): Dark Angels, Black Templars, Blood Angels and Space Wolves are their own codexes; Lost and the Damned stays standalone (Chaos/Guard hybrid); Sisters of Battle, Genestealer Cults and the ally lists (Daemon Hunters, Witch Hunters, Assassins, Harlequins, Kroot, Arbites) stay standalone.

Known limitation: variant lists that bring their own force type (Saim-Hann Wild Rider Force) offer it whenever the parent codex is used, not only when that variant is chosen.

## 4th Edition — not started (13 source catalogues)

Source: Kothra/Warhammer-40-000-4th-Edition-for-NewRecruit. Black Templars, Blood Angels, Chaos Daemons, Chaos Space Marines, Dark Angels, Eldar, Orks, Space Marines, Tau Empire, Tyranids (all 4E); also Blood Angels, Dark Angels and Space Wolves marked 3E.

Gaps: 4th Edition codexes not in this source (e.g. Necrons, Dark Eldar, Imperial Guard, Witch Hunters/Daemon Hunters were not updated in 4th) need checking against a list of 4th Edition publications.

## 5th Edition — 1 tested, 21 not started (22 source catalogues)

Source: AnonymousCheese/WH40K5E. Built with `tools/convert_5e_catalogue.py` / `tools/build_unified.py`.

| Catalogue | Status |
|---|---|
| Imperial Guard (5th Edition, 2009) | Tested 2026-10-29 |

Not started: Black Templars, Blood Angels, Chaos Daemons, Chaos Space Marines, Dark Angels, Dark Eldar, Eldar, Grey Knights, Necrons, Orks, Sisters of Battle, Space Marines, Space Wolves, Tau Empire, Tyranids, Witch Hunters, Tyranids (3rd Ed).

To review before converting (no 5th Edition codex was published for these; likely homebrew under policy): Adeptus Custodes, Adeptus Mechanicus, Genestealer Cult, Leagues of Votann.

## 6th Edition — not started (40 source catalogues)

Source: BSData/wh40k-7th-edition release v3.1.4 (BattleScribe 1.14b format). Needs `tools/convert_legacy_6e.py`; Space Marines 2013 is the experimental pilot and is currently blocked (see `docs/space-marines-2013-conversion.md`). Catalogue list to be recorded from the archive.

## 7th Edition — not started (44 source catalogues)

Source: BSData/wh40k-7th-edition (modern format). Unmodified copies of the game system and Space Marines (2015) sit at the repository root as a separate test system.

Adepta Sororitas; Adeptus Astra Telepathica; Adeptus Custodes Dataslate; Aeronautica Imperialis; Assassins; Astra Militarum (Codex, FW Armoured Battle Group, FW Death Korps of Krieg Assault Brigade, FW Death Korps of Krieg Siege Regiment, FW Elysian, FW Elysian Detachment D-99); Blood Angels (2014); Chaos Daemons; Khorne Daemonkin; Chaos Renegade Knights; Chaos Space Marines; Cult Mechanicus (2015); Dark Angels (2015); Haemonculus Covens; Dark Eldar (2014); Deathwatch; Eldar Corsairs (2015); Eldar Craftworlds (2015); Fallen Angels; Genestealer Cults; Grey Knights (2014); Harlequins; Imperial Knights (2015); Inquisition; Legion of the Damned; Militarum Tempestus; Necrons (2015); Necrons FW Dark Harvest; Orks; Renegades & Heretics; Sisters of Silence Dataslate; Skitarii; Space Marines (2015); Space Marines FW Siege Assault Vanguard; Space Wolves; Tau (2015); Tyranids; Tyrant's Legion FW Defenders of Badab; Ynnari.

Unification notes for 7th Edition: Formations and Allied Detachments must be removed, Command Benefits ignored, Lords of War remapped, Castellans of the Imperium detachment excluded, Imperial/Renegade Knights allowed as Lord of War for 6th/7th Imperium/Chaos codexes. See `docs/unification-rules-ledger.md`.

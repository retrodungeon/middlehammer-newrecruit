# Codex coverage

Every army list in the pinned source repositories (see `sources/upstreams.json`) and its status in Middlehammer. Policy: all official material is included — codexes, Chapter Approved, White Dwarf, Citadel Journal, campaign books, Forge World / Imperial Armour. Homebrew and unofficial lists are excluded, as are homebrew units inside official lists.

Status meanings: **Tested** — imported and used in New Recruit by the maintainer. **Converted** — published and structurally validated (`tools/validate_middlehammer.py`), not yet tested in New Recruit. **Not started**.

## Faction catalogues (all editions)

New Recruit shows **one entry per faction**. Every codex and variant list of that faction, from every edition, is an option of the required **Army List** entry (Configuration section); only the chosen list's units are shown and its minimum requirements apply. Built by `tools/build_middlehammer.py` (using `convert_3e_catalogues.py` and `merge_factions.py`). Faction names are the most common across 3rd–7th Edition.

Status: Imperial Guard 5th Ed 2009 and Chaos Space Marines 3rd Ed 2002 were tested in New Recruit on 2026-10-29 as standalone catalogues and need retesting as faction options. Everything else is converted and structurally validated, awaiting New Recruit testing. Each option was simulated to show exactly the units of its original list.

| Faction | Army List options | Options |
|---|---:|---|
| **Space Marines** | 7 | 3rd Ed – Codex: Space Marines (1999)<br>3rd Ed – Salamanders (2000)<br>3rd Ed – White Scars (2002)<br>3rd Ed – Iron Hands (2001)<br>3rd Ed – Imperial Fists (2003)<br>3rd Ed – Relictors (White Dwarf 281)<br>3rd Ed – Cursed Foundings (Chapter Approved 2004) |
| **Blood Angels** | 2 | 3rd Ed – Codex: Blood Angels (1998)<br>3rd Ed – Blood Angels Death Company (Chapter Approved 2001) |
| **Dark Angels** | 1 | 3rd Ed – Codex: Dark Angels (1999) |
| **Space Wolves** | 2 | 3rd Ed – Codex: Space Wolves (2000)<br>3rd Ed – Space Wolves 13th Company (2003) |
| **Black Templars** | 1 | 3rd Ed – Codex: Black Templars (2000) |
| **Imperial Guard** | 17 | 3rd Ed – Codex: Imperial Guard (1999)<br>3rd Ed – Deathworld Veterans (2000)<br>3rd Ed – Catachan (2000)<br>3rd Ed – Armageddon Ork Hunters (Chapter Approved 2003)<br>3rd Ed – Tanith First and Only (Chapter Approved 2003)<br>3rd Ed – Cityfighting Imperial Guard (Chapter Approved 2003)<br>3rd Ed – Planetary Defence Regiment (Armageddon 2000)<br>3rd Ed – Steel Legion Mechanised Infantry (Armageddon 2000)<br>3rd Ed – Death Korps of Krieg (Chapter Approved 2003)<br>3rd Ed – Elysian Drop Troops (Chapter Approved 2003)<br>3rd Ed – Armoured Company (Chapter Approved 2001)<br>3rd Ed – Cadian Shock Troops (Eye of Terror 2003)<br>3rd Ed – Salvar Chem-Dogs (Chapter Approved 2003)<br>3rd Ed – Codex: Imperial Guard (2003)<br>3rd Ed – Imperial Guard Armoured Company (Chapter Approved 2004)<br>3rd Ed – Armoured Battle Group (IA 2003)<br>5th Ed – Codex: Imperial Guard (2009) |
| **Chaos Space Marines** | 2 | 3rd Ed – Codex: Chaos Space Marines (1999)<br>3rd Ed – Codex: Chaos Space Marines (2002) |
| **Renegades & Heretics** | 1 | 3rd Ed – Lost and the Damned (Eye of Terror 2003) |
| **Eldar** | 7 | 3rd Ed – Codex: Eldar (2000)<br>3rd Ed – Biel-Tan Swordwind Army (2000)<br>3rd Ed – Saim-Hann Wild Rider Host (2000)<br>3rd Ed – Rangers of Alaitoc (2000)<br>3rd Ed – Ulthwe The Damned (2000)<br>3rd Ed – Ulthwe Strike Force (Eye of Terror 2003)<br>3rd Ed – Iyanden Ghost Warriors (2000) |
| **Dark Eldar** | 2 | 3rd Ed – Codex: Dark Eldar (2001)<br>3rd Ed – Dark Eldar Wych Cult (2001) |
| **Harlequins** | 1 | 3rd Ed – Harlequins (2000) |
| **Orks** | 3 | 3rd Ed – Codex: Orks (1999)<br>3rd Ed – Feral Orks (Chapter Approved 2004)<br>3rd Ed – Speed Freeks (Armageddon 2000) |
| **Tyranids** | 2 | 3rd Ed – Codex: Tyranids (2001)<br>3rd Ed – Tyranid Seeding Swarm (Chapter Approved 2003) |
| **Genestealer Cults** | 1 | 3rd Ed – Genestealer Cults (Citadel Journal 40) |
| **Necrons** | 1 | 3rd Ed – Codex: Necrons (2002) |
| **Tau Empire** | 1 | 3rd Ed – Codex: Tau (2001) |
| **Kroot Mercenaries** | 1 | 3rd Ed – Kroot Mercenaries (Chapter Approved 2004) |
| **Sisters of Battle** | 2 | 3rd Ed – Codex: Witch Hunters (2003)<br>3rd Ed – Sisters of Battle (Chapter Approved 2001) |
| **Grey Knights** | 1 | 3rd Ed – Codex: Daemon Hunters (2003) |
| **Assassins** | 1 | 3rd Ed – Codex Assassins (1999) |
| **Adeptus Arbites** | 1 | 3rd Ed – Adeptus Arbites (Citadel Journal 29) |

Faction decisions (2026-10-29): Blood Angels, Dark Angels, Space Wolves and Black Templars are separate factions; Witch Hunters → Sisters of Battle; Daemon Hunters → Grey Knights; Lost and the Damned → Renegades & Heretics (7th Ed Forge World list joins later); Kroot Mercenaries separate; a future 7th Ed Inquisition codex gets its own faction.

Source fix: Codex Assassins (1999) defines the Officio Assassinorum Operative but never offers it in its army list; the build adds the missing entry (Elites).

Known limitation: lists that bring their own force type (e.g. Saim-Hann Wild Rider Force, Daemon Hunter and Witch Hunter allies) offer it whenever the faction is used, not only when that list is chosen.

## 3rd Edition source — 56 lists converted, 7 excluded

Source: KSnyder1986/Warhammer-40k-3rd-Edition. Excluded as homebrew/unofficial: Adeptus Custodes (Homebrew), Adeptus Mechanicus (Homebrew), Alien Hunters (Homebrew), Daemons of Chaos (Homebrew), Imperial Knights (Homebrew), Squats (Unofficial 2000), The Badab War (Homebrew). Homebrew units inside official lists are hidden; Imperial Armour content is unlocked.

## 4th Edition — not started (13 source catalogues)

Source: Kothra/Warhammer-40-000-4th-Edition-for-NewRecruit. Black Templars, Blood Angels, Chaos Daemons, Chaos Space Marines, Dark Angels, Eldar, Orks, Space Marines, Tau Empire, Tyranids (all 4E); also Blood Angels, Dark Angels and Space Wolves marked 3E.

Gaps: 4th Edition codexes not in this source (e.g. Necrons, Dark Eldar, Imperial Guard, Witch Hunters/Daemon Hunters were not updated in 4th) need checking against a list of 4th Edition publications.

## 5th Edition — 1 tested, 21 not started (22 source catalogues)

Source: AnonymousCheese/WH40K5E. Built with `tools/convert_5e_catalogue.py` / `tools/build_unified.py`.

| Catalogue | Status |
|---|---|
| Imperial Guard (2009) → option of the Imperial Guard faction | Tested 2026-10-29 as a standalone catalogue; retest |

Not started: Black Templars, Blood Angels, Chaos Daemons, Chaos Space Marines, Dark Angels, Dark Eldar, Eldar, Grey Knights, Necrons, Orks, Sisters of Battle, Space Marines, Space Wolves, Tau Empire, Tyranids, Witch Hunters, Tyranids (3rd Ed).

To review before converting (no 5th Edition codex was published for these; likely homebrew under policy): Adeptus Custodes, Adeptus Mechanicus, Genestealer Cult, Leagues of Votann.

## 6th Edition — not started (40 source catalogues)

Source: BSData/wh40k-7th-edition release v3.1.4 (BattleScribe 1.14b format). Needs `tools/convert_legacy_6e.py`; Space Marines 2013 is the experimental pilot and is currently blocked (see `docs/space-marines-2013-conversion.md`). Catalogue list to be recorded from the archive.

## 7th Edition — not started (44 source catalogues)

Source: BSData/wh40k-7th-edition (modern format). Unmodified copies of the game system and Space Marines (2015) sit at the repository root as a separate test system.

Adepta Sororitas; Adeptus Astra Telepathica; Adeptus Custodes Dataslate; Aeronautica Imperialis; Assassins; Astra Militarum (Codex, FW Armoured Battle Group, FW Death Korps of Krieg Assault Brigade, FW Death Korps of Krieg Siege Regiment, FW Elysian, FW Elysian Detachment D-99); Blood Angels (2014); Chaos Daemons; Khorne Daemonkin; Chaos Renegade Knights; Chaos Space Marines; Cult Mechanicus (2015); Dark Angels (2015); Haemonculus Covens; Dark Eldar (2014); Deathwatch; Eldar Corsairs (2015); Eldar Craftworlds (2015); Fallen Angels; Genestealer Cults; Grey Knights (2014); Harlequins; Imperial Knights (2015); Inquisition; Legion of the Damned; Militarum Tempestus; Necrons (2015); Necrons FW Dark Harvest; Orks; Renegades & Heretics; Sisters of Silence Dataslate; Skitarii; Space Marines (2015); Space Marines FW Siege Assault Vanguard; Space Wolves; Tau (2015); Tyranids; Tyrant's Legion FW Defenders of Badab; Ynnari.

Unification notes for 7th Edition: Formations and Allied Detachments must be removed, Command Benefits ignored, Lords of War remapped, Castellans of the Imperium detachment excluded, Imperial/Renegade Knights allowed as Lord of War for 6th/7th Imperium/Chaos codexes. See `docs/unification-rules-ledger.md`.

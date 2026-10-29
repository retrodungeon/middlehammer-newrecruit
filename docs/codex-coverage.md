# Codex coverage

Every army list in the pinned source repositories (see `sources/upstreams.json`) and its status in Middlehammer. Policy: all official material is included — codexes, Chapter Approved, White Dwarf, Citadel Journal, campaign books, Forge World / Imperial Armour. Homebrew and unofficial lists are excluded, as are homebrew units inside official lists.

Status meanings: **Tested** — imported and used in New Recruit by the maintainer. **Converted** — published and structurally validated (`tools/validate_middlehammer.py`), not yet tested in New Recruit. **Not started**.

## Faction catalogues (all editions)

New Recruit shows **one entry per faction**. Every codex and variant list of that faction, from every edition, is an option of the required **Army List** entry (Configuration section); only the chosen list's units are shown and its minimum requirements apply. Built by `tools/build_middlehammer.py` (using `convert_3e_catalogues.py` and `merge_factions.py`). Faction names are the most common across 3rd–7th Edition.

Status: faction structure and Army List selection tested in New Recruit on 2026-10-29. Individual lists are converted and structurally validated; most have not been played through in New Recruit. Each option was simulated to show exactly the units of its original list.

| Faction | Army List options | Options |
|---|---:|---|
| **Space Marines** | 8 | 3rd Ed – Codex: Space Marines (1999)<br>3rd Ed – Salamanders (2000)<br>3rd Ed – White Scars (2002)<br>3rd Ed – Iron Hands (2001)<br>3rd Ed – Imperial Fists (2003)<br>3rd Ed – Relictors (White Dwarf 281)<br>3rd Ed – Cursed Foundings (Chapter Approved 2004)<br>5th Ed – Codex: Space Marines (2008) |
| **Blood Angels** | 3 | 3rd Ed – Codex: Blood Angels (1998)<br>3rd Ed – Blood Angels Death Company (Chapter Approved 2001)<br>5th Ed – Codex: Blood Angels (2010) |
| **Dark Angels** | 2 | 3rd Ed – Codex: Dark Angels (1999)<br>4th Ed – Codex: Dark Angels (2007) |
| **Space Wolves** | 3 | 3rd Ed – Codex: Space Wolves (2000)<br>3rd Ed – Space Wolves 13th Company (2003)<br>5th Ed – Codex: Space Wolves (2009) |
| **Black Templars** | 2 | 3rd Ed – Codex: Black Templars (2000)<br>4th Ed – Codex: Black Templars (2005) |
| **Imperial Guard** | 17 | 3rd Ed – Codex: Imperial Guard (1999)<br>3rd Ed – Deathworld Veterans (2000)<br>3rd Ed – Catachan (2000)<br>3rd Ed – Armageddon Ork Hunters (Chapter Approved 2003)<br>3rd Ed – Tanith First and Only (Chapter Approved 2003)<br>3rd Ed – Cityfighting Imperial Guard (Chapter Approved 2003)<br>3rd Ed – Planetary Defence Regiment (Armageddon 2000)<br>3rd Ed – Steel Legion Mechanised Infantry (Armageddon 2000)<br>3rd Ed – Death Korps of Krieg (Chapter Approved 2003)<br>3rd Ed – Elysian Drop Troops (Chapter Approved 2003)<br>3rd Ed – Armoured Company (Chapter Approved 2001)<br>3rd Ed – Cadian Shock Troops (Eye of Terror 2003)<br>3rd Ed – Salvar Chem-Dogs (Chapter Approved 2003)<br>3rd Ed – Codex: Imperial Guard (2003)<br>3rd Ed – Imperial Guard Armoured Company (Chapter Approved 2004)<br>3rd Ed – Armoured Battle Group (IA 2003)<br>5th Ed – Codex: Imperial Guard (2009) |
| **Chaos Space Marines** | 3 | 3rd Ed – Codex: Chaos Space Marines (1999)<br>3rd Ed – Codex: Chaos Space Marines (2002)<br>4th Ed – Codex: Chaos Space Marines (2007) |
| **Chaos Daemons** | 1 | 4th Ed – Codex: Chaos Daemons (2008) |
| **Renegades & Heretics** | 1 | 3rd Ed – Lost and the Damned (Eye of Terror 2003) |
| **Eldar** | 8 | 3rd Ed – Codex: Eldar (2000)<br>3rd Ed – Biel-Tan Swordwind Army (2000)<br>3rd Ed – Saim-Hann Wild Rider Host (2000)<br>3rd Ed – Rangers of Alaitoc (2000)<br>3rd Ed – Ulthwe The Damned (2000)<br>3rd Ed – Ulthwe Strike Force (Eye of Terror 2003)<br>3rd Ed – Iyanden Ghost Warriors (2000)<br>4th Ed – Codex: Eldar (2006) |
| **Dark Eldar** | 3 | 3rd Ed – Codex: Dark Eldar (2001)<br>3rd Ed – Dark Eldar Wych Cult (2001)<br>5th Ed – Codex: Dark Eldar (2010) |
| **Harlequins** | 1 | 3rd Ed – Harlequins (2000) |
| **Orks** | 4 | 3rd Ed – Codex: Orks (1999)<br>3rd Ed – Feral Orks (Chapter Approved 2004)<br>3rd Ed – Speed Freeks (Armageddon 2000)<br>4th Ed – Codex: Orks (2008) |
| **Tyranids** | 3 | 3rd Ed – Codex: Tyranids (2001)<br>3rd Ed – Tyranid Seeding Swarm (Chapter Approved 2003)<br>5th Ed – Codex: Tyranids (2010) |
| **Genestealer Cults** | 1 | 3rd Ed – Genestealer Cults (Citadel Journal 40) |
| **Necrons** | 2 | 3rd Ed – Codex: Necrons (2002)<br>5th Ed – Codex: Necrons (2011) |
| **Tau Empire** | 2 | 3rd Ed – Codex: Tau (2001)<br>4th Ed – Codex: Tau Empire (2005) |
| **Kroot Mercenaries** | 1 | 3rd Ed – Kroot Mercenaries (Chapter Approved 2004) |
| **Sisters of Battle** | 3 | 3rd Ed – Codex: Witch Hunters (2003)<br>3rd Ed – Sisters of Battle (Chapter Approved 2001)<br>5th Ed – Codex: Sisters of Battle (White Dwarf 2011) |
| **Grey Knights** | 2 | 3rd Ed – Codex: Daemon Hunters (2003)<br>5th Ed – Codex: Grey Knights (2011) |
| **Assassins** | 1 | 3rd Ed – Codex Assassins (1999) |
| **Adeptus Arbites** | 1 | 3rd Ed – Adeptus Arbites (Citadel Journal 29) |

Faction decisions (2026-10-29): Blood Angels, Dark Angels, Space Wolves and Black Templars are separate factions; Witch Hunters → Sisters of Battle; Daemon Hunters → Grey Knights; Lost and the Damned → Renegades & Heretics (7th Ed Forge World list joins later); Kroot Mercenaries separate; a future 7th Ed Inquisition codex gets its own faction.

Source fix: Codex Assassins (1999) defines the Officio Assassinorum Operative but never offers it in its army list; the build adds the missing entry (Elites).

Known limitation: lists that bring their own force type (e.g. Saim-Hann Wild Rider Force, Daemon Hunter and Witch Hunter allies) offer it whenever the faction is used, not only when that list is chosen.

## 3rd Edition source — 56 lists converted, 7 excluded

Source: KSnyder1986/Warhammer-40k-3rd-Edition. Excluded as homebrew/unofficial: Adeptus Custodes (Homebrew), Adeptus Mechanicus (Homebrew), Alien Hunters (Homebrew), Daemons of Chaos (Homebrew), Imperial Knights (Homebrew), Squats (Unofficial 2000), The Badab War (Homebrew). Homebrew units inside official lists are hidden; Imperial Armour content is unlocked.

## 4th Edition

The 5th Edition source includes seven 4th Edition codexes that were still current during 5th Edition (Black Templars 2005, Tau Empire 2005, Eldar 2006, Chaos Space Marines 2007, Dark Angels 2007, Chaos Daemons 2008, Orks 2008). They are converted from that source and labelled "4th Ed".

Not started: the 4th Edition source (Kothra/Warhammer-40-000-4th-Edition-for-NewRecruit, 13 catalogues). Most of its codexes are the same books as above, so only books not already covered should be added (e.g. its Space Marines 2004, Blood Angels/Dark Angels/Space Wolves variants, Tyranids 2005), after comparing the two sources for the overlapping books.

## 5th Edition source — 16 converted, 6 skipped

Source: AnonymousCheese/WH40K5E, converted by `tools/convert_5e_catalogues.py`. The source's "Hide Homebrew Units" switch is treated as permanently on (switch removed). Its "Hide Apocalypse Units" switch is kept for Imperial Guard only, where it hides the Baneblade family of super-heavies by default.

Units were audited against the codex each catalogue represents. Removals were made only where the unit is certainly from a later edition. Possibly anachronistic units kept pending review: Black Templars Grimaldus and High Marshal Helbrecht; Dark Eldar Harlequins; Sisters of Battle Arch-Confessor Kyrinov; Space Wolves Bran Redmaw. Some 5th Edition lists also look incomplete in the source (e.g. no Land Raiders or Chaplain Lemartes in Blood Angels 2010).

| Source catalogue | Book | Result |
|---|---|---|
| Black Templars | 4th Ed Codex 2005 | Converted. later-edition units removed: Gladiator, Repulsor |
| Blood Angels | 5th Ed Codex 2010 | Converted. later-edition units removed: Gladiator, Repulsor |
| Chaos Daemons | 4th Ed Codex 2008 | Converted.  |
| Chaos Space Marines | 4th Ed Codex 2007 | Converted. homebrew hidden: Cultist Mob, Forgefiend, Maulerfiend, Venomcrawler; later-edition units removed: Khorne Lord of Skulls |
| Dark Angels | 4th Ed Codex 2007 | Converted. later-edition units removed: Gladiator, Repulsor |
| Dark Eldar | 5th Ed Codex 2010 | Converted.  |
| Eldar | 4th Ed Codex 2006 | Converted. homebrew hidden: Skyreavers |
| Grey Knights | 5th Ed Codex 2011 | Converted.  |
| Imperial Guard | 5th Ed Codex 2009 | Converted. homebrew hidden: Artillery Battery, Bullgryn Squad, Company Commander on Horse, Cyclops Remote Control Demolition Vehicle, Earthshaker Platform, Field Ordnance Battery, Rogal Dorn Battle Tank |
| Necrons | 5th Ed Codex 2011 | Converted.  |
| Orks | 4th Ed Codex 2008 | Converted.  |
| Sisters of Battle | 5th Ed White Dwarf 2011 | Converted.  |
| Space Marines | 5th Ed Codex 2008 | Converted. homebrew hidden: Aggressor Squad, Bladeguard Veteran Squad, Gladiator, Repulsor |
| Space Wolves | 5th Ed Codex 2009 | Converted. later-edition units removed: Gladiator, Repulsor |
| Tau Empire | 4th Ed Codex 2005 | Converted.  |
| Tyranids | 5th Ed Codex 2010 | Converted. homebrew hidden: Barbgaunt Brood, Haruspex Brood, Neurogaunt Brood, Neurolictor Brood, Neurotyrant, Norn Assimilator, Norn Emmisary, Psychophage Brood, Toxicrene Brood, Von Ryan's Leaper Brood; later-edition units removed: Exocrine Brood, Maleceptor Brood; restored (wrongly tagged homebrew): Pyrovore Brood |
| Adeptus Custodes | — | Skipped: homebrew |
| Adeptus Mechanicus | — | Skipped: homebrew |
| Genestealer Cult | — | Skipped: homebrew |
| Leagues of Votann | — | Skipped: homebrew |
| Tyranids (3rd Ed) | — | Skipped: hybrid of the 2001 codex with 5th Edition units; 2001 codex comes from the 3rd Edition source |
| Witch Hunters | — | Skipped: duplicate of 3rd Edition source Witch Hunters (2003) |

## 6th Edition — not started (40 source catalogues)

Source: BSData/wh40k-7th-edition release v3.1.4 (BattleScribe 1.14b format). Needs `tools/convert_legacy_6e.py`; Space Marines 2013 is the experimental pilot and is currently blocked (see `docs/space-marines-2013-conversion.md`). Catalogue list to be recorded from the archive.

## 7th Edition — not started (44 source catalogues)

Source: BSData/wh40k-7th-edition (modern format).

Adepta Sororitas; Adeptus Astra Telepathica; Adeptus Custodes Dataslate; Aeronautica Imperialis; Assassins; Astra Militarum (Codex, FW Armoured Battle Group, FW Death Korps of Krieg Assault Brigade, FW Death Korps of Krieg Siege Regiment, FW Elysian, FW Elysian Detachment D-99); Blood Angels (2014); Chaos Daemons; Khorne Daemonkin; Chaos Renegade Knights; Chaos Space Marines; Cult Mechanicus (2015); Dark Angels (2015); Haemonculus Covens; Dark Eldar (2014); Deathwatch; Eldar Corsairs (2015); Eldar Craftworlds (2015); Fallen Angels; Genestealer Cults; Grey Knights (2014); Harlequins; Imperial Knights (2015); Inquisition; Legion of the Damned; Militarum Tempestus; Necrons (2015); Necrons FW Dark Harvest; Orks; Renegades & Heretics; Sisters of Silence Dataslate; Skitarii; Space Marines (2015); Space Marines FW Siege Assault Vanguard; Space Wolves; Tau (2015); Tyranids; Tyrant's Legion FW Defenders of Badab; Ynnari.

Unification notes for 7th Edition: Formations and Allied Detachments must be removed, Command Benefits ignored, Lords of War remapped, Castellans of the Imperium detachment excluded, Imperial/Renegade Knights allowed as Lord of War for 6th/7th Imperium/Chaos codexes. See `docs/unification-rules-ledger.md`.

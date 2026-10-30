# Codex coverage

Every army list in the pinned source repositories (see `sources/upstreams.json`) and its status in Middlehammer. Policy: all official material is included — codexes, Chapter Approved, White Dwarf, Citadel Journal, campaign books, Forge World / Imperial Armour. Homebrew and unofficial lists are excluded, as are homebrew units inside official lists.

Status meanings: **Tested** — imported and used in New Recruit by the maintainer. **Converted** — published and structurally validated (`tools/validate_middlehammer.py`), not yet tested in New Recruit. **Not started**.

## Faction catalogues (all editions)

New Recruit shows **one entry per faction**. Every codex and variant list of that faction, from every edition, is an option of the required **Army List** entry (Configuration section); only the chosen list's units are shown and its minimum requirements apply. Built by `tools/build_middlehammer.py` (using `convert_3e_catalogues.py` and `merge_factions.py`). Faction names are the most common across 3rd–7th Edition.

Status: faction structure and Army List selection tested in New Recruit on 2026-10-29. Individual lists are converted and structurally validated; most have not been played through in New Recruit. Each option was simulated to show exactly the units of its original list.

| Faction | Army List options | Options |
|---|---:|---|
| **Space Marines** | 17 | 3rd Ed – Codex: Space Marines (1999)<br>3rd Ed – Salamanders (2000)<br>3rd Ed – White Scars (2002)<br>3rd Ed – Iron Hands (2001)<br>3rd Ed – Imperial Fists (2003)<br>3rd Ed – Relictors (White Dwarf 281)<br>3rd Ed – Cursed Foundings (Chapter Approved 2004)<br>4th Ed – Codex: Space Marines (2004)<br>5th Ed – Codex: Space Marines (2008)<br>6th Ed – Codex: Space Marines (2013)<br>6th Ed – Clan Raukaan (supplement, 2013)<br>6th Ed – Sentinels of Terra (supplement, 2013)<br>6th Ed – Forge World: Siege Assault Vanguard (IA10, 6th Ed update)<br>6th Ed – Codex: Legion of the Damned (2014)<br>7th Ed – Codex: Space Marines (2015)<br>7th Ed – Forge World: Siege Assault Vanguard<br>7th Ed – Forge World: Tyrant's Legion (Defenders of Badab) |
| **Blood Angels** | 5 | 3rd Ed – Codex: Blood Angels (1998)<br>3rd Ed – Blood Angels Death Company (Chapter Approved 2001)<br>4th Ed – Codex: Blood Angels (White Dwarf 2007)<br>5th Ed – Codex: Blood Angels (2010)<br>7th Ed – Codex: Blood Angels (2014) |
| **Dark Angels** | 4 | 3rd Ed – Codex: Dark Angels (1999)<br>4th Ed – Codex: Dark Angels (2007)<br>6th Ed – Codex: Dark Angels (2013)<br>7th Ed – Codex: Dark Angels (2015) |
| **Space Wolves** | 4 | 3rd Ed – Codex: Space Wolves (2000)<br>3rd Ed – Space Wolves 13th Company (2003)<br>5th Ed – Codex: Space Wolves (2009)<br>7th Ed – Codex: Space Wolves (2014) |
| **Deathwatch** | 1 | 7th Ed – Codex: Deathwatch (2016) |
| **Black Templars** | 2 | 3rd Ed – Codex: Black Templars (2000)<br>4th Ed – Codex: Black Templars (2005) |
| **Imperial Guard** | 26 | 3rd Ed – Codex: Imperial Guard (1999)<br>3rd Ed – Deathworld Veterans (2000)<br>3rd Ed – Catachan (2000)<br>3rd Ed – Armageddon Ork Hunters (Chapter Approved 2003)<br>3rd Ed – Tanith First and Only (Chapter Approved 2003)<br>3rd Ed – Cityfighting Imperial Guard (Chapter Approved 2003)<br>3rd Ed – Planetary Defence Regiment (Armageddon 2000)<br>3rd Ed – Steel Legion Mechanised Infantry (Armageddon 2000)<br>3rd Ed – Death Korps of Krieg (Chapter Approved 2003)<br>3rd Ed – Elysian Drop Troops (Chapter Approved 2003)<br>3rd Ed – Armoured Company (Chapter Approved 2001)<br>3rd Ed – Cadian Shock Troops (Eye of Terror 2003)<br>3rd Ed – Salvar Chem-Dogs (Chapter Approved 2003)<br>3rd Ed – Codex: Imperial Guard (2003)<br>3rd Ed – Imperial Guard Armoured Company (Chapter Approved 2004)<br>3rd Ed – Armoured Battle Group (IA 2003)<br>5th Ed – Codex: Imperial Guard (2009)<br>6th Ed – Codex: Astra Militarum (2014)<br>6th Ed – Codex: Militarum Tempestus (2014)<br>7th Ed – Forge World: Armoured Battle Group<br>7th Ed – Forge World: Death Korps of Krieg Assault Brigade<br>7th Ed – Forge World: Death Korps of Krieg Siege Regiment<br>7th Ed – Forge World: Elysian Drop Troops<br>7th Ed – Forge World: Elysian Detachment D-99<br>7th Ed – Adeptus Astra Telepathica<br>7th Ed – Aeronautica Imperialis |
| **Chaos Space Marines** | 7 | 3rd Ed – Codex: Chaos Space Marines (1999)<br>3rd Ed – Codex: Chaos Space Marines (2002)<br>4th Ed – Codex: Chaos Space Marines (2007)<br>6th Ed – Codex: Chaos Space Marines (2012)<br>6th Ed – Black Legion (supplement, 2013)<br>6th Ed – Crimson Slaughter (supplement, 2014)<br>7th Ed – Codex: Khorne Daemonkin (2015) |
| **Chaos Daemons** | 3 | 4th Ed – Codex: Chaos Daemons (2008)<br>6th Ed – Codex: Chaos Daemons (2013)<br>7th Ed – Codex: Chaos Daemons (2015) |
| **Renegades & Heretics** | 2 | 3rd Ed – Lost and the Damned (Eye of Terror 2003)<br>7th Ed – Forge World: Renegades & Heretics |
| **Eldar** | 12 | 3rd Ed – Codex: Eldar (2000)<br>3rd Ed – Biel-Tan Swordwind Army (2000)<br>3rd Ed – Saim-Hann Wild Rider Host (2000)<br>3rd Ed – Rangers of Alaitoc (2000)<br>3rd Ed – Ulthwe The Damned (2000)<br>3rd Ed – Ulthwe Strike Force (Eye of Terror 2003)<br>3rd Ed – Iyanden Ghost Warriors (2000)<br>4th Ed – Codex: Eldar (2006)<br>6th Ed – Codex: Eldar (2013)<br>6th Ed – Iyanden (supplement, 2013)<br>7th Ed – Codex: Craftworlds (2015)<br>7th Ed – Forge World: Eldar Corsairs |
| **Ynnari** | 1 | 7th Ed – Ynnari (Gathering Storm: Fracture of Biel-Tan) |
| **Dark Eldar** | 5 | 3rd Ed – Codex: Dark Eldar (2001)<br>3rd Ed – Dark Eldar Wych Cult (2001)<br>5th Ed – Codex: Dark Eldar (2010)<br>7th Ed – Codex: Dark Eldar (2014)<br>7th Ed – Haemonculus Covens (supplement) |
| **Harlequins** | 2 | 3rd Ed – Harlequins (2000)<br>7th Ed – Codex: Harlequins (2015) |
| **Orks** | 6 | 3rd Ed – Codex: Orks (1999)<br>3rd Ed – Feral Orks (Chapter Approved 2004)<br>3rd Ed – Speed Freeks (Armageddon 2000)<br>4th Ed – Codex: Orks (2008)<br>6th Ed – Forge World: Dread Mob (IA8, 2013)<br>7th Ed – Codex: Orks (2014) |
| **Tyranids** | 5 | 3rd Ed – Codex: Tyranids (2001)<br>3rd Ed – Tyranid Seeding Swarm (Chapter Approved 2003)<br>4th Ed – Codex: Tyranids (2005)<br>5th Ed – Codex: Tyranids (2010)<br>6th Ed – Codex: Tyranids (2014) |
| **Genestealer Cults** | 2 | 3rd Ed – Genestealer Cults (Citadel Journal 40)<br>7th Ed – Codex: Genestealer Cults (2016) |
| **Necrons** | 4 | 3rd Ed – Codex: Necrons (2002)<br>5th Ed – Codex: Necrons (2011)<br>7th Ed – Codex: Necrons (2015)<br>7th Ed – Forge World: Dark Harvest |
| **Tau Empire** | 5 | 3rd Ed – Codex: Tau (2001)<br>4th Ed – Codex: Tau Empire (2005)<br>6th Ed – Codex: Tau Empire (2013)<br>6th Ed – Farsight Enclaves (supplement, 2013)<br>7th Ed – Codex: Tau Empire (2015) |
| **Kroot Mercenaries** | 1 | 3rd Ed – Kroot Mercenaries (Chapter Approved 2004) |
| **Sisters of Battle** | 4 | 3rd Ed – Codex: Witch Hunters (2003)<br>3rd Ed – Sisters of Battle (Chapter Approved 2001)<br>5th Ed – Codex: Sisters of Battle (White Dwarf 2011)<br>6th Ed – Codex: Adepta Sororitas (2013) |
| **Grey Knights** | 3 | 3rd Ed – Codex: Daemon Hunters (2003)<br>5th Ed – Codex: Grey Knights (2011)<br>7th Ed – Codex: Grey Knights (2014) |
| **Adeptus Mechanicus** | 2 | 7th Ed – Codex: Skitarii (2015)<br>7th Ed – Codex: Cult Mechanicus (2015) |
| **Adeptus Custodes** | 2 | 7th Ed – Adeptus Custodes (dataslate)<br>7th Ed – Sisters of Silence (dataslate) |
| **Imperial Knights** | 2 | 7th Ed – Codex: Imperial Knights (2015)<br>7th Ed – Renegade Knights |
| **Inquisition** | 3 | 3rd Ed – Codex Assassins (1999)<br>6th Ed – Codex: Inquisition (2013)<br>7th Ed – Officio Assassinorum |
| **Adeptus Arbites** | 1 | 3rd Ed – Adeptus Arbites (Citadel Journal 29) |

Faction decisions (2026-10-29): Ynnari is its own faction; Skitarii and Cult Mechanicus form Adeptus Mechanicus; Deathwatch and Adeptus Custodes are new factions; Militarum Tempestus and the Forge World Guard lists are Imperial Guard options; Khorne Daemonkin is a Chaos Space Marines option; Corsairs are an Eldar option. Blood Angels, Dark Angels, Space Wolves and Black Templars are separate factions; Witch Hunters → Sisters of Battle; Daemon Hunters → Grey Knights; Lost and the Damned → Renegades & Heretics (7th Ed Forge World list joins later); Kroot Mercenaries separate; the 7th Ed Inquisition list is its own faction, and both Assassins lists are part of it.

Source fix: Codex Assassins (1999) defines the Officio Assassinorum Operative but never offers it in its army list; the build adds the missing entry (Elites).

Known limitation: lists that bring their own force type (e.g. Saim-Hann Wild Rider Force, Daemon Hunter and Witch Hunter allies) offer it whenever the faction is used, not only when that list is chosen.

## 3rd Edition source — 56 lists converted, 7 excluded

Source: KSnyder1986/Warhammer-40k-3rd-Edition. Excluded as homebrew/unofficial: Adeptus Custodes (Homebrew), Adeptus Mechanicus (Homebrew), Alien Hunters (Homebrew), Daemons of Chaos (Homebrew), Imperial Knights (Homebrew), Squats (Unofficial 2000), The Badab War (Homebrew). Homebrew units inside official lists are hidden; Imperial Armour content is unlocked.

## 4th Edition

The 5th Edition source includes seven 4th Edition codexes that were still current during 5th Edition (Black Templars 2005, Tau Empire 2005, Eldar 2006, Chaos Space Marines 2007, Dark Angels 2007, Chaos Daemons 2008, Orks 2008). They are converted from that source and labelled "4th Ed".

Source: Kothra/Warhammer-40-000-4th-Edition-for-NewRecruit (pinned), converted by `tools/convert_4e_catalogues.py`. Only the books no other source provides are converted:

| Source catalogue | Book | Result |
|---|---|---|
| Space Marines (4E) | Codex: Space Marines (2004) | Converted. Forge World switch always on; chapter-specific characters (Calgar, Tigurius, Cassius, Shrike, Lysander, Tyrannic War Veterans) appear when their chapter is chosen, as in the source |
| Tyranids (4E) | Codex: Tyranids (2005) | Converted |
| Blood Angels (4E) | Codex: Blood Angels (White Dwarf 2007) | Converted. The source names no publication; the label needs confirming |
| Black Templars, Chaos Daemons, Chaos Space Marines, Dark Angels, Eldar, Orks, Tau Empire (4E) | — | Not converted: the same books come from the 5th Edition source |
| Blood Angels, Dark Angels, Space Wolves (3E) | — | Not converted: 3rd Edition books, which come from the 3rd Edition source |

Source fixes: conditions that point at entries of other 4th Edition books (left over from copying entries between catalogues) can never be true inside one book and are removed.

## 5th Edition source — 16 converted, 6 skipped

Source: AnonymousCheese/WH40K5E, converted by `tools/convert_5e_catalogues.py`. The source's "Hide Homebrew Units" switch is treated as permanently on (switch removed). Its "Hide Apocalypse Units" switch is kept for Imperial Guard only, where it hides the Baneblade family of super-heavies by default.

Units were audited against the codex each catalogue represents. Removals were made only where the unit is certainly from a later edition.

Verified against the maintainer's codex PDFs (2026-10-29):

| Book | Checked | Result |
|---|---|---|
| Black Templars (2005) | High Marshal Helbrecht, Chaplain Grimaldus | Both are special characters in the codex — kept |
| Sisters of Battle (White Dwarf 2011) | Arch-Confessor Kyrinov | In the codex — kept |
| Dark Angels (2007) | Every unit in the list; Gladiator, Repulsor | All listed units appear in the codex; Gladiator and Repulsor do not — removal confirmed |
| Blood Angels (2010) | Every unit in the list; Gladiator, Repulsor; Land Raiders, Lemartes, Corbulo | All listed units appear; Gladiator and Repulsor do not — removal confirmed. Land Raiders are Dedicated Transports in this codex and the source has them as transport options — correct. Lemartes is an option of the Death Company unit in both — correct. **Brother Corbulo (105 pts, one of the Sanguinary Priests) was missing — added.** |
| Dark Eldar (2010) | Harlequins | An Elites choice in the codex (18 pts per model) — kept. Raven Strike Fighter, Reaper and Tantalus are Forge World units, tagged as such by the source — kept per policy |
| Space Wolves (2009) | Every unit in the list; Gladiator, Repulsor, Bran Redmaw | Gladiator and Repulsor do not appear — removal confirmed. **Bran Redmaw appears only in background and markings, with no army list entry — removed.** |
| Tyranids (2010) | Every unit in the list; removed, restored and homebrew-hidden units | All kept units appear, including Pyrovore (restore confirmed), Harpy and Spore Mine Cluster; Exocrine, Maleceptor and every homebrew-tagged unit do not appear — removals confirmed |
| Chaos Space Marines (2007) | Every unit in the list; removed and homebrew-hidden units | All listed units appear (including Huron Blackheart, p. 56); Forgefiend, Maulerfiend and Venomcrawler do not appear; Lord of Skulls and cultists appear only in background text — removals confirmed |

All 5th Edition source books flagged in the audit have now been checked.

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

## Imperial Armour (hand-transcribed)

No community data exists for Imperial Armour Volume Nine and Ten (The Badab War, 2010 and 2011, 5th Edition era). Entries are transcribed from the maintainer's copies in `tools/imperial_armour_5e.py` and added to the list each book names. They reuse the source list's weapon, wargear and rule profiles; new special rules are written out in full in our own words, so the list can be played from New Recruit alone. Profiles, points, wargear and options follow the book.

| Entry | Book | Added to | Status |
|---|---|---|---|
| Captain Mordaci Blaylock (Novamarines) | IA9 p. 171 | 5th Ed – Codex: Space Marines (2008), HQ | Added; to be checked against the book in New Recruit |

## 6th Edition source — 13 converted

Source: BSData/wh40k-7th-edition release v3.1.4, asset `Warhammer_40000_6th_Ed_last_revision.bsr` (pinned by SHA-256 in `sources/upstreams.json`), BattleScribe 1.14b format. Translated to the current format by `tools/convert_6e_catalogues.py`, then adjusted for the Unification as the 7th Edition lists are: Formations, Battle Formations, Spearheads, Fortifications and extra-detachment markers removed; Lords of War reassigned (independent characters → HQ, super-heavies → Super-Heavy, others → Heavy Support); Apocalypse Legendary Units that repeat a Lord of War dropped; super-heavies behind the "Hide super-heavies" switch; conditions on the Primary Detachment always true, on Apocalypse following the switch, on other force types never true.

Rules text: the 6th Edition source records most special rules by name only. Text is filled by `tools/rules_text_6e.py`, in order: rules written out in our own words from the maintainer's books (Codex: Space Marines 2013: Chapter Tactics, Combat Squads, character and unit rules; Forge World's 6th Edition Chapter Tactics for Imperial Armour Chapters; the Siege Assault Vanguard and Badab War character updates); the 5th Edition core rules (universal special rules); the same faction's 7th Edition data; the 7th Edition core rules. Text from 7th Edition data ends "(7th Ed wording)". Still without text: mostly Forge World, Apocalypse and Escalation rules carried in the supplements, and Warlord Traits (not used). The build report lists every rule left empty.

| Source catalogue | Book | Status |
|---|---|---|
| Tau - Codex | Codex: Tau Empire (2013) | Converted (pilot) |
| Tau - Supplement - Farsight Enclaves | Farsight Enclaves (2013) | Converted (pilot) |
| Dark Angels - Codex | Codex: Dark Angels (2013) | Converted |
| Eldar - Codex, Eldar - Supplement - Iyanden | Codex: Eldar (2013), Iyanden (2013) | Converted |
| Space Marines - FW - Siege Assault Vanguard | Imperial Armour 10 Siege Assault Vanguard, Forge World 6th Edition update | Converted. Its own force chart (1-2 HQ, 2-6 Troops, 0-3 Elites, 0-2 Fast Attack, 1-4 Heavy Support) is offered as a force type, slot limits only; the standard chart can also be used |
| (Badab War Characters Update, Forge World, 6th Ed) | Imperial Armour 9 and 10 characters | 22 characters as HQ choices in both the Siege Assault Vanguard (IA10) and Codex: Space Marines (2013) lists. Tyberos and Lias Issodon are hand-built from the update (`tools/sixth_additions.py`); the others come from the 6th Edition data. Points corrected to the update: Androcles 145 (data: 155), Enkomi 145 (data: 155). Not included: Malakim Phoros (Lamenters use Codex: Blood Angels; no 6th Edition Blood Angels list here) and Carnac Commodus (Tyrant's Legion list, not converted) |
| Space Marines - Codex, Supplements Clan Raukaan, Sentinels of Terra | Codex: Space Marines (2013), Clan Raukaan (2013), Sentinels of Terra (2013) | Converted. Uncategorised units (Command Squad, Honour Guard, Techmarine, Servitors, Damocles, Cypher) use no slot; the Allied Detachment Chapter Tactics entry is removed. "DEVASTATOR PLACEHOLDER (IA12)" is the source's container for Vigilator-Sergeant Hamath Kraatos and is kept as is |
| Chaos Daemons (40K) - Codex | Codex: Chaos Daemons (2013) | Converted |
| Chaos Space Marines - Supplements Black Legion, Crimson Slaughter | Black Legion (2013), Crimson Slaughter (2014) | Converted |
| Orks - FW - Dread Mob | IA08 Dread Mob (2013) | Converted. Gargantuan Squiggoth is treated as a super-heavy (Gargantuan Creature) |
| Renegades & Heretics - FW - Defenders of Vraks, Servants of Decay, Servants of Slaughter; Eldar - FW - Corsairs | Forge World lists of 2008–2011 | To decide (earlier Forge World books than the 7th Edition source's) |
| Adepta Sororitas, Chaos Space Marines - Codex, Inquisition - Codex, Legion of the Damned - Codex | Same books as the 7th Edition source (later revision there) | Not converted |
| Astra Militarum and Forge World Guard / Space Marine / Necron lists | Same books as the 7th Edition source | Not converted |
| Blood Angels, Dark Eldar, Grey Knights, Imperial Guard, Necrons, Orks, Space Wolves Codex | 5th Edition codexes (from the 5th Edition source) | Not converted |
| Imperial Knights - Codex | Almost empty in the source | Not converted |
| Imperial Guard - Apocalypse, Fortifications and Stronghold Assault | Apocalypse / fortifications | Not converted |

## 7th Edition source — 43 converted, 1 not used

Source: BSData/wh40k-7th-edition (pinned), converted by `tools/convert_7e_catalogues.py`. Book editions in the Army List labels follow the maintainer's library: Astra Militarum, Militarum Tempestus and Tyranids (2014) are 6th Edition books; the rest are 7th Edition.

What the converter does (see the rules ledger for page references):
- Translates the source's BattleScribe 2.00 format to the 2.03 format used here.
- Removes Formations, Battle Formations, Decurion-style Command/Core/Auxiliary slots, Flyer Wings, Spearheads and Primary Detachment markers, and every 7th Edition detachment except the codex detachments listed below (890 top-level entries). Rules that depended on the Combined Arms Detachment now depend on the standard force; rules that depended on any other detachment or formation never apply.
- Hides Warlord Traits.
- Lords of War: 8 independent characters → HQ; 301 super-heavies (by unit type, or 9+ Hull Points) → super-heavy allowance; 36 others → Heavy Support.
- Super-heavies are hidden by a **Super-heavies → Hide super-heavies** switch (Configuration), on by default; untick when both players agree. Rules that depended on the Apocalypse detachment follow this switch.
- Fortifications are removed (decision 2026-10-29; may be revisited).
- Forge World and dataslate switches are treated as always on.
- IDs are made unique per list, because the 7th Edition source lists reuse each other's IDs and factions import one another.

To verify against the books:
- Lords of War classified as Heavy Support because the source does not mark them as independent characters or super-heavies: (FW) Sokar Pattern Stormbird, (Y) The Yncarne, Avatar of Ynnead, * Caestus Assault Ram, Avatar of Khaine, Gargantuan Squiggoth, Giant Chaos Spawn, Giant Chaos Spawns, Imotekh the Stormlord, Magnus the Red, Roboute Guilliman, Primarch of the Ultramarines, Sokar Pattern Stormbird, Spined Chaos Beast, Spined Chaos Beasts, The Yncarne, Avatar of Ynnead, [FW] Cor'bax Utterblight, [FW] Samus. In particular Imotekh the Stormlord (likely an independent character) and the Sokar Pattern Stormbird (likely super-heavy) look wrong in the source.
- Entries the source leaves uncategorised, kept with no force organisation slot as in the source: * Damocles Command Rhino, Belisarius Cawl, Celestine, The Living Saint (FoC), Cypher, Lord of the Fallen, Drop Sentinel Squadron, Imperial Navy Lightnings (DftS), Imperial Navy Thunderbolts (DftS), Inquisitor Greyfax, [FW] Ferrum Infernus Chaos Dreadnought.

Codex detachments (decision 2026-10-29). The nine smaller lists keep their own detachments, offered as extra force types for their faction. None of them has both an HQ and a Troops choice, so they are fielded only through these detachments (their Army List option is hidden in the standard force). Only slot limits are kept: all detachment special rules (Command Benefits and the like) are dropped, and the Legion of the Damned detachment's "cannot be your Primary Detachment" limit is not enforced. In a detachment, only its own list can be chosen as the Army List. Lord of War slots apply to the Super-Heavy section, where this data puts every Knight; Knights are still hidden by the super-heavy switch until it is unticked. Not kept: Castellans of the Imperium (patched out) and the Adeptus Mechanicus convocations (built from Formations). Fallen Angels (supplement) is not converted: it could only be fielded as a Formation, which the Unification bans (author's ruling, 2026-10-29).
  - Oathsworn Detachment (Imperial Knights): Super-Heavy 1-3
  - Household Detachment (Imperial Knights): Super-Heavy 3-5
  - Forsworn Knight Detachment (Renegade Knights): Super-Heavy 1-3
  - Inquisitorial Detachment (Inquisition): HQ 1-2, Elites 0-3, Fast Attack 0-1
  - Inquisitorial Representative (Inquisition): HQ 1-1, Elites 0-3
  - Officio Assassinorum Detachment (Assassins): Elites 1-1
  - Assassinorum Operative (Assassins): Elites 1-1
  - Null-Maiden Task Force (Sisters of Silence): Elites 1-3
  - Legion of the Damned Detachment (Legion of the Damned): Elites 1-4
  - Spectral Host (Legion of the Damned): Elites 1-4
  - Psykana Division (Astra Telepathica): HQ 1-1, Elites 0-3
  - Imperial Navy Section (Aeronautica Imperialis): HQ 0-1, Fast Attack 1-1
  - Covenite Coterie Detachment (Haemonculus Covens): No Force Org Slot 0-any, HQ 2-6, Elites 2-8, Heavy Support 0-4

Placement: Imperial Knights and Renegade Knights → Imperial Knights faction; Inquisition and Officio Assassinorum → Inquisition faction; Sisters of Silence → Adeptus Custodes; Astra Telepathica and Aeronautica Imperialis → Imperial Guard; Legion of the Damned → Space Marines; Haemonculus Covens → Dark Eldar.

To verify: the book edition shown for Inquisition, Legion of the Damned, Officio Assassinorum, Astra Telepathica, Aeronautica Imperialis, and Renegade Knights (labelled 7th Ed after the source; some may be 6th Edition publications). The Null-Maiden Rhino is a Fast Attack choice in the source, so it is not available in a Null-Maiden Task Force. The Inquisition source also offers the Gathering Storm characters (Guilliman, Celestine, Cawl, Voldus, Cypher), as the other 7th Edition Imperium lists do.

**File size:** the 7th Edition sources are large (Astra Militarum plus six Forge World lists is about 10 MB). The Imperial Guard faction file is about 14 MB and Space Marines about 10 MB; performance on phones needs testing.

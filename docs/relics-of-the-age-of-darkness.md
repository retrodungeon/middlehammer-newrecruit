# Relics of the Age of Darkness (optional add-on)

Horus Heresy 1st Edition units for 6th and 7th Edition Army Lists. **Off by default.** In a list whose Army List is a 6th or 7th Edition book, tick **Configuration → Relics of the Age of Darkness → Use Horus Heresy 1st Edition units**; the Heresy units then appear in the normal sections, marked "(Heresy)". Both players should agree before using them.

Source: [BSData/horus-heresy-1st-edition](https://github.com/BSData/horus-heresy-1st-edition), pinned in `sources/upstreams.json` (the archived, final Heresy 1st Edition data). Built by `tools/convert_hh1_relics.py`.

## Status

Pilot: **Legiones Astartes** only. Not yet tested in New Recruit. Still to do: Mechanicum (→ Adeptus Mechanicus), Questoris Knights (→ Imperial Knights), Solar Auxilia and Imperialis Militia (→ Imperial Guard; Militia and Dark Compliance also → Renegades & Heretics), Talons of the Emperor (→ Adeptus Custodes), Daemons of the Ruinstorm (→ Chaos Daemons), Agents of the Emperor (→ Inquisition).

## Rulings (maintainer, 2026-10-30)

| Rule | How it is applied |
|---|---|
| Optional, 6th/7th Edition lists only | Configuration toggle, shown only when the chosen Army List is a 6th or 7th Edition book; every Heresy unit is hidden unless it is ticked. |
| Standard 5th Edition chart only; no Rites of War | Units keep their base slot. Rite of War, Heresy force types (Crusade, Zone Mortalis, Strategic Raid, Onslaught, Leviathan, Castellan) and Allied Detachments are not used; options that need them never appear. Unlocks by a unit's own options (e.g. a Primus Nullificator Consul makes Nullificators Troops) are kept. |
| No named characters, no Primarchs | Listed in `NAMED` in the converter. |
| Legion-specific units go to the successor faction | Dark Angels → Dark Angels; Blood Angels → Blood Angels; Space Wolves → Space Wolves; Ultramarines, Imperial Fists, White Scars, Iron Hands, Salamanders, Raven Guard → Space Marines; the nine Traitor Legions → Chaos Space Marines. Blackshields are not converted. Generic Legion units go to all five; Loyalist/Traitor-only options follow the host. |
| Legion traits dropped; host army rules instead | The army-wide Legion traits are removed (from the Legiones Astartes category and from units that link them). Each Heresy unit carries the rule **Relics of the Age of Darkness**: it counts as having the army-wide special rules of its Army List and is affected by them as if it were from that list. Units keep their own rules, including the Legiones Astartes rule. This is a Middlehammer ruling, not printed text. |
| Legion-specific wargear | In single-Legion hosts (Dark Angels, Blood Angels, Space Wolves) every unit has that Legion's options. In Space Marines and Chaos Space Marines, a Legion's own units have that Legion's options; generic units have none. |
| Lords of War | Only Legion super-heavies (Fellblade, Falchion, Glaive, Typhon, Cerberus, Stormblade, Thunderhawks, Sokar Stormbird, Mastodon, Malcador). Super-heavies use the Super-Heavy section and the list's "Hide super-heavies" switch; others become Heavy Support (Unification p. 10). Titans, Knights and Imperial Army super-heavies wait for their own Heresy lists. |
| No Hull Points; Structure Points for super-heavies | Hull Points are removed from profiles; super-heavies get Structure Points of 1/3 their Hull Points, rounded (Unification p. 9–10). |
| No Warlord Traits; no fortifications | As for 7th Edition lists. |
| Heresy army construction removed | The "(Compulsory)" labels and compulsory-slot categories of the Crusade chart are removed. The Warlord option stays (for Slay the Warlord) but is no longer required. "Master of the Legion" (Rite of War choice, one per 1,000 points) is hidden; Command Squads remain available. |
| Not converted (content policy) | Fan-made: Necron, Asuryani and Mournival Units catalogues. Varangian Heresy Legions (provenance unverified). The Heresy copy of Codex: Chaos Daemons (2013), already in the data. |

## Units per faction

### Space Marines (101 entries)

Entries in square brackets are Legion-specific. A unit listed twice can be taken in either section.

- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Dark Sons of Death Squad (Karaoghlanlar) [White Scars]
- Elites: Deliverer Squad [Raven Guard]
- Elites: Destroyer Squad, Legion
- Elites: Dreadnought Talon, Legion
- Elites: Ebon Keshig, The [White Scars]
- Elites: Firedrake Terminator Squad [Salamanders]
- Elites: Golden Keshig, The [White Scars]
- Elites: Gorgon Terminator Squad [Iron Hands]
- Elites: Invictarus Suzerain Squad [Ultramarines]
- Elites: Medusan Immortals [Iron Hands]
- Elites: Mor Deythan Strike Squad [Raven Guard]
- Elites: Mortis Dreadnought, Legion
- Elites: Nemesis Destroyer Squad [Ultramarines]
- Elites: Nullificators, Legion
- Elites: Quad Launcher Support Battery, Legion
- Elites: Rapier Weapons Battery, Legion
- Elites: Techmarine Covenant
- Elites: Templar Brethren [Imperial Fists]
- Elites: Terminator Squad, Legion
- Elites: Veteran Tactical Squad, Legion
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Attack Bike Squadron, Legion
- Fast Attack: Dark Fury Assault Squad [Raven Guard]
- Fast Attack: Darkwing Storm Eagle [Raven Guard]
- Fast Attack: Falcon's Claws, The [White Scars]
- Fast Attack: Javelin Attack Speeder Squadron, Legion
- Fast Attack: Jetbike Sky Hunter Squadron, Legion
- Fast Attack: Land Speeder Squadron, Legion
- Fast Attack: Locutarus Storm Squad [Ultramarines]
- Fast Attack: Outrider Squad, Legion
- Fast Attack: Phalanx Warder Squad [Imperial Fists]
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Seeker Squad, Legion
- Fast Attack: Storm Eagle Assault Gunship, Legion Unit
- Fast Attack: Tarantula Sentry Gun Battery, Legion
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: White Scars Kyzagan Assault Speeder [White Scars]
- Fast Attack: Xiphon Interceptor
- HQ: Centurion, Legion
- HQ: Damocles Command Rhino
- HQ: Huscarl Squad [Imperial Fists]
- HQ: Knight-Errant
- HQ: Master of Armour
- HQ: Navigator
- HQ: Praetor Tribune, Legion
- HQ: Praetor, Legion
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Artillery Tank Squadron, Legion
- Heavy Support: Caestus Assault Ram, Legion
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Fire Raptor Gunship, Legion
- Heavy Support: Fulmentarus Terminator Squad [Ultramarines]
- Heavy Support: Heavy Support Squad, Legion
- Heavy Support: Jetbike Sky Slayer Support Squadron, Legion
- Heavy Support: Kharybdis Assault Claw, Legion Unit
- Heavy Support: Land Raider Battle Squadron, Legion
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Malcador Assault Tank Squadron, Legion
- Heavy Support: Predator Strike Armoured Squadron, Legion
- Heavy Support: Pyroclast Squad [Salamanders]
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Spartan Assault Tank, Legion Unit
- Heavy Support: Thallax Cohort
- Heavy Support: Vindicator Siege Tank Squadron, Legion
- Heavy Support: Vorax Class Battle-automata Maniple
- Heavy Support: Whirlwind Scorpius, Legion
- Lords of War: Cerberus Heavy Tank Destroyer, Legion
- Lords of War: Falchion Super-heavy Tank Destroyer, Legion
- Lords of War: Fellblade, Legion
- Lords of War: Glaive Special Weapons Tank, Legion
- Lords of War: Malcador Assault Tank, Legion
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- Lords of War: Stormblade, Legion
- Lords of War: Thunderhawk Gunship, Legion
- Lords of War: Thunderhawk Transporter, Legion
- Lords of War: Typhon Heavy Siege Tank, Legion
- No Force Org Slot: Command Squad, Legion
- No Force Org Slot: Dark Sons of Death Squad (Karaoghlanlar) [White Scars]
- No Force Org Slot: Huscarl Squad [Imperial Fists]
- No Force Org Slot: Invictarus Suzerain Squad [Ultramarines]
- Troops: Assault Squad, Legion
- Troops: Breacher Siege Squad, Legion
- Troops: Hussar Squadron, Legion
- Troops: Jetbike Sky Seeker Squadron, Legion
- Troops: Nullificators, Legion
- Troops: Reconnaissance Squad, Legion
- Troops: Tactical Squad, Legion
- Troops: Tactical Support Squad, Legion

### Dark Angels (84 entries)


- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Destroyer Squad, Legion
- Elites: Dreadnought Talon, Legion
- Elites: Dreadwing Interemptor Squad
- Elites: Inner Circle Knights Cenobium
- Elites: Inner Circle Knights Cenobium - Order of the Broken Claws
- Elites: Mortis Dreadnought, Legion
- Elites: Nullificators, Legion
- Elites: Quad Launcher Support Battery, Legion
- Elites: Rapier Weapons Battery, Legion
- Elites: Techmarine Covenant
- Elites: Terminator Squad, Legion
- Elites: Veteran Tactical Squad, Legion
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Attack Bike Squadron, Legion
- Fast Attack: Firewing Enigmatus Cabal
- Fast Attack: Javelin Attack Speeder Squadron, Legion
- Fast Attack: Jetbike Sky Hunter Squadron, Legion
- Fast Attack: Land Speeder Squadron, Legion
- Fast Attack: Outrider Squad, Legion
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Seeker Squad, Legion
- Fast Attack: Storm Eagle Assault Gunship, Legion Unit
- Fast Attack: Tarantula Sentry Gun Battery, Legion
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Centurion, Legion
- HQ: Damocles Command Rhino
- HQ: Knight-Errant
- HQ: Master of Armour
- HQ: Navigator
- HQ: Praetor Tribune, Legion
- HQ: Praetor, Legion
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Artillery Tank Squadron, Legion
- Heavy Support: Caestus Assault Ram, Legion
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Fire Raptor Gunship, Legion
- Heavy Support: Heavy Support Squad, Legion
- Heavy Support: Ironwing Excindio Class Battle-Automata
- Heavy Support: Jetbike Sky Slayer Support Squadron, Legion
- Heavy Support: Kharybdis Assault Claw, Legion Unit
- Heavy Support: Land Raider Battle Squadron, Legion
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Malcador Assault Tank Squadron, Legion
- Heavy Support: Predator Strike Armoured Squadron, Legion
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Spartan Assault Tank, Legion Unit
- Heavy Support: Thallax Cohort
- Heavy Support: Vindicator Siege Tank Squadron, Legion
- Heavy Support: Vorax Class Battle-automata Maniple
- Heavy Support: Whirlwind Scorpius, Legion
- Lords of War: Cerberus Heavy Tank Destroyer, Legion
- Lords of War: Falchion Super-heavy Tank Destroyer, Legion
- Lords of War: Fellblade, Legion
- Lords of War: Glaive Special Weapons Tank, Legion
- Lords of War: Malcador Assault Tank, Legion
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- Lords of War: Stormblade, Legion
- Lords of War: Thunderhawk Gunship, Legion
- Lords of War: Thunderhawk Transporter, Legion
- Lords of War: Typhon Heavy Siege Tank, Legion
- No Force Org Slot: Command Squad, Legion
- No Force Org Slot: Deathwing Companions Detachment
- Troops: Assault Squad, Legion
- Troops: Breacher Siege Squad, Legion
- Troops: Hussar Squadron, Legion
- Troops: Jetbike Sky Seeker Squadron, Legion
- Troops: Nullificators, Legion
- Troops: Reconnaissance Squad, Legion
- Troops: Tactical Squad, Legion
- Troops: Tactical Support Squad, Legion

### Blood Angels (82 entries)


- Elites: Angel's Tears, The
- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Crimson Paladins
- Elites: Dawnbreaker Cohort
- Elites: Destroyer Squad, Legion
- Elites: Dreadnought Talon, Legion
- Elites: Mortis Dreadnought, Legion
- Elites: Nullificators, Legion
- Elites: Quad Launcher Support Battery, Legion
- Elites: Rapier Weapons Battery, Legion
- Elites: Techmarine Covenant
- Elites: Terminator Squad, Legion
- Elites: Veteran Tactical Squad, Legion
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Attack Bike Squadron, Legion
- Fast Attack: Contemptor Incaendius Class Dreadnought
- Fast Attack: Javelin Attack Speeder Squadron, Legion
- Fast Attack: Jetbike Sky Hunter Squadron, Legion
- Fast Attack: Land Speeder Squadron, Legion
- Fast Attack: Outrider Squad, Legion
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Seeker Squad, Legion
- Fast Attack: Storm Eagle Assault Gunship, Legion Unit
- Fast Attack: Tarantula Sentry Gun Battery, Legion
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Centurion, Legion
- HQ: Damocles Command Rhino
- HQ: Knight-Errant
- HQ: Master of Armour
- HQ: Navigator
- HQ: Praetor Tribune, Legion
- HQ: Praetor, Legion
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Artillery Tank Squadron, Legion
- Heavy Support: Caestus Assault Ram, Legion
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Fire Raptor Gunship, Legion
- Heavy Support: Heavy Support Squad, Legion
- Heavy Support: Jetbike Sky Slayer Support Squadron, Legion
- Heavy Support: Kharybdis Assault Claw, Legion Unit
- Heavy Support: Land Raider Battle Squadron, Legion
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Malcador Assault Tank Squadron, Legion
- Heavy Support: Predator Strike Armoured Squadron, Legion
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Spartan Assault Tank, Legion Unit
- Heavy Support: Thallax Cohort
- Heavy Support: Vindicator Siege Tank Squadron, Legion
- Heavy Support: Vorax Class Battle-automata Maniple
- Heavy Support: Whirlwind Scorpius, Legion
- Lords of War: Cerberus Heavy Tank Destroyer, Legion
- Lords of War: Falchion Super-heavy Tank Destroyer, Legion
- Lords of War: Fellblade, Legion
- Lords of War: Glaive Special Weapons Tank, Legion
- Lords of War: Malcador Assault Tank, Legion
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- Lords of War: Stormblade, Legion
- Lords of War: Thunderhawk Gunship, Legion
- Lords of War: Thunderhawk Transporter, Legion
- Lords of War: Typhon Heavy Siege Tank, Legion
- No Force Org Slot: Command Squad, Legion
- Troops: Assault Squad, Legion
- Troops: Breacher Siege Squad, Legion
- Troops: Hussar Squadron, Legion
- Troops: Jetbike Sky Seeker Squadron, Legion
- Troops: Nullificators, Legion
- Troops: Reconnaissance Squad, Legion
- Troops: Tactical Squad, Legion
- Troops: Tactical Support Squad, Legion

### Space Wolves (82 entries)


- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Deathsworn, The
- Elites: Destroyer Squad, Legion
- Elites: Dreadnought Talon, Legion
- Elites: Mortis Dreadnought, Legion
- Elites: Nullificators, Legion
- Elites: Quad Launcher Support Battery, Legion
- Elites: Rapier Weapons Battery, Legion
- Elites: Techmarine Covenant
- Elites: Terminator Squad, Legion
- Elites: Varagyr Wolf Guard Terminator Squad
- Elites: Veteran Tactical Squad, Legion
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Attack Bike Squadron, Legion
- Fast Attack: Javelin Attack Speeder Squadron, Legion
- Fast Attack: Jetbike Sky Hunter Squadron, Legion
- Fast Attack: Land Speeder Squadron, Legion
- Fast Attack: Outrider Squad, Legion
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Seeker Squad, Legion
- Fast Attack: Storm Eagle Assault Gunship, Legion Unit
- Fast Attack: Tarantula Sentry Gun Battery, Legion
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Centurion, Legion
- HQ: Damocles Command Rhino
- HQ: Knight-Errant
- HQ: Master of Armour
- HQ: Navigator
- HQ: Praetor Tribune, Legion
- HQ: Praetor, Legion
- HQ: Priest of Fenris
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Artillery Tank Squadron, Legion
- Heavy Support: Caestus Assault Ram, Legion
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Fire Raptor Gunship, Legion
- Heavy Support: Heavy Support Squad, Legion
- Heavy Support: Jetbike Sky Slayer Support Squadron, Legion
- Heavy Support: Kharybdis Assault Claw, Legion Unit
- Heavy Support: Land Raider Battle Squadron, Legion
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Malcador Assault Tank Squadron, Legion
- Heavy Support: Predator Strike Armoured Squadron, Legion
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Spartan Assault Tank, Legion Unit
- Heavy Support: Thallax Cohort
- Heavy Support: Vindicator Siege Tank Squadron, Legion
- Heavy Support: Vorax Class Battle-automata Maniple
- Heavy Support: Whirlwind Scorpius, Legion
- Lords of War: Cerberus Heavy Tank Destroyer, Legion
- Lords of War: Falchion Super-heavy Tank Destroyer, Legion
- Lords of War: Fellblade, Legion
- Lords of War: Glaive Special Weapons Tank, Legion
- Lords of War: Malcador Assault Tank, Legion
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- Lords of War: Stormblade, Legion
- Lords of War: Thunderhawk Gunship, Legion
- Lords of War: Thunderhawk Transporter, Legion
- Lords of War: Typhon Heavy Siege Tank, Legion
- No Force Org Slot: Command Squad, Legion
- Troops: Assault Squad, Legion
- Troops: Breacher Siege Squad, Legion
- Troops: Grey Slayer Pack
- Troops: Hussar Squadron, Legion
- Troops: Jetbike Sky Seeker Squadron, Legion
- Troops: Nullificators, Legion
- Troops: Reconnaissance Squad, Legion
- Troops: Tactical Squad, Legion
- Troops: Tactical Support Squad, Legion

### Chaos Space Marines (109 entries)

Entries in square brackets are Legion-specific. A unit listed twice can be taken in either section.

- Elites: 'Iron Circle' Domitar-Ferrum Class Battle-automata Maniple [Iron Warriors]
- Elites: Apothecarion Detachment
- Elites: Atramentar Squad [Night Lords]
- Elites: Contekar Terminator Elite [Night Lords]
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Deathshroud Terminator Squad [Death Guard]
- Elites: Destroyer Squad, Legion
- Elites: Dominator Cohort [Iron Warriors]
- Elites: Dreadnought Talon, Legion
- Elites: Gal Vorbak Dark Brethren [Word Bearers]
- Elites: Justaerin Terminator Squad [Sons of Horus]
- Elites: Khenetai Blade Occult Cabal [Thousand Sons]
- Elites: Lernaean Terminator Squad [Alpha Legion]
- Elites: Mhara Gal Tainted Dreadnought [Word Bearers]
- Elites: Mortis Dreadnought, Legion
- Elites: Mortus Poisoner Squad [Death Guard]
- Elites: Nullificators, Legion
- Elites: Palatine Blade Squad [Emperor's Children]
- Elites: Phoenix Terminator Squad [Emperor's Children]
- Elites: Quad Launcher Support Battery, Legion
- Elites: Rampager Squads [World Eaters]
- Elites: Rapier Weapons Battery, Legion
- Elites: Red Butchers [World Eaters]
- Elites: Red Hand Destroyer Assault Squad [World Eaters]
- Elites: Sekhmet Terminator Cabal [Thousand Sons]
- Elites: Techmarine Covenant
- Elites: Terminator Squad, Legion
- Elites: Terror Squad [Night Lords]
- Elites: Veteran Tactical Squad, Legion
- Fast Attack: Ammitara Occult Intercession Cabal [Thousand Sons]
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Ashen Circle, The [Word Bearers]
- Fast Attack: Attack Bike Squadron, Legion
- Fast Attack: Headhunter Kill Teams [Alpha Legion]
- Fast Attack: Javelin Attack Speeder Squadron, Legion
- Fast Attack: Jetbike Sky Hunter Squadron, Legion
- Fast Attack: Land Speeder Squadron, Legion
- Fast Attack: Night Raptor Squad [Night Lords]
- Fast Attack: Outrider Squad, Legion
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Rampager Squads [World Eaters]
- Fast Attack: Reaver Attack Squad [Sons of Horus]
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Seeker Squad, Legion
- Fast Attack: Storm Eagle Assault Gunship, Legion Unit
- Fast Attack: Tarantula Sentry Gun Battery, Legion
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Centurion, Legion
- HQ: Contekar Terminator Elite [Night Lords]
- HQ: Damocles Command Rhino
- HQ: Deathshroud Terminator Squad [Death Guard]
- HQ: Master of Armour
- HQ: Navigator
- HQ: Praetor Tribune, Legion
- HQ: Praetor, Legion
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Artillery Tank Squadron, Legion
- Heavy Support: Caestus Assault Ram, Legion
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Castellax-Achea Battle Maniple [Thousand Sons]
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Fire Raptor Gunship, Legion
- Heavy Support: Grave Warden Terminator Squad [Death Guard]
- Heavy Support: Heavy Support Squad, Legion
- Heavy Support: Iron Havoc Support Squad [Iron Warriors]
- Heavy Support: Jetbike Sky Slayer Support Squadron, Legion
- Heavy Support: Kakophoni of the Emperor's Children, The [Emperor's Children]
- Heavy Support: Kharybdis Assault Claw, Legion Unit
- Heavy Support: Land Raider Battle Squadron, Legion
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Malcador Assault Tank Squadron, Legion
- Heavy Support: Predator Strike Armoured Squadron, Legion
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Spartan Assault Tank, Legion Unit
- Heavy Support: Sun Killer Squad [Emperor's Children]
- Heavy Support: Thallax Cohort
- Heavy Support: Tyrant Siege Terminator Squad [Iron Warriors]
- Heavy Support: Vindicator Siege Tank Squadron, Legion
- Heavy Support: Vorax Class Battle-automata Maniple
- Heavy Support: Whirlwind Scorpius, Legion
- Lords of War: Cerberus Heavy Tank Destroyer, Legion
- Lords of War: Falchion Super-heavy Tank Destroyer, Legion
- Lords of War: Fellblade, Legion
- Lords of War: Glaive Special Weapons Tank, Legion
- Lords of War: Malcador Assault Tank, Legion
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- Lords of War: Stormblade, Legion
- Lords of War: Thunderhawk Gunship, Legion
- Lords of War: Thunderhawk Transporter, Legion
- Lords of War: Typhon Heavy Siege Tank, Legion
- No Force Org Slot: Command Squad, Legion
- Troops: Assault Squad, Legion
- Troops: Breacher Siege Squad, Legion
- Troops: Hussar Squadron, Legion
- Troops: Jetbike Sky Seeker Squadron, Legion
- Troops: Nullificators, Legion
- Troops: Reconnaissance Squad, Legion
- Troops: Tactical Squad, Legion
- Troops: Tactical Support Squad, Legion

## Known issues

- A Heresy Warlord and the host list's own Warlord option are separate, so the data does not stop a list from naming two Warlords. Pick one.

- Several Heresy vehicles also exist as 40k Forge World units in the same lists (e.g. Sicaran, Spartan, Fellblade, Deredeo, Storm Eagle, Fire Raptor). Both versions are offered; the Heresy one is marked "(Heresy)".
- Some rules have no text in the source and no match elsewhere: Exemplary Tribune, Extremely Bulky, Missile.
- Points and options come from the community data and have not been checked against the Heresy books.

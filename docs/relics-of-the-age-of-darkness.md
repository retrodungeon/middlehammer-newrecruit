# Relics of the Age of Darkness (optional add-on)

Horus Heresy 1st Edition units for 6th and 7th Edition Army Lists. **Off by default.** In a list whose Army List is a 6th or 7th Edition book, tick **Configuration → Relics of the Age of Darkness → Use Horus Heresy 1st Edition units**; the Heresy units then appear in the normal sections, marked "(Heresy)" like Forge World "(FW)" and Imperial Armour "(IA)" units. Both players should agree before using them.

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
| Heresy army construction removed | The Crusade chart's compulsory choices do not apply under the 5th Edition chart: the "(Compulsory)" labels, compulsory-slot categories and "Compulsory" options are removed (unit rules that mention compulsory HQ or Troops choices are kept, as the 5th Edition chart has compulsory choices too). The Warlord option stays (for Slay the Warlord) but is no longer required. "Master of the Legion" (Rite of War choice, one per 1,000 points) is hidden; Command Squads remain available. |
| Not converted (content policy) | Fan-made: Necron, Asuryani and Mournival Units catalogues. Varangian Heresy Legions (provenance unverified). The Heresy copy of Codex: Chaos Daemons (2013), already in the data. |

## Units per faction

Names follow the Heresy books ("Legion Praetor", "The Ebon Keshig"); every unit ends in "(Heresy)". Master of Armour is not offered: it needs the Armoured Breakthrough Rite of War.

### Space Marines (100 entries)

Entries in square brackets are Legion-specific. A unit listed twice can be taken in either section.

- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Dark Sons of Death Squad (Karaoghlanlar) [White Scars]
- Elites: Deliverer Squad [Raven Guard]
- Elites: Firedrake Terminator Squad [Salamanders]
- Elites: Gorgon Terminator Squad [Iron Hands]
- Elites: Invictarus Suzerain Squad [Ultramarines]
- Elites: Legion Destroyer Squad
- Elites: Legion Dreadnought Talon
- Elites: Legion Mortis Dreadnought
- Elites: Legion Nullificators
- Elites: Legion Quad Launcher Support Battery
- Elites: Legion Rapier Weapons Battery
- Elites: Legion Terminator Squad
- Elites: Legion Veteran Tactical Squad
- Elites: Medusan Immortals [Iron Hands]
- Elites: Mor Deythan Strike Squad [Raven Guard]
- Elites: Nemesis Destroyer Squad [Ultramarines]
- Elites: Techmarine Covenant
- Elites: Templar Brethren [Imperial Fists]
- Elites: The Ebon Keshig [White Scars]
- Elites: The Golden Keshig [White Scars]
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Dark Fury Assault Squad [Raven Guard]
- Fast Attack: Darkwing Storm Eagle [Raven Guard]
- Fast Attack: Legion Attack Bike Squadron
- Fast Attack: Legion Javelin Attack Speeder Squadron
- Fast Attack: Legion Jetbike Sky Hunter Squadron
- Fast Attack: Legion Land Speeder Squadron
- Fast Attack: Legion Outrider Squad
- Fast Attack: Legion Seeker Squad
- Fast Attack: Legion Storm Eagle Assault Gunship
- Fast Attack: Legion Tarantula Sentry Gun Battery
- Fast Attack: Locutarus Storm Squad [Ultramarines]
- Fast Attack: Phalanx Warder Squad [Imperial Fists]
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: The Falcon's Claws [White Scars]
- Fast Attack: White Scars Kyzagan Assault Speeder [White Scars]
- Fast Attack: Xiphon Interceptor
- HQ: Damocles Command Rhino
- HQ: Huscarl Squad [Imperial Fists]
- HQ: Knight-Errant
- HQ: Legion Centurion
- HQ: Legion Praetor
- HQ: Legion Praetor Tribune
- HQ: Navigator
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Fulmentarus Terminator Squad [Ultramarines]
- Heavy Support: Legion Artillery Tank Squadron
- Heavy Support: Legion Caestus Assault Ram
- Heavy Support: Legion Fire Raptor Gunship
- Heavy Support: Legion Heavy Support Squad
- Heavy Support: Legion Jetbike Sky Slayer Support Squadron
- Heavy Support: Legion Kharybdis Assault Claw
- Heavy Support: Legion Land Raider Battle Squadron
- Heavy Support: Legion Malcador Assault Tank Squadron
- Heavy Support: Legion Predator Strike Armoured Squadron
- Heavy Support: Legion Spartan Assault Tank
- Heavy Support: Legion Vindicator Siege Tank Squadron
- Heavy Support: Legion Whirlwind Scorpius
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Pyroclast Squad [Salamanders]
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Thallax Cohort
- Heavy Support: Vorax Class Battle-automata Maniple
- Lords of War: Legion Cerberus Heavy Tank Destroyer
- Lords of War: Legion Falchion Super-heavy Tank Destroyer
- Lords of War: Legion Fellblade
- Lords of War: Legion Glaive Special Weapons Tank
- Lords of War: Legion Malcador Assault Tank
- Lords of War: Legion Stormblade
- Lords of War: Legion Thunderhawk Gunship
- Lords of War: Legion Thunderhawk Transporter
- Lords of War: Legion Typhon Heavy Siege Tank
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- No Force Org Slot: Dark Sons of Death Squad (Karaoghlanlar) [White Scars]
- No Force Org Slot: Huscarl Squad [Imperial Fists]
- No Force Org Slot: Invictarus Suzerain Squad [Ultramarines]
- No Force Org Slot: Legion Command Squad
- Troops: Legion Assault Squad
- Troops: Legion Breacher Siege Squad
- Troops: Legion Hussar Squadron
- Troops: Legion Jetbike Sky Seeker Squadron
- Troops: Legion Nullificators
- Troops: Legion Reconnaissance Squad
- Troops: Legion Tactical Squad
- Troops: Legion Tactical Support Squad

### Dark Angels (83 entries)

- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Dreadwing Interemptor Squad
- Elites: Inner Circle Knights Cenobium
- Elites: Inner Circle Knights Cenobium - Order of the Broken Claws
- Elites: Legion Destroyer Squad
- Elites: Legion Dreadnought Talon
- Elites: Legion Mortis Dreadnought
- Elites: Legion Nullificators
- Elites: Legion Quad Launcher Support Battery
- Elites: Legion Rapier Weapons Battery
- Elites: Legion Terminator Squad
- Elites: Legion Veteran Tactical Squad
- Elites: Techmarine Covenant
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Firewing Enigmatus Cabal
- Fast Attack: Legion Attack Bike Squadron
- Fast Attack: Legion Javelin Attack Speeder Squadron
- Fast Attack: Legion Jetbike Sky Hunter Squadron
- Fast Attack: Legion Land Speeder Squadron
- Fast Attack: Legion Outrider Squad
- Fast Attack: Legion Seeker Squad
- Fast Attack: Legion Storm Eagle Assault Gunship
- Fast Attack: Legion Tarantula Sentry Gun Battery
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Damocles Command Rhino
- HQ: Knight-Errant
- HQ: Legion Centurion
- HQ: Legion Praetor
- HQ: Legion Praetor Tribune
- HQ: Navigator
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Ironwing Excindio Class Battle-Automata
- Heavy Support: Legion Artillery Tank Squadron
- Heavy Support: Legion Caestus Assault Ram
- Heavy Support: Legion Fire Raptor Gunship
- Heavy Support: Legion Heavy Support Squad
- Heavy Support: Legion Jetbike Sky Slayer Support Squadron
- Heavy Support: Legion Kharybdis Assault Claw
- Heavy Support: Legion Land Raider Battle Squadron
- Heavy Support: Legion Malcador Assault Tank Squadron
- Heavy Support: Legion Predator Strike Armoured Squadron
- Heavy Support: Legion Spartan Assault Tank
- Heavy Support: Legion Vindicator Siege Tank Squadron
- Heavy Support: Legion Whirlwind Scorpius
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Thallax Cohort
- Heavy Support: Vorax Class Battle-automata Maniple
- Lords of War: Legion Cerberus Heavy Tank Destroyer
- Lords of War: Legion Falchion Super-heavy Tank Destroyer
- Lords of War: Legion Fellblade
- Lords of War: Legion Glaive Special Weapons Tank
- Lords of War: Legion Malcador Assault Tank
- Lords of War: Legion Stormblade
- Lords of War: Legion Thunderhawk Gunship
- Lords of War: Legion Thunderhawk Transporter
- Lords of War: Legion Typhon Heavy Siege Tank
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- No Force Org Slot: Deathwing Companions Detachment
- No Force Org Slot: Legion Command Squad
- Troops: Legion Assault Squad
- Troops: Legion Breacher Siege Squad
- Troops: Legion Hussar Squadron
- Troops: Legion Jetbike Sky Seeker Squadron
- Troops: Legion Nullificators
- Troops: Legion Reconnaissance Squad
- Troops: Legion Tactical Squad
- Troops: Legion Tactical Support Squad

### Blood Angels (81 entries)

- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Crimson Paladins
- Elites: Dawnbreaker Cohort
- Elites: Legion Destroyer Squad
- Elites: Legion Dreadnought Talon
- Elites: Legion Mortis Dreadnought
- Elites: Legion Nullificators
- Elites: Legion Quad Launcher Support Battery
- Elites: Legion Rapier Weapons Battery
- Elites: Legion Terminator Squad
- Elites: Legion Veteran Tactical Squad
- Elites: Techmarine Covenant
- Elites: The Angel's Tears
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Contemptor Incaendius Class Dreadnought
- Fast Attack: Legion Attack Bike Squadron
- Fast Attack: Legion Javelin Attack Speeder Squadron
- Fast Attack: Legion Jetbike Sky Hunter Squadron
- Fast Attack: Legion Land Speeder Squadron
- Fast Attack: Legion Outrider Squad
- Fast Attack: Legion Seeker Squad
- Fast Attack: Legion Storm Eagle Assault Gunship
- Fast Attack: Legion Tarantula Sentry Gun Battery
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Damocles Command Rhino
- HQ: Knight-Errant
- HQ: Legion Centurion
- HQ: Legion Praetor
- HQ: Legion Praetor Tribune
- HQ: Navigator
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Legion Artillery Tank Squadron
- Heavy Support: Legion Caestus Assault Ram
- Heavy Support: Legion Fire Raptor Gunship
- Heavy Support: Legion Heavy Support Squad
- Heavy Support: Legion Jetbike Sky Slayer Support Squadron
- Heavy Support: Legion Kharybdis Assault Claw
- Heavy Support: Legion Land Raider Battle Squadron
- Heavy Support: Legion Malcador Assault Tank Squadron
- Heavy Support: Legion Predator Strike Armoured Squadron
- Heavy Support: Legion Spartan Assault Tank
- Heavy Support: Legion Vindicator Siege Tank Squadron
- Heavy Support: Legion Whirlwind Scorpius
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Thallax Cohort
- Heavy Support: Vorax Class Battle-automata Maniple
- Lords of War: Legion Cerberus Heavy Tank Destroyer
- Lords of War: Legion Falchion Super-heavy Tank Destroyer
- Lords of War: Legion Fellblade
- Lords of War: Legion Glaive Special Weapons Tank
- Lords of War: Legion Malcador Assault Tank
- Lords of War: Legion Stormblade
- Lords of War: Legion Thunderhawk Gunship
- Lords of War: Legion Thunderhawk Transporter
- Lords of War: Legion Typhon Heavy Siege Tank
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- No Force Org Slot: Legion Command Squad
- Troops: Legion Assault Squad
- Troops: Legion Breacher Siege Squad
- Troops: Legion Hussar Squadron
- Troops: Legion Jetbike Sky Seeker Squadron
- Troops: Legion Nullificators
- Troops: Legion Reconnaissance Squad
- Troops: Legion Tactical Squad
- Troops: Legion Tactical Support Squad

### Space Wolves (81 entries)

- Elites: Apothecarion Detachment
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Legion Destroyer Squad
- Elites: Legion Dreadnought Talon
- Elites: Legion Mortis Dreadnought
- Elites: Legion Nullificators
- Elites: Legion Quad Launcher Support Battery
- Elites: Legion Rapier Weapons Battery
- Elites: Legion Terminator Squad
- Elites: Legion Veteran Tactical Squad
- Elites: Techmarine Covenant
- Elites: The Deathsworn
- Elites: Varagyr Wolf Guard Terminator Squad
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Legion Attack Bike Squadron
- Fast Attack: Legion Javelin Attack Speeder Squadron
- Fast Attack: Legion Jetbike Sky Hunter Squadron
- Fast Attack: Legion Land Speeder Squadron
- Fast Attack: Legion Outrider Squad
- Fast Attack: Legion Seeker Squad
- Fast Attack: Legion Storm Eagle Assault Gunship
- Fast Attack: Legion Tarantula Sentry Gun Battery
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: Xiphon Interceptor
- HQ: Damocles Command Rhino
- HQ: Knight-Errant
- HQ: Legion Centurion
- HQ: Legion Praetor
- HQ: Legion Praetor Tribune
- HQ: Navigator
- HQ: Priest of Fenris
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Legion Artillery Tank Squadron
- Heavy Support: Legion Caestus Assault Ram
- Heavy Support: Legion Fire Raptor Gunship
- Heavy Support: Legion Heavy Support Squad
- Heavy Support: Legion Jetbike Sky Slayer Support Squadron
- Heavy Support: Legion Kharybdis Assault Claw
- Heavy Support: Legion Land Raider Battle Squadron
- Heavy Support: Legion Malcador Assault Tank Squadron
- Heavy Support: Legion Predator Strike Armoured Squadron
- Heavy Support: Legion Spartan Assault Tank
- Heavy Support: Legion Vindicator Siege Tank Squadron
- Heavy Support: Legion Whirlwind Scorpius
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Thallax Cohort
- Heavy Support: Vorax Class Battle-automata Maniple
- Lords of War: Legion Cerberus Heavy Tank Destroyer
- Lords of War: Legion Falchion Super-heavy Tank Destroyer
- Lords of War: Legion Fellblade
- Lords of War: Legion Glaive Special Weapons Tank
- Lords of War: Legion Malcador Assault Tank
- Lords of War: Legion Stormblade
- Lords of War: Legion Thunderhawk Gunship
- Lords of War: Legion Thunderhawk Transporter
- Lords of War: Legion Typhon Heavy Siege Tank
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- No Force Org Slot: Legion Command Squad
- Troops: Grey Slayer Pack
- Troops: Legion Assault Squad
- Troops: Legion Breacher Siege Squad
- Troops: Legion Hussar Squadron
- Troops: Legion Jetbike Sky Seeker Squadron
- Troops: Legion Nullificators
- Troops: Legion Reconnaissance Squad
- Troops: Legion Tactical Squad
- Troops: Legion Tactical Support Squad

### Chaos Space Marines (108 entries)

Entries in square brackets are Legion-specific. A unit listed twice can be taken in either section.

- Elites: 'Iron Circle' Domitar-Ferrum Class Battle-automata Maniple [Iron Warriors]
- Elites: Apothecarion Detachment
- Elites: Atramentar Squad [Night Lords]
- Elites: Contekar Terminator Elite [Night Lords]
- Elites: Contemptor Dreadnought Talon
- Elites: Contemptor-Cortus Class Dreadnought Talon
- Elites: Contemptor-Mortis Dreadnought
- Elites: Deathshroud Terminator Squad [Death Guard]
- Elites: Dominator Cohort [Iron Warriors]
- Elites: Gal Vorbak Dark Brethren [Word Bearers]
- Elites: Justaerin Terminator Squad [Sons of Horus]
- Elites: Khenetai Blade Occult Cabal [Thousand Sons]
- Elites: Legion Destroyer Squad
- Elites: Legion Dreadnought Talon
- Elites: Legion Mortis Dreadnought
- Elites: Legion Nullificators
- Elites: Legion Quad Launcher Support Battery
- Elites: Legion Rapier Weapons Battery
- Elites: Legion Terminator Squad
- Elites: Legion Veteran Tactical Squad
- Elites: Lernaean Terminator Squad [Alpha Legion]
- Elites: Mhara Gal Tainted Dreadnought [Word Bearers]
- Elites: Mortus Poisoner Squad [Death Guard]
- Elites: Palatine Blade Squad [Emperor's Children]
- Elites: Phoenix Terminator Squad [Emperor's Children]
- Elites: Rampager Squads [World Eaters]
- Elites: Red Butchers [World Eaters]
- Elites: Red Hand Destroyer Assault Squad [World Eaters]
- Elites: Sekhmet Terminator Cabal [Thousand Sons]
- Elites: Techmarine Covenant
- Elites: Terror Squad [Night Lords]
- Fast Attack: Ammitara Occult Intercession Cabal [Thousand Sons]
- Fast Attack: Anvillus Pattern Dreadclaw Drop Pod Unit
- Fast Attack: Headhunter Kill Teams [Alpha Legion]
- Fast Attack: Legion Attack Bike Squadron
- Fast Attack: Legion Javelin Attack Speeder Squadron
- Fast Attack: Legion Jetbike Sky Hunter Squadron
- Fast Attack: Legion Land Speeder Squadron
- Fast Attack: Legion Outrider Squad
- Fast Attack: Legion Seeker Squad
- Fast Attack: Legion Storm Eagle Assault Gunship
- Fast Attack: Legion Tarantula Sentry Gun Battery
- Fast Attack: Night Raptor Squad [Night Lords]
- Fast Attack: Primaris-Lightning Strike Fighter
- Fast Attack: Rampager Squads [World Eaters]
- Fast Attack: Reaver Attack Squad [Sons of Horus]
- Fast Attack: Sabre Strike Tank Squadron
- Fast Attack: Terrax Pattern Termite Assault Drill Unit
- Fast Attack: The Ashen Circle [Word Bearers]
- Fast Attack: Xiphon Interceptor
- HQ: Contekar Terminator Elite [Night Lords]
- HQ: Damocles Command Rhino
- HQ: Deathshroud Terminator Squad [Death Guard]
- HQ: Legion Centurion
- HQ: Legion Praetor
- HQ: Legion Praetor Tribune
- HQ: Navigator
- Heavy Support: Achilles-Alpha Pattern Land Raider
- Heavy Support: Arquitor Bombard
- Heavy Support: Castellax Class Battle-Automata Maniple
- Heavy Support: Castellax-Achea Battle Maniple [Thousand Sons]
- Heavy Support: Deathstorm Drop Pod
- Heavy Support: Deredeo Pattern Dreadnought
- Heavy Support: Grave Warden Terminator Squad [Death Guard]
- Heavy Support: Iron Havoc Support Squad [Iron Warriors]
- Heavy Support: Legion Artillery Tank Squadron
- Heavy Support: Legion Caestus Assault Ram
- Heavy Support: Legion Fire Raptor Gunship
- Heavy Support: Legion Heavy Support Squad
- Heavy Support: Legion Jetbike Sky Slayer Support Squadron
- Heavy Support: Legion Kharybdis Assault Claw
- Heavy Support: Legion Land Raider Battle Squadron
- Heavy Support: Legion Malcador Assault Tank Squadron
- Heavy Support: Legion Predator Strike Armoured Squadron
- Heavy Support: Legion Spartan Assault Tank
- Heavy Support: Legion Vindicator Siege Tank Squadron
- Heavy Support: Legion Whirlwind Scorpius
- Heavy Support: Leviathan Siege Dreadnought Talon
- Heavy Support: Sicaran Arcus Strike Tank
- Heavy Support: Sicaran Battle Tank Squadron
- Heavy Support: Sicaran Omega Tank Destroyer Squadron
- Heavy Support: Sicaran Punisher Assault Tank Squadron
- Heavy Support: Sicaran Venator Tank Destroyer Squadron
- Heavy Support: Sun Killer Squad [Emperor's Children]
- Heavy Support: Thallax Cohort
- Heavy Support: The Kakophoni of the Emperor's Children [Emperor's Children]
- Heavy Support: Tyrant Siege Terminator Squad [Iron Warriors]
- Heavy Support: Vorax Class Battle-automata Maniple
- Lords of War: Legion Cerberus Heavy Tank Destroyer
- Lords of War: Legion Falchion Super-heavy Tank Destroyer
- Lords of War: Legion Fellblade
- Lords of War: Legion Glaive Special Weapons Tank
- Lords of War: Legion Malcador Assault Tank
- Lords of War: Legion Stormblade
- Lords of War: Legion Thunderhawk Gunship
- Lords of War: Legion Thunderhawk Transporter
- Lords of War: Legion Typhon Heavy Siege Tank
- Lords of War: Mastadon Heavy Assault Transport
- Lords of War: Sokar Pattern Stormbird
- No Force Org Slot: Legion Command Squad
- Troops: Legion Assault Squad
- Troops: Legion Breacher Siege Squad
- Troops: Legion Hussar Squadron
- Troops: Legion Jetbike Sky Seeker Squadron
- Troops: Legion Nullificators
- Troops: Legion Reconnaissance Squad
- Troops: Legion Tactical Squad
- Troops: Legion Tactical Support Squad

## Known issues

- A Heresy Warlord and the host list's own Warlord option are separate, so the data does not stop a list from naming two Warlords. Pick one.

- Several Heresy vehicles also exist as 40k Forge World units in the same lists (e.g. Sicaran, Spartan, Fellblade, Deredeo, Storm Eagle, Fire Raptor). Both versions are offered; the Heresy one is marked "(Heresy)".
- Some rules have no text in the source and no match elsewhere: Exemplary Tribune, Extremely Bulky, Missile.
- Points and options come from the community data and have not been checked against the Heresy books.

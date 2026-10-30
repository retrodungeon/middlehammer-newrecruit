"""Rules text for 6th Edition lists.

The 6th Edition source (BattleScribe 1.14b) mostly records special rules as a name and a
page reference, with no text. Each empty rule is filled, in order of preference, from:

  1. CODEX_TEXT below: the 6th Edition codex's rule, written out in full in our own words
     from the maintainer's copy of the book (the books' wording is not copied);
  2. the 5th Edition core rules (universal special rules; the Unification plays on the 5th
     Edition core, so these are the versions that apply);
  3. the same faction's 7th Edition codex data, tagged "(7th Ed wording)";
  4. the 7th Edition core rules, tagged "(7th Ed wording)".

Rules none of these cover keep their name only and are listed in the build report.
"""
import re
from pathlib import Path
import xml.etree.ElementTree as ET

CACHE = Path(__file__).resolve().parents[1] / "upstream-cache"
TAG = " (7th Ed wording)"

# 6th Edition source catalogue -> 7th Edition source catalogue of the same faction.
SEVENTH = {
    "Space Marines": "wh40k-7th-edition/Space Marines - Codex (2015).cat",
    "Tau": "wh40k-7th-edition/Tau - Codex (2015).cat",
    "Dark Angels": "wh40k-7th-edition/Dark Angels - Codex (2015).cat",
    "Eldar": "wh40k-7th-edition/Eldar Craftworlds - Codex (2015).cat",
    "Chaos Daemons (40K)": "wh40k-7th-edition/Chaos Daemons (40K) - Codex.cat",
    "Chaos Space Marines": "wh40k-7th-edition/Chaos Space Marines - Codex.cat",
    "Orks": "wh40k-7th-edition/Orks - Codex.cat",
}

# {faction key: {rule name: text}}. Written from the 6th Edition codexes (Codex: Space
# Marines 2013, Codex: Tau Empire 2013), page numbers in comments.
_UM = ("Combat Doctrines: each of the three doctrines below can be used once per game. At the start of your turn "
       "you may declare one (only one per turn); it lasts until the start of your next turn. "
       "Tactical Doctrine: models in the detachment re-roll To Hit rolls of 1 in the Shooting phase; models in its "
       "Tactical Squads re-roll all failed To Hit rolls in the Shooting phase instead. "
       "Assault Doctrine: units in the detachment may re-roll their charge range; models in its Assault Squads, Bike "
       "Squads and Attack Bike Squads gain Fleet instead. "
       "Devastator Doctrine: models in the detachment may re-roll To Hit rolls made as Snap Shots (including "
       "Overwatch); models in its Devastator Squads gain Relentless unless they disembarked from a transport in that "
       "Movement phase.")
_WS = ("Born in the Saddle: Bike models in the detachment automatically pass Dangerous Terrain tests, add 1 to their "
       "Jink cover saves and add 1 to their Strength for Hammer of Wrath hits. "
       "Fight on the Move: models in the detachment have Hit & Run, except in units that include Terminator armour, "
       "Devastator Centurions or Assault Centurions.")
_IF = ("Bolter Drill: models in the detachment re-roll To Hit rolls of 1 with bolt pistols, boltguns, storm bolters, "
       "heavy bolters and combi-weapons firing as boltguns (not Hellfire, Kraken, Vengeance or Dragonfire rounds). "
       "Siege Masters: models in the detachment's Devastator Squads and Centurion Devastator Squads have Tank "
       "Hunters and add 1 to their rolls on the Building Damage table.")
_BT = ("Accept Any Challenge, No Matter the Odds: Black Templars characters in a challenge re-roll failed To Hit rolls "
       "and have Rending. "
       "Crusaders: Black Templars models have the Crusader and Adamantium Will special rules, and Black Templars "
       "detachments may take Crusader Squads.")
_SAL = ("Flamecraft: models in the detachment may re-roll saves against Wounds from flamer weapons; their own flamer "
        "weapons may re-roll failed To Wound rolls and armour penetration rolls that fail to glance or penetrate. "
        "Master Artisans: when the army is chosen, each character in the detachment may make one of his weapons "
        "(including one bought as an upgrade) Master-crafted at no cost.")
_RG = ("Strike from the Shadows: models in the detachment have Scout, and Stealth during the first game turn; units "
       "that include Bulky or Very Bulky models gain neither. "
       "Winged Deliverance: Jump Infantry in the detachment may use their jump packs in both the Movement and Assault "
       "phases of the same turn, and must re-roll failed To Wound rolls for their Hammer of Wrath hits.")
_IH = ("The Flesh is Weak: models in the detachment have Feel No Pain (6+); a model with a better Feel No Pain uses "
       "the better one. "
       "Machine Empathy: all vehicles and characters in the detachment have It Will Not Die (vehicles included, though "
       "they lack Chapter Tactics), and its Techmarines and Masters of the Forge add 1 to Blessing of the Omnissiah "
       "rolls.")

# Codex: Space Marines (2013). Keys are rule names as the source spells them (normalised).
CODEX_TEXT = {"Space Marines": {
    "Chapter Tactics": "Each Space Marine detachment chooses a Chapter (tell your opponent). Models with this rule "
                       "follow that Chapter's tactics: Ultramarines, White Scars, Imperial Fists, Black Templars, "
                       "Salamanders, Raven Guard or Iron Hands. A successor Chapter uses its founding Chapter's tactics "
                       "(Black Templars have their own); a Chapter of your own invention picks the founding Chapter it "
                       "descends from. Units and special characters tied to a Chapter can only be taken in a "
                       "detachment of that Chapter.",
    "Chapter Tactics (Ultramarines)": _UM, "Chapter Tactics (White Scars)": _WS,
    "Chapter Tactics (Imperial Fists)": _IF, "Chapter Tactics (Black Templars)": _BT,
    "Chapter Tactics (Salamanders)": _SAL, "Chapter Tactics (Raven Guard)": _RG, "Chapter Tactics (Iron Hands)": _IH,
    # The supplements name each tactic separately.
    "Chapter Tactics: Tactical": _UM, "Chapter Tactics: Assault": _UM, "Chapter Tactics: Devastator": _UM,
    "Chapter Tactics: Born in the Saddle": _WS.split(" Fight on the Move")[0],
    "Chapter Tactics: Fight on the Move": "Fight on the Move" + _WS.split(" Fight on the Move")[1],
    "Chapter Tactics: Bolter Drill": _IF.split(" Siege Masters")[0],
    "Chapter Tactics: Siegemasters": "Siege Masters" + _IF.split(" Siege Masters")[1],
    "Chapter Tactics: Accept Any Challenges, No Matter the Odds": _BT.split(" Crusaders")[0],
    "Chapter Tactics: Crusaders": "Crusaders" + _BT.split(" Crusaders")[1],
    "Chapter Tactics: Flamecraft": _SAL.split(" Master Artisans")[0],
    "Chapter Tactics: Master Artisan": "Master Artisans" + _SAL.split(" Master Artisans")[1],
    "Chapter Tactics: Strike from the Shadows": _RG.split(" Winged Deliverance")[0],
    "Chapter Tactics: Wings of Deliverance": "Winged Deliverance" + _RG.split(" Winged Deliverance")[1],
    "Chapter Tactics: The Flesh is Weak": _IH.split(" Machine Empathy")[0],
    "Chapter Tactics: Machine Empathy": "Machine Empathy" + _IH.split(" Machine Empathy")[1],
    "Combat Squads": "A full-strength ten-model unit with this rule may split into two five-model units of the same "
                     "type. Decide which units split, and which models go where, immediately before determining "
                     "Warlord Traits (i.e. before deployment). Each half is a separate unit for all purposes, "
                     "including unit counts and Reserves, and the split is permanent for the battle. Both halves may "
                     "start embarked in the same transport if it has room. A Bike Squad is at full strength with eight "
                     "Bikers and one Attack Bike; it splits into five Bikers, and three Bikers plus the Attack Bike.",
    "Orbital Bombardment": "Chapter Master only. Once per game, in his Shooting phase, he may call an orbital "
                           "bombardment instead of firing: Range Infinite, S10, AP1, Ordnance 1, Barrage, Large Blast, "
                           "Orbital. He and his unit may still charge the target that turn. Orbital: if the scatter "
                           "dice shows an arrow, the blast always scatters the full 2D6\" regardless of Ballistic Skill.",
    "Honour or Death": "A model with this rule must always issue and accept a challenge whenever possible.",
    "Heroic Intervention": "Vanguard Veteran Squads ignore the penalty for disordered charges, and a Vanguard Veteran "
                           "Sergeant automatically passes the Initiative test to make a Glorious Intervention.",
    "Decimator Protocols": "Centurions may fire up to two weapons each Shooting phase, at the same target.",
    "Escort Craft": "A Stormtalon in Reserve may escort one friendly unit in Reserve from its detachment (not a unit "
                    "arriving by Deep Strike or Outflank, and not another Stormtalon; at most one Stormtalon per unit, "
                    "or per group of units rolled for together). Do not roll Reserves for the Stormtalon: it arrives "
                    "with the escorted unit, moving on within 6\" of where that unit entered.",
    "Aid Unlooked For": "The Legion of the Damned ignore Chapter Tactics and cannot be joined by Independent "
                        "Characters. They always start in Reserve and arrive by Deep Strike; you may re-roll the "
                        "scatter dice when they do.",
    "Flaming Projectiles": "Ranged attacks made by the Legion of the Damned have Ignores Cover.",
    "Unyielding Spectres": "The Legion of the Damned have a 3+ invulnerable save.",
    "God of War": "Marneus Calgar and all friendly units with Chapter Tactics (Ultramarines) may choose to pass or "
                  "fail any Morale check. If Calgar is your Warlord, one Combat Doctrine may be used twice in the "
                  "game (declared when used the second time).",
    "Titanic Might": "Marneus Calgar re-rolls failed armour penetration rolls against vehicles in close combat, and "
                     "may re-roll glancing hits to try for a penetrating hit (the second roll stands).",
    "Battle-forged Heroes": "If Sicarius is in the army, one Ultramarines Tactical Squad (chosen during deployment) "
                            "gains one of Counter-attack, Infiltrate, Scout or Tank Hunters, free.",
    "Rites of Battle": "While Sicarius is on the battlefield, friendly units with Chapter Tactics (Ultramarines) may "
                       "use his Leadership for Morale and Pinning tests.",
    "Surprise Attack": "While Sicarius is on the battlefield, add 1 to your Reserve Rolls.",
    "Coup de Grace": "Instead of his normal close combat attacks, Sicarius may make a single Attack with the Tempest "
                     "Blade at +2 Strength with Instant Death.",
    "Gift of Prescience": "If Tigurius is in the army, you may re-roll any Reserve Rolls for units from his "
                          "detachment, even successful ones.",
    "Master Psyker": "When generating psychic powers, Tigurius may re-roll any or all of the dice.",
    "Eye of Vengeance": "All of Sergeant Telion's shooting hits are Precision Shots.",
    "Voice of Experience": "If Telion neither shoots nor Runs in the Shooting phase, one model in his squad may use "
                           "his Ballistic Skill that phase (declare before any shots are fired).",
    "Ultramarine Tank Commander": "Chronus is bought as an upgrade commanding an Ultramarines tank. That tank has It "
                                  "Will Not Die, ignores Crew Shaken and Crew Stunned (still losing a Hull Point), "
                                  "and uses his BS 5. He is a passenger taking no transport space (even in a tank "
                                  "without Transport Capacity) and cannot disembark voluntarily. If the tank is wrecked "
                                  "or explodes he follows the normal passenger rules (emergency disembarkation if it has "
                                  "no Access Points); afterwards he uses his own profile with And They Shall Know No "
                                  "Fear, Chapter Tactics (Ultramarines) and Independent Character, and may not command "
                                  "another tank.",
    "Prey's Bane": "Kor'sarro Khan's To Wound rolls of 6 have Instant Death.",
    "Master of the Hunt": "If Khan is your Warlord, friendly models with Chapter Tactics (White Scars) that are Bikes "
                          "or have Dedicated Transports have Scout.",
    "The Forgefather": "If Vulkan He'stan is your Warlord, meltaguns, combi-meltas and multi-meltas in his "
                       "detachment are Master-crafted.",
    "See, But Remain Unseen": "Shrike has Stealth and Infiltrate. Before deployment he may only join Jump Infantry "
                              "squads.",
    "Icon of Obstinacy": "If Lysander is your Warlord, friendly units with Chapter Tactics (Imperial Fists) within "
                         "12\" of him re-roll failed Morale and Pinning tests.",
    "Oath of Rynn": "If Kantor is your Warlord, friendly models in Crimson Fists detachments have Preferred Enemy "
                    "(Orks), and those within 12\" of him have +1 Attack while he lives (not Kantor himself; does "
                    "not stack with a Chapter Banner's bonus).",
    "Hold the Line": "If Pedro Kantor is in the army, friendly Crimson Fists Sternguard Veteran units are scoring "
                     "units.",
    "Crusade of Wrath": "Once per game, at the start of your Assault phase, Helbrecht may give all friendly models "
                        "with Chapter Tactics (Black Templars) Hatred and Fleet until the end of the phase.",
    "Legacy of Dorn": "The Sword of the High Marshals gives Helbrecht D3 bonus Attacks on the charge instead of one.",
    "Relics of Helsreach": "Friendly models with Chapter Tactics (Black Templars) within 6\" of any Cenobyte "
                           "Servitor have a 6+ invulnerable save.",
    "Unmatched Zeal": "Friendly models with Chapter Tactics (Black Templars) within 6\" of Chaplain Grimaldus have "
                      "Zealot.",
    "Slayer of Champions": "The Emperor's Champion must issue and accept challenges whenever possible (and must be "
                           "the model to do so if several could). In a challenge he picks a stance at the start of "
                           "each Fight sub-phase, lasting to the end of the challenge: Smite the Unclean, +2 Strength "
                           "with the Black Sword gaining Two-handed and Unwieldy; or Slay the Heretic, Black Sword To "
                           "Wound rolls of 6 have Instant Death.",
    "Graviton": "The To Wound roll is always the target's armour save (6+ if it has none or a worse one). Against "
                "vehicles roll a D6 per hit instead of armour penetration: on a 6 the vehicle is Immobilised and loses "
                "a Hull Point. No effect on buildings.",
    "Mindlock": "An unengaged unit with this rule and no Master of the Forge or Techmarine rolls a D6 at the start of "
                "its turn: on 1-3 it may not voluntarily move, shoot or charge until its next turn (compulsory moves "
                "still happen).",
    "Bolster Defences": "After deployment, before Scout redeployments and Infiltrators deploy, pick one terrain piece "
                        "in your deployment zone that you did not buy: its cover save improves by 1 (to a best of 3+) "
                        "for the game. A piece can only be bolstered once.",
    "Skies of Fury": "If the Stormraven moved more than 6\", passengers may still disembark: pick a point it passed "
                     "over and Deep Strike them there. If they scatter, every model takes a Dangerous Terrain test; "
                     "if any model cannot be placed the whole unit is destroyed. They cannot charge that turn.",
    "Drop Pod Assault": "Drop Pods and their passengers start in Reserve and arrive by Deep Strike. At the start of "
                        "your first turn, half your Drop Pods (rounding up) arrive automatically; roll for the rest "
                        "as normal. A unit arriving by Drop Pod cannot charge that turn.",
    "Immobile": "A Drop Pod cannot move after arriving and counts as Immobilised (cannot be repaired), without "
                "losing a Hull Point for it.",
    "Inertial Guidance System": "If a Drop Pod would scatter onto impassable terrain or another model, reduce the "
                                "scatter just enough to avoid it. Scattering off the board is a Deep Strike Mishap.",
    "Repair": "If Immobilised, in later turns the vehicle may try to repair itself instead of shooting: roll a D6 in "
              "the Shooting phase; on a 6 it is no longer Immobilised (no Hull Point is restored).",
    "Servo-tracking": "The Stalker may fire in dual-target mode, declared before choosing targets: it makes a full "
                      "shooting attack at each of two different targets using the dual-target profile, all at BS2.",
    "Savant Lock": "Each shot that misses a Flyer or Flying Monstrous Creature places a Savant Lock counter by the "
                   "target. At the start of each of your Shooting phases roll a D6 per counter: on 5+ remove it and "
                   "the target takes a hit with the weapon's profile (rear armour against vehicles). Counters are "
                   "discarded if the target leaves combat airspace or is locked in combat.",
    "Tremor": "A unit hit moves as if in difficult terrain in its next Movement phase (rolling one fewer dice, to a "
              "minimum of one, if already in difficult terrain). A vehicle must instead take a Dangerous Terrain test "
              "if it moves in its next Movement phase.",
    "Signum": "At the start of the Shooting phase, instead of shooting, the bearer may use the signum (declare before "
              "any To Hit rolls): one model in his squad is Ballistic Skill 5 for that phase.",
    "Ceramite Plating": "Melta weapons do not roll an extra D6 for armour penetration against this vehicle at half "
                        "range or less.",
}, "Tau": {}}

# Forge World: Space Marine Chapter Tactics for 6th Edition (Forge World PDF), for
# Imperial Armour Chapters. Chapters not listed use a codex Chapter's tactics: Howling
# Griffons, Fire Angels, Marines Errant, Novamarines and (before 991.M41) Angels Revenant
# use Ultramarines; Sons of Medusa use Iron Hands; Exorcists pick any; Lamenters use Codex:
# Blood Angels.
FORGE_WORLD_TACTICS = {
    "Purity Above All": "Red Scorpions. Any Tactical Squad Sergeant or Veteran Sergeant may be made an Apothecary, "
                        "taking a narthecium for free (no other change to wargear, options or profile; must be shown "
                        "on the model).",
    "Fortitude and Contempt": "Red Scorpions. Models re-roll failed Pinning tests, but cannot voluntarily Go to Ground "
                              "and cannot take camo cloaks.",
    "Reavers of the Outer Darkness": "Carcharodons. Models have Fear. Any model in a Tactical Squad may swap its "
                                     "boltgun for a close combat weapon (e.g. chainsword or combat blade) for free, or "
                                     "add a close combat weapon for +1 point per model (must be shown on the model). "
                                     "A Carcharodons force may only ally with other Imperial armies, always as "
                                     "Desperate Allies.",
    "Blood Hunger": "Carcharodons. A unit gains Rage (mark it) once it has destroyed an enemy infantry unit in an "
                    "assault or forced one to Fall Back. A marked unit's Consolidation move must be towards the "
                    "nearest enemy unit it can damage in an assault.",
    "Legendary Marksmen": "Raptors (who also have Strike from the Shadows). A unit that did not move in its Movement "
                          "phase may give its boltguns, bolt pistols and combi-weapons firing as boltguns Rending in "
                          "that Shooting phase; those weapons then count as Heavy 1 instead of Rapid Fire or Pistol "
                          "that turn.",
    "Shadow Killers": "Mantis Warriors. Infantry in the detachment have Move Through Cover and Hammer of Wrath, and "
                      "gain Furious Charge on a turn they charge from inside terrain that gives a cover save (not a "
                      "bought Fortification). Not for units that include any Bulky model.",
    "Children of Prophecy": "Mantis Warriors. If the primary detachment is Mantis Warriors you may re-roll a failed "
                            "attempt to Seize the Initiative. Mantis Warriors Librarians may generate powers from "
                            "Divination instead of their codex disciplines.",
    "Bitter Mettle": "Executioners. Models ignore every negative modifier to their Leadership.",
    "Headhunters": "Executioners. Characters with this rule inflict Instant Death on To Wound rolls of 6 in a "
                   "challenge (roll saves for those separately). In each assault, the character with this rule and "
                   "the highest WS (owner picks on a tie) must issue a challenge if possible.",
    "A Legacy of Hatred": "Angels Revenant (after 991.M41). Models have Preferred Enemy (Necrons) and Hatred "
                          "(Necrons). This is the detachment's only Chapter Tactic; if the enemy army has no models "
                          "from Codex: Necrons, it has To the Last Breath instead.",
    "To the Last Breath": "Angels Revenant (after 991.M41, against armies without Necrons). Once the detachment has "
                          "lost half (rounding down) of its units, all its remaining units have Fearless.",
    "Mnemonic Redaction Protocols": "Red Hunters. Models have Adamantium Will. Once per game, at the start of any "
                                    "player turn, a number of Red Hunters units (Dreadnoughts included) equal to the "
                                    "turn number each gain one of Counter-attack, Monster Hunter, Tank Hunters, "
                                    "Hatred, Skyfire or Interceptor (your choice per unit) until the start of your "
                                    "next turn.",
    "By this Seal": "Red Hunters. For the Allies Matrix, the detachment treats Codex: Grey Knights and Sisters of "
                    "Battle units as Battle Brothers, provided the allied detachment includes an Inquisitor.",
    "Orbital Wave Attack": "Star Phantoms. Units arriving by Deep Strike may re-roll Reserve Rolls of 1.",
    "Hail of Destruction": "Star Phantoms. Once per game, from the start of your Shooting phase until the start of "
                           "your next one, the detachment's Rapid Fire, Assault, Salvo and Heavy weapons are "
                           "twin-linked.",
    "Unrelenting Assault": "Minotaurs. Models take no Panic tests from shooting attacks and re-roll failed Pinning "
                           "tests.",
    "Trample and Crush": "Minotaurs. Models have Crusader and add 1 to their charge distance rolls while in the enemy "
                         "deployment zone.",
    "On Wings of Fire": "Fire Hawks. Flamers, hand flamers and heavy flamers get +1 Strength on the turn their unit "
                        "arrives by Deep Strike (including from a Drop Pod), and jump pack models get +1 Strength for "
                        "Hammer of Wrath. Space Marines with this Chapter Tactic may also take a hand flamer for +5 "
                        "points as a ranged weapon option.",
    "Speed and Fury": "Fire Hawks. The detachment's Assault Squads and Vanguard Veteran Squads are scoring units.",
    "Reckless Courage": "Astral Claws. Models have Stubborn and may never choose to automatically fail a Morale check.",
    "Rapid Attack and Encirclement": "Astral Claws. Bikes have Skilled Rider; Fast Skimmer vehicles in the same "
                                     "detachment have Scout.",
    "The Badab Wars": "Astral Claws before and during the Badab War use Chapter Tactics (Astral Claws): Reckless "
                      "Courage and Rapid Attack and Encirclement. After their fall (as the Red Corsairs) use Codex: "
                      "Chaos Space Marines instead.",
    "The Tyrant's Legion": "In a Tyrant's Legion army (Imperial Armour Volume Nine), every model with And They Shall "
                           "Know No Fear also uses Chapter Tactics (Astral Claws).",
}
CODEX_TEXT["Space Marines"].update({f"Chapter Tactics: {k}": v for k, v in FORGE_WORLD_TACTICS.items()})

# Forge World updates for 6th Edition: Siege Assault Vanguard army list (IA10) and the Badab
# War character update (IA9/IA10).
CODEX_TEXT["Space Marines"].update({
    "Siege Master": "While the Siege Master is in play, the army may re-roll all Reserve Rolls, successful or not. At "
                    "the start of the game he picks one friendly Infantry unit, or one non-Flyer vehicle or vehicle "
                    "squadron, from Codex: Space Marines or the Siege Assault Vanguard list; it gains Tank Hunters, "
                    "Monster Hunter, Interceptor or Furious Charge (your choice) for the game.",
    "Siege Objective": "The Siege Assault Vanguard player supplies a 40mm Siege Objective marker, which the opponent "
                       "places in their own deployment zone, by the normal objective placement rules, before "
                       "deployment. It is controlled like other objectives but is worth no Victory Points. Unless the "
                       "Siege Assault Vanguard player controls it at the end of the game or has wiped out the enemy, "
                       "the best they can achieve is a draw.",
    "Siege Dreadnought Talon": "Troops. Three Dreadnoughts, Ironclad (135 pts) or Siege (120 pts) in any mix. When "
                               "first deployed (at the start or from Reserve) they must be placed within 6\" of each "
                               "other; afterwards each acts individually and they are not a vehicle squadron.",
    "Brethren of Ancients": "The army may include no more Siege Dreadnought Talons than half its Tactical and Siege "
                            "Assault Squads. If more than half of all Dreadnoughts in the army (Talon or not) are "
                            "destroyed, every remaining friendly Dreadnought that is not Immobilised gains Rage.",
    "Siege Mantlets": "A Tactical Squad in a Siege Assault Vanguard may take siege mantlets (+50 points per squad; "
                      "shown on the models as large shields): it re-rolls failed armour saves against shooting, has "
                      "Bulky, may not Run or make Sweeping Advances, and may not take a Dedicated Transport. Independent "
                      "Characters joining it gain the benefits and the restrictions.",
    "The Tip of the Spear": "Siege Assault Squads may re-roll Sweeping Advance rolls. (Imperial Armour Volume 10 p. "
                            "190; the 6th Edition update gives the squad Crusader instead.)",
    "Assault Drill": "A Dreadnought close combat weapon that rolls an extra D6 for armour penetration against "
                     "Buildings, Fortifications and vehicles that have not moved this turn. When it scores a "
                     "penetrating hit on a Transport or Building, every model embarked takes one hit from the heavy "
                     "flamer after all close combat attacks are resolved (once per phase, not once per hit).",
    "Void Hardened Armour": "Anton Narvaez and any Command Squad with him count as wearing Void Hardened armour in "
                            "Zone Mortalis / Blood in the Void games.",
    "Unflinching Resolve": "Mir'san, and any friendly Codex: Space Marines unit with Chapter Tactics (Salamanders) he "
                           "joins, may choose to automatically pass or fail any Morale check or Pinning test.",
    "Weapon Mastery": "Tyberos may split his Attacks in an assault freely between Hunger and Slake (his profile "
                      "already includes the extra Attack for two weapons).",
})


def norm(name):
    name = (name or "").lower().replace("salemanders", "salamanders").replace("tempars", "templars")
    name = name.replace("&", " and ").replace("suprise", "surprise").replace("spectors", "spectres")
    name = name.replace("unyeilding", "unyielding").rstrip(":")
    return re.sub(r"[^a-z0-9]", "", name)


def base(name):
    """'Preferred Enemy (Orks)' -> 'Preferred Enemy'."""
    return re.sub(r"\s*\(.*\)\s*$", "", name or "")


def _texts(path):
    out = {}
    for e in ET.parse(path).getroot().iter():
        t = e.tag.rsplit("}", 1)[-1]
        if t == "rule":
            text = (e.findtext("{*}description") or "").strip()
        elif t == "profile" and (e.get("typeName") or "") in ("Abilities", "Special Rule", "Special Rules"):
            text = " ".join((c.text or "") for c in e.iter() if c.tag.endswith("characteristic")).strip()
        else:
            continue
        if text and norm(e.get("name")) not in out:
            out[norm(e.get("name"))] = text
    return out


_cache = {}


def sources(faction):
    if faction not in _cache:
        five = {}
        for p in (CACHE / "WH40K5E").glob("*.gst"):
            five.update(_texts(p))
        seven_core = _texts(CACHE / "wh40k-7th-edition" / "Warhammer40K.gst")
        seven_codex = _texts(CACHE / SEVENTH[faction]) if faction in SEVENTH else {}
        codex = {norm(k): v for k, v in CODEX_TEXT.get(faction, {}).items()}
        _cache[faction] = [("6th Ed codex", codex, ""), ("5th Ed core", five, ""),
                           ("7th Ed codex", seven_codex, TAG), ("7th Ed core", seven_core, TAG)]
    return _cache[faction]


def lookup(faction, name):
    for label, table, tag in sources(faction):
        for key in (norm(name), norm(base(name))):
            if key and key in table:
                return label, table[key] + tag
    return None, None


def fill_rules(cat, faction, q):
    """Fill every empty rule description in a converted catalogue. Returns a report."""
    used, missing = {}, set()
    for r in cat.iter(q("rule")):
        d = r.find(q("description"))
        if d is None:
            d = ET.SubElement(r, q("description"))
        if (d.text or "").strip():
            continue
        label, text = lookup(faction, r.get("name"))
        if text is None:
            missing.add(r.get("name"))
            continue
        d.text = text
        used[label] = used.get(label, 0) + 1
    return {"filled": used, "stillEmpty": sorted(missing)}

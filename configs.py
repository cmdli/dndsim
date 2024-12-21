from typing import Set, List

from sim import CharacterConfig
from classes.monk import Monk
from classes.barbarian import BerserkerBarbarian
from classes.fighter import (
    ChampionFighter,
    PrecisionTrippingFighter,
)
from classes.rogue import AssassinRogue, ArcaneTricksterRogue
from classes.wizard import Wizard
from classes.paladin import Paladin
from classes.ranger import GloomstalkerRanger, BeastMasterRanger
from classes.cleric import Cleric
from classes.au import AssaultUnit
from classes.bard import ValorBard

CONFIGS = {
    # Classes
    "barbarian": CharacterConfig("Barbarian", BerserkerBarbarian),
    "fighter": CharacterConfig("Fighter", ChampionFighter),
    "monk": CharacterConfig("Monk", Monk),
    "paladin": CharacterConfig("Paladin", Paladin),
    "ranger": CharacterConfig("Ranger", GloomstalkerRanger),
    "rogue": CharacterConfig("Rogue", AssassinRogue),
    "wizard": CharacterConfig("Wizard", Wizard),
    "cleric": CharacterConfig("Cleric", Cleric),
    "bard": CharacterConfig("Bard", ValorBard),
    # TODO: Warlock
    # TODO: Sorcerer
    # Subclasses
    "champion": CharacterConfig("Champion Fighter", ChampionFighter),
    "battlemaster": CharacterConfig("Battlemaster Fighter", PrecisionTrippingFighter),
    "gloomstalker": CharacterConfig("Gloomstalker Ranger", GloomstalkerRanger),
    "beastmaster": CharacterConfig("Beastmaster Ranger", BeastMasterRanger),
    "arcane_trickster": CharacterConfig("Arcane Trickster", ArcaneTricksterRogue),
    "au": CharacterConfig("Assault Unit 2 1", AssaultUnit),
}

SHORTCUTS = {
    "all": [
        "monk",
        "fighter",
        "barbarian",
        "paladin",
        "ranger",
        "rogue",
        "wizard",
        "cleric",
    ]
}


def break_out_shortcuts(names: Set[str]) -> Set[str]:
    for name in names:
        if name in SHORTCUTS:
            names = set(SHORTCUTS[name])
            break
    return names


def get_configs(names: Set[str]) -> List[CharacterConfig]:
    for name in names:
        if name in SHORTCUTS:
            names = set(SHORTCUTS[name])
            break
    characters = []
    for name in names:
        characters.append(CONFIGS[name.lower()])
    return characters

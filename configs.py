from typing import Set, List

from sim import CharacterConfig
from classes.monk import Monk
from classes.barbarian import Barbarian
from classes.fighter import (
    ChampionFighter,
)
from classes.rogue import AssassinRogue, ArcaneTricksterRogue
from classes.wizard import Wizard
from classes.paladin import Paladin
from classes.ranger import GloomstalkerRanger, BeastMasterRanger
from classes.cleric import Cleric
from classes.au import AssaultUnit
from classes.bard import ValorBard

CONFIGS = {
    "monk": CharacterConfig("Monk", Monk),
    "champion": CharacterConfig("Champion Fighter", ChampionFighter),
    "battlemaster": CharacterConfig("Battlemaster Fighter", ChampionFighter),
    "barbarian": CharacterConfig("Barbarian", Barbarian),
    "paladin": CharacterConfig("Paladin", Paladin),
    "gloomstalker": CharacterConfig("Gloomstalker Ranger", GloomstalkerRanger),
    "beastmaster": CharacterConfig("Beastmaster Ranger", BeastMasterRanger),
    "rogue": CharacterConfig("Assassin", AssassinRogue),
    "arcane_trickster": CharacterConfig("Arcane Trickster", ArcaneTricksterRogue),
    "wizard": CharacterConfig("Wizard", Wizard),
    "cleric": CharacterConfig("Cleric", Cleric),
    "au": CharacterConfig("Assault Unit 2 1", AssaultUnit),
    "bard": CharacterConfig("Bard", ValorBard),
}

SHORTCUTS = {
    "all": [
        "monk",
        "champion",
        "barbarian",
        "paladin",
        "beastmaster",
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

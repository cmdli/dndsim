from typing import List, Optional

from sim.events import AttackResultArgs
from util.util import apply_asi_feats

import sim.core_feats
import sim.feat


class WarlockLevel(sim.core_feats.ClassLevels):
    def __init__(self, level):
        super().__init__(name="Warlock", level=level)
        # TODO: Add pact magic spell slots here


class AgonizingBlast(sim.feat.Feat):
    def attack_result(self, args: AttackResultArgs):
        if (
            args.hits()
            and args.attack.spell is not None
            and args.attack.spell.name == "EldritchBlast"
        ):
            args.add_damage(source="Agonizing Blast", damage=self.character.mod("cha"))


def warlock_feats(
    level: int, asis: Optional[List["sim.feat.Feat"]] = None
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    # TODO
    if level >= 1:
        feats.append(WarlockLevel(level))
    apply_asi_feats(level, feats, asis)
    return feats

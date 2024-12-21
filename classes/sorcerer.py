from typing import List, Literal

import sim.character
import sim.spells
import sim.feat

# TODO: Complete the list
Metamagic = Literal["Quickened"]


class Metamagics(sim.feat.Feat):
    def __init__(self, metamagics: List[Metamagic]):
        self.metamagics = metamagics

    def apply(self, character):
        super().apply(character)
        character.metamagics.update(self.metamagics)


class InnateSorcery(sim.feat.Feat):
    pass


class FontOfMagic(sim.feat.Feat):
    def __init__(self, level: int):
        self.level = level

    def apply(self, character):
        super().apply(character)
        character.sorcery.max = self.level


class SorcerousRestoration(sim.feat.Feat):
    pass


class ArcaneApotheosis(sim.feat.Feat):
    pass


class ElementalAffinity(sim.feat.Feat):
    pass


class DefaultSorcererAction(sim.feat.Feat):
    def action(self, target):
        pass


def sorcerer_feats(level: int, metamagics: List[Metamagic]):
    feats: List["sim.feat.Feat"] = []
    feats.append(InnateSorcery())
    if level >= 2:
        feats.append(FontOfMagic(level))
        feats.append(Metamagics(metamagics))
    if level >= 5:
        feats.append(SorcerousRestoration())
    # Level 7 (Sorcery Incarnate) is currently not used
    # TODO: Add 2 more metamagics at 10 and 17
    if level >= 20:
        feats.append(ArcaneApotheosis())
    return feats


def draconic_sorcerer_feats(level: int):
    feats: List["sim.feat.Feat"] = []
    # Level 3 (Draconic Resilience) is irrelevant
    if level >= 6:
        feats.append(ElementalAffinity())
    # Level 14 (Dragon Wings) is irrelevant
    # TODO: Implement Dragon Companion
    return feats


class DraconicSorcerer(sim.character.Character):
    def __init__(self, level: int):
        feats: List["sim.feat.Feat"] = []
        super().init(
            level=level,
            stats=[10, 10, 10, 10, 10, 17],
            base_feats=feats,
            spellcaster=sim.spells.Spellcaster.FULL,
            spell_mod="cha",
        )

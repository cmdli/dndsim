import sim.character
import sim.spells
import sim.target


def sample_character():
    character = sim.character.Character()
    character.init(
        level=5,
        stats=[10, 10, 10, 10, 10, 10],
        base_feats=[],
        spellcaster=sim.spells.Spellcaster.FULL,
        spell_mod="int",
    )
    return character


class ExampleSpell(sim.spells.BasicSaveSpell):
    def dice(self):
        return [10]


class ExampleConcentrationSpell(sim.spells.ConcentrationSpell):
    pass


def test_spellcasting():
    character = sample_character()
    target = sim.target.Target(level=5)
    spell = ExampleSpell("Test", slot=1)
    character.spells.cast(spell=spell, target=target)
    assert target.dmg > 0


def test_concentration():
    character = sample_character()
    spell = ExampleConcentrationSpell("Test", slot=1)
    character.spells.cast(spell=spell)
    assert character.spells.concentrating_on("Test")

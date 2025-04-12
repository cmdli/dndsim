import sim.weapons
import sim.test_helpers
import sim.events
import sim.target


def sample_weapon():
    return sim.weapons.Weapon("TestWeapon", num_dice=1, die=6, damage_type="piercing")


def test_weapon():
    target = sim.target.Target(level=5)
    weapon = sample_weapon()
    character = sim.test_helpers.sample_character()
    assert weapon.mod(character) == "str"
    assert weapon.to_hit(character) == 4
    attack = sim.events.AttackArgs(character, target, weapon)
    dmg = weapon.damage(character, attack, crit=False)
    assert dmg >= 1 and dmg <= 6


def test_mod():
    shortsword = sim.weapons.Shortsword()
    character = sim.test_helpers.sample_character()
    character.stats["str"] = 10
    character.stats["dex"] = 14
    assert shortsword.mod(character) == "dex"
    glaive = sim.weapons.Glaive()
    assert glaive.mod(character) == "str"

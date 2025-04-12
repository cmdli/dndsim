import sim.test_helpers
import sim.weapons
import sim.target


def test_attacks():
    character = sim.test_helpers.sample_character()
    always_hit = sim.weapons.Weapon("AlwaysHit", num_dice=1, die=6, attack_bonus=10000)
    target = sim.target.Target(level=5)
    character.weapon_attack(target, always_hit)
    assert target.dmg > 0
    always_miss = sim.weapons.Weapon(
        "AlwaysMiss", num_dice=1, die=6, attack_bonus=-10000
    )
    target = sim.target.Target(level=5)
    character.weapon_attack(target, always_miss)
    assert target.dmg == 0

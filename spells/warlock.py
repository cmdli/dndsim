import sim.weapons
import sim.spells
import sim.character


class EldritchBlastBolt(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__("EldritchBlastBolt", num_dice=1, die=10, mod="none")


class EldritchBlast(sim.spells.Spell):
    def __init__(self, character_level: int, **kwargs):
        super().__init__("EldritchBlast", 0, **kwargs)
        self.character_level = character_level
        self.weapon = EldritchBlastBolt()

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        for _ in range(character.spells.cantrip_dice()):
            character.attack(target, self.weapon)

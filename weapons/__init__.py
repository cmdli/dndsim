import sim.weapons


class Glaive(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Glaive",
            num_dice=1,
            die=10,
            damage_type="slashing",
            mastery="Graze",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class GlaiveButt(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="GlaiveButt",
            num_dice=1,
            die=4,
            damage_type="bludgeoning",
            mastery="Graze",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class Greatsword(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Greatsword",
            num_dice=2,
            die=6,
            damage_type="slashing",
            mastery="Graze",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class Shortsword(sim.weapons.Weapon):
    def __init__(self, name="Shortsword", **kwargs):
        super().__init__(
            name=name,
            num_dice=1,
            die=6,
            damage_type="piercing",
            mastery="Vex",
            tags=["finesse", "light"],
            **kwargs,
        )


class Rapier(sim.weapons.Weapon):
    def __init__(self, name="Rapier", **kwargs):
        super().__init__(
            name=name,
            num_dice=1,
            die=8,
            damage_type="piercing",
            mastery="Vex",
            tags=["finesse"],
            **kwargs,
        )


class Scimitar(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Scimitar",
            num_dice=1,
            die=6,
            damage_type="slashing",
            mastery="Nick",
            tags=["finesse", "light"],
            **kwargs,
        )


class Maul(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Maul",
            num_dice=2,
            die=6,
            damage_type="bludgeoning",
            mastery="Topple",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class Quarterstaff(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Quarterstaff",
            num_dice=1,
            die=8,
            damage_type="bludgeoning",
            mastery="Topple",
            tags=["twohanded"],
            **kwargs,
        )


class HandCrossbow(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="HandCrossbow",
            num_dice=1,
            die=6,
            damage_type="piercing",
            mastery="Vex",
            tags=["ranged", "light"],
            **kwargs,
        )


class Dagger(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Dagger",
            num_dice=1,
            die=4,
            damage_type="piercing",
            mastery="Nick",
            tags=["finesse", "light"],
            **kwargs,
        )


class Warhammer(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Warhammer",
            num_dice=1,
            die=8,
            damage_type="bludgeoning",
            **kwargs,
        )

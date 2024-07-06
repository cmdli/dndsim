class Weapon:
    def __init__(
        self,
        name=None,
        num_dice=0,
        die=6,
        mod=None,
        bonus=0,
        graze=False,
        vex=False,
        min_crit=20,
        **kwargs
    ) -> None:
        self.name = name
        self.num_dice = num_dice
        self.die = die
        self.mod = mod
        self.bonus = bonus
        self.graze = graze
        self.vex = vex
        self.min_crit = min_crit


class Glaive(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Glaive", num_dice=1, die=10, mod="str", graze=True, **kwargs
        )


class Greatsword(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Greatsword", num_dice=2, die=6, mod="str", graze=True, **kwargs
        )


class Shortsword(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Shortsword", num_dice=1, die=6, mod="dex", vex=True, **kwargs
        )


class Scimitar(Weapon):
    def __init__(self, **kwargs):
        super().__init__(name="Scimitar", num_dice=1, die=6, mod="dex", **kwargs)


class GlaiveButt(Weapon):
    def __init__(self, **kwargs):
        super().__init__(name="GlaiveButt", num_dice=1, die=4, graze=True, **kwargs)

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
        ranged=False,
        topple=False,
        base=None,
        is_other_creature=False,
    ) -> None:
        self.name = name
        self.num_dice = num_dice
        self.die = die
        self.mod = mod
        self.bonus = bonus
        self.graze = graze
        self.vex = vex
        self.min_crit = min_crit
        self.ranged = ranged
        self.topple = topple
        self.base = base
        self.is_other_creature = is_other_creature

class Glaive(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Glaive", num_dice=1, die=10, mod="str", graze=True, **kwargs
        )


class GlaiveButt(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="GlaiveButt", num_dice=1, die=4, mod="str", graze=True, **kwargs
        )


class Greatsword(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Greatsword", num_dice=2, die=6, mod="str", graze=True, **kwargs
        )


class Shortsword(Weapon):
    def __init__(self, mod="dex", name="Shortsword", **kwargs):
        super().__init__(
            name=name, num_dice=1, die=6, mod=mod, vex=True, **kwargs
        )

class Rapier(Weapon):
    def __init__(self, mod="dex", name="Rapier", **kwargs):
        super().__init__(
            name=name, num_dice=1, die=8, mod=mod, vex=True, **kwargs
        )

class Scimitar(Weapon):
    def __init__(self, mod="dex", **kwargs):
        super().__init__(name="Scimitar", num_dice=1, die=6, mod=mod, **kwargs)


class Maul(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Maul", num_dice=2, die=6, mod="str", topple=True, **kwargs
        )


class HandCrossbow(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="HandCrossbow",
            num_dice=1,
            die=6,
            mod="dex",
            vex=True,
            ranged=True,
            **kwargs
        )

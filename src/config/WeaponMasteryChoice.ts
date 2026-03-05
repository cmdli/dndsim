import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { Character } from "../sim/Character"
import { WEAPON_MASTERIES, WeaponMastery } from "../sim/types"
import { Choice, Option, StaticOption } from "./config"

export class WeaponMasteryChoice implements Choice {
    options(character: Character): Option[] {
        return WEAPON_MASTERIES.map((mastery) => new StaticOption(mastery))
    }

    apply(character: Character, optionId: WeaponMastery) {
        character.addFeature(new WeaponMasteries([optionId]))
    }
}

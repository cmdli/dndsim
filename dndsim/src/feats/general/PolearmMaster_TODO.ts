import { AfterActionEvent } from "../../sim/events/AfterActionEvent"
import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Quarterstaff, Spear } from "../../weapons"
import { HeavyWeapon, ReachWeapon, Weapon } from "../../sim/Weapon"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"

const PolearmMasterTag = "polearm_master"

function isPolearm(weapon: Weapon): Boolean {
    return weapon instanceof Quarterstaff
        || weapon instanceof Spear
        || (weapon.hasTag(HeavyWeapon) && weapon.hasTag(ReachWeapon))
}

export class PolearmMaster extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // We ignore the reaction attack from PAM
        // TODO: Figure out how to handle the bonus action attack
        character.increaseStat(this.stat, 1)
        character.events.on("after_action", (event) => this.afterAction(event))
        character.events.on("attack_result", (event) => this.attackResult(event))
    }

    attackResult(event: AttackResultEvent) {
        if (!event.attack.attack.hasTag(PolearmMasterTag)) {
            return
        }

        // TODO: Make sure that this can't be replaced by effects like Shillelagh
        event.damageRolls
            .filter((damageRoll) => damageRoll.hasTag("base_weapon_damage"))
            .forEach((damageRoll) => damageRoll.replaceDice([4]))
    }

    afterAction(event: AfterActionEvent) {
        if (!this.character.bonus.has()) {
            return
        }

        // TODO: Verify that we took the attack action with this weapon, and
        // ensure that we're picking the correct one if there are multiple

        const polearm = this.character.weapons.filter(isPolearm)[0]

        if (!polearm) {
            return
        }

        this.character.bonus.use()
        this.character.weaponAttack({
            target: event.target,
            weapon: polearm,
            damageType: "bludgeoning",
            tags: [PolearmMasterTag],
        })
    }
}

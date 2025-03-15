import { IrresistibleOffense } from "./epic/IrresistibleOffense"
import { GreatWeaponFighting } from "./fightingStyle/GreatWeaponFighting"
import { GreatWeaponMaster } from "./GreatWeaponMaster"
import { SavageAttacker } from "./origin/SavageAttacker"
import { TavernBrawler } from "./origin/TavernBrawler"
import { AbilityScoreImprovement } from "./shared/AbilityScoreImprovement"

const epicBoons = {
    IrresistibleOffense,
    GreatWeaponFighting,
}

const fightingStyles = {
    GreatWeaponFighting,
}

const originFeats = {
    SavageAttacker,
    TavernBrawler,
}

export {
    GreatWeaponMaster,
    AbilityScoreImprovement,
    epicBoons,
    fightingStyles,
    originFeats,
}

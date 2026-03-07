import { StandardOption } from "../config/config"
import { WeaponMasteryChoice } from "../config/WeaponMasteryChoice"
import { FightingStyleChoice } from "../config/FightingStyleChoice"
import { FeatChoice } from "../config/featChoice/FeatChoice"
import { AddClassLevel } from "../sim/coreFeats/ClassLevel"
import { Fighter } from "./Fighter"

export class FighterLevel1 extends StandardOption {
    constructor() {
        super({
            id: "FighterLevel1",
            choices: {
                mastery1: new WeaponMasteryChoice(),
                mastery2: new WeaponMasteryChoice(),
                fightingStyle: new FightingStyleChoice(),
            },
            feats: [new AddClassLevel("Fighter", 1)],
        })
    }
}

export class FighterLevel2 extends StandardOption {
    constructor() {
        super({
            id: "FighterLevel2",
            feats: [Fighter.level2()],
        })
    }
}

export class FighterLevel3 extends StandardOption {
    constructor() {
        super({
            id: "FighterLevel3",
            // TODO: Subclass choices
        })
    }
}

export class FighterLevel4 extends StandardOption {
    constructor() {
        super({
            id: "FighterLevel4",
            choices: {
                feat: new FeatChoice(),
            },
        })
    }
}

export class FighterLevel5 extends StandardOption {
    constructor() {
        super({
            id: "FighterLevel5",
            feats: [Fighter.level5()],
        })
    }
}

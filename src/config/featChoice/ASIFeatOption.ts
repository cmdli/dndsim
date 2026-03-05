import { Stat } from "../../sim/types"
import { AbilityScoreImprovement } from "../../feats/general/AbilityScoreImprovement"
import { Character } from "../../sim/Character"
import { Choice, Option, StaticOption } from "../config"

class StatChoice implements Choice {
    options(character: Character): Option[] {
        return [
            new StaticOption("str"),
            new StaticOption("dex"),
            new StaticOption("con"),
            new StaticOption("int"),
            new StaticOption("wis"),
            new StaticOption("cha"),
            new StaticOption("none"),
        ]
    }

    apply(character: Character, optionId: string): void {}
}

export class ASIOption implements Option {
    id: string = "ASIOption"

    choices(): Record<string, Choice> {
        return {
            stat1: new StatChoice(),
            stat2: new StatChoice(),
        }
    }

    apply(character: Character, choices: Record<string, string>): void {
        const stats: Stat[] = []
        if (choices.stat1 && choices.stat1 !== "none") {
            stats.push(choices.stat1 as Stat)
        }
        if (choices.stat2 && choices.stat2 !== "none") {
            stats.push(choices.stat2 as Stat)
        }
        if (stats.length > 0) {
            character.addFeature(
                new AbilityScoreImprovement(stats[0], stats[1])
            )
        }
    }
}

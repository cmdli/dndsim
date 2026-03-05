import { Choice, Option } from "../config"
import { Character } from "../../sim/Character"
import { ASIOption } from "./ASIFeatOption"

const FEAT_CHOICES = {
    ASI: () => new ASIOption(),
} as const

export class FeatChoice implements Choice {
    options(character: Character): Option[] {
        return Object.values(FEAT_CHOICES).map((feat) => feat())
    }

    apply(character: Character, optionId: string): void {
        const feat = FEAT_CHOICES[optionId as keyof typeof FEAT_CHOICES]
        if (feat) {
            feat().apply(character, {})
        }
    }
}

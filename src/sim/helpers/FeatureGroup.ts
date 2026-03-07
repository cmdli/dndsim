import { Character } from "../Character"
import { Feature } from "../Feature"

export class FeatureGroup extends Feature {
    constructor(private features: Feature[]) {
        super()
    }

    apply(character: Character): void {
        for (const feature of this.features) {
            feature.apply(character)
        }
    }
}

import { Character } from "../Character"
import { Feat } from "../Feat"
import { Class } from "../types"

export class ClassLevel extends Feat {
    class_: Class
    level_: number
    constructor(class_: Class, level?: number) {
        super()
        this.class_ = class_
        this.level_ = level ?? 1
    }

    apply(character: Character): void {
        character.addClassLevel(this.class_, this.level_)
    }
}

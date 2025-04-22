import { Character } from "../Character"
import { Feature } from "../Feature"
import { Class } from "../types"

export class ClassLevel extends Feature {
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

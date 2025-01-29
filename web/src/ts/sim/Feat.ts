import { Character } from "./Character"
import { CharacterEvent, CharacterEventMapping } from "./CharacterEvent"

export abstract class Feat<Events extends CharacterEvent> {
    name: string
    events_: Array<Events>
    character: Character | undefined
    constructor(name: string, events: Array<Events>) {
        this.name = name
        this.events_ = events
    }

    apply(character: Character): void {
        this.character = character
        character.addFeat(this)
    }

    events(): Array<Events> {
        return this.events_
    }

    abstract onEvent(event: Events, data: CharacterEventMapping[Events]): void
}

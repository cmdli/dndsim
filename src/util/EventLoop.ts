type Listener<Data> = (data: Data) => void

type ListenerMap<
    Event extends string,
    EventMapping extends Record<Event, any>
> = {
        [eventName in Event]?: Set<Listener<EventMapping[eventName]>>
    }

export class EventLoop<
    Event extends string,
    EventMapping extends Record<Event, any>
> {
    private listeners: ListenerMap<Event, EventMapping> = {}

    on<SpecificEvent extends Event>(
        event: SpecificEvent,
        listener: Listener<EventMapping[SpecificEvent]>
    ) {
        if (this.listeners[event]) {
            this.listeners[event].add(listener)
        } else {
            this.listeners[event] = new Set([listener])
        }
    }

    removeListener<SpecificEvent extends Event>(
        event: SpecificEvent,
        listener: Listener<EventMapping[SpecificEvent]>
    ) {
        if (this.listeners[event]) {
            this.listeners[event].delete(listener)
        }
    }

    emit<SpecificEvent extends Event>(
        event: SpecificEvent,
        data: EventMapping[SpecificEvent]
    ) {
        if (this.listeners[event]) {
            for (const listener of this.listeners[event]) {
                listener(data)
            }
        }
    }
}

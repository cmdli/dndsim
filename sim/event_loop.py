from typing import Dict, Any, List


class Listener:
    pass


class EventLoop:
    def __init__(self) -> None:
        self.listeners: Dict[str, List[Listener]] = dict()

    def add(self, listener: Listener, events: List[str]) -> None:
        if isinstance(events, str):
            events = [events]
        for event in events:
            if event not in self.listeners:
                self.listeners[event] = []
            self.listeners[event].append(listener)

    def remove(self, listener: Listener) -> None:
        for event in self.listeners:
            if listener in self.listeners[event]:
                self.listeners[event].remove(listener)

    def emit(self, event: str, *args, **kwargs) -> None:
        listeners = self.listeners[event] if event in self.listeners else []
        for listener in listeners:
            func = getattr(listener, event)
            func(*args, **kwargs)

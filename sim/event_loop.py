from typing import Dict, Any, List


class Listener:
    def events(self) -> List[str]:
        pass


class EventLoop:
    def __init__(self) -> None:
        self.listeners: Dict[str, List[Listener]] = dict()

    def add(self, listener: Listener) -> None:
        for event in listener.events():
            if event not in self.listeners:
                self.listeners[event] = []
            self.listeners[event].append(listener)

    def emit(self, event: str, *args, **kwargs) -> None:
        listeners = self.listeners[event] if event in self.listeners else []
        for listener in listeners:
            func = getattr(listener, event)
            func(*args, **kwargs)

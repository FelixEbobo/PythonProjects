from __future__ import annotations
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class SimpleCommand(Command):
    def __init__(self, payload: str) -> None:
        self._payload = payload

    def execute(self):
        print(f"simple command {self._payload}")

class ComplexCommand(Command):
    def __init__(self, receiver: Receiver, 
                 a: str, b: str) -> None:
        self._receiver = receiver
        self._a = a
        self._b = b

    def execute(self) -> None:
        print("ComplexCommand:")
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)

class Receiver:
    def do_something(self, a: str) -> None:
        print(f"Receiver: Working on ({a}.)")
    
    def do_something_else(self, b: str) -> None:
        print(f"Receiver: Working on ({b}.)")

class Invoker:
    _on_start = None
    _on_finish = None
    
    @property
    def on_start(self):
        return self._on_start

    @property
    def on_finish(self):
        return self._on_finish

    @on_start.setter
    def on_start(self, command: Command):
        self._on_start = command

    @on_finish.setter
    def on_finish(self, command: Command):
        self._on_finish = command

    def do_something_important(self) -> None:
        print("Before work command:")
        if isinstance(self.on_start, Command):
            self.on_start.execute()

        print("After end command:")
        if isinstance(self.on_finish, Command):
            self.on_finish.execute()

if __name__ == "__main__":
    invoker = Invoker()
    invoker.on_start = SimpleCommand("Say hi!")
    receiver = Receiver()
    invoker.on_finish = ComplexCommand(
        receiver, "Send email", "Save report")
    invoker.do_something_important()
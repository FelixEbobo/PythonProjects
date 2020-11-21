from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits

class Originator():
    _state = None
    def __init__(self, state: str) -> None:
        self._state = state
        print(f"Originator: My original state is {self._state}")

    def do_something(self) -> None:
        print("Originator: I'm doing something")
        self._state = self._generate_random_string(12)
        print(f"Originator: and my state changed to {self._state}")

    def _generate_random_string(self, lenght: int = 10) -> None:
        return "".join(sample(ascii_letters, lenght))

    def save(self) -> Memento:
        return ConcreteMemento(self._state)

    def restore(self, memento: Memento) -> None:
        self._state = memento.state
        print(f"Originator: My state has changed to: {self._state}")
    
class Memento(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def date(self) -> str:
        pass

class ConcreteMemento(Memento):
    def __init__(self, state: str) -> None:
        self._state = state
        self._date = str(datetime.now())[:19]

    @property
    def state(self) -> str:
        return self._state
    
    @property
    def name(self) -> str:
        return f"{self.date} / ({self.state[0:9]}...)"

    @property
    def date(self) -> str:
        return self._date
    
class Caretaker():
    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator

    def backup(self) -> None:
        print("\n Caretaker: Saving Originator's state...")
        self._mementos.append(self._originator.save())

    def undo(self) -> None:
        if not len(self._mementos):
            return
        memento = self._mementos.pop()
        print(f"Caretaker: restoring state to: {memento.name}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento.name)

if __name__ == "__main__":
    originator = Originator("Test testing test")
    caretaker = Caretaker(originator)

    for _ in range(3):
        caretaker.backup()
        originator.do_something()
    
    print()
    caretaker.show_history()

    print("\nClient: Rollback time!")
    caretaker.undo()

    print("\nClient: Rollback time!")
    caretaker.undo()

    print()
    caretaker.show_history()
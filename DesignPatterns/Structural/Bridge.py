from __future__ import annotations
from abc import ABC, abstractmethod

class Abstraction:
    def __init__(self, implementation: Implementation):
        self.implementation = implementation
    
    def operation(self) -> str:
        return ("Abstraction: Base operation with: \n"
                f"{self.implementation.operation_implementation()}")
    
class ExtendedAbstraction(Abstraction):
    def operation(self):
        return ("ExtendedAbstraction: Extended operation with: \n"
                f"{self.implementation.operation_implementation()}")

class Implementation(ABC):
    @abstractmethod
    def operation_implementation(self) -> str:
        pass

class ConcreteImplementationA(Implementation):
    def operation_implementation(self):
        return "ConcreteImplementationA: Here's the result of A"

class ConcreteImplementationB(Implementation):
    def operation_implementation(self):
        return "ConcreteImplementationB: Here's the result of A"

def client_code(abstraction: Abstraction) -> None:
    print(abstraction.operation(), end="")

if __name__ == "__main__":
    implementation = ConcreteImplementationA()
    abstraction = Abstraction(implementation)
    client_code(abstraction)

    print("\n")

    implementation = ConcreteImplementationB()
    abstraction = ExtendedAbstraction(implementation)
    client_code(abstraction)
    print()
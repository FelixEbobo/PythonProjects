import time

class Component():
    def operation(self) -> str:
        pass

class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"

class Decorator(Component):
    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> str:
        return self._component

    def operation(self) -> str:
        return self._component.operation()

class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA({self.component.operation()})"

class ConcreteDecoratorB(Decorator):
    def operation(self):
        return f"ConcreteDecoratorB({self.component.operation()})"

def client_code(component: Component) -> None:
    print(f"Result: {component.operation()}")

def time_calc(function):
    def wrapper(*args):
        start_time = time.time()
        function(*args)
        end_time = time.time()
        print(f"Time during executing: {end_time - start_time}")
    return wrapper

@time_calc
def fibonacci(number: int, fib_dict):
    temp = fib_dict
    get_number = 0
    if temp.get(number, -1) != -1:
        get_number = temp[number]
    else:
        for i in range(number + 1):
            if temp.get(i, -1) == -1:
                temp[i] = temp[i - 1] + temp[i - 2]
            else:
                continue
        get_number = temp[number]

    print(f"Fibonacci number for {number} is {get_number}")
    return temp

if __name__ == "__main__":
    simple = ConcreteComponent()
    print("Simple component")
    client_code(simple)

    print()

    decorator1 = ConcreteDecoratorA(simple)
    decorator2 = ConcreteDecoratorB(decorator1)
    print("Decorated component")
    client_code(decorator1)
    print("Decorated decorator")
    client_code(decorator2)

    print()

    fib_dict = {0: 0, 1: 1}
    fibonacci(100, fib_dict)
    fibonacci(65, fib_dict)


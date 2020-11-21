class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):

    def __init__(self, some: int):
        self.some = some

    def some_business_logic(self):
        pass

if __name__ == "__main__":
    s1 = Singleton(3)
    s2 = Singleton(4)

    if id(s1) == id(s2):
        print("There are the same objects")
    else:
        print("There are different objects, no Singleton")
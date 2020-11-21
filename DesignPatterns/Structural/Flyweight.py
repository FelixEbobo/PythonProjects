class Lamp:
    def __init__(self, color: str) -> None:
        self.color = color

class LampFactory:
    lamps = {}

    @staticmethod
    def get_lamp(color: str):
        return LampFactory.lamps.setdefault(color, Lamp(color))

class TreeBranch:
    def __init__(self, branch_number: int):
        self.branch_number = branch_number
    
    def hang(self, lamp: Lamp):
        print(f"Hang {lamp.color} [{id(lamp)}] lamp on branch "
        f"{self.branch_number} [{id(self)}]")

class ChristmassTree:
    def __init__(self): 
        self.lamps_hung = 0
        self.branches = {}

    def get_branch(self, number: int):
        return self.branches.setdefault(number, TreeBranch(number))

    def hang_lamp(self, color: str, branch_number: int):
        self.get_branch(branch_number).hang(LampFactory.get_lamp(color))
        self.lamps_hung += 1

def client_code(tree: ChristmassTree):
    for branch_number in range(1, 7):
        for color in ('red', 'blue', 'yellow'):
            tree.hang_lamp(color, branch_number)

christmass_tree = ChristmassTree()
client_code(christmass_tree)
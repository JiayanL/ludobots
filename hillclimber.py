from solution import SOLUTION
import constants as c
import copy


class HILL_ClIMBER():
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate()

        # Evolve
        for currentgeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate()
        self.Select()
        exit()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()
        print(
            f"parent weights: {self.parent.weights} \n child weights: {self.child.weights}")
        exit()

    def Select(self):
        pass

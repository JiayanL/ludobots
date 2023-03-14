from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle


class PARALLEL_HILL_ClIMBER():
    def __init__(self, seed):
        self.seed = seed
        # remove files we no longer need
        os.system("rm body*.urdf")
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

        self.fitnessCurves = np.zeros(c.numberOfGenerations)

    def Log_Best(self, currentGeneration):
        best_fitness = float('-inf')
        for key in self.parents.keys():
            parent = self.parents[key]
            if (parent.fitness > best_fitness):
                best_fitness = parent.fitness

        if currentGeneration in [0, c.numberOfGenerations / 2 - 1, c.numberOfGenerations - 1]:
            with open(f"seed{self.seed}_gen{currentGeneration}.pickle", "wb") as f:
                pickle.dump(parent, f)

        self.fitnessCurves[currentGeneration] = best_fitness

    def Plot(self):
        plt.plot(self.fitnessCurves, label="Fitness Curve", linewidth=4)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.show()

    def Evolve(self):
        self.Evaluate(self.parents)

        # # Evolve
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.Log_Best(currentGeneration)

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            parent = solutions[i]
            parent.Start_Simulation("DIRECT")

        for i in range(c.populationSize):
            parent = solutions[i]
            parent.Wait_For_Simulation_To_End()

    def Show_Best(self):
        best_fitness = float('-inf')

        for key in self.parents.keys():
            parent = self.parents[key]
            if (parent.fitness > best_fitness):
                best_parent = parent
                best_fitness = parent.fitness

        # changed this to best parent
        best_parent.Start_Simulation("GUI")
        # self.parent.Evaluate("GUI")

    def Spawn(self):
        self.children = {}

        for key in self.parents.keys():
            child = copy.deepcopy(self.parents[key])
            self.children[key] = child
            child.Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()

    def Select(self):
        for key in self.parents.keys():
            parent = self.parents[key]
            child = self.children[key]
            if (parent.fitness < child.fitness):
                self.parents[key] = child

    def Print(self):
        for key in self.parents.keys():
            parent = self.parents[key]
            child = self.children[key]
            print(
                f"\nPARENT FITNESS: {parent.fitness}\n CHILD FITNESS: {child.fitness}\n")

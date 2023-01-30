import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os


class SOLUTION():
    def __init__(self):
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

    def Evaluate(self, directOrGUI):
        # Create robot's world, body, neural network
        # send six weights in this solution when it sends synaptic weights
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system("python3 simulate.py " + directOrGUI)

        # read fitness
        fitnessFile = open("fitness.txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()

    def Mutate(self):
        row = random.randint(0, 2)
        column = random.randint(0, 1)
        self.weights[row][column] = random.random()*2-1

    def Create_World(self):
        # use pyrosim to Create a link
        # tells pyrosim the name of the file where information about the world should be stored
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box",
                          pos=[3, 4, .5], size=[1, 1, 1])
        # closes the file
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # create Torso (root link)
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])

        # Front Leg
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso",
                           child="FrontLeg", type="revolute", position=[.5, 0, 1])

        # create FrontLeg
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[1, 1, 1])

        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso",
                           child="BackLeg", type="revolute", position=[-.5, 0, 1])
        # create BackLeg
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[1, 1, 1])

        # create joints
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + 3, weight=self.weights[currentRow][currentColumn])
        # End pyrosim
        pyrosim.End()

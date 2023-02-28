import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import math


class ROBOT():
    def __init__(self, solutionID):
        self.solutionID = solutionID

        body_file = "body" + str(self.solutionID) + ".urdf"
        self.robotID = p.loadURDF(body_file)
        os.system("rm " + body_file)

        # creates neural network and adds neurons and synapses from brain.nndf
        brain_file = "brain" + str(self.solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brain_file)

        os.system("rm " + brain_file)
        # preparation for simulating sensors
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                # extract name of joint
                jointName = self.nn.Get_Motor_Neurons_Joint(
                    neuronName).encode('ASCII')
                desiredAngle = self.nn.Get_Value_Of(
                    neuronName) * c.motorJointRange
                try:
                    self.motors[jointName].Set_Value(
                        self.robotID, desiredAngle)
                except:
                    print(f"\n JOINT {jointName}\n")
                    print(f"\n {self.motors}\n")
                    exit()

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        positionAndOrientation = p.getBasePositionAndOrientation(
            self.robotID)

        torsoPosition = positionAndOrientation[0]
        torsoX = torsoPosition[0]
        # torsoY = torsoPosition[1]
        # torsoZ = torsoPosition[2]

        fitness = torsoX

        # write file
        # first temporarily
        tmp_file = "tmp" + str(self.solutionID) + ".txt"
        f = open(tmp_file, "w")
        f.write(str(fitness))
        f.close()

        # then rename
        os.system(f"mv {tmp_file} fitness{self.solutionID}.txt")

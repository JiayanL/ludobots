import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c


class ROBOT():
    def __init__(self, solutionID):
        self.robotID = p.loadURDF("body.urdf")
        self.solutionID = solutionID
        # creates neural network and adds neurons and synapses from brain.nndf
        brain_file = "brain" + str(solutionID) + ".nndf"
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
                self.motors[jointName].Set_Value(self.robotID, desiredAngle)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(
            self.robotID)
        basePosition = basePositionAndOrientation[0]
        yPosition = basePosition[1]
        zPosition = basePosition[2]

        hipPosition = basePositionAndOrientation[1]
        hipHeight = hipPosition[2]

        fitness = yPosition + zPosition + hipHeight

        # stateOfLinkZero = p.getLinkState(self.robotID, 0)[0]
        # xCoordinateofLinkZero = stateOfLinkZero[0]

        # write file
        # first temporarily
        tmp_file = "tmp" + str(self.solutionID) + ".txt"
        f = open(tmp_file, "w")
        f.write(str(fitness))
        f.close()

        # then rename
        os.system(f"mv {tmp_file} fitness{self.solutionID}.txt")

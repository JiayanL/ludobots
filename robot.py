import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT():
    def __init__(self):
        self.robotID = p.loadURDF("body.urdf")
        # creates neural network and adds neurons and synapses from brain.nndf
        self.nn = NEURAL_NETWORK("brain.nndf")
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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotID, desiredAngle)

    def Think(self):
        self.nn.Update()
        self.nn.Print()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotID, 0)[0]
        xCoordinateofLinkZero = stateOfLinkZero[0]

        # write file
        f = open("fitness.txt", "w")
        f.write(str(xCoordinateofLinkZero))
        f.close()

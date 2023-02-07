import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c


class SOLUTION():
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        self.sensor_to_hidden_weights = np.random.rand(
            c.numSensorNeurons, c.numHiddenNeurons)
        self.sensor_to_hidden_weights = self.sensor_to_hidden_weights * 2 - 1

        self.hidden_to_motor_weights = np.random.rand(
            c.numHiddenNeurons, c.numMotorNeurons)
        self.hidden_to_motor_weights = self.hidden_to_motor_weights * 2 - 1

        self.weights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system("python3 simulate.py " + directOrGUI +
                  " " + str(self.myID) + " 2&>1 &")

        # make sure the simulation has finished and the file is ready to be read in
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        # read fitness
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        simulate = "python3 simulate.py " + \
            directOrGUI + " " + str(self.myID) + " &"
        os.system(simulate)

    def Wait_For_Simulation_To_End(self):
        # make sure the simulation has finished and the file is ready to be read in
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        # read fitness
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system(f"rm {fitnessFileName}")

    def Mutate(self):
        # update first layer
        row = random.randint(0, c.numSensorNeurons-1)
        column = random.randint(0, c.numHiddenNeurons-1)
        self.sensor_to_hidden_weights[row][column] = random.random()*2-1

        # update second layer
        row = random.randint(0, c.numHiddenNeurons-1)
        column = random.randint(0, c.numMotorNeurons-1)
        self.hidden_to_motor_weights[row][column] = random.random()*2-1

        # update test weights
        row = random.randint(0, c.numSensorNeurons-1)
        column = random.randint(0, c.numMotorNeurons - 1)
        self.weights[row][column] = random.random()*2-1

    def Create_World(self):
        # use pyrosim to Create a link
        # tells pyrosim the name of the file where information about the world should be stored
        pyrosim.Start_SDF("world.sdf")

        # Make stairs or runway
        pyrosim.Send_Cube(name="Stairs", pos=[0, .2, .1], size=[.2, .2, .2])
        pyrosim.Send_Cube(name="Stairs2", pos=[0, .3, .2], size=[.2, .2, .4])
        pyrosim.Send_Cube(name="Stairs3", pos=[0, .4, .3], size=[.2, .2, .6])
        # closes the file
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # create Torso (root link)
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 2], size=[.5, .5, 1])

        # Create Left Leg
        pyrosim.Send_Joint(name="Torso_Hip", parent="Torso", child="Hip",
                           type="revolute", position=[0, 0, 1.5], jointAxis="0 0 1")
        pyrosim.Send_Cube(name="Hip", pos=[0, 0, 0], size=[.5, 1, .2])

        # Create left leg and foot
        pyrosim.Send_Joint(name="Hip_LeftFemur", parent="Hip", child="LeftFemur",
                           type="revolute", position=[0, -.5, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftFemur", pos=[
                          0, 0, -.4], size=[.2, .2, .8])

        pyrosim.Send_Joint(name="LeftFemur_LeftTibia", parent="LeftFemur",
                           child="LeftTibia", type="revolute", position=[0, 0, -.8], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftTibia", pos=[0, 0, -.3], size=[.2, .2, .6])

        pyrosim.Send_Joint(name="LeftTibia_LeftFoot", parent="LeftTibia",
                           child="LeftFoot", type="revolute", position=[0, 0, -.6], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftFoot", pos=[
                          0, 0, 0], size=[.4, .4, .2])

        # Create Right Leg
        pyrosim.Send_Joint(name="Hip_RightFemur", parent="Hip", child="RightFemur",
                           type="revolute", position=[0, .5, 0], jointAxis="0 1 0 ")
        pyrosim.Send_Cube(name="RightFemur", pos=[
                          0, 0, -.4], size=[.2, .2, .8])

        pyrosim.Send_Joint(name="RightFemur_RightTibia", parent="RightFemur",
                           child="RightTibia", type="revolute", position=[0, 0, -.8], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightTibia", pos=[
                          0, 0, -.3], size=[.2, .2, .6])

        pyrosim.Send_Joint(name="RightTibia_RightFoot", parent="RightTibia",
                           child="RightFoot", type="revolute", position=[0, 0, -.6], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightFoot", pos=[0, 0, 0], size=[.4, .4, .2])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="LeftFoot")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="RightFoot")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="Torso")

        pyrosim.Send_Hidden_Neuron(name=3)
        pyrosim.Send_Hidden_Neuron(name=4)
        pyrosim.Send_Hidden_Neuron(name=5)
        pyrosim.Send_Hidden_Neuron(name=6)

        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_Hip")
        pyrosim.Send_Motor_Neuron(name=8, jointName="Hip_LeftFemur")
        pyrosim.Send_Motor_Neuron(name=9, jointName="Hip_RightFemur")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftFemur_LeftTibia")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightFemur_RightTibia")
        pyrosim.Send_Motor_Neuron(name=12, jointName="LeftTibia_LeftFoot")
        pyrosim.Send_Motor_Neuron(name=13, jointName="RightTibia_RightFoot")

        # pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_Hip")
        # pyrosim.Send_Motor_Neuron(name=4, jointName="Hip_LeftFemur")
        # pyrosim.Send_Motor_Neuron(name=5, jointName="Hip_RightFemur")
        # pyrosim.Send_Motor_Neuron(name=6, jointName="LeftFemur_LeftTibia")
        # pyrosim.Send_Motor_Neuron(name=7, jointName="RightFemur_RightTibia")
        # pyrosim.Send_Motor_Neuron(name=8, jointName="LeftTibia_LeftFoot")
        # pyrosim.Send_Motor_Neuron(name=9, jointName="RightTibia_RightFoot")

        # connect sensors to hidden layer
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numHiddenNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + c.numSensorNeurons, weight=self.sensor_to_hidden_weights[currentRow][currentColumn])

        # connect hidden layer to motors
        for currentRow in range(c.numHiddenNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow + c.numSensorNeurons,
                                     targetNeuronName=currentColumn + c.numSensorNeurons + c.numHiddenNeurons, weight=self.hidden_to_motor_weights[currentRow][currentColumn])

        # for currentRow in range(c.numSensorNeurons):
        #     for currentColumn in range(c.numMotorNeurons):
        #         pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn +
        #                              c.numSensorNeurons, weight=self.weights[currentRow][currentColumn])
        # End pyrosim
        pyrosim.End()

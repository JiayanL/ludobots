import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from link import LINK


class SOLUTION():
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        # random sensors
        self.link_count = random.randint(1, 15)

        percent = random.randint(1, self.link_count)
        nums = percent * [1] + (self.link_count - percent) * [0]
        random.shuffle(nums)
        self.sensor_list = nums

        self.sensor_list = nums
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

        pyrosim.Send_Cube(name="Block", pos=[
                          0, 20, 1], size=[4, 3, 1], mass=1000)

        # closes the file
        pyrosim.End()

    def Create_Body(self):
        """
        Snake Study
        pyrosim.Send_Cube(name="Body0", pos=[0, 0, .5], size=[
                          1, 1, 1], colorString="1.0 0 0 1.0", colorName="Red")
        pyrosim.Send_Joint(name="Body0_Body1", parent="Body0", child="Body1", type="revolute", position=[.5, 0, .5], jointAxis="0 0 1")

        pyrosim.Send_Cube(name="Body1", pos=[.5, 0, 0], size=[1, 2, .5], colorString="1.0 0 0 1.0", colorName="Red")
        pyrosim.Send_Joint(name="Body1_Body2", parent="Body1", child="Body2", type="revolute", position=[1, 0, 0], jointAxis="0 0 1")

        pyrosim.Send_Cube(name="Body2", pos=[1, 0, 0], size=[2, 1, .5], colorString="1.0 0 0 1.0", colorName="Red")

        pyrosim.End()
        return
        """
        dimension = random.randint(2, 3)

        pyrosim.Start_URDF("body.urdf")

        for link in range(0, self.link_count):
            cLink = LINK(link, dimension)

            if self.sensor_list[cLink.id] == 1:
                colorString = "0 1.0 0 1.0"
                colorName = "Green"
            else:
                colorString = "0 0 1.0 1.0"
                colorName = "Blue"

            # Create the link
            pyrosim.Send_Cube(name=cLink.parent,
                              pos=[cLink.Pos["x"], cLink.Pos["y"], cLink.Pos["z"]],
                              size=[cLink.Size["length"],
                                    cLink.Size["width"], cLink.Size["height"]],
                              colorString=colorString,
                              colorName=colorName)

            # Create first joint
            if cLink.id == 0:
                pyrosim.Send_Joint(name=f"{cLink.parent}_{cLink.child}",
                                   parent=cLink.parent,
                                   child=cLink.child,
                                   type=cLink.jointType,
                                   position=[cLink.Size["length"] / 2,
                                             0, cLink.Size["height"] / 2],
                                   jointAxis=cLink.jointAxis)

            # Create second joint
            elif cLink.id < self.link_count - 1:
                pyrosim.Send_Joint(name=f"{cLink.parent}_{cLink.child}",
                                   parent=cLink.parent, child=cLink.child,
                                   type=cLink.jointType,
                                   position=[cLink.Size["length"], 0, 0],
                                   jointAxis=cLink.jointAxis)

            # Create legs (if they exist)

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensor_count = 0
        for link in range(0, self.link_count):
            if self.sensor_list[link] == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensor_count, linkName="Body" + str(link))
                sensor_count += 1

        motor_count = 0
        for link in range(0, self.link_count):
            if link < self.link_count - 1:
                pyrosim.Send_Motor_Neuron(
                    name=sensor_count + motor_count, jointName="Body" + str(link) + "_Body" + str(link+1))
                motor_count += 1

        # connect sensors to motors
        for sensor in range(0, sensor_count):
            for motor in range(0, motor_count):
                pyrosim.Send_Synapse(
                    sourceNeuronName=sensor, targetNeuronName=motor + sensor_count, weight=random.uniform(-1, 1))

        pyrosim.End()

import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from link import LINK
from leg import Leg


class SOLUTION():
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.idToLink = {}

        # ------------------------- Attributes of Snake Size ------------------------- #
        self.linkCount = random.randint(c.minLinks, c.maxLinks)
        self.legCount = 0
        # self.legCount, self.legExists, self.dimension = self.Set_Legs(self.linkCount)
        self.legExists = self.Set_Legs()

        # place my sensors
        percent = random.randint(1, self.linkCount)
        nums = percent * [1] + (self.linkCount - percent) * [0]
        random.shuffle(nums)
        self.sensor_list = nums

        # ---------------------------------- Weights --------------------------------- #
        self.sensor_to_hidden_weights = np.random.rand(
            c.numSensorNeurons, c.numHiddenNeurons)
        self.sensor_to_hidden_weights = self.sensor_to_hidden_weights * 2 - 1

        self.hidden_to_motor_weights = np.random.rand(
            c.numHiddenNeurons, c.numMotorNeurons)
        self.hidden_to_motor_weights = self.hidden_to_motor_weights * 2 - 1

        self.weights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

    def Set_Legs(self):
        legCount = random.randint(0, self.linkCount)
        legExists = legCount * [1] + (self.linkCount - legCount) * [0]
        random.shuffle(legExists)
        return legExists

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
        legCount = 0
        pyrosim.Start_URDF("body.urdf")

        for link in range(0, self.linkCount):
            cLink = LINK(link)
            self.idToLink[cLink.id] = cLink

            # ----------------------------------- Body ----------------------------------- #
            # Link
            pyrosim.Send_Cube(name=cLink.parent,
                              pos=[cLink.Pos["x"], cLink.Pos["y"], cLink.Pos["z"]],
                              size=[cLink.Size["length"],
                                    cLink.Size["width"], cLink.Size["height"]],
                              colorString=cLink.colorString,
                              colorName=cLink.colorName)

            # First joint (Absolute)
            if cLink.id == 0 and self.linkCount > 1:
                pyrosim.Send_Joint(name=f"{cLink.parent}_{cLink.child}",
                                   parent=cLink.parent,
                                   child=cLink.child,
                                   type=cLink.jointType,
                                   position=[cLink.Size["length"] / 2,
                                             0, cLink.Size["height"] / 2 + 2],
                                   jointAxis=cLink.jointAxis)

            # All other joints (Relative)
            elif cLink.id < self.linkCount - 1:
                pyrosim.Send_Joint(name=f"{cLink.parent}_{cLink.child}",
                                   parent=cLink.parent, child=cLink.child,
                                   type=cLink.jointType,
                                   position=[cLink.Size["length"], 0, 0],
                                   jointAxis=cLink.jointAxis)

            # ----------------------------------- Legs ----------------------------------- #
            if (cLink.id != 0):

                # Left Side - Leg
                if True or cLink.leftLimbs > 0:
                    legId = self.linkCount + legCount
                    leftLeg = Leg(cLink, legId, "left")
                    self.idToLink[leftLeg.id] = leftLeg
                    legCount += 1
                    pyrosim.Send_Joint(name=f"{cLink.parent}_{leftLeg.name}",
                                       parent=cLink.parent, child=leftLeg.name,
                                       type=leftLeg.jointType,
                                       position=[
                                           leftLeg.jointPos.x, leftLeg.jointPos.y, leftLeg.jointPos.z],
                                       jointAxis=leftLeg.jointAxis)

                    pyrosim.Send_Cube(name=leftLeg.name,
                                      pos=[leftLeg.linkPos.x,
                                           leftLeg.linkPos.y, leftLeg.linkPos.z],
                                      size=[
                                          leftLeg.Size.length, leftLeg.Size.width, leftLeg.Size.height],
                                      colorString=leftLeg.colorString, colorName=leftLeg.colorName)

                    # Left Side - Foot
                    if True or cLink.leftLimbs == 2:
                        footId = self.linkCount + legCount
                        leftFoot = Leg(leftLeg, footId, "left-down")
                        self.idToLink[leftFoot.id] = leftFoot
                        legCount += 1

                        pyrosim.Send_Joint(name=f"{leftLeg.name}_{leftFoot.name}",
                                           parent=leftLeg.name, child=leftFoot.name,
                                                type=leftFoot.jointType,
                                                position=[
                                                    leftFoot.jointPos.x, leftFoot.jointPos.y, leftFoot.jointPos.z],
                                                jointAxis=cLink.jointAxis)

                        pyrosim.Send_Cube(name=leftFoot.name,
                                          pos=[
                                              leftFoot.linkPos.x, leftFoot.linkPos.y, leftFoot.linkPos.z],
                                          size=[
                                              leftFoot.Size.length, leftFoot.Size.width, leftFoot.Size.height],
                                          colorString=leftFoot.colorString, colorName=leftFoot.colorName)

                # --------------------------------- Right Leg -------------------------------- #
                # Right Leg
                if True or cLink.rightLimbs > 0:
                    legId = self.linkCount + legCount
                    rightLeg = Leg(cLink, legId, "right")
                    legCount += 1
                    self.idToLink[rightLeg.id] = rightLeg

                    pyrosim.Send_Joint(name=f"{cLink.parent}_{rightLeg.name}",
                                       parent=cLink.parent,
                                       child=rightLeg.name,
                                       type=rightLeg.jointType,
                                       position=[rightLeg.jointPos.x,
                                                 rightLeg.jointPos.y,
                                                 rightLeg.jointPos.z],
                                       jointAxis=rightLeg.jointAxis)

                    pyrosim.Send_Cube(name=rightLeg.name,
                                      pos=[rightLeg.linkPos.x,
                                           rightLeg.linkPos.y,
                                           rightLeg.linkPos.z],
                                      size=[
                                          rightLeg.Size.length,
                                          rightLeg.Size.width,
                                          rightLeg.Size.height],
                                      colorString=rightLeg.colorString,
                                      colorName=rightLeg.colorName)

                    # Right Foot
                    if True or cLink.rightLimbs == 2:
                        footId = self.linkCount + legCount
                        rightFoot = Leg(rightLeg, footId, "right-down")
                        legCount += 1
                        self.idToLink[rightFoot.id] = rightFoot

                        pyrosim.Send_Joint(name=f"{rightLeg.name}_{rightFoot.name}",
                                           parent=rightLeg.name, child=rightFoot.name,
                                                type=rightFoot.jointType,
                                                position=[
                                                    rightFoot.jointPos.x, rightFoot.jointPos.y, rightFoot.jointPos.z],
                                                jointAxis=rightFoot.jointAxis)

                        pyrosim.Send_Cube(name=rightFoot.name,
                                          pos=[
                                              rightFoot.linkPos.x, rightFoot.linkPos.y, rightFoot.linkPos.z],
                                          size=[
                                              rightFoot.Size.length, rightFoot.Size.width, rightFoot.Size.height],
                                          colorString=rightFoot.colorString,
                                          colorName=rightFoot.colorName)
            self.legCount = legCount - 1
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")\

        # Plumbing to test body shape
        totalLinks = self.linkCount + self.legCount
        sensor_count = 0

        for link in range(0, totalLinks):
            currLink = self.idToLink[link]
            if currLink.sensorExists == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensor_count, linkName="Body" + str(currLink.id))
                sensor_count += 1

        # motor_count = 0
        # # start by connecting body
        # for link in range(0, self.linkCount):
        #     if link < self.linkCount - 1:
        #         pyrosim.Send_Motor_Neuron(
        #             name=sensor_count + motor_count, jointName="Body" + str(link) + "_Body" + str(link+1))
        #         motor_count += 1

        # # then go for the legs
        # for link in range(self.linkCount, totalLinks):
        #     currLink = self.idToLink[link]
        #     if isinstance(currLink.parent.parent, str):
        #         parent = currLink.parent.parent
        #     else:
        #         parent = currLink.parent.name

        #     pyrosim.Send_Motor_Neuron(
        #         name=sensor_count+motor_count, jointName=f"{parent}_{currLink.name}")
        #     print(f"{parent}_{currLink.name}")
        #     motor_count += 1

        # connect sensors to motors
        # for sensor in range(0, sensor_count):
        #     for motor in range(0, motor_count):
        #         pyrosim.Send_Synapse(
        #             sourceNeuronName=sensor, targetNeuronName=motor + sensor_count, weight=random.uniform(-1, 1))
        pyrosim.End()

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
        self.linkCount = random.randint(1, c.maxLinks)
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
            if cLink.id == 0:
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
            if (cLink.id != 0 and (True or cLink.legExists)):
                if True or cLink.leftLimbs > 0:
                    legId = self.linkCount + legCount
                    leftLeg = Leg(cLink, legId, "left")
                    # Left leg

                    legName = f"Body{legId}"

                    legLength = random.uniform(0, cLink.Size["length"])
                    legWidth = random.uniform(0, 2)
                    legHeight = random.uniform(0, 2)

                    pyrosim.Send_Joint(name=f"{cLink.parent}_{leftLeg.name}",
                                       parent=cLink.parent, child=leftLeg.name,
                                       type=leftLeg.jointType,
                                       position=[leftLeg.jointPos.x, leftLeg.jointPos.y, leftLeg.jointPos.z], jointAxis=leftLeg.jointAxis)

                    pyrosim.Send_Cube(name=leftLeg.name,
                                      pos=[leftLeg.linkPos.x,
                                           leftLeg.linkPos.y, leftLeg.linkPos.z],
                                      size=[
                                          leftLeg.Size.length, leftLeg.Size.width, leftLeg.Size.height],
                                      colorString=leftLeg.colorString, colorName=leftLeg.colorName)
                    legCount += 1

                    # Left foot
                    if True or cLink.leftLimbs == 2:
                        footID = self.linkCount + legCount
                        footName = f"Body{footID}"
                        footLength = random.uniform(0, cLink.Size["length"])
                        pyrosim.Send_Joint(name=f"{leftLeg.name}_{footName}",
                                           parent=leftLeg.name, child=footName,
                                                type=cLink.jointType,
                                                position=[0, leftLeg.Size.width, -leftLeg.Size.height/2], jointAxis=cLink.jointAxis)
                        pyrosim.Send_Cube(name=footName,
                                          pos=[0, 0, -.5],
                                          size=[footLength, 1, 1],
                                          colorString=cLink.colorString, colorName=cLink.colorName)
                        legCount += 1

                # --------------------------------- Right Leg -------------------------------- #
                # Right Leg
                if cLink.rightLimbs > 0:
                    legId = self.linkCount + legCount
                    legName = f"Body{legId}"
                    pyrosim.Send_Joint(name=f"{cLink.parent}_{legName}",
                                       parent=cLink.parent, child=legName,
                                       type=cLink.jointType,
                                       position=[cLink.Size["length"]/2, -cLink.Size["width"]/2, 0], jointAxis=cLink.jointAxis)
                    pyrosim.Send_Cube(name=legName,
                                      pos=[0, -.5, 0],
                                      size=[random.uniform(
                                          0, cLink.Size["length"]), 1, 1],
                                      colorString=cLink.colorString, colorName=cLink.colorName)
                    legCount += 1

                    # Right Foot
                    if cLink.rightLimbs == 2:
                        footId = self.linkCount + legCount
                        footName = f"Body{footId}"
                        pyrosim.Send_Joint(name=f"{legName}_{footName}",
                                           parent=legName, child=footName,
                                                type=cLink.jointType,
                                                position=[0, -1, -.5], jointAxis=cLink.jointAxis)
                        pyrosim.Send_Cube(name=footName,
                                          pos=[0, 0, -.5],
                                          size=[random.uniform(
                                              0, cLink.Size["length"]), 1, 1],
                                          colorString=cLink.colorString, colorName=cLink.colorName)
                        legCount += 1

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")\

        # Plumbing to test body shape

        sensor_count = 0
        for link in range(0, self.linkCount):
            if self.sensor_list[link] == 1:
                pyrosim.Send_Sensor_Neuron(
                    name=sensor_count, linkName="Body" + str(link))
                sensor_count += 1

        # motor_count = 0
        # for link in range(0, self.linkCount):
        #     if link < self.linkCount - 1:
        #         pyrosim.Send_Motor_Neuron(
        #             name=sensor_count + motor_count, jointName="Body" + str(link) + "_Body" + str(link+1))
        #         motor_count += 1

        # # connect sensors to motors
        # for sensor in range(0, sensor_count):
        #     for motor in range(0, motor_count):
        #         pyrosim.Send_Synapse(
        #             sourceNeuronName=sensor, targetNeuronName=motor + sensor_count, weight=random.uniform(-1, 1))

        pyrosim.End()

import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c
from link import LINK
from leg import Leg
from collections import defaultdict
from linkjoint import JOINT


class SOLUTION():
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.idToLink = {}
        self.linksToJoint = {}

        # -------------------------- Generate Creature Body -------------------------- #
        self.Create_Body_Plan()

        # ---------------------------------- Weights --------------------------------- #
        # self.sensor_to_hidden_weights = np.random.rand(
        #     c.numSensorNeurons, c.numHiddenNeurons)
        # self.sensor_to_hidden_weights = self.sensor_to_hidden_weights * 2 - 1

        # self.hidden_to_motor_weights = np.random.rand(
        #     c.numHiddenNeurons, c.numMotorNeurons)
        # self.hidden_to_motor_weights = self.hidden_to_motor_weights * 2 - 1

        # self.weights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)
        # self.weights = self.weights * 2 - 1

    def Create_Body_Plan(self):
        self.spineCount = random.randint(c. minLinks, c.maxLinks)
        self.left_legs = self.Random_Placement(0, self.spineCount, "legs")
        self.left_legs[0] = 0
        self.right_legs = self.Random_Placement(0, self.spineCount, "legs")
        self.right_legs[0] = 0

        self.totalLinks = 5 * self.spineCount
        # ----------------------------- Establish Sensors ---------------------------- #
        self.sensor_list = self.Random_Placement(1, self.totalLinks, "sensors")
        self.sensorCount = sum(self.sensor_list)

        # ---------------------- Design Body (Links and Joints) ---------------------- #
        legCount = 0
        jointCount = 0

        for id in range(self.spineCount):
            # Spine link
            cLink = LINK(id, self.sensor_list[id])
            self.idToLink[id] = cLink

            # Create link to next spine
            if cLink.id == 0:
                first = True
            else:
                first = False

            cJoint = JOINT(jointCount, "spine", cLink.parent, cLink.child,
                           cLink.Size["length"], cLink.Size["width"], cLink.Size["height"], first=first,)
            jointCount += 1
            self.linksToJoint[cJoint.jointName] = cJoint

            # make sure I'm not building at the first one
            if cLink.id > 0:
                # create left leg
                legId = self.spineCount + legCount
                leftLeg = Leg(cLink, legId, self.sensor_list[legId], "left")
                self.idToLink[leftLeg.id] = leftLeg
                cJoint = JOINT(jointCount, "left", cLink, leftLeg,
                               leftLeg.Size.length, leftLeg.Size.width, leftLeg.Size.height)
                jointCount += 1
                self.linksToJoint[cJoint.jointName] = cJoint
                legCount += 1

                # create left foot
                footId = self.spineCount + legCount
                leftFoot = Leg(leftLeg, footId,
                               self.sensor_list[footId], "left-down")
                self.idToLink[leftFoot.id] = leftFoot
                cJoint = JOINT(jointCount, "left-down", leftLeg, leftFoot, leftFoot.Size.length,
                               leftFoot.Size.width, leftFoot.Size.height)
                jointCount += 1
                self.linksToJoint[cJoint.jointName] = cJoint
                legCount += 1

                # create right leg
                legId = self.spineCount + legCount
                rightLeg = Leg(cLink, legId, self.sensor_list[legId], "right")
                self.idToLink[rightLeg.id] = rightLeg
                cJoint = JOINT(jointCount, "right", cLink, rightLeg,
                               rightLeg.Size.length, rightLeg.Size.width, rightLeg.Size.height)
                jointCount += 1
                self.linksToJoint[cJoint.jointName] = cJoint
                legCount += 1

                # create right foot
                footId = self.spineCount + legCount
                rightFoot = Leg(rightLeg, footId,
                                self.sensor_list[footId], "right-down")
                self.idToLink[rightFoot.id] = rightFoot
                cJoint = JOINT(jointCount, "right-down", rightLeg, rightFoot, rightFoot.Size.length,
                               rightFoot.Size.width, rightFoot.Size.height)
                jointCount += 1
                self.linksToJoint[cJoint.jointName] = cJoint
                legCount += 1

        self.legCount = legCount - 1

        # ------------------------------ Create weights ------------------------------ #
        # links (potential sensors) --> joints (potential motors)
        self.sensor_to_motor_weights = np.random.rand(
            self.totalLinks, len(self.linksToJoint))
        self.sensor_to_motor_weights = self.sensor_to_motor_weights * 2 - 1

    def Select_Body(self):
        # choose the links and joints I'm going to build
        testing = False
        self.links_to_build = []
        self.joints_to_build = []
        self.items_to_build_in_order = []
        self.sensors_to_build = []

        # traverse along the spine, adding all necessary links and joints
        linkCount = 0
        legCount = 0
        tempLegCount = 0

        if testing:
            print("all links I have stored: " + str(self.linksToJoint.keys()))
            print("spineCount: " + str(self.spineCount))
            print("all the links I have: " + str(self.idToLink.keys()))

        for i in range(self.spineCount):
            cLink = self.idToLink[i]
            cLink.SetTempId(linkCount)
            linkCount += 1

            # self.links_to_build.append(self.idToLink[i])
            if cLink.sensorExists:
                self.sensors_to_build.append(cLink)
            self.links_to_build.append(cLink.tempName)
            self.items_to_build_in_order.append(self.idToLink[i])

            if cLink.id < self.spineCount - 1:
                jointName = f"{cLink.parent}_{cLink.child}"
                cJoint = self.linksToJoint[jointName]
                cJoint.SetTempId(cLink.tempId, cLink.tempChildId)

                # self.joints_to_build.append(cJoint)
                self.joints_to_build.append(cJoint)
                self.items_to_build_in_order.append(cJoint)

            if cLink.id > 0:
                # left legs
                if self.left_legs[i] > 1:
                    leftLeg = self.idToLink[self.spineCount + legCount]
                    leftLeg.SetTempId(
                        cLink.tempId, self.spineCount + tempLegCount)
                    tempLegCount += 1

                    jointName = f"{cLink.name}_{leftLeg.name}"
                    cJoint = self.linksToJoint[jointName]
                    cJoint.SetTempId(cLink.tempId, leftLeg.tempId)

                    self.joints_to_build.append(cJoint)
                    self.items_to_build_in_order.append(
                        self.linksToJoint[jointName])

                    # censors and link
                    if leftLeg.sensorExists:
                        self.sensors_to_build.append(leftLeg)
                    self.links_to_build.append(leftLeg.tempName)
                    self.items_to_build_in_order.append(leftLeg)
                legCount += 1

                if self.left_legs[i] == 2:
                    leftFoot = self.idToLink[self.spineCount + legCount]
                    leftFoot.SetTempId(
                        leftLeg.tempId, self.spineCount + tempLegCount)
                    tempLegCount += 1

                    jointName = f"{leftLeg.name}_{leftFoot.name}"
                    cJoint = self.linksToJoint[jointName]
                    cJoint.SetTempId(leftLeg.tempId, leftFoot.tempId)

                    self.joints_to_build.append(cJoint)
                    self.items_to_build_in_order.append(cJoint)

                    # censors and link
                    if leftFoot.sensorExists:
                        self.sensors_to_build.append(leftFoot)
                    self.links_to_build.append(leftFoot.tempName)
                    self.items_to_build_in_order.append(leftFoot)
                legCount += 1

                if self.right_legs[i] > 1:
                    rightLeg = self.idToLink[self.spineCount + legCount]
                    jointName = f"{cLink.name}_{rightLeg.name}"
                    rightLeg.SetTempId(
                        cLink.tempId, self.spineCount + tempLegCount)

                    tempLegCount += 1

                    cJoint = self.linksToJoint[jointName]
                    cJoint.SetTempId(cLink.tempId, rightLeg.tempId)
                    self.joints_to_build.append(cJoint)
                    self.items_to_build_in_order.append(
                        cJoint)

                    # sensors and link
                    if rightLeg.sensorExists:
                        self.sensors_to_build.append(rightLeg)
                    self.links_to_build.append(rightLeg.tempName)
                    self.items_to_build_in_order.append(rightLeg)
                legCount += 1

                if self.right_legs[i] == 2:
                    rightFoot = self.idToLink[self.spineCount + legCount]
                    rightFoot.SetTempId(
                        rightLeg.tempId, self.spineCount + tempLegCount)
                    jointName = f"{rightLeg.name}_{rightFoot.name}"
                    cJoint = self.linksToJoint[jointName]
                    cJoint.SetTempId(rightLeg.tempId, rightFoot.tempId)

                    tempLegCount += 1

                    self.joints_to_build.append(cJoint)
                    self.items_to_build_in_order.append(
                        self.linksToJoint[jointName])

                    # sensors and link
                    if rightFoot.sensorExists:
                        self.sensors_to_build.append(rightFoot)
                    self.links_to_build.append(rightFoot.tempName)
                    self.items_to_build_in_order.append(rightFoot)
                legCount += 1
        if testing:
            print("left leg placement: " + str(self.left_legs))
            print("right leg placement: " + str(self.right_legs))
            print("links to build: " + str(self.links_to_build))
            print("joints to build: " + str(self.joints_to_build))

    def Random_Placement(self, low, high, type):
        if type == "sensors":
            percent = random.randint(low, high)
            nums = percent * [1] + (high - percent) * [0]
            random.shuffle(nums)

        if type == "legs":
            p_1 = random.randint(low, high)
            p_2 = random.randint(low, high - p_1)
            nums = p_1 * [1] + p_2 * [2] + (high - p_1 - p_2) * [0]
            random.shuffle(nums)

        return nums

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

        # update body (4 options) then update weights (always)

        # mutate body shape

        # swap sensors

        # add link

        # remove link

        try:
            # choose a random sensor
            sensor = random.choice(self.sensors_to_build).id
            # choose a random motor
            motor = random.choice(self.joints_to_build).id

            # and update
            self.sensor_to_motor_weights[sensor][motor] = random.random()*2-1
        except:
            print("update weights invalid")

    def Create_World(self):
        # use pyrosim to Create a link
        # tells pyrosim the name of the file where information about the world should be stored
        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Cube(name="Block", pos=[
                          0, 20, 1], size=[4, 3, 1], mass=1000)

        # closes the file
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        self.Select_Body()
        for entity in self.items_to_build_in_order:
            if isinstance(entity, LINK):
                cLink = entity
                pyrosim.Send_Cube(name=cLink.tempName,
                                  pos=[cLink.Pos["x"],
                                       cLink.Pos["y"], cLink.Pos["z"]],
                                  size=[cLink.Size["length"],
                                        cLink.Size["width"], cLink.Size["height"]],
                                  colorString=cLink.colorString,
                                  colorName=cLink.colorName)
            elif isinstance(entity, Leg):
                cLink = entity
                pyrosim.Send_Cube(name=cLink.tempName,
                                  pos=[cLink.linkPos.x,
                                       cLink.linkPos.y, cLink.linkPos.z],
                                  size=[
                                      cLink.Size.length, cLink.Size.width, cLink.Size.height],
                                  colorString=cLink.colorString, colorName=cLink.colorName)
            elif isinstance(entity, JOINT):
                cJoint = entity
                pyrosim.Send_Joint(name=cJoint.tempJointName,
                                   parent=cJoint.tempParentName, child=cJoint.tempChildName,
                                   type=cJoint.jointType,
                                   position=[
                                       cJoint.x, cJoint.y, cJoint.z],
                                   jointAxis=cJoint.jointAxis)

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        numSensors = len(self.sensors_to_build)
        numMotors = len(self.joints_to_build)

        for i, link in enumerate(self.sensors_to_build):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=link.tempName)

        for i, joint in enumerate(self.joints_to_build):
            pyrosim.Send_Motor_Neuron(
                name=numSensors + i, jointName=joint.tempJointName)

        for sensor_count, sensor in enumerate(self.sensors_to_build):
            for motor_count, motor in enumerate(self.joints_to_build):
                pyrosim.Send_Synapse(
                    sourceNeuronName=sensor_count, targetNeuronName=motor_count + numSensors, weight=self.sensor_to_motor_weights[sensor.id][motor.id])

        pyrosim.End()

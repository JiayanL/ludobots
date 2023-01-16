from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import constants as c


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)

        # loads files like plane.urdf
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # set gravity
        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for i in range(c.steps):
            # c.steps inside the physics world for a small amount
            p.stepSimulation()

            self.robot.Sense(i)
            self.robot.Act(i)

            time.sleep(1/240)

    def __del__(self):
        p.disconnect()

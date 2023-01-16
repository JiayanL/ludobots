import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random

"""
Controlling Virtual Camera
- Hold down control and click and drag
"""

physicsClient = p.connect(p.GUI)

# loads files like plane.urdf
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# set gravity
p.setGravity(0, 0, -9.8)
# add a floor
planeID = p.loadURDF("plane.urdf")

# load robot
robotID = p.loadURDF("body.urdf")
# tells pybullet to read in the world described in box.sdf
p.loadSDF("world.sdf")

# preparation for simulating sensors
pyrosim.Prepare_To_Simulate(robotID)
steps = 1000
backLegSensorValues = np.zeros(steps)
frontLegSensorValues = np.zeros(steps)

# set the target angle
BackLeg_amplitude = np.pi/4
BackLeg_frequency = 5
BackLeg_phaseOffset = np.pi/2

FrontLeg_amplitude = np.pi/3
FrontLeg_frequency = 5
FrontLeg_phaseOffset = 0

BackLeg_targetAngles = np.arange(0, np.pi*2, np.pi*2/steps)
BackLeg_targetAngles = BackLeg_amplitude * \
    np.sin(BackLeg_frequency * (BackLeg_targetAngles + BackLeg_phaseOffset))

FrontLeg_targetAngles = np.arange(0, np.pi*2, np.pi*2/steps)
FrontLeg_targetAngles = FrontLeg_amplitude * \
    np.sin(FrontLeg_frequency * (FrontLeg_targetAngles + FrontLeg_phaseOffset))

# save loop
# run the simulation for 1000 steps
for i in range(steps):
    # steps inside the physics world for a small amount
    p.stepSimulation()

    # create sensors
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(
        "FrontLeg")

    # simulate motors
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotID,
        jointName=b"Torso_BackLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=BackLeg_targetAngles[i],
        maxForce=50)

    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotID,
        jointName=b"Torso_FrontLeg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=FrontLeg_targetAngles[i],
        maxForce=50)
    time.sleep(1/240)

p.disconnect()
np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)

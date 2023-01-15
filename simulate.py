import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

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
steps = 100
backLegSensorValues = np.zeros(steps)
frontLegSensorValues = np.zeros(steps)

# run the simulation for 1000 steps
for i in range(steps):
    # steps inside the physics world for a small amount
    p.stepSimulation()
    # create sensors
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(
        "FrontLeg")
    time.sleep(1/60)
p.disconnect()
np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)

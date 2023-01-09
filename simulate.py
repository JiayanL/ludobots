import pybullet as p
import pybullet_data
import time

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
# tells pybullet to read in the world described in box.sdf
p.loadSDF("boxes.sdf")


# run the simulation for 1000 steps
for i in range(1000):
    # steps inside the physics world for a small amount
    p.stepSimulation()
    time.sleep(1/600)
    print(i)
p.disconnect()

import pybullet as p
import time

"""
Controlling Virtual Camera
- Hold down control and click and drag
"""

physicsClient = p.connect(p.GUI)
# tells pybullet to read in the world described in box.sdf
p.loadSDF("box.sdf")
for i in range(1000):
    # steps inside the physics world for a small amount
    p.stepSimulation()
    time.sleep(1/600)
    print(i)
p.disconnect()

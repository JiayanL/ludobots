import pybullet as p


class WORLD():
    def __init__(self):
        self.planeID = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")

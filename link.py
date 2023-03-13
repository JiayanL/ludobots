import random
from leg import Leg


class Joint():
    def __init__(self, length, height, first=False):
        if first:
            self.x = length / 2
            self.y = 0
            self.z = height / 2 + 2
        else:
            self.x = length
            self.y = 0
            self.z = 0


class LINK():
    def __init__(self, id, sensorExists):
        self.type = "spine"
        self.id = id
        self.display_position = 0
        # Link Info

        self.Size = {
            "length": random.uniform(.1, 1),
            "width": random.uniform(.1, 1),
            "height": random.uniform(.1, 1),
        }

        self.Pos = {
            "y": 0,
            "z": 0 if id > 0 else self.Size["height"] / 2 + 2,
            "x": 0 if id == 0 else self.Size["length"] / 2,
        }

        # Generate Names for Joints
        self.parent = f"Body{str(id)}"
        self.child = f"Body{str(id+1)}"

        # Joint Axis
        jointAxisType = random.randint(1, 2)
        if jointAxisType == 0:
            self.jointAxis = "0 0 1"
        if jointAxisType == 1:
            self.jointAxis = "0 1 0"
        if jointAxisType == 2:
            self.jointAxis = "1 0 0"

        # Joint Type
        jointTypes = ["revolute", "floating",
                      "planar"]
        self.jointType = jointTypes[random.randint(0, 2)]
        self.jointType = "revolute"

        # Joint Position
        if self.id == 0:
            self.jointPosition = Joint(
                self.Size["length"], self.Size["height"], first=True)
        else:
            self.jointPosition = Joint(
                self.Size["length"], self.Size["height"])

        # Create children
        self.legs = []
        self.legExists = random.randint(0, 1)
        if self.legExists == 1:
            pass
            # self.legs = self.Create_Legs(dimension)

        # Sensor and Color
        self.sensorExists = sensorExists
        if self.sensorExists == 1:
            self.colorString = "0 1.0 0 1.0"
            self.colorName = "Green"
        if self.sensorExists == 0:
            self.colorString = "0 0 1.0 1.0"
            self.colorName = "Blue"

        # Appendages
        self.legExists = random.choice([True, False])
        self.leftLimbs = random.randint(0, 2)
        self.rightLimbs = random.randint(0, 2)
